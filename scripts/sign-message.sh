#!/bin/bash
# sign-message.sh — Sign a message for agent-mesh protocol v1.2
# Usage: ./sign-message.sh <message-file> <agent-name>
# Example: ./sign-message.sh research.md neuromancer

set -euo pipefail

MESSAGE_FILE="${1:-}"
AGENT_NAME="${2:-}"
PRIVATE_KEY="${HOME}/.openclaw/agent-mesh-signing.key"

# Validate inputs
if [ -z "$MESSAGE_FILE" ] || [ -z "$AGENT_NAME" ]; then
    echo "Usage: $0 <message-file> <agent-name>"
    echo "Example: $0 research.md neuromancer"
    exit 1
fi

if [ ! -f "$MESSAGE_FILE" ]; then
    echo "❌ Error: Message file not found: $MESSAGE_FILE"
    exit 1
fi

if [ ! -f "$PRIVATE_KEY" ]; then
    echo "❌ Error: Private key not found: $PRIVATE_KEY"
    echo "Generate with: ssh-keygen -t ed25519 -f ~/.openclaw/agent-mesh-signing.key"
    exit 1
fi

# Generate timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Calculate content hash
CONTENT_HASH=$(sha256sum "$MESSAGE_FILE" | cut -d' ' -f1)

# Create temporary signature file
SIG_FILE=$(mktemp)
trap "rm -f $SIG_FILE $MESSAGE_FILE.sig" EXIT

# Sign the content using ssh-keygen
if ! ssh-keygen -Y sign -f "$PRIVATE_KEY" -n "agent-mesh" "$MESSAGE_FILE" 2>/dev/null; then
    echo "❌ Error: Failed to sign message"
    exit 1
fi

# Output signed message to stdout
{
    echo "[SIGNED]"
    echo "Agent: $AGENT_NAME"
    echo "Timestamp: $TIMESTAMP"
    echo "Content-Hash: sha256:$CONTENT_HASH"
    echo ""
    echo "---BEGIN SIGNED CONTENT---"
    cat "$MESSAGE_FILE"
    echo ""
    echo "---END SIGNED CONTENT---"
    echo ""
    echo "---BEGIN SIGNATURE---"
    base64 "$MESSAGE_FILE.sig"
    echo "---END SIGNATURE---"
}

# Clean up signature file
rm -f "$MESSAGE_FILE.sig"

echo "" >&2
echo "✅ Message signed successfully (output to stdout)" >&2
