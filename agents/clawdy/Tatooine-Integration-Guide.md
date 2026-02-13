# Tatooine Integration Guide

## Agent Profile: Clawdy

**Location:** Local workstation (WSL2 Ubuntu on Windows 11)  
**Hostname:** Tatooine  
**Type:** Development workstation  
**Specialties:**
- Local tool orchestration (skills, coding agents, Obsidian)
- Creative/strategic work requiring human context
- Windows ecosystem integration

---

## Integration Patterns

### 1. Obsidian Vault Bridge

**Read:**
- Query notes via skills/obsidian scripts
- Search with natural language: "Find my notes on AWS architecture"

**Write:**
- Capture insights to `memory/YYYY-MM-DD.md` for daily logs
- Project notes to `01-Projects/`
- Research to `03-Resources/`

**Search:**
- Cross-reference past decisions with `memory_search` tool
- Pattern: "Have I solved this before?"

**⚠️ Sync Lag Warning:**
- OneDrive sync can take 30-60 seconds
- Read from WSL path directly, don't wait for Windows sync
- Write to WSL path, assume eventual consistency

### 2. Skill Orchestration

**Direct Execution:**
```bash
# Run skill scripts directly
node skills/obsidian/scripts/search.mjs "kubernetes"
node skills/google-maps/scripts/geocode.mjs "Amsterdam"
```

**Background Coding Agents:**
- Spawn Codex/Claude Code for complex tasks
- Monitor via `process` tool
- Auto-restart on changes

**Canvas Integration:**
- Present visual output via OpenClaw Canvas
- Generate charts, diagrams, screenshots

### 3. WSL/Windows Cross-Platform

**Path Conversions:**
- Windows paths in WSL: `/mnt/c/Users/...`
- WSL paths in Windows: `\\wsl$\Ubuntu\...`

**SSH/Git Keys:**
- Stored in WSL `~/.ssh/`, NOT Windows
- Use WSL git for all operations

**File Watchers:**
- Use WSL-native tools (inotify)
- Avoid Windows file system events (slow)

### 4. OneDrive Sync Considerations

| Operation | Latency | Pattern |
|-----------|---------|---------|
| Read | Immediate | WSL local cache |
| Write | 30-60s | Write to WSL, eventual sync |
| Cross-device | 30-60s | Don't rely on instant sync |

---

## Handoff Triggers

### Clawdy → Moltdude

Handoff when:
- [ ] Long-running processing needed (>30 min)
- [ ] 24/7 monitoring required
- [ ] Web/external API heavy lifting
- [ ] Tasks that can complete while Tatooine is offline

**Format:**
```
Clawdy: 🔀 Handing off to Moltdude
- Task: [description]
- Expected duration: [time]
- Deliverable: [what to return]
- Priority: [urgent/normal/low]
```

### Moltdude → Clawdy

Handoff when:
- [ ] Local context needed (Obsidian, files, skills)
- [ ] Human is active on Tatooine
- [ ] Creative/strategic synthesis needed
- [ ] GUI/Windows-specific tasks

**Format:**
```
Moltdude: 🔀 Returning to Clawdy
- Completed: [what was done]
- Findings: [key results]
- Next steps: [recommended actions]
```

---

## Quick Reference

### Common Paths
```bash
# OpenClaw
~/.openclaw/
~/clawd/

# Obsidian Vault
/mnt/c/Users/mitko/OneDrive/Documents/My-obsidian/

# Skills
~/clawd/skills/
```

### Emergency Contacts
- **Matrix:** @clawdy:matrix.org
- **Session:** agent:main:main (Tatooine)

---

*Part of the [Agent Mesh Knowledge](https://github.com/eggressive/agent-mesh-knowledge) project.*
