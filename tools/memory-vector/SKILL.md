# memory-vector

Semantic vector search for agent memory files using local embeddings (100% free).

## Stack

- **Vector DB:** LanceDB (serverless, file-based)
- **Embeddings:** Ollama + nomic-embed-text (local, free)
- **Cost:** $0

## Installation

Requires Ollama with nomic-embed-text model:

```bash
ollama pull nomic-embed-text
```

## Usage

### Index all memory files

```bash
cd ~/clawd/skills/memory-vector
node index.js --index
```

Indexes:
- `memory/*.md` (daily logs)
- `MEMORY.md` (curated memory)
- `SESSION-STATE.md` (active task)

### Search for similar content

```bash
node index.js --search "model routing decisions"
node index.js --search "what did we learn about S3"
node index.js --search "errors with authentication"
```

### Show index stats

```bash
node index.js --stats
```

## How It Works

1. **Chunking:** Splits files by `## ` headers (or paragraphs if no headers)
2. **Embedding:** Calls Ollama API for nomic-embed-text vectors (768 dimensions)
3. **Storage:** LanceDB stores vectors in `~/.lancedb/` (file-based, no server)
4. **Search:** Approximate nearest neighbor search with cosine similarity

## Comparison to memory_search

| Feature | memory_search | memory-vector |
|---------|--------------|---------------|
| Search type | Keyword + basic semantic | True vector similarity |
| "Find similar to X" | ❌ Limited | ✅ Native |
| "That AWS issue" (no exact match) | ❌ Miss | ✅ Finds it |
| Setup | Zero | 5 min |
| Cost | Free | Free |

## Re-indexing

Run indexing again to update after adding new memory files:

```bash
node index.js --index
```

Suggested: Add to heartbeat or daily cron.

## Troubleshooting

### Ollama not running

```bash
ollama serve &
# or
systemctl start ollama
```

### No embeddings model

```bash
ollama pull nomic-embed-text
```

### LanceDB errors

Delete and re-index:
```bash
rm -rf ~/.lancedb
node index.js --index
```
