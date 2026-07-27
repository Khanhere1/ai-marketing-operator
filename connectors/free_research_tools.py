"""
Free Research Tools for AI Marketing Operator.

Uses ONLY free, public APIs and web scraping via standard library (urllib).
No paid API keys required. No external dependencies beyond Python stdlib.

Supported Free Data Sources:
  - Reddit Search API (no auth for basic search)
  - Google Ads Transparency Center (public)
  - Meta Ad Library (public, no auth for basic queries)
  - Google Trends (public RSS/widget endpoints)
  - Hacker News / Algolia Search (public)
  - Product Hunt (public, limited)
  - GitHub Search (public, no auth for basic search)
  - Common Crawl / Web Archives (public)
"""

import json
import logging
import urllib.request
import urllib.parse
import urllib.error
import ssl
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from html.parser import HTMLParser

logger = logging.getLogger(__name__)

# Create a permissive SSL context for environments with certificate issues
_SSL_CONTEXT = ssl.create_default_context()
_SSL_CONTEXT.check_hostname = False
_SSL_CONTEXT.verify_mode = ssl.CERT_NONE

# Default timeout for all HTTP requests (seconds)
_TIMEOUT = 15

# Standard user agent to avoid bot-blocking
_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


class _TextExtractor(HTMLParser):
    """Simple HTML-to-text extractor."""

    def __init__(self):
        super().__init__()
        self.result = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            text = data.strip()
            if text:
                self.result.append(text)


def _fetch_json(url: str, headers: Optional[Dict] = None) -> Any:
    """Fetch JSON from a URL using only stdlib."""
    req_headers = {"User-Agent": _USER_AGENT}
    if headers:
        req_headers.update(headers)

    req = urllib.request.Request(url, headers=req_headers)
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT, context=_SSL_CONTEXT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
        logger.warning("Failed to fetch %s: %s", url, str(e))
        return None


def _fetch_text(url: str, headers: Optional[Dict] = None) -> Optional[str]:
    """Fetch raw text from a URL using only stdlib."""
    req_headers = {"User-Agent": _USER_AGENT}
    if headers:
        req_headers.update(headers)

    req = urllib.request.Request(url, headers=req_headers)
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT, context=_SSL_CONTEXT) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        logger.warning("Failed to fetch %s: %s", url, str(e))
        return None


def _html_to_text(html: str) -> str:
    """Extract plain text from HTML."""
    parser = _TextExtractor()
    parser.feed(html)
    return " ".join(parser.result)


# ─────────────────────────────────────────────────────────────────────
# Reddit Search (Free, No Auth)
# ─────────────────────────────────────────────────────────────────────

def search_reddit(
    query: str,
    subreddit: Optional[str] = None,
    sort: str = "relevance",
    time_filter: str = "month",
    limit: int = 15,
) -> List[Dict[str, Any]]:
    """
    Search Reddit using the public JSON API (no auth required).

    Uses old.reddit.com endpoint which is more permissive with JSON requests.

    Args:
        query: Search keywords
        subreddit: Optional specific subreddit (e.g., "marketing")
        sort: relevance, hot, top, new, comments
        time_filter: hour, day, week, month, year, all
        limit: Max results (max 100)

    Returns:
        List of evidence items with titles, URLs, scores, and comments.
    """
    params = urllib.parse.urlencode({
        "q": query,
        "sort": sort,
        "t": time_filter,
        "limit": min(limit, 100),
        "restrict_sr": "on" if subreddit else "off",
    })

    if subreddit:
        url = f"https://old.reddit.com/r/{subreddit}/search.json?{params}"
    else:
        url = f"https://old.reddit.com/search.json?{params}"

    data = _fetch_json(url)
    if not data or "data" not in data:
        return []

    results = []
    for child in data["data"].get("children", []):
        post = child.get("data", {})
        results.append({
            "source": "Reddit",
            "source_url": f"https://www.reddit.com{post.get('permalink', '')}",
            "title": post.get("title", ""),
            "text": post.get("selftext", "")[:500],
            "author": post.get("author", "unknown"),
            "subreddit": post.get("subreddit", ""),
            "score": post.get("score", 0),
            "num_comments": post.get("num_comments", 0),
            "created_utc": datetime.fromtimestamp(
                post.get("created_utc", 0), tz=timezone.utc
            ).isoformat(),
            "data_source": "reddit_public_api",
        })

    return results


# ─────────────────────────────────────────────────────────────────────
# Hacker News / Algolia Search (Free, No Auth)
# ─────────────────────────────────────────────────────────────────────

def search_hacker_news(
    query: str,
    limit: int = 15,
    sort_by: str = "relevance",
) -> List[Dict[str, Any]]:
    """
    Search Hacker News via the free Algolia API.

    Args:
        query: Search keywords
        limit: Max results
        sort_by: "relevance" or "date"

    Returns:
        List of evidence items from HN discussions.
    """
    endpoint = "search" if sort_by == "relevance" else "search_by_date"
    params = urllib.parse.urlencode({
        "query": query,
        "tags": "story",
        "hitsPerPage": min(limit, 50),
    })
    url = f"https://hn.algolia.com/api/v1/{endpoint}?{params}"

    data = _fetch_json(url)
    if not data or "hits" not in data:
        return []

    results = []
    for hit in data["hits"]:
        results.append({
            "source": "Hacker News",
            "source_url": f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
            "title": hit.get("title", ""),
            "author": hit.get("author", "unknown"),
            "points": hit.get("points", 0),
            "num_comments": hit.get("num_comments", 0),
            "created_at": hit.get("created_at", ""),
            "external_url": hit.get("url", ""),
            "data_source": "hackernews_algolia_api",
        })

    return results


# ─────────────────────────────────────────────────────────────────────
# GitHub Search (Free, No Auth — rate limited to 10 req/min)
# ─────────────────────────────────────────────────────────────────────

def search_github(
    query: str,
    search_type: str = "repositories",
    sort: str = "stars",
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Search GitHub using the public API (no auth, rate-limited).

    Args:
        query: Search keywords
        search_type: "repositories", "code", "issues"
        sort: "stars", "forks", "updated", "best-match"
        limit: Max results

    Returns:
        List of evidence items from GitHub search.
    """
    params = urllib.parse.urlencode({
        "q": query,
        "sort": sort,
        "per_page": min(limit, 30),
    })
    url = f"https://api.github.com/search/{search_type}?{params}"

    data = _fetch_json(url, headers={"Accept": "application/vnd.github.v3+json"})
    if not data or "items" not in data:
        return []

    results = []
    for item in data["items"]:
        results.append({
            "source": "GitHub",
            "source_url": item.get("html_url", ""),
            "title": item.get("full_name", item.get("name", "")),
            "description": (item.get("description") or "")[:300],
            "stars": item.get("stargazers_count", 0),
            "forks": item.get("forks_count", 0),
            "language": item.get("language", ""),
            "updated_at": item.get("updated_at", ""),
            "data_source": "github_public_api",
        })

    return results


# ─────────────────────────────────────────────────────────────────────
# Google Ads Transparency Center (Free, Public)
# ─────────────────────────────────────────────────────────────────────

def get_google_ads_transparency_url(advertiser_name: str) -> str:
    """
    Generate the Google Ads Transparency Center URL for a given advertiser.
    The Antigravity agent can use ego-browser to visit this page and extract
    active ad creatives.

    This is a URL generator — actual scraping should be done via ego-browser
    since the page requires JavaScript rendering.
    """
    encoded = urllib.parse.quote_plus(advertiser_name)
    return f"https://adstransparency.google.com/?search_type=3&query={encoded}"


# ─────────────────────────────────────────────────────────────────────
# Meta Ad Library (Free, Public)
# ─────────────────────────────────────────────────────────────────────

def get_meta_ad_library_url(
    query: str,
    country: str = "US",
    ad_type: str = "all",
) -> str:
    """
    Generate the Meta Ad Library URL for research.
    The Antigravity agent can use ego-browser to browse competitor ads.

    Args:
        query: Advertiser name or keyword
        country: Country code (US, GB, IN, etc.)
        ad_type: "all", "political_and_issue_ads"
    """
    params = urllib.parse.urlencode({
        "ad_type": ad_type,
        "country": country,
        "q": query,
        "search_type": "keyword_unordered",
        "media_type": "all",
    })
    return f"https://www.facebook.com/ads/library/?{params}"


# ─────────────────────────────────────────────────────────────────────
# Google Trends (Free, Public — via RSS/Explore widget)
# ─────────────────────────────────────────────────────────────────────

def get_google_trends_url(keyword: str, geo: str = "US", timeframe: str = "today 3-m") -> str:
    """
    Generate Google Trends explore URL for the Antigravity agent to visit.

    Args:
        keyword: Search keyword
        geo: Country code
        timeframe: "now 7-d", "today 1-m", "today 3-m", "today 12-m"
    """
    params = urllib.parse.urlencode({
        "q": keyword,
        "geo": geo,
        "date": timeframe,
    })
    return f"https://trends.google.com/trends/explore?{params}"


def get_trending_searches(geo: str = "US") -> List[Dict[str, Any]]:
    """
    Fetch current trending searches from Google Trends daily trends API.
    """
    url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={geo}"
    xml_text = _fetch_text(url)
    if not xml_text:
        return []

    # Simple XML parsing for trending items
    results = []
    import re
    titles = re.findall(r"<title>(.+?)</title>", xml_text)
    traffic = re.findall(r"<ht:approx_traffic>(.+?)</ht:approx_traffic>", xml_text)

    for i, title in enumerate(titles[1:], 0):  # Skip RSS feed title
        results.append({
            "source": "Google Trends",
            "source_url": f"https://trends.google.com/trends/explore?q={urllib.parse.quote_plus(title)}&geo={geo}",
            "title": title,
            "approximate_traffic": traffic[i] if i < len(traffic) else "unknown",
            "data_source": "google_trends_rss",
        })

    return results[:15]


# ─────────────────────────────────────────────────────────────────────
# Product Hunt (Free, Public)
# ─────────────────────────────────────────────────────────────────────

def get_product_hunt_search_url(query: str) -> str:
    """Generate Product Hunt search URL for browser-based research."""
    return f"https://www.producthunt.com/search?q={urllib.parse.quote_plus(query)}"


# ─────────────────────────────────────────────────────────────────────
# Free Review Platforms
# ─────────────────────────────────────────────────────────────────────

def get_review_platform_urls(product_name: str) -> Dict[str, str]:
    """
    Generate URLs for free review platforms where the Antigravity agent
    can research product reviews and competitor sentiment.
    """
    encoded = urllib.parse.quote_plus(product_name)
    return {
        "G2": f"https://www.g2.com/search?utf8=%E2%9C%93&query={encoded}",
        "Capterra": f"https://www.capterra.com/search/?query={encoded}",
        "TrustPilot": f"https://www.trustpilot.com/search?query={encoded}",
        "Product Hunt": f"https://www.producthunt.com/search?q={encoded}",
        "AlternativeTo": f"https://alternativeto.net/browse/search/?q={encoded}",
    }


# ─────────────────────────────────────────────────────────────────────
# Combined Intelligence Gatherer
# ─────────────────────────────────────────────────────────────────────

def gather_free_intelligence(
    query: str,
    company_name: Optional[str] = None,
    platforms: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Gather competitive intelligence using ALL free data sources.
    No API keys required.

    Args:
        query: Primary search query (product/company/keyword)
        company_name: Optional company name for ad library lookups
        platforms: Optional list of platforms to search.
                   Default: ["reddit", "hackernews", "github"]

    Returns:
        Consolidated intelligence package with evidence items from
        all available free sources.
    """
    target_platforms = platforms or ["reddit", "hackernews", "github"]
    target = company_name or query

    results = {
        "query": query,
        "company_name": company_name,
        "gathered_at": datetime.now(timezone.utc).isoformat(),
        "data_source": "free_public_apis",
        "evidence_items": [],
        "browser_research_urls": {},
        "errors": [],
    }

    # 1. Reddit search
    if "reddit" in target_platforms:
        try:
            reddit_results = search_reddit(query, limit=10)
            results["evidence_items"].extend(reddit_results)
            logger.info("Reddit: found %d results", len(reddit_results))
        except Exception as e:
            results["errors"].append(f"Reddit search failed: {str(e)}")

    # 2. Hacker News search
    if "hackernews" in target_platforms:
        try:
            hn_results = search_hacker_news(query, limit=10)
            results["evidence_items"].extend(hn_results)
            logger.info("Hacker News: found %d results", len(hn_results))
        except Exception as e:
            results["errors"].append(f"Hacker News search failed: {str(e)}")

    # 3. GitHub search
    if "github" in target_platforms:
        try:
            gh_results = search_github(query, limit=5)
            results["evidence_items"].extend(gh_results)
            logger.info("GitHub: found %d results", len(gh_results))
        except Exception as e:
            results["errors"].append(f"GitHub search failed: {str(e)}")

    # 4. Browser-based research URLs (for ego-browser or read_url_content)
    results["browser_research_urls"] = {
        "google_ads_transparency": get_google_ads_transparency_url(target),
        "meta_ad_library": get_meta_ad_library_url(target),
        "google_trends": get_google_trends_url(query),
        "product_hunt": get_product_hunt_search_url(target),
        **get_review_platform_urls(target),
    }

    # 5. Google Trends trending searches
    try:
        trending = get_trending_searches()
        if trending:
            results["trending_searches"] = trending[:5]
    except Exception as e:
        results["errors"].append(f"Google Trends failed: {str(e)}")

    return results


# ─────────────────────────────────────────────────────────────────────
# CLI Entry Point for Testing
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "AI marketing automation"

    print(f"\n🔍 Gathering free intelligence for: '{query}'\n")
    print("=" * 60)

    results = gather_free_intelligence(query, company_name=query)

    print(f"\n📊 Evidence Items Found: {len(results['evidence_items'])}")
    print(f"🔗 Browser Research URLs: {len(results['browser_research_urls'])}")

    if results["errors"]:
        print(f"\n⚠️ Errors: {len(results['errors'])}")
        for err in results["errors"]:
            print(f"  - {err}")

    print("\n📋 Evidence Items:")
    for item in results["evidence_items"][:5]:
        print(f"\n  [{item['source']}] {item.get('title', 'Untitled')}")
        print(f"  URL: {item.get('source_url', 'N/A')}")
        if item.get("score"):
            print(f"  Score: {item['score']}")

    print("\n🌐 Browser Research URLs:")
    for name, url in results["browser_research_urls"].items():
        print(f"  {name}: {url}")

    print("\n" + "=" * 60)
    print("✅ Free intelligence gathering complete!")
