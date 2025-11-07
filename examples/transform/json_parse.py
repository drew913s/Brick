"""JSON parsing brick with type coercion."""
import json


def json_parse(json_string, default=None):
    """
    Parse JSON with fallback to default value.

    Args:
        json_string: String to parse
        default: Value to return on error

    Returns:
        dict: {data: any, error: str|None}
    """
    try:
        data = json.loads(json_string)
        return {"data": data, "error": None}
    except json.JSONDecodeError as e:
        if default is not None:
            return {"data": default, "error": str(e)}
        return {"data": None, "error": str(e)}


def test_json_parse():
    """Test successful parse."""
    result = json_parse('{"key": "value"}')
    assert result["error"] is None
    assert result["data"]["key"] == "value"


def test_json_parse_default():
    """Test default on error."""
    result = json_parse("invalid", default={})
    assert result["data"] == {}
    assert result["error"] is not None
