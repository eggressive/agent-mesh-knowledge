#!/bin/bash
# agent-heartbeat.sh — Send an agent heartbeat to the shared blackboard
# 
# Usage: ./agent-heartbeat.sh <session-id> [--message "progress note"]
#
# Each running agent calls this periodically to signal liveness.
# The sweep/stale-agent detector checks for heartbeats that haven't
# been updated beyond the STALE_THRESHOLD.
#
# Integration: Call from cron or wrap your agent launch script:
#   while true; do
#     sleep 300  # 5-minute heartbeat interval
#     ./agent-heartbeat.sh "$HERMES_SESSION_ID" --message "working on section 3"
#   done &
#   heartbeat_pid=$!
#   ... run agent task ...
#   kill $heartbeat_pid 2>/dev/null
#   ./agent-heartbeat.sh "$HERMES_SESSION_ID" --message "completed"

set -e

REPO_DIR="${HOME}/agent-mesh-knowledge"
HEARTBEAT_DIR="${REPO_DIR}/status/heartbeats"
STALE_THRESHOLD=900  # 15 minutes in seconds
SESSION_ID="${1:-unknown}"
MESSAGE="${2:-alive}"

# Parse optional --message flag
if [ "$1" = "--message" ] || [ "$2" = "--message" ]; then
  shift 2 2>/dev/null || true
  MESSAGE="${1:-alive}"
  SESSION_ID="${SESSION_ID:-unknown}"
fi

mkdir -p "$HEARTBEAT_DIR"

# Write heartbeat: timestamp + optional message
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "{\"session_id\":\"${SESSION_ID}\",\"timestamp\":\"${TIMESTAMP}\",\"message\":\"${MESSAGE}\"}" \
  > "${HEARTBEAT_DIR}/${SESSION_ID}.json"

echo "[heartbeat] ${SESSION_ID} — ${MESSAGE} @ ${TIMESTAMP}"

# Also record in git for cross-agent visibility
cd "$REPO_DIR"
git add "status/heartbeats/${SESSION_ID}.json" 2>/dev/null || true
git commit -m "heartbeat: ${SESSION_ID} — ${MESSAGE}" --no-gpg-sign 2>/dev/null || true
git push 2>/dev/null || echo "[heartbeat] push skipped (no remote or offline)"