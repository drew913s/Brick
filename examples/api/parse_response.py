"""Parse API response brick."""
import json


def parse_response(response_text, expected_keys=None):
    """
    Parse JSON response and validate expected keys.

    Args:
        response_text: JSON string to parse
        expected_keys: Optional list of required keys

    Returns:
        dict: {data: dict|None, error: str|None}
    """
    try:
        data = json.loads(response_text)

        if expected_keys:
            missing = [k for k in expected_keys if k not in data]
            if missing:
                return {
                    "data": None,
                    "error": f"Missing keys: {', '.join(missing)}"
                }

        return {"data": data, "error": None}
    except json.JSONDecodeError as e:
        return {"data": None, "error": f"JSON parse error: {str(e)}"}


def test_parse_response():
    """Test successful parsing."""
    result = parse_response('{"id": 1, "name": "test"}')
    assert result["error"] is None
    assert result["data"]["id"] == 1


def test_parse_response_invalid():
    """Test invalid JSON."""
    result = parse_response("not json")
    assert result["error"] is not None
