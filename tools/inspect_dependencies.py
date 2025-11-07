"""Dependency inspector for brick validation."""

import ast
from pathlib import Path


RISKY_IMPORTS = ["pickle", "marshal", "shelve", "os.system"]


def inspect_dependencies(brick_file):
    """
    Validate brick dependencies.

    Returns: {score_deduction: int, issues: list}
    """
    issues = []
    deduction = 0

    try:
        code = Path(brick_file).read_text()
        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in RISKY_IMPORTS:
                        issues.append(f"Risky import: {alias.name}")
                        deduction += 5
            elif isinstance(node, ast.ImportFrom):
                if node.module in RISKY_IMPORTS:
                    issues.append(f"Risky import: {node.module}")
                    deduction += 5
    except SyntaxError:
        issues.append("Syntax error")
        deduction += 10

    return {"score_deduction": deduction, "issues": issues}
