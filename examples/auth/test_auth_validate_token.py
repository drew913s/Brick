"""Tests for auth_validate_token brick."""
import jwt
from datetime import datetime
from auth_validate_token import auth_validate_token


def test_valid_token():
    """Test valid token validation."""
    secret = "test_secret_key"
    token = jwt.encode(
        {'user_id': 123, 'username': 'testuser', 'roles': ['admin'], 'exp': datetime.now().timestamp() + 3600},
        secret,
        algorithm='HS256'
    )
    result = auth_validate_token(token, secret)
    assert result['user_id'] == 123
    assert result['username'] == 'testuser'
    assert result['roles'] == ['admin']
    assert result['error'] is None


def test_expired_token():
    """Test expired token handling."""
    secret = "test_secret_key"
    token = jwt.encode(
        {'user_id': 123, 'username': 'testuser', 'exp': datetime.now().timestamp() - 3600},
        secret,
        algorithm='HS256'
    )
    result = auth_validate_token(token, secret)
    assert result['error'] == 'Token expired'
    assert result['user_id'] is None


def test_invalid_token():
    """Test invalid token handling."""
    result = auth_validate_token("invalid_token", "test_secret_key")
    assert result['error'] is not None
    assert 'Invalid token' in result['error']


def test_wrong_secret():
    """Test token with wrong secret key."""
    token = jwt.encode({'user_id': 123}, "secret1", algorithm='HS256')
    result = auth_validate_token(token, "secret2")
    assert result['error'] is not None


if __name__ == "__main__":
    test_valid_token()
    test_expired_token()
    test_invalid_token()
    test_wrong_secret()
    print("All tests passed!")
