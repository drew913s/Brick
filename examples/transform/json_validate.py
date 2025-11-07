"""JSON validation brick."""
import json


def json_validate(json_string, schema=None):
    """
    Validate JSON string and optionally check schema.

    Args:
        json_string: String to validate
        schema: Optional dict with required_keys list

    Returns:
        dict: {valid: bool, data: dict|None, error: str|None}
    """
    try:
        data = json.loads(json_string)

        if schema and "required_keys" in schema:
            missing = [k for k in schema["required_keys"] if k not in data]
            if missing:
                return {
                    "valid": False,
                    "data": None,
                    "error": f"Missing required keys: {', '.join(missing)}"
                }

        return {"valid": True, "data": data, "error": None}
    except json.JSONDecodeError as e:
        return {"valid": False, "data": None, "error": str(e)}


def test_json_validate():
    """Test valid JSON."""
    result = json_validate('{"name": "test", "value": 123}')
    assert result["valid"] is True
    assert result["data"]["name"] == "test"


def test_json_validate_schema():
    """Test schema validation."""
    result = json_validate('{"name": "test"}', {"required_keys": ["name", "id"]})
    assert result["valid"] is False
    assert "id" in result["error"]
