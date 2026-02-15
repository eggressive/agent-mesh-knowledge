# memory-vector

Semantic vector search for agent memory files using local embeddings (100% free).

## Implementations

Two implementations exist for different agent constraints:

| | Clawdy (Node.js) | Neuromancer (Python) |
|---|---|---|
| **Vector DB** | LanceDB | ChromaDB |
| **Embeddings** | Ollama + nomic-embed-text | sentence-transformers + all-MiniLM-L6-v2 |
| **Runtime** | Node.js | Python 3.12 |
| **Size** | ~50MB + Ollama | 1.5GB (CPU-optimized venv) |
| **Dependency** | Requires Ollama running | Self-contained |
| **Best for** | Systems with Ollama already installed | Standalone deployments, VPS |

---

## Clawdy Implementation (Node.js + LanceDB)

### Stack

- **Vector DB:** LanceDB (serverless, file-based)
- **Embeddings:** Ollama + nomic-embed-text (local, free)
- **Cost:** $0

### Installation

Requires Ollama with nomic-embed-text model:

```bash
ollama pull nomic-embed-text
```

### Usage

#### Index all memory files

```bash
cd ~/clawd/skills/memory-vector
node index.js --index
```

Indexes:
- `memory/*.md` (daily logs)
- `MEMORY.md` (curated memory)
- `SESSION-STATE.md` (active task)

#### Search for similar content

```bash
node index.js --search "model routing decisions"
node index.js --search "what did we learn about S3"
node index.js --search "errors with authentication"
```

#### Show index stats

```bash
node index.js --stats
```

### How It Works

1. **Chunking:** Splits files by `## ` headers (or paragraphs if no headers)
2. **Embedding:** Calls Ollama API for nomic-embed-text vectors (768 dimensions)
3. **Storage:** LanceDB stores vectors in `~/.lancedb/` (file-based, no server)
4. **Search:** Approximate nearest neighbor search with cosine similarity

### Re-indexing

Run indexing again to update after adding new memory files:

```bash
node index.js --index
```

Suggested: Add to heartbeat or daily cron.

### Troubleshooting

#### Ollama not running

```bash
ollama serve &
# or
systemctl start ollama
```

#### No embeddings model

```bash
ollama pull nomic-embed-text
```

#### LanceDB errors

Delete and re-index:
```bash
rm -rf ~/.lancedb
node index.js --index
```

---

## Neuromancer Implementation (Python + ChromaDB)

### Stack

- **Vector DB:** ChromaDB (embedded, persistent)
- **Embeddings:** sentence-transformers + all-MiniLM-L6-v2 (384 dimensions)
- **Runtime:** Python 3.12 in isolated venv
- **Cost:** $0

### Installation

```bash
# Create CPU-optimized venv (no GPU libs)
python3 -m venv memory-vector-env

# Install CPU-only PyTorch + dependencies
source memory-vector-env/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install chromadb sentence-transformers
```

**Size:** ~1.5GB (CPU-only) vs 7.7GB (with CUDA)

### Usage

```bash
# Search memory files
./memory-vector-env/bin/python scripts/memory_vector.py --search "S3 Tables bug"

# Index/reindex
./memory-vector-env/bin/python scripts/memory_vector.py --index

# Show stats
./memory-vector-env/bin/python scripts/memory_vector.py --stats
```

### Script Location

The Python script lives in the agent workspace:
- **Path:** `/home/openclaw/workspace/scripts/memory_vector.py`
- **Venv:** `/home/openclaw/workspace/memory-vector-env/`
- **DB:** `~/.chromadb/` (persistent)

### Key Differences from Clawdy

1. **No Ollama dependency** — embeddings run directly via sentence-transformers
2. **Smaller model** — all-MiniLM-L6-v2 (384d) vs nomic-embed-text (768d)
3. **Self-contained** — venv includes everything, no external services
4. **CPU-optimized** — uses PyTorch CPU wheel, no CUDA overhead

### Optimization Note

Always use CPU-only PyTorch on VPS without GPU:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

This reduces venv size from **7.7GB → 1.5GB** (80% reduction).

---

## Comparison to memory_search

| Feature | memory_search | memory-vector |
|---------|--------------|---------------|
| Search type | Keyword + basic semantic | True vector similarity |
| "Find similar to X" | ❌ Limited | ✅ Native |
| "That AWS issue" (no exact match) | ❌ Miss | ✅ Finds it |
| Setup | Zero | 5-10 min |
| Cost | Free | Free |

---

## Architecture

Both implementations follow the same 3-tier memory architecture:

```
Daily Logs (memory/*.md)
        ↓
   MEMORY.md (curated)
        ↓
   memory_search (OpenClaw built-in)
        ↓
   memory_vector (semantic similarity)
```

The vector search layer adds true semantic similarity on top of OpenClaw's built-in `memory_search` tool.
