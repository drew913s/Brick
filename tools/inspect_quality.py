"""Quality inspector for brick validation."""

import ast
from pathlib import Path


def inspect_quality(brick_file):
    """
    Check code quality (size, docs, naming).

    Returns: {score_deduction: int, issues: list}
    """
    issues = []
    deduction = 0

    code = Path(brick_file).read_text()
    lines = [l for l in code.split("\n") if l.strip()]

    # Check size limit
    if len(lines) > 50:
        issues.append(f"Exceeds 50 lines: {len(lines)} lines")
        deduction += 10

    # Check for docstring
    try:
        tree = ast.parse(code)
        if not ast.get_docstring(tree):
            issues.append("Missing module docstring")
            deduction += 5

        # Check function docstrings
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    issues.append(f"Missing docstring: {node.name}")
                    deduction += 3
    except SyntaxError:
        issues.append("Syntax error")
        deduction += 20

    return {"score_deduction": deduction, "issues": issues}
