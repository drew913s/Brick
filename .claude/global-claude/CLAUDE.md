# Ant Colony System

You may be part of a multi-agent orchestration system. A HUMAN operator manages multiple Claude sessions simultaneously.

## Roles

| ID | Role | Code |
|----|------|------|
| Q | Queen - architect | NO |
| Q-XX | Princess - domain designer | ≤20 lines |
| Q-XX-N | Ant - brick builder | ≤50 lines |

If HUMAN assigns you a role or mentions "ant colony" or "brick", these rules apply:

## Core Rules

1. **≤50 lines per file** - Always
2. **One task per session** - No scope creep
3. **Commit every 15-20 min** - Small commits
4. **Stay in your lane** - Only files in your ownership list

## Brick Format

```
bricks/{domain}/{name}.py        # ≤50 lines
bricks/{domain}/{name}.meta.json # Metadata
bricks/{domain}/test_{name}.py   # Tests
```

## Return Format

All bricks return: `{'result': X, 'error': str|None}`

## Commands

Type `/user:help` to see available role commands:
- `/user:queen` - Architecture mode
- `/user:queen-audit` - Existing code audit
- `/user:princess` - Domain design
- `/user:ant` - Build a brick
- `/user:wrapper` - Wrap legacy code
- `/user:status` - Progress report

These work from any directory.

## Not in Ant Colony Mode?

If HUMAN doesn't mention roles, sessions, or bricks - just work normally. This context only activates when relevant.
