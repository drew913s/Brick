"""Data sanitization brick."""
import html
import re


def data_sanitize(text, allow_html=False):
    """
    Sanitize user input for safe storage/display.

    Args:
        text: Input text to sanitize
        allow_html: Whether to allow HTML tags

    Returns:
        dict: {sanitized: str, removed: list}
    """
    removed = []

    # Remove null bytes
    if "\x00" in text:
        text = text.replace("\x00", "")
        removed.append("null_bytes")

    # Remove control characters
    text = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", text)

    # Handle HTML
    if not allow_html:
        original = text
        text = html.escape(text)
        if text != original:
            removed.append("html_tags")

    # Normalize whitespace
    text = " ".join(text.split())

    return {"sanitized": text, "removed": removed}


def test_data_sanitize():
    """Test sanitization."""
    result = data_sanitize("<script>alert('xss')</script>")
    assert "&lt;script&gt;" in result["sanitized"]
    assert "html_tags" in result["removed"]


def test_data_sanitize_allow_html():
    """Test with HTML allowed."""
    result = data_sanitize("<b>bold</b>", allow_html=True)
    assert "<b>bold</b>" == result["sanitized"]
