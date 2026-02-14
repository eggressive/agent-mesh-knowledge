#!/bin/bash
# test-slack-api.sh — Test Slack API with curl (no Python needed)
# Usage: ./test-slack-api.sh

set -euo pipefail

BOT_TOKEN="${SLACK_BOT_TOKEN:-}"
CHANNEL="${SLACK_FALLBACK_CHANNEL:-agent-mesh-night-city}"

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ Error: SLACK_BOT_TOKEN not set"
    exit 1
fi

echo "🧪 Testing Slack API connection..."
echo "=========================================================="
echo ""

# Test 1: Auth test
echo "1️⃣  Testing authentication..."
AUTH_RESPONSE=$(curl -s -X POST \
    -H "Authorization: Bearer $BOT_TOKEN" \
    -H "Content-type: application/json" \
    https://slack.com/api/auth.test)

if echo "$AUTH_RESPONSE" | grep -q '"ok":true'; then
    echo "   ✅ Authentication successful"
    echo "   Bot: $(echo "$AUTH_RESPONSE" | grep -o '"user":"[^"]*"' | cut -d'"' -f4)"
    echo "   Team: $(echo "$AUTH_RESPONSE" | grep -o '"team":"[^"]*"' | cut -d'"' -f4)"
else
    echo "   ❌ Authentication failed"
    echo "   Response: $AUTH_RESPONSE"
    exit 1
fi
echo ""

# Test 2: Post message
echo "2️⃣  Posting test message to #$CHANNEL..."
MESSAGE_RESPONSE=$(curl -s -X POST \
    -H "Authorization: Bearer $BOT_TOKEN" \
    -H "Content-type: application/json" \
    --data "{\"channel\":\"#$CHANNEL\",\"text\":\"🧪 Test from Agent Mesh — 3-agent coordination activated!\",\"blocks\":[{\"type\":\"header\",\"text\":{\"type\":\"plain_text\",\"text\":\"[SYSTEM] Agent Mesh Test\"}},{\"type\":\"section\",\"text\":{\"type\":\"mrkdwn\",\"text\":\"*3-agent coordination activated:*\\n🔮 Neuromancer (VPS)\\n🤖 Clawdy (Tatooine)\\n🦞 Moltdude (VPS)\\n\\n✅ Ready for Slack fallback coordination.\"}}]}" \
    https://slack.com/api/chat.postMessage)

if echo "$MESSAGE_RESPONSE" | grep -q '"ok":true'; then
    echo "   ✅ Message posted successfully"
    TS=$(echo "$MESSAGE_RESPONSE" | grep -o '"ts":"[^"]*"' | head -1 | cut -d'"' -f4)
    echo "   Timestamp: $TS"
else
    echo "   ❌ Failed to post message"
    echo "   Response: $MESSAGE_RESPONSE"
    exit 1
fi
echo ""

# Test 3: List channels
echo "3️⃣  Checking channel access..."
CHANNELS_RESPONSE=$(curl -s -X POST \
    -H "Authorization: Bearer $BOT_TOKEN" \
    https://slack.com/api/conversations.list)

if echo "$CHANNELS_RESPONSE" | grep -q "$CHANNEL"; then
    echo "   ✅ Channel #$CHANNEL accessible"
else
    echo "   ⚠️  Channel #$CHANNEL may not exist or bot not invited"
    echo "   Create the channel and invite @AgentMesh bot"
fi
echo ""

echo "✅ All tests complete!"
echo ""
echo "3-agent Slack coordination is operational."
echo "Agents: Neuromancer 🔮, Clawdy 🤖, Moltdude 🦞"
