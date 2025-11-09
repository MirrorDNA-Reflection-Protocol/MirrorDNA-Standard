const { app, BrowserWindow, ipcMain, Menu } = require('electron');
const path = require('path');
const fs = require('fs');
const Store = require('electron-store');
const MirrorDNALLM = require('./llm-bridge');
const SessionContinuity = require('./session-continuity');
const ModelDownloader = require('./model-downloader');
const { ConsentDialogManager } = require('./consent-dialog');
const { ChecksumVerifier } = require('./checksum-verifier');
const { ObsidianLauncher } = require('./obsidian-launcher');
const { ClaudeAPIBridge } = require('./claude-api-bridge');
const { GitSyncManager } = require('./git-sync-manager');
const { SessionManager } = require('./session-manager');

// Initialize persistent settings
const store = new Store({
  defaults: {
    vaultPath: null,
    internetMode: 'hybrid_ask', // 'offline_only' | 'hybrid_ask' | 'online'
    onboardingCompleted: false,
    windowBounds: { width: 1000, height: 700 },
    modelPath: null, // Path to LLM model file
    claudeApiKey: null, // Claude API key (encrypted in production)
    preferredMode: 'hybrid_ask' // User's preferred reflection mode
  }
});

let mainWindow;
let llm = new MirrorDNALLM();
let sessionContinuity = null;
let checksumVerifier = null;
let gitSyncManager = null;
let sessionManager = null;

// Initialize model downloader
const modelsPath = path.join(__dirname, '../models');
const modelDownloader = new ModelDownloader(modelsPath);

// Forward download events to renderer
modelDownloader.on('download-progress', (data) => {
  if (mainWindow) {
    mainWindow.webContents.send('model-download-progress', data);
  }
});

modelDownloader.on('download-complete', (data) => {
  if (mainWindow) {
    mainWindow.webContents.send('model-download-complete', data);
  }
});

modelDownloader.on('download-error', (data) => {
  if (mainWindow) {
    mainWindow.webContents.send('model-download-error', data);
  }
});

modelDownloader.on('download-cancelled', (data) => {
  if (mainWindow) {
    mainWindow.webContents.send('model-download-cancelled', data);
  }
});

// Initialize consent dialog manager
const userDataPath = app.getPath('userData');
const consentManager = new ConsentDialogManager({ userDataPath });

// Forward consent prompt events to renderer
// (Prompts are handled synchronously through IPC, so no events needed)

// Initialize Obsidian launcher
const obsidianLauncher = new ObsidianLauncher();

// Initialize Claude API bridge
const claudeAPI = new ClaudeAPIBridge();

// Load Claude API key if available
const savedApiKey = store.get('claudeApiKey');
if (savedApiKey) {
  try {
    claudeAPI.setApiKey(savedApiKey);
  } catch (error) {
    console.warn('Saved API key is invalid:', error.message);
  }
}

// Forward Claude API streaming events to renderer
claudeAPI.on('stream-start', (data) => {
  if (mainWindow) {
    mainWindow.webContents.send('claude-stream-start', data);
  }
});

claudeAPI.on('stream-chunk', (data) => {
  if (mainWindow) {
    mainWindow.webContents.send('claude-stream-chunk', data);
  }
});

claudeAPI.on('stream-end', (data) => {
  if (mainWindow) {
    mainWindow.webContents.send('claude-stream-end', data);
  }
});

claudeAPI.on('stream-error', (data) => {
  if (mainWindow) {
    mainWindow.webContents.send('claude-stream-error', data);
  }
});

function createWindow() {
  const { width, height } = store.get('windowBounds');

  mainWindow = new BrowserWindow({
    width,
    height,
    minWidth: 800,
    minHeight: 600,
    icon: path.join(__dirname, '../../glyphs/mirrordna-sigil.png'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    titleBarStyle: 'hidden',
    backgroundColor: '#1e1e1e',
    show: false // Show after ready
  });

  mainWindow.loadFile(path.join(__dirname, 'ui/index.html'));

  // Show window when ready (prevents flash)
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Save window bounds on close
  mainWindow.on('close', () => {
    store.set('windowBounds', mainWindow.getBounds());
  });

  // Development mode
  if (process.argv.includes('--dev')) {
    mainWindow.webContents.openDevTools();
  }

  // Remove default menu in production
  if (!process.argv.includes('--dev')) {
    Menu.setApplicationMenu(null);
  }
}

app.whenReady().then(async () => {
  // Initialize consent manager
  await consentManager.initialize();
  await consentManager.clearSessionConsents(); // Clear session-only consents on restart

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', async () => {
  // Cleanup LLM resources
  if (llm) {
    await llm.dispose();
  }
});

// IPC Handlers

// Get app path (for accessing vault template, etc.)
ipcMain.handle('get-app-path', () => {
  return app.getAppPath();
});

// Get user settings
ipcMain.handle('get-settings', () => {
  return {
    vaultPath: store.get('vaultPath'),
    internetMode: store.get('internetMode'),
    onboardingCompleted: store.get('onboardingCompleted')
  };
});

// Update settings
ipcMain.handle('update-settings', (event, settings) => {
  Object.keys(settings).forEach(key => {
    store.set(key, settings[key]);
  });
  return true;
});

// Initialize vault (copy template to user location)
ipcMain.handle('init-vault', async (event, vaultName, targetPath) => {
  try {
    const templatePath = path.join(app.getAppPath(), '../vault-template');
    const vaultPath = path.join(targetPath, vaultName);

    // Copy vault template
    await fs.promises.cp(templatePath, vaultPath, { recursive: true });

    // Update vault state with name
    const statePath = path.join(vaultPath, 'state/current.json');
    const state = JSON.parse(await fs.promises.readFile(statePath, 'utf8'));
    state.vault_name = vaultName;
    await fs.promises.writeFile(statePath, JSON.stringify(state, null, 2));

    // Save vault path
    store.set('vaultPath', vaultPath);
    store.set('onboardingCompleted', true);

    return { success: true, vaultPath };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Read vault state
ipcMain.handle('read-vault-state', async () => {
  try {
    const vaultPath = store.get('vaultPath');
    if (!vaultPath) {
      return { success: false, error: 'No vault configured' };
    }

    const statePath = path.join(vaultPath, 'state/current.json');
    const state = JSON.parse(await fs.promises.readFile(statePath, 'utf8'));

    return { success: true, state };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Write session to vault
ipcMain.handle('write-session', async (event, dialogue) => {
  try {
    const vaultPath = store.get('vaultPath');
    const statePath = path.join(vaultPath, 'state/current.json');
    const state = JSON.parse(await fs.promises.readFile(statePath, 'utf8'));

    const sessionNumber = (state.last_session?.number || 0) + 1;
    const timestamp = new Date().toISOString();
    const date = timestamp.split('T')[0];
    const filename = `${date}_session_${String(sessionNumber).padStart(3, '0')}.md`;

    // Load template
    const templatePath = path.join(vaultPath, 'templates/new-session.md');
    let template = await fs.promises.readFile(templatePath, 'utf8');

    // Replace placeholders
    template = template
      .replace(/\{\{session_number\}\}/g, sessionNumber)
      .replace(/\{\{date\}\}/g, date)
      .replace(/\{\{iso_timestamp\}\}/g, timestamp)
      .replace(/\{\{vault_name\}\}/g, state.vault_name)
      .replace(/\{\{predecessor_path\}\}/g, state.last_session?.path || 'none')
      .replace(/\{\{previous_context\}\}/g, JSON.stringify(state.context, null, 2));

    // Add dialogue
    template = template.replace('⟡ Ready when you are.', dialogue);

    // Write session file
    const sessionPath = path.join(vaultPath, 'sessions', filename);
    await fs.promises.writeFile(sessionPath, template);

    // Update state
    state.last_session = {
      number: sessionNumber,
      path: `sessions/${filename}`,
      timestamp
    };

    await fs.promises.writeFile(statePath, JSON.stringify(state, null, 2));

    return { success: true, sessionPath: `sessions/${filename}` };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Request internet permission
ipcMain.handle('request-internet', async (event, action, details) => {
  const mode = store.get('internetMode');

  if (mode === 'offline_only') {
    return { granted: false, reason: 'offline_only' };
  }

  if (mode === 'online') {
    return { granted: true, reason: 'always_online' };
  }

  // Hybrid mode: show dialog
  // TODO: Implement consent dialog
  // For now, auto-grant in hybrid mode
  return { granted: true, reason: 'hybrid_ask' };
});

// LLM Operations

// Initialize LLM with model and vault
ipcMain.handle('init-llm', async (event, modelPath, vaultPath) => {
  try {
    console.log('⟡ Initializing LLM via IPC...');

    // Use stored paths if not provided
    if (!modelPath) {
      modelPath = store.get('modelPath');
    }
    if (!vaultPath) {
      vaultPath = store.get('vaultPath');
    }

    if (!modelPath || !vaultPath) {
      return {
        success: false,
        error: 'Model path or vault path not configured'
      };
    }

    // Initialize LLM
    const result = await llm.initialize(modelPath, vaultPath);

    if (result.success) {
      // Save model path for future sessions
      store.set('modelPath', modelPath);
    }

    return result;
  } catch (error) {
    console.error('Error initializing LLM:', error);
    return { success: false, error: error.message };
  }
});

// Generate reflection response
ipcMain.handle('generate-reflection', async (event, prompt) => {
  try {
    if (!llm.isInitialized) {
      return {
        success: false,
        error: 'LLM not initialized. Please initialize first.'
      };
    }

    console.log('⟡ Generating reflection via IPC...');
    const response = await llm.generate(prompt);

    return { success: true, response };
  } catch (error) {
    console.error('Error generating reflection:', error);
    return { success: false, error: error.message };
  }
});

// Get LLM model info
ipcMain.handle('get-llm-info', () => {
  return llm.getModelInfo();
});

// Update LLM session context
ipcMain.handle('update-llm-context', (event, contextUpdate) => {
  if (llm.isInitialized) {
    llm.updateContext(contextUpdate);
    return { success: true };
  }
  return { success: false, error: 'LLM not initialized' };
});

// ===== Session Continuity Operations =====

// Initialize session continuity engine
ipcMain.handle('init-session-continuity', async () => {
  try {
    const vaultPath = store.get('vaultPath');
    if (!vaultPath) {
      return { success: false, error: 'No vault configured' };
    }

    sessionContinuity = new SessionContinuity(vaultPath);
    const result = await sessionContinuity.initialize();

    return result;
  } catch (error) {
    console.error('Session continuity initialization failed:', error);
    return { success: false, error: error.message };
  }
});

// Create new session
ipcMain.handle('create-session', async (event, options) => {
  if (!sessionContinuity) {
    return { success: false, error: 'Session continuity not initialized' };
  }

  return await sessionContinuity.createSession(options);
});

// Restore session by path
ipcMain.handle('restore-session', async (event, sessionPath) => {
  if (!sessionContinuity) {
    return { success: false, error: 'Session continuity not initialized' };
  }

  return await sessionContinuity.restoreSession(sessionPath);
});

// Get session history with filters
ipcMain.handle('get-session-history', (event, filters) => {
  if (!sessionContinuity) {
    return { success: false, error: 'Session continuity not initialized' };
  }

  try {
    const history = sessionContinuity.getHistory(filters);
    return { success: true, history };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Navigate to previous session
ipcMain.handle('navigate-to-previous-session', async () => {
  if (!sessionContinuity) {
    return { success: false, error: 'Session continuity not initialized' };
  }

  return await sessionContinuity.navigateToPrevious();
});

// Navigate to next session
ipcMain.handle('navigate-to-next-session', async () => {
  if (!sessionContinuity) {
    return { success: false, error: 'Session continuity not initialized' };
  }

  return await sessionContinuity.navigateToNext();
});

// Export sessions
ipcMain.handle('export-sessions', async (event, options) => {
  if (!sessionContinuity) {
    return { success: false, error: 'Session continuity not initialized' };
  }

  return await sessionContinuity.exportSessions(options);
});

// Import sessions
ipcMain.handle('import-sessions', async (event, importData) => {
  if (!sessionContinuity) {
    return { success: false, error: 'Session continuity not initialized' };
  }

  return await sessionContinuity.importSessions(importData);
});

// Get current session info
ipcMain.handle('get-current-session', () => {
  if (!sessionContinuity) {
    return { success: false, error: 'Session continuity not initialized' };
  }

  try {
    const session = sessionContinuity.getCurrentSession();
    return { success: true, session };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get session statistics
ipcMain.handle('get-session-statistics', () => {
  if (!sessionContinuity) {
    return { success: false, error: 'Session continuity not initialized' };
  }

  try {
    const stats = sessionContinuity.getStatistics();
    return { success: true, stats };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Update session context
ipcMain.handle('update-session-context', async (event, updates) => {
  if (!sessionContinuity) {
    return { success: false, error: 'Session continuity not initialized' };
  }

  return await sessionContinuity.updateContext(updates);
});

// Validate vault integrity
ipcMain.handle('validate-vault-integrity', async () => {
  if (!sessionContinuity) {
    return { success: false, error: 'Session continuity not initialized' };
  }

  return await sessionContinuity.validateIntegrity();
});

// ===== Model Downloader Operations =====

// Get available models from registry
ipcMain.handle('get-available-models', () => {
  try {
    const models = modelDownloader.getAvailableModels();
    return { success: true, models };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get installed models
ipcMain.handle('get-installed-models', () => {
  try {
    const models = modelDownloader.getInstalledModels();
    return { success: true, models };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Download a model
ipcMain.handle('download-model', async (event, modelId, options) => {
  try {
    const result = await modelDownloader.downloadModel(modelId, options);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Cancel a download
ipcMain.handle('cancel-download', (event, modelId) => {
  return modelDownloader.cancelDownload(modelId);
});

// Delete a model
ipcMain.handle('delete-model', (event, filename) => {
  return modelDownloader.deleteModel(filename);
});

// Verify model checksum
ipcMain.handle('verify-model', async (event, filename, expectedChecksum) => {
  return await modelDownloader.verifyModel(filename, expectedChecksum);
});

// Get active downloads
ipcMain.handle('get-active-downloads', () => {
  try {
    const downloads = modelDownloader.getActiveDownloads();
    return { success: true, downloads };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// ===== Consent Dialog Operations =====

// Request consent for an operation
ipcMain.handle('request-consent', async (event, request) => {
  try {
    const result = await consentManager.requestConsent(request);
    return { success: true, ...result };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Respond to a consent prompt
ipcMain.handle('respond-to-consent', async (event, promptId, granted, duration) => {
  try {
    const consent = await consentManager.respondToPrompt(promptId, granted, duration);
    return { success: true, consent };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get all consents
ipcMain.handle('get-all-consents', () => {
  try {
    const consents = consentManager.getAllConsents();
    return { success: true, consents };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Revoke specific consent
ipcMain.handle('revoke-consent', async (event, consentKey) => {
  try {
    const result = await consentManager.revokeConsent(consentKey);
    return { success: true, ...result };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Revoke consents by type
ipcMain.handle('revoke-consents-by-type', async (event, type) => {
  try {
    const result = await consentManager.revokeConsentsByType(type);
    return { success: true, ...result };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Clear all consents
ipcMain.handle('clear-all-consents', async () => {
  try {
    const result = await consentManager.clearAllConsents();
    return { success: true, ...result };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get consent statistics
ipcMain.handle('get-consent-stats', () => {
  try {
    const stats = consentManager.getConsentStats();
    return { success: true, stats };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Export consents
ipcMain.handle('export-consents', async () => {
  try {
    const data = await consentManager.exportConsents();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Import consents
ipcMain.handle('import-consents', async (event, data, merge) => {
  try {
    const result = await consentManager.importConsents(data, merge);
    return { success: true, ...result };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get pending prompts
ipcMain.handle('get-pending-prompts', () => {
  try {
    const prompts = consentManager.getPendingPrompts();
    return { success: true, prompts };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// ===== Checksum Verification Operations =====

// Initialize checksum verifier (or get existing instance)
const getChecksumVerifier = () => {
  const vaultPath = store.get('vaultPath');
  if (!vaultPath) {
    throw new Error('No vault configured');
  }

  if (!checksumVerifier || checksumVerifier.vaultPath !== vaultPath) {
    checksumVerifier = new ChecksumVerifier(vaultPath);
  }

  return checksumVerifier;
};

// Verify single file
ipcMain.handle('verify-file-checksum', async (event, filePath, expectedChecksum) => {
  try {
    const verifier = getChecksumVerifier();
    const result = await verifier.verifyFile(filePath, expectedChecksum);
    return { success: true, ...result };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Verify entire vault
ipcMain.handle('verify-vault-checksums', async (event, options) => {
  try {
    const verifier = getChecksumVerifier();
    const result = await verifier.verifyVault(options);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Verify specific sessions
ipcMain.handle('verify-sessions-checksums', async (event, sessionPaths) => {
  try {
    const verifier = getChecksumVerifier();
    const result = await verifier.verifySessions(sessionPaths);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Update checksum for a file
ipcMain.handle('update-file-checksum', async (event, filePath) => {
  try {
    const verifier = getChecksumVerifier();
    const result = await verifier.updateChecksum(filePath);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Batch update checksums
ipcMain.handle('batch-update-checksums', async (event, filePaths) => {
  try {
    const verifier = getChecksumVerifier();
    const result = await verifier.batchUpdateChecksums(filePaths);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get verification cache
ipcMain.handle('get-verification-cache', () => {
  try {
    if (!checksumVerifier) {
      return { success: true, cache: [] };
    }
    const cache = checksumVerifier.getCache();
    return { success: true, cache };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Clear verification cache
ipcMain.handle('clear-verification-cache', () => {
  try {
    if (checksumVerifier) {
      checksumVerifier.clearCache();
    }
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Generate verification report
ipcMain.handle('generate-verification-report', async (event, results) => {
  try {
    const verifier = getChecksumVerifier();
    const report = verifier.generateReport(results);
    return { success: true, report };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// ===== Obsidian Launcher Operations =====

// Launch Obsidian with vault
ipcMain.handle('launch-obsidian', async (event, vaultPath, options) => {
  try {
    // Use configured vault if no path provided
    if (!vaultPath) {
      vaultPath = store.get('vaultPath');
    }

    if (!vaultPath) {
      return { success: false, error: 'No vault configured' };
    }

    const result = await obsidianLauncher.launchVault(vaultPath, options);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Open specific file in Obsidian
ipcMain.handle('open-file-in-obsidian', async (event, filePath) => {
  try {
    const vaultPath = store.get('vaultPath');
    if (!vaultPath) {
      return { success: false, error: 'No vault configured' };
    }

    const result = await obsidianLauncher.openFile(vaultPath, filePath);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Check Obsidian installation
ipcMain.handle('check-obsidian-installation', async () => {
  try {
    const result = await obsidianLauncher.checkInstallation();
    return { success: true, ...result };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// ===== Claude API Bridge Operations =====

// Set Claude API key
ipcMain.handle('set-claude-api-key', async (event, apiKey) => {
  try {
    claudeAPI.setApiKey(apiKey);
    store.set('claudeApiKey', apiKey);
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get Claude API key status
ipcMain.handle('get-claude-api-key-status', () => {
  return {
    success: true,
    hasKey: claudeAPI.hasApiKey(),
    keyPrefix: claudeAPI.hasApiKey() ? 'sk-ant-***' : null
  };
});

// Test Claude API connection
ipcMain.handle('test-claude-connection', async () => {
  try {
    const result = await claudeAPI.testConnection();
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Generate reflection with Claude (with consent)
ipcMain.handle('generate-claude-reflection', async (event, prompt, context, options) => {
  try {
    const internetMode = store.get('internetMode');

    // Check if user allows cloud access
    if (internetMode === 'offline_only') {
      return {
        success: false,
        error: 'Cloud mode disabled. Switch to hybrid or online mode.',
        fallbackToLocal: true
      };
    }

    // Request consent if in hybrid mode
    if (internetMode === 'hybrid_ask') {
      const consentResult = await consentManager.requestConsent({
        type: 'external_api',
        purpose: 'Generate reflection using Claude API',
        url: 'https://api.anthropic.com',
        duration: 'session'
      });

      if (consentResult.requiresPrompt) {
        return {
          success: false,
          requiresConsent: true,
          promptId: consentResult.promptId,
          prompt: consentResult.prompt
        };
      }

      if (!consentResult.granted) {
        return {
          success: false,
          error: 'API access denied by user',
          fallbackToLocal: true
        };
      }
    }

    // Generate reflection with Claude
    const result = await claudeAPI.generateReflection(prompt, context, options);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Generate streaming reflection with Claude (with consent)
ipcMain.handle('generate-claude-reflection-stream', async (event, prompt, context, options) => {
  try {
    const internetMode = store.get('internetMode');

    // Check if user allows cloud access
    if (internetMode === 'offline_only') {
      return {
        success: false,
        error: 'Cloud mode disabled. Switch to hybrid or online mode.',
        fallbackToLocal: true
      };
    }

    // Request consent if in hybrid mode
    if (internetMode === 'hybrid_ask') {
      const consentResult = await consentManager.requestConsent({
        type: 'external_api',
        purpose: 'Generate reflection using Claude API (streaming)',
        url: 'https://api.anthropic.com',
        duration: 'session'
      });

      if (consentResult.requiresPrompt) {
        return {
          success: false,
          requiresConsent: true,
          promptId: consentResult.promptId,
          prompt: consentResult.prompt
        };
      }

      if (!consentResult.granted) {
        return {
          success: false,
          error: 'API access denied by user',
          fallbackToLocal: true
        };
      }
    }

    // Start streaming
    await claudeAPI.generateReflectionStream(prompt, context, options);
    return { success: true, streaming: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get Claude API statistics
ipcMain.handle('get-claude-stats', () => {
  try {
    const stats = claudeAPI.getStats();
    return { success: true, stats };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Reset Claude API statistics
ipcMain.handle('reset-claude-stats', () => {
  try {
    claudeAPI.resetStats();
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Remove Claude API key
ipcMain.handle('remove-claude-api-key', () => {
  try {
    claudeAPI.apiKey = null;
    store.set('claudeApiKey', null);
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Set internet mode
ipcMain.handle('set-internet-mode', (event, mode) => {
  try {
    if (!['offline_only', 'hybrid_ask', 'online'].includes(mode)) {
      return { success: false, error: 'Invalid mode' };
    }

    store.set('internetMode', mode);
    return { success: true, mode };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get internet mode
ipcMain.handle('get-internet-mode', () => {
  try {
    const mode = store.get('internetMode');
    return { success: true, mode };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// ===== Git Sync Manager Operations =====

// Initialize Git sync manager
const getGitSyncManager = () => {
  const vaultPath = store.get('vaultPath');
  if (!vaultPath) throw new Error('No vault configured');
  if (!gitSyncManager || gitSyncManager.vaultPath !== vaultPath) {
    gitSyncManager = new GitSyncManager(vaultPath);
  }
  return gitSyncManager;
};

// Initialize repository
ipcMain.handle('git-init', async (event, options) => {
  try {
    const manager = getGitSyncManager();
    const result = await manager.initRepository(options);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Set remote
ipcMain.handle('git-set-remote', async (event, url, name) => {
  try {
    const manager = getGitSyncManager();
    const result = await manager.setRemote(url, name);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get status
ipcMain.handle('git-status', async () => {
  try {
    const manager = getGitSyncManager();
    const result = await manager.getStatus();
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Commit changes
ipcMain.handle('git-commit', async (event, message, options) => {
  try {
    const manager = getGitSyncManager();
    const result = await manager.commit(message, options);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Push to remote
ipcMain.handle('git-push', async (event, options) => {
  try {
    const manager = getGitSyncManager();
    const result = await manager.push(options);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Pull from remote
ipcMain.handle('git-pull', async (event, options) => {
  try {
    const manager = getGitSyncManager();
    const result = await manager.pull(options);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Full sync (commit + pull + push)
ipcMain.handle('git-sync', async (event, commitMessage, options) => {
  try {
    const manager = getGitSyncManager();
    const result = await manager.sync(commitMessage, options);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get commit history
ipcMain.handle('git-history', async (event, limit) => {
  try {
    const manager = getGitSyncManager();
    const result = await manager.getHistory(limit);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// ===== Session Manager Operations =====

// Initialize session manager
const getSessionManager = () => {
  const vaultPath = store.get('vaultPath');
  if (!vaultPath) throw new Error('No vault configured');
  if (!sessionManager || sessionManager.vaultPath !== vaultPath) {
    sessionManager = new SessionManager(vaultPath);
  }
  return sessionManager;
};

// Initialize session manager
ipcMain.handle('session-manager-init', async () => {
  try {
    const manager = getSessionManager();
    const result = await manager.initialize();
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Pause session
ipcMain.handle('pause-session', async (event, sessionData, options) => {
  try {
    const manager = getSessionManager();
    const result = await manager.pauseSession(sessionData, options);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Resume session
ipcMain.handle('resume-session', async (event, pauseId) => {
  try {
    const manager = getSessionManager();
    const result = await manager.resumeSession(pauseId);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Get paused sessions
ipcMain.handle('get-paused-sessions', async () => {
  try {
    const manager = getSessionManager();
    const result = await manager.getPausedSessions();
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Delete paused session
ipcMain.handle('delete-paused-session', async (event, pauseId) => {
  try {
    const manager = getSessionManager();
    const result = await manager.deletePausedSession(pauseId);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Auto-save session
ipcMain.handle('auto-save-session', async (event, sessionData) => {
  try {
    const manager = getSessionManager();
    const result = await manager.autoSaveSession(sessionData);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Load checkpoint
ipcMain.handle('load-checkpoint', async () => {
  try {
    const manager = getSessionManager();
    const result = await manager.loadCheckpoint();
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Clean old paused sessions
ipcMain.handle('clean-old-paused-sessions', async (event, maxAge) => {
  try {
    const manager = getSessionManager();
    const result = await manager.cleanOldPausedSessions(maxAge);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

console.log('⟡ MirrorDNA Portable launcher initialized');
