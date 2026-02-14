# model-router

Dynamic model switching based on task classification.

## Installation

```bash
openclaw skill install model-router
```

## Usage

### Automatic Routing (via trigger)
Prefix your message with intent:

| Prefix | Model | Use Case |
|--------|-------|----------|
| `/code` | codex | Programming, debugging, refactoring |
| `/research` | kimi | Long context, web search, analysis |
| `/deep` | opus | Complex reasoning, architecture, security |
| `/fast` | haiku | Quick tasks, summaries, simple Q&A |
| `/cheap` | kimi-free | Cost-sensitive, low priority |

Example:
```
/code Review this Python function for bugs
/research What are the latest developments in LLM agents?
/deep Design a distributed system for real-time event processing
```

### Direct Switching
```
/model codex    # Switch to Codex
/model kimi     # Switch to Kimi K2.5
/model opus     # Switch to Opus
/model haiku    # Switch to Haiku
```

### Sub-agent Spawning (Isolated Context)
For complex multi-model workflows:

```javascript
// From any session
sessions_spawn({
  task: "Analyze this codebase for security issues",
  model: "opus",
  thinking: "high"
})
```

## Configuration

Edit `~/.openclaw/skills/model-router/config.json`:

```json
{
  "default": "kimi",
  "autoRoute": true,
  "routes": {
    "code": {
      "model": "codex",
      "patterns": ["code", "function", "bug", "refactor", "implement"],
      "threshold": 0.7
    },
    "research": {
      "model": "kimi",
      "patterns": ["research", "find", "search", "latest", "what is"],
      "threshold": 0.6
    },
    "complex": {
      "model": "opus",
      "patterns": ["design", "architecture", "analyze", "security audit"],
      "threshold": 0.8
    }
  },
  "costLimits": {
    "dailyOpusTokens": 100000,
    "alertThreshold": 0.8
  }
}
```

## How It Works

1. **Intent Detection**: Simple keyword/pattern matching on user input
2. **Cost Awareness**: Tracks daily spend per model, suggests cheaper alternatives when approaching limits
3. **Context Preservation**: Main session switches model; sub-agents get isolated context with specific model
4. **Fallback Chain**: If model unavailable → fallback to next best option

## Architecture

```
User Input
    ↓
Intent Classifier (keyword-based, lightweight)
    ↓
    ├─→ Code detected → Spawn Codex agent OR switch to Codex
    ├─→ Research detected → Switch to Kimi (long context)
    ├─→ Complex detected → Switch to Opus (reasoning)
    └─→ Default → Stay on current model
    ↓
Cost Check (if high-cost model requested)
    ↓
Execute with selected model
```

## Advanced: Multi-Agent Workflows

```javascript
// Parallel execution with different models
const results = await Promise.all([
  sessions_spawn({ task: "Code review", model: "codex" }),
  sessions_spawn({ task: "Security check", model: "opus" }),
  sessions_spawn({ task: "Documentation", model: "kimi" })
]);
```

## Why Not Auto-Detect Everything?

Explicit routing > magic:
- **Predictable costs** — you know which model runs
- **Consistent behavior** — no surprise switches mid-conversation  
- **User control** — override anytime with `/model`
- **Simple** — no LLM-based classification overhead

## Future Ideas

- [ ] Usage analytics dashboard (`/router stats`)
- [ ] Smart fallback when rate-limited
- [ ] "Best of 3" ensemble (run task on 3 models, vote on best)
- [ ] Automatic escalation (cheap model fails → retry with better model)
