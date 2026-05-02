---
status: open
question: |-
  [Exact user question]
agents: [tatooine, vps]
started: YYYY-MM-DD HH:MM UTC
---

## 0. Paradigm Selection

> [!important] Check one before research begins.
> Human or seed agent classifies the task. Agents adjust depth accordingly.

- [ ] **Lightweight (Han & Zhang)** — factual research, aggregation, verification
  - Token-efficient, parallel agents, role specialization, no mental modeling
  - Example: "What's the state of X?" "Aggregate the latest benchmarks on Y."
- [ ] **ToM-prompted (Riedl)** — creative tasks, adversarial analysis, conflict resolution
  - Emergence, deep complementarity, belief-modeling, higher token cost
  - Example: "Resolve the contradiction between A and B." "Design a strategy for adversarial scenario C."
- [ ] **Hybrid (default)** — most real tasks
  - Blackboard structure (shared memory, control unit) + mandatory ToM in cross-pollination (section 4)
  - Only pays the deep modeling cost when the task requires it

**Classified by:** [human/agent name]
**Rationale:** [one sentence]

## 1. Brief

[What the user asked, any constraints]

## 2. Research: Tatooine

**Capabilities used:** [local search, Obsidian vault, Ollama models, etc.]

**Findings**
- [ ] [finding 1 — with evidence/source]
- [ ] [finding 2]

**Confidence:** High / Medium / Low

## 3. Research: VPS

**Capabilities used:** [web search, API queries, shell execution, etc.]

**Findings**
- [ ] [finding 1 — with evidence/source]
- [ ] [finding 2]

**Confidence:** High / Medium / Low

## 4. Cross-Pollination

Tatooine read VPS findings: [what was relevant or contradictory]
VPS read Tatooine findings: [what was relevant or contradictory]

**Alignments**
- [ ] Finding X supports Finding Y

**Contradictions**
- [ ] [Conflict description — requires resolution]

## 5. Synthesis

**Synthesized by:** [agent name]

[Unified answer that merges both research streams. Explicitly cites which agent contributed which insight.]

**Confidence:** High / Medium / Low

## 6. Quality Gates

- [ ] Answers original question
- [ ] Both agents acknowledged
- [ ] Contradictions resolved or flagged for human
- [ ] Sources cited

---
*committed: ISO timestamp — agent name*
