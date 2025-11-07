"""SQL injection prevention through identifier sanitization.

Args:
    identifier: str - SQL identifier (table/column name)
    value: any - Value to escape for SQL string literals

Returns:
    dict: {'sanitized': str|None, 'safe': bool, 'error': str|None}
"""
import re

def sanitize_sql(identifier=None, value=None):
    """Sanitize SQL identifiers and values to prevent injection."""
    try:
        result = {'sanitized': None, 'safe': False, 'error': None}
        # Sanitize identifier (table/column name)
        if identifier is not None:
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier):
                return {'sanitized': None, 'safe': False, 'error': 'Invalid identifier'}
            keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE',
                       'ALTER', 'EXEC', 'EXECUTE', 'UNION', 'WHERE']
            if identifier.upper() in keywords:
                return {'sanitized': None, 'safe': False, 'error': 'Reserved keyword'}
            result['sanitized'] = identifier
            result['safe'] = True
        # Sanitize value (escape single quotes)
        if value is not None:
            if isinstance(value, str):
                sanitized_value = value.replace("'", "''")
                dangerous = ['--', '/*', '*/', ';', 'UNION', 'DROP', 'EXEC']
                if any(d in value.upper() for d in dangerous):
                    result['safe'] = False
                    result['error'] = 'Suspicious pattern detected'
                else:
                    result['sanitized'] = sanitized_value
                    result['safe'] = True
            else:
                result['sanitized'] = str(value)
                result['safe'] = True
        return result
    except Exception as e:
        return {'sanitized': None, 'safe': False, 'error': str(e)}


# Tests
def test_sanitize_sql():
    """Test SQL sanitization."""
    # Test valid identifier
    result = sanitize_sql(identifier='users')
    assert result['safe'] is True
    assert result['sanitized'] == 'users'

    # Test SQL injection attempt in identifier
    result = sanitize_sql(identifier='users; DROP TABLE users--')
    assert result['safe'] is False
    assert 'Invalid' in result['error']

    # Test SQL keyword as identifier
    result = sanitize_sql(identifier='SELECT')
    assert result['safe'] is False

    # Test value sanitization
    result = sanitize_sql(value="O'Reilly")
    assert result['safe'] is True
    assert result['sanitized'] == "O''Reilly"

    # Test suspicious pattern in value
    result = sanitize_sql(value="test'; DROP TABLE users--")
    assert result['safe'] is False
