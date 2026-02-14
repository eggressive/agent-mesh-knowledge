#!/bin/bash
# Thin wrapper around Python implementation
# Usage: ./scripts/verify-message.sh <message.md> <agent_name>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/verify_message.py" "$@"
