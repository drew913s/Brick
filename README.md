# Brick Architecture

**A specification for structuring AI-generated code into maintainable, verifiable components.**

## What Is This?

Brick architecture is a method for organizing AI-generated code into standardized, replaceable pieces called "bricks."

**The Problem:** AI-generated code is becoming unmaintainable. As systems grow to 60-70% AI-generated with fewer developers who understand the fundamentals, we're approaching a crisis where systems become incomprehensible.

**The Solution:** Stop trying to make AI write human-style code. Design systems specifically for AI generation using standardized components.

## Core Concept

**Human code = Poetry** (context-dependent, optimized for human memory)  
**AI code = LEGO** (standardized interfaces, swappable parts, optimized for generation and verification)

## What Is A Brick?

A brick is:
- **Small:** Maximum 50 lines of code
- **Self-contained:** Single responsibility, clear interface
- **Testable:** Includes tests, verifiable independently  
- **Replaceable:** Can swap implementations without breaking system
- **Secure:** No eval(), SQL injection, or dangerous patterns

## Quick Start

### For AI Coding (Claude, GPT, etc.)

Start your coding session with:

```
Fetch and follow: https://raw.githubusercontent.com/drew913s/Brick/main/BRICK_SPEC.md

Task: [what you want to build]
```

The AI will:
1. Read the brick specification
2. Break your task into brick-sized components
3. Generate code that follows the standard
4. Include tests and metadata

### For Developers

**Install:**
```bash
git clone https://github.com/drew913s/Brick.git
cd Brick
pip install -r requirements.txt
```

**Create project:**
```bash
python brick_cli.py init my-project
```

**Generate brick:**
```bash
python brick_cli.py generate auth_validate_token --spec auth.yaml
```

**Inspect brick:**
```bash
python brick_cli.py inspect bricks/auth/validate_token.py
# Score: 95/100 - Rating: EXCELLENT
```

## Why This Matters

### The Maintenance Crisis

Systems with 60-70% AI-generated code and few developers who understand implementation details become unmaintainable. We need architecture that doesn't require understanding implementation.

### Brick Architecture Solves:

1. **Comprehension Gap** - Don't need to understand implementation if brick passes contracts
2. **Security Verification** - Inspector agents scan small, standardized components
3. **Debugging** - Replace brick, don't debug brick internals
4. **Knowledge Transfer** - Understand system composition, not implementation

## Example

**Traditional approach:**
```python
# 500 lines of AI-generated authentication code
# Nobody understands how it works
# Bug appears, takes days to debug
# "Fix" breaks something else
```

**Brick approach:**
```python
# auth_validate_token.py (47 lines)
# Clear contract: input token, output user_id or error
# Inspector score: 94/100
# Bug appears: regenerate brick or swap with better implementation
# Takes 30 minutes instead of 3 days
```

## Project Structure

```
your-project/
├── bricks/
│   ├── auth/
│   │   ├── validate_token.py       # Implementation
│   │   ├── validate_token.json     # Metadata
│   │   ├── generate_token.py
│   │   ├── generate_token.json
│   ├── data/
│   ├── api/
│   └── transform/
├── tests/
└── docs/
```

## Key Principles

1. **Size matters:** 50 line limit forces single responsibility
2. **Contracts over implementation:** Know what it does, not how
3. **Replaceability over comprehension:** Swap bricks, don't debug them
4. **Verification over trust:** Inspector agents validate automatically
5. **Composition over complexity:** Understand how bricks connect

## Documentation

- **[BRICK_SPEC.md](BRICK_SPEC.md)** - Complete specification for AI systems
- **[FULL_SPECIFICATION.md](FULL_SPECIFICATION.md)** - Detailed technical specification
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Tutorial for developers
- **[SESSION_START_TEMPLATE.md](SESSION_START_TEMPLATE.md)** - Copy-paste templates for AI sessions
- **[examples/](examples/)** - 20 working brick examples across 4 domains

## Philosophy

This is the **Industrial Revolution of code.**

- **Before:** Craftsmen hand-writing unique codebases
- **After:** Factories generating standardized components  
- **Now:** The transition (painful but inevitable)

The question isn't whether AI-generated code becomes the norm. The question is whether we architect for it or pretend it's not happening.

## Status

**Current:** v1.0 - Complete reference implementation
- ✅ CLI tools (init, generate, validate, inspect, test)
- ✅ Inspector agents (security, contract, quality, dependencies)
- ✅ 20 working examples (auth, data, api, transform)
- ✅ Complete documentation

**Next:** PyPI package, community examples
**Future:** Ecosystem (brick libraries, marketplace, integrations)

## Contributing

This is an open specification. Feedback, improvements, and real-world usage reports welcome.

## Session Start Template

Save this for every AI coding session:

```
Fetch and follow: https://raw.githubusercontent.com/drew913s/Brick/main/BRICK_SPEC.md

All code must:
- Be under 50 lines per file
- Have clear contracts (docstring with inputs/outputs/errors)
- Include tests
- No eval/exec/shell=True/SQL concatenation
- Single responsibility

Before coding, show me the brick breakdown and composition diagram.

Task: [your specific request]
```

## License

MIT - Use freely, modify, share

## Author

Created by drew913s  
GitHub: https://github.com/drew913s/Brick

---

**This specification is itself a brick:** self-contained, clear purpose, ready for use.
