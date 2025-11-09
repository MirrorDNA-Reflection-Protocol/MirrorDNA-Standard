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

  // Utilities
  getAppPath: () => ipcRenderer.invoke('get-app-path')
});

console.log('⟡ MirrorDNA Portable preload initialized');
