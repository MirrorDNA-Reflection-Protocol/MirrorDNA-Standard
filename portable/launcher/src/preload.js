const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods to renderer process
contextBridge.exposeInMainWorld('mirrorDNA', {
  // Settings
  getSettings: () => ipcRenderer.invoke('get-settings'),
  updateSettings: (settings) => ipcRenderer.invoke('update-settings', settings),

  // Vault operations
  initVault: (vaultName, targetPath) => ipcRenderer.invoke('init-vault', vaultName, targetPath),
  readVaultState: () => ipcRenderer.invoke('read-vault-state'),
  writeSession: (dialogue) => ipcRenderer.invoke('write-session', dialogue),

  // LLM operations
  initLLM: (modelPath, vaultPath) => ipcRenderer.invoke('init-llm', modelPath, vaultPath),
  generateReflection: (prompt) => ipcRenderer.invoke('generate-reflection', prompt),
  getLLMInfo: () => ipcRenderer.invoke('get-llm-info'),
  updateLLMContext: (contextUpdate) => ipcRenderer.invoke('update-llm-context', contextUpdate),

  // Internet consent
  requestInternet: (action, details) => ipcRenderer.invoke('request-internet', action, details),

  // Session Continuity operations
  initSessionContinuity: () => ipcRenderer.invoke('init-session-continuity'),
  createSession: (options) => ipcRenderer.invoke('create-session', options),
  restoreSession: (sessionPath) => ipcRenderer.invoke('restore-session', sessionPath),
  getSessionHistory: (filters) => ipcRenderer.invoke('get-session-history', filters),
  navigateToPreviousSession: () => ipcRenderer.invoke('navigate-to-previous-session'),
  navigateToNextSession: () => ipcRenderer.invoke('navigate-to-next-session'),
  exportSessions: (options) => ipcRenderer.invoke('export-sessions', options),
  importSessions: (importData) => ipcRenderer.invoke('import-sessions', importData),
  getCurrentSession: () => ipcRenderer.invoke('get-current-session'),
  getSessionStatistics: () => ipcRenderer.invoke('get-session-statistics'),
  updateSessionContext: (updates) => ipcRenderer.invoke('update-session-context', updates),
  validateVaultIntegrity: () => ipcRenderer.invoke('validate-vault-integrity'),

  // Model Downloader operations
  getAvailableModels: () => ipcRenderer.invoke('get-available-models'),
  getInstalledModels: () => ipcRenderer.invoke('get-installed-models'),
  downloadModel: (modelId, options) => ipcRenderer.invoke('download-model', modelId, options),
  cancelDownload: (modelId) => ipcRenderer.invoke('cancel-download', modelId),
  deleteModel: (filename) => ipcRenderer.invoke('delete-model', filename),
  verifyModel: (filename, expectedChecksum) => ipcRenderer.invoke('verify-model', filename, expectedChecksum),
  getActiveDownloads: () => ipcRenderer.invoke('get-active-downloads'),

  // Model download event listeners
  onDownloadProgress: (callback) => ipcRenderer.on('model-download-progress', (event, data) => callback(data)),
  onDownloadComplete: (callback) => ipcRenderer.on('model-download-complete', (event, data) => callback(data)),
  onDownloadError: (callback) => ipcRenderer.on('model-download-error', (event, data) => callback(data)),
  onDownloadCancelled: (callback) => ipcRenderer.on('model-download-cancelled', (event, data) => callback(data)),

  // Consent Dialog operations
  requestConsent: (request) => ipcRenderer.invoke('request-consent', request),
  respondToConsent: (promptId, granted, duration) => ipcRenderer.invoke('respond-to-consent', promptId, granted, duration),
  getAllConsents: () => ipcRenderer.invoke('get-all-consents'),
  revokeConsent: (consentKey) => ipcRenderer.invoke('revoke-consent', consentKey),
  revokeConsentsByType: (type) => ipcRenderer.invoke('revoke-consents-by-type', type),
  clearAllConsents: () => ipcRenderer.invoke('clear-all-consents'),
  getConsentStats: () => ipcRenderer.invoke('get-consent-stats'),
  exportConsents: () => ipcRenderer.invoke('export-consents'),
  importConsents: (data, merge) => ipcRenderer.invoke('import-consents', data, merge),
  getPendingPrompts: () => ipcRenderer.invoke('get-pending-prompts'),

  // Checksum Verification operations
  verifyFileChecksum: (filePath, expectedChecksum) => ipcRenderer.invoke('verify-file-checksum', filePath, expectedChecksum),
  verifyVaultChecksums: (options) => ipcRenderer.invoke('verify-vault-checksums', options),
  verifySessionsChecksums: (sessionPaths) => ipcRenderer.invoke('verify-sessions-checksums', sessionPaths),
  updateFileChecksum: (filePath) => ipcRenderer.invoke('update-file-checksum', filePath),
  batchUpdateChecksums: (filePaths) => ipcRenderer.invoke('batch-update-checksums', filePaths),
  getVerificationCache: () => ipcRenderer.invoke('get-verification-cache'),
  clearVerificationCache: () => ipcRenderer.invoke('clear-verification-cache'),
  generateVerificationReport: (results) => ipcRenderer.invoke('generate-verification-report', results),

  // Obsidian Launcher operations
  launchObsidian: (vaultPath, options) => ipcRenderer.invoke('launch-obsidian', vaultPath, options),
  openFileInObsidian: (filePath) => ipcRenderer.invoke('open-file-in-obsidian', filePath),
  checkObsidianInstallation: () => ipcRenderer.invoke('check-obsidian-installation'),

  // Claude API Bridge operations
  setClaudeApiKey: (apiKey) => ipcRenderer.invoke('set-claude-api-key', apiKey),
  getClaudeApiKeyStatus: () => ipcRenderer.invoke('get-claude-api-key-status'),
  testClaudeConnection: () => ipcRenderer.invoke('test-claude-connection'),
  generateClaudeReflection: (prompt, context, options) => ipcRenderer.invoke('generate-claude-reflection', prompt, context, options),
  generateClaudeReflectionStream: (prompt, context, options) => ipcRenderer.invoke('generate-claude-reflection-stream', prompt, context, options),
  getClaudeStats: () => ipcRenderer.invoke('get-claude-stats'),
  resetClaudeStats: () => ipcRenderer.invoke('reset-claude-stats'),
  removeClaudeApiKey: () => ipcRenderer.invoke('remove-claude-api-key'),
  setInternetMode: (mode) => ipcRenderer.invoke('set-internet-mode', mode),
  getInternetMode: () => ipcRenderer.invoke('get-internet-mode'),

  // Claude streaming event listeners
  onClaudeStreamStart: (callback) => ipcRenderer.on('claude-stream-start', (event, data) => callback(data)),
  onClaudeStreamChunk: (callback) => ipcRenderer.on('claude-stream-chunk', (event, data) => callback(data)),
  onClaudeStreamEnd: (callback) => ipcRenderer.on('claude-stream-end', (event, data) => callback(data)),
  onClaudeStreamError: (callback) => ipcRenderer.on('claude-stream-error', (event, data) => callback(data)),

  // Git Sync Manager operations
  gitInit: (options) => ipcRenderer.invoke('git-init', options),
  gitSetRemote: (url, name) => ipcRenderer.invoke('git-set-remote', url, name),
  gitStatus: () => ipcRenderer.invoke('git-status'),
  gitCommit: (message, options) => ipcRenderer.invoke('git-commit', message, options),
  gitPush: (options) => ipcRenderer.invoke('git-push', options),
  gitPull: (options) => ipcRenderer.invoke('git-pull', options),
  gitSync: (commitMessage, options) => ipcRenderer.invoke('git-sync', commitMessage, options),
  gitHistory: (limit) => ipcRenderer.invoke('git-history', limit),

  // Session Manager operations
  sessionManagerInit: () => ipcRenderer.invoke('session-manager-init'),
  pauseSession: (sessionData, options) => ipcRenderer.invoke('pause-session', sessionData, options),
  resumeSession: (pauseId) => ipcRenderer.invoke('resume-session', pauseId),
  getPausedSessions: () => ipcRenderer.invoke('get-paused-sessions'),
  deletePausedSession: (pauseId) => ipcRenderer.invoke('delete-paused-session', pauseId),
  autoSaveSession: (sessionData) => ipcRenderer.invoke('auto-save-session', sessionData),
  loadCheckpoint: () => ipcRenderer.invoke('load-checkpoint'),
  cleanOldPausedSessions: (maxAge) => ipcRenderer.invoke('clean-old-paused-sessions', maxAge),

  // Utilities
  getAppPath: () => ipcRenderer.invoke('get-app-path')
});

console.log('⟡ MirrorDNA Portable preload initialized');
