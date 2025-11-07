"""
Tests for hash_password brick
"""

import pytest
import bcrypt
from hash_password import hash_password


def test_hash_password_valid():
    """Test successful password hashing."""
    result = hash_password('mypassword123', 10)

    assert result['hash'] is not None
    assert result['error'] is None
    assert result['hash'].startswith('$2b$')

    # Verify the hash works with bcrypt
    assert bcrypt.checkpw(
        'mypassword123'.encode('utf-8'),
        result['hash'].encode('utf-8')
    )


def test_hash_password_different_rounds():
    """Test hashing with different round counts."""
    result1 = hash_password('password', 4)
    result2 = hash_password('password', 12)

    assert result1['hash'] is not None
    assert result2['hash'] is not None
    assert result1['hash'] != result2['hash']


def test_hash_password_empty():
    """Test error handling for empty password."""
    result = hash_password('', 10)
    assert result['error'] == 'empty_password'

    result = hash_password(None, 10)
    assert result['error'] == 'empty_password'


def test_hash_password_invalid_rounds():
    """Test error handling for invalid rounds."""
    result = hash_password('password', 3)
    assert result['error'] == 'invalid_rounds'

    result = hash_password('password', 32)
    assert result['error'] == 'invalid_rounds'

    result = hash_password('password', -1)
    assert result['error'] == 'invalid_rounds'


def test_hash_password_unique():
    """Test that same password produces different hashes (salt)."""
    result1 = hash_password('samepassword', 10)
    result2 = hash_password('samepassword', 10)

    assert result1['hash'] != result2['hash']
    assert bcrypt.checkpw('samepassword'.encode('utf-8'), result1['hash'].encode('utf-8'))
    assert bcrypt.checkpw('samepassword'.encode('utf-8'), result2['hash'].encode('utf-8'))
