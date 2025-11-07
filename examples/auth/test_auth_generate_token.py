"""Tests for auth_generate_token brick."""
import jwt
from datetime import datetime
from auth_generate_token import auth_generate_token


def test_generate_valid_token():
    """Test generating a valid token."""
    result = auth_generate_token(123, 'testuser', ['admin'], 'secret_key')
    assert result['token'] is not None
    assert result['expires_at'] is not None
    assert result['error'] is None
    
    # Verify token can be decoded
    decoded = jwt.decode(result['token'], 'secret_key', algorithms=['HS256'])
    assert decoded['user_id'] == 123
    assert decoded['username'] == 'testuser'
    assert decoded['roles'] == ['admin']


def test_custom_expiration():
    """Test custom expiration time."""
    result = auth_generate_token(456, 'user2', ['user'], 'secret_key', expires_in=7200)
    assert result['token'] is not None

    decoded = jwt.decode(result['token'], 'secret_key', algorithms=['HS256'])
    exp = decoded['exp']
    iat = decoded['iat']
    # Allow small tolerance for timestamp precision
    assert abs((exp - iat) - 7200) < 1


def test_empty_roles():
    """Test generating token with empty roles."""
    result = auth_generate_token(789, 'user3', [], 'secret_key')
    assert result['token'] is not None
    assert result['error'] is None


def test_multiple_roles():
    """Test generating token with multiple roles."""
    result = auth_generate_token(999, 'admin', ['admin', 'user', 'moderator'], 'secret_key')
    assert result['token'] is not None
    
    decoded = jwt.decode(result['token'], 'secret_key', algorithms=['HS256'])
    assert len(decoded['roles']) == 3


if __name__ == "__main__":
    test_generate_valid_token()
    test_custom_expiration()
    test_empty_roles()
    test_multiple_roles()
    print("All tests passed!")
