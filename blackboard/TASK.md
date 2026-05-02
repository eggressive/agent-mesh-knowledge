---
status: open
question: |-
  How should Agent-Mesh Phase 2 extend the blackboard beyond git?
agents: [tatooine, vps]
started: 2026-05-02 17:15 UTC
---

## 0. Paradigm Selection

> [!important] Check one before research begins.
> Human or seed agent classifies the task. Agents adjust depth accordingly.

- [ ] **Lightweight (Han & Zhang)** — factual research, aggregation, verification
  - Token-efficient, parallel agents, role specialization, no mental modeling
  - Example: "What's the state of X?" "Aggregate the latest benchmarks on Y."
- [ ] **ToM-prompted (Riedl)** — creative tasks, adversarial analysis, conflict resolution
  - Emergence, deep complementarity, belief-modeling, higher token cost
  - Example: "Resolve the contradiction between A and B." "Design a strategy for adversarial scenario C."
- [x] **Hybrid (default)** — most real tasks
  - Blackboard structure (shared memory, control unit) + mandatory ToM in cross-pollination (section 4)
  - Only pays the deep modeling cost when the task requires it

**Classified by:** Mitko (human)
**Rationale:** Requires factual survey of existing tools/protocols + creative design of next-phase architecture. Hybrid covers both requirements.

## 1. Brief

Agent-Mesh Phase 1 uses git as the shared blackboard. Two endpoints (Tatooine local, VPS remote) write to the same `TASK.md` in `agent-mesh-knowledge/blackboard/`. The mechanism works but has known limitations:

- Latency: requires explicit `git pull` → write → `git commit` → `git push` cycles
- No notifications: agents only see updates when they poll
- No structured indexing: archived tasks exist but are not searchable beyond `grep`
- No automatic conflict resolution: merge conflicts surface as text, not as structured contradictions
- Single file bottleneck: only one task active at a time

**Question:** What should Phase 2 add to extend the blackboard beyond git, and why?

**Constraints:**
- Must work with current Hermes topology (Tatooine Fedora ↔ VPS Ubuntu 24.04, both running Hermes v0.12.0)
- No Matrix, no Slack, no third-party coordination services unless justified
- Must be runnable today or with minimal setup (< 30 min per endpoint)
- Should leverage tools already in the repo (`model-router`, `memory-vector`) if viable

## 2. Research: Tatooine

**Capabilities used:** Local filesystem search, Obsidian vault search, repository inspection

**Findings**
- [x] **Finding 1 — Existing tool inventory in the repo.** The `agent-mesh-knowledge` repo already contains:
  - `tools/model-router/` — Node.js prefix-based model router with keyword routing via `skill.json`. Supports keyword→model mapping (e.g., "security" → Opus). Not currently running.
  - `tools/memory-vector/` — Node.js semantic search using LanceDB + Ollama embeddings. Requires LanceDB install + Ollama running. Not currently running.
  - `protocols/` — Memory Architecture v1.0 (3-tier), Bayesian Update v1.3, Git Workflow v1.1, Authentication v1.2 (Ed25519 signing). Designed for old topology but runtime-independent.
- [x] **Finding 2 — VPS services inventory.** From verified data, the VPS already runs:
  - n8n (Docker), webhook handlers, cron jobs. n8n at `:5678` with Gmail OAuth2 and n8n-mcp at `:3000`.
  - These could serve as event bus or automation trigger for blackboard updates.
- [x] **Finding 3 — Git webhook possibility.** GitHub supports webhooks on push events. The VPS webhook endpoint `:8645` exists (from memory). Could trigger Hermes to `git pull` blackboard on push.
- [x] **Finding 4 — Hermes memory tools.** Hermes v0.12.0 has `memory` tool (save/retrieve persistent facts) and `lcm_grep` (search session history). Not directly shared between endpoints but available per-agent.
- [x] **Finding 5 — Limitation: no inter-endpoint messaging.** Tailscale provides mesh connectivity but no messaging/pub-sub layer. Agents must poll git or implement a push mechanism.

**Confidence:** High

**Open questions for VPS:**
- Can n8n trigger a script on push? Would need a webhook handler that runs `git pull` in `~/agent-mesh-knowledge/`.
- Is `memory-vector` viable to index archived tasks? Requires LanceDB install (apt or binary).
- Does the VPS have webhook `:8645` still active, or was that for old topology only?

## 4. Cross-Pollination

Tatooine read VPS findings: [to be filled after VPS research]
VPS read Tatooine findings: [to be filled after VPS research]

**Alignments**
- [ ] Finding X supports Finding Y

**Contradictions**
- [ ] [Conflict description — requires resolution]

## 5. Synthesis

**Synthesized by:** [agent name]

[To be filled after cross-pollination]

**Confidence:** High / Medium / Low

## 6. Quality Gates

- [ ] Answers original question
- [ ] Both agents acknowledged
- [ ] Contradictions resolved or flagged for human
- [ ] Sources cited

---
*committed: 2026-05-02 17:16 UTC — tatooine*
