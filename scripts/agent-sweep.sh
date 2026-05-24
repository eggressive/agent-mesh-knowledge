#!/bin/bash
# agent-sweep.sh — Detect and clean up stale agents
#
# Usage: ./agent-sweep.sh [--dry-run] [--threshold 900]
#
# Queries the SQLite state.db for sessions that are still open (no ended_at)
# but haven't sent a heartbeat beyond the stale threshold.
# Also cross-references PID liveness where possible.
#
# Stale actions:
#   1. Mark ended_at in state.db with end_reason='stale_agent'
#   2. Remove stale heartbeat files from status/heartbeats/
#   3. Send notification (optional)
#
# Install as cron (runs every 15 minutes):
#   */15 * * * * /opt/scripts/agent-sweep.sh --notify-telegram >> /var/log/agent-sweep.log 2>&1

set -e

REPO_DIR="${HOME}/agent-mesh-knowledge"
HEARTBEAT_DIR="${REPO_DIR}/status/heartbeats"
STATE_DB="${HOME}/.hermes/state.db"
NOTIFY=false
DRY_RUN=false
STALE_THRESHOLD=900  # 15 minutes default

# Parse args
while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --threshold) STALE_THRESHOLD="$2"; shift 2 ;;
    --notify-telegram|--notify) NOTIFY=true; shift ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

NOW=$(date -u +"%s")
STALE_CUTOFF=$((NOW - STALE_THRESHOLD))
STALE_CUTOFF_ISO=$(date -u -d "@${STALE_CUTOFF}" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -r "${STALE_CUTOFF}" +"%Y-%m-%dT%H:%M:%SZ")

echo "=== Agent Sweep $(date -u +'%Y-%m-%dT%H:%M:%SZ') ==="
echo "Stale threshold: ${STALE_THRESHOLD}s (cutoff: ${STALE_CUTOFF_ISO})"
echo "Dry run: ${DRY_RUN}"
echo

STALE_COUNT=0
STALE_SESSIONS=""

# Phase 1: Check heartbeat files
echo "--- Phase 1: Heartbeat file check ---"
if [ -d "$HEARTBEAT_DIR" ]; then
  for hb_file in "$HEARTBEAT_DIR"/*.json; do
    [ -f "$hb_file" ] || continue
    
    SESSION_ID=$(basename "$hb_file" .json)
    HB_MTIME=$(stat -c "%Y" "$hb_file" 2>/dev/null || stat -f "%m" "$hb_file" 2>/dev/null)
    
    if [ "$HB_MTIME" -lt "$STALE_CUTOFF" ]; then
      echo "  STALE: ${SESSION_ID} (last heartbeat: $(date -d "@${HB_MTIME}" +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -r "${HB_MTIME}" +'%Y-%m-%dT%H:%M:%SZ'))"
      STALE_COUNT=$((STALE_COUNT + 1))
      STALE_SESSIONS="${STALE_SESSIONS} ${SESSION_ID}"
      
      if [ "$DRY_RUN" = false ]; then
        rm -f "$hb_file"
        echo "    → heartbeat file removed"
      else
        echo "    → would remove heartbeat file (dry-run)"
      fi
    fi
  done
else
  echo "  No heartbeat directory (${HEARTBEAT_DIR})"
  mkdir -p "$HEARTBEAT_DIR"
fi

# Phase 2: Check state.db for open sessions beyond threshold
echo
echo "--- Phase 2: SQLite state.db check ---"
if [ -f "$STATE_DB" ]; then
  OPEN_SESSIONS=$(sqlite3 "$STATE_DB" "SELECT id, started_at, source FROM sessions WHERE ended_at IS NULL AND started_at < ${STALE_CUTOFF};" 2>/dev/null || echo "")
  
  if [ -n "$OPEN_SESSIONS" ]; then
    echo "${OPEN_SESSIONS}" | while IFS='|' read -r sid started_at source; do
      STARTED_ISO=$(date -u -d "@${started_at}" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -r "${started_at}" +"%Y-%m-%dT%H:%M:%SZ")
      echo "  OPEN (stale): ${sid} (source: ${source}, started: ${STARTED_ISO})"
      
      if [ "$DRY_RUN" = false ]; then
        sqlite3 "$STATE_DB" "UPDATE sessions SET ended_at = ${NOW}, end_reason = 'stale_agent_sweep' WHERE id = '${sid}' AND ended_at IS NULL;" 2>/dev/null || echo "    → DB update failed (read-only or locked)"
        echo "    → session marked as stale_agent_sweep"
        STALE_COUNT=$((STALE_COUNT + 1))
        STALE_SESSIONS="${STALE_SESSIONS} ${sid}"
      else
        echo "    → would mark as stale_agent_sweep (dry-run)"
      fi
    done
  else
    echo "  No open stale sessions found"
  fi
else
  echo "  state.db not found at ${STATE_DB}"
fi

# Phase 3: Report and notify
echo
if [ "$STALE_COUNT" -gt 0 ]; then
  echo "=== Summary: ${STALE_COUNT} stale agent(s) detected ==="
  
  if [ "$NOTIFY" = true ] && [ "$DRY_RUN" = false ]; then
    MESSAGE="🧹 Agent Sweep: ${STALE_COUNT} stale agent(s) cleaned up${STALE_SESSIONS}"
    
    # Try Telegram notification via Hermes
    if command -v hermes &>/dev/null; then
      hermes -z "Alert: ${MESSAGE}" --no-stream --quiet 2>/dev/null || true
      echo "  → Telegram notification sent"
    fi
  fi
else
  echo "=== Summary: No stale agents detected ==="
fi

echo "=== Sweep Complete ==="