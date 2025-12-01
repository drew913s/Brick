# Ant Colony Commands

Available slash commands (global):

## Role Assignment
| Command | Use When |
|---------|----------|
| `/user:queen` | Starting new project - system architecture |
| `/user:queen-audit` | Analyzing existing codebase for migration |
| `/user:princess` | Designing domain - breaking into brick tasks |
| `/user:ant` | Building a single brick (new code) |
| `/user:wrapper` | Building a wrapper brick (legacy code) |

## During Work
| Command | Use When |
|---------|----------|
| `/user:status` | HUMAN asks for progress update |
| `/user:help` | Show this list |

## Quick Reference

**Queen (Q):** Architecture only, no code
**Princess (Q-XX):** Domain design, ≤20 lines code  
**Ant (Q-XX-N):** Single brick, ≤50 lines code

## Workflow

1. HUMAN spawns you with a role command
2. You do your job (design or build)
3. HUMAN runs `/user:status` to check progress
4. You complete and stop
5. HUMAN tests and closes

## Rules Reminder

- Stay in your lane (file ownership)
- Commit every 15-20 min
- Update GitHub issue every 30 min
- ≤50 lines per file
- If stuck 10+ min: Ask, don't loop
