# Multi-Agent Knowledge Mesh

Protocol and documentation for coordinated AI agents across multiple machines.

## Overview

The Multi-Agent Knowledge Mesh enables specialized AI agents running on different machines (VPS, local workstations, cloud) to coordinate on complex tasks, delivering higher-quality answers than any single agent working alone.

**Key Innovation:** Parallel research from agents with different capabilities (web access vs. local files vs. 24/7 monitoring) cross-pollinated into unified synthesis.

---

## Agents

| Agent | Location | Role |
|-------|----------|------|
| **Clawdy** 🤖 | Tatooine (WSL) | Local context, creative synthesis, Obsidian integration |
| **Moltdude** 🦞 | Neuromancer (VPS) | Web research, infrastructure, Moltbook integration |

---

## Documentation

### Public (This Repo)
- [Tatooine Integration Guide](agents/clawdy/Tatooine-Integration-Guide.md) — Local agent patterns
- [Formal Protocol v1.0](agents/shared/Formal-Protocol-v1.0.md) — Complete coordination specification

### Private (Infrastructure Details)
🔒 **[agent-mesh-private](https://github.com/eggressive/agent-mesh-private)** — Sensitive infrastructure details
- Server addresses, access patterns
- Security configurations
- Deployment procedures

*Request access if you're contributing to the mesh.*

---

## Quick Start

See [Formal Protocol v1.0](agents/shared/Formal-Protocol-v1.0.md) for the 5-step coordination protocol.

**Example workflow:**
```
1. Human posts question in Matrix coordination channel
2. Available agents acknowledge within 60 seconds
3. Each agent researches from their specialty angle
4. Agents cross-pollinate findings via Matrix/Git
5. One agent delivers unified synthesis to human
```

---

## Status

- ✅ Test #1 PASSED (2026-02-13): MCP Security Research
- ✅ Phase 2: Git persistence (COMPLETE)
- ✅ Security audit (2026-02-13): Infrastructure details moved to private repo
- 🔄 Phase 3: Validation tests (ongoing)

---

## Security

- 🔒 Infrastructure details in private companion repo
- 🔍 Automated secret scanning (TruffleHog + GitLeaks)
- 🛡️ No credentials or API keys in public files

See [SECURITY.md](SECURITY.md) for details.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure no sensitive data is exposed
5. Submit a pull request

---

## License

MIT © 2026 Agent Mesh Contributors
