"""
Check if user has required permission based on role-based access control (RBAC).

Args:
    user_roles (list): List of roles assigned to user
    required_permission (str): Required permission to check
    role_permissions (dict): Mapping of roles to their permissions

Returns:
    dict: {
        'allowed': bool,
        'matched_role': str or None,
        'error': str or None
    }
"""


def auth_check_permission(user_roles, required_permission, role_permissions):
    """Check if user roles grant required permission."""
    try:
        # Validate inputs
        if not isinstance(user_roles, list):
            return {'allowed': False, 'matched_role': None, 'error': 'user_roles must be a list'}
        
        if not required_permission:
            return {'allowed': False, 'matched_role': None, 'error': 'required_permission cannot be empty'}
        
        if not isinstance(role_permissions, dict):
            return {'allowed': False, 'matched_role': None, 'error': 'role_permissions must be a dict'}
        
        # Check each user role
        for role in user_roles:
            permissions = role_permissions.get(role, [])
            if required_permission in permissions:
                return {
                    'allowed': True,
                    'matched_role': role,
                    'error': None
                }
        
        # No matching permission found
        return {
            'allowed': False,
            'matched_role': None,
            'error': None
        }
    
    except Exception as e:
        return {'allowed': False, 'matched_role': None, 'error': f'Permission check failed: {str(e)}'}
