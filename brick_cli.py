#!/usr/bin/env python3
"""
Brick Architecture CLI Tool

Commands:
  init        Initialize a new brick project
  generate    Generate brick from specification
  validate    Validate brick compliance
  inspect     Inspect brick security and quality
  test        Run brick tests
"""

import sys
import argparse
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent / "tools"))

from cli_init import run as init_run
from cli_generate import run as generate_run
from cli_validate import run as validate_run
from cli_inspect import run as inspect_run
from cli_test import run as test_run


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="brick",
        description="Brick Architecture CLI - Build maintainable AI-generated code"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # brick init
    init_parser = subparsers.add_parser("init", help="Initialize new brick project")
    init_parser.add_argument("project_name", help="Name of the project")

    # brick generate
    gen_parser = subparsers.add_parser("generate", help="Generate brick from spec")
    gen_parser.add_argument("brick_name", help="Name of the brick")
    gen_parser.add_argument("--spec", required=True, help="Path to spec file")
    gen_parser.add_argument("--output", default=".", help="Output directory")

    # brick validate
    val_parser = subparsers.add_parser("validate", help="Validate brick")
    val_parser.add_argument("brick_file", help="Path to brick file")

    # brick inspect
    ins_parser = subparsers.add_parser("inspect", help="Inspect brick")
    ins_parser.add_argument("brick_file", help="Path to brick file")

    # brick test
    test_parser = subparsers.add_parser("test", help="Run brick tests")
    test_parser.add_argument("brick_file", help="Path to brick file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Route to command
    try:
        if args.command == "init":
            return init_run(args) or 0
        elif args.command == "generate":
            return generate_run(args) or 0
        elif args.command == "validate":
            return validate_run(args) or 0
        elif args.command == "inspect":
            return inspect_run(args) or 0
        elif args.command == "test":
            return test_run(args) or 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
