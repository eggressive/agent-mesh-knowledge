#!/usr/bin/env node
/**
 * Model Router Test Suite
 * Run: node tests/router.test.js
 */

const { route } = require('../router');

const testCases = [
  // Explicit prefixes (always win)
  { input: '/code review this', expected: 'codex', reason: 'explicit prefix' },
  { input: '/deep analyze architecture', expected: 'opus', reason: 'explicit prefix' },
  { input: '/research find latest papers', expected: 'kimi', reason: 'explicit prefix' },
  { input: '/fast quick question', expected: 'haiku', reason: 'explicit prefix' },
  { input: '/cheap low priority task', expected: 'kimi-free', reason: 'explicit prefix' },
  
  // Strong keywords (single match = route)
  { input: 'review the architecture', expected: 'opus', reason: 'strong keyword' },
  { input: 'perform security audit', expected: 'opus', reason: 'strong keyword' },
  { input: 'debug this function', expected: 'codex', reason: 'strong keyword' },
  { input: 'refactor this code', expected: 'codex', reason: 'strong keyword' },
  
  // Medium keywords (2+ matches = route)
  { input: 'design a distributed system', expected: 'opus', reason: 'medium keywords' },
  { input: 'review this code for bugs', expected: 'codex', reason: 'medium keywords' },
  { input: 'research and find latest info', expected: 'kimi', reason: 'medium keywords' },
  
  // Edge cases
  { input: '', expected: 'kimi', reason: 'empty → default' },
  { input: 'hello world', expected: 'kimi', reason: 'no match → default' },
  { input: 'DESIGN A DISTRIBUTED SYSTEM', expected: 'opus', reason: 'case insensitive + 2 keywords' },
  
  // Conflict resolution (opus > codex)
  { input: 'design the code architecture', expected: 'opus', reason: 'opus wins conflict' },
  
  // Single medium keyword (should NOT match)
  { input: 'design something', expected: 'kimi', reason: 'only 1 medium keyword' },
];

let passed = 0;
let failed = 0;

console.log('Running Model Router Tests\n');

testCases.forEach(({ input, expected, reason }) => {
  const result = route({ task: input, _: [input] });
  const pass = result.model === expected;
  
  if (pass) {
    passed++;
    console.log(`✅ "${input}" → ${result.model} [${reason}]`);
  } else {
    failed++;
    console.log(`❌ "${input}" → ${result.model} (expected: ${expected}) [${reason}]`);
  }
});

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
