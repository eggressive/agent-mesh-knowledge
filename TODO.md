# Agent-Mesh — Engineering Roadmap

> Operational backlog derived from open-source blackboard/orchestration research (May 2026).
> Each item maps to a proven pattern from production multi-agent systems.
> Priority = P0 (blocker) → P1 (next) → P2 (soon) → P3 (later).

---

## P0 — Crash Recovery (Checkpoint & Resume)

**Why now:** Sessions die (timeout, context exhaustion, network drop). A crashed VPS session mid-Section-3 means half-written `TASK.md` and hallucination on the next cron pull.

**Pattern:** Write atomic JSON checkpoints at every phase boundary. On cold start, read the checkpoint and resume from `next` step — never restart from scratch.

**Deliverable:**
- `checkpoints/` directory with `{task-slug}.json` files
- Checkpoint written atomically (`.tmp` → `mv`) after each section completes
- Cron bootstrap checks for latest checkpoint before writing
- Template fields: `phase`, `step`, `completed[]`, `next`, `artifacts[]`, `pending_tasks[]`, `updated_at`

**Effort:** Low (~1–2 hrs)  
**Impact:** Very High — zero lost work across ephemeral sessions

**Reference:** `orchestration-playbook/patterns/checkpoint-resume.md`

---

## P0 — Failure Isolation (Circuit Breaker + Dead Letter Queue)

**Why now:** VPS hits rate limits (429) or service outages (503). Naive retries hammer the API, burn budget, and get the IP throttled. No failure isolation exists today.

**Pattern:**
- **Circuit Breaker:** Per-provider JSON state (`CLOSED` → `OPEN` → `HALF-OPEN`). 3 failures in 60s = 5-min cooldown.
- **Dead Letter Queue:** Failed tasks are serialized to `dead-letters/{task-id}.json` instead of dropped. Periodic sweep retries when breaker is `CLOSED`.

**Deliverable:**
- `.agent-mesh/circuit-breakers/{provider}.json` (e.g., `openwebsearch.json`)
- `dead-letters/` directory with structured failure records
- Cron sweep script: retry dead letters whose `retry_after` has passed
- Distinguish transient (429, 503, timeout) vs. logic errors (400, 401) — only transient goes to DLQ

**Effort:** Low (~2–3 hrs)  
**Impact:** Very High — prevents retry storms, survives provider outages

**Reference:** `orchestration-playbook/patterns/circuit-breaker.md`, `patterns/dead-letter-queue.md`

---

## P1 — Structured Task Envelope + Error Events

**Why now:** Agents can silently fail and write nonsense into a section. The next agent consumes it uncritically, producing a hallucination cascade. No acceptance criteria or budget guardrails exist.

**Pattern:** Every `TASK.md` carries an operational envelope in the frontmatter: Goal, Acceptance Criteria, Inputs, Budget (max tool calls / cost), Stop Conditions, and mandatory structured status reporting (`COMPLETED` / `FAILED` / `BLOCKED`).

**Deliverable:**
- Extend `TASK-TEMPLATE.md` with envelope fields:
  ```yaml
  envelope:
    goal: "..."
    acceptance_criteria: ["..."]
    budget_tools: 5
    budget_usd: 0.50
    stop_on: ["missing_input", "auth_error"]
    escalation: notify   # autonomous | notify | gate
  ```
- Every agent appends `STATUS: {state} | ...` to its output section
- Orchestrator (cron script) parses status before allowing downstream work
- If `FAILED`, pause dependent sections and surface to human

**Effort:** Medium (~3–4 hrs)  
**Impact:** High — stops bad-data cascades, enforces cost discipline

**Reference:** `orchestration-playbook/patterns/structured-error-events.md`, `patterns/task-envelope.md`

---

## P1 — Semantic Vector Memory (Phase 2.2)

**Why now:** README defers this to "when grep on archive/ becomes painful." With growing archive, keyword search misses conceptually related tasks. This unlocks Phase 2.2 without cloud dependencies.

**Pattern:** Embed every archived `TASK.md` using `all-MiniLM-L6-v2` (~90MB, CPU-only, zero API keys). Store 384-dim vectors as `.npy` alongside archives. On new task, embed the objective and retrieve top-k similar past tasks as prompt context.

**Deliverable:**
- Integrate existing `tools/memory-vector/` (already present, needs activation)
- Batch-embed archive on first run; incrementally embed new tasks on completion
- `memory search "database optimization" --limit 3` CLI or script
- Inject top-3 similar past syntheses into agent prompt for cross-task learning

**Effort:** Medium (~3–4 hrs)  
**Impact:** High — archive becomes queryable institutional memory

**Reference:** `flock/docs/guides/semantic-subscriptions.md`, `agent-blackboard/README.md` (embedding-based knowledge)

---

## P2 — Auto-Paradigm Selection (Phase 2.3)

**Why now:** README defers this to "when task volume exceeds 5/week." The Hybrid paradigm is default because humans manually classify every task. A lightweight router can automate this.

**Pattern:** Use the existing `tools/model-router/` with prefix-based rules or a tiny local classifier (e.g., keyword + sentiment heuristics) to select paradigm automatically from the brief text.

**Deliverable:**
- Activate `tools/model-router/` with Hermes config adaptation
- Router reads Section 1 (Brief) and selects paradigm based on keywords:
  - "aggregate", "benchmark", "state of" → Lightweight
  - "resolve contradiction", "adversarial", "design strategy" → ToM-prompted
  - default → Hybrid
- Write selected paradigm into frontmatter before agents begin
- Human override always available

**Effort:** Medium (~2–3 hrs)  
**Impact:** Medium — reduces manual classification overhead at scale

**Reference:** `README.md` Phase 2.3, existing `tools/model-router/`

---

## P2 — Human-in-the-Loop Escalation Tiers

**Why now:** Some autonomous actions are low-risk (research), others are irreversible (auto-commit to `main`, shell execution on VPS). Today there is no tiered gating.

**Pattern:** Three-tier escalation:
- **Autonomous** — low risk, reversible → agent executes freely
- **Notify** — medium risk, important milestone → execute, then inform human
- **Gate** — high risk, irreversible → stop and wait for human approval

**Deliverable:**
- Add `escalation:` field to task envelope (see P1)
- Telegram or webhook notification on `notify` / `gate` events
- Gate blocking: write `PENDING_APPROVAL` marker in `TASK.md`; human removes it to proceed
- Audit log of all escalated decisions

**Effort:** Medium (~3–4 hrs)  
**Impact:** High — safety guardrail for autonomous systems

**Reference:** `orchestration-playbook/patterns/hitl-escalation.md`

---

## P3 — Persistent Blackboard Store (SQLite Backend)

**Why now:** Git is great for text, but querying history (agent performance, failure rates, cost per task) requires structured storage. Optional enhancement; keep git as the source of truth.

**Pattern:** Mirror every completed task into SQLite with: task ID, agents involved, paradigm, duration, cost, status, failure count, tags. Enables operational dashboards and retrospective analytics.

**Deliverable:**
- `.agent-mesh/history.db` — local SQLite, no network deps
- Schema: `tasks`, `agents`, `sections`, `failures`, `costs`
- CLI query: `blackboard history --since 2026-05-01 --agent vps`
- Optional web dashboard (`ivy-blackboard` pattern) for local viewing

**Effort:** Medium (~4–5 hrs)  
**Impact:** Medium — operational visibility and metrics

**Reference:** `ivy-blackboard/README.md` (SQLite-backed blackboard with dashboard)

---

## Backlog (Future / Unprioritized)

| Idea | Trigger | Source |
|------|---------|--------|
| Agent heartbeat / stale-agent detection | When >3 agents run concurrently | `ivy-blackboard` PID liveness checking |
| Publish/subscribe semantic routing | When archive exceeds 100 tasks | `flock` blackboard auto-chaining |
| Snapshot handoff protocol (AGOR-style) | When switching agents mid-task | `agor/docs/strategies.md` |
| Challenge Loop (adversarial review) | When synthesis quality drops | `orchestration-playbook/patterns/challenge-loop.md` |

---

## How to Move an Item

```bash
# 1. Pick the top open item from the table above
# 2. Create a branch: git checkout -b feat/checkpoint-resume
# 3. Implement, test on Tatooine, push
# 4. Update this file: move item to "Completed" section, date it
# 5. Commit with: git add TODO.md && git commit -m "feat: checkpoint-resume (#N)"
```

## Completed

| Date | Item | Commit |
|------|------|--------|
| 2026-05-02 | Phase 2.1 — Webhook + cron auto-detection | (deployed on VPS) |

---

*Generated: 2026-05-03 from analysis of `orchestration-playbook`, `flock`, `ivy-blackboard`, `agor`, `agent-blackboard`.*
*All referenced repos cloned to `/tmp/agent-mesh-research/` — awaiting cleanup order.*
