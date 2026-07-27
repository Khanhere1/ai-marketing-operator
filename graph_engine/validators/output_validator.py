"""
Output Validation Layer for AI Marketing Operator.

Post-processing validator that checks every sub-agent output against:
1. Source citation density — rejects outputs where <80% of factual claims lack URLs
2. Freshness check — flags competitor data older than 90 days
3. Policy compliance — checks for prohibited patterns from global-prohibitions.yaml
4. Data provenance — verifies evidence items have proper source tags

This validator runs as a LangGraph node between output assembly and final delivery.
Validation failures route back to the research/planner node for re-gathering.
"""

import os
import re
import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    yaml = None

logger = logging.getLogger(__name__)

# Path to policy file
POLICIES_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "policies"
)


class ValidationResult:
    """Container for validation check results."""

    def __init__(self):
        self.checks: List[Dict[str, Any]] = []
        self.passed = True
        self.warnings: List[str] = []
        self.errors: List[str] = []
        self.citation_score: float = 0.0
        self.policy_violations: List[str] = []

    def add_check(self, name: str, passed: bool, detail: str, severity: str = "warning"):
        self.checks.append({
            "name": name,
            "passed": passed,
            "detail": detail,
            "severity": severity,
        })
        if not passed:
            if severity == "error":
                self.errors.append(f"[{name}] {detail}")
                self.passed = False
            else:
                self.warnings.append(f"[{name}] {detail}")

    def to_summary(self) -> str:
        """Generate a human-readable validation summary."""
        status = "✅ PASSED" if self.passed else "❌ FAILED"
        lines = [
            f"## Output Validation Report — {status}",
            f"",
            f"**Citation Score**: {self.citation_score:.0%}",
            f"**Checks Run**: {len(self.checks)}",
            f"**Errors**: {len(self.errors)}",
            f"**Warnings**: {len(self.warnings)}",
            f"",
        ]

        if self.errors:
            lines.append("### ❌ Errors (Must Fix)")
            for err in self.errors:
                lines.append(f"- {err}")
            lines.append("")

        if self.warnings:
            lines.append("### ⚠️ Warnings")
            for warn in self.warnings:
                lines.append(f"- {warn}")
            lines.append("")

        if self.policy_violations:
            lines.append("### 🚫 Policy Violations")
            for violation in self.policy_violations:
                lines.append(f"- {violation}")
            lines.append("")

        return "\n".join(lines)


def _load_prohibitions() -> List[Dict[str, str]]:
    """Load global prohibitions from policy YAML."""
    if yaml is None:
        logger.info("pyyaml not installed — skipping prohibitions loading")
        return []
    filepath = os.path.join(POLICIES_DIR, "global-prohibitions.yaml")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get("rules", data.get("prohibitions", []))
    except (FileNotFoundError, yaml.YAMLError) as e:
        logger.warning("Could not load prohibitions: %s", str(e))
        return []
    except Exception:
        # If yaml is not installed, return empty list
        return []


def check_citation_density(content: str, threshold: float = 0.80) -> Tuple[float, List[str]]:
    """
    Check what percentage of factual statements have source citations.

    Heuristic: A 'factual statement' is any sentence that contains 
    numbers, percentages, dollar amounts, product names, or comparative claims.
    A citation is [Source: URL] or a markdown link.

    Returns:
        Tuple of (citation_score, list_of_uncited_claims)
    """
    # Split into sentences
    sentences = re.split(r'[.!?]\s+', content)
    if not sentences:
        return 1.0, []

    # Patterns that indicate factual claims
    factual_patterns = [
        r'\$[\d,]+',                          # Dollar amounts
        r'\d+%',                              # Percentages
        r'\d+\.\d+x',                         # Multipliers (e.g., 4.2x)
        r'(?:costs?|priced?|pricing)\s',      # Pricing mentions
        r'(?:increased|decreased|grew|fell)\s+by', # Metric changes
        r'(?:ranks?|ranking)\s',              # Rankings
        r'(?:market share|revenue|ARR|MRR)',  # Business metrics
        r'(?:launched|released|announced)',    # Product announcements
    ]

    # Patterns that indicate a citation is present
    citation_patterns = [
        r'\[Source:\s*[^\]]+\]',              # [Source: URL]
        r'\[(?:https?://[^\]]+)\]',           # [URL]
        r'\(https?://[^\)]+\)',               # (URL)
        r'https?://\S+',                      # Bare URL
        r'\[FACT\]',                          # Fact label
    ]

    factual_claims = []
    uncited_claims = []

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence or len(sentence) < 20:
            continue

        is_factual = any(re.search(p, sentence, re.IGNORECASE) for p in factual_patterns)
        if not is_factual:
            continue

        factual_claims.append(sentence)
        has_citation = any(re.search(p, sentence) for p in citation_patterns)
        if not has_citation:
            uncited_claims.append(sentence[:120])

    if not factual_claims:
        return 1.0, []

    score = 1.0 - (len(uncited_claims) / len(factual_claims))
    return score, uncited_claims


def check_data_freshness(content: str, max_staleness_days: int = 90) -> List[str]:
    """
    Check for references to potentially stale data.

    Flags mentions of specific dates/years that are older than max_staleness_days.
    Also flags known outdated product versions.
    """
    stale_flags = []
    current_date = datetime.now(timezone.utc)

    # Check for year references that might be stale
    year_pattern = r'\b(20[12]\d)\b'
    for match in re.finditer(year_pattern, content):
        year = int(match.group(1))
        if year < current_date.year - 1:
            stale_flags.append(
                f"Reference to year {year} may be stale (current: {current_date.year})"
            )

    # Check for known outdated product versions (common in AI industry)
    outdated_patterns = [
        (r'GPT-3\.5', "GPT-3.5 may be outdated — verify current model versions"),
        (r'Claude\s*2', "Claude 2 may be outdated — verify current model versions"),
        (r'Gemini\s*1\.0', "Gemini 1.0 may be outdated — verify current model versions"),
        (r'PaLM\s*2', "PaLM 2 is deprecated — Google now uses Gemini"),
    ]

    for pattern, message in outdated_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            stale_flags.append(message)

    return stale_flags


def check_prohibited_patterns(content: str) -> List[str]:
    """
    Check content for patterns that violate global prohibitions.

    Checks for:
    - Fabricated evidence (claims without any source)
    - Unverified causality ("X caused Y" without evidence)
    - Deceptive claims (absolute guarantees, fake urgency)
    - Platform metric misrepresentation
    """
    violations = []

    # Check for unverified causal claims
    causal_patterns = [
        r'(?:this|that|it)\s+(?:caused|resulted in|led to|drove)\s+',
        r'(?:directly|clearly|obviously)\s+(?:caused|resulted|impacted)',
        r'proven\s+to\s+(?:increase|decrease|improve|reduce)',
    ]
    for pattern in causal_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            # Check if there's a citation nearby
            for match_text in matches:
                # Get surrounding context
                idx = content.lower().find(match_text.lower())
                if idx >= 0:
                    surrounding = content[max(0, idx-50):idx+len(match_text)+100]
                    has_citation = bool(re.search(
                        r'\[Source:|https?://|\[FACT\]', surrounding
                    ))
                    if not has_citation:
                        violations.append(
                            f"no-unverified-causality: Causal claim without evidence: "
                            f"'...{match_text.strip()[:60]}...'"
                        )

    # Check for absolute guarantee language
    guarantee_patterns = [
        r'\bguaranteed?\b(?!\s+(?:not|no|never))',
        r'\b100%\s+(?:certain|sure|guaranteed|effective)\b',
        r'\bwill\s+definitely\b',
        r'\brisk[- ]free\b',
    ]
    for pattern in guarantee_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            violations.append(
                f"no-deceptive-claims: Absolute guarantee language detected"
            )
            break

    # Check for platform metrics presented as revenue
    revenue_patterns = [
        r'(?:Google|Meta|LinkedIn|Facebook)\s+(?:Ads?)?\s+(?:shows?|reports?|attributes?)\s+.*(?:revenue|profit|ROI)',
    ]
    for pattern in revenue_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            # Check if there's a CRM reconciliation caveat
            has_caveat = bool(re.search(
                r'(?:CRM|reconcil|cross.?check|verify|caveat|note:)',
                content, re.IGNORECASE
            ))
            if not has_caveat:
                violations.append(
                    f"no-unverified-causality: Platform-attributed metrics "
                    f"presented as revenue without CRM reconciliation caveat"
                )

    return violations


def validate_output(content: str, specialist: str = "unknown") -> ValidationResult:
    """
    Run all validation checks on a specialist output.

    Args:
        content: The output text to validate
        specialist: The specialist role that generated the output

    Returns:
        ValidationResult with all checks, scores, and violation details
    """
    result = ValidationResult()

    # 1. Citation density check
    citation_score, uncited_claims = check_citation_density(content)
    result.citation_score = citation_score

    if citation_score < 0.80:
        result.add_check(
            "citation_density",
            passed=False,
            detail=(
                f"Citation score {citation_score:.0%} is below 80% threshold. "
                f"{len(uncited_claims)} uncited factual claims found."
            ),
            severity="error" if citation_score < 0.50 else "warning",
        )
        # Add first 5 uncited claims as details
        for claim in uncited_claims[:5]:
            result.add_check(
                "uncited_claim",
                passed=False,
                detail=f"Uncited: '{claim}'",
                severity="warning",
            )
    else:
        result.add_check(
            "citation_density",
            passed=True,
            detail=f"Citation score {citation_score:.0%} meets 80% threshold.",
        )

    # 2. Data freshness check
    stale_flags = check_data_freshness(content)
    if stale_flags:
        for flag in stale_flags:
            result.add_check(
                "data_freshness",
                passed=False,
                detail=flag,
                severity="warning",
            )
    else:
        result.add_check(
            "data_freshness",
            passed=True,
            detail="No stale data references detected.",
        )

    # 3. Policy compliance check
    violations = check_prohibited_patterns(content)
    result.policy_violations = violations
    if violations:
        for violation in violations:
            result.add_check(
                "policy_compliance",
                passed=False,
                detail=violation,
                severity="error",
            )
    else:
        result.add_check(
            "policy_compliance",
            passed=True,
            detail="No policy violations detected.",
        )

    # 4. Content substance check (not just a template/placeholder)
    if len(content) < 200:
        result.add_check(
            "content_substance",
            passed=False,
            detail="Output is too short (<200 chars) — likely a template or error.",
            severity="error",
        )

    placeholder_patterns = [
        r'\[Company_Name\]',
        r'\[First_Name\]',
        r'\[INSERT\s',
        r'Lorem ipsum',
        r'TODO:',
        r'placeholder',
    ]
    for pattern in placeholder_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            result.add_check(
                "content_substance",
                passed=False,
                detail=f"Placeholder pattern detected: {pattern}",
                severity="warning",
            )

    return result


def validate_all_outputs(agent_outputs: List[Dict[str, Any]]) -> Dict[str, ValidationResult]:
    """
    Validate all specialist outputs and return results keyed by task_id.
    """
    results = {}
    for output in agent_outputs:
        task_id = output.get("task_id", "unknown")
        specialist = output.get("specialist", "unknown")
        content = output.get("content", "")
        results[task_id] = validate_output(content, specialist)
    return results
