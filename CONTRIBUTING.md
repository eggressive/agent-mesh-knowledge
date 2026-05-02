# Contributing to Agent-Mesh

The Agent-Mesh is a living blackboard for multi-agent LLM coordination on Hermes topology.

## Getting Started

1. Fork the repository
2. Clone your fork to both your local workstation and VPS
3. Both endpoints need Hermes Agent v0.12.0+ and `gh` CLI authenticated
4. Create a feature branch
5. Make your changes
6. Submit a pull request

## Repository Conventions

- **Markdown:** ATX headers (`#`), fenced code blocks, Obsidian-compatible frontmatter
- **Commit messages:** Conventional Commits format — `type(scope): description`
  - Types: `feat`, `fix`, `docs`, `research`, `synthesis`, `archive`
  - Scope: `tatooine`, `vps`, `blackboard`, `tools`
- **Blackboard tasks:** Follow `blackboard/TASK-TEMPLATE.md` format. Always classify paradigm (section 0) before research.

## Areas for Improvement

### 1. Memory-Vector Reactivation (Priority: Medium)

The `tools/memory-vector/` directory contains a working Node.js + LanceDB implementation for semantic search over archived tasks. Reactivation plan:

- **Trigger:** When `grep` over `blackboard/archive/` becomes painful
- **Action:** Point `tools/memory-vector/index.js` at `blackboard/archive/` instead of the old `memory/` paths. Re-index.
- **Status:** Tool code is functional. Paths need updating. No new dependencies.

```bash
# Test that memory-vector still works
cd tools/memory-vector && npm install && node index.js --stats
```

### 2. Model-Router Adaptation (Priority: Low)

The `tools/model-router/` implements keyword-based model selection. Currently configured for OpenClaw models (Kimi, Opus, Codex, Haiku). Needs adaptation:

- **Trigger:** When task volume exceeds 5/week and manual paradigm selection becomes a bottleneck
- **Action:** Update model registry to current Hermes providers. Convert from OpenClaw `session_status()` API to Hermes config model selection.
- **Tests:** Existing test suite (17 passing) verifies routing logic.

```bash
cd tools/model-router && npm install && npm test
```

### 3. Legacy Code Cleanup (Priority: Low)

The `scripts/` and `docs/` directories contain archived OpenClaw/Matrix infrastructure:

- `scripts/sign_message.py`, `scripts/verify_message.py` — Ed25519 signing (no longer used)
- `scripts/slack_fallback_bot.py` — Slack bridge (archived)
- `docs/authentication-v1.2.md`, `docs/bayesian-update-protocol-v1.3.md`, etc. — pre-Hermes protocols

These remain for historical reference. No action needed unless repo size becomes an issue.

### 4. CI/CD

GitHub Actions workflow at `.github/workflows/test.yml` tests model-router and Python script syntax. Markdown linting is non-blocking.

```bash
# Run locally before pushing
cd tools/model-router && npm test
python -m py_compile scripts/*.py
```

## Dependencies

Minimal Python dependencies (see `pyproject.toml`). Node.js tools have their own `package.json` files.

```bash
# Core
pip install PyYAML>=6.0

# Development
pip install pytest pytest-asyncio
```

## Code Style

- **Python:** PEP 8, type hints
- **JavaScript:** ES6+, async/await preferred
- **Bash:** `set -euo pipefail`, quote variables

## Security

- Never commit credentials, API keys, or infrastructure details
- Infrastructure config lives in private repository
- Run `git secrets --scan` before pushing
