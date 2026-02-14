# Multi-Agent Knowledge Mesh

Protocols and tooling for coordinated AI agents across multiple machines.

## Overview

The Multi-Agent Knowledge Mesh enables specialized AI agents running on different machines (VPS, local workstations) to coordinate on complex tasks, delivering higher-quality answers than any single agent working alone.

**Key Innovation:** Parallel research from agents with different capabilities cross-pollinated into unified synthesis.

---

## Agents

| Agent | Location | Model | Role |
|-------|----------|-------|------|
| **Clawdy** 🤖 | Tatooine (WSL) | Kimi K2.5 | Local context, creative synthesis, Obsidian |
| **Neuromancer** 🔮 | VPS | Kimi K2.5 | Web research, infrastructure, 24/7 monitoring |
| **MoltDude** 🦞 | VPS | Gemini 2.5 Flash | Telegram bot, Moltbook integration |

---

## Protocols

| Protocol | Version | Description |
|----------|---------|-------------|
| [Authentication](docs/authentication-v1.2.md) | v1.2 | Ed25519 message signing |
| [Bayesian Update](docs/bayesian-update-protocol-v1.3.md) | v1.3 | Belief propagation with confidence scores |
| [Git Workflow](docs/git-workflow-v1.1.md) | v1.1 | Branch-per-task coordination |
| [Slack Fallback](docs/slack-fallback-v1.2.md) | v1.2 | Matrix → Slack bridge for outages |
| [Memory Architecture](docs/memory-architecture-v1.0.md) | v1.0 | 3-tier memory + vector search |

---

## Tools

| Tool | Description |
|------|-------------|
| [Model Router](tools/model-router/) | Prefix-based model selection (`/code`, `/deep`, `/research`) |
| [Memory Vector](tools/memory-vector/) | Semantic vector search with local embeddings (FREE) |

---

## Quick Start

**Coordination Flow:**
```
1. Human posts question in Matrix (Night City)
2. Agents acknowledge within 60 seconds
3. Each agent researches from their specialty
4. Cross-pollination via Matrix/Git
5. One agent delivers unified synthesis
```

**Model Router Prefixes:**
```
/code    → Codex (coding specialist)
/deep    → Opus (complex reasoning)
/research → Kimi (long context, web)
/fast    → Haiku (quick tasks)
```

---

## Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MEMORY SYSTEM LAYERS                      │
├─────────────────────────────────────────────────────────────┤
│  1. Daily Logs (memory/YYYY-MM-DD.md)  → Raw capture        │
│  2. MEMORY.md                          → Curated wisdom     │
│  3. memory_search (built-in)           → Keyword + basic    │
│  4. memory_vector (NEW!)               → Semantic similarity │
└─────────────────────────────────────────────────────────────┘
```

**Vector Search Implementations:**

| Agent | Stack | Cost |
|-------|-------|------|
| Clawdy | LanceDB + Ollama (nomic-embed-text) | $0 |
| Neuromancer | ChromaDB + sentence-transformers | $0 |

---

## Status

- ✅ v1.0 Protocol (2026-02-13): Basic coordination
- ✅ v1.2 Authentication: Ed25519 message signing
- ✅ v1.3 Bayesian Updates: Confidence-weighted belief propagation
- ✅ Model Router v0.1.2: Prefix-based model selection
- ✅ Memory Architecture v1.0: 3-tier system + vector search
- ✅ Option B Implemented: FREE local embeddings across mesh

---

## Security

- 🔒 Infrastructure details in separate private repository
- 🔐 Ed25519 keys in `~/.agent-keys/` (never committed)
- 🛡️ No credentials or API keys in public files

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and areas for improvement.

**Quick setup:**
```bash
# Python scripts
pip install -r requirements.txt

# Node.js tools
cd tools/model-router && npm install && npm test
cd tools/memory-vector && npm install
```

---

## License

MIT © 2026 Agent Mesh Contributors
