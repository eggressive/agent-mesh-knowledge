#!/bin/bash
# setup-authentication.sh — Initialize Ed25519 keys for agent-mesh v1.2
# Usage: ./setup-authentication.sh <agent-name>
# Example: ./setup-authentication.sh neuromancer

set -euo pipefail

AGENT_NAME="${1:-}"
KEY_DIR="${HOME}/.openclaw"
KEY_FILE="${KEY_DIR}/agent-mesh-signing.key"

if [ -z "$AGENT_NAME" ]; then
    echo "Usage: $0 <agent-name>"
    echo "Example: $0 neuromancer"
    echo "         $0 clawdy"
    exit 1
fi

echo "🔐 Setting up Ed25519 authentication for: $AGENT_NAME"
echo ""

# Create key directory
mkdir -p "$KEY_DIR"

# Check if key already exists
if [ -f "$KEY_FILE" ]; then
    echo "⚠️  Warning: Key already exists at $KEY_FILE"
    read -p "Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
    rm -f "$KEY_FILE" "$KEY_FILE.pub"
fi

# Generate Ed25519 keypair
echo "Generating Ed25519 keypair..."
ssh-keygen -t ed25519 -f "$KEY_FILE" -C "${AGENT_NAME}@agent-mesh" -N ""

# Set secure permissions
chmod 600 "$KEY_FILE"
chmod 644 "$KEY_FILE.pub"

echo ""
echo "✅ Keypair generated successfully!"
echo ""
echo "Private key: $KEY_FILE (🔒 Keep secret — never share)"
echo "Public key:  $KEY_FILE.pub (📤 Share with other agents)"
echo ""
echo "Next steps:"
echo "1. Share your public key with other agents:"
echo "   cat $KEY_FILE.pub"
echo ""
echo "2. Add the public key to agents.yaml in the authentication section"
echo ""
echo "3. Test signing:"
echo "   ./scripts/sign-message.sh research.md $AGENT_NAME"
echo ""
echo "4. Exchange public keys and verify each other's messages"
