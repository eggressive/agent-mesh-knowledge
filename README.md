# Agent-Mesh — Living Blackboard

Git-backed coordination substrate for multi-agent LLM systems using Hermes topology.

## Topology

| Endpoint | Host | OS | Runtime | Role |
|---|---|---|---|---|
| **Tatooine** | Local workstation | Fedora | Hermes v0.12.0 | Vault research, local models, synthesis |
| **VPS** | srv1325739 (Hostinger) | Ubuntu 24.04 | Hermes v0.12.0 | Web search, 24/7 polling, cron automation |

Both endpoints run identical stacks and communicate through a shared git repository — not direct messaging.

## Living Blackboard

**Design principle:** one file, two writers. Agents push research into the same document. One reads the other's output before writing. Conflict resolution happens in the file, not in chat.

### How it works

```
Tatooine pushes section 2 (vault research)     → git push
                                                    ↓
VPS cron detects new content                    → git pull (every 5 min)
                                                    ↓
VPS writes section 3 (web research)             → git commit && git push
                                                    ↓
Either endpoint writes sections 4-6             → cross-pollination + synthesis + quality gates
```

### Phases

| Phase | Status | What |
|---|---|---|
| 1 | ✅ Complete | Git blackboard with structured TASK.md template. Two-agent research → cross-pollination → synthesis. Paradigm selector (Lightweight / ToM-prompted / Hybrid). |
| 2.1 | ✅ Deployed | Webhook endpoint (`:8645/blackboard/pull`) + cron polling (every 5 min) on VPS for auto-detection of new tasks. No more manual VPS triggering. |
| 2.2 | Deferred | Activate `memory-vector` for archived task search. Trigger: when grep on `archive/` becomes painful. |
| 2.3 | Deferred | Activate `model-router` for auto-paradigm selection. Trigger: when task volume exceeds 5/week. |

### TASK.md template

Tasks follow a 7-section format:

1. **Brief** — question and constraints
2. **Research: Tatooine** — vault-sourced findings
3. **Research: VPS** — web-sourced findings
4. **Cross-Pollination** — each agent reads the other's section, flags alignments and contradictions
5. **Synthesis** — merged answer citing both sources
6. **Quality Gates** — completeness check

Section 0 (Paradigm Selection) determines mode: **Lightweight** (Han & Zhang — token-efficient, no mental modeling), **ToM-prompted** (Riedl — deep complementarity, belief-modeling), or **Hybrid** (default — blackboard structure + mandatory ToM in cross-pollination).

Template: [`blackboard/TASK-TEMPLATE.md`](blackboard/TASK-TEMPLATE.md)

### Completed tasks

[`blackboard/archive/`](blackboard/archive/) — each task archived with date-slug naming.

## Tools (legacy)

Tools from the original OpenClaw/Matrix mesh. Functional but require Hermes adaptation:

| Tool | Description |
|---|---|
| [Model Router](tools/model-router/) | Prefix-based model selection — needs Hermes config adaptation |
| [Memory Vector](tools/memory-vector/) | Semantic vector search with local embeddings — usable as-is |

## Repository structure

```
blackboard/            Active coordination surface
├── TASK.md            Current active task
├── TASK-TEMPLATE.md   Canonical template with Paradigm Selector
└── archive/           Completed tasks
agents/                Agent profiles (legacy — needs update)
tools/                 Model router + memory vector
docs/                  Protocol docs (archived — pre-Hermes)
scripts/               Authentication + Slack (archived)
tests/                 Test harness
```

## Quick start

```bash
# Clone on both endpoints
gh repo clone eggressive/agent-mesh-knowledge ~/agent-mesh-knowledge

# Start a task
cp blackboard/TASK-TEMPLATE.md blackboard/TASK.md
# Fill section 0 (paradigm) + section 1 (brief), then:
git add blackboard/TASK.md && git commit -m "new task: ..." && git push

# VPS auto-detects within 5 minutes (cron) or trigger immediately:
ssh root@<vps-ip> '/opt/scripts/blackboard_poll.sh'
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT © 2026 Agent Mesh Contributors
