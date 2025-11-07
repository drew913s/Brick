"""Tests for validate_input brick."""
from validate_input import validate_input


def test_validate_input():
    """Test input validation and sanitization."""
    # Test string validation
    result = validate_input('hello', {'type': 'string'})
    assert result['valid'] is True
    assert result['sanitized'] == 'hello'

    # Test integer validation
    result = validate_input('42', {'type': 'integer'})
    assert result['valid'] is True
    assert result['sanitized'] == 42

    # Test range validation
    result = validate_input(50, {'type': 'integer', 'min': 0, 'max': 100})
    assert result['valid'] is True

    result = validate_input(150, {'type': 'integer', 'max': 100})
    assert result['valid'] is False
    assert 'maximum' in result['error']

    # Test pattern validation
    result = validate_input('test@email.com', {'type': 'string', 'pattern': r'^[\w\.-]+@[\w\.-]+\.\w+$'})
    assert result['valid'] is True

    result = validate_input('not-an-email', {'type': 'string', 'pattern': r'^[\w\.-]+@[\w\.-]+\.\w+$'})
    assert result['valid'] is False

    # Test allowed values
    result = validate_input('red', {'type': 'string', 'allowed': ['red', 'blue', 'green']})
    assert result['valid'] is True

    result = validate_input('yellow', {'type': 'string', 'allowed': ['red', 'blue', 'green']})
    assert result['valid'] is False

    print("All validate_input tests passed!")


if __name__ == '__main__':
    test_validate_input()
