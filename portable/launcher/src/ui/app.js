// MirrorDNA Portable - UI Controller

class MirrorDNAApp {
  constructor() {
    this.currentScreen = null;
    this.settings = null;
    this.vaultState = null;
    this.init();
  }

  async init() {
    console.log('⟡ Initializing MirrorDNA UI');

    // Load settings
    this.settings = await window.mirrorDNA.getSettings();

    // Setup event listeners
    this.setupEventListeners();

    // Determine which screen to show
    if (this.settings.onboardingCompleted && this.settings.vaultPath) {
      await this.loadSessionScreen();
    } else {
      this.showScreen('onboarding');
    }

    // Update status indicator
    this.updateStatusIndicator(this.settings.internetMode);
  }

  setupEventListeners() {
    // Onboarding buttons
    document.getElementById('btn-new-user').addEventListener('click', () => {
      this.showScreen('setup');
    });

    document.getElementById('btn-existing-user').addEventListener('click', async () => {
      // TODO: Implement vault selection dialog
      alert('Vault selection not yet implemented. Please use "I\'m New" for now.');
    });

    // Setup form
    document.getElementById('choose-path-btn').addEventListener('click', () => {
      // TODO: Implement directory picker
      const defaultPath = process.platform === 'win32' ? 'D:\\MirrorDNA' : '/home/user/MirrorDNA';
      document.getElementById('vault-path-input').value = defaultPath;
    });

    document.getElementById('complete-setup-btn').addEventListener('click', async () => {
      await this.completeSetup();
    });

    // Session input
    document.getElementById('send-btn').addEventListener('click', () => {
      this.sendMessage();
    });

    document.getElementById('user-input').addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });

    // Settings
    document.getElementById('settings-btn').addEventListener('click', () => {
      this.toggleSettings();
    });

    document.getElementById('close-settings-btn').addEventListener('click', () => {
      this.toggleSettings();
    });

    document.getElementById('internet-mode-select').addEventListener('change', async (e) => {
      await this.updateInternetMode(e.target.value);
    });

    // Status indicator click
    document.getElementById('status-indicator').addEventListener('click', () => {
      this.showInternetModeDialog();
    });
  }

  showScreen(screenName) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(screen => {
      screen.classList.add('hidden');
    });

    // Show requested screen
    const screen = document.getElementById(`${screenName}-screen`);
    if (screen) {
      screen.classList.remove('hidden');
      this.currentScreen = screenName;
    }
  }

  async completeSetup() {
    const vaultName = document.getElementById('vault-name-input').value.trim();
    const vaultPath = document.getElementById('vault-path-input').value.trim();
    const internetMode = document.querySelector('input[name="internet-mode"]:checked').value;

    if (!vaultName || !vaultPath) {
      alert('Please provide vault name and location');
      return;
    }

    // Create vault
    const result = await window.mirrorDNA.initVault(vaultName, vaultPath);

    if (!result.success) {
      alert(`Error creating vault: ${result.error}`);
      return;
    }

    // Update settings
    await window.mirrorDNA.updateSettings({
      vaultPath: result.vaultPath,
      internetMode,
      onboardingCompleted: true
    });

    // Reload settings and show session screen
    this.settings = await window.mirrorDNA.getSettings();
    await this.loadSessionScreen();
  }

  async loadSessionScreen() {
    // Load vault state
    const result = await window.mirrorDNA.readVaultState();

    if (!result.success) {
      alert(`Error loading vault: ${result.error}`);
      return;
    }

    this.vaultState = result.state;

    // Update UI
    document.getElementById('vault-name').textContent = `Vault: ${this.vaultState.vault_name}`;

    // Show session screen
    this.showScreen('session');

    // Load last session if exists
    if (this.vaultState.last_session) {
      this.appendMessage('system', `Last session: ${this.vaultState.last_session.timestamp}`);
    }
  }

  async sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();

    if (!message) return;

    // Disable input while processing
    input.disabled = true;
    document.getElementById('send-btn').disabled = true;

    // Display user message
    this.appendMessage('user', message);
    input.value = '';

    try {
      // Generate reflection
      // TODO: Implement actual LLM integration
      const response = await this.generateReflection(message);

      // Display assistant response
      this.appendMessage('assistant', response);

      // Write session to vault
      const dialogue = this.formatDialogue(message, response);
      await window.mirrorDNA.writeSession(dialogue);

    } catch (error) {
      this.appendMessage('system', `Error: ${error.message}`);
    } finally {
      // Re-enable input
      input.disabled = false;
      document.getElementById('send-btn').disabled = false;
      input.focus();
    }
  }

  async generateReflection(prompt) {
    // Placeholder for LLM integration
    // TODO: Implement actual LLM bridge

    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    return `⟡ Reflection placeholder

I received your input: "${prompt}"

This is where the local LLM (Phi-3 Mini) would generate a thoughtful reflection following the MirrorDNA protocol and AHP (Cite or Silence).

For now, this is a placeholder response until the LLM integration is complete.

**Next steps:**
- Integrate llama.cpp runtime
- Load Phi-3 Mini model
- Implement context injection (Master Citation + session state)
- Add streaming responses

⟡ MirrorDNA Portable - Development Mode`;
  }

  formatDialogue(userMessage, assistantResponse) {
    const timestamp = new Date().toISOString();
    return `## ${timestamp}

### User
${userMessage}

### Reflection
${assistantResponse}`;
  }

  appendMessage(role, content) {
    const history = document.getElementById('session-history');
    const message = document.createElement('div');
    message.className = `message ${role}`;

    const meta = document.createElement('div');
    meta.className = 'message-meta';
    meta.textContent = role === 'user' ? 'You' : (role === 'assistant' ? '⟡ MirrorDNA' : 'System');

    const text = document.createElement('div');
    text.className = 'message-content';
    text.textContent = content;

    message.appendChild(meta);
    message.appendChild(text);
    history.appendChild(message);

    // Scroll to bottom
    history.scrollTop = history.scrollHeight;
  }

  toggleSettings() {
    const panel = document.getElementById('settings-panel');
    panel.classList.toggle('hidden');

    if (!panel.classList.contains('hidden')) {
      // Update settings values
      document.getElementById('current-vault-path').textContent = `Path: ${this.settings.vaultPath || 'Not set'}`;
      document.getElementById('internet-mode-select').value = this.settings.internetMode;
    }
  }

  async updateInternetMode(mode) {
    await window.mirrorDNA.updateSettings({ internetMode: mode });
    this.settings.internetMode = mode;
    this.updateStatusIndicator(mode);
  }

  updateStatusIndicator(mode) {
    const indicator = document.getElementById('status-indicator');

    // Remove all status classes
    indicator.classList.remove('status-offline', 'status-hybrid', 'status-online');

    // Add appropriate class and update icon
    switch (mode) {
      case 'offline_only':
        indicator.classList.add('status-offline');
        indicator.innerHTML = '<img src="../../../glyphs/status-icons/offline.svg" alt="⟡">';
        indicator.title = 'Offline - Self-contained';
        break;
      case 'hybrid_ask':
        indicator.classList.add('status-hybrid');
        indicator.innerHTML = '<img src="../../../glyphs/status-icons/hybrid.svg" alt="⟡◌">';
        indicator.title = 'Hybrid - Ask before internet';
        break;
      case 'online':
        indicator.classList.add('status-online');
        indicator.innerHTML = '<img src="../../../glyphs/status-icons/online.svg" alt="⟡⟐">';
        indicator.title = 'Online - Cloud features enabled';
        break;
    }
  }

  showInternetModeDialog() {
    const currentMode = this.settings.internetMode;
    const modeNames = {
      'offline_only': '⟡ Offline Only',
      'hybrid_ask': '⟡◌ Hybrid',
      'online': '⟡⟐ Online'
    };

    const message = `Current mode: ${modeNames[currentMode]}\n\nClick the settings button to change internet mode.`;
    alert(message);
  }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.app = new MirrorDNAApp();
});

console.log('⟡ MirrorDNA UI loaded');
