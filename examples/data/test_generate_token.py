"""
Tests for generate_token brick
"""

import pytest
import jwt
from datetime import datetime
from generate_token import generate_token


def test_generate_token_valid():
    """Test successful token generation."""
    result = generate_token(123, 'testuser', 'secret', 3600)

    assert result['token'] is not None
    assert result['expires_at'] is not None
    assert result['error'] is None

    # Verify token can be decoded
    payload = jwt.decode(result['token'], 'secret', algorithms=['HS256'])
    assert payload['user_id'] == 123
    assert payload['username'] == 'testuser'
    assert payload['exp'] == result['expires_at']


def test_generate_token_invalid_user_id():
    """Test error handling for invalid user_id."""
    result = generate_token(0, 'testuser', 'secret', 3600)
    assert result['error'] == 'invalid_user_id'

    result = generate_token(-1, 'testuser', 'secret', 3600)
    assert result['error'] == 'invalid_user_id'

    result = generate_token('not_an_int', 'testuser', 'secret', 3600)
    assert result['error'] == 'invalid_user_id'


def test_generate_token_invalid_username():
    """Test error handling for invalid username."""
    result = generate_token(123, '', 'secret', 3600)
    assert result['error'] == 'invalid_username'

    result = generate_token(123, None, 'secret', 3600)
    assert result['error'] == 'invalid_username'


def test_generate_token_invalid_expires_in():
    """Test error handling for invalid expires_in_seconds."""
    result = generate_token(123, 'testuser', 'secret', 0)
    assert result['error'] == 'invalid_expires_in'

    result = generate_token(123, 'testuser', 'secret', -100)
    assert result['error'] == 'invalid_expires_in'


def test_generate_token_expiration_timing():
    """Test that expiration is set correctly."""
    before = int(datetime.now().timestamp())
    result = generate_token(123, 'testuser', 'secret', 7200)
    after = int(datetime.now().timestamp())

    expected_min = before + 7200
    expected_max = after + 7200

    assert expected_min <= result['expires_at'] <= expected_max
