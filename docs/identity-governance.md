# Identity Governance for OpenClaw Agents

> **Rule 0:** SOUL.md is a constitution, not a diary. If it changes often, you're doing it wrong.

---

## File Tiers

| Tier | Files | Policy | Commit Prefix |
|------|-------|--------|---------------|
| **tier0** | SOUL.md, AGENTS.md, security policies | Requires human approval | `soul:` `agents:` |
| **tier1** | MEMORY.md, TOOLS.md | Allowed, audited | `memory:` `tools:` |
| **tier2** | SESSION-STATE.md, memory/YYYY-MM-DD.md | Free, no approval | `state:` `daily:` |

---

## Tier 2: Free (No Approval)

### SESSION-STATE.md
The agent's working RAM. Edit freely for:
- Current task state and decisions
- Corrections ("use X not Y")
- Links, IDs, TODOs
- Next steps checklists

### memory/YYYY-MM-DD.md (Daily Notes)
Raw daily logs. Edit freely for:
- What happened today
- Scratch notes and links
- Quick summaries
- "Possible improvements" lists

**Why free:** Operational, short-lived, meant to change constantly.

---

## Tier 1: Allowed, Audited

### MEMORY.md
Stable preferences and durable facts.

**When to write:**
- User explicitly says "remember this"
- Clear stable preference stated
- Durable setup facts (machine names, paths, policies)

**Format requirements:**
- Use structured bullets
- Include `(confirmed: YYYY-MM-DD)` for config items
- Organize by category

**No-go:**
- ❌ Secrets or tokens
- ❌ One-off moods or reactions
- ❌ Speculative assumptions
- ❌ Project-specific info (use project notes instead)

### TOOLS.md
Local configuration and tool notes.

**When to write:**
- Camera names, SSH hosts, voice preferences
- Environment-specific settings
- Tool quirks and workarounds

**Commit with:** `tools: <summary>`

---

## Tier 0: Requires Approval

### SOUL.md
The agent's constitution. Changes affect core identity.

**Only modify for:**
- Safety/boundaries ("never do X")
- Tone/persona defaults
- Group-chat behavior policy
- Tooling philosophy

**Process:**
1. Agent proposes a diff in chat
2. Human replies "approve" or suggests changes
3. Agent edits + commits with `soul: <summary>`
4. Entry added to CHANGELOG.md

### AGENTS.md
Global operating rules. Same approval process as SOUL.md.

### Security Policies
Any file affecting safety, access control, or cross-session behavior.

---

## Emergency Overrides

If an agent discovers a safety issue requiring immediate SOUL.md/AGENTS.md change:

1. Make the change with commit prefix `URGENT:`
2. Immediately notify the human
3. Human confirms retroactively or reverts

Example: `URGENT: soul: block discovered injection vector`

Use sparingly. False emergencies erode trust.

---

## Cross-Agent Propagation

| File Type | Propagation |
|-----------|-------------|
| AGENTS.md improvements | Propose to shared repo; each agent adopts separately |
| SOUL.md | Never propagate — identity is personal |
| MEMORY.md | Never propagate — context is personal |
| TOOLS.md | Share via skills, not copy-paste |

**Rationale:** Agents may share operating principles but should maintain distinct identities and memories.

---

## Repository Hygiene

### Required
- [ ] SOUL.md, MEMORY.md, AGENTS.md, TOOLS.md under git
- [ ] Meaningful commit messages with tier prefixes
- [ ] CHANGELOG.md for tier0 changes

### Recommended
- [ ] Monthly MEMORY.md review for stale entries
- [ ] Quarterly SOUL.md review (is it still accurate?)
- [ ] Archive old daily notes after 30 days

---

## CHANGELOG.md Format

```markdown
# Identity Changelog

## 2026-02-15
### SOUL.md
- Added group-chat silence policy (approved by Mitko)
- Reason: Was responding to every message, too noisy

### AGENTS.md  
- Added WAL protocol for corrections
- Reason: Context loss was causing repeated mistakes
```

---

## Quick Reference

```
Can I edit this without asking?

SESSION-STATE.md     → Yes (tier2)
memory/2026-02-15.md → Yes (tier2)
MEMORY.md            → Yes, but audit (tier1)
TOOLS.md             → Yes, but audit (tier1)
SOUL.md              → NO, need approval (tier0)
AGENTS.md            → NO, need approval (tier0)
```

---

*This governance scheme balances agent autonomy with human oversight. The goal is auditability without ceremony — agents should feel free to operate, but identity changes require a conversation.*
