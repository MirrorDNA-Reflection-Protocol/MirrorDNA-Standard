/**
 * MirrorDNA Portable Launcher - Integration Tests
 *
 * Tests for IPC handlers, vault operations, and LLM integration.
 * These tests verify the interaction between different components.
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

console.log(`${colors.cyan}⟡ MirrorDNA Launcher - Integration Tests${colors.reset}\n`);

// IPC Handler Tests
test('main.js imports required Electron modules', () => {
  const mainPath = path.join(__dirname, '..', 'src', 'main.js');
  const content = fs.readFileSync(mainPath, 'utf8');

  const requiredModules = ['app', 'BrowserWindow', 'ipcMain', 'Menu', 'dialog'];
  requiredModules.forEach(mod => {
    assert(
      content.includes(mod),
      `Required module ${mod} not imported`
    );
  });
});

test('main.js has directory selection handlers', () => {
  const mainPath = path.join(__dirname, '..', 'src', 'main.js');
  const content = fs.readFileSync(mainPath, 'utf8');

  assert(
    content.includes("'choose-directory'"),
    'choose-directory handler not found'
  );
  assert(
    content.includes("'choose-file'"),
    'choose-file handler not found'
  );
});

test('main.js has consent dialog implementation', () => {
  const mainPath = path.join(__dirname, '..', 'src', 'main.js');
  const content = fs.readFileSync(mainPath, 'utf8');

  assert(
    content.includes('dialog.showMessageBox'),
    'Consent dialog not implemented'
  );
  assert(
    content.includes('Internet Permission Request'),
    'Consent dialog message not found'
  );
});

test('preload.js exposes directory chooser API', () => {
  const preloadPath = path.join(__dirname, '..', 'src', 'preload.js');
  const content = fs.readFileSync(preloadPath, 'utf8');

  assert(
    content.includes('chooseDirectory:'),
    'chooseDirectory not exposed'
  );
  assert(
    content.includes('chooseFile:'),
    'chooseFile not exposed'
  );
});

// UI Integration Tests
test('app.js has vault selection handler', () => {
  const appPath = path.join(__dirname, '..', 'src', 'ui', 'app.js');
  const content = fs.readFileSync(appPath, 'utf8');

  assert(
    content.includes('loadExistingVault'),
    'loadExistingVault method not found'
  );
  assert(
    content.includes('btn-existing-user'),
    'existing user button handler not found'
  );
});

test('app.js has directory picker for vault path', () => {
  const appPath = path.join(__dirname, '..', 'src', 'ui', 'app.js');
  const content = fs.readFileSync(appPath, 'utf8');

  assert(
    content.includes('choose-path-btn'),
    'vault path chooser button not found'
  );
  assert(
    content.includes('chooseDirectory'),
    'chooseDirectory call not found'
  );
});

test('app.js has model file picker', () => {
  const appPath = path.join(__dirname, '..', 'src', 'ui', 'app.js');
  const content = fs.readFileSync(appPath, 'utf8');

  assert(
    content.includes('choose-model-btn'),
    'model chooser button handler not found'
  );
  assert(
    content.includes('chooseFile'),
    'chooseFile call not found'
  );
});

test('app.js has change vault button handler', () => {
  const appPath = path.join(__dirname, '..', 'src', 'ui', 'app.js');
  const content = fs.readFileSync(appPath, 'utf8');

  assert(
    content.includes('change-vault-btn'),
    'change vault button handler not found'
  );
});

// HTML/CSS Integration Tests
test('index.html has consent dialog markup', () => {
  const htmlPath = path.join(__dirname, '..', 'src', 'ui', 'index.html');
  const content = fs.readFileSync(htmlPath, 'utf8');

  assert(
    content.includes('consent-dialog'),
    'Consent dialog markup not found'
  );
  assert(
    content.includes('consent-allow-btn'),
    'Allow button not found'
  );
  assert(
    content.includes('consent-deny-btn'),
    'Deny button not found'
  );
});

test('index.html has model path settings', () => {
  const htmlPath = path.join(__dirname, '..', 'src', 'ui', 'index.html');
  const content = fs.readFileSync(htmlPath, 'utf8');

  assert(
    content.includes('choose-model-btn'),
    'Choose model button not found'
  );
  assert(
    content.includes('current-model-path'),
    'Model path display not found'
  );
});

test('styles.css has consent dialog styles', () => {
  const cssPath = path.join(__dirname, '..', 'src', 'ui', 'styles.css');
  const content = fs.readFileSync(cssPath, 'utf8');

  assert(
    content.includes('.consent-dialog') || content.includes('.dialog'),
    'Consent dialog styles not found'
  );
  assert(
    content.includes('.consent-btn'),
    'Consent button styles not found'
  );
});

// LLM Integration Tests
test('llm-bridge.js has modelPath tracking', () => {
  const llmPath = path.join(__dirname, '..', 'src', 'llm-bridge.js');
  const content = fs.readFileSync(llmPath, 'utf8');

  assert(
    content.includes('this.modelPath'),
    'modelPath property not tracked'
  );
});

test('LLM initialization stores modelPath', () => {
  const llmPath = path.join(__dirname, '..', 'src', 'llm-bridge.js');
  const content = fs.readFileSync(llmPath, 'utf8');

  // Check that modelPath is assigned during initialization
  assert(
    content.match(/this\.modelPath\s*=\s*modelPath/),
    'modelPath not assigned during initialization'
  );
});

test('getModelInfo returns modelPath', () => {
  const llmPath = path.join(__dirname, '..', 'src', 'llm-bridge.js');
  const content = fs.readFileSync(llmPath, 'utf8');

  // Check that getModelInfo method exists and returns modelPath
  assert(
    content.includes('getModelInfo()'),
    'getModelInfo method not found'
  );

  // Find the section that includes the return statement
  const lines = content.split('\n');
  let inMethod = false;
  let foundModelPath = false;
  let braceCount = 0;

  for (const line of lines) {
    if (line.includes('getModelInfo()')) {
      inMethod = true;
    }
    if (inMethod) {
      if (line.includes('{')) braceCount++;
      if (line.includes('modelPath:')) {
        foundModelPath = true;
        break;
      }
      if (line.includes('}')) {
        braceCount--;
        if (braceCount <= 0) break;
      }
    }
  }

  assert(foundModelPath, 'getModelInfo does not return modelPath');
});

// File Structure Tests
test('DEPLOYMENT.md exists', () => {
  const deployPath = path.join(__dirname, '..', '..', 'docs', 'DEPLOYMENT.md');
  assert(fs.existsSync(deployPath), 'DEPLOYMENT.md not found');
});

test('DEPLOYMENT.md has build instructions', () => {
  const deployPath = path.join(__dirname, '..', '..', 'docs', 'DEPLOYMENT.md');
  const content = fs.readFileSync(deployPath, 'utf8');

  assert(
    content.includes('npm run build'),
    'Build instructions not found'
  );
  assert(
    content.includes('electron-builder'),
    'Electron builder not mentioned'
  );
});

test('package.json has build scripts', () => {
  const pkgPath = path.join(__dirname, '..', 'package.json');
  const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));

  assert(pkg.scripts.build, 'build script not found');
  assert(pkg.scripts['build:win'], 'build:win script not found');
  assert(pkg.scripts['build:mac'], 'build:mac script not found');
  assert(pkg.scripts['build:linux'], 'build:linux script not found');
});

// Consent Flow Tests
test('main.js consent flow has proper branches', () => {
  const mainPath = path.join(__dirname, '..', 'src', 'main.js');
  const content = fs.readFileSync(mainPath, 'utf8');

  // Check for offline, hybrid, and online mode handling
  assert(
    content.includes("mode === 'offline_only'"),
    'Offline mode check not found'
  );
  assert(
    content.includes("mode === 'online'"),
    'Online mode check not found'
  );
  assert(
    content.includes('Hybrid mode'),
    'Hybrid mode handling not found'
  );
});

test('consent dialog returns proper structure', () => {
  const mainPath = path.join(__dirname, '..', 'src', 'main.js');
  const content = fs.readFileSync(mainPath, 'utf8');

  // Check that consent returns granted/reason/action
  assert(
    content.includes('granted:'),
    'granted property not returned'
  );
  assert(
    content.includes('reason:'),
    'reason property not returned'
  );
});

// Summary
console.log(`\n${colors.cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${colors.reset}`);
console.log(`${colors.green}Passed: ${passed}${colors.reset}`);
if (failed > 0) {
  console.log(`${colors.red}Failed: ${failed}${colors.reset}`);
  process.exit(1);
} else {
  console.log(`${colors.cyan}⟡ All integration tests passed!${colors.reset}`);
  process.exit(0);
}
