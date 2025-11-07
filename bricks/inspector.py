"""Main inspector combining all inspection modules."""

import sys
from pathlib import Path

# Add tools to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from inspect_security import inspect_security
from inspect_contract import inspect_contract
from inspect_quality import inspect_quality
from inspect_dependencies import inspect_dependencies


def inspect_brick(brick_file):
    """
    Run all inspections and return combined score.

    Args:
        brick_file: Path to brick file

    Returns:
        dict: {score: int, rating: str, issues: list}
    """
    score = 100
    all_issues = []

    # Run all inspections
    security = inspect_security(brick_file)
    contract = inspect_contract(brick_file)
    quality = inspect_quality(brick_file)
    deps = inspect_dependencies(brick_file)

    # Deduct scores
    score -= security["score_deduction"]
    score -= contract["score_deduction"]
    score -= quality["score_deduction"]
    score -= deps["score_deduction"]

    # Collect issues
    all_issues.extend(security.get("violations", []))
    all_issues.extend(contract.get("violations", []))
    all_issues.extend(quality.get("issues", []))
    all_issues.extend(deps.get("issues", []))

    # Determine rating
    if score >= 90:
        rating = "EXCELLENT"
    elif score >= 70:
        rating = "GOOD"
    elif score >= 50:
        rating = "NEEDS WORK"
    else:
        rating = "POOR"

    return {"score": max(0, score), "rating": rating, "issues": all_issues}
