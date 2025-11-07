"""Tests for auth_verify_password brick."""
import bcrypt
from auth_verify_password import auth_verify_password


def test_verify_correct_password():
    """Test verifying correct password."""
    password = 'correctpassword'
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    result = auth_verify_password(password, hashed)
    assert result['valid'] is True
    assert result['error'] is None


def test_verify_incorrect_password():
    """Test verifying incorrect password."""
    password = 'correctpassword'
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    result = auth_verify_password('wrongpassword', hashed)
    assert result['valid'] is False
    assert result['error'] is None


def test_empty_password():
    """Test with empty password."""
    hashed = bcrypt.hashpw('test'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    result = auth_verify_password('', hashed)
    assert result['valid'] is False
    assert 'cannot be empty' in result['error']


def test_empty_hash():
    """Test with empty hash."""
    result = auth_verify_password('password', '')
    assert result['valid'] is False
    assert 'cannot be empty' in result['error']


def test_invalid_hash_format():
    """Test with invalid hash format."""
    result = auth_verify_password('password', 'invalid_hash_format')
    assert result['valid'] is False
    assert 'hash format' in result['error']


def test_case_sensitive():
    """Test that verification is case sensitive."""
    password = 'Password123'
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    result = auth_verify_password('password123', hashed)
    assert result['valid'] is False


if __name__ == "__main__":
    test_verify_correct_password()
    test_verify_incorrect_password()
    test_empty_password()
    test_empty_hash()
    test_invalid_hash_format()
    test_case_sensitive()
    print("All tests passed!")
