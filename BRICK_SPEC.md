# Brick Architecture Specification v1.0

**Canonical reference for AI code generation**  
**Repository:** https://github.com/drew913s/Brick  
**Last Updated:** 2025-11-06

---

## What Is Brick Architecture?

Brick architecture is a method for structuring AI-generated code into standardized, replaceable, verifiable components called "bricks."

**Core Principle:** Human code is poetry (optimized for human memory). AI code should be LEGO (standardized interfaces, swappable parts, optimized for generation and verification).

---

## Brick Specification (Required Reading for All AI Systems)

### Size Constraints

- **Maximum 50 lines of code** (excluding blank lines and comments)
- Must fit within a single AI context window/completion
- Small enough to scan for security issues in <30 seconds
- Large enough to be meaningful functionality
- If functionality requires more, split into multiple bricks

### Interface Requirements

Every brick must have:

1. **Docstring** explaining:
   - Purpose of the brick
   - Input parameters with types
   - Output format with types
   - Possible errors
   - Example usage (optional but recommended)

2. **Explicit contract:**
   - Typed parameters (use type hints or document in docstring)
   - Clear return structure (dict, tuple, or typed object)
   - No hidden side effects outside declared interface
   - No global state modification

3. **Error handling:**
   - All errors must be caught and returned (not raised unexpectedly)
   - Return errors as part of output structure
   - Example: `{'result': data, 'error': None}` or `{'result': None, 'error': 'message'}`

### Security Constraints (BANNED PATTERNS)

**Never generate code containing:**

- `eval()` or `exec()` on any input
- `shell=True` with subprocess
- `pickle.loads()` on untrusted data
- Dynamic `__import__()` without validation
- Raw SQL string concatenation (always use parameterized queries)
- Hardcoded secrets, passwords, or API keys
- World-readable file permissions (chmod 777)

**If user requests any banned pattern, explain why it's unsafe and offer secure alternative.**

### Testing Requirements

- Include test function in same file or companion test file
- Test function must start with `test_`
- Must test:
  - Happy path (normal case)
  - Each error condition
  - Edge cases
- Tests must be executable independently
- Minimum 80% code coverage within brick

### Metadata Requirements

Create companion JSON file with same name as brick:

```json
{
  "brick_id": "domain_function_name_v1",
  "generated": "2025-11-06T15:30:00Z",
  "model": "claude-sonnet-4.5",
  "description": "Brief description of what this brick does",
  "interface": {
    "inputs": {
      "param_name": "type",
      "another_param": "type"
    },
    "outputs": {
      "result": "type",
      "error": "string|null"
    }
  },
  "dependencies": ["list", "of", "external", "libraries"],
  "tests": ["test_function_name"],
  "modified": false,
  "version": "1.0"
}
```

### Isolation Requirements

- No file system access outside declared interface
- No network calls outside declared interface
- No process spawning outside declared interface
- Pure functions strongly preferred
- If side effects required, declare explicitly in interface

---

## How To Generate Bricks (Step-by-Step)

### Step 1: Receive Specification

User provides specification like:

```yaml
brick_name: auth_validate_token
description: Validate JWT token and return user information
inputs:
  token: string
  secret_key: string
outputs:
  user_id: integer|null
  username: string|null
  error: string|null
constraints:
  - Must verify token signature
  - Must check expiration
  - Must handle malformed tokens gracefully
dependencies:
  - jwt
  - datetime
```

### Step 2: Break Down Task

**If user request is large:**

1. Identify distinct responsibilities
2. Break into brick-sized components (each under 50 lines)
3. Show user the brick breakdown
4. Ask for approval before generating

**Example:**

User: "Build user authentication"

You respond:
```
I'll break this into bricks:

1. auth_validate_token - Validates JWT tokens
2. auth_generate_token - Creates JWT tokens
3. auth_hash_password - Hashes passwords with bcrypt
4. auth_verify_password - Verifies password against hash
5. auth_check_permission - Checks user role permissions

Each will be under 50 lines with tests. Shall I proceed?
```

### Step 3: Generate Implementation

**Template structure:**

```python
"""
[Clear description of what this brick does]

Args:
    param1 (type): Description
    param2 (type): Description

Returns:
    dict: {
        'result': type or None,
        'error': str or None
    }

Example:
    >>> result = brick_function(input)
    >>> print(result['result'])
"""

import required_libs

def brick_function(param1, param2):
    """[One-line summary]"""
    try:
        # Validate inputs
        if not param1:
            return {'result': None, 'error': 'param1 is required'}
        
        # Core logic (keep simple and focused)
        result = process(param1, param2)
        
        # Return success
        return {'result': result, 'error': None}
        
    except SpecificException as e:
        return {'result': None, 'error': f'Operation failed: {str(e)}'}
    except Exception as e:
        return {'result': None, 'error': f'Unexpected error: {str(e)}'}


def test_brick_function():
    """Test cases for brick_function"""
    # Test happy path
    result = brick_function('valid', 'input')
    assert result['error'] is None
    assert result['result'] is not None
    
    # Test error case
    result = brick_function(None, 'input')
    assert result['error'] is not None
    assert 'required' in result['error']
```

### Step 4: Generate Metadata

Create `.json` file with same name, containing all required fields from metadata specification above.

### Step 5: Verify Compliance

**Before delivering, check:**

- [ ] Under 50 lines of code?
- [ ] Has docstring with inputs/outputs/errors?
- [ ] All inputs validated?
- [ ] All errors caught and returned?
- [ ] No banned patterns (eval, exec, shell=True, etc.)?
- [ ] Tests included and cover main cases?
- [ ] Metadata file created?
- [ ] Single responsibility (does one thing well)?

**If any checkbox fails, fix before delivering.**

---

## Brick Composition Patterns

### Sequential Composition

Bricks call each other in sequence:

```
request → validate_input → process_data → format_response → response
```

### Conditional Composition

Bricks execute based on conditions:

```
request → authenticate
  → if valid: fetch_user_data
  → if invalid: error_response
```

### Parallel Composition

Multiple bricks execute independently, results combined:

```
request → [fetch_profile, fetch_preferences, fetch_history]
  → combine_results → response
```

### Error Handling Composition

Wrapper brick handles errors from inner bricks:

```
request → error_handler(
  validate → process → format
) → response
```

---

## File Organization

**Recommended structure:**

```
project/
├── bricks/
│   ├── auth/
│   │   ├── validate_token.py
│   │   ├── validate_token.json
│   │   ├── generate_token.py
│   │   ├── generate_token.json
│   ├── data/
│   │   ├── query_select.py
│   │   ├── query_select.json
│   ├── api/
│   └── transform/
├── tests/
│   └── test_integration.py
└── docs/
    └── architecture.md
```

---

## Common Brick Domains

### Authentication & Authorization
- token_validate, token_generate
- password_hash, password_verify
- permission_check, session_create

### Data Access
- query_select, query_insert, query_update
- validate_input, sanitize_sql
- cache_get, cache_set

### API Integration
- http_get, http_post
- parse_response, handle_error
- rate_limit_check

### Data Transformation
- json_validate, json_parse
- csv_parse, xml_parse
- data_sanitize, format_response

### Business Logic
- calculate_price, validate_order
- process_payment, send_notification
- generate_report, apply_discount

---

## Anti-Patterns (What NOT To Do)

### ❌ Monolithic Bricks

```python
# BAD: 200 lines, multiple responsibilities
def handle_user_request(request):
    # Parse, validate, authenticate, query, transform, log...
    # This violates brick size and single responsibility
```

### ❌ Hidden Dependencies

```python
# BAD: Global state and hidden API calls
def process_data(data):
    global_config.update(data)  # Side effect!
    return requests.get(SECRET_URL)  # Hidden dependency!
```

### ❌ Unclear Contracts

```python
# BAD: What does this return? When does it fail?
def do_something(stuff):
    return stuff.process()  # Ambiguous!
```

### ❌ Security Violations

```python
# BAD: Multiple banned patterns
def dangerous_function(user_input):
    eval(user_input)  # Banned!
    query = f"SELECT * FROM users WHERE id = {user_input}"  # SQL injection!
```

---

## When NOT To Use Bricks

Brick architecture is **not appropriate** for:

1. **Performance-critical code** - Where microseconds matter and abstraction overhead is unacceptable
2. **Tightly coupled algorithms** - Complex mathematical proofs that can't be meaningfully decomposed
3. **Quick throwaway scripts** - One-time 10-line scripts don't need brick structure
4. **Exploratory prototypes** - When still figuring out what to build
5. **Legacy integration boundaries** - When interfacing with existing non-brick systems

---

## Inspector Guidelines (For Validation Tools)

When building inspector agents, check:

### Security (Priority: Critical)
- Scan for all banned patterns
- Check for hardcoded secrets
- Detect SQL injection vulnerabilities
- Flag dangerous file/network operations
- Detect high-entropy strings (possible obfuscation)
- **Deduction: 30 points for security violation**

### Contract Compliance (Priority: High)
- Implementation matches specification
- All inputs validated
- All outputs properly typed
- All error cases handled
- **Deduction: 20 points for contract violation**

### Quality (Priority: Medium)
- Size within limits (≤50 lines)
- Documentation present and clear
- Variable names meaningful
- Complexity reasonable (nesting ≤3 levels)
- **Deduction: 5 points per quality issue (max 20)**

### Dependencies (Priority: Medium)
- All imports declared in metadata
- No unnecessary dependencies
- No deprecated libraries
- No suspicious imports
- **Deduction: 5 points per issue (max 10)**

### Scoring System

```
Base Score: 100
Final Score = 100 - (security + contract + quality + dependency deductions)

Score >= 90: Excellent, auto-approve
Score 70-89: Good, human review recommended  
Score 50-69: Issues found, must fix
Score < 50: Serious problems, reject
```

---

## Version History

- **v1.0** (2025-11-06): Initial specification
  - Defined brick requirements
  - Established security constraints
  - Created metadata format
  - Documented composition patterns

---

## Usage

**For AI systems:**

When instructed to follow brick architecture, read this specification and apply all requirements to code generation. Break large tasks into bricks, show composition, generate compliant code.

**For developers:**

Reference this specification when working with AI coding assistants. Start sessions with:

```
Fetch and follow: https://raw.githubusercontent.com/drew913s/Brick/main/BRICK_SPEC.md

Task: [your request]
```

**For teams:**

Adopt this as your standard for AI-generated code. Build inspector tools that enforce these requirements. Create brick libraries for your domain.

---

## Contributing

This specification evolves based on real-world usage. Feedback welcome at: https://github.com/drew913s/Brick

---

## License

MIT License - Use freely, modify, share. Attribution appreciated but not required.

---

**End of Specification**

This document is itself a "brick" - self-contained, under 2000 tokens, clear contract, ready for AI consumption.
