"""
Hash password using bcrypt algorithm.

Args:
    password (str): Plain text password to hash
    rounds (int): Number of bcrypt rounds (default: 12, range: 4-31)

Returns:
    dict: {
        'hash': str or None,
        'error': str or None
    }
"""
import bcrypt


def auth_hash_password(password, rounds=12):
    """Hash password using bcrypt with specified rounds."""
    try:
        # Validate inputs
        if not password:
            return {'hash': None, 'error': 'Password cannot be empty'}
        
        if rounds < 4 or rounds > 31:
            return {'hash': None, 'error': 'Rounds must be between 4 and 31'}
        
        # Hash password
        salt = bcrypt.gensalt(rounds=rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        return {
            'hash': hashed.decode('utf-8'),
            'error': None
        }
    
    except Exception as e:
        return {'hash': None, 'error': f'Hashing failed: {str(e)}'}


# Tests
def test_auth_hash_password_valid():
    result = auth_hash_password('mypassword123')
    assert result['hash'] is not None and result['error'] is None
    assert result['hash'].startswith('$2b$')

def test_auth_hash_password_empty():
    result = auth_hash_password('')
    assert result['hash'] is None and 'empty' in result['error'].lower()
