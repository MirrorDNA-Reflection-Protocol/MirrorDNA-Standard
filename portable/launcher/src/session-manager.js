/**
 * Session Manager
 *
 * Handles session pause/resume functionality.
 * Allows users to save session state and restore later.
 *
 * Part of MirrorDNA Portable Launcher - Phase 5
 */

const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

class SessionManager {
  constructor(vaultPath) {
    this.vaultPath = vaultPath;
    this.pausedSessionsPath = path.join(vaultPath, 'state', 'paused');
    this.currentSession = null;
  }

  /**
   * Initialize session manager
   */
  async initialize() {
    try {
      // Ensure paused sessions directory exists
      await fs.mkdir(this.pausedSessionsPath, { recursive: true });

      return {
        success: true,
        initialized: true
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Pause current session
   * @param {Object} sessionData - Current session data
   * @param {Object} options - Pause options
   * @returns {Promise<Object>} Pause result
   */
  async pauseSession(sessionData, options = {}) {
    const {
      reason = 'User paused session',
      saveContext = true
    } = options;

    try {
      const pauseId = this._generatePauseId();
      const timestamp = new Date().toISOString();

      const pausedSession = {
        pauseId,
        pausedAt: timestamp,
        reason,
        sessionData: saveContext ? sessionData : null,
        metadata: {
          sessionNumber: sessionData.sessionNumber,
          startedAt: sessionData.startedAt,
          messageCount: sessionData.messages?.length || 0,
          lastMessage: sessionData.messages?.[sessionData.messages.length - 1] || null
        }
      };

      // Save paused session
      const pauseFile = path.join(this.pausedSessionsPath, `${pauseId}.json`);
      await fs.writeFile(pauseFile, JSON.stringify(pausedSession, null, 2));

      return {
        success: true,
        pauseId,
        pausedAt: timestamp,
        sessionData: pausedSession.metadata
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Resume paused session
   * @param {string} pauseId - Pause identifier
   * @returns {Promise<Object>} Resumed session data
   */
  async resumeSession(pauseId) {
    try {
      const pauseFile = path.join(this.pausedSessionsPath, `${pauseId}.json`);

      // Read paused session
      const data = await fs.readFile(pauseFile, 'utf8');
      const pausedSession = JSON.parse(data);

      // Calculate pause duration
      const pausedAt = new Date(pausedSession.pausedAt);
      const resumedAt = new Date();
      const pauseDuration = resumedAt - pausedAt;

      // Delete pause file
      await fs.unlink(pauseFile);

      return {
        success: true,
        sessionData: pausedSession.sessionData,
        pausedAt: pausedSession.pausedAt,
        resumedAt: resumedAt.toISOString(),
        pauseDuration: this._formatDuration(pauseDuration),
        pauseDurationMs: pauseDuration
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Get all paused sessions
   * @returns {Promise<Object>} List of paused sessions
   */
  async getPausedSessions() {
    try {
      const files = await fs.readdir(this.pausedSessionsPath);
      const pausedSessions = [];

      for (const file of files) {
        if (file.endsWith('.json')) {
          try {
            const data = await fs.readFile(
              path.join(this.pausedSessionsPath, file),
              'utf8'
            );
            const session = JSON.parse(data);

            // Calculate pause age
            const pausedAt = new Date(session.pausedAt);
            const now = new Date();
            const age = now - pausedAt;

            pausedSessions.push({
              pauseId: session.pauseId,
              pausedAt: session.pausedAt,
              pauseAge: this._formatDuration(age),
              pauseAgeMs: age,
              reason: session.reason,
              metadata: session.metadata
            });
          } catch (error) {
            // Skip invalid files
            console.warn(`Failed to read paused session ${file}:`, error.message);
          }
        }
      }

      // Sort by most recent
      pausedSessions.sort((a, b) => {
        return new Date(b.pausedAt) - new Date(a.pausedAt);
      });

      return {
        success: true,
        sessions: pausedSessions,
        count: pausedSessions.length
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Delete paused session
   * @param {string} pauseId - Pause identifier
   * @returns {Promise<Object>} Deletion result
   */
  async deletePausedSession(pauseId) {
    try {
      const pauseFile = path.join(this.pausedSessionsPath, `${pauseId}.json`);
      await fs.unlink(pauseFile);

      return {
        success: true,
        pauseId,
        deleted: true
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Auto-save current session (periodic checkpoint)
   * @param {Object} sessionData - Current session data
   * @returns {Promise<Object>} Auto-save result
   */
  async autoSaveSession(sessionData) {
    try {
      const checkpointPath = path.join(this.vaultPath, 'state', 'checkpoint.json');

      const checkpoint = {
        savedAt: new Date().toISOString(),
        sessionData,
        autoSave: true
      };

      await fs.writeFile(checkpointPath, JSON.stringify(checkpoint, null, 2));

      return {
        success: true,
        savedAt: checkpoint.savedAt
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Load auto-saved session
   * @returns {Promise<Object>} Loaded checkpoint
   */
  async loadCheckpoint() {
    try {
      const checkpointPath = path.join(this.vaultPath, 'state', 'checkpoint.json');

      const data = await fs.readFile(checkpointPath, 'utf8');
      const checkpoint = JSON.parse(data);

      return {
        success: true,
        checkpoint: checkpoint.sessionData,
        savedAt: checkpoint.savedAt,
        age: this._formatDuration(new Date() - new Date(checkpoint.savedAt))
      };
    } catch (error) {
      if (error.code === 'ENOENT') {
        return {
          success: false,
          error: 'No checkpoint found'
        };
      }

      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Clean old paused sessions
   * @param {number} maxAge - Maximum age in milliseconds (default: 30 days)
   * @returns {Promise<Object>} Cleanup result
   */
  async cleanOldPausedSessions(maxAge = 30 * 24 * 60 * 60 * 1000) {
    try {
      const pausedSessions = await this.getPausedSessions();
      if (!pausedSessions.success) {
        return pausedSessions;
      }

      const now = new Date();
      const deleted = [];

      for (const session of pausedSessions.sessions) {
        if (session.pauseAgeMs > maxAge) {
          const result = await this.deletePausedSession(session.pauseId);
          if (result.success) {
            deleted.push(session.pauseId);
          }
        }
      }

      return {
        success: true,
        deleted: deleted.length,
        pauseIds: deleted
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Generate pause ID
   */
  _generatePauseId() {
    const timestamp = Date.now();
    const random = crypto.randomBytes(4).toString('hex');
    return `pause_${timestamp}_${random}`;
  }

  /**
   * Format duration for display
   */
  _formatDuration(ms) {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d ${hours % 24}h`;
    if (hours > 0) return `${hours}h ${minutes % 60}m`;
    if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
    return `${seconds}s`;
  }
}

module.exports = { SessionManager };
