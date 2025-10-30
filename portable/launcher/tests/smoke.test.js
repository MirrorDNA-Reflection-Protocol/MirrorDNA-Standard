/**
 * MirrorDNA Portable Launcher - Smoke Tests
 *
 * Basic validation tests that don't require dependencies to be installed.
 * These tests verify file structure, code syntax, and basic logic.
 */

const fs = require('fs');
const path = require('path');

// ANSI colors for output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m'
};

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`${colors.green}✓${colors.reset} ${name}`);
    passed++;
  } catch (error) {
    console.log(`${colors.red}✗${colors.reset} ${name}`);
    console.log(`  ${colors.red}${error.message}${colors.reset}`);
    failed++;
  }
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message || 'Assertion failed');
  }
}

console.log(`${colors.cyan}⟡ MirrorDNA Launcher - Smoke Tests${colors.reset}\n`);

// File structure tests
test('package.json exists', () => {
  const pkgPath = path.join(__dirname, '..', 'package.json');
  assert(fs.existsSync(pkgPath), 'package.json not found');
});

test('package.json is valid JSON', () => {
  const pkgPath = path.join(__dirname, '..', 'package.json');
  const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
  assert(pkg.name === 'mirrordna-portable', 'package name incorrect');
  assert(pkg.version, 'version missing');
});

test('main.js exists', () => {
  const mainPath = path.join(__dirname, '..', 'src', 'main.js');
  assert(fs.existsSync(mainPath), 'main.js not found');
});

test('preload.js exists', () => {
  const preloadPath = path.join(__dirname, '..', 'src', 'preload.js');
  assert(fs.existsSync(preloadPath), 'preload.js not found');
});

test('llm-bridge.js exists', () => {
  const llmPath = path.join(__dirname, '..', 'src', 'llm-bridge.js');
  assert(fs.existsSync(llmPath), 'llm-bridge.js not found');
});

test('app.js exists', () => {
  const appPath = path.join(__dirname, '..', 'src', 'ui', 'app.js');
  assert(fs.existsSync(appPath), 'app.js not found');
});

test('index.html exists', () => {
  const htmlPath = path.join(__dirname, '..', 'src', 'ui', 'index.html');
  assert(fs.existsSync(htmlPath), 'index.html not found');
});

test('models directory exists', () => {
  const modelsPath = path.join(__dirname, '..', 'models');
  assert(fs.existsSync(modelsPath), 'models directory not found');
});

test('models README exists', () => {
  const readmePath = path.join(__dirname, '..', 'models', 'README.md');
  assert(fs.existsSync(readmePath), 'models/README.md not found');
});

// Code structure tests
test('llm-bridge.js exports MirrorDNALLM class', () => {
  const llmPath = path.join(__dirname, '..', 'src', 'llm-bridge.js');
  const content = fs.readFileSync(llmPath, 'utf8');
  assert(content.includes('class MirrorDNALLM'), 'MirrorDNALLM class not found');
  assert(content.includes('module.exports = MirrorDNALLM'), 'module.exports missing');
});

test('llm-bridge.js has required methods', () => {
  const llmPath = path.join(__dirname, '..', 'src', 'llm-bridge.js');
  const content = fs.readFileSync(llmPath, 'utf8');

  const requiredMethods = [
    'initialize',
    'loadVaultContext',
    'injectMasterCitation',
    'generate',
    'updateContext',
    'dispose',
    'getModelInfo'
  ];

  requiredMethods.forEach(method => {
    assert(
      content.includes(`async ${method}(`) || content.includes(`${method}(`),
      `Method ${method} not found`
    );
  });
});

test('llm-bridge.js has proper error handling', () => {
  const llmPath = path.join(__dirname, '..', 'src', 'llm-bridge.js');
  const content = fs.readFileSync(llmPath, 'utf8');
  assert(content.includes('try {'), 'No try-catch blocks found');
  assert(content.includes('catch (error)'), 'No error catching found');
});

test('main.js has IPC handlers for LLM', () => {
  const mainPath = path.join(__dirname, '..', 'src', 'main.js');
  const content = fs.readFileSync(mainPath, 'utf8');

  const requiredHandlers = [
    'init-llm',
    'generate-reflection',
    'get-llm-info',
    'update-llm-context'
  ];

  requiredHandlers.forEach(handler => {
    assert(
      content.includes(`'${handler}'`),
      `IPC handler ${handler} not found`
    );
  });
});

test('preload.js exposes LLM API', () => {
  const preloadPath = path.join(__dirname, '..', 'src', 'preload.js');
  const content = fs.readFileSync(preloadPath, 'utf8');

  const requiredMethods = ['initLLM', 'generateReflection', 'getLLMInfo', 'updateLLMContext'];

  requiredMethods.forEach(method => {
    assert(
      content.includes(`${method}:`),
      `Preload method ${method} not exposed`
    );
  });
});

test('app.js has LLM initialization', () => {
  const appPath = path.join(__dirname, '..', 'src', 'ui', 'app.js');
  const content = fs.readFileSync(appPath, 'utf8');
  assert(content.includes('initializeLLM'), 'initializeLLM method not found');
  assert(content.includes('generateReflection'), 'generateReflection method not found');
  assert(content.includes('generatePlaceholderResponse'), 'generatePlaceholderResponse method not found');
});

test('app.js has proper fallback behavior', () => {
  const appPath = path.join(__dirname, '..', 'src', 'ui', 'app.js');
  const content = fs.readFileSync(appPath, 'utf8');
  assert(
    content.includes('generatePlaceholderResponse'),
    'Fallback behavior not implemented'
  );
});

test('No stale TODO for LLM integration', () => {
  const appPath = path.join(__dirname, '..', 'src', 'ui', 'app.js');
  const content = fs.readFileSync(appPath, 'utf8');
  assert(
    !content.includes('TODO: Implement actual LLM integration'),
    'Stale TODO comment found - LLM is already integrated'
  );
});

test('Master Citation injection is implemented', () => {
  const llmPath = path.join(__dirname, '..', 'src', 'llm-bridge.js');
  const content = fs.readFileSync(llmPath, 'utf8');
  assert(
    content.includes('injectMasterCitation'),
    'Master Citation injection not implemented'
  );
  assert(
    content.includes('00_MASTER_CITATION.md'),
    'Master Citation file reference not found'
  );
});

test('Session state continuity is implemented', () => {
  const llmPath = path.join(__dirname, '..', 'src', 'llm-bridge.js');
  const content = fs.readFileSync(llmPath, 'utf8');
  assert(
    content.includes('current.json'),
    'Session state file reference not found'
  );
  assert(
    content.includes('sessionState'),
    'Session state tracking not implemented'
  );
});

test('GlyphSig symbols are used', () => {
  const llmPath = path.join(__dirname, '..', 'src', 'llm-bridge.js');
  const content = fs.readFileSync(llmPath, 'utf8');
  assert(
    content.includes('⟡'),
    'GlyphSig symbol ⟡ not used in LLM bridge'
  );
});

// Summary
console.log(`\n${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
console.log(`${colors.green}Passed: ${passed}${colors.reset}`);
if (failed > 0) {
  console.log(`${colors.red}Failed: ${failed}${colors.reset}`);
  process.exit(1);
} else {
  console.log(`${colors.cyan}⟡ All smoke tests passed!${colors.reset}`);
  process.exit(0);
}
