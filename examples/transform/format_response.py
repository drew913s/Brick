"""Response formatting brick."""
import json


def format_response(data, format_type="json", status=200):
    """
    Format data for API response.

    Args:
        data: Data to format
        format_type: Output format (json, xml, text)
        status: HTTP status code

    Returns:
        dict: {body: str, content_type: str, status: int}
    """
    if format_type == "json":
        return {
            "body": json.dumps(data, indent=2),
            "content_type": "application/json",
            "status": status
        }
    elif format_type == "xml":
        # Simple XML formatting
        xml = "<response>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</response>"
        return {
            "body": xml,
            "content_type": "application/xml",
            "status": status
        }
    else:
        return {
            "body": str(data),
            "content_type": "text/plain",
            "status": status
        }


def test_format_response_json():
    """Test JSON formatting."""
    result = format_response({"key": "value"})
    assert result["content_type"] == "application/json"
    assert "key" in result["body"]


def test_format_response_xml():
    """Test XML formatting."""
    result = format_response({"key": "value"}, format_type="xml")
    assert result["content_type"] == "application/xml"
    assert "<key>value</key>" in result["body"]
