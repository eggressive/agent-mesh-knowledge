#!/usr/bin/env node
/**
 * Model Router - Lightweight task classifier and model switcher
 */

const fs = require('fs');
const path = require('path');

const CONFIG_PATH = path.join(__dirname, 'config.json');

// Load or create config
function loadConfig() {
  if (fs.existsSync(CONFIG_PATH)) {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  }
  return require('./skill.json').config;
}

// Hierarchical intent classification (Option C)
// Priority: explicit prefix > strong keywords > medium keywords > default
function classifyIntent(text, routes) {
  const lower = text.toLowerCase();
  
  // Strong keywords = single match routes to model
  const strongKeywords = {
    opus: ['architecture', 'security review', 'threat model', 'security audit', 'design system'],
    codex: ['debug this', 'fix this bug', 'refactor', 'implement function', 'write code']
  };
  
  // Medium keywords = need 2+ matches
  const mediumKeywords = {
    opus: ['design', 'complex', 'distributed', 'scale', 'optimize', 'evaluate', 'analyze'],
    codex: ['code', 'function', 'bug', 'review', 'implement', 'test'],
    kimi: ['research', 'find', 'search', 'latest', 'what is', 'how to', 'explain']
  };
  
  // Check strong keywords first (single match = route)
  for (const [model, keywords] of Object.entries(strongKeywords)) {
    if (keywords.some(k => lower.includes(k))) {
      return { intent: model, model, confidence: 0.9, reason: 'strong keyword match' };
    }
  }
  
  // Check medium keywords (2+ matches = route)
  let bestMatch = null;
  let bestScore = 0;
  
  for (const [model, keywords] of Object.entries(mediumKeywords)) {
    const matches = keywords.filter(k => lower.includes(k)).length;
    if (matches >= 2 && matches > bestScore) {
      bestScore = matches;
      bestMatch = { intent: model, model, confidence: matches / keywords.length, reason: `${matches} medium keywords` };
    }
  }
  
  return bestMatch;
}

// Map shorthand to full model aliases
const MODEL_MAP = {
  'code': 'codex',
  'research': 'kimi',
  'deep': 'opus',
  'fast': 'haiku',
  'cheap': 'kimi-free'
};

// Main router logic
function route(args) {
  const config = loadConfig();
  const task = args.task || args._[0];
  const hint = args.hint || args._[1];
  
  // Check for explicit prefix
  const prefixMatch = task?.match(/^\/(\w+)\s/);
  if (prefixMatch && MODEL_MAP[prefixMatch[1]]) {
    return {
      action: 'switch',
      model: MODEL_MAP[prefixMatch[1]],
      reason: `explicit /${prefixMatch[1]} prefix`
    };
  }
  
  // Auto-classify if enabled
  if (config.autoRoute && task) {
    const classification = classifyIntent(task, config.routes);
    if (classification) {
      return {
        action: 'switch',
        model: classification.model,
        reason: `${classification.intent} detected (${Math.round(classification.confidence * 100)}% confidence)`
      };
    }
  }
  
  // Stay on current
  return {
    action: 'continue',
    model: config.default,
    reason: 'no route match, using default'
  };
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const task = args.join(' ');
  
  const result = route({ task, _: args });
  console.log(JSON.stringify(result, null, 2));
}

module.exports = { route, classifyIntent, loadConfig };
