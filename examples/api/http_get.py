"""HTTP GET request brick."""
import requests


def http_get(url, headers=None, timeout=10):
    """
    Perform HTTP GET request with error handling.

    Args:
        url: URL to fetch
        headers: Optional headers dict
        timeout: Request timeout in seconds

    Returns:
        dict: {status: int, data: str|None, error: str|None}
    """
    try:
        response = requests.get(url, headers=headers or {}, timeout=timeout)
        return {
            "status": response.status_code,
            "data": response.text,
            "error": None
        }
    except requests.Timeout:
        return {"status": 0, "data": None, "error": "Request timeout"}
    except requests.RequestException as e:
        return {"status": 0, "data": None, "error": str(e)}


def test_http_get():
    """Test HTTP GET with httpbin."""
    result = http_get("https://httpbin.org/get")
    assert result["status"] == 200
    assert result["error"] is None
    assert "httpbin" in result["data"]


def test_http_get_timeout():
    """Test timeout handling."""
    result = http_get("https://httpbin.org/delay/20", timeout=1)
    assert result["error"] == "Request timeout"
