---
name: Wrapper Brick Task
about: Create brick wrapper for existing/legacy code
title: '[WRAPPER] '
labels: worker, wrapper
assignees: ''
---

## Wrapper Brick Task

**Task ID:** Q-{DOMAIN}-{N}
**Parent Domain:** Q-{DOMAIN}
**Parent Issue:** #{PARENT_ISSUE_NUMBER}

---

## Legacy Function to Wrap

**Module:** `module.submodule`
**Function:** `function_name()`
**File:** `path/to/file.py`
**Line:** 

```python
# Existing signature
def function_name(param1: type, param2: type) -> ReturnType:
    """
    [Copy existing docstring here]
    """
```

---

## Known Behaviors

**Returns:**
- On success: 
- On failure: 

**Raises:**
- `ExceptionType`: When...
- `ExceptionType`: When...

**Side effects:**
- (none / list any)

---

## New Brick Interface

**Brick name:** `{domain}_{function_name}`
**File:** `bricks/{domain}/{brick_name}.py`

```python
def brick_name(param1: type, param2: type) -> dict:
    """
    Wrapper for legacy function_name.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        dict: {'result': X, 'error': str|None}
    
    Raises:
        Nothing - all exceptions caught
    """
```

---

## Wrapper Requirements

- [ ] Import from legacy module: `from module.submodule import function_name`
- [ ] Call legacy function with same params
- [ ] Convert return value to brick dict format
- [ ] Catch `ExceptionType` → `{'result': None, 'error': 'message'}`
- [ ] Catch all other exceptions → `{'result': None, 'error': 'Unexpected: {e}'}`
- [ ] NO modifications to legacy code

---

## Test Requirements

Using mocks (don't depend on legacy code working):

- [ ] Test success path (mock returns success value)
- [ ] Test failure path (mock returns failure value)
- [ ] Test exception handling (mock raises ExceptionType)
- [ ] Test unexpected exception (mock raises Exception)

Optional integration test:
- [ ] One real call to verify wrapper connects properly

---

## File Ownership

**This task CREATES:**
- [ ] `bricks/{domain}/{brick_name}.py` (NEW)
- [ ] `bricks/{domain}/{brick_name}.meta.json` (NEW)
- [ ] `bricks/{domain}/test_{brick_name}.py` (NEW)

**This task MODIFIES:**
- (none)

**OFF LIMITS (do not touch):**
- `path/to/legacy/file.py`
- All other legacy files

---

## Access Method

**HUMAN tests this by:**

```bash
# Run wrapper tests (with mocks)
python -m pytest bricks/{domain}/test_{brick_name}.py -v

# Optional: Integration test
python -c "from bricks.{domain}.{brick_name} import {brick_name}; print({brick_name}(test_input))"
```

**Success looks like:**
All tests pass, wrapper returns dict with 'result' and 'error' keys.

**Failure looks like:**
Import error, exception not caught, wrong return format.

---

## Progress Log

_Worker updates here every 30 minutes_

<!-- 
## Progress Update - YYYY-MM-DDTHH:MM
**Status:** Working | Blocked | Complete
**Done:** 
**Current:**
**Blockers:**
**Files:**
-->
