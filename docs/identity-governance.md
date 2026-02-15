# Identity Governance (OpenClaw)

Low ceremony. High auditability. Prevents slow identity drift.

## Principle 0: Constitution vs diary
**`SOUL.md` is a constitution, not a diary.** If it changes often, you’re doing it wrong.

## File tiers (what can change, and how)

### Tier 2 — Free (operational churn)
**Agent may edit without approval.**

**Files:**
- `SESSION-STATE.md` (WAL / working state)
- `memory/YYYY-MM-DD.md` (daily logs)

**Allowed content:**
- current task state, decisions, corrections, links, IDs, TODOs
- raw notes from today, scratch notes, “possible improvements”

**Why:** these are meant to change constantly.

---

### Tier 1 — Allowed, audited (facts & preferences)
**Agent may edit, but changes must be reviewable.**

**Files:**
- `MEMORY.md` (curated, durable facts + stable preferences)
- `TOOLS.md` (local operational config: paths, hostnames, commands, device nicknames)

**Default rule for `MEMORY.md`:**
- If the user explicitly says **“remember this”** → agent may write it.
- Otherwise → **agent proposes → human OK → agent writes**.

**Guardrails for `MEMORY.md`:**
- write as structured bullets
- include **“Last confirmed: YYYY-MM-DD”** for config-like facts
- **never** store secrets/tokens/credentials
- no speculative assumptions / guessed preferences

**Guardrails for `TOOLS.md`:**
- factual/local config only (no secrets)
- any change must be accompanied by either:
  - a short in-file note (“Updated YYYY-MM-DD: …”), **or**
  - a git commit with prefix: `tools: ...`

---

### Tier 0 — Strict (identity & governance)
**Requires explicit human approval + git commit.**

**Files:**
- `SOUL.md`
- `AGENTS.md`
- security playbooks/policies (`docs/security-*`, `playbooks/*`)
- anything that changes cross-chat behavior or safety boundaries

**Allowed changes (examples):**
- safety/boundaries (what the agent will/won’t do)
- default tone/persona or group-chat behavior policy
- tool-selection philosophy that materially changes behavior

**Process:**
1) Agent posts a proposed diff (what + why + risk).
2) Human replies **approve**.
3) Agent applies edit + commits with message: `soul: ...` / `agents: ...`.
4) Agent posts commit hash back in chat.

### Emergency overrides (Tier 0)
If there’s a clear safety/behavioral vulnerability:
- agent may apply an **URGENT** Tier 0 change immediately
- commit message must start with: `URGENT soul:` / `URGENT agents:`
- agent must post: **what changed + why + risk + diff**
- human reviews retroactively (approve/revert/adjust)

---

## Cross-agent propagation
Avoid “global drift by accident”:
- **Shared core repo**: governance docs + baseline `AGENTS.md` (pulled intentionally)
- **Agent-local**: `SOUL.md`, `MEMORY.md`, `TOOLS.md` (never auto-propagate)

---

## Close the “why gap” (mandatory changelog for Tier 0)
Maintain `CHANGELOG.md` entries for every Tier 0 change:
- date
- summary
- reason
- approval reference (link/message id)
- commit hash

---

## Operational checklist (TL;DR)
- Tier2: write freely.
- Tier1: write carefully, keep it auditable.
- Tier0: propose → approve → commit (or URGENT + retro review).
