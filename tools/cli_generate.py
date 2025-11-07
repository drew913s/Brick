"""CLI command: Generate brick from specification."""

import json
import yaml
import hashlib
from pathlib import Path
from datetime import datetime


def run(args):
    """
    Generate brick from specification file.

    Args:
        args: Namespace with brick_name, spec attributes
    """
    brick_name = args.brick_name
    spec_file = Path(args.spec)
    output_dir = Path(args.output) if hasattr(args, "output") else Path(".")

    if not spec_file.exists():
        print(f"Error: Spec file not found: {spec_file}")
        return 1

    # Parse specification
    spec = parse_spec(spec_file)
    if not spec:
        return 1

    # Generate metadata
    metadata = generate_metadata(spec, spec_file)
    metadata_path = output_dir / f"{brick_name}.meta.json"
    metadata_path.write_text(json.dumps(metadata, indent=2))

    print(f"✓ Generated metadata: {metadata_path}")
    print("\nNote: Brick implementation placeholder created.")
    print("  Install anthropic package for AI generation")
    print("  Or implement manually following the spec")
    return 0


def parse_spec(spec_file):
    """Parse YAML or JSON spec file."""
    try:
        content = spec_file.read_text()
        if spec_file.suffix in [".yaml", ".yml"]:
            return yaml.safe_load(content)
        else:
            return json.loads(content)
    except Exception as e:
        print(f"Error parsing spec: {e}")
        return None


def generate_metadata(spec, spec_file):
    """Generate brick metadata from spec."""
    spec_hash = hashlib.sha256(spec_file.read_bytes()).hexdigest()
    return {
        "brick_id": f"{spec['brick_name']}_v1",
        "generated": datetime.utcnow().isoformat() + "Z",
        "model": "manual",
        "prompt_hash": f"sha256:{spec_hash}",
        "interface": {
            "inputs": spec.get("inputs", {}),
            "outputs": spec.get("outputs", {}),
        },
        "dependencies": spec.get("dependencies", []),
        "tests": [f"test_{spec['brick_name']}"],
    }
