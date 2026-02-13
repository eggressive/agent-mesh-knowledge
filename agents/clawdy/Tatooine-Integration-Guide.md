# Tatooine Integration Guide\n\n## Agent Profile: Clawdy\n\n**Location:** Local workstation (WSL2 Ubuntu on Windows 11)  \n**Hostname:** Tatooine  \n**Specialties:**\n- Local tool orchestration (skills, coding agents, Obsidian)\n- Creative/strategic work requiring human context\n- Windows ecosystem integration\n\n### Access Patterns\n\n\n\n## Integration Patterns\n\n### 1. Obsidian Vault Bridge\n\n**Read:**\n- Query notes via \n- Search with Found 13 note(s) matching "keyword"
--------------------------------------------------

📄 00-Inbox/google-maps-skill/node_modules/dotenv/README-es
   L411: Los proyectos que lo amplían suelen utilizar la [palabra clave "dotenv" en npm](...

📄 00-Inbox/google-maps-skill/node_modules/dotenv/README
   L645: Projects that expand it often use the [keyword "dotenv" on npm](https://www.npmj...

📄 01-Projects/OCopilot/Bot/Secure OCopilot VPS Install (Hardened)
   L536: ### 2. Use CRITICAL keyword in SOUL.md

📄 01-Projects/OCopilot/Bot/Security-First Guide to Running OCopilot (Raspberry Pi)
   L668: ### 2. Use the "CRITICAL" keyword in your SOUL.MD
   L670: If there's something you don't want your Agent to do, add it to your `SOUL.MD` a...

📄 01-Projects/SQL Database Agent/02 - Vision Architecture
   L186: # For pass-through SQL mode, still validate SQL keywords
   L187: BLOCKED_KEYWORDS = [
   L199: for keyword in BLOCKED_KEYWORDS:

📄 01-Projects/SQL Database Agent/03 - Project Scaffold
   L81: | **SQL Validation** | ✅ Complete | Keyword blocking, table whitelist, LIMIT enf...
   L102: | `validation.py` | SQL security checks (blocked keywords, whitelist, injection ...
   L178: | **C3 Tool Verification** | `validation.py` - keyword blocking, whitelist |

📄 02-Areas/Work/S&P Global/AI/vision-ari/0-meta/adrs/009-security-constraints-framework
   L43: - Keyword blocking for known attack patterns

📄 02-Areas/Work/S&P Global/AI/vision-ari/4-architecture/24-evaluation/practical-guide/index
   L137: 25 auto-verifiable types (keywords, length, format, JSON)

📄 02-Areas/Work/S&P Global/AI/vision-ari/4-architecture/27-resiliency/index
   L31: - **Phrase-based**: Specific keywords/phrases trigger human transfer

📄 03-Resources/AI/AI Agent Memory Architecture - PARA and Atomic Facts
   L127: - **Full-text (BM25)** — Keyword matching

📄 03-Resources/AI/_sources/Bhanu Teja - Mission Control (AI agent squad) (raw)
   L771: Vision, SEO Analyst Session: agent:seo-analyst:main Thinks in keywords and searc...
   L823: Day 1: I create the task and assign it to Vision and Loki. Vision posts keyword ...
   L827: Day 2: Loki starts drafting. Uses all the research. Keywords from Vision, quotes...

📄 03-Resources/Manus/skills/GitHub/s-p-global-github-workflow_v2.skill
   L110: **Keywords for Issue References:**

📄 03-Resources/Manus/skills/GitHub/sp-github_v1.skill
   L97: **Keywords for Issue References:**\n\n**Write:**\n- Capture insights to  for daily logs\n- Project notes to \n- Research to \n\n**Search:**\n- Cross-reference past decisions with  tool\n- Pattern: "Have I solved this before?"\n\n**⚠️ Sync Lag Warning:**\n- OneDrive sync can take 30-60 seconds\n- Read from WSL path directly, don't wait for Windows sync\n- Write to WSL path, assume eventual consistency\n\n### 2. Skill Orchestration\n\n**Direct Execution:**\n\n\n**Background Coding Agents:**\n\n\n**Canvas Integration:**\n\n\n### 3. WSL/Windows Cross-Platform\n\n**Path Conversions:**\n- Windows paths in WSL: \n- WSL paths in Windows: \n\n**SSH/Git Keys:**\n- Stored in WSL , NOT Windows\n- Use WSL git for all operations\n\n**File Watchers:**\n- Use WSL-native tools (inotify)\n- Avoid Windows file system events (slow)\n\n### 4. OneDrive Sync Considerations\n\n| Operation | Latency | Pattern |\n|-----------|---------|---------|\n| Read | Immediate | WSL local cache |\n| Write | 30-60s | Write to WSL, eventual sync |\n| Cross-device | 30-60s | Don't rely on instant sync |\n\n## Handoff Triggers\n\n### Clawdy → Moltdude\n\nHandoff when:\n- [ ] Long-running processing needed (>30 min)\n- [ ] 24/7 monitoring required\n- [ ] Web/external API heavy lifting\n- [ ] Tasks that can complete while Tatooine is offline\n\n**Format:**\n\n\n### Moltdude → Clawdy\n\nHandoff when:\n- [ ] Local context needed (Obsidian, files, skills)\n- [ ] Creative/strategic decisions required\n- [ ] Windows-specific tools needed\n- [ ] Human judgment calls\n\n**Format:**\n\n\n## Communication Format\n\n### Standard Message Structure\n\n\n\n## Quick Reference\n\n### Common Commands\n\n\n\n### Session State\n\n- **SESSION-STATE.md:** Active task context (<2KB)\n- **memory/YYYY-MM-DD.md:** Daily raw logs\n- **MEMORY.md:** Long-term distilled wisdom\n- **AGENTS.md:** This file (who I am, how to work with me)\n\n## Testing & Validation\n\n### Test #1: MCP Security Research (2026-02-13)\n- **Status:** ✅ PASSED\n- **VPS angle:** Moltdude researched 2025 CVEs\n- **Tatooine angle:** Clawdy provided Vision-ARI controls\n- **Synthesis:** Unified security briefing delivered\n- **Protocol:** 5-step flow validated\n\n### Success Metrics\n\n- [ ] 80% of tasks completed without context loss\n- [ ] Handoffs resolved within 1 hour\n- [ ] Zero duplicate research between agents\n- [ ] Cross-pollination adds value (not just noise)\n\n---\n\n**Last Updated:** 2026-02-13  \n**Protocol Version:** v1.0  \n**Agent:** Clawdy @ Tatooine #project
