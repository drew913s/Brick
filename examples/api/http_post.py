"""HTTP POST request brick."""
import requests
import json


def http_post(url, data, headers=None, timeout=10):
    """
    Perform HTTP POST request with JSON data.

    Args:
        url: URL to post to
        data: Dict to send as JSON
        headers: Optional headers dict
        timeout: Request timeout in seconds

    Returns:
        dict: {status: int, data: str|None, error: str|None}
    """
    try:
        headers = headers or {}
        headers.setdefault("Content-Type", "application/json")
        response = requests.post(url, json=data, headers=headers, timeout=timeout)
        return {
            "status": response.status_code,
            "data": response.text,
            "error": None
        }
    except requests.Timeout:
        return {"status": 0, "data": None, "error": "Request timeout"}
    except requests.RequestException as e:
        return {"status": 0, "data": None, "error": str(e)}


def test_http_post():
    """Test HTTP POST."""
    result = http_post("https://httpbin.org/post", {"test": "data"})
    assert result["status"] == 200
    assert result["error"] is None
