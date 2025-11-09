/**
 * Git Sync Manager
 *
 * Enables cross-device vault synchronization via Git.
 * Provides push/pull/status operations with conflict detection.
 *
 * Part of MirrorDNA Portable Launcher - Phase 5
 */

const { spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');
const { EventEmitter } = require('events');

class GitSyncManager extends EventEmitter {
  constructor(vaultPath) {
    super();
    this.vaultPath = vaultPath;
    this.isInitialized = false;
    this.syncInProgress = false;
  }

  /**
   * Initialize Git repository
   * @param {Object} options - Init options
   * @returns {Promise<Object>} Init result
   */
  async initRepository(options = {}) {
    const {
      remote = null,
      branch = 'main',
      userName = 'MirrorDNA User',
      userEmail = 'user@mirrordna.local'
    } = options;

    try {
      // Check if already a git repo
      const isRepo = await this._isGitRepo();

      if (!isRepo) {
        // Initialize git
        await this._execGit(['init']);
        await this._execGit(['config', 'user.name', userName]);
        await this._execGit(['config', 'user.email', userEmail]);
        await this._execGit(['branch', '-M', branch]);

        // Create .gitignore
        const gitignore = `.mirrordna/
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.DS_Store
*.tmp
`;
        await fs.writeFile(path.join(this.vaultPath, '.gitignore'), gitignore);
      }

      // Add remote if provided
      if (remote) {
        await this.setRemote(remote);
      }

      this.isInitialized = true;

      return {
        success: true,
        initialized: !isRepo,
        branch
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Set remote URL
   * @param {string} url - Remote repository URL
   * @param {string} name - Remote name (default: origin)
   * @returns {Promise<Object>} Result
   */
  async setRemote(url, name = 'origin') {
    try {
      // Check if remote exists
      const remotes = await this._execGit(['remote']);

      if (remotes.includes(name)) {
        // Update existing remote
        await this._execGit(['remote', 'set-url', name, url]);
      } else {
        // Add new remote
        await this._execGit(['remote', 'add', name, url]);
      }

      return {
        success: true,
        remote: name,
        url
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Get repository status
   * @returns {Promise<Object>} Status info
   */
  async getStatus() {
    try {
      const isRepo = await this._isGitRepo();
      if (!isRepo) {
        return {
          success: false,
          error: 'Not a Git repository'
        };
      }

      const statusOutput = await this._execGit(['status', '--porcelain']);
      const branchOutput = await this._execGit(['branch', '--show-current']);

      // Parse status
      const lines = statusOutput.trim().split('\n').filter(l => l);
      const changes = lines.map(line => {
        const status = line.substring(0, 2);
        const file = line.substring(3);
        return { status, file };
      });

      // Count changes
      const stats = {
        modified: changes.filter(c => c.status.includes('M')).length,
        added: changes.filter(c => c.status.includes('A')).length,
        deleted: changes.filter(c => c.status.includes('D')).length,
        untracked: changes.filter(c => c.status.includes('??')).length
      };

      return {
        success: true,
        branch: branchOutput.trim(),
        changes,
        stats,
        clean: changes.length === 0
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Commit changes
   * @param {string} message - Commit message
   * @param {Object} options - Commit options
   * @returns {Promise<Object>} Commit result
   */
  async commit(message, options = {}) {
    const {
      addAll = true,
      allowEmpty = false
    } = options;

    try {
      // Add files
      if (addAll) {
        await this._execGit(['add', '.']);
      }

      // Commit
      const args = ['commit', '-m', message];
      if (allowEmpty) {
        args.push('--allow-empty');
      }

      const output = await this._execGit(args);

      // Get commit hash
      const hash = await this._execGit(['rev-parse', 'HEAD']);

      return {
        success: true,
        hash: hash.trim().substring(0, 7),
        message,
        output
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Push changes to remote
   * @param {Object} options - Push options
   * @returns {Promise<Object>} Push result
   */
  async push(options = {}) {
    const {
      remote = 'origin',
      branch = null,
      setUpstream = true
    } = options;

    if (this.syncInProgress) {
      return { success: false, error: 'Sync already in progress' };
    }

    try {
      this.syncInProgress = true;
      this.emit('sync-start', { operation: 'push' });

      // Get current branch if not specified
      const currentBranch = branch || (await this._execGit(['branch', '--show-current'])).trim();

      // Build push command
      const args = ['push'];
      if (setUpstream) {
        args.push('-u');
      }
      args.push(remote, currentBranch);

      const output = await this._execGit(args);

      this.syncInProgress = false;
      this.emit('sync-complete', { operation: 'push', success: true });

      return {
        success: true,
        remote,
        branch: currentBranch,
        output
      };
    } catch (error) {
      this.syncInProgress = false;
      this.emit('sync-error', { operation: 'push', error: error.message });

      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Pull changes from remote
   * @param {Object} options - Pull options
   * @returns {Promise<Object>} Pull result
   */
  async pull(options = {}) {
    const {
      remote = 'origin',
      branch = null,
      rebase = false
    } = options;

    if (this.syncInProgress) {
      return { success: false, error: 'Sync already in progress' };
    }

    try {
      this.syncInProgress = true;
      this.emit('sync-start', { operation: 'pull' });

      // Get current branch if not specified
      const currentBranch = branch || (await this._execGit(['branch', '--show-current'])).trim();

      // Check for conflicts
      const status = await this.getStatus();
      if (!status.clean) {
        this.syncInProgress = false;
        return {
          success: false,
          error: 'Uncommitted changes detected. Commit or stash before pulling.',
          hasChanges: true
        };
      }

      // Build pull command
      const args = ['pull'];
      if (rebase) {
        args.push('--rebase');
      }
      args.push(remote, currentBranch);

      const output = await this._execGit(args);

      this.syncInProgress = false;
      this.emit('sync-complete', { operation: 'pull', success: true });

      return {
        success: true,
        remote,
        branch: currentBranch,
        output
      };
    } catch (error) {
      this.syncInProgress = false;

      // Check if it's a conflict
      if (error.message.includes('CONFLICT')) {
        this.emit('sync-conflict', { operation: 'pull', error: error.message });
        return {
          success: false,
          error: 'Merge conflict detected',
          conflict: true
        };
      }

      this.emit('sync-error', { operation: 'pull', error: error.message });

      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Sync vault (commit, pull, push)
   * @param {string} commitMessage - Commit message
   * @param {Object} options - Sync options
   * @returns {Promise<Object>} Sync result
   */
  async sync(commitMessage, options = {}) {
    const {
      remote = 'origin',
      branch = null,
      pullFirst = true
    } = options;

    try {
      const results = {
        commit: null,
        pull: null,
        push: null
      };

      // Check if there are changes
      const status = await this.getStatus();

      if (!status.clean) {
        // Commit changes
        results.commit = await this.commit(commitMessage || `Sync: ${new Date().toISOString()}`);
        if (!results.commit.success) {
          return { success: false, error: 'Commit failed', results };
        }
      }

      // Pull if requested
      if (pullFirst) {
        results.pull = await this.pull({ remote, branch });
        if (!results.pull.success) {
          return { success: false, error: 'Pull failed', results };
        }
      }

      // Push
      results.push = await this.push({ remote, branch });
      if (!results.push.success) {
        return { success: false, error: 'Push failed', results };
      }

      return {
        success: true,
        results
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Get commit history
   * @param {number} limit - Number of commits
   * @returns {Promise<Object>} Commit history
   */
  async getHistory(limit = 20) {
    try {
      const format = '%H|%an|%ae|%at|%s';
      const output = await this._execGit(['log', `--format=${format}`, `-n${limit}`]);

      const commits = output.trim().split('\n').filter(l => l).map(line => {
        const [hash, author, email, timestamp, message] = line.split('|');
        return {
          hash: hash.substring(0, 7),
          fullHash: hash,
          author,
          email,
          timestamp: parseInt(timestamp) * 1000,
          date: new Date(parseInt(timestamp) * 1000).toISOString(),
          message
        };
      });

      return {
        success: true,
        commits
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Check if directory is a Git repository
   */
  async _isGitRepo() {
    try {
      await this._execGit(['rev-parse', '--git-dir']);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Execute Git command
   */
  async _execGit(args) {
    return new Promise((resolve, reject) => {
      const git = spawn('git', args, {
        cwd: this.vaultPath,
        stdio: 'pipe'
      });

      let stdout = '';
      let stderr = '';

      git.stdout?.on('data', (data) => {
        stdout += data.toString();
      });

      git.stderr?.on('data', (data) => {
        stderr += data.toString();
      });

      git.on('close', (code) => {
        if (code === 0) {
          resolve(stdout);
        } else {
          reject(new Error(stderr || stdout || `Git command failed with code ${code}`));
        }
      });

      git.on('error', (error) => {
        reject(new Error(`Failed to execute git: ${error.message}`));
      });
    });
  }
}

module.exports = { GitSyncManager };
