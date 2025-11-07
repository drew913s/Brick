"""
Verify password against bcrypt hash.

Args:
    password (str): Plain text password to verify
    password_hash (str): Bcrypt hash to verify against

Returns:
    dict: {
        'valid': bool,
        'error': str or None
    }
"""
import bcrypt


def auth_verify_password(password, password_hash):
    """Verify password against bcrypt hash."""
    try:
        # Validate inputs
        if not password:
            return {'valid': False, 'error': 'Password cannot be empty'}
        
        if not password_hash:
            return {'valid': False, 'error': 'Hash cannot be empty'}
        
        # Verify password
        is_valid = bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
        
        return {
            'valid': is_valid,
            'error': None
        }
    
    except ValueError as e:
        return {'valid': False, 'error': 'Invalid hash format'}
    except Exception as e:
        return {'valid': False, 'error': f'Verification failed: {str(e)}'}


# Tests
def test_auth_verify_password_correct():
    hashed = bcrypt.hashpw('mypassword'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    result = auth_verify_password('mypassword', hashed)
    assert result['valid'] is True and result['error'] is None
