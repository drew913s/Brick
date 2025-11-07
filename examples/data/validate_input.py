"""Input validation and sanitization for user data.

Args:
    data: any - Input data to validate
    rules: dict - Validation rules {'type', 'min', 'max', 'pattern', 'allowed'}

Returns:
    dict: {'valid': bool, 'sanitized': any, 'error': str|None}
"""
import re


def validate_input(data, rules):
    """Validate and sanitize input data against rules."""
    try:
        # Type validation
        expected_type = rules.get('type', 'string')
        if expected_type == 'string' and not isinstance(data, str):
            return {'valid': False, 'sanitized': None, 'error': 'Must be string'}
        if expected_type == 'integer':
            try:
                data = int(data)
            except (ValueError, TypeError):
                return {'valid': False, 'sanitized': None, 'error': 'Must be integer'}
        if expected_type == 'float':
            try:
                data = float(data)
            except (ValueError, TypeError):
                return {'valid': False, 'sanitized': None, 'error': 'Must be float'}

        # Range validation for numbers
        if expected_type in ['integer', 'float']:
            if 'min' in rules and data < rules['min']:
                return {'valid': False, 'sanitized': None, 'error': f'Below minimum {rules["min"]}'}
            if 'max' in rules and data > rules['max']:
                return {'valid': False, 'sanitized': None, 'error': f'Above maximum {rules["max"]}'}

        # String validation
        if expected_type == 'string':
            if 'pattern' in rules and not re.match(rules['pattern'], data):
                return {'valid': False, 'sanitized': None, 'error': 'Pattern mismatch'}
            if 'allowed' in rules and data not in rules['allowed']:
                return {'valid': False, 'sanitized': None, 'error': 'Not in allowed values'}

        return {'valid': True, 'sanitized': data, 'error': None}

    except Exception as e:
        return {'valid': False, 'sanitized': None, 'error': str(e)}


def test_validate_input():
    """Test input validation."""
    result = validate_input('hello', {'type': 'string'})
    assert result['valid'] is True

    result = validate_input('123', {'type': 'integer'})
    assert result['valid'] is True

    result = validate_input(50, {'type': 'integer', 'min': 0, 'max': 100})
    assert result['valid'] is True

    result = validate_input(150, {'type': 'integer', 'max': 100})
    assert result['valid'] is False
