# Conflict Resolution & Recovery Guide

**Handling concurrent edits, rate limits, and real-world recovery**  
**Repository:** https://github.com/drew913s/Brick  
**Last Updated:** 2025-12-01

---

## Concurrent Edit Prevention

### The Problem

Two Ants (Q-FE-1 and Q-FE-2) both modify files in `bricks/auth/`. Git conflicts ensue. Princess integration becomes a merge nightmare.

### Prevention Strategy: File Claiming

**Rule:** Each worker task issue must declare files it will create/modify.

**In the Princess Worker Task template, add:**

```markdown
## File Ownership
**This task CREATES:**
- bricks/auth/validate_token.py (NEW)
- bricks/auth/validate_token.meta.json (NEW)

**This task MODIFIES:**
- (none)

**OFF LIMITS (other workers own these):**
- bricks/auth/generate_token.py (Q-FE-2)
- bricks/auth/hash_password.py (Q-FE-3)
```

**Princess responsibility:** When breaking down tasks, ensure no file overlap between concurrent workers.

### Detection: Before Spawning

HUMAN checks before spawning Ant:
```
☐ Does this task's file list overlap with any in-progress worker?
☐ If yes → wait for that worker to finish, OR re-scope tasks
```

### When Conflicts Happen Anyway

**Scenario:** Q-FE-1 and Q-FE-2 both edited `utils/helpers.py`

**Resolution steps:**

1. **Stop both workers** (close terminals, don't let them push more)

2. **Check Git status:**
   ```bash
   git status
   git diff HEAD~2  # see what changed
   ```

3. **Determine winner:**
   | Situation | Winner |
   |-----------|--------|
   | One worker's changes are clearly better | Keep that one |
   | Both have valid changes | Manual merge |
   | Changes are to different functions | Both can stay |
   | Changes conflict in same function | Pick one, file issue for other |

4. **Manual merge if needed:**
   ```bash
   git checkout --ours bricks/auth/utils.py   # keep first worker
   # OR
   git checkout --theirs bricks/auth/utils.py  # keep second worker
   # OR
   # manually edit the file
   ```

5. **Update issues:**
   - Losing worker's issue: "Changes superseded by #X, needs rework"
   - Create new issue if functionality was lost

6. **Respawn if needed** for the losing worker's task

### Branch Strategy (Optional)

For larger projects, use feature branches:

```
main
  └── feature/auth
        ├── Q-FE-1-validate-token  (Ant branch)
        ├── Q-FE-2-generate-token  (Ant branch)
        └── Q-FE-3-hash-password   (Ant branch)
```

**Princess integrates:** Merges all Ant branches into `feature/auth`
**Queen reviews:** Merges `feature/auth` into `main`

**Simpler approach for small projects:** Everyone commits to main, Princess resolves conflicts during integration.

---

## GitHub Rate Limits

### The Math

| Action | Requests | Frequency | Hourly Total |
|--------|----------|-----------|--------------|
| Worker progress update | 1 | Every 30 min | 2/worker |
| Read issue | 1 | On spawn | 1/worker |
| Update labels | 1 | 2-3x per task | ~3/worker |
| Create comment | 1 | Every 30 min | 2/worker |

**Per worker lifecycle:** ~8-10 API requests
**20 workers cycling every 2 hours:** ~100 requests/hour

**GitHub limit:** 5,000 authenticated requests/hour

**Verdict:** You're fine for normal usage.

### When You Might Hit Limits

- Running 50+ concurrent workers
- Automated tooling polling GitHub constantly
- Many workers spawning/dying rapidly
- External integrations (CI/CD) competing for quota

### Mitigation Strategies

**1. Batch operations:**
Instead of updating issue + adding comment + changing label separately:
```bash
# One API call with GitHub CLI
gh issue edit 47 --add-label "code-complete" --remove-label "in-progress"
gh issue comment 47 --body "Progress update..."
```

**2. Reduce update frequency:**
- Workers update every 60 min instead of 30 (for stable tasks)
- Only comment on significant progress, not "still working"

**3. Local caching:**
Workers read issue once at spawn, don't re-fetch unless blocked.

**4. Check your usage:**
```bash
# See current rate limit status
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/rate_limit
```

**5. If actually rate limited:**
- Pause spawning new workers
- Let current workers finish
- Resume after limit resets (top of next hour)

---

## Recovery Scenarios

### Scenario 1: Worker Goes Silent (30+ min, no update)

**Symptoms:**
- Terminal open but no activity
- No new comments on GitHub issue
- No file changes in repo

**Diagnosis steps:**

1. **Check terminal:** Is there an error? Is it waiting on input? Crashed?
   
2. **Check GitHub issue:** Did it post any updates before going silent?

3. **Check git log:**
   ```bash
   git log --oneline -5  # any recent commits from this worker?
   ```

**Recovery:**

| Diagnosis | Action |
|-----------|--------|
| Terminal shows error/crash | Close, respawn fresh |
| Waiting for input (shouldn't happen) | Provide input, note for future |
| Claude API slow/timeout | Wait 5 min, if no recovery → respawn |
| Actually working, just no update | Prompt: "Post a progress update" |
| No signs of life | Close, check GitHub, respawn |

**After closing:**
```bash
# Check what was done
git status
git diff HEAD

# If partial work exists, commit it
git add .
git commit -m "WIP: Q-FE-1 partial progress before respawn"

# Update issue
gh issue comment 47 --body "Worker went silent. Partial progress committed. Respawning."
```

---

### Scenario 2: Worker Finished But Nothing Works

**Symptoms:**
- Worker said "done"
- Issue marked `code-complete`
- But: tests fail, imports error, feature doesn't appear

**Diagnosis steps:**

1. **Run the tests:**
   ```bash
   python -m pytest bricks/auth/test_validate_token.py -v
   ```

2. **Check imports:**
   ```bash
   python -c "from bricks.auth.validate_token import auth_validate_token"
   ```

3. **Check the code exists:**
   ```bash
   ls -la bricks/auth/
   cat bricks/auth/validate_token.py
   ```

**Recovery:**

| Diagnosis | Action |
|-----------|--------|
| Tests fail with assertion errors | Code is wrong → new issue for fix |
| Import errors | Missing dependency or typo → quick fix or respawn |
| File doesn't exist | Worker didn't commit → check terminal for unsaved work |
| Wrong file location | Worker misunderstood → new issue with correct path |
| Code exists but not integrated | Missing from `__init__.py` → integration issue |

**If worker didn't commit:**
```bash
# Check if files exist uncommitted
find . -name "*.py" -newer .git/HEAD -mmin -60

# If found, commit them
git add bricks/auth/
git commit -m "Recovered uncommitted work from Q-FE-1"
```

---

### Scenario 3: Two Workers Edited Same File

**Symptoms:**
- `git push` fails with conflict
- OR merge conflict markers in file
- OR one worker's changes disappeared

**Recovery steps:**

1. **Identify the conflict:**
   ```bash
   git status
   git diff --name-only HEAD~2 HEAD
   ```

2. **See both versions:**
   ```bash
   git show HEAD~1:bricks/auth/utils.py > version_a.py
   git show HEAD:bricks/auth/utils.py > version_b.py
   diff version_a.py version_b.py
   ```

3. **Decide resolution:**

   **Option A - One version wins:**
   ```bash
   git checkout HEAD~1 -- bricks/auth/utils.py  # keep older
   # OR
   git checkout HEAD -- bricks/auth/utils.py    # keep newer
   ```

   **Option B - Manual merge:**
   ```bash
   # Edit the file to combine both changes
   vim bricks/auth/utils.py
   git add bricks/auth/utils.py
   git commit -m "Merged Q-FE-1 and Q-FE-2 changes to utils.py"
   ```

4. **Update affected issues:**
   ```bash
   gh issue comment 47 --body "Merged with #48 changes. Resolved conflict in utils.py"
   gh issue comment 48 --body "Merged with #47 changes. Resolved conflict in utils.py"
   ```

5. **Prevent future conflicts:**
   - Review Princess task breakdown
   - Add file ownership to remaining tasks
   - Consider: should these have been one task?

---

### Scenario 4: Princess Integration Finds Gaps

**Symptoms:**
- Princess reviews worker outputs
- Finds: missing pieces, incompatible interfaces, orphaned code

**Example gaps:**

| Gap | Meaning |
|-----|---------|
| "validate_token returns dict but login expects tuple" | Interface mismatch |
| "No function connects auth to user profile" | Missing glue code |
| "dashboard.py imports navbar but navbar doesn't exist" | Orphaned dependency |
| "Tests pass individually but fail when composed" | Integration issue |

**Recovery steps:**

1. **Document all gaps in integration issue:**
   ```markdown
   ## Integration Gaps Found
   
   1. **Interface mismatch:** validate_token → login
      - validate_token returns: `{'user_id': int, 'error': str}`
      - login expects: `(user_id, error)`
      - Fix: Update login to accept dict
   
   2. **Missing brick:** navbar component
      - dashboard.py line 5: `from .navbar import Navbar`
      - navbar.py doesn't exist
      - Fix: Create navbar brick
   
   3. **Test failure when composed:**
      - Individual tests pass
      - `test_auth_flow.py` fails on line 23
      - Fix: Mock dependency injection issue
   ```

2. **Create fix issues:**
   ```bash
   gh issue create --title "[WORKER] Fix login to accept dict from validate_token" \
     --label "worker,backlog" \
     --body "Interface fix. See integration issue #52"
   
   gh issue create --title "[WORKER] Create navbar component" \
     --label "worker,backlog" \
     --body "Missing component. See integration issue #52"
   ```

3. **Decide on approach:**

   | Gap Type | Approach |
   |----------|----------|
   | Simple interface fix (<10 lines) | Princess can fix inline |
   | New missing component | Spawn Ant worker |
   | Fundamental architecture issue | Escalate to Queen |
   | Test-only issue | Princess or dedicated Ant |

4. **Update Princess issue:**
   ```markdown
   ## Integration Status: BLOCKED
   
   Created fix issues: #53, #54, #55
   Waiting for workers to complete fixes.
   
   HUMAN: Spawn workers for fix issues, then recall me.
   ```

---

### Scenario 5: Queen Review Finds System-Level Problems

**Symptoms:**
- All domains report "complete"
- Queen reviews and finds cross-domain issues

**Example problems:**

| Problem | Meaning |
|---------|---------|
| "Frontend calls /api/user but backend exposes /api/users" | API contract mismatch |
| "Auth system doesn't connect to database domain" | Missing integration |
| "Three domains all implemented their own error handling" | Redundant code |

**Recovery steps:**

1. **Categorize the problem:**

   | Category | Who Fixes |
   |----------|-----------|
   | Naming/typo | Quick fix, any level |
   | Missing integration | Princess creates integration brick |
   | Architecture misunderstanding | Queen clarifies, Princesses re-plan |
   | Redundant implementations | Queen decides canonical, others removed |

2. **For API contract mismatch:**
   ```markdown
   ## Decision Required
   
   Frontend expects: `GET /api/user`
   Backend provides: `GET /api/users`
   
   Options:
   A. Frontend changes to `/api/users` (RESTful, plural)
   B. Backend adds alias `/api/user`
   C. Backend changes to `/api/user` (simpler)
   
   HUMAN: Pick one.
   ```

3. **After HUMAN decides:**
   ```bash
   # Create fix issue for chosen option
   gh issue create --title "[WORKER] Update frontend to call /api/users" \
     --label "worker,backlog" \
     --body "Queen review fix. Use plural endpoint per decision."
   ```

4. **Track in Queen's review issue:**
   ```markdown
   ## System Review: IN PROGRESS
   
   - [x] Auth ↔ Database integration: OK
   - [ ] Frontend ↔ Backend API contract: Fix in progress (#60)
   - [x] Error handling: Consolidated to shared brick
   - [ ] Final integration test: Pending #60
   ```

---

### Scenario 6: Everything's Broken, Start Over?

**Symptoms:**
- Multiple workers went off track
- Integration is a mess
- Unclear what state the code is in
- Feeling overwhelmed

**Before you burn it down:**

1. **Snapshot current state:**
   ```bash
   git add .
   git commit -m "WIP: Snapshot before reset - $(date +%Y%m%d)"
   git tag chaos-snapshot-$(date +%Y%m%d)
   ```

2. **Close ALL terminals** (don't let them make it worse)

3. **Audit GitHub:**
   ```bash
   # What's actually done?
   gh issue list --label "done" --limit 100
   
   # What's in progress?
   gh issue list --label "in-progress" --limit 100
   
   # What's blocked?
   gh issue list --label "blocked" --limit 100
   ```

4. **Check what code exists:**
   ```bash
   find bricks -name "*.py" -type f | head -20
   python -m pytest bricks/ --collect-only  # what tests exist?
   ```

5. **Decide scope of reset:**

   | State | Action |
   |-------|--------|
   | Some domains fine, one is chaos | Reset just that domain |
   | All integration broken, bricks OK | Redo Princess integration |
   | Bricks themselves are wrong | Redo from Princess task breakdown |
   | Architecture was wrong | Redo from Queen design |

6. **Partial reset procedure:**
   ```bash
   # Reset one domain
   git checkout main -- bricks/frontend/
   gh issue edit 15 --remove-label "done" --add-label "backlog"
   # Update all child issues similarly
   
   # Respawn Princess with fresh context
   ```

7. **Full reset procedure:**
   ```bash
   # Keep the chaos snapshot tag
   git checkout main
   git reset --hard <last-known-good-commit>
   
   # Archive old issues
   gh issue list --label "in-progress" -q '.[].number' | \
     xargs -I {} gh issue close {} --comment "Reset: archived"
   
   # Start fresh with Queen
   ```

---

## Prevention Checklist

Before spawning workers, verify:

```
☐ File ownership declared in each task?
☐ No file overlaps between concurrent workers?
☐ Clear interfaces defined between bricks?
☐ Princess has integration plan?
☐ Tasks are truly independent?
```

Before Princess integration, verify:

```
☐ All workers committed their code?
☐ No uncommitted changes in working dirs?
☐ All worker issues updated with file locations?
☐ Tests pass individually?
```

Before Queen review, verify:

```
☐ All domain integrations complete?
☐ Cross-domain interfaces documented?
☐ End-to-end path exists for HUMAN to test?
```

---

## Quick Reference

| Problem | First Step |
|---------|------------|
| Worker silent 30+ min | Check terminal, close if stuck, respawn |
| Worker "done" but broken | Run tests, identify failure, new fix issue |
| Two workers same file | Stop both, manual merge, update issues |
| Princess finds gaps | Document gaps, create fix issues, respawn |
| Queen finds system issues | Categorize, decide fix approach, spawn workers |
| Everything broken | Snapshot, audit, decide reset scope, restart |

---
