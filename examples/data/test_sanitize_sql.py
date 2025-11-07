"""Tests for sanitize_sql brick."""
from sanitize_sql import sanitize_sql


def test_sanitize_sql():
    """Test SQL injection prevention."""
    # Test valid identifier
    result = sanitize_sql(identifier='users_table')
    assert result['safe'] is True
    assert result['sanitized'] == 'users_table'

    # Test invalid identifier with special chars
    result = sanitize_sql(identifier='users; DROP TABLE users;')
    assert result['safe'] is False
    assert result['error'] is not None

    # Test SQL keyword as identifier
    result = sanitize_sql(identifier='SELECT')
    assert result['safe'] is False
    assert 'keyword' in result['error']

    # Test value sanitization
    result = sanitize_sql(value="O'Reilly")
    assert result['safe'] is True
    assert result['sanitized'] == "O''Reilly"

    # Test SQL injection attempt in value
    result = sanitize_sql(value="'; DROP TABLE users; --")
    assert result['safe'] is False
    assert 'Suspicious' in result['error']

    # Test clean value
    result = sanitize_sql(value='normal text')
    assert result['safe'] is True

    # Test numeric value
    result = sanitize_sql(value=42)
    assert result['safe'] is True
    assert result['sanitized'] == '42'

    print("All sanitize_sql tests passed!")


if __name__ == '__main__':
    test_sanitize_sql()
