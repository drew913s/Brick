"""CLI command: Validate brick compliance."""

import ast
from pathlib import Path


def run(args):
    """
    Validate brick meets basic requirements.

    Args:
        args: Namespace with brick_file attribute
    """
    brick_file = Path(args.brick_file)

    if not brick_file.exists():
        print(f"Error: File not found: {brick_file}")
        return 1

    violations = []
    code = brick_file.read_text()

    # Check size
    lines = [l for l in code.split("\n") if l.strip()]
    if len(lines) > 50:
        violations.append(f"Exceeds 50 lines: {len(lines)}")

    # Check syntax
    try:
        ast.parse(code)
    except SyntaxError as e:
        violations.append(f"Syntax error: {e}")

    # Check docstring
    if '"""' not in code and "'''" not in code:
        violations.append("Missing docstring")

    # Check metadata
    meta_file = brick_file.with_suffix(".meta.json")
    if not meta_file.exists():
        violations.append(f"Missing metadata: {meta_file.name}")

    # Report results
    print(f"Validating: {brick_file}")
    if violations:
        print("\n❌ Violations:")
        for v in violations:
            print(f"  • {v}")
        return 1
    else:
        print("\n✓ Brick is valid")
        return 0
