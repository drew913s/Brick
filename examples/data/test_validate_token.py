"""
Tests for validate_token brick
"""

import pytest
import jwt
from datetime import datetime, timedelta
from validate_token import validate_token


def test_validate_token_valid():
    """Test valid token validation."""
    secret = "test_secret_key"
    exp_time = int((datetime.now() + timedelta(hours=1)).timestamp())

    token = jwt.encode(
        {'user_id': 123, 'username': 'testuser', 'exp': exp_time},
        secret,
        algorithm='HS256'
    )

    result = validate_token(token, secret)
    assert result['user_id'] == 123
    assert result['username'] == 'testuser'
    assert result['exp'] == exp_time
    assert result['error'] is None


def test_validate_token_expired():
    """Test expired token handling."""
    secret = "test_secret_key"
    exp_time = int((datetime.now() - timedelta(hours=1)).timestamp())

    token = jwt.encode(
        {'user_id': 123, 'username': 'testuser', 'exp': exp_time},
        secret,
        algorithm='HS256'
    )

    result = validate_token(token, secret)
    assert result['user_id'] is None
    assert result['error'] == 'token_expired'


def test_validate_token_invalid():
    """Test invalid token handling."""
    result = validate_token("invalid_token", "secret")
    assert result['user_id'] is None
    assert result['error'] is not None
    assert 'invalid_token' in result['error']


def test_validate_token_wrong_secret():
    """Test token with wrong secret key."""
    token = jwt.encode({'user_id': 123}, "secret1", algorithm='HS256')
    result = validate_token(token, "secret2")
    assert result['error'] is not None
    assert 'invalid_token' in result['error']


def test_validate_token_no_expiration():
    """Test token without expiration."""
    secret = "test_secret_key"
    token = jwt.encode(
        {'user_id': 456, 'username': 'noexp'},
        secret,
        algorithm='HS256'
    )

    result = validate_token(token, secret)
    assert result['user_id'] == 456
    assert result['username'] == 'noexp'
    assert result['exp'] is None
    assert result['error'] is None
