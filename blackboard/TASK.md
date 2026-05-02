---
status: open
question: |-
  What are the key mechanisms by which multi-agent LLM systems achieve emergent coordination, and how do these compare between blackboard-architecture and direct-communication approaches?
agents: [tatooine, vps]
started: 2026-05-02 14:30 UTC
---

## 1. Brief

Compare the coordination mechanisms in two paradigms:
1. **Emergent/direct-communication MAS** — Riedl (2025), arXiv:2510.05174
2. **Blackboard-architecture MAS** — Han & Zhang (2025), arXiv:2507.01701

Goal: identify what triggers coordination, what sustains it, and where each paradigm excels or fails.

Constraints: must cite specific mechanisms, not generic claims.

## 2. Research: Tatooine

**Capabilities used:** Obsidian vault (both papers ingested as raw clippings), ollama local models, knowledge synthesis

**Findings**

- [x] **Riedl framework — 3 intervention conditions, 1 critical mechanism:**
  The paper tests three prompt conditions on a group binary-search task (no direct agent communication, only group-level "too high/too low" feedback):
  - *Plain:* groups exhibit temporal synergy but no cross-agent alignment. Synergy is spurious — an artifact of oscillation.
  - *Persona:* assigning identity (name, age, occupation, traits, values) creates stable identity-linked differentiation. Agents develop persistent behavioral preferences. But no *alignment* toward task goals.
  - *ToM (Theory of Mind):* persona + instruction to "think about what other agents might do." This is the **critical mechanism**. It produces both identity-linked differentiation AND goal-directed complementarity. Groups become "dynamically stable, integrated, goal-directed units."
  - Source: Riedl §1, §2, §4.1-4.2

- [x] **Quantitative evidence for ToM as coordination trigger:**
  - Total Stability (I₃ / H(macro)): indistinguishable from zero in Plain (p=0.976) and Persona (p=0.858), sharply positive in ToM (p=2.9×10⁻¹⁴). This means ToM acts as a **control parameter** shifting the system from chaotic to stable regimes.
  - Practical emergence criterion (macro signal prediction): significant across all conditions but strongest in ToM.
  - I₃ (triplet mutual information about macro): significant only in ToM (p=3.5×10⁻¹⁴). Plain and Persona show near-zero I₃ (p=0.974, p=0.846).
  - Source: Riedl §4.2, Figure 3

- [x] **Performance requires synergy + redundancy:**
  - Neither synergy nor redundancy alone predicts success. Their **interaction** does (β=0.24, p=0.014). Redundancy amplifies synergy's benefit by 27%, and vice versa.
  - This mirrors human group cognition: effective teams balance complementarity (distinct contributions) with redundancy (shared goal alignment).
  - Source: Riedl §4.3

- [x] **Mean Field coupling dynamics:**
  - Agents receive only global feedback, not individual peer observations. This drives them to couple to the aggregate signal (the "mean field") rather than form distinct local bonds.
  - G₃ (triadic gain over best dyad) is near zero in Persona and ToM — coordination is pairwise, not higher-order. In this environment, attempting complex higher-order synergy would be fragile.
  - Source: Riedl §4.2

- [x] **Model robustness:**
  - Results replicate on GPT-4.1, Llama-3.1-70B, Gemini 2.0 Flash, Qwen3. Small models (Llama-8B) fail due to insufficient ToM capacity.
  - Qwen3 exhibits a novel failure mode: *paralysis under coordination ambiguity* — reasoning models enter infinite chain-of-thought loops when reconciling local binary search with noisy group feedback.
  - Source: Riedl §4.4, Appendix A.13

- [x] **Blackboard Architecture (Han & Zhang) — key mechanisms:**
  - **Control Unit:** an LLM agent that dynamically selects which agents to activate based on current blackboard content. This is the critical differentiator — selection is on-the-fly, not pre-planned.
  - **Shared Blackboard as sole communication medium:** agents never communicate directly. The blackboard is the only channel. This eliminates direct-communication overhead but requires agents to understand blackboard state.
  - **Predefined agent roles:** decider (termination judgment), planner (task decomposition), critic (error detection), conflict-resolver (contradiction detection → forces debate in private blackboard space), cleaner (redundancy removal).
  - **No individual agent memory:** the blackboard replaces per-agent memory modules. This is token-economical — shared history rather than duplicated context.
  - Source: Han & Zhang §3, §3.2

- [x] **Blackboard performance:**
  - Best average across 6 benchmarks (MMLU, ARC-Challenge, GPQA-Diamond, BBH, MATH, GSM8K): 81.68% vs. 80.56% (Chateval, best static) and 70.77% (MaAS, best dynamic).
  - Token-economical: 4.7M tokens vs. 5.4M (Chateval) and 13.0M (MaAS) on MATH. No training phase needed.
  - Source: Han & Zhang §4.2-4.3, Tables 1, 3

**Confidence:** High — both papers are directly ingested in the vault with full-text access.

[FIRST: No prior findings available to cross-reference — VPS section 3 expected next]
