"""API error handler brick."""


def handle_error(status_code, response_text):
    """
    Convert HTTP errors to user-friendly messages.

    Args:
        status_code: HTTP status code
        response_text: Response body

    Returns:
        dict: {severity: str, message: str, retryable: bool}
    """
    if status_code >= 500:
        return {
            "severity": "error",
            "message": "Server error, please try again",
            "retryable": True
        }
    elif status_code == 429:
        return {
            "severity": "warning",
            "message": "Rate limit exceeded",
            "retryable": True
        }
    elif status_code >= 400:
        return {
            "severity": "error",
            "message": f"Client error: {response_text[:100]}",
            "retryable": False
        }
    else:
        return {
            "severity": "info",
            "message": "Request successful",
            "retryable": False
        }


def test_handle_error_server():
    """Test server error."""
    result = handle_error(500, "Internal error")
    assert result["severity"] == "error"
    assert result["retryable"] is True
