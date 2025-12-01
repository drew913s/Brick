# Working With Existing Code

**Applying ant colony orchestration to legacy and existing codebases**  
**Repository:** https://github.com/drew913s/Brick  
**Last Updated:** 2025-12-01

---

## The Problem

You have existing code. It's not in brick format. Files are 500+ lines. No clear interfaces. Tests are spotty or missing. You want to use the ant colony model without rewriting everything from scratch.

---

## Strategy: Wrap, Then Migrate

**Don't rewrite. Wrap first, migrate incrementally.**

```
Phase 1: AUDIT     → Understand what exists
Phase 2: WRAP      → Create brick interfaces around existing code
Phase 3: TEST      → Ensure wrappers work
Phase 4: MIGRATE   → Replace internals with proper bricks (optional)
```

---

## Phase 1: Audit (Queen Role)

### Audit Bootstrap Prompt

```markdown
# Session: Q (Queen - Audit Mode)

You are auditing an existing codebase to plan brick migration.

## Your Identity
- **ID:** Q
- **Role:** Auditor/Architect
- **Code:** NONE (analysis only)

## Your Job
1. Map the existing code structure
2. Identify logical domains
3. Find integration points
4. Assess brick-readiness of each component
5. Create migration plan as GitHub issues

## Output: Codebase Map

For each major file/module, document:
- Purpose (what it does)
- Size (lines, complexity)
- Dependencies (what it imports)
- Dependents (what imports it)
- Brick-ready? (Y/N/Partial)
- Migration priority (High/Med/Low)

## Output: Domain Map

Group files into logical domains:
- Domain name
- Files included
- Entry points (what external code calls)
- Exit points (what it calls externally)

## Output: Migration Issues

Create GitHub issues for:
1. Each domain that needs a Princess
2. Known problem areas
3. Files that need immediate attention
4. Integration points that need wrapper bricks

## Rules
- NO CODE changes
- Document everything in GitHub
- Be honest about complexity
- Flag files that are "too scary to touch"

## Codebase Location
[PASTE REPO PATH OR STRUCTURE HERE]
```

### Audit Output Template

```markdown
## Codebase Audit - [Project Name]

### Structure Overview
```
src/
├── auth/           # 3 files, ~400 lines total
├── api/            # 8 files, ~1200 lines total  
├── models/         # 5 files, ~600 lines total
├── utils/          # 12 files, ~800 lines total (mixed bag)
└── legacy/         # 4 files, ~2000 lines (here be dragons)
```

### Domain Assessment

| Domain | Files | Lines | Brick-Ready | Priority | Notes |
|--------|-------|-------|-------------|----------|-------|
| auth | 3 | 400 | Partial | High | Clean interfaces, big internals |
| api | 8 | 1200 | No | High | Tightly coupled to models |
| models | 5 | 600 | Yes | Med | Already small, clean |
| utils | 12 | 800 | Mixed | Low | Some good, some garbage |
| legacy | 4 | 2000 | No | Low | Don't touch unless necessary |

### Critical Files

| File | Lines | Risk | Notes |
|------|-------|------|-------|
| auth/handler.py | 280 | High | Does 5 things, needs splitting |
| api/routes.py | 450 | High | All routes in one file |
| legacy/processor.py | 800 | Extreme | Nobody understands this |
| utils/helpers.py | 200 | Med | Used everywhere |

### Recommended Approach
1. Wrap auth/ first (clean boundary)
2. Create API route bricks (high value)
3. Leave legacy/ alone (wrap at boundary)
4. Refactor utils/ as needed
```

---

## Phase 2: Wrap (Princess Role)

### Wrapper Strategy

**Don't refactor internals. Create brick interfaces that call existing code.**

```python
# BEFORE: 300-line auth handler
# File: auth/handler.py (legacy, don't touch)

# AFTER: Brick wrapper
# File: bricks/auth/validate_user.py (new, 40 lines)

"""
Wrapper brick for legacy auth validation.

Wraps: auth.handler.validate_user_credentials()

Args:
    username (str): User's username
    password (str): User's password

Returns:
    dict: {'user_id': int|None, 'error': str|None}
"""
from auth.handler import validate_user_credentials


def auth_validate_user(username, password):
    """Brick interface to legacy auth validation."""
    try:
        # Call legacy code
        result = validate_user_credentials(username, password)
        
        # Normalize output to brick format
        if result.success:
            return {'user_id': result.user_id, 'error': None}
        else:
            return {'user_id': None, 'error': result.message}
    
    except Exception as e:
        return {'user_id': None, 'error': f'Auth failed: {str(e)}'}


def test_auth_validate_user():
    """Test wrapper brick."""
    # Test with known test credentials
    result = auth_validate_user('testuser', 'testpass')
    assert 'user_id' in result
    assert 'error' in result
```

### Wrapper Princess Bootstrap

```markdown
# Session: Q-{DOMAIN} (Princess - Wrapper Mode)

You are creating brick wrappers for existing code in {DOMAIN}.

## Your Identity
- **ID:** Q-{DOMAIN}
- **Role:** Wrapper architect
- **Code:** Wrapper bricks only

## Your Job
1. Read the audit for this domain
2. Identify public interfaces in existing code
3. Create wrapper brick tasks (one per interface)
4. Wrappers call existing code, normalize output

## Wrapper Brick Rules
- DO NOT modify existing code
- Import and call existing functions
- Normalize outputs to brick format: `{'result': X, 'error': str|None}`
- Handle exceptions from legacy code
- Add tests that verify wrapper works

## Output
Create GitHub issues for wrapper bricks:
- One issue per public interface
- Include: what to wrap, expected inputs/outputs
- Mark as `wrapper` label

## Domain Audit
[PASTE DOMAIN AUDIT SECTION HERE]

## Existing Code Location
[PASTE FILE PATHS HERE]
```

### Wrapper Task Template

```markdown
## Wrapper Brick Task

**Wrap:** `auth.handler.validate_user_credentials()`
**New brick:** `bricks/auth/validate_user.py`

### Existing Interface
```python
# In auth/handler.py, line 45
def validate_user_credentials(username: str, password: str) -> AuthResult:
    """
    Returns AuthResult with .success, .user_id, .message
    Raises: DatabaseError, ValidationError
    """
```

### Brick Interface
```python
def auth_validate_user(username: str, password: str) -> dict:
    """
    Returns: {'user_id': int|None, 'error': str|None}
    Raises: Nothing (catches all exceptions)
    """
```

### Wrapper Requirements
- [ ] Import from `auth.handler`
- [ ] Call `validate_user_credentials()`
- [ ] Convert `AuthResult` to dict format
- [ ] Catch `DatabaseError` → `{'error': 'Database unavailable'}`
- [ ] Catch `ValidationError` → `{'error': 'Invalid credentials'}`
- [ ] Catch all other → `{'error': 'Auth failed: {message}'}`

### Test Requirements
- [ ] Test success case (if test credentials exist)
- [ ] Test invalid credentials
- [ ] Test wrapper handles exceptions
```

---

## Phase 3: Test (Ant Role)

### Wrapper Testing Strategy

**Test the wrapper, not the legacy code.**

```python
"""
Tests for auth_validate_user wrapper brick.

These tests verify the WRAPPER works correctly.
They do NOT test the legacy auth.handler internals.
"""
from unittest.mock import patch, MagicMock
from bricks.auth.validate_user import auth_validate_user


def test_wrapper_success():
    """Test wrapper returns correct format on success."""
    # Mock the legacy function
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.user_id = 123
    
    with patch('bricks.auth.validate_user.validate_user_credentials') as mock:
        mock.return_value = mock_result
        result = auth_validate_user('user', 'pass')
    
    assert result['user_id'] == 123
    assert result['error'] is None


def test_wrapper_failure():
    """Test wrapper returns correct format on failure."""
    mock_result = MagicMock()
    mock_result.success = False
    mock_result.message = 'Invalid password'
    
    with patch('bricks.auth.validate_user.validate_user_credentials') as mock:
        mock.return_value = mock_result
        result = auth_validate_user('user', 'wrongpass')
    
    assert result['user_id'] is None
    assert result['error'] == 'Invalid password'


def test_wrapper_handles_exception():
    """Test wrapper catches legacy exceptions."""
    with patch('bricks.auth.validate_user.validate_user_credentials') as mock:
        mock.side_effect = Exception('Database exploded')
        result = auth_validate_user('user', 'pass')
    
    assert result['user_id'] is None
    assert 'Database exploded' in result['error']
```

---

## Phase 4: Migrate (Optional)

### When to Actually Migrate

| Situation | Action |
|-----------|--------|
| Legacy code works fine | Keep wrapper, don't migrate |
| Legacy code has bugs | Fix via new brick, swap wrapper |
| Legacy code is slow | Optimize in new brick, swap wrapper |
| Legacy code is security risk | Rewrite as brick, swap wrapper |
| Adding features to legacy | Write brick, compose with wrapper |

### Migration Pattern

```python
# Step 1: Wrapper calls legacy
def auth_validate_user(username, password):
    from auth.handler import validate_user_credentials
    result = validate_user_credentials(username, password)
    # ... normalize ...

# Step 2: Write new brick implementation
def auth_validate_user_v2(username, password):
    # New, clean implementation
    # ... proper brick code ...

# Step 3: Swap (wrapper now calls new brick)
def auth_validate_user(username, password):
    return auth_validate_user_v2(username, password)

# Step 4: Remove wrapper, use v2 directly
# Update all callers to use auth_validate_user_v2
# Delete wrapper
```

### Gradual Migration Bootstrap

```markdown
# Session: Q-{DOMAIN}-{N} (Ant - Migration Mode)

You are migrating a wrapper brick to a proper implementation.

## Your Identity
- **ID:** Q-{DOMAIN}-{N}
- **Role:** Migration worker
- **Code:** YES - replacement brick

## Your Job
1. Read the existing wrapper brick
2. Read the legacy code it wraps
3. Write a new brick that does the same thing
4. New brick must pass same tests as wrapper
5. DO NOT modify the wrapper yet

## Migration Rules
- New brick must have identical interface to wrapper
- New brick must pass all wrapper tests
- Keep wrapper working during migration
- Only swap after new brick verified

## Wrapper Location
[PATH TO WRAPPER BRICK]

## Legacy Code Location  
[PATH TO LEGACY CODE]

## Tests Location
[PATH TO WRAPPER TESTS]
```

---

## Handling Common Legacy Patterns

### Monster File (500+ lines, does everything)

**Don't try to understand it. Wrap the entry points.**

```markdown
## Monster File Strategy

File: `legacy/processor.py` (800 lines)

### Step 1: Find entry points
What external code calls into this file?
- `process_order()` called by api/orders.py
- `validate_item()` called by api/items.py
- `calculate_totals()` called by reports/daily.py

### Step 2: Create wrapper for each entry point
- bricks/legacy/process_order.py (wrapper)
- bricks/legacy/validate_item.py (wrapper)
- bricks/legacy/calculate_totals.py (wrapper)

### Step 3: Update callers to use wrappers
- api/orders.py imports from bricks/legacy/
- api/items.py imports from bricks/legacy/
- reports/daily.py imports from bricks/legacy/

### Step 4: Monster file is now isolated
- Nothing calls it directly
- Can migrate one wrapper at a time
- Can eventually delete when all migrated
```

### Circular Dependencies

**Break cycles with interface bricks.**

```markdown
## Circular Dependency

Problem:
- auth/handler.py imports user/profile.py
- user/profile.py imports auth/handler.py

### Solution: Interface brick

Create: bricks/interfaces/user_lookup.py
```python
"""Interface for user lookup. Breaks circular dependency."""

_lookup_impl = None

def register_lookup(impl):
    global _lookup_impl
    _lookup_impl = impl

def lookup_user(user_id):
    if _lookup_impl is None:
        raise RuntimeError('User lookup not registered')
    return _lookup_impl(user_id)
```

### Initialization
```python
# In app startup
from bricks.interfaces.user_lookup import register_lookup
from user.profile import get_user_profile
register_lookup(get_user_profile)
```

### Usage
```python
# auth/handler.py now uses interface
from bricks.interfaces.user_lookup import lookup_user
# Instead of: from user.profile import get_user_profile
```
```

### Global State / Singletons

**Wrap the accessor, not the state.**

```python
# Legacy: global database connection
# File: db/connection.py
_connection = None

def get_connection():
    global _connection
    if _connection is None:
        _connection = create_connection()
    return _connection

# Wrapper brick: bricks/db/get_connection.py
"""
Wrapper for legacy database connection singleton.

Returns:
    dict: {'connection': Connection|None, 'error': str|None}
"""
from db.connection import get_connection as legacy_get_connection


def db_get_connection():
    """Get database connection via legacy singleton."""
    try:
        conn = legacy_get_connection()
        return {'connection': conn, 'error': None}
    except Exception as e:
        return {'connection': None, 'error': str(e)}
```

### No Tests Exist

**Write tests for wrappers, not legacy code.**

```markdown
## No Tests Strategy

Legacy code has no tests. Don't try to add them.

### Step 1: Write wrapper
Wrapper calls legacy code, normalizes output.

### Step 2: Write wrapper tests with mocks
Mock the legacy function, test wrapper behavior.

### Step 3: Write integration test (optional)
One test that calls wrapper with real legacy code.
Just verifies "it doesn't crash."

### Step 4: If migrating later
New brick gets proper unit tests.
Wrapper tests become integration tests.
```

---

## Audit Issue Template

```markdown
---
name: Codebase Audit
about: Initial audit of existing code for brick migration
title: '[AUDIT] '
labels: queen, audit
assignees: ''
---

## Codebase Audit

**Project:** 
**Audited by:** Q (Queen)
**Date:** 

---

## Structure Map

```
[PASTE DIRECTORY TREE]
```

---

## Domain Assessment

| Domain | Files | Lines | Brick-Ready | Priority | Notes |
|--------|-------|-------|-------------|----------|-------|
| | | | | | |

---

## Critical Files

| File | Lines | Risk | Notes |
|------|-------|------|-------|
| | | | |

---

## Migration Plan

### Phase 1: Wrap (High Priority)
- [ ] Domain: 
- [ ] Domain:

### Phase 2: Wrap (Medium Priority)
- [ ] Domain:

### Phase 3: Leave Alone
- [ ] Domain: (reason)

---

## Known Risks

1. 
2. 

---

## Recommended First Steps

1. 
2. 
3. 
```

---

## Wrapper Issue Template

```markdown
---
name: Wrapper Brick Task
about: Create brick wrapper for existing code
title: '[WRAPPER] '
labels: worker, wrapper
assignees: ''
---

## Wrapper Brick Task

**Legacy function:** `module.file.function_name()`
**New brick:** `bricks/{domain}/{brick_name}.py`

---

## Existing Interface

```python
# Location: [file path, line number]
def function_name(param1: type, param2: type) -> ReturnType:
    """
    [existing docstring]
    """
```

**Known exceptions:**
- 
- 

**Known side effects:**
- 

---

## Brick Interface

```python
def brick_name(param1: type, param2: type) -> dict:
    """
    Returns: {'result': X, 'error': str|None}
    Raises: Nothing
    """
```

---

## Wrapper Requirements

- [ ] Import from legacy module
- [ ] Call legacy function
- [ ] Normalize return value to dict
- [ ] Catch exception type: → error message
- [ ] Catch all other: → generic error

---

## Test Requirements

- [ ] Test success case (mock legacy)
- [ ] Test failure case (mock legacy)
- [ ] Test exception handling (mock raises)
- [ ] Integration test (optional, real call)

---

## File Ownership

**CREATES:**
- bricks/{domain}/{brick_name}.py
- bricks/{domain}/{brick_name}.meta.json
- bricks/{domain}/test_{brick_name}.py

**MODIFIES:**
- (none)

**OFF LIMITS:**
- [legacy files - do not touch]
```

---

## Quick Reference

| Scenario | Strategy |
|----------|----------|
| Existing code works | Wrap it, don't rewrite |
| Monster file | Wrap entry points only |
| Circular deps | Interface brick |
| Global state | Wrap accessor |
| No tests | Test wrappers with mocks |
| Need to fix bug | Write new brick, swap wrapper |
| Need new feature | New brick, compose with wrappers |

---

## Labels for Existing Code Work

```
audit       - Codebase audit tasks
wrapper     - Wrapper brick tasks
migration   - Converting wrapper to proper brick
legacy      - Issues related to legacy code
```

---

## Phase Flow for Existing Code

```
1. AUDIT (Queen)
   └── Map codebase
   └── Identify domains
   └── Create migration plan
   
2. WRAP (Princess + Ants)
   └── Princess designs wrappers per domain
   └── Ants write wrapper bricks
   └── Tests verify wrappers work
   
3. STABILIZE (HUMAN)
   └── Test wrapped system
   └── Verify nothing broke
   └── System works with brick interfaces
   
4. MIGRATE (Optional, incremental)
   └── Pick one wrapper to replace
   └── Write proper brick
   └── Swap wrapper internals
   └── Repeat as needed
```

---

## The Golden Rule

**If it works, wrap it. If it's broken, replace it. If it's scary, isolate it.**

Don't refactor working code just because it's ugly. Wrap it, move on, fix what's actually broken.

---
