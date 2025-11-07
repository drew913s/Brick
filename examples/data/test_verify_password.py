"""
Tests for verify_password brick
"""

import pytest
import bcrypt
from verify_password import verify_password


def test_verify_password_valid():
    """Test successful password verification."""
    password = 'mypassword123'
    hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    result = verify_password(password, hash)
    assert result['valid'] is True
    assert result['error'] is None


def test_verify_password_invalid():
    """Test verification with wrong password."""
    password = 'correctpassword'
    hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    result = verify_password('wrongpassword', hash)
    assert result['valid'] is False
    assert result['error'] is None


def test_verify_password_empty_password():
    """Test error handling for empty password."""
    hash = bcrypt.hashpw(b'password', bcrypt.gensalt()).decode('utf-8')

    result = verify_password('', hash)
    assert result['error'] == 'empty_password'
    assert result['valid'] is False

    result = verify_password(None, hash)
    assert result['error'] == 'empty_password'


def test_verify_password_invalid_hash():
    """Test error handling for invalid hash."""
    result = verify_password('password', '')
    assert result['error'] == 'invalid_hash'
    assert result['valid'] is False

    result = verify_password('password', None)
    assert result['error'] == 'invalid_hash'


def test_verify_password_malformed_hash():
    """Test error handling for malformed hash."""
    result = verify_password('password', 'not_a_valid_bcrypt_hash')
    assert result['error'] is not None
    assert 'verification_failed' in result['error']
    assert result['valid'] is False


def test_verify_password_case_sensitive():
    """Test that password verification is case-sensitive."""
    password = 'MyPassword123'
    hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    result = verify_password('mypassword123', hash)
    assert result['valid'] is False
    assert result['error'] is None
