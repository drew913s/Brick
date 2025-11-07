"""Tests for auth_check_permission brick."""
from auth_check_permission import auth_check_permission


def test_permission_granted():
    """Test permission is granted for valid role."""
    role_perms = {
        'admin': ['read', 'write', 'delete'],
        'user': ['read']
    }
    result = auth_check_permission(['admin'], 'delete', role_perms)
    assert result['allowed'] is True
    assert result['matched_role'] == 'admin'
    assert result['error'] is None


def test_permission_denied():
    """Test permission is denied when not in role."""
    role_perms = {
        'admin': ['read', 'write', 'delete'],
        'user': ['read']
    }
    result = auth_check_permission(['user'], 'delete', role_perms)
    assert result['allowed'] is False
    assert result['matched_role'] is None


def test_multiple_roles():
    """Test user with multiple roles."""
    role_perms = {
        'admin': ['admin_panel'],
        'moderator': ['moderate_content'],
        'user': ['read']
    }
    result = auth_check_permission(['user', 'moderator'], 'moderate_content', role_perms)
    assert result['allowed'] is True
    assert result['matched_role'] == 'moderator'


def test_unknown_role():
    """Test user with unknown role."""
    role_perms = {'admin': ['delete']}
    result = auth_check_permission(['unknown_role'], 'delete', role_perms)
    assert result['allowed'] is False


def test_empty_roles():
    """Test user with no roles."""
    role_perms = {'admin': ['delete']}
    result = auth_check_permission([], 'delete', role_perms)
    assert result['allowed'] is False


def test_invalid_user_roles_type():
    """Test with invalid user_roles type."""
    result = auth_check_permission('not_a_list', 'permission', {})
    assert result['allowed'] is False
    assert 'must be a list' in result['error']


def test_empty_permission():
    """Test with empty permission."""
    result = auth_check_permission(['admin'], '', {'admin': ['read']})
    assert result['allowed'] is False
    assert 'cannot be empty' in result['error']


if __name__ == "__main__":
    test_permission_granted()
    test_permission_denied()
    test_multiple_roles()
    test_unknown_role()
    test_empty_roles()
    test_invalid_user_roles_type()
    test_empty_permission()
    print("All tests passed!")
