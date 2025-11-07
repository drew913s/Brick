"""Security inspector for brick validation."""

import re
from pathlib import Path


BANNED_PATTERNS = [
    (r"eval\s*\(", "eval() on untrusted input", 30),
    (r"exec\s*\(", "exec() on untrusted input", 30),
    (r"shell\s*=\s*True", "shell=True with user input", 30),
    (r"__import__\s*\(", "dynamic __import__()", 30),
    (r"pickle\.loads?\s*\(", "pickle.loads() on untrusted data", 30),
]

RISKY_PATTERNS = [
    (r"password\s*=\s*['\"][^'\"]{8,}", "hardcoded password", 20),
    (r"api[_-]?key\s*=\s*['\"][^'\"]{8,}", "hardcoded API key", 20),
    (r"secret\s*=\s*['\"][^'\"]{8,}", "hardcoded secret", 20),
    (r"SELECT.*\+.*FROM", "SQL injection risk", 20),
]


def inspect_security(brick_file):
    """
    Scan brick for security violations.

    Returns: {score_deduction: int, violations: list}
    """
    violations = []
    deduction = 0

    code = Path(brick_file).read_text()

    for pattern, desc, penalty in BANNED_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE):
            violations.append(f"CRITICAL: {desc}")
            deduction += penalty

    for pattern, desc, penalty in RISKY_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE):
            violations.append(f"RISK: {desc}")
            deduction += penalty

    return {"score_deduction": deduction, "violations": violations}
