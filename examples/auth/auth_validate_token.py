"""
Validate JWT token and extract user information.

Args:
    token (str): JWT token string
    secret_key (str): Secret key for token verification

Returns:
    dict: {
        'user_id': int or None,
        'username': str or None,
        'roles': list or None,
        'error': str or None
    }
"""
import jwt
from datetime import datetime


def auth_validate_token(token, secret_key):
    """Validate JWT token and return user information."""
    try:
        # Verify and decode token
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=['HS256']
        )

        # Extract user info
        return {
            'user_id': payload.get('user_id'),
            'username': payload.get('username'),
            'roles': payload.get('roles', []),
            'error': None
        }

    except jwt.ExpiredSignatureError:
        return {'user_id': None, 'username': None, 'roles': None, 'error': 'Token expired'}
    except jwt.InvalidTokenError as e:
        return {'user_id': None, 'username': None, 'roles': None, 'error': f'Invalid token: {str(e)}'}
    except Exception as e:
        return {'user_id': None, 'username': None, 'roles': None, 'error': f'Validation failed: {str(e)}'}
