# Ant Colony Orchestration

**Multi-agent coordination for parallel AI development**

---

## The Problem

You're running 20+ parallel Claude Code sessions building software. Each session:
- Has limited context window
- Doesn't know what other sessions are doing
- Claims "done" when code compiles but there's no UI to test
- Goes off track and needs killing

You need coordination without expensive API access.

---

## The Solution: Ant Colony Model

**Core Insight:** Stop trying to make one smart AI. Make many dumb, disposable workers with all knowledge stored externally.

```
HUMAN (you - router, tester, decision-maker)
  │
  └── QUEEN (Q) - Top architect, NO CODE
        │
        ├── PRINCESS (Q-FE) - Domain architect
        │     ├── ANT (Q-FE-1) - ONE task, writes code, dies
        │     ├── ANT (Q-FE-2) - ONE task, writes code, dies
        │     └── ...
        │
        ├── PRINCESS (Q-BE) - Domain architect  
        │     └── ...
        │
        └── PRINCESS (Q-DB) - Domain architect
              └── ...
```

**Key principles:**
- Sessions are disposable (kill and respawn freely)
- GitHub is the permanent brain (all context in issues)
- HUMAN routes work (spawns/closes terminals)
- Each worker does ONE thing then dies

---

## New Documentation

| File | Purpose |
|------|---------|
| **SESSION_SPEC.md** | How AI sessions behave |
| **HUMAN_SPEC.md** | Human operator's manual |
| **BOOTSTRAP_PROMPTS.md** | Ready-to-paste prompts |
| **BRICK_SPEC.md** | Core brick requirements (+ ant colony section) |

---

## Quick Start

### 1. Start a Project

```bash
# Open terminal for Queen
# Paste Queen bootstrap from BOOTSTRAP_PROMPTS.md
# Replace [PROJECT REQUIREMENTS] with your brief
```

### 2. Queen Creates Architecture

Queen outputs:
- Domain specs as GitHub issues
- List of Princess terminals to spawn

### 3. Spawn Princesses

```bash
# Open terminals Q-FE, Q-BE, Q-DB
# Paste Princess bootstrap for each
# Point to parent issue from Queen
```

### 4. Princesses Create Tasks

Each Princess outputs:
- Worker tasks as GitHub issues (≤50 lines each)
- List of Ant terminals to spawn

### 5. Spawn Workers in Waves

```bash
# Open 5-10 Ant terminals
# Paste Ant bootstrap for each
# Point to task issue from Princess
# Track in spreadsheet/cards
```

### 6. Monitor and Test

Every 30 minutes:
- Check tracker for stale sessions
- Check GitHub for `test-ready` items
- Test features yourself
- Close completed terminals
- Spawn next wave

---

## The Rules

### Session Hierarchy

| Role | Code | Focus |
|------|------|-------|
| Queen | NONE | System architecture |
| Princess | Minimal (≤20 lines) | Domain design |
| Ant | YES (≤50 lines) | Implementation |

### Abandon Triggers

Kill session immediately if:
- Argues about task validity
- 500+ words without code
- Claims "done" but no access method
- Same error 3+ times
- Working on wrong task
- 30+ min silence

### Completion Requirements

Not done until:
- HUMAN can access it (URL/command/button)
- HUMAN tested it
- GitHub issue updated
- Label set to `done`

---

## File Structure

```
Brick/
├── BRICK_SPEC.md         # Core brick rules
├── SESSION_SPEC.md       # AI session behavior (NEW)
├── HUMAN_SPEC.md         # Human operator manual (NEW)
├── BOOTSTRAP_PROMPTS.md  # Ready-to-paste prompts (NEW)
├── .github/
│   └── ISSUE_TEMPLATE/
│       ├── queen-domain-spec.md
│       └── princess-worker-task.md
├── templates/
│   ├── terminal_tracker.csv
│   └── quick_reference.html
└── ... (existing files)
```

---

## Labels

```
Roles:      queen | princess | worker
Status:     backlog | in-progress | blocked | code-complete | test-ready | done
```

---

## Philosophy

This is NOT about making AI smarter. It's about:

1. **Disposability** - Sessions are cheap, context is expensive
2. **Externalization** - All knowledge in GitHub, not chat
3. **Human routing** - You spawn and kill, AI executes
4. **Small tasks** - ≤50 lines per brick, one responsibility
5. **Testability** - If HUMAN can't test it, it's not done

---

## Related Docs

- [SESSION_SPEC.md](SESSION_SPEC.md) - Full session behavior spec
- [HUMAN_SPEC.md](HUMAN_SPEC.md) - Complete human operator guide
- [BOOTSTRAP_PROMPTS.md](BOOTSTRAP_PROMPTS.md) - All prompt templates
- [BRICK_SPEC.md](BRICK_SPEC.md) - Core architecture rules

---
