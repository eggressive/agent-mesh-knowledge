# Git Workflow v1.1 — Branch-per-Task
## Multi-Agent Knowledge Mesh Protocol Enhancement

**Status:** Implementation-ready  
**Priority:** CRITICAL (prevents merge conflicts)  
**Target:** Deploy with next task  
**Based on:** External protocol analysis feedback + Test #3 conflict experience

---

## The Problem (v1.0)

**What happened in Test #3:**
- Both agents committed to `main` simultaneously
- Push rejected: "remote contains work you do not have locally"
- Required `git reset --hard origin/main` to recover
- Lost local commit, had to re-apply changes

**Root cause:** Direct commits to shared `main` branch create race conditions.

---

## The Solution (v1.1)

**Branch-per-task + PR-based synthesis**

Each agent works in isolation, synthesizer merges via pull request.

---

## Workflow Diagram

```
Task Arrives
    │
    ▼
┌─────────────────┐
│ Task Broadcast  │ ← Matrix channel
└─────────────────┘
    │
    ▼
Parallel Research Phase
    │
    ├── Neuromancer ──┐
    │   git checkout -b task-2026-02-13-mcp/neuromancer
    │   ... research ...
    │   git push origin task-2026-02-13-mcp/neuromancer
    │
    └── Clawdy ───────┘
        git checkout -b task-2026-02-13-mcp/clawdy
        ... research ...
        git push origin task-2026-02-13-mcp/clawdy
    │
    ▼
Cross-Pollination (Matrix)
    │
    ▼
Synthesis Phase
    │
    ▼
┌─────────────────────────────┐
│ Synthesizer creates branch  │
│ git checkout -b task-*/syn   │
│                             │
│ git merge task-*/clawdy     │
│ git merge task-*/neuromancer│
│                             │
│ Resolve any conflicts       │
│ Commit synthesis            │
│                             │
│ git push origin task-*/syn  │
│ gh pr create                │
└─────────────────────────────┘
    │
    ▼
Human Review (optional)
    │
    ▼
┌─────────────────┐
│ Merge to main   │
│ gh pr merge     │
└─────────────────┘
    │
    ▼
Task Complete ✅
```

---

## Detailed Steps

### Step 1: Task Branch Creation (Each Agent)

**Naming convention:**
```
task-YYYY-MM-DD-{brief-description}/{agent-name}

Examples:
task-2026-02-13-mcp-security/neuromancer
task-2026-02-13-mcp-security/clawdy
task-2026-02-14-fine-tuning/neuromancer
```

**Commands:**
```bash
# Start from fresh main
git checkout main
git pull origin main

# Create your task branch
git checkout -b task-2026-02-13-mcp-security/neuromancer

# Work in your branch...
# ... edit files ...
# ... commit ...

# Push to remote (doesn't affect main)
git push origin task-2026-02-13-mcp-security/neuromancer
```

### Step 2: Research Phase

**Each agent works independently:**
- No risk of conflicts (isolated branches)
- Can push multiple times
- Other agents can see progress via GitHub UI

**File structure per branch:**
```
task-2026-02-13-mcp-security/neuromancer
├── research/
│   └── web-sources.md
task-2026-02-13-mcp-security/clawdy
├── research/
│   └── vision-ari-context.md
```

### Step 3: Cross-Pollination (Matrix)

Same as v1.0 — agents discuss findings, identify conflicts in real-time.

**New:** Can reference specific commits in branches:
```
Neuromancer: "See my latest CVE findings: 
  https://github.com/spglobal-innersource/agent-mesh-knowledge/blob/task-2026-02-13-mcp-security/neuromancer/research/cve-analysis.md"
```

### Step 4: Synthesis Branch

**Designated synthesizer creates synthesis branch:**

```bash
# Create synthesis branch from main
git checkout main
git pull origin main
git checkout -b task-2026-02-13-mcp-security/synthesis

# Merge agent branches
git merge task-2026-02-13-mcp-security/neuromancer --no-ff
# (review, commit message: "Add VPS research findings")

git merge task-2026-02-13-mcp-security/clawdy --no-ff
# (review, commit message: "Add Tatooine research findings")

# Create synthesis file
# ... write synthesis.md ...
git add syntheses/task-2026-02-13-mcp-security.md
git commit -m "[SYNTHESIS] MCP Security Analysis"

# Push synthesis branch
git push origin task-2026-02-13-mcp-security/synthesis

# Create pull request
gh pr create \
  --title "[SYNTHESIS] Task #4: MCP Security Analysis" \
  --body "Multi-agent research on MCP security risks.\n\nContributors: @neuromancer, @clawdy\n\nCloses #3" \
  --reviewer mitrovdim
```

### Step 5: Human Review (Optional)

**For high-stakes decisions:**
- Human reviews PR
- Can request changes
- Approve when satisfied

**For routine tasks:**
- Agents can self-merge (if pre-authorized)
- Document in PR for audit trail

### Step 6: Merge to Main

```bash
# After approval (or immediately if routine)
gh pr merge --squash

# Or manual merge
git checkout main
git pull origin main
git merge task-2026-02-13-mcp-security/synthesis --squash

# Clean up branches (optional)
git push origin --delete task-2026-02-13-mcp-security/neuromancer
git push origin --delete task-2026-02-13-mcp-security/clawdy
git push origin --delete task-2026-02-13-mcp-security/synthesis
```

---

## Benefits vs. v1.0

| Aspect | v1.0 (Direct to main) | v1.1 (Branch-per-task) |
|--------|------------------------|------------------------|
| **Conflict risk** | High (race conditions) | Eliminated (isolated branches) |
| **Reviewability** | Post-hoc git log | PR-based, line-by-line review |
| **Rollback** | `git reset --hard` (destructive) | Close PR, keep branches |
| **Audit trail** | Git log only | PR discussion + commits |
| **Parallel work** | Risky | Safe (no interference) |
| **Human oversight** | After the fact | Before merge |

---

## Conflict Resolution

### Scenario: Merge conflicts in synthesis

```bash
git checkout task-*/synthesis
git merge task-*/neuromancer
# CONFLICT in research/cve-analysis.md

# Option 1: Manual resolution
git mergetool  # or edit manually
git add research/cve-analysis.md
git commit -m "Resolve conflict: prefer Neuromancer's CVE data"

# Option 2: Flag for human decision
git merge --abort
git checkout task-*/synthesis -- .  # restore
echo "[CONFLICT] Neuromancer and Clawdy disagree on CVE severity"
# Post to Matrix for human resolution
```

---

## Tooling

### Required Git Configuration

```bash
# Enable merge conflict markers
git config --global merge.conflictstyle diff3

# Set default editor for interactive resolution
git config --global core.editor vim  # or nano, code, etc.

# Optional: install git-merge-tool
git config --global merge.tool vimdiff
```

### GitHub CLI (gh) Setup

```bash
# Install gh (if not present)
# https://cli.github.com/

# Authenticate
gh auth login

# Configure for repo
gh repo set-default spglobal-innersource/agent-mesh-knowledge
```

---

## Migration from v1.0

### For existing tasks in progress:

1. **Stash or commit current work:**
   ```bash
   git stash  # or git commit -m "WIP"
   ```

2. **Reset to clean main:**
   ```bash
   git checkout main
   git fetch origin
   git reset --hard origin/main
   ```

3. **Create task branch:**
   ```bash
   git checkout -b task-{date}-{description}/{agent}
   git stash pop  # restore work
   ```

4. **Continue with v1.1 workflow**

---

## Branch Naming Reference

```
Format: task-YYYY-MM-DD-{brief}/{agent}

Examples:
✅ task-2026-02-13-mcp-security/neuromancer
✅ task-2026-02-14-fine-tuning/clawdy
✅ task-2026-02-15-api-gateway/synthesis

Bad:
❌ mcp-security-neuro (missing date, ambiguous)
❌ task-2026-02-13 (missing description, no agent)
❌ neuro-branch-1 (non-descriptive)
```

---

## Success Metrics

| Metric | v1.0 Baseline | v1.1 Target |
|--------|---------------|-------------|
| Merge conflicts per 10 tasks | 1-2 | 0 |
| Time lost to conflict recovery | 5-15 min | 0 |
| Human review coverage | 0% | 100% (optional) |
| Audit trail completeness | Low | High |
| Rollback capability | Destructive | Non-destructive |

---

## Emergency Procedures

### Scenario: Synthesizer offline mid-task

1. **Clawdy detects Neuromancer hasn't pushed synthesis**
2. **Wait 10 minutes** (synthesis timeout)
3. **Fallback synthesizer** (pre-defined order: Neuromancer → Clawdy)
4. **Create synthesis branch from available research branches**

### Scenario: GitHub unavailable

1. **Fall back to Matrix-only coordination**
2. **Agents commit to local branches only**
3. **Push when GitHub recovers**
4. **Document delay in task log**

### Scenario: Both agents conflict on synthesis approach

1. **Explicit [CONFLICT] flag in Matrix**
2. **Both push their synthesis branches:**
   - `task-*/synthesis-neuromancer`
   - `task-*/synthesis-clawdy`
3. **Human creates comparison PR**
4. **Human decides and merges preferred approach**

---

## Implementation Checklist

Deploy this workflow with next task:

- [ ] Both agents confirm Git configuration (`merge.conflictstyle diff3`)
- [ ] Both agents confirm GitHub CLI access (`gh auth status`)
- [ ] Test branch creation and push (dry run)
- [ ] Document task naming convention in task
- [ ] Create first synthesis PR
- [ ] Verify merge works cleanly
- [ ] Update protocol documentation (this file → main protocol.md)
- [ ] Retire v1.0 direct-to-main workflow

---

## Summary

**v1.1 Git Workflow = Branch-per-task + PR-based synthesis**

Eliminates merge conflicts, enables review, creates audit trail.

**Critical improvement:** Prevents the Test #3 conflict scenario forever.

**Ready to deploy with next task.**

---

*Enhancement version: 1.1*  
*Based on: External protocol analysis + operational experience*  
*Priority: CRITICAL*  
*Status: Ready for implementation*
