#!/bin/bash
# verify-message.sh — Verify a signed agent-mesh message v1.2
# Usage: ./verify-message.sh <signed-message-file> [agents-yaml-path]
# Example: ./verify-message.sh signed-message.txt

set -euo pipefail

SIGNED_FILE="${1:-}"
AGENTS_YAML="${2:-./agents/agents.yaml}"

# Validate inputs
if [ -z "$SIGNED_FILE" ]; then
    echo "Usage: $0 <signed-message-file> [agents-yaml-path]"
    echo "Example: $0 signed-message.txt"
    exit 1
fi

if [ ! -f "$SIGNED_FILE" ]; then
    echo "❌ Error: Signed message file not found: $SIGNED_FILE"
    exit 1
fi

if [ ! -f "$AGENTS_YAML" ]; then
    echo "❌ Error: agents.yaml not found: $AGENTS_YAML"
    exit 1
fi

# Check for yq (YAML parser)
if ! command -v yq &> /dev/null; then
    echo "❌ Error: yq not found. Install with:"
    echo "   wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/local/bin/yq && chmod +x /usr/local/bin/yq"
    exit 1
fi

# Extract agent name from signed message
AGENT=$(grep "^Agent:" "$SIGNED_FILE" | head -1 | cut -d' ' -f2- || echo "")
if [ -z "$AGENT" ]; then
    echo "❌ Error: Could not extract Agent from signed message"
    exit 1
fi

# Extract timestamp
TIMESTAMP=$(grep "^Timestamp:" "$SIGNED_FILE" | head -1 | cut -d' ' -f2- || echo "")
if [ -z "$TIMESTAMP" ]; then
    echo "❌ Error: Could not extract Timestamp from signed message"
    exit 1
fi

# Check timestamp freshness (reject messages >5 minutes old)
MESSAGE_TIME=$(date -d "$TIMESTAMP" +%s 2>/dev/null || echo "0")
CURRENT_TIME=$(date -u +%s)
TIME_DIFF=$((CURRENT_TIME - MESSAGE_TIME))

if [ $TIME_DIFF -gt 300 ]; then
    echo "⚠️  Warning: Message is >5 minutes old ($TIME_DIFF seconds)"
    echo "   Verify manually or reject if suspicious"
fi

# Extract public key from agents.yaml
PUBKEY=$(yq ".agents.${AGENT}.authentication.public_key" "$AGENTS_YAML" 2>/dev/null || echo "null")

if [ "$PUBKEY" = "null" ] || [ -z "$PUBKEY" ]; then
    echo "❌ Error: No public key found for agent '$AGENT' in $AGENTS_YAML"
    exit 1
fi

# Create temp files
PUBKEY_FILE=$(mktemp)
CONTENT_FILE=$(mktemp)
SIG_FILE=$(mktemp)
trap "rm -f $PUBKEY_FILE $CONTENT_FILE $SIG_FILE" EXIT

# Save public key
echo "$PUBKEY" > "$PUBKEY_FILE"

# Extract signed content block
sed -n '/---BEGIN SIGNED CONTENT---/,/---END SIGNED CONTENT---/p' "$SIGNED_FILE" | \
    sed '1d;$d' > "$CONTENT_FILE"

# Extract signature
sed -n '/---BEGIN SIGNATURE---/,/---END SIGNATURE---/p' "$SIGNED_FILE" | \
    sed '1d;$d' | base64 -d > "$SIG_FILE"

# Verify signature
if ssh-keygen -Y verify -f "$PUBKEY_FILE" -n "agent-mesh" \
    -s "$SIG_FILE" "$CONTENT_FILE" 2>/dev/null; then
    echo "✅ Signature VALID — Message from $AGENT authenticated"
    echo "   Timestamp: $TIMESTAMP"
    echo "   Content hash verified"
    exit 0
else
    echo "❌ Signature INVALID — Possible impersonation!"
    echo "   Agent: $AGENT"
    echo "   DO NOT TRUST THIS MESSAGE"
    exit 1
fi
