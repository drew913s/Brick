"""
Tests for check_permission brick
"""

import pytest
from check_permission import check_permission


def test_check_permission_admin_all():
    """Test that admin role has all permissions."""
    result = check_permission('admin', 'read', 'document.pdf')
    assert result['allowed'] is True
    assert result['error'] is None

    result = check_permission('admin', 'write', 'document.pdf')
    assert result['allowed'] is True

    result = check_permission('admin', 'delete', 'document.pdf')
    assert result['allowed'] is True

    result = check_permission('admin', 'admin', 'document.pdf')
    assert result['allowed'] is True


def test_check_permission_user():
    """Test user role permissions."""
    result = check_permission('user', 'read', 'document.pdf')
    assert result['allowed'] is True
    assert result['error'] is None

    result = check_permission('user', 'write', 'document.pdf')
    assert result['allowed'] is True

    result = check_permission('user', 'delete', 'document.pdf')
    assert result['allowed'] is False
    assert result['error'] is None

    result = check_permission('user', 'admin', 'document.pdf')
    assert result['allowed'] is False


def test_check_permission_guest():
    """Test guest role permissions."""
    result = check_permission('guest', 'read', 'document.pdf')
    assert result['allowed'] is True
    assert result['error'] is None

    result = check_permission('guest', 'write', 'document.pdf')
    assert result['allowed'] is False

    result = check_permission('guest', 'delete', 'document.pdf')
    assert result['allowed'] is False


def test_check_permission_invalid_role():
    """Test error handling for invalid role."""
    result = check_permission('superuser', 'read', 'document.pdf')
    assert result['error'] == 'invalid_role'
    assert result['allowed'] is False


def test_check_permission_invalid_permission():
    """Test error handling for invalid permission."""
    result = check_permission('user', 'execute', 'document.pdf')
    assert result['error'] == 'invalid_permission'
    assert result['allowed'] is False


def test_check_permission_empty_resource():
    """Test error handling for empty resource."""
    result = check_permission('user', 'read', '')
    assert result['error'] == 'empty_resource'
    assert result['allowed'] is False

    result = check_permission('user', 'read', None)
    assert result['error'] == 'empty_resource'
