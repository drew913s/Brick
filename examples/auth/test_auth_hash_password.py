"""Tests for auth_hash_password brick."""
import bcrypt
from auth_hash_password import auth_hash_password


def test_hash_valid_password():
    """Test hashing a valid password."""
    result = auth_hash_password('mypassword123')
    assert result['hash'] is not None
    assert result['error'] is None
    assert result['hash'].startswith('$2b$')


def test_hash_with_custom_rounds():
    """Test hashing with custom rounds."""
    result = auth_hash_password('password', rounds=10)
    assert result['hash'] is not None
    assert '$2b$10$' in result['hash']


def test_empty_password():
    """Test hashing empty password."""
    result = auth_hash_password('')
    assert result['hash'] is None
    assert 'cannot be empty' in result['error']


def test_invalid_rounds():
    """Test with invalid rounds."""
    result = auth_hash_password('password', rounds=50)
    assert result['hash'] is None
    assert 'between 4 and 31' in result['error']


def test_hash_uniqueness():
    """Test that same password produces different hashes."""
    result1 = auth_hash_password('samepassword')
    result2 = auth_hash_password('samepassword')
    assert result1['hash'] != result2['hash']


def test_hash_verification():
    """Test that hash can be verified."""
    password = 'testpassword'
    result = auth_hash_password(password)
    assert bcrypt.checkpw(password.encode('utf-8'), result['hash'].encode('utf-8'))


if __name__ == "__main__":
    test_hash_valid_password()
    test_hash_with_custom_rounds()
    test_empty_password()
    test_invalid_rounds()
    test_hash_uniqueness()
    test_hash_verification()
    print("All tests passed!")
