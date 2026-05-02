#!/bin/bash
# Blackboard push helper — commit, push, notify VPS
# Usage: ./push_and_notify.sh "commit message"
# Run from ~/agent-mesh-knowledge

set -e

REPO_DIR="$HOME/agent-mesh-knowledge"
VPS_WEBHOOK="http://100.117.221.84:8645/blackboard/pull"
MSG="${1:-blackboard update}"

cd "$REPO_DIR"

# Commit and push
git add -A
git commit -m "$MSG" || { echo "Nothing to commit"; exit 0; }
git push

echo "Pushed. Notifying VPS..."
curl -s -X POST "$VPS_WEBHOOK" | python3 -m json.tool

echo "Done."
