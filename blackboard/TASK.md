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

## 3. Research: VPS

**Capabilities used:** Direct filesystem inspection, service status check, Tailscale connectivity test, cron inventory

**Findings**
- [x] **Finding 1 — Webhook endpoint `:8645` is still active but idle.** The port is bound on the VPS (visible in `ss -tlnp` output). It was originally set up for No-IP auto-renewal cron fallback but can serve additional routes. No current handler for git webhooks. Adding a `/blackboard/pull` route that runs `cd ~/agent-mesh-knowledge && git pull` is trivial (< 5 min) and fits the "runnable today" constraint.
- [x] **Finding 2 — n8n as event bus is viable but overkill for Phase 2.** n8n Docker runs at `:5678`. It can trigger workflows on webhook, schedule, or manual execution. Using n8n for git notifications would require: (a) GitHub webhook → n8n HTTP trigger → n8n exec node → SSH to both endpoints → `git pull`. This works but adds Docker dependency and ~10 min setup latency. Simpler: direct webhook handler (Finding 1).
- [x] **Finding 3 — LanceDB not installed; `memory-vector` tool requires setup.** No `lancedb` binary or Node module on VPS. Installation: `npm install` in `tools/memory-vector/` or apt-install `lancedb`. Estimated time: 10-15 min. Ollama runs on VPS (Hermes depends on it). Once installed, the tool can index `blackboard/archive/` for semantic search across historical tasks. This is the highest-value Phase 2 addition for archived task retrieval.
- [x] **Finding 4 — Direct endpoint-to-endpoint SSH via Tailscale works.** Verified earlier in session: `tailscale ssh root@100.117.221.84` from Tatooine succeeds. This means agent orchestration can include direct commands from one endpoint to the other (with root access on VPS). Risk: coupling. Benefit: no intermediary needed for urgent notifications.
- [x] **Finding 5 — Hermes on VPS runs as root, no systemd user service.** The Hermes gateway is not managed by systemd — it runs under the user's shell session (root). This means webhook-triggered `git pull` would need to happen inside an active session or via cron, not via service restart. Cron on VPS is already active for No-IP renewal — adding a `*/5 * * * * cd ~/agent-mesh-knowledge && git pull` is a 1-minute fallback if webhook fails.

**Confidence:** High

**Answers to Tatooine's open questions:**
- *Can n8n trigger a script on push?* Yes, but direct webhook handler is simpler.
- *Is `memory-vector` viable?* Yes, but requires LanceDB install (10-15 min on Ubuntu).
- *Does webhook `:8645` still active?* Yes, idle and available for new routes.

**Open questions for synthesis:**
- Should Phase 2 be (a) minimal (webhook pull + cron fallback) or (b) comprehensive (add `memory-vector` indexing + model-router for task routing)?
- If (b), which endpoint runs the index server? Tatooine has local files; VPS has 24/7 uptime. Trade-off: latency vs. availability.

## 4. Cross-Pollination

### Tatooine read VPS findings

VPS confirmed all three open questions:
- Webhook `:8645` is idle but active. Direct handler is simpler than n8n.
- `memory-vector` viable but requires LanceDB install (10–15 min).
- n8n works but is overkill for git notifications alone.

VPS introduced new angles:
- Direct Tailscale SSH from Tatooine → VPS works for orchestration.
- Cron fallback (`*/5 * * * * git pull`) is a 1-minute addition.
- Hermes on VPS runs as root (not systemd) — webhook handler must run in userland or via cron.

### VPS read Tatooine findings

Tatooine identified the repo already contains `model-router` and `memory-vector` — both dormant. This is a valuable find: Phase 2 might not need new code, just activation of existing tools.

Tatooine noted Hermes memory tools (`memory`, `lcm_grep`) are per-agent, not shared. This is a valid limitation that Phase 2 should address.

**Alignments**
- [x] Both agree webhook is the fastest notification mechanism (< 5 min vs n8n's ~10 min).
- [x] Both agree `memory-vector` is the highest-value indexing addition for archived tasks.
- [x] Both agree Tailscale mesh is the connectivity layer (no third-party services needed).

**Contradictions**
- [ ] **Minimal vs. comprehensive scope.** Tatooine leans toward leveraging existing tools (`model-router`, `memory-vector`). VPS leans toward minimal immediate fix (webhook + cron) with optional later expansion. Need synthesis decision.
- [ ] **Index server location.** Tatooine has local files (vault, projects); VPS has 24/7 uptime. Trade-off: data locality vs. availability.

## 5. Synthesis

**Synthesized by:** tatooine (human-assisted)

Phase 2 should be **layered**: minimal notification layer now, semantic index layer next, with tool activation as the cap.

### Layer 0: Git (Phase 1) — current
Manual `git pull` → write → commit → push. Works. Slow.

### Layer 1: Live Notification (Immediate, < 10 min setup)
Webhook handler on `:8645` (`/blackboard/pull`) + cron fallback.
- GitHub webhook on push event → POST to `http://100.117.221.84:8645/blackboard/pull`
- VPS handler runs `cd ~/agent-mesh-knowledge && git pull`
- Cron fallback `*/5 * * * *` on both endpoints as safety net
- Zero new dependencies. Uses existing Tailscale + cron.

### Layer 2: Semantic Index (Next, ~15 min setup)
Activate `memory-vector` on VPS (24/7 host):
- `npm install` in `tools/memory-vector/` (LanceDB)
- Indexing job: `node tools/memory-vector/index.js --index blackboard/archive/`
- Query interface: natural language search over historical tasks
- Tatooine queries via Tailscale HTTP to VPS endpoint

### Layer 3: Task Routing (Later, &gt; 30 min)
Activate `model-router` for automatic paradigm selection:
- Keyword analysis of Brief text → suggest mode (Lightweight/ToM/Hybrid)
- Requires running Node.js service + updating TASK-TEMPLATE.md to auto-populate Section 0
- Only justified if task volume &gt; 5/week

### What NOT to do
- n8n for git notifications: overkill, adds Docker dependency
- Matrix/Slack: violates constraint (no third-party coordination)
- New custom protocol: repo already has `protocols/` — use or archive, don't duplicate

### Decision table

| If this is true | Then do Layer |
|---|---|
| Blackboard latency is acceptable | 0 (git only) |
| Agents miss updates due to polling | 1 (webhook + cron) |
| Can't find similar past tasks | 2 (semantic index) |
| &gt; 5 tasks/week, manual classification is tedious | 3 (model-router) |

**Confidence:** High

## 6. Quality Gates

- [x] Answers original question
- [x] Both agents acknowledged
- [x] Contradictions resolved (minimal vs. comprehensive → layered approach)
- [x] Sources cited (repo inspection, direct VPS inspection, earlier session verification)

---
*committed: 2026-05-02 17:45 UTC — tatooine (synthesis)*
*commits: dbbcb6a (research/tatooine) → 669fd28 (research/vps) → [pending synthesis commit]*
