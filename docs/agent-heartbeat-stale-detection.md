# Agent Heartbeat & Stale-Agent Detection

**Status:** ✅ IMPLEMENTED  
**Date:** 2026-05-24  
**Pattern Source:** `ivy-blackboard` PID liveness checking  
**Priority:** Backlog (was P3)

---

## Problem

When multiple agents run concurrently — especially on the VPS behind Tailscale where sessions are ephemeral (cron timeouts, network drops, context exhaustion) — there's no way to detect:

1. **Which agents are actively working** vs. crashed/hung
2. **Stale agent sessions** that claimed work but never completed
3. **Resource leaks** from abandoned sessions (half-written files, dangling claims)

The problem surfaces because:
- Hermes cron jobs run with `max_iterations` and timeouts — if an agent exceeds these, the session dies silently
- Delegate_task spawns child agents; if the parent finishes but children are still running, sessions orphan
- No cross-session visibility into who's alive

---

## Design

### Two-Component Architecture

| Component | Role | Runs On | Frequency |
|-----------|------|---------|-----------|
| **`agent-heartbeat.sh`** | Agent sends periodic liveness signal | Per-agent (inside cron task) | Every 5 min during active work |
| **`agent-sweep.sh`** | Detects and cleans up stale agents | VPS cron | Every 15 min |

### No New Infrastructure

Both components use existing resources:
- **Filesystem:** `status/heartbeats/` directory in `agent-mesh-knowledge` repo
- **Git:** Heartbeat commits provide cross-agent visibility (agents on Tatooine can see VPS heartbeats via git pull)
- **SQLite:** `state.db` sessions table — `ended_at IS NULL` + old `started_at` = stale candidate
- **Cron:** Existing VPS cron infrastructure runs the sweep

---

## Usage

### Send a Heartbeat

```bash
# Simple
./scripts/agent-heartbeat.sh "session-abc-123"

# With progress message
./scripts/agent-heartbeat.sh "session-abc-123" --message "researching section 2"

# From within a cron job — wrap your agent task:
heartbeat_pid=""
cleanup() { kill $heartbeat_pid 2>/dev/null; ./scripts/agent-heartbeat.sh "$HERMES_SESSION_ID" --message "completed/failed"; }
trap cleanup EXIT

# Start background heartbeat loop
while true; do
    sleep 300
    ./scripts/agent-heartbeat.sh "$HERMES_SESSION_ID" --message "working..."
done &
heartbeat_pid=$!
```

### Run a Sweep

```bash
# Dry run (shows what would be cleaned)
./scripts/agent-sweep.sh --dry-run

# Actual sweep with 15-minute stale threshold (default)
./scripts/agent-sweep.sh

# Custom threshold (e.g., 5 minutes for aggressive cleanup)
./scripts/agent-sweep.sh --threshold 300

# With Telegram notification
./scripts/agent-sweep.sh --notify-telegram
```

### Cron Installation (VPS)

Add to crontab (`crontab -e`):

```cron
# Agent heartbeat sweep — every 15 minutes
*/15 * * * * /opt/scripts/agent-sweep.sh --notify-telegram >> /var/log/agent-sweep.log 2>&1
```

---

## Implementation Details

### Heartbeat File Format

Each heartbeat is a JSON file at `status/heartbeats/{session-id}.json`:

```json
{
  "session_id": "cron_61189ba18029_20260524_091512",
  "timestamp": "2026-05-24T09:20:00Z",
  "message": "researching section 3"
}
```

Files are committed to git on each beat for cross-agent visibility.

### Stale Detection Logic

1. **Heartbeat file check:** Compare file mtime vs. current time. If mtime > `STALE_THRESHOLD` seconds ago → stale.
2. **SQLite session check:** Query `sessions WHERE ended_at IS NULL AND started_at < cutoff`. Sessions without recent heartbeats AND open in DB are stale.
3. **Cleanup actions:**
   - Remove heartbeat file
   - Set `ended_at = now`, `end_reason = 'stale_agent_sweep'` in state.db
   - Send Telegram notification (optional)

### Integration with Existing Patterns

| Existing Pattern | Heartbeat Integration |
|-----------------|----------------------|
| **Blackboard TASK.md** | Sweep can detect if VPS has been working on a section but went stale → re-queue |
| **Circuit Breaker (TODO P0)** | Stale agents from failed providers can be cleaned up without manual intervention |
| **Dead Letter Queue (TODO P0)** | Sweep can check if DLQ items have stale agents that were processing them |
| **Checkpoint/Resume (TODO P0)** | Stale checkpoint = sweep-and-resume signal |
| **Task Envelope (TODO P1)** | `stop_on: ["stale_agent"]` condition |

---

## Future Enhancements

1. **Agent liveness dashboard:** Web endpoint at `:8645/agents/status` showing heartbeat timestamps
2. **PID-level liveness:** Cross-reference heartbeat session IDs with actual running processes on VPS
3. **Auto-resume:** If a stale agent was working on a TASK.md section, auto-reassign to next available agent
4. **Heartbeat expiry chain:** If sweep runs 3 times with same stale agent → escalate to Telegram alert

---

**Related files:**
- `scripts/agent-heartbeat.sh` — Heartbeat sender
- `scripts/agent-sweep.sh` — Stale agent detector/cleanup
- `status/heartbeats/` — Live heartbeat files
- `TODO.md` — Task #8 entry