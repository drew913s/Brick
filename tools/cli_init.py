"""CLI command: Initialize new brick project."""

from pathlib import Path


def run(args):
    """
    Initialize a new brick project.

    Args:
        args: Namespace with project_name attribute
    """
    project_name = args.project_name
    project_path = Path(project_name)

    if project_path.exists():
        print(f"Error: Directory '{project_name}' already exists")
        return 1

    # Create directory structure
    folders = ["bricks/auth", "bricks/data", "bricks/api",
               "bricks/transform", "tests", "specs"]
    for folder in folders:
        (project_path / folder).mkdir(parents=True, exist_ok=True)

    # Create README
    readme = f"""# {project_name}

A Brick Architecture project.

## Structure
- bricks/auth/ - Authentication bricks
- bricks/data/ - Data access bricks
- bricks/api/ - API integration bricks
- bricks/transform/ - Data transformation bricks
- tests/ - Test files
- specs/ - Specification files (YAML/JSON)

## Usage
Generate: brick generate <name> --spec specs/<spec>.yaml
Validate: brick validate bricks/<category>/<name>.py
Inspect: brick inspect bricks/<category>/<name>.py
Test: brick test bricks/<category>/<name>.py
"""
    (project_path / "README.md").write_text(readme)

    print(f"✓ Project '{project_name}' created successfully")
    return 0
