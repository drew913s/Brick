---
name: Princess Worker Task
about: Worker-sized task specification created by Princess session
title: '[WORKER] '
labels: worker, backlog
assignees: ''
---

## Worker Task

**Task ID:** Q-{DOMAIN}-{N}
**Parent Domain:** Q-{DOMAIN}
**Parent Issue:** #{PARENT_ISSUE_NUMBER}

---

## Single Responsibility

**What this worker builds:**
(One sentence, one thing)



---

## Brick Specification

**Brick Name:** `{domain}_{function_name}`

### Interface

```yaml
inputs:
  param_name: type
  param_name: type

outputs:
  result: type
  error: string|null

errors:
  - error_type_1
  - error_type_2
```

### Constraints
- 
- 
- 

### Dependencies
- 

---

## Acceptance Criteria

- [ ] Brick ≤50 lines
- [ ] Docstring with inputs/outputs/errors
- [ ] Tests included
- [ ] No banned patterns (eval, exec, shell=True, etc.)
- [ ] Metadata file created

---

## Access Method

**HUMAN tests this by:**

| Method | Location |
|--------|----------|
| URL | |
| Command | |
| Button | |
| API Call | |

**Success looks like:**


**Failure looks like:**


---

## File Ownership

**This task CREATES:**
- [ ] `bricks/{domain}/{brick_name}.py` (NEW)
- [ ] `bricks/{domain}/{brick_name}.meta.json` (NEW)
- [ ] (optional) `bricks/{domain}/test_{brick_name}.py` (NEW)

**This task MODIFIES:**
- (none - or list files)

**OFF LIMITS (other workers own these):**
- (list files owned by concurrent workers)

---

## Integration Notes

**This brick is used by:**
- 

**This brick uses:**
- 

---

## Worker Assignment

**Spawn Ant:** `Q-{DOMAIN}-{N}`
**Bootstrap:** See SESSION_SPEC.md Ant template

---

## Progress Log

_Worker updates here every 30 minutes_

<!-- 
## Progress Update - YYYY-MM-DDTHH:MM
**Status:** Working | Blocked | Complete
**Done:** 
**Current:**
**Blockers:**
**Files:**
-->
