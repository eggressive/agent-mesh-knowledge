#!/bin/bash
# test-slack-fallback.sh — Test Slack fallback coordination
# Usage: ./test-slack-fallback.sh

set -euo pipefail

echo "🧪 Testing Slack Fallback for Multi-Agent Knowledge Mesh"
echo "=========================================================="
echo ""

# Check environment
if [ -z "${SLACK_BOT_TOKEN:-}" ]; then
    echo "❌ Error: SLACK_BOT_TOKEN not set"
    echo "Set it with: export SLACK_BOT_TOKEN='xoxb-your-token'"
    exit 1
fi

if [ -z "${SLACK_APP_TOKEN:-}" ]; then
    echo "❌ Error: SLACK_APP_TOKEN not set"
    echo "Set it with: export SLACK_APP_TOKEN='xapp-your-token'"
    exit 1
fi

# Check Python dependencies
echo "1️⃣  Checking Python dependencies..."
python3 -c "import slack_sdk" 2>/dev/null || {
    echo "Installing slack-sdk..."
    pip install slack-sdk aiohttp
}
echo "   ✅ Dependencies OK"
echo ""

# Test posting messages
echo "2️⃣  Testing message posting..."
cd "$(dirname "$0")"
python3 slack_fallback_bot.py --test
echo "   ✅ Messages posted"
echo ""

# Check queue file
echo "3️⃣  Checking message queue..."
if [ -f /tmp/agent-mesh-slack-queue.jsonl ]; then
    echo "   ✅ Queue file exists: /tmp/agent-mesh-slack-queue.jsonl"
    echo "   📄 Contents:"
    tail -3 /tmp/agent-mesh-slack-queue.jsonl | while read line; do
        echo "      $line"
    done
else
    echo "   ⚠️  Queue file not created yet (normal for test mode)"
fi
echo ""

echo "✅ Slack fallback test complete!"
echo ""
echo "Next steps:"
echo "1. Verify messages appeared in Slack #agent-mesh-night-city"
echo "2. Start full bot: python3 slack_fallback_bot.py"
echo "3. Test coordination between agents"
echo ""
echo "To run full bot:"
echo "   export SLACK_ENABLED=true"
echo "   python3 slack_fallback_bot.py"
