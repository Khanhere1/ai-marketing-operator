"""
Agent-Reach Adapter for AI Marketing Operator Intelligence Plane.

Integrates Agent-Reach (zero-API-fee social & platform scraping) directly
into the AI Marketing Operator framework for advanced market research, 
competitor intelligence, and Voice of Customer (VoC) extraction.

IMPORTANT: This adapter NO LONGER silently falls back to mock data.
If Agent-Reach CLI is unavailable or fails, it raises AgentReachUnavailableError
so the calling pipeline can decide how to handle the failure explicitly.
"""

import sys
import os
import json
import logging
import subprocess
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Add embedded Agent-Reach to sys.path
AGENT_REACH_DIR = os.path.join(os.path.dirname(__file__), "agent-reach")
if AGENT_REACH_DIR not in sys.path:
    sys.path.insert(0, AGENT_REACH_DIR)

# Configurable timeout via environment variable (default: 30 seconds)
AGENT_REACH_TIMEOUT = int(os.environ.get("AGENT_REACH_TIMEOUT_SECONDS", "30"))


class AgentReachUnavailableError(Exception):
    """
    Raised when Agent-Reach CLI is not installed, not configured, 
    or fails to execute. The pipeline MUST handle this explicitly
    instead of silently degrading to mock data.
    """
    pass


class AgentReachExecutionError(Exception):
    """Raised when Agent-Reach CLI returns a non-zero exit code."""
    pass


class AgentReachAdapter:
    """
    Adapter bridging Agent-Reach multi-platform search capabilities
    into the AI Marketing Operator Intelligence Plane.

    Data Provenance:
        Every evidence item returned by this adapter includes a 
        `data_source` field with one of:
        - "agent_reach_live"  — Real scraped data from platform CLI
        - "agent_reach_error" — CLI execution failed (never silent)
    """

    SUPPORTED_PLATFORMS = [
        "twitter", "reddit", "youtube", "github", "bilibili", "xiaohongshu"
    ]

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.join(AGENT_REACH_DIR, "config")

    @classmethod
    def is_available(cls) -> bool:
        """
        Check if Agent-Reach CLI is installed and accessible.
        Returns True if the CLI can be invoked, False otherwise.
        """
        try:
            result = subprocess.run(
                [sys.executable, "-m", "agent_reach.cli", "--help"],
                cwd=AGENT_REACH_DIR,
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            return False

    def search_competitor_mentions(
        self,
        keyword: str,
        platforms: Optional[List[str]] = None,
        max_results: int = 20,
    ) -> Dict[str, Any]:
        """
        Scrape competitor mentions, ad reactions, and brand discussions 
        across social platforms.

        Raises:
            AgentReachUnavailableError: If CLI is not available.
            AgentReachExecutionError: If CLI returns non-zero exit code.
        """
        if not self.is_available():
            raise AgentReachUnavailableError(
                "Agent-Reach CLI is not installed or not accessible. "
                "Install it via: cd connectors/agent-reach && pip install -e . "
                "The pipeline should fall back to web search tools instead of mock data."
            )

        target_platforms = platforms or ["twitter", "reddit", "youtube"]
        results = {
            "keyword": keyword,
            "searched_at": datetime.now(timezone.utc).isoformat(),
            "data_source": "agent_reach_live",
            "platforms": {},
        }

        errors = []
        for platform in target_platforms:
            if platform.lower() in self.SUPPORTED_PLATFORMS:
                try:
                    platform_data = self._execute_platform_search(
                        platform.lower(), keyword, max_results
                    )
                    results["platforms"][platform.lower()] = platform_data
                except AgentReachExecutionError as e:
                    logger.warning(
                        "Agent-Reach search failed for platform '%s': %s",
                        platform, str(e),
                    )
                    errors.append({"platform": platform, "error": str(e)})

        if errors:
            results["errors"] = errors
            if not results["platforms"]:
                raise AgentReachExecutionError(
                    f"All platform searches failed: {errors}"
                )

        return results

    def extract_voc_sentiment(
        self,
        brand_or_topic: str,
        platforms: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Extract Voice of Customer (VoC) pain points, customer complaints, 
        and feature requests. Converts scraped data directly into 
        evidence_item objects adhering to 
        schemas/definitions.schema.json#/$defs/evidence_item.

        Raises:
            AgentReachUnavailableError: If CLI is not available.
            AgentReachExecutionError: If all platform searches fail.
        """
        search_data = self.search_competitor_mentions(brand_or_topic, platforms)
        evidence_items = []

        for platform, items in search_data.get("platforms", {}).items():
            for idx, item in enumerate(items.get("results", [])):
                evidence_items.append({
                    "source": f"Agent-Reach ({platform.upper()})",
                    "source_url": item.get("url", ""),
                    "metric": "customer_sentiment_and_voc",
                    "value": item.get("text", item.get("title", "")),
                    "context": (
                        f"Social mention of '{brand_or_topic}' on {platform}. "
                        f"Author: {item.get('author', 'unknown')}"
                    ),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "data_source": "agent_reach_live",
                    "confidence": item.get("confidence", "medium"),
                })

        return evidence_items

    def discover_market_trends(
        self,
        category_keyword: str,
        platforms: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Discover market trends, emerging competitors, and viral content 
        across target platforms.

        Raises:
            AgentReachUnavailableError: If CLI is not available.
        """
        return self.search_competitor_mentions(
            category_keyword, platforms, max_results=30
        )

    def _execute_platform_search(
        self,
        platform: str,
        query: str,
        max_results: int,
    ) -> Dict[str, Any]:
        """
        Execute Agent-Reach CLI search for a specific platform.

        Raises:
            AgentReachExecutionError: If CLI execution fails or returns 
                non-zero exit code.
        """
        cmd = [
            sys.executable,
            "-m", "agent_reach.cli",
            "search",
            "--platform", platform,
            "--query", query,
            "--limit", str(max_results),
        ]

        try:
            process = subprocess.run(
                cmd,
                cwd=AGENT_REACH_DIR,
                capture_output=True,
                text=True,
                timeout=AGENT_REACH_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            raise AgentReachExecutionError(
                f"Agent-Reach CLI timed out after {AGENT_REACH_TIMEOUT}s "
                f"for platform '{platform}' with query '{query}'. "
                f"Increase timeout via AGENT_REACH_TIMEOUT_SECONDS env var."
            )
        except FileNotFoundError:
            raise AgentReachExecutionError(
                f"Python executable not found: {sys.executable}"
            )

        if process.returncode != 0:
            raise AgentReachExecutionError(
                f"Agent-Reach CLI exited with code {process.returncode} "
                f"for platform '{platform}'. "
                f"stderr: {process.stderr.strip()[:500]}"
            )

        if not process.stdout.strip():
            raise AgentReachExecutionError(
                f"Agent-Reach CLI returned empty output for "
                f"platform '{platform}' with query '{query}'."
            )

        try:
            parsed = json.loads(process.stdout)
            return {"status": "success", "data_source": "agent_reach_live", "results": parsed}
        except json.JSONDecodeError:
            # Return raw text output but mark provenance clearly
            return {
                "status": "raw_output",
                "data_source": "agent_reach_live",
                "results": [{"text": process.stdout.strip()}],
            }


if __name__ == "__main__":
    print("Testing AgentReachAdapter availability...")
    print(f"  CLI Available: {AgentReachAdapter.is_available()}")
    print(f"  Timeout: {AGENT_REACH_TIMEOUT}s")

    if AgentReachAdapter.is_available():
        adapter = AgentReachAdapter()
        try:
            voc = adapter.extract_voc_sentiment(
                "AI Marketing Operator", ["reddit", "twitter"]
            )
            print(f"  Extracted {len(voc)} VoC evidence items:")
            print(json.dumps(voc, indent=2))
        except (AgentReachExecutionError, AgentReachUnavailableError) as e:
            print(f"  Error: {e}")
    else:
        print(
            "  Agent-Reach CLI is NOT available. "
            "The pipeline will use web search tools as fallback."
        )
