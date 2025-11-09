const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

/**
 * MirrorDNA Session Continuity Engine
 *
 * Manages session persistence, restoration, history, and lineage tracking.
 * Implements constitutive continuity: memory that compounds, not resets.
 */
class SessionContinuity {
  constructor(vaultPath) {
    this.vaultPath = vaultPath;
    this.statePath = path.join(vaultPath, 'state/current.json');
    this.sessionsPath = path.join(vaultPath, 'sessions');
    this.historyPath = path.join(vaultPath, 'state/session_history.json');
    this.state = null;
    this.history = null;
  }

  /**
   * Initialize the continuity engine
   * Loads state, validates integrity, restores context
   */
  async initialize() {
    try {
      console.log('⟡ Initializing Session Continuity Engine...');

      // Load current state
      await this.loadState();

      // Load session history
      await this.loadHistory();

      // Validate vault integrity
      await this.validateIntegrity();

      // Restore last session context if exists
      if (this.state.last_session?.path) {
        await this.restoreSession(this.state.last_session.path);
      }

      console.log('✓ Session Continuity Engine initialized');
      return { success: true };
    } catch (error) {
      console.error('Session Continuity initialization failed:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Load current state from vault
   */
  async loadState() {
    if (!fs.existsSync(this.statePath)) {
      // Initialize default state if not exists
      this.state = {
        version: '1.0',
        vault_name: 'AMOS',
        last_session: null,
        context: {
          active_topics: [],
          key_insights: [],
          pending_tasks: []
        },
        settings: {
          internet_mode: 'hybrid_ask',
          llm_model: 'phi3-mini-4k',
          onboarding_completed: false
        },
        integrity: {
          vault_checksum: null,
          last_verified: null,
          spec_versions: {}
        }
      };
      await this.saveState();
    } else {
      const data = await fs.promises.readFile(this.statePath, 'utf8');
      this.state = JSON.parse(data);
    }
  }

  /**
   * Save current state to vault
   */
  async saveState() {
    await fs.promises.writeFile(
      this.statePath,
      JSON.stringify(this.state, null, 2),
      'utf8'
    );
  }

  /**
   * Load session history (chronological index)
   */
  async loadHistory() {
    if (!fs.existsSync(this.historyPath)) {
      this.history = {
        sessions: [],
        total_sessions: 0,
        first_session_date: null,
        last_updated: null
      };
      await this.saveHistory();
    } else {
      const data = await fs.promises.readFile(this.historyPath, 'utf8');
      this.history = JSON.parse(data);
    }
  }

  /**
   * Save session history
   */
  async saveHistory() {
    await fs.promises.writeFile(
      this.historyPath,
      JSON.stringify(this.history, null, 2),
      'utf8'
    );
  }

  /**
   * Create a new session
   * @param {Object} options - Session configuration
   * @returns {Object} Session metadata
   */
  async createSession(options = {}) {
    try {
      const sessionNumber = (this.state.last_session?.number || 0) + 1;
      const timestamp = new Date().toISOString();
      const date = timestamp.split('T')[0];
      const filename = `${date}_session_${String(sessionNumber).padStart(3, '0')}.md`;

      // Load template
      const templatePath = path.join(this.vaultPath, 'templates/new-session.md');
      let template = await fs.promises.readFile(templatePath, 'utf8');

      // Calculate context summary
      const contextSummary = this.generateContextSummary();

      // Replace placeholders
      template = template
        .replace(/\{\{session_number\}\}/g, sessionNumber)
        .replace(/\{\{date\}\}/g, date)
        .replace(/\{\{iso_timestamp\}\}/g, timestamp)
        .replace(/\{\{vault_name\}\}/g, this.state.vault_name)
        .replace(/\{\{predecessor_path\}\}/g, this.state.last_session?.path || 'none')
        .replace(/\{\{previous_context\}\}/g, contextSummary);

      // Add initial dialogue if provided
      if (options.dialogue) {
        template = template.replace('⟡ Ready when you are.', options.dialogue);
      }

      // Compute checksum
      const checksum = this.computeChecksum(template);

      // Write session file
      const sessionPath = path.join(this.sessionsPath, filename);
      await fs.promises.writeFile(sessionPath, template);

      // Create session metadata
      const sessionMetadata = {
        number: sessionNumber,
        path: `sessions/${filename}`,
        timestamp,
        checksum,
        title: options.title || `Session ${sessionNumber}`,
        tags: options.tags || ['reflection', 'continuity']
      };

      // Update state
      this.state.last_session = sessionMetadata;
      await this.saveState();

      // Update history
      this.history.sessions.push(sessionMetadata);
      this.history.total_sessions = sessionNumber;
      this.history.last_updated = timestamp;
      if (!this.history.first_session_date) {
        this.history.first_session_date = timestamp;
      }
      await this.saveHistory();

      console.log(`✓ Created session ${sessionNumber}: ${filename}`);
      return { success: true, session: sessionMetadata };
    } catch (error) {
      console.error('Failed to create session:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Restore a session (load its context)
   * @param {string} sessionPath - Relative path to session file
   */
  async restoreSession(sessionPath) {
    try {
      const fullPath = path.join(this.vaultPath, sessionPath);

      if (!fs.existsSync(fullPath)) {
        throw new Error(`Session not found: ${sessionPath}`);
      }

      const content = await fs.promises.readFile(fullPath, 'utf8');

      // Extract context from session file
      const context = this.extractContext(content);

      // Update current context
      this.state.context = {
        ...this.state.context,
        ...context,
        restored_from: sessionPath,
        restored_at: new Date().toISOString()
      };

      console.log(`✓ Restored session: ${sessionPath}`);
      return { success: true, context };
    } catch (error) {
      console.error('Failed to restore session:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Get session history with filtering
   * @param {Object} filters - Filter options
   * @returns {Array} Filtered sessions
   */
  getHistory(filters = {}) {
    let sessions = [...this.history.sessions];

    // Filter by date range
    if (filters.startDate) {
      sessions = sessions.filter(s => s.timestamp >= filters.startDate);
    }
    if (filters.endDate) {
      sessions = sessions.filter(s => s.timestamp <= filters.endDate);
    }

    // Filter by tags
    if (filters.tags) {
      sessions = sessions.filter(s =>
        filters.tags.some(tag => s.tags?.includes(tag))
      );
    }

    // Filter by search term
    if (filters.search) {
      sessions = sessions.filter(s =>
        s.title?.toLowerCase().includes(filters.search.toLowerCase()) ||
        s.path?.toLowerCase().includes(filters.search.toLowerCase())
      );
    }

    // Sort (default: newest first)
    sessions.sort((a, b) => {
      if (filters.sortOrder === 'asc') {
        return a.timestamp.localeCompare(b.timestamp);
      }
      return b.timestamp.localeCompare(a.timestamp);
    });

    return sessions;
  }

  /**
   * Navigate to previous session
   */
  async navigateToPrevious() {
    const currentNumber = this.state.last_session?.number || 0;
    if (currentNumber <= 1) {
      return { success: false, error: 'No previous session' };
    }

    const previousSession = this.history.sessions.find(
      s => s.number === currentNumber - 1
    );

    if (!previousSession) {
      return { success: false, error: 'Previous session not found' };
    }

    return await this.restoreSession(previousSession.path);
  }

  /**
   * Navigate to next session
   */
  async navigateToNext() {
    const currentNumber = this.state.last_session?.number || 0;
    const nextSession = this.history.sessions.find(
      s => s.number === currentNumber + 1
    );

    if (!nextSession) {
      return { success: false, error: 'No next session' };
    }

    return await this.restoreSession(nextSession.path);
  }

  /**
   * Export session or session range
   * @param {Object} options - Export options
   */
  async exportSessions(options = {}) {
    try {
      const {
        sessionNumbers = [],
        startDate,
        endDate,
        format = 'json'
      } = options;

      let sessionsToExport = [];

      // Export specific sessions
      if (sessionNumbers.length > 0) {
        sessionsToExport = this.history.sessions.filter(
          s => sessionNumbers.includes(s.number)
        );
      }
      // Export date range
      else if (startDate || endDate) {
        sessionsToExport = this.getHistory({ startDate, endDate });
      }
      // Export all
      else {
        sessionsToExport = this.history.sessions;
      }

      // Load full session content
      const exportData = {
        vault_name: this.state.vault_name,
        export_date: new Date().toISOString(),
        sessions: []
      };

      for (const session of sessionsToExport) {
        const fullPath = path.join(this.vaultPath, session.path);
        if (fs.existsSync(fullPath)) {
          const content = await fs.promises.readFile(fullPath, 'utf8');
          exportData.sessions.push({
            ...session,
            content
          });
        }
      }

      return {
        success: true,
        data: format === 'json' ? JSON.stringify(exportData, null, 2) : exportData,
        count: exportData.sessions.length
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Import sessions
   * @param {Object} importData - Session data to import
   */
  async importSessions(importData) {
    try {
      const data = typeof importData === 'string' ? JSON.parse(importData) : importData;

      let imported = 0;
      for (const session of data.sessions) {
        const filename = path.basename(session.path);
        const targetPath = path.join(this.sessionsPath, filename);

        // Check if already exists
        if (!fs.existsSync(targetPath)) {
          await fs.promises.writeFile(targetPath, session.content);

          // Add to history if not duplicate
          const exists = this.history.sessions.find(s => s.number === session.number);
          if (!exists) {
            this.history.sessions.push({
              number: session.number,
              path: session.path,
              timestamp: session.timestamp,
              checksum: session.checksum,
              title: session.title,
              tags: session.tags
            });
            imported++;
          }
        }
      }

      // Re-sort history
      this.history.sessions.sort((a, b) => a.number - b.number);
      this.history.total_sessions = this.history.sessions.length;
      await this.saveHistory();

      return { success: true, imported };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Validate vault integrity
   */
  async validateIntegrity() {
    try {
      // Verify session files match history
      const missingFiles = [];

      for (const session of this.history.sessions) {
        const fullPath = path.join(this.vaultPath, session.path);
        if (!fs.existsSync(fullPath)) {
          missingFiles.push(session.path);
        }
      }

      // Update integrity check timestamp
      this.state.integrity.last_verified = new Date().toISOString();
      this.state.integrity.missing_sessions = missingFiles.length;
      await this.saveState();

      if (missingFiles.length > 0) {
        console.warn(`⚠️ Missing ${missingFiles.length} session files`);
        return { valid: false, missing: missingFiles };
      }

      console.log('✓ Vault integrity validated');
      return { valid: true };
    } catch (error) {
      console.error('Integrity validation failed:', error);
      return { valid: false, error: error.message };
    }
  }

  /**
   * Generate context summary from current state
   */
  generateContextSummary() {
    const { active_topics, key_insights, pending_tasks } = this.state.context;

    const parts = [];

    if (active_topics?.length > 0) {
      parts.push(`**Active Topics:** ${active_topics.join(', ')}`);
    }

    if (key_insights?.length > 0) {
      parts.push(`**Key Insights:**\n${key_insights.map(i => `- ${i}`).join('\n')}`);
    }

    if (pending_tasks?.length > 0) {
      parts.push(`**Pending Tasks:**\n${pending_tasks.map(t => `- ${t}`).join('\n')}`);
    }

    return parts.length > 0 ? parts.join('\n\n') : 'No previous context';
  }

  /**
   * Extract context from session markdown
   */
  extractContext(content) {
    const context = {
      active_topics: [],
      key_insights: [],
      pending_tasks: []
    };

    // Extract key insights section
    const insightsMatch = content.match(/### Key Insights\n([\s\S]*?)\n###/);
    if (insightsMatch) {
      const insights = insightsMatch[1]
        .split('\n')
        .filter(line => line.trim().startsWith('-'))
        .map(line => line.replace(/^-\s*/, '').trim())
        .filter(Boolean);
      context.key_insights = insights;
    }

    // Extract next steps section
    const nextStepsMatch = content.match(/### Next Steps\n([\s\S]*?)\n---/);
    if (nextStepsMatch) {
      const tasks = nextStepsMatch[1]
        .split('\n')
        .filter(line => line.trim().startsWith('-'))
        .map(line => line.replace(/^-\s*/, '').trim())
        .filter(Boolean);
      context.pending_tasks = tasks;
    }

    return context;
  }

  /**
   * Compute checksum for session content
   */
  computeChecksum(content) {
    return crypto.createHash('sha256').update(content).digest('hex');
  }

  /**
   * Update session context
   */
  async updateContext(updates) {
    this.state.context = {
      ...this.state.context,
      ...updates,
      last_updated: new Date().toISOString()
    };
    await this.saveState();
    return { success: true };
  }

  /**
   * Get current session info
   */
  getCurrentSession() {
    return this.state.last_session;
  }

  /**
   * Get session statistics
   */
  getStatistics() {
    const now = new Date();
    const firstDate = new Date(this.history.first_session_date || now);
    const daysSinceFirst = Math.floor((now - firstDate) / (1000 * 60 * 60 * 24));

    return {
      total_sessions: this.history.total_sessions,
      first_session: this.history.first_session_date,
      last_session: this.state.last_session?.timestamp,
      days_active: daysSinceFirst,
      average_sessions_per_day: daysSinceFirst > 0
        ? (this.history.total_sessions / daysSinceFirst).toFixed(2)
        : 0,
      current_context_items:
        (this.state.context.active_topics?.length || 0) +
        (this.state.context.key_insights?.length || 0) +
        (this.state.context.pending_tasks?.length || 0)
    };
  }
}

module.exports = SessionContinuity;
