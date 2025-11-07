"""CLI command: Inspect brick security and quality."""

import sys
from pathlib import Path

# Add bricks to path
sys.path.insert(0, str(Path(__file__).parent.parent / "bricks"))
from inspector import inspect_brick


def run(args):
    """
    Run security and quality inspection.

    Args:
        args: Namespace with brick_file attribute
    """
    brick_file = args.brick_file

    print(f"Inspecting: {brick_file}")
    print("=" * 50)

    result = inspect_brick(brick_file)
    score = result["score"]
    rating = result["rating"]
    issues = result["issues"]

    print(f"\nScore: {score}/100")
    print(f"Rating: {rating}")

    if issues:
        print("\nIssues found:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("\n✓ No issues found")

    print("=" * 50)

    # Return exit code
    if score >= 70:
        print("✓ Brick passes inspection")
        return 0
    else:
        print("✗ Brick requires improvements")
        return 1
