---
status: open
question: |-
  How should Agent-Mesh Phase 2 extend the blackboard beyond git?
agents: [tatooine, vps]
started: 2026-05-02 15:30 UTC
---

## 0. Paradigm Selection

> [!important] Check one before research begins.
> Human or seed agent classifies the task. Agents adjust depth accordingly.

- [ ] **Lightweight (Han & Zhang)** — factual research, aggregation, verification
- [ ] **ToM-prompted (Riedl)** — creative tasks, adversarial analysis, conflict resolution
- [x] **Hybrid (default)** — most real tasks
  - Blackboard structure (shared memory, control unit) + mandatory ToM in cross-pollination (section 4)
  - Only pays the deep modeling cost when the task requires it

**Classified by:** Mitko
**Rationale:** Requires factual research (what exists) + creative design (what to build) — neither pure aggregation nor pure adversarial reasoning.

## 1. Brief

Phase 1 proved the blackboard works with git as the shared substrate. Phase 2 asks: what comes next?

Design constraints:
- Must stay simple — no message brokers, no new infrastructure services
- Must leverage what's already running on the VPS (webhook server at :8645, n8n, cron)
- Must work with Tatooine behind NAT (no inbound connections)
- Must be measurable — can we detect when the blackboard is "stale" and auto-trigger?

## 2. Research: Tatooine

**Capabilities used:** Obsidian vault (current architecture reference, Phase 1 plan, DDNS skill), Ollama models, local code analysis, session memory

**Findings**

- [x] **What's already proven on this infrastructure (precedent):**
  - The VPS already runs a Flask webhook server on port 8645 handling No-IP renewal triggered by n8n (Gmail → extract URL → POST to :8645 → Selenium → renew). This pattern (HTTP webhook + script execution) is battle-tested.
  - n8n runs on the VPS with Gmail OAuth2 trigger capability, meaning the VPS can *detect* external events (email, webhooks) and cascade into actions.
  - Hermes Agent on VPS has cron capability — scheduled agent runs for periodic tasks. The No-IP renewal cron (`0 3 */25 * *`) already demonstrates cron-to-agent pipeline.
  - Source: [[ddns-hostname-renewal-automation]] skill, `ssh root@100.117.221.84 crontab -l`

- [x] **Architectural constraints (Tatooine → VPS communication):**
  - Tatooine is behind home NAT — no public IP, no inbound webhooks possible here.
  - VPS has a public IP (100.117.221.84) accessible via Tailscale, but Tailscale is point-to-point, not externally routable from GitHub.
  - This means: **Tatooine pushes to GitHub. VPS polls GitHub.** Push-based triggering (GitHub webhook → VPS) won't work because GitHub can't reach VPS's Tailscale address. Pull-based (VPS cron polls) is the correct pattern.
  - Source: [[Current-Architecture-Reference]] topology, verified via `tailscale status`

- [x] **Three-layer design (user's proposal):**
  The user decomposed Phase 2 into incremental layers based on complexity and need:

  | Layer | What | Time | Trigger |
  |---|---|---|---|
  | 1 | `/blackboard/pull` webhook endpoint + cron fallback | < 10 min | Now — unblocks immediate auto-response |
  | 2 | Activate `memory-vector` for archived task search | ~15 min | When grep on archive/ becomes painful |
  | 3 | Activate `model-router` for auto-paradigm selection | > 30 min | When task volume exceeds 5/week |

  This layered approach is correct: each layer adds capability without breaking the previous one. It avoids the trap of designing a comprehensive system upfront.

- [x] **Layer 1 design — webhook endpoint pattern:**
  - Add `/blackboard/pull` POST endpoint to the existing Flask server at `:8645`
  - Endpoint behavior: `git pull` in `~/agent-mesh-knowledge`, scan `blackboard/TASK.md`, return `{vps_action_needed: true/false, task_status: ...}`
  - Add `/blackboard/status` GET for health monitoring
  - Cron fallback: `*/5 * * * * /opt/scripts/blackboard_poll.sh` — curl localhost endpoint, if `vps_action_needed=true`, spawn `hermes -z "write section 3"`

- [x] **Why Layer 1 matters beyond just speeding up Phase 1:**
  - Phase 1 required manual orchestration: human (or agent on Tatooine) had to remember to `git push`, then manually trigger VPS. This creates coordination debt.
  - With auto-detection: push → cron detects → VPS auto-responds. The blackboard becomes event-driven without external webhooks.
  - This is the minimal change that turns the blackboard from a *passive document* into an *active coordination surface*.

- [x] **Precautions (learned from No-IP webhook):**
  - The webhook server runs as `root` — same caveats as Phase 1 git commits (acceptable for now)
  - Detection heuristic must distinguish "section has actual content" from "section is still template". `[x]` count + keyword presence (`p=`, `Source:`) is the heuristic used.
  - Idempotency: if cron runs twice before VPS finishes writing, the second run should detect section 3 already exists → no-op. The `already up to date` git output handles this.

**Confidence:** High — based on verified infrastructure (not speculation). The No-IP renewal webhook is the proven template.
