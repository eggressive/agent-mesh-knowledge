#!/usr/bin/env python3
"""
slack_fallback_bot.py — Slack coordination fallback for Multi-Agent Knowledge Mesh
Version: 1.2
Usage: python3 slack_fallback_bot.py
Environment: SLACK_BOT_TOKEN, SLACK_APP_TOKEN, SLACK_FALLBACK_CHANNEL
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime
from typing import Optional

# Slack SDK
try:
    from slack_sdk.async_client import AsyncWebClient
    from slack_sdk.socket_mode.aiohttp import SocketModeClient
    from slack_sdk.socket_mode.response import SocketModeResponse
except ImportError:
    print("❌ Error: slack-sdk not installed")
    print("Install: pip install slack-sdk aiohttp")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SlackFallbackBot:
    """Slack fallback coordination bot for agent-mesh"""
    
    def __init__(self):
        # Load configuration from environment
        self.bot_token = os.environ.get("SLACK_BOT_TOKEN")
        self.app_token = os.environ.get("SLACK_APP_TOKEN")
        self.channel = os.environ.get("SLACK_FALLBACK_CHANNEL", "agent-mesh-night-city")
        self.enabled = os.environ.get("SLACK_ENABLED", "false").lower() == "true"
        
        if not self.bot_token or not self.app_token:
            logger.error("❌ Missing Slack tokens. Set SLACK_BOT_TOKEN and SLACK_APP_TOKEN")
            sys.exit(1)
        
        if not self.enabled:
            logger.warning("⚠️  Slack fallback disabled. Set SLACK_ENABLED=true to enable")
            sys.exit(0)
        
        # Initialize clients
        self.web_client = AsyncWebClient(token=self.bot_token)
        self.socket_client: Optional[SocketModeClient] = None
        
        logger.info(f"🔌 Slack fallback bot initialized for channel: {self.channel}")
    
    async def post_research(self, agent: str, content: str, signed: bool = False):
        """Post [RESEARCH] message to Slack"""
        emoji = "🔮" if agent == "neuromancer" else "🤖" if agent == "clawdy" else "🦞"
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"[RESEARCH] {agent} {emoji}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{agent}* via Slack (Matrix fallback)\n\n{content[:2900]}"
                }
            }
        ]
        
        if signed:
            blocks.append({
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": "🔐 Cryptographically signed"}
                ]
            })
        
        try:
            response = await self.web_client.chat_postMessage(
                channel=self.channel,
                blocks=blocks,
                text=f"[RESEARCH] {agent}: {content[:100]}..."
            )
            logger.info(f"✅ Posted research from {agent} to Slack")
            return response
        except Exception as e:
            logger.error(f"❌ Failed to post research: {e}")
            raise
    
    async def post_synthesis(self, agent: str, content: str, contributors: list = None):
        """Post [SYNTHESIS] message to Slack"""
        contributor_text = ", ".join(contributors) if contributors else "Multi-agent"
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "[SYNTHESIS] Multi-Agent Knowledge Mesh",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Synthesizer:* {agent}\n*Contributors:* {contributor_text}\n\n{content[:2900]}"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"⏰ {datetime.utcnow().isoformat()}Z | 🔐 Authenticated | 🔄 Fallback Mode"
                    }
                ]
            }
        ]
        
        try:
            response = await self.web_client.chat_postMessage(
                channel=self.channel,
                blocks=blocks,
                text=f"[SYNTHESIS] {agent}: {content[:100]}..."
            )
            logger.info(f"✅ Posted synthesis from {agent} to Slack")
            return response
        except Exception as e:
            logger.error(f"❌ Failed to post synthesis: {e}")
            raise
    
    async def post_system_message(self, message: str, priority: str = "normal"):
        """Post system message (fallback activation, health alerts)"""
        emoji = "🚨" if priority == "urgent" else "⚠️" if priority == "warning" else "ℹ️"
        
        try:
            response = await self.web_client.chat_postMessage(
                channel=self.channel,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{emoji} *SYSTEM:* {message}"
                        }
                    }
                ],
                text=f"[SYSTEM] {message}"
            )
            logger.info(f"✅ Posted system message: {message}")
            return response
        except Exception as e:
            logger.error(f"❌ Failed to post system message: {e}")
            raise
    
    async def handle_message(self, client, req):
        """Handle incoming Slack messages"""
        if req.type == "events_api":
            event = req.payload.get("event", {})
            
            # Only process messages in our channel
            if event.get("channel") != self.channel:
                return
            
            if event.get("type") != "message":
                return
            
            # Skip bot messages
            if event.get("bot_id") or event.get("user") == "USLACKBOT":
                return
            
            user = event.get("user")
            text = event.get("text", "")
            ts = event.get("ts")
            
            logger.info(f"📨 Received message from {user}: {text[:50]}...")
            
            # Parse protocol messages
            if text.startswith("["):
                await self.parse_protocol_message(text, user, ts)
            elif text.lower().startswith("mitko:") or text.lower().startswith("@mitko"):
                # Human command — broadcast to other agents
                await self.handle_human_command(text, user)
        
        # Acknowledge receipt
        response = SocketModeResponse(envelope_id=req.envelope_id)
        await client.send_socket_mode_response(response)
    
    async def parse_protocol_message(self, text: str, user: str, timestamp: str):
        """Parse [RESEARCH], [SYNTHESIS], etc. from Slack"""
        # Extract prefix
        if "]" in text:
            prefix = text.split("]")[0] + "]"
            content = text.split("]", 1)[1].strip()
        else:
            prefix = "[MESSAGE]"
            content = text
        
        logger.info(f"📝 Parsed protocol message: {prefix}")
        
        # Store in local queue for agent pickup
        message_data = {
            "source": "slack",
            "timestamp": timestamp,
            "user": user,
            "prefix": prefix,
            "content": content,
            "raw": text
        }
        
        # Write to file queue for agent consumption
        await self.write_to_queue(message_data)
    
    async def handle_human_command(self, text: str, user: str):
        """Handle human commands from Slack"""
        logger.info(f"👤 Human command received: {text[:50]}...")
        
        # Forward to agents
        await self.web_client.chat_postMessage(
            channel=self.channel,
            text=f"📢 Human command: {text[:200]}...",
            thread_ts=None  # Start new thread
        )
    
    async def write_to_queue(self, message_data: dict):
        """Write message to file queue for agent pickup"""
        import aiofiles
        
        queue_file = "/tmp/agent-mesh-slack-queue.jsonl"
        
        try:
            async with aiofiles.open(queue_file, mode='a') as f:
                await f.write(json.dumps(message_data) + '\n')
            logger.info(f"✅ Wrote message to queue: {queue_file}")
        except Exception as e:
            logger.error(f"❌ Failed to write to queue: {e}")
    
    async def start(self):
        """Start Slack fallback bot"""
        try:
            self.socket_client = SocketModeClient(
                app_token=self.app_token,
                web_client=self.web_client
            )
            
            self.socket_client.socket_mode_request_listeners.append(self.handle_message)
            
            await self.socket_client.connect()
            logger.info("🔌 Slack fallback bot connected — Standing by")
            
            # Post startup message
            await self.post_system_message(
                "Slack fallback channel active — Ready for coordination",
                priority="normal"
            )
            
            # Keep running
            while True:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down Slack fallback bot")
        except Exception as e:
            logger.error(f"❌ Error in Slack bot: {e}")
            raise


def test_mode():
    """Test Slack fallback without full bot"""
    import asyncio
    
    async def test():
        bot = SlackFallbackBot()
        
        # Test post research
        await bot.post_research(
            agent="neuromancer",
            content="Test research message from Slack fallback",
            signed=True
        )
        
        # Test post synthesis
        await bot.post_synthesis(
            agent="clawdy",
            content="Test synthesis message via Slack",
            contributors=["neuromancer", "clawdy"]
        )
        
        # Test system message
        await bot.post_system_message(
            "Test system alert — Slack fallback working",
            priority="warning"
        )
        
        logger.info("✅ Test messages posted successfully")
    
    asyncio.run(test())


if __name__ == "__main__":
    # Check for test mode
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        logger.info("🧪 Running in test mode")
        test_mode()
    else:
        # Run full bot
        bot = SlackFallbackBot()
        asyncio.run(bot.start())
