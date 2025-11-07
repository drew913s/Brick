# Getting Started with Brick Architecture

This tutorial will guide you through using the Brick Architecture system to build maintainable, AI-generated code.

## What is Brick Architecture?

Brick Architecture is a new paradigm for structuring AI-generated code into standardized, replaceable, verifiable components called "bricks." Each brick is:
- **Small**: Under 50 lines of code
- **Self-contained**: Clear inputs/outputs, no hidden dependencies
- **Testable**: Includes embedded tests
- **Secure**: Scanned for vulnerabilities
- **Replaceable**: Can swap out without understanding internals

## Installation

```bash
# Clone the repository
git clone https://github.com/drew913s/Brick.git
cd Brick

# Install dependencies
pip install -r requirements.txt

# Test the CLI
python brick_cli.py --help
```

## Quick Start: Your First Brick Project

### Step 1: Initialize a Project

```bash
python brick_cli.py init my_app
cd my_app
```

This creates a project structure:
```
my_app/
├── bricks/
│   ├── auth/     # Authentication bricks
│   ├── data/     # Data access bricks
│   ├── api/      # API integration bricks
│   └── transform/  # Data transformation bricks
├── tests/
├── specs/
└── README.md
```

### Step 2: Create a Brick Specification

Create `specs/calculate_total.yaml`:

```yaml
brick_name: calculate_total
description: Calculate order total with tax and discount
inputs:
  subtotal: float
  tax_rate: float
  discount_percent: float
outputs:
  total: float
  tax_amount: float
  error: string | null
constraints:
  - Subtotal must be non-negative
  - Tax rate must be 0-100
  - Discount must be 0-100
dependencies:
  - decimal
errors:
  - invalid_subtotal
  - invalid_tax_rate
  - invalid_discount
```

### Step 3: Implement the Brick

Create `bricks/transform/calculate_total.py`:

```python
"""Calculate order total with tax and discount."""
from decimal import Decimal


def calculate_total(subtotal, tax_rate, discount_percent):
    """
    Calculate order total.

    Args:
        subtotal: Order subtotal
        tax_rate: Tax rate as percentage (0-100)
        discount_percent: Discount as percentage (0-100)

    Returns:
        dict: {total: float, tax_amount: float, error: str|None}
    """
    # Validate inputs
    if subtotal < 0:
        return {"total": 0, "tax_amount": 0, "error": "invalid_subtotal"}
    if not 0 <= tax_rate <= 100:
        return {"total": 0, "tax_amount": 0, "error": "invalid_tax_rate"}
    if not 0 <= discount_percent <= 100:
        return {"total": 0, "tax_amount": 0, "error": "invalid_discount"}

    # Calculate
    sub = Decimal(str(subtotal))
    discount = sub * Decimal(str(discount_percent / 100))
    discounted = sub - discount
    tax = discounted * Decimal(str(tax_rate / 100))
    total = discounted + tax

    return {
        "total": float(total),
        "tax_amount": float(tax),
        "error": None
    }


def test_calculate_total():
    """Test valid calculation."""
    result = calculate_total(100.0, 10.0, 20.0)
    assert result["error"] is None
    assert result["total"] == 88.0  # (100 - 20) + 8 tax


def test_calculate_total_invalid():
    """Test invalid inputs."""
    result = calculate_total(-10, 10.0, 0)
    assert result["error"] == "invalid_subtotal"
```

### Step 4: Create Metadata

Create `bricks/transform/calculate_total.meta.json`:

```json
{
  "brick_id": "calculate_total_v1",
  "generated": "2025-11-06T12:00:00Z",
  "model": "manual",
  "interface": {
    "inputs": {
      "subtotal": "float",
      "tax_rate": "float",
      "discount_percent": "float"
    },
    "outputs": {
      "total": "float",
      "tax_amount": "float",
      "error": "string|null"
    }
  },
  "dependencies": ["decimal"],
  "tests": ["test_calculate_total", "test_calculate_total_invalid"],
  "modified": false,
  "lineage": [],
  "inspector_score": null
}
```

### Step 5: Validate Your Brick

```bash
python brick_cli.py validate bricks/transform/calculate_total.py
```

Expected output:
```
Validating: bricks/transform/calculate_total.py

✓ Brick is valid
```

### Step 6: Inspect for Security and Quality

```bash
python brick_cli.py inspect bricks/transform/calculate_total.py
```

Expected output:
```
Inspecting: bricks/transform/calculate_total.py
==================================================

Score: 95/100
Rating: EXCELLENT

✓ No issues found
==================================================
✓ Brick passes inspection
```

### Step 7: Run Tests

```bash
python brick_cli.py test bricks/transform/calculate_total.py
```

Expected output:
```
Running tests: bricks/transform/test_calculate_total.py
--------------------------------------------------
✓ test_calculate_total
✓ test_calculate_total_invalid

Results: 2 passed, 0 failed
```

## Exploring Example Bricks

The repository includes working examples in four categories:

### Authentication (`examples/auth/`)
- `auth_validate_token.py` - Validate JWT tokens
- `auth_generate_token.py` - Generate JWT tokens
- `auth_hash_password.py` - Hash passwords with bcrypt
- `auth_verify_password.py` - Verify password hashes
- `auth_check_permission.py` - Check user permissions

### Data Access (`examples/data/`)
- `query_select.py` - Safe SQL SELECT queries
- `query_insert.py` - Safe SQL INSERT queries
- `validate_input.py` - Input validation
- `sanitize_sql.py` - SQL string sanitization
- `cache_get.py` - Cache retrieval

### API Integration (`examples/api/`)
- `http_get.py` - HTTP GET requests
- `http_post.py` - HTTP POST requests
- `parse_response.py` - Parse API responses
- `handle_error.py` - Handle API errors
- `rate_limit.py` - Rate limiting

### Data Transformation (`examples/transform/`)
- `json_validate.py` - JSON validation
- `json_parse.py` - JSON parsing with defaults
- `csv_parse.py` - CSV parsing
- `data_sanitize.py` - Data sanitization
- `format_response.py` - Format API responses

Try inspecting any example:
```bash
python brick_cli.py inspect examples/auth/auth_validate_token.py
python brick_cli.py test examples/auth/auth_validate_token.py
```

## Understanding the Inspection System

The inspector checks four areas:

### 1. Security (`tools/inspect_security.py`)
Scans for:
- `eval()` or `exec()` on untrusted input (-30 points)
- `shell=True` with user input (-30 points)
- Hardcoded passwords/API keys (-20 points)
- SQL injection risks (-20 points)
- Dangerous imports like `pickle` (-5 points)

### 2. Contract (`tools/inspect_contract.py`)
Validates:
- Metadata file exists (-20 if missing)
- Required metadata fields present (-5 each)
- Code matches interface specification (-10 points)

### 3. Quality (`tools/inspect_quality.py`)
Checks:
- Size limit (50 lines) (-10 if exceeded)
- Module docstring present (-5 if missing)
- Function docstrings (-3 each missing)

### 4. Dependencies (`tools/inspect_dependencies.py`)
Reviews:
- Risky imports (-5 each)
- Deprecated libraries (warnings)
- Undeclared dependencies

**Scoring:**
- 90-100: EXCELLENT - Auto-approve
- 70-89: GOOD - Human review recommended
- 50-69: NEEDS WORK - Issues found
- 0-49: POOR - Serious problems

## Brick Composition Patterns

Bricks are designed to be composed together. Here are common patterns:

### Pattern 1: Sequential Pipeline
```python
# Request → Validate → Process → Format → Response
from auth import auth_validate_token
from data import query_select
from transform import format_response

def handle_request(token, user_id):
    # Step 1: Validate
    auth_result = auth_validate_token(token)
    if auth_result["error"]:
        return format_response({"error": "Unauthorized"}, status=401)

    # Step 2: Query
    data_result = query_select("users", {"id": user_id})
    if data_result["error"]:
        return format_response({"error": "Not found"}, status=404)

    # Step 3: Format
    return format_response(data_result["data"], status=200)
```

### Pattern 2: Parallel Execution
```python
# Fetch multiple data sources in parallel
from concurrent.futures import ThreadPoolExecutor
from api import http_get

def fetch_dashboard_data(user_id):
    with ThreadPoolExecutor() as executor:
        profile = executor.submit(http_get, f"/api/profile/{user_id}")
        orders = executor.submit(http_get, f"/api/orders/{user_id}")
        stats = executor.submit(http_get, f"/api/stats/{user_id}")

    return {
        "profile": profile.result(),
        "orders": orders.result(),
        "stats": stats.result()
    }
```

### Pattern 3: Error Handling Wrapper
```python
# Wrap bricks with consistent error handling
def safe_brick_call(brick_func, *args, **kwargs):
    try:
        result = brick_func(*args, **kwargs)
        if result.get("error"):
            log_error(result["error"])
        return result
    except Exception as e:
        return {"error": f"Brick failure: {str(e)}"}
```

## Best Practices

### 1. Keep Bricks Focused
**Good:**
```python
def validate_email(email):
    """Validate email format."""
    # Does one thing well
```

**Bad:**
```python
def validate_and_send_email(email, message):
    """Validate email and send message."""
    # Does too much - split into two bricks
```

### 2. Explicit Error Handling
**Good:**
```python
def divide(a, b):
    if b == 0:
        return {"result": None, "error": "division_by_zero"}
    return {"result": a / b, "error": None}
```

**Bad:**
```python
def divide(a, b):
    return a / b  # Raises exception - unclear error handling
```

### 3. Include Tests in the Same File
**Good:**
```python
def my_function(x):
    return x * 2


def test_my_function():
    assert my_function(5) == 10
```

**Bad:**
```python
# my_function.py
def my_function(x):
    return x * 2

# test_my_function.py (separate file - less discoverable)
def test_my_function():
    assert my_function(5) == 10
```

### 4. Use Metadata for Documentation
Always include complete metadata with:
- Interface specification (inputs/outputs)
- Dependencies list
- Test function names
- Version information in brick_id

## Troubleshooting

### "Missing metadata file"
Create a `.meta.json` file with the same name as your brick:
```bash
# For my_brick.py, create my_brick.meta.json
```

### "Exceeds 50 lines"
Your brick is too large. Split it into multiple bricks:
- Extract helper functions as separate bricks
- Move complex logic to new bricks
- Compose bricks together

### "Missing docstring"
Add a module-level docstring:
```python
"""Brief description of what this brick does."""
```

### Tests Not Found
Include tests in the same file as the brick, or create a test file with the same name prefixed with `test_`:
```
my_brick.py → test_my_brick.py
```

## Next Steps

1. **Browse Examples**: Study the example bricks to learn patterns
2. **Build Your First Brick**: Start with a simple data transformation
3. **Compose Bricks**: Combine multiple bricks into a larger feature
4. **Contribute**: Share your bricks with the community

## Resources

- [README.md](README.md) - Full Brick Architecture specification
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [CLI_GUIDE.md](CLI_GUIDE.md) - Complete CLI reference
- [GitHub](https://github.com/drew913s/Brick) - Repository

## Getting Help

- **Issues**: https://github.com/drew913s/Brick/issues
- **Discussions**: https://github.com/drew913s/Brick/discussions
- **Examples**: See `examples/` directory

Welcome to the future of AI-generated code! 🧱
