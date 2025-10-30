const { app, BrowserWindow, ipcMain, Menu } = require('electron');
const path = require('path');
const fs = require('fs');
const Store = require('electron-store');

// Initialize persistent settings
const store = new Store({
  defaults: {
    vaultPath: null,
    internetMode: 'hybrid_ask', // 'offline_only' | 'hybrid_ask' | 'online'
    onboardingCompleted: false,
    windowBounds: { width: 1000, height: 700 }
  }
});

let mainWindow;

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

app.whenReady().then(() => {
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

console.log('⟡ MirrorDNA Portable launcher initialized');
