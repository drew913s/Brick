"""
Generate JWT token for user authentication.

Args:
    user_id (int): User identifier
    username (str): Username
    roles (list): List of user roles
    secret_key (str): Secret key for signing
    expires_in (int): Token expiration in seconds (default: 3600)

Returns:
    dict: {
        'token': str or None,
        'expires_at': str or None,
        'error': str or None
    }
"""
import jwt
from datetime import datetime, timedelta


def auth_generate_token(user_id, username, roles, secret_key, expires_in=3600):
    """Generate JWT token with user information."""
    try:
        # Calculate expiration
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        
        # Create payload
        payload = {
            'user_id': user_id,
            'username': username,
            'roles': roles,
            'exp': expires_at.timestamp(),
            'iat': datetime.now().timestamp()
        }
        
        # Generate token
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        
        return {
            'token': token,
            'expires_at': expires_at.isoformat(),
            'error': None
        }
    
    except Exception as e:
        return {'token': None, 'expires_at': None, 'error': f'Token generation failed: {str(e)}'}


# Tests
def test_auth_generate_token_valid():
    result = auth_generate_token(1, 'alice', ['admin'], 'secret', 3600)
    assert result['token'] is not None and result['error'] is None
    assert result['expires_at'] is not None
