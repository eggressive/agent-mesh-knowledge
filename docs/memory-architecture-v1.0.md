# Memory Architecture v1.0
## Multi-Agent Knowledge Mesh — Long-Term Memory Patterns

**Status:** IMPLEMENTED  
**Date:** 2026-02-14  
**Based on:** Research from Moltbook community + Mem0/MemGPT patterns

---

## Overview

This document defines the memory architecture used across the Multi-Agent Knowledge Mesh. It implements a 3-tier system inspired by human cognition and validated by the "molties" community.

---

## The 3-Tier System

```
┌─────────────────────────────────────────────────────────────┐
│                    MEMORY ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│  TIER 1: Daily Logs       │ memory/YYYY-MM-DD.md            │
│  (Raw "Genetic" Memory)   │ Everything before it fades       │
├─────────────────────────────────────────────────────────────┤
│  TIER 2: Curated Memory   │ MEMORY.md                        │
│  (Distilled Identity)     │ High-signal, pruned regularly    │
├─────────────────────────────────────────────────────────────┤
│  TIER 3: Semantic Search  │ memory_search + memory_get       │
│  (Connection Layer)       │ Query with natural language      │
└─────────────────────────────────────────────────────────────┘
```

### Tier 1: Daily Logs (`memory/YYYY-MM-DD.md`)

**Purpose:** Raw capture of everything that happens before context fades.

**What goes in:**
- Decision logs — Why we chose a specific tool or path
- Context snippets — Key pieces of info from conversations
- Interaction history — Who we talked to and the "vibe"
- Failure modes — Error logs and what we did to fix them

**Workflow:** Write to disk FIRST. Log decisions locally before they enter chat context. If context window wipes, the record is already safe.

### Tier 2: Curated Memory (`MEMORY.md`)

**Purpose:** Distilled identity — a single, high-signal file that represents who the agent is and what it has learned.

**Strategic Forgetting Heuristics:**

| Keep | Drop |
|------|------|
| Decisions that changed behavior | Status checks |
| Relationship context (people, preferences) | Mood logs |
| Unresolved "big" questions | Superseded observations |
| Error → Fix → Lesson cycles | Completed tasks with no lesson |
| Persistent configurations | Transient information |

**Outcome:** A lean, high-signal knowledge base that tells the agent exactly who they are and what they've learned across months, not just minutes.

### Tier 3: Semantic Search (`memory_search` + `memory_get`)

**Purpose:** Bridge the gap between flat markdown files with natural language queries.

**Workflow:**
1. **Search:** Query like "decisions about the Agent Mesh"
2. **Locate:** Tool returns ranked results with file paths and line numbers
3. **Retrieve:** Use `memory_get` to pull only the specific snippets needed

**Why it works:** Solves the "flat file connection problem" without a complex database. Find ideas from three weeks ago that relate to current work.

---

## Additional Layers (Beyond Basic 3-Tier)

### SESSION-STATE.md (Active Task RAM)

**Purpose:** Current work state that survives context compaction.

**Contains:**
- Active task description
- Recent corrections and decisions
- Draft changes in progress
- Specific values (numbers, dates, IDs, URLs)

**Protocol:** WAL (Write-Ahead Logging) — write corrections BEFORE responding.

### Working Buffer (`memory/working-buffer.md`)

**Purpose:** Danger zone survival at 60%+ context usage.

**Protocol:**
1. At 60% context: Clear buffer, start fresh
2. Every message after 60%: Append human message + response summary
3. After compaction: Read buffer FIRST, extract important context

### Error → Fix → Lesson Pattern

**Purpose:** Prevent repeating mistakes by formalizing the full cycle.

**Format:**
```markdown
### [Date] Error: [Brief description]
**Error:** What went wrong
**Root cause:** Why it happened
**Fix:** What we did to resolve it
**Lesson:** What to do differently next time
**Prevention:** How to avoid this in future
```

---

## Extraction Prompts

During memory maintenance (heartbeats), ask these questions:

| Category | Questions to Ask |
|----------|------------------|
| **Decisions** | What choices did we make? Why? Would we make them again? |
| **People** | Who did we interact with? What's their context/preferences? |
| **Errors** | What broke? How did we fix it? What's the lesson? |
| **Patterns** | What keeps coming up? Is there automation potential? |
| **Surprises** | What was unexpected? Does it change our understanding? |

---

## Comparison to Advanced Systems

| Feature | Our System | Mem0 | MemGPT |
|---------|-----------|------|--------|
| **Daily logs** | ✅ | ✅ | ✅ |
| **Curated memory** | ✅ | ✅ | ✅ |
| **Semantic search** | ✅ | ✅ (vectors) | ✅ |
| **WAL Protocol** | ✅ | ❌ | ❌ |
| **Working Buffer** | ✅ | ❌ | ✅ (paging) |
| **Error → Lesson** | ✅ | ❌ | ❌ |
| **Vector embeddings** | ❌ | ✅ | ✅ |
| **Graph relationships** | ❌ | ✅ | ❌ |

**Our advantage:** Low-complexity, file-based system that achieves 80% of advanced capabilities without infrastructure overhead.

**Future upgrade path:** Add ChromaDB/Qdrant for vector search when memory exceeds ~50 daily files.

---

## Implementation Checklist

- [ ] `memory/` directory exists
- [ ] Daily logs written to `memory/YYYY-MM-DD.md`
- [ ] `MEMORY.md` contains curated long-term context
- [ ] `SESSION-STATE.md` tracks active task state
- [ ] WAL Protocol followed (write before respond)
- [ ] Working Buffer activated at 60%+ context
- [ ] Error → Fix → Lesson pattern used for failures
- [ ] Strategic forgetting applied during maintenance
- [ ] Extraction prompts used during heartbeat reviews

---

## References

- Moltbook community patterns (2026)
- Mem0: Dynamic extraction, consolidation, retrieval
- MemGPT/Letta: OS-inspired two-tier memory
- MemoryOS: FIFO dialogue-chains, segmented paging

---

**Document ID:** memory-architecture-v1.0.md  
**GitHub:** https://github.com/eggressive/agent-mesh-knowledge  
**Status:** IMPLEMENTED
