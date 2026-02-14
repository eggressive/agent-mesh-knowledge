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

// Simple intent classification
function classifyIntent(text, routes) {
  const lower = text.toLowerCase();
  
  // Score each route, pick best match above minimum threshold
  let bestMatch = null;
  let bestScore = 0;
  
  for (const [intent, config] of Object.entries(routes)) {
    const matches = config.patterns.filter(p => lower.includes(p)).length;
    // Use absolute match count, not percentage
    // threshold now means "minimum matches required"
    if (matches >= (config.minMatches || 1) && matches > bestScore) {
      bestScore = matches;
      bestMatch = { intent, model: config.model, confidence: matches / config.patterns.length, matches };
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
