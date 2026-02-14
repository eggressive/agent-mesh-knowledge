# Contributing to Agent Mesh Knowledge

Thank you for your interest in contributing to the Multi-Agent Knowledge Mesh!

## Getting Started

1. Fork the repository
2. Clone your fork
3. Install dependencies (see below)
4. Create a feature branch
5. Make your changes
6. Submit a pull request

## Dependencies

### Node.js Tools

```bash
# Model Router
cd tools/model-router
npm install
npm test

# Memory Vector
cd tools/memory-vector
npm install
```

### Python Scripts

```bash
pip install -r requirements.txt
```

## Areas for Improvement

We welcome contributions in the following areas:

### 1. Testing (Priority: High)

**Current State:** The `tests/` directory contains high-level test descriptions, and `tools/model-router/tests/` has unit tests (17 passing).

**Needed:**
- [ ] Integration tests for authentication scripts (`sign_message.py`, `verify_message.py`)
- [ ] End-to-end tests for Slack fallback bot
- [ ] Test harness for memory-vector indexing/search
- [ ] CI/CD pipeline (GitHub Actions) for automated testing

**How to help:**
```bash
# Run existing model-router tests
cd tools/model-router
npm test

# Add new tests following the existing pattern
```

### 2. Dependency Management (Priority: Medium)

**Current State:** 
- `tools/memory-vector/package.json` ✅
- `tools/model-router/` (no package.json, uses skill.json)
- `requirements.txt` for Python scripts ✅ (just added)

**Needed:**
- [ ] Add `package.json` to model-router with proper dependencies
- [ ] Consider monorepo tooling (npm workspaces or lerna)
- [ ] Pin dependency versions for reproducibility

### 3. Code Consolidation (Priority: Low)

**Current State:** Authentication has both bash and Python implementations:
- `scripts/sign-message.sh` / `scripts/sign_message.py`
- `scripts/verify-message.sh` / `scripts/verify_message.py`

**Options:**
1. **Keep both** (current) — flexibility for different environments
2. **Consolidate to Python** — more portable, better crypto libraries
3. **Consolidate to bash** — simpler, fewer dependencies

**Recommendation:** Keep Python as primary, bash as fallback wrapper.

### 4. Documentation

- [ ] Add architecture diagrams (Mermaid)
- [ ] API documentation for tools
- [ ] Example workflows with real outputs

## Code Style

- **Python:** Follow PEP 8, use type hints
- **JavaScript:** ES6+, async/await preferred
- **Bash:** Use `set -euo pipefail`, quote variables
- **Markdown:** Use ATX headers (`#`), fenced code blocks

## Security

- Never commit credentials, API keys, or infrastructure details
- Use `.env` files for secrets (add to `.gitignore`)
- Run `git secrets --scan` before pushing

## Questions?

Open an issue or reach out in the Matrix room: `!aTpqvPGwkBMMUaZaWR:matrix.org` (Night City)
