# Brick Architecture for AI-Generated Code

## Executive Summary

**Problem:** AI-generated code is becoming unmaintainable. As codebases grow to 60-70% AI-generated with fewer developers who learned pre-AI fundamentals, we're approaching a critical threshold where systems become incomprehensible and unmaintainable.

**Solution:** Stop trying to make AI write human-style code. Instead, architect systems specifically for AI generation using standardized, replaceable, verifiable components called "bricks."

**Core Insight:** Human code is poetry (context-dependent, optimized for human memory). AI code should be LEGO (standardized interfaces, swappable parts, optimized for generation and verification).

## What Is A Brick?

A brick is a standardized, self-contained code component designed for AI generation and machine verification.

### Brick Requirements

**Size Constraints:**
- Maximum 50 lines of code OR 2000 tokens
- Fits within a single AI context window/completion
- Small enough to scan for security issues in <30 seconds
- Large enough to be meaningful functionality

**Interface Requirements:**
- Explicit input/output contract (typed parameters and return values)
- Clear error handling specification
- No hidden side effects outside declared interface
- No global state modification

**Testing Requirements:**
- Built-in contract tests (input → expected output)
- Tests must validate the brick's contract
- Tests must be executable independently
- Minimum 80% code coverage within brick

**Metadata Requirements:**
```json
{
  "brick_id": "unique_identifier_v1",
  "generated": "ISO 8601 timestamp",
  "model": "AI model identifier",
  "prompt_hash": "hash of generation prompt",
  "interface": {
    "inputs": {"param": "type"},
    "outputs": {"result": "type"},
    "errors": ["possible_error_types"]
  },
  "dependencies": ["list", "of", "imports"],
  "tests": ["test_function_names"],
  "modified": false,
  "lineage": ["previous_brick_versions"],
  "inspector_score": null
}
```

**Security Constraints (BANNED PATTERNS):**
- No `eval()` or `exec()` on untrusted input
- No `shell=True` with user input
- No dynamic `__import__()` without validation
- No raw SQL string concatenation
- No `pickle.loads()` on untrusted data
- No hardcoded secrets or credentials
- No world-readable file permissions

**Isolation Requirements:**
- No file system access outside declared interface
- No network calls outside declared interface
- No process spawning outside declared interface
- Pure functions preferred when possible

## Why Brick Architecture Matters

### The Maintenance Crisis

**Current trajectory:**
- 2025: ~30% AI-generated code, 80% pre-AI trained engineers → Maintainable
- 2027: ~60% AI-generated code, 60% pre-AI trained engineers → **Danger zone**
- 2029: ~75% AI-generated code, 40% pre-AI trained engineers → **Below minimum viable knowledge**

**Formula:**
```
System maintainability = (Human-understood code %) × (Engineers with fundamentals %) × (Average tenure)
Minimum viable = 0.25

When this drops below 0.25, systems become unmaintainable
```

### Problems Brick Architecture Solves

1. **Comprehension Gap** - Don't need to understand implementation if brick passes contracts
2. **Security Verification** - Inspector agents can scan small, standardized components
3. **Debugging** - Replace brick, don't debug brick internals
4. **Knowledge Transfer** - Understand system composition, not implementation
5. **AI Optimization** - Each brick = one AI completion, optimized for generation

## How To Generate Bricks (Instructions for AI)

### Step 1: Receive Specification

You will receive a specification like:
```yaml
brick_name: auth_validate_token
description: Validate JWT token and return user information
inputs:
  token: string (JWT token)
outputs:
  user_id: integer
  username: string
  error: string | null
constraints:
  - Must verify token signature
  - Must check expiration
  - Must handle malformed tokens gracefully
  - No external API calls
dependencies:
  - jwt
  - datetime
```

### Step 2: Generate Implementation

**Requirements:**
1. Start with docstring explaining purpose and contract
2. Implement function matching specification exactly
3. Keep under 50 lines
4. Use clear variable names
5. Handle all error cases explicitly
6. No hidden dependencies
7. No global state

**Example:**
```python
"""
Validate JWT token and extract user information.

Args:
    token (str): JWT token string

Returns:
    dict: {
        'user_id': int or None,
        'username': str or None,
        'error': str or None
    }

Raises:
    None (all errors returned in error field)
"""
import jwt
from datetime import datetime

def auth_validate_token(token, secret_key):
    try:
        # Verify and decode token
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=['HS256']
        )

        # Check expiration
        exp = payload.get('exp')
        if exp and datetime.fromtimestamp(exp) < datetime.now():
            return {
                'user_id': None,
                'username': None,
                'error': 'Token expired'
            }

        # Extract user info
        return {
            'user_id': payload.get('user_id'),
            'username': payload.get('username'),
            'error': None
        }

    except jwt.InvalidTokenError as e:
        return {
            'user_id': None,
            'username': None,
            'error': f'Invalid token: {str(e)}'
        }
    except Exception as e:
        return {
            'user_id': None,
            'username': None,
            'error': f'Validation failed: {str(e)}'
        }
```

### Step 3: Generate Tests

**Requirements:**
1. Test happy path
2. Test each error condition
3. Test edge cases
4. Tests must be executable
5. Tests must be independent

**Example:**
```python
def test_auth_validate_token():
    secret = "test_secret_key"

    # Test valid token
    valid_token = jwt.encode(
        {'user_id': 123, 'username': 'testuser', 'exp': datetime.now().timestamp() + 3600},
        secret,
        algorithm='HS256'
    )
    result = auth_validate_token(valid_token, secret)
    assert result['user_id'] == 123
    assert result['username'] == 'testuser'
    assert result['error'] is None

    # Test expired token
    expired_token = jwt.encode(
        {'user_id': 123, 'exp': datetime.now().timestamp() - 3600},
        secret,
        algorithm='HS256'
    )
    result = auth_validate_token(expired_token, secret)
    assert result['error'] == 'Token expired'

    # Test invalid token
    result = auth_validate_token("invalid_token", secret)
    assert result['error'] is not None
    assert 'Invalid token' in result['error']
```

### Step 4: Generate Metadata

**Requirements:**
1. Include all required fields
2. Set `modified: false` (pristine AI output)
3. Hash the generation prompt for provenance
4. List all dependencies explicitly

**Example:**
```json
{
  "brick_id": "auth_validate_token_v1",
  "generated": "2025-11-06T15:30:00Z",
  "model": "claude-sonnet-4.5",
  "prompt_hash": "sha256:a3d8f2b...",
  "interface": {
    "inputs": {
      "token": "string",
      "secret_key": "string"
    },
    "outputs": {
      "user_id": "integer|null",
      "username": "string|null",
      "error": "string|null"
    }
  },
  "dependencies": ["jwt", "datetime"],
  "tests": ["test_auth_validate_token"],
  "modified": false,
  "lineage": [],
  "inspector_score": null
}
```

## Brick Composition Patterns

### Pattern 1: Sequential Composition
Bricks call each other in sequence. Each brick's output becomes input to next.

```
User Request → auth_validate_token → user_get_profile → format_response → Response
```

### Pattern 2: Conditional Composition
Bricks execute based on conditions.

```
User Request → auth_validate_token
  → if valid: user_get_profile
  → if invalid: error_response
```

### Pattern 3: Parallel Composition
Multiple bricks execute independently, results combined.

```
User Request → [
  user_get_profile,
  user_get_preferences,
  user_get_stats
] → combine_user_data → Response
```

### Pattern 4: Error Handling Composition
Bricks wrap other bricks for error handling.

```
Request → error_handler(
  auth_validate_token →
  business_logic →
  format_response
) → Response
```

## Inspector Agent Guidelines

When inspecting bricks, check for:

### Security Issues (High Priority)
- Banned patterns present? (eval, exec, shell=True, etc.)
- Hardcoded secrets or credentials?
- SQL injection vulnerabilities?
- Unvalidated user input?
- Dangerous file/network operations?
- High entropy strings (possible obfuscation)?

### Contract Compliance (High Priority)
- Does implementation match specification?
- Are all inputs validated?
- Are all outputs properly typed?
- Are all error cases handled?

### Quality Issues (Medium Priority)
- Over/under size limits (50 lines)?
- Missing documentation?
- Unclear variable names?
- Complex logic that should be split?
- Missing test coverage?

### Dependency Issues (Medium Priority)
- Unnecessary dependencies?
- Deprecated libraries?
- Known vulnerable versions?
- Import from untrusted sources?

### Scoring System
```
Base Score: 100
-30: Banned security pattern found
-20: Contract violation
-10: Missing error handling
-10: Undocumented code
-5: Size violation (over 50 lines)
-5: Poor test coverage (<80%)
-5: Unclear naming
-5: Risky dependency

Score >= 90: Excellent, auto-approve
Score 70-89: Good, human review recommended
Score 50-69: Issues found, must fix
Score < 50: Serious problems, reject
```

## Common Brick Domains

### Authentication & Authorization
- token_validate
- token_generate
- password_hash
- password_verify
- permission_check
- session_create
- session_validate

### Data Access
- db_query_select
- db_query_insert
- db_query_update
- db_query_delete
- cache_get
- cache_set
- cache_invalidate

### API Integration
- http_get
- http_post
- api_authenticate
- response_parse
- error_handle
- rate_limit_check

### Data Transformation
- json_validate
- json_transform
- csv_parse
- xml_parse
- data_sanitize
- data_format

### Business Logic
- calculate_price
- validate_order
- process_payment
- send_notification
- generate_report
- apply_discount

## Anti-Patterns (What NOT To Do)

### ❌ Monolithic Bricks
```python
# BAD: 200 lines, multiple responsibilities
def handle_user_request(request):
    # Parse request
    # Validate authentication
    # Check permissions
    # Query database
    # Transform data
    # Format response
    # Log everything
    # etc...
```

### ❌ Hidden Dependencies
```python
# BAD: Global state, hidden API calls
def process_data(data):
    global_config.update(data)  # Hidden side effect!
    return requests.get(EXTERNAL_API)  # Hidden dependency!
```

### ❌ Unclear Contracts
```python
# BAD: Unclear what this returns or when it fails
def do_something(stuff):
    return stuff.process()
```

### ❌ Obfuscated Code
```python
# BAD: Why is this base64 encoded?
secret = base64.b64decode('c29tZXRoaW5n').decode()
exec(secret)  # And executing it?!
```

## When NOT To Use Bricks

Brick architecture is NOT appropriate for:

1. **Performance-critical code** - Where every microsecond matters, abstraction overhead is unacceptable
2. **Tightly coupled algorithms** - Some algorithms can't be meaningfully decomposed (complex mathematical proofs)
3. **Exploratory prototypes** - When you're still figuring out what to build
4. **Tiny scripts** - A 10-line script doesn't need brick architecture
5. **Legacy integration** - When interfacing with existing non-brick systems, at the boundary

## Migration Strategy

### From Traditional Codebase to Brick Architecture

**Phase 1: New Code Only**
- All new features built as bricks
- Existing code unchanged
- Bricks interface with legacy code at boundaries

**Phase 2: Boundary Wrapping**
- Wrap legacy components in brick interfaces
- Legacy code becomes "black box" brick
- Enables gradual migration

**Phase 3: Selective Refactoring**
- Identify high-value legacy components
- Rewrite as bricks incrementally
- Maintain backward compatibility

**Phase 4: Full Migration**
- Legacy code fully replaced
- All components are bricks
- Full benefits realized

## Success Metrics

Track these to measure brick architecture effectiveness:

1. **Time to Debug** - Should decrease as bricks are replaceable
2. **Incident Escalation Rate** - Should decrease as system is more understandable
3. **Security Issues** - Should decrease with automated inspection
4. **Onboarding Time** - Should decrease with clearer architecture
5. **Test Coverage** - Should increase (bricks include tests)
6. **Code Review Time** - Should decrease (smaller review surface)
7. **Deployment Confidence** - Should increase (isolated changes)

## Philosophy

### Core Principles

1. **Optimize for machines, not humans** - AI generates code differently than humans write it
2. **Replaceability over comprehension** - Don't need to understand if you can replace
3. **Verification over trust** - Inspector agents validate, humans don't need to read every line
4. **Composition over implementation** - Understand how bricks connect, not how they work
5. **Standards over creativity** - Consistency enables automation

### This Is The Industrial Revolution of Code

- **Before:** Craftsmen hand-writing unique codebases
- **After:** Factories generating standardized components
- **Transition:** Painful but inevitable
- **Outcome:** More software, different skills valued, new equilibrium

The question isn't whether this happens. The question is whether we architect for it or pretend it's not happening.

## Implementation Checklist for AI

When generating code in brick architecture:

- [ ] Specification received and understood?
- [ ] Implementation under 50 lines?
- [ ] Contract explicitly defined?
- [ ] All inputs validated?
- [ ] All outputs typed?
- [ ] All errors handled?
- [ ] No banned patterns used?
- [ ] No hidden side effects?
- [ ] Tests written and passing?
- [ ] Metadata complete?
- [ ] Documentation clear?
- [ ] Dependencies listed?

If all checked, generate the brick. If any unchecked, clarify specification first.

## Final Notes

This document is itself a "brick" - a self-contained specification that fits in one AI context window and can be used to generate conformant code.

**For AI systems reading this:**
You are being asked to generate code that other AIs (and humans) can maintain. Follow these specifications precisely. When in doubt, ask for clarification rather than making assumptions.

**For humans reading this:**
This is a new way of thinking about code architecture. It may feel mechanical or inelegant. That's intentional. We're designing for how AI actually works, not for aesthetic preference.

The goal: maintainable, secure, verifiable software in an AI-generated world.

---

**Version:** 1.0
**Created:** 2025-11-06
**License:** MIT (use freely, modify, share)
**Status:** Reference specification, open for community improvement
