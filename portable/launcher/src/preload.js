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
  generateReflection: (prompt) => ipcRenderer.invoke('generate-reflection', prompt),

  // Internet consent
  requestInternet: (action, details) => ipcRenderer.invoke('request-internet', action, details),

  // Utilities
  getAppPath: () => ipcRenderer.invoke('get-app-path')
});

console.log('⟡ MirrorDNA Portable preload initialized');
