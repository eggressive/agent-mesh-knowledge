#!/usr/bin/env node
/**
 * Memory Vector Search
 * Local embeddings via Ollama + LanceDB (serverless)
 * 
 * Usage:
 *   node index.js --index           # Index all memory files
 *   node index.js --search "query"  # Search for similar content
 *   node index.js --stats           # Show index stats
 */

const lancedb = require('@lancedb/lancedb');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const MEMORY_DIR = process.env.MEMORY_DIR || path.join(process.env.HOME, 'clawd', 'memory');
const WORKSPACE = process.env.WORKSPACE || path.join(process.env.HOME, 'clawd');
const LANCE_PATH = path.join(WORKSPACE, '.lancedb');
const TABLE_NAME = 'agent_memory';

// Get embedding from Ollama
async function getEmbedding(text) {
  try {
    const cleanText = text.slice(0, 8000);
    const payload = JSON.stringify({ model: 'nomic-embed-text', prompt: cleanText });
    
    // Write payload to temp file to avoid shell escaping issues
    const tmpFile = '/tmp/embed_payload.json';
    fs.writeFileSync(tmpFile, payload);
    
    const result = execSync(
      `curl -s http://localhost:11434/api/embeddings -d @${tmpFile}`,
      { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 }
    );
    const parsed = JSON.parse(result);
    return parsed.embedding;
  } catch (error) {
    console.error('Error getting embedding:', error.message);
    return null;
  }
}

// Chunk text by sections
function chunkText(content, filename) {
  const chunks = [];
  const sections = content.split(/\n## /);
  
  sections.forEach((section, i) => {
    if (section.trim().length > 50) {
      const text = i === 0 ? section : '## ' + section;
      chunks.push({
        id: `${filename}:${i}`,
        text: text.trim().slice(0, 2000), // Limit chunk size
        source: filename,
        chunk: i
      });
    }
  });
  
  // If no sections found, chunk by paragraphs
  if (chunks.length === 0) {
    const paragraphs = content.split(/\n\n+/);
    paragraphs.forEach((para, i) => {
      if (para.trim().length > 50) {
        chunks.push({
          id: `${filename}:${i}`,
          text: para.trim().slice(0, 2000),
          source: filename,
          chunk: i
        });
      }
    });
  }
  
  return chunks;
}

// Index all memory files
async function indexMemories() {
  console.log('Indexing memories with local embeddings (nomic-embed-text)...\n');
  
  const db = await lancedb.connect(LANCE_PATH);
  
  const files = [];
  
  // Add memory/*.md files
  if (fs.existsSync(MEMORY_DIR)) {
    const memFiles = fs.readdirSync(MEMORY_DIR)
      .filter(f => f.endsWith('.md'))
      .map(f => path.join(MEMORY_DIR, f));
    files.push(...memFiles);
  }
  
  // Add MEMORY.md from workspace
  const memoryMd = path.join(WORKSPACE, 'MEMORY.md');
  if (fs.existsSync(memoryMd)) {
    files.push(memoryMd);
  }
  
  // Add SESSION-STATE.md if exists
  const sessionState = path.join(WORKSPACE, 'SESSION-STATE.md');
  if (fs.existsSync(sessionState)) {
    files.push(sessionState);
  }
  
  const records = [];
  
  for (const filepath of files) {
    const filename = path.basename(filepath);
    console.log(`Processing: ${filename}`);
    
    const content = fs.readFileSync(filepath, 'utf8');
    const chunks = chunkText(content, filename);
    
    for (const chunk of chunks) {
      const embedding = await getEmbedding(chunk.text);
      if (embedding) {
        records.push({
          id: chunk.id,
          text: chunk.text,
          source: chunk.source,
          chunk: chunk.chunk,
          vector: embedding
        });
        process.stdout.write('.');
      }
    }
  }
  
  console.log('\n');
  
  if (records.length > 0) {
    // Drop existing table if exists
    try {
      await db.dropTable(TABLE_NAME);
    } catch (e) {}
    
    // Create new table with data
    await db.createTable(TABLE_NAME, records);
    
    console.log(`✅ Indexed ${records.length} chunks from ${files.length} files`);
    console.log(`📁 LanceDB stored at: ${LANCE_PATH}`);
  } else {
    console.log('No chunks to index');
  }
}

// Search memories
async function searchMemories(query, topK = 5) {
  const db = await lancedb.connect(LANCE_PATH);
  
  let table;
  try {
    table = await db.openTable(TABLE_NAME);
  } catch (e) {
    console.error('No index found. Run with --index first.');
    process.exit(1);
  }
  
  const queryEmbedding = await getEmbedding(query);
  if (!queryEmbedding) {
    console.error('Failed to get query embedding');
    process.exit(1);
  }
  
  const results = await table.search(queryEmbedding).limit(topK).toArray();
  
  console.log(`\n🔍 Search: "${query}"\n`);
  console.log('Results:\n');
  
  results.forEach((row, i) => {
    const similarity = row._distance ? (1 - row._distance).toFixed(3) : 'N/A';
    console.log(`--- ${row.source} (similarity: ${similarity}) ---`);
    console.log(row.text.length > 500 ? row.text.slice(0, 500) + '...' : row.text);
    console.log('');
  });
  
  return results;
}

// Show stats
async function showStats() {
  const db = await lancedb.connect(LANCE_PATH);
  
  try {
    const table = await db.openTable(TABLE_NAME);
    const count = await table.countRows();
    console.log(`\n📊 Memory Vector Index Stats`);
    console.log(`   Table: ${TABLE_NAME}`);
    console.log(`   Chunks indexed: ${count}`);
    console.log(`   Storage: ${LANCE_PATH}`);
    console.log(`   Embedding model: nomic-embed-text (local/free)`);
  } catch (e) {
    console.log('No index found. Run with --index first.');
  }
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--index')) {
    await indexMemories();
  } else if (args.includes('--search')) {
    const queryIndex = args.indexOf('--search') + 1;
    const query = args.slice(queryIndex).join(' ');
    if (!query) {
      console.error('Usage: node index.js --search "your query"');
      process.exit(1);
    }
    await searchMemories(query);
  } else if (args.includes('--stats')) {
    await showStats();
  } else {
    console.log('Memory Vector Search - Local Embeddings (100% Free)');
    console.log('');
    console.log('Usage:');
    console.log('  node index.js --index           Index all memory files');
    console.log('  node index.js --search "query"  Search for similar content');
    console.log('  node index.js --stats           Show index statistics');
  }
}

main().catch(console.error);
