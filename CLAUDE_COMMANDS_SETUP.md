# Ant Colony - Claude Code Setup

## One-Time Install

Copy the `.claude` folder to your home directory:

```bash
cp -r global-claude ~/.claude
```

That's it. Now these commands work from any terminal:

| Command | Role |
|---------|------|
| `/user:queen` | System architect (no code) |
| `/user:queen-audit` | Audit existing codebase |
| `/user:princess` | Domain designer |
| `/user:ant` | Brick builder |
| `/user:wrapper` | Legacy code wrapper |
| `/user:status` | Progress check |
| `/user:help` | List all commands |

## Usage

1. Open any terminal
2. Run `claude`
3. Type `/user:ant` (or whichever role)
4. Give it the task

## What's in the folder

```
~/.claude/
├── CLAUDE.md              # Auto-loads minimal context
└── commands/
    ├── ant.md             # /user:ant
    ├── help.md            # /user:help
    ├── princess.md        # /user:princess
    ├── queen.md           # /user:queen
    ├── queen-audit.md     # /user:queen-audit
    ├── status.md          # /user:status
    └── wrapper.md         # /user:wrapper
```

## Printable Materials

- `PRINT_ALL.html` - All 3 pages in one file
- `CHEAT_SHEET.html` - Quick reference (page 1)
- `FLOWCHART_PAGE1.html` - Visual flow (page 2)
- `FLOWCHART_PAGE2.html` - Commands by step (page 3)

Print `PRINT_ALL.html` for the complete operator manual.
