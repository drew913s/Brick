# Session Start Template

Copy-paste this at the start of every AI coding session (Claude Code, ChatGPT, etc.):

---

```
Fetch and follow: https://raw.githubusercontent.com/drew913s/Brick/main/BRICK_SPEC.md

All code you generate must follow brick architecture:
- Maximum 50 lines per file
- Clear docstring with inputs/outputs/errors
- No eval/exec/shell=True/SQL concatenation
- Include tests
- Single responsibility

Before writing any code:
1. Break my request into brick-sized components
2. Show me the brick breakdown
3. Show me how bricks compose together
4. Ask for approval

Then generate bricks one at a time with tests and metadata.

Verify each brick before delivering:
✓ Under 50 lines?
✓ Docstring present?
✓ Error handling?
✓ Tests included?
✓ No banned patterns?

Confirm you understand and have read the specification.

My task: [PASTE YOUR TASK HERE]
```

---

## Examples

### Example 1: Web API
```
Fetch and follow: https://raw.githubusercontent.com/drew913s/Brick/main/BRICK_SPEC.md

Follow brick architecture for this session.

My task: Build a REST API for user authentication with JWT tokens, including login, logout, and token refresh endpoints.
```

### Example 2: Data Processing
```
Fetch and follow: https://raw.githubusercontent.com/drew913s/Brick/main/BRICK_SPEC.md

Follow brick architecture for this session.

My task: Build a CSV processor that validates input, transforms data, and exports to JSON with error reporting.
```

### Example 3: Refactoring
```
Fetch and follow: https://raw.githubusercontent.com/drew913s/Brick/main/BRICK_SPEC.md

Follow brick architecture for this session.

My task: Refactor this existing code into bricks. [paste existing code]
```

---

## Tips

1. **Be specific in your task** - The clearer you are, the better the brick breakdown
2. **Review the breakdown** - Make sure bricks are properly separated before generation
3. **Save the template** - Bookmark it or save as text snippet for quick access
4. **One session, one standard** - Paste this at the start of EVERY coding session

---

## What The AI Will Do

After reading the specification, the AI will:

1. ✓ Acknowledge it understands brick architecture
2. ✓ Break your task into brick-sized components (under 50 lines each)
3. ✓ Show you a composition diagram (how bricks connect)
4. ✓ Ask for your approval
5. ✓ Generate bricks one at a time
6. ✓ Include tests and metadata for each brick
7. ✓ Verify compliance before delivering

---

## Troubleshooting

**Q: AI generates large files anyway**  
A: Stop it and remind: "This violates brick spec. Break into files under 50 lines each."

**Q: AI doesn't fetch the spec**  
A: Make sure you included the fetch command. Try again with explicit instruction.

**Q: How do I verify bricks are compliant?**  
A: Count lines, check for docstrings, check for tests. Inspector tools coming soon.

**Q: What if I need to generate quick prototype?**  
A: Still use bricks, just generate fewer of them. Even prototypes benefit from structure.

---

Last updated: 2025-11-06
