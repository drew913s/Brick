"""CLI command: Run brick tests."""

import subprocess
import sys
from pathlib import Path


def run(args):
    """
    Run tests for a brick.

    Args:
        args: Namespace with brick_file attribute
    """
    brick_file = Path(args.brick_file)

    if not brick_file.exists():
        print(f"Error: File not found: {brick_file}")
        return 1

    # Find test file
    test_file = brick_file.parent / f"test_{brick_file.name}"
    if not test_file.exists():
        test_file = Path("tests") / f"test_{brick_file.name}"

    if not test_file.exists():
        print(f"Error: Test file not found for {brick_file.name}")
        return 1

    print(f"Running tests: {test_file}")
    print("-" * 50)

    # Try pytest first
    try:
        result = subprocess.run(["pytest", str(test_file), "-v"],
                                capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return result.returncode
    except FileNotFoundError:
        # Fallback to python -m unittest
        print("pytest not found, using fallback")
        return run_fallback(test_file)


def run_fallback(test_file):
    """Run tests using exec as fallback."""
    namespace = {}
    exec(test_file.read_text(), namespace)

    passed = failed = 0
    for name, obj in namespace.items():
        if name.startswith("test_") and callable(obj):
            try:
                obj()
                print(f"✓ {name}")
                passed += 1
            except Exception as e:
                print(f"✗ {name}: {e}")
                failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1
