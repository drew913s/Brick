"""Contract inspector for brick validation."""

import ast
import json
from pathlib import Path


def inspect_contract(brick_file):
    """
    Validate brick against its metadata contract.

    Returns: {score_deduction: int, violations: list}
    """
    violations = []
    deduction = 0

    brick_path = Path(brick_file)
    meta_path = brick_path.with_suffix(".meta.json")

    if not meta_path.exists():
        violations.append("Missing metadata file")
        return {"score_deduction": 20, "violations": violations}

    try:
        metadata = json.loads(meta_path.read_text())
    except json.JSONDecodeError:
        violations.append("Invalid metadata JSON")
        return {"score_deduction": 20, "violations": violations}

    # Check required metadata fields
    required = ["brick_id", "interface", "dependencies", "tests"]
    for field in required:
        if field not in metadata:
            violations.append(f"Missing metadata field: {field}")
            deduction += 5

    # Validate code matches interface
    try:
        code = brick_path.read_text()
        tree = ast.parse(code)

        # Check for main function
        funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
        if not funcs:
            violations.append("No function defined")
            deduction += 10
    except SyntaxError:
        violations.append("Syntax error in code")
        deduction += 20

    return {"score_deduction": deduction, "violations": violations}
