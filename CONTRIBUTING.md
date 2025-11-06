# Contributing to Brick Architecture

Thank you for your interest in contributing to the Brick Architecture project! This project aims to create a new paradigm for AI-generated code that is maintainable, secure, and verifiable.

## Ways to Contribute

We welcome contributions in many forms:

### 1. Documentation Improvements
- Clarify existing specifications
- Add examples and use cases
- Fix typos or formatting issues
- Translate documentation to other languages

### 2. Example Brick Implementations
- Create reference implementations in various programming languages
- Build example applications using brick architecture
- Develop templates and boilerplate code

### 3. Bug Reports and Feature Requests
- Report issues with the specification
- Suggest improvements to the architecture
- Propose new brick patterns or composition strategies

### 4. Inspector Agent Development
- Build tools to validate brick compliance
- Create security scanners for banned patterns
- Develop automated testing frameworks

### 5. Tooling and Automation
- IDE plugins for brick development
- CLI tools for brick generation and management
- CI/CD integrations for brick validation

## Getting Started

### For Documentation and Specification Changes

1. **Fork the repository** to your GitHub account
2. **Clone your fork** locally:
   ```bash
   git clone git@github.com:YOUR-USERNAME/Brick.git
   cd Brick
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and commit with clear messages
5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request** against the main repository

### For Code Examples and Tools

1. Follow the same fork/clone/branch workflow
2. Create your code in the appropriate directory:
   - `examples/` for example brick implementations
   - `tools/` for inspector agents, generators, etc.
   - `templates/` for boilerplate and scaffolding
3. Ensure your code includes tests and documentation
4. Submit a pull request

## Contribution Guidelines

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

### Submitting Issues

When reporting bugs or requesting features:

- **Search existing issues** first to avoid duplicates
- **Use clear, descriptive titles**
- **Provide context**: What were you trying to do?
- **Include examples**: Show expected vs actual behavior
- **Be specific**: Version info, environment details, reproduction steps

**For specification issues:**
- Quote the relevant section
- Explain the problem or ambiguity
- Suggest a potential solution

**For feature requests:**
- Describe the use case
- Explain why it's valuable
- Consider backward compatibility

### Submitting Pull Requests

Before submitting:

- [ ] Ensure your changes follow the project's style
- [ ] Update documentation if needed
- [ ] Add tests for new functionality
- [ ] Verify all tests pass
- [ ] Write clear commit messages
- [ ] Reference related issues

**Pull Request Description Should Include:**
- Summary of changes
- Motivation and context
- Testing performed
- Screenshots (if applicable)
- Breaking changes (if any)

**Review Process:**
- Maintainers will review PRs within 1-2 weeks
- Address review feedback promptly
- Be patient and professional during reviews
- PRs may require multiple rounds of review

## Brick Submission Guidelines

If you're submitting example bricks or brick implementations:

### Requirements

1. **Follow the Specification**
   - Maximum 50 lines of code OR 2000 tokens
   - Explicit input/output contracts
   - Clear error handling
   - No banned patterns

2. **Include Complete Metadata**
   ```json
   {
     "brick_id": "your_brick_name_v1",
     "generated": "ISO 8601 timestamp",
     "model": "AI model used",
     "interface": { /* inputs/outputs */ },
     "dependencies": [],
     "tests": []
   }
   ```

3. **Provide Tests**
   - Test happy path
   - Test error conditions
   - Test edge cases
   - Minimum 80% coverage

4. **Security Review**
   - No `eval()` or `exec()` on untrusted input
   - No `shell=True` with user input
   - No hardcoded secrets
   - No SQL injection vulnerabilities
   - Run security linters

5. **Documentation**
   - Clear docstring explaining purpose
   - Document all parameters and return values
   - Include usage examples

### Brick Example Structure

```
examples/
  python/
    auth_validate_token/
      brick.py          # Implementation
      brick.test.py     # Tests
      brick.meta.json   # Metadata
      README.md         # Usage documentation
```

## Style Guide

### Documentation Style

- Use clear, concise language
- Write for both AI and human readers
- Include code examples where helpful
- Use proper markdown formatting
- Keep lines under 100 characters for readability

### Code Style

Follow language-specific conventions:

**Python:**
- PEP 8 style guide
- Type hints for function signatures
- Docstrings in Google or NumPy format

**JavaScript/TypeScript:**
- ESLint with standard config
- JSDoc comments for functions
- Prefer TypeScript for new code

**Go:**
- `gofmt` for formatting
- Godoc comments for exported functions

**Rust:**
- `rustfmt` for formatting
- Clippy for linting

### Commit Message Style

```
<type>: <short summary>

<longer description if needed>

Fixes #<issue-number>
```

**Types:**
- `docs:` Documentation changes
- `feat:` New features
- `fix:` Bug fixes
- `refactor:` Code refactoring
- `test:` Test additions or changes
- `chore:` Maintenance tasks

**Examples:**
```
docs: clarify brick size constraints

Added examples showing what counts toward the 50-line limit
and how to measure token count.

Fixes #42
```

```
feat: add Python brick generator CLI tool

Implements command-line tool for generating brick boilerplate
from specifications. Includes tests and documentation.
```

## Community & Communication

### Questions and Discussions

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions, ideas, and general discussion
- **Pull Requests**: For code review and technical discussions

### Getting Help

If you're stuck or need clarification:

1. Check the [README.md](README.md) specification
2. Search existing issues and discussions
3. Open a new discussion with your question
4. Be specific about what you're trying to accomplish

### Staying Updated

- **Watch the repository** for notifications
- **Star the repository** to bookmark it
- **Follow releases** for major updates

## Recognition

Contributors will be recognized in the following ways:

- Listed in CONTRIBUTORS.md (if you submit a substantial PR)
- Mentioned in release notes for significant contributions
- Co-author attribution in commits (when applicable)

## License

By contributing to Brick Architecture, you agree that your contributions will be licensed under the MIT License. This means your contributions can be freely used, modified, and distributed by others.

When you submit a pull request, you certify that:
- You have the right to submit the contribution
- Your contribution is your original work (or properly attributed)
- You agree to the MIT License for your contribution

## Questions?

If you have questions about contributing that aren't answered here:

1. Check the [README.md](README.md) for project overview
2. Open a GitHub Discussion
3. Reference this document in your question

Thank you for helping build the future of AI-generated code architecture!

---

**Last Updated:** 2025-11-06
**Version:** 1.0
