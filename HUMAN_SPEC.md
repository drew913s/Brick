# Human Operator Specification v1.0

**Operating manual for humans running multi-agent AI coding sessions**  
**Repository:** https://github.com/drew913s/Brick  
**Last Updated:** 2025-12-01

---

## Purpose

This specification defines how human operators manage disposable AI coding sessions in the ant colony model. The human is the router, tester, and decision-maker. AI sessions are workers.

**Core Principle:** You are the only persistent intelligence. Sessions die. GitHub remembers. You decide.

---

## Your Role

| Role | What It Means |
|------|---------------|
| **Visionary** | What to build, what matters, what's good enough |
| **Router** | Spawn terminals, close terminals, assign work |
| **Tester** | Does it work? Can you use it? Does it do the thing? |
| **Decision-maker** | When AI asks, you answer. When blocked, you unblock. |

**What you DON'T do:**
- Debug AI-generated code (replace the session instead)
- Argue with stuck sessions (close them)
- Track context in your head (GitHub tracks it)
- Write code yourself (unless you want to)

---

## Tracking System

### Terminal Tracker

Track active terminals. Options:

**Option A: Physical Index Cards**
```
┌─────────────────────────────────┐
│ ID: Q-FE-1                      │
│ Role: Worker                    │
│ Task: Build auth UI             │
│ GitHub: #47                     │
│ Status: ☐ Working ☐ Blocked    │
│         ☐ Test Ready ☐ Done    │
│ Started: 2:30pm                 │
│ Last Update: 3:15pm             │
└─────────────────────────────────┘
```
- One card per terminal
- Spread on desk
- Move to "Done" pile when complete
- Throw away when abandoned

**Option B: Simple Spreadsheet**

| ID | Role | Task | GitHub # | Status | Started | Last Update | Notes |
|----|------|------|----------|--------|---------|-------------|-------|
| Q | Queen | Overall arch | #1 | WAITING | 2:00pm | 2:15pm | Waiting on princesses |
| Q-FE | Princess | Frontend | #2 | WAITING | 2:15pm | 2:30pm | Waiting on workers |
| Q-FE-1 | Worker | Auth UI | #5 | WORKING | 3:00pm | 3:30pm | |
| Q-FE-2 | Worker | Dashboard | #6 | TEST_READY | 3:15pm | 3:45pm | **TEST THIS** |
| Q-BE-1 | Worker | API endpoints | #8 | ABANDONED | 3:00pm | 3:00pm | Went off track |

**Option C: GitHub Projects Board**
- Use labels: `in-progress`, `test-ready`, `blocked`, `done`
- Use milestone per project
- View as Kanban board in browser

### Phase Tracker

Know which phase you're in:

```
☐ Phase 1: Queen designs system
☐ Phase 2: Princesses design domains
☐ Phase 3: Workers build (Wave 1)
☐ Phase 4: Princesses integrate
☐ Phase 5: Queen reviews
☐ Phase 6: HUMAN tests full system
```

### Queues (from GitHub)

| Queue | Where | Action |
|-------|-------|--------|
| Test Queue | Label: `test-ready` | You test these |
| Decision Queue | Label: `blocked` | You decide these |
| Review Queue | Label: `code-complete` | Sessions waiting on you |

---

## Size Constraints

| Constraint | Limit | Why |
|------------|-------|-----|
| Active terminals | Max 20 | You can't track more |
| Tracker size | One screen | If you scroll, you're lost |
| Task size | ≤50 lines per brick | Fits in session context |
| Wave size | 5-10 workers | Manageable parallelism |

**If overwhelmed:**
1. STOP spawning new workers
2. Let current wave finish
3. Test what's ready
4. Then start next wave

---

## Spawn Protocol

**Before opening a new terminal:**

1. ☐ Is the GitHub issue created?
2. ☐ Is the task small enough (one thing, ≤50 lines)?
3. ☐ Do I have a terminal ID assigned?
4. ☐ Can I add one more card to my tracker?
5. ☐ Is there room in current wave?
6. ☐ **File conflict check:** Do any files overlap with in-progress workers?

**Spawn steps:**

1. Open new terminal (iTerm, Terminal, VS Code, etc.)
2. Start Claude Code session
3. Paste bootstrap prompt (see SESSION_SPEC.md)
4. Note on tracker: ID, GitHub #, time started
5. Let it work

---

## Check-In Rhythm

**Every 30 minutes:**

1. Scan terminal tracker - any stale (no update 30+ min)?
2. Check GitHub board - any `test-ready`?
3. Check GitHub - any `blocked` needing decisions?
4. Close any completed terminals
5. Spawn new workers if wave has room

**Quick scan checklist:**
```
☐ All workers updated in last 30 min?
☐ Any test-ready items?
☐ Any blocked items?
☐ Any terminals to close?
☐ Room for more workers?
```

---

## Test Protocol

When a task is marked `test-ready`:

1. Read the issue's access instructions
2. Go to URL / run command / find button
3. Try the happy path (does it work?)
4. Try an edge case (does it handle errors?)
5. Record result:
   - **Pass:** Move to `done`
   - **Fail:** Comment what failed, move to `backlog`, spawn new worker

**Test result comment template:**
```markdown
## Test Result - [timestamp]
**Tester:** HUMAN
**Result:** PASS / FAIL

**Steps taken:**
1. [what you did]
2. [what you did]

**Expected:** [what should happen]
**Actual:** [what happened]

**Verdict:** [pass/fail with notes]
```

---

## Decision Protocol

When a task is `blocked`:

1. Read the blocker description in issue
2. Understand the options presented
3. Make a decision (don't overthink)
4. Comment your decision on the issue
5. Remove `blocked` label, add `backlog` or `in-progress`
6. If worker is waiting, tell them to proceed

**Decision comment template:**
```markdown
## Decision - [timestamp]
**Decided by:** HUMAN

**Question:** [what they asked]
**Decision:** [your choice]
**Rationale:** [brief reason]

**Next:** [what should happen now]
```

**If you don't know:**
- Pick the simpler option
- Note it's provisional ("try this, we can change later")
- Don't block on perfect decisions

---

## Abandon Protocol

### Signs a Session Needs Abandoning

| Symptom | What It Means | Action |
|---------|---------------|--------|
| "I think we should discuss..." | Stalling | Abandon |
| "Before I do that, let me explain..." | Deflecting | Abandon |
| 500+ words, no code | Lost | Abandon |
| Claims "done" but no URL/access | Lying (confused) | Abandon |
| Same error 3+ times | Stuck in loop | Abandon |
| Working on different task | Context lost | Abandon |
| Argues about task validity | Rebellion | Abandon |
| 30+ min silence, no update | Crashed/stuck | Check GitHub, maybe abandon |

### How to Abandon

```
1. Don't argue with it
2. Close the terminal (⌘W / Ctrl+D / click X)
3. Cross off tracker (or move to "Abandoned" pile)
4. Check GitHub - is the issue updated?
   - If yes: spawn fresh session, point to issue
   - If no: you may need to re-explain in new session
5. Note what went wrong (for pattern recognition)
```

### Abandon Recovery

If session died without updating GitHub:

1. Check what files it created/modified
2. Read the code if helpful
3. Update the GitHub issue yourself with:
   - What got done
   - What's remaining
   - Any learnings
4. Spawn new session with that context

---

## Gap Detection

Watch for these gaps that sessions miss:

| Gap Type | Symptom | Fix |
|----------|---------|-----|
| MISSING_UI | Code done, no interface | Create UI task, spawn worker |
| NO_ACCESS_METHOD | Says "test-ready" but no URL | Reject, require access info |
| ORPHANED_FEATURE | Built but not connected | Integration task for Princess |
| STALE_WORKER | No update 30+ min | Check in, maybe abandon |
| BACKEND_ONLY | API exists, no frontend | Create frontend task |

**Before accepting `test-ready`:**
```
☐ Is there a URL I can visit?
☐ Is there a command I can run?
☐ Is there a button I can click?
☐ Do I know what "success" looks like?
☐ Do I know what "failure" looks like?
```

---

## Phase Flow

### Phase 1: Queen Designs
1. Open Terminal Q (Queen)
2. Paste Queen bootstrap with project brief
3. Queen creates domain specs as issues
4. Queen tells you which Princesses to spawn
5. Close Terminal Q (Queen is done for now)

### Phase 2: Princesses Design
1. Open Terminal Q-FE, Q-BE, Q-DB (per Queen's instructions)
2. Paste Princess bootstraps, point to parent issues
3. Princesses create worker tasks as issues
4. Princesses tell you which Ants to spawn
5. Close Princess terminals (they return later)

### Phase 3: Workers Build (Wave)
1. Open 5-10 Ant terminals (per Princess instructions)
2. Paste Ant bootstraps, point to task issues
3. Workers write code, update issues
4. Workers mark `code-complete` when done
5. Close worker terminals as they complete
6. Spawn next wave if more tasks

### Phase 4: Princesses Integrate
1. Reopen Princess terminals (fresh sessions)
2. Paste Princess bootstrap with "integration mode"
3. Princesses review worker output, integrate
4. Princesses mark domain `code-complete`
5. Close Princess terminals

### Phase 5: Queen Reviews
1. Reopen Terminal Q (fresh session)
2. Paste Queen bootstrap with "review mode"
3. Queen reviews all domain integrations
4. Queen marks system `test-ready`
5. Close Terminal Q

### Phase 6: HUMAN Tests
1. Test the full system yourself
2. File issues for bugs found
3. Spawn workers for fixes
4. Repeat until satisfied
5. Mark project DONE

---

## Quick Reference Card

**Print this and keep at desk:**

```
┌────────────────────────────────────────────┐
│           ANT COLONY QUICK REF             │
├────────────────────────────────────────────┤
│ EVERY 30 MIN:                              │
│ □ Check tracker - any stale?               │
│ □ Check GitHub - test-ready?               │
│ □ Check GitHub - blocked?                  │
│ □ Close done terminals                     │
│ □ Spawn if room                            │
├────────────────────────────────────────────┤
│ ABANDON IF:                                │
│ • Argues or philosophizes                  │
│ • 500 words, no code                       │
│ • "Done" but no access method              │
│ • Same error 3x                            │
│ • Wrong task                               │
│ • 30 min silence                           │
├────────────────────────────────────────────┤
│ BEFORE ACCEPTING TEST-READY:               │
│ □ URL/command/button exists?               │
│ □ Know what success looks like?            │
│ □ Know what failure looks like?            │
├────────────────────────────────────────────┤
│ SPAWN CHECKLIST:                           │
│ □ GitHub issue exists?                     │
│ □ Task ≤50 lines?                          │
│ □ ID assigned?                             │
│ □ Room in tracker?                         │
└────────────────────────────────────────────┘
```

---

## Troubleshooting

### "All my workers are stuck"
- Check if they're all blocked on same thing
- Make the decision, unblock them
- If different issues, abandon stuck ones and respawn

### "Worker claims done but I can't find the feature"
- Abandon
- Create new task: "Create UI for [feature]"
- Spawn worker for UI task

### "I've lost track of what's happening"
- Stop all spawning
- Review GitHub board
- Close any unclear terminals
- Update your tracker from GitHub
- Resume with clear state

### "Session keeps going off track"
- Task might be poorly defined
- Review the issue - is it clear?
- Rewrite issue with more specific requirements
- Spawn fresh session

### "Same bug keeps appearing"
- Might be architecture issue (Princess level)
- Escalate to Princess session
- Or the spec is wrong (Queen level)
- Don't keep spawning workers for the same problem

---

## Anti-Patterns

### ❌ Arguing with a stuck session
**Don't:** Spend 20 minutes trying to get it back on track  
**Do:** Close terminal, spawn fresh

### ❌ Tracking in your head
**Don't:** "I think Q-FE-3 was working on the login..."  
**Do:** Check tracker, check GitHub

### ❌ Too many parallel workers
**Don't:** Spawn 30 workers and lose track  
**Do:** Max 20 active, in waves of 5-10

### ❌ Accepting "done" without testing
**Don't:** Trust the AI's word that it works  
**Do:** Click the URL, run the command, verify yourself

### ❌ Making decisions for the AI
**Don't:** "I'll just fix this one line myself"  
**Do:** Comment decision on issue, spawn worker to implement

---

## Success Criteria

A task is **DONE** when:
- [ ] You can access it (URL, button, command)
- [ ] You tested it
- [ ] It works as expected
- [ ] GitHub issue moved to Done

A project is **DONE** when:
- [ ] All tasks marked Done
- [ ] You tested the integrated system
- [ ] It does what you wanted
- [ ] You're satisfied

---

## Version History

- **v1.0** (2025-12-01): Initial specification
  - Defined human roles
  - Created tracking systems
  - Established protocols
  - Added troubleshooting guide

---

## Related Documentation

- **SESSION_SPEC.md** - How AI sessions behave
- **BRICK_SPEC.md** - Core brick requirements
- **BOOTSTRAP_PROMPTS.md** - Ready-to-paste prompts
- **CONFLICT_RESOLUTION.md** - Handling concurrent edits, rate limits, recovery scenarios

---

**End of Human Operator Specification**
