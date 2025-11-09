/**
 * Obsidian Launcher
 *
 * Launches Obsidian application with the configured vault.
 * Supports cross-platform detection and process management.
 *
 * Part of MirrorDNA Portable Launcher - Phase 2
 */

const { spawn } = require('child_process');
const { existsSync } = require('fs');
const path = require('path');
const os = require('os');

class ObsidianLauncher {
  constructor() {
    this.platform = process.platform;
    this.obsidianProcess = null;
    this.obsidianPaths = this._getObsidianPaths();
  }

  /**
   * Launch Obsidian with specified vault
   * @param {string} vaultPath - Path to vault directory
   * @param {Object} options - Launch options
   * @returns {Promise<Object>} Launch result
   */
  async launchVault(vaultPath, options = {}) {
    const {
      detached = true,     // Run Obsidian in detached mode
      openFile = null,     // Optional file to open within vault
      newWindow = false    // Open in new window
    } = options;

    try {
      // Validate vault path
      if (!vaultPath || !existsSync(vaultPath)) {
        return {
          success: false,
          error: 'Vault path does not exist'
        };
      }

      // Find Obsidian executable
      const obsidianPath = await this._findObsidianExecutable();
      if (!obsidianPath) {
        return {
          success: false,
          error: 'Obsidian not found. Please install Obsidian from https://obsidian.md'
        };
      }

      // Build command arguments
      const args = this._buildArgs(vaultPath, { openFile, newWindow });

      // Spawn Obsidian process
      this.obsidianProcess = spawn(obsidianPath, args, {
        detached,
        stdio: 'ignore', // Ignore stdio to avoid blocking
        shell: this.platform === 'win32' // Use shell on Windows
      });

      // Allow the process to run independently
      if (detached) {
        this.obsidianProcess.unref();
      }

      // Wait a moment to check if process started successfully
      await this._waitForProcessStart();

      if (this.obsidianProcess.killed) {
        return {
          success: false,
          error: 'Obsidian process failed to start'
        };
      }

      return {
        success: true,
        pid: this.obsidianProcess.pid,
        vaultPath,
        obsidianPath,
        launchedAt: new Date().toISOString()
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Open specific file in Obsidian
   * @param {string} vaultPath - Path to vault
   * @param {string} filePath - Path to file (relative to vault)
   * @returns {Promise<Object>} Launch result
   */
  async openFile(vaultPath, filePath) {
    return await this.launchVault(vaultPath, { openFile: filePath });
  }

  /**
   * Check if Obsidian is installed
   * @returns {Promise<Object>} Installation status
   */
  async checkInstallation() {
    try {
      const obsidianPath = await this._findObsidianExecutable();

      if (obsidianPath) {
        return {
          installed: true,
          path: obsidianPath,
          platform: this.platform
        };
      } else {
        return {
          installed: false,
          platform: this.platform,
          downloadUrl: 'https://obsidian.md/download'
        };
      }
    } catch (error) {
      return {
        installed: false,
        error: error.message
      };
    }
  }

  /**
   * Get common Obsidian installation paths by platform
   */
  _getObsidianPaths() {
    const home = os.homedir();

    switch (this.platform) {
      case 'darwin': // macOS
        return [
          '/Applications/Obsidian.app/Contents/MacOS/Obsidian',
          path.join(home, 'Applications/Obsidian.app/Contents/MacOS/Obsidian')
        ];

      case 'win32': // Windows
        return [
          path.join(process.env.LOCALAPPDATA || '', 'Obsidian', 'Obsidian.exe'),
          path.join(process.env.PROGRAMFILES || 'C:\\Program Files', 'Obsidian', 'Obsidian.exe'),
          path.join(process.env['PROGRAMFILES(X86)'] || 'C:\\Program Files (x86)', 'Obsidian', 'Obsidian.exe')
        ];

      case 'linux': // Linux
        return [
          '/usr/bin/obsidian',
          '/usr/local/bin/obsidian',
          path.join(home, '.local/bin/obsidian'),
          '/opt/Obsidian/obsidian',
          '/snap/bin/obsidian'
        ];

      default:
        return [];
    }
  }

  /**
   * Find Obsidian executable on system
   */
  async _findObsidianExecutable() {
    // Check common installation paths
    for (const path of this.obsidianPaths) {
      if (existsSync(path)) {
        return path;
      }
    }

    // Try PATH environment variable (Linux/macOS)
    if (this.platform !== 'win32') {
      return await this._checkPathForObsidian();
    }

    return null;
  }

  /**
   * Check if 'obsidian' is available in PATH
   */
  async _checkPathForObsidian() {
    return new Promise((resolve) => {
      const which = spawn('which', ['obsidian'], {
        stdio: 'pipe'
      });

      let output = '';
      which.stdout?.on('data', (data) => {
        output += data.toString();
      });

      which.on('close', (code) => {
        if (code === 0 && output.trim()) {
          resolve(output.trim());
        } else {
          resolve(null);
        }
      });

      which.on('error', () => {
        resolve(null);
      });
    });
  }

  /**
   * Build command-line arguments for Obsidian
   */
  _buildArgs(vaultPath, options) {
    const args = [];

    // Vault path (use obsidian:// URI scheme)
    const vaultUri = `obsidian://open?path=${encodeURIComponent(vaultPath)}`;
    args.push(vaultUri);

    // Open specific file
    if (options.openFile) {
      const fileUri = `obsidian://open?vault=${encodeURIComponent(path.basename(vaultPath))}&file=${encodeURIComponent(options.openFile)}`;
      args[0] = fileUri; // Replace vault URI with file URI
    }

    // New window flag
    if (options.newWindow && this.platform !== 'win32') {
      args.unshift('--new-window');
    }

    return args;
  }

  /**
   * Wait for process to start
   */
  async _waitForProcessStart() {
    return new Promise((resolve) => {
      setTimeout(resolve, 500); // Wait 500ms for process to initialize
    });
  }

  /**
   * Kill Obsidian process if running
   */
  kill() {
    if (this.obsidianProcess && !this.obsidianProcess.killed) {
      this.obsidianProcess.kill();
      return { success: true };
    }
    return { success: false, error: 'No process running' };
  }
}

module.exports = { ObsidianLauncher };
