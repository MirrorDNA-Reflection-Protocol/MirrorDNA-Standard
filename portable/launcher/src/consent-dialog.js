/**
 * Consent Dialog Manager
 *
 * Privacy-first consent management for internet-connected operations.
 * Implements explicit user consent for all network activities.
 *
 * Part of MirrorDNA Portable Launcher - Phase 2
 */

const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

class ConsentDialogManager {
  constructor(options = {}) {
    this.userDataPath = options.userDataPath || path.join(process.cwd(), '.mirrordna');
    this.consentFilePath = path.join(this.userDataPath, 'consent.json');
    this.consents = {};
    this.pendingPrompts = new Map();
    this.initialized = false;
  }

  /**
   * Initialize consent manager
   */
  async initialize() {
    if (this.initialized) return;

    try {
      // Ensure user data directory exists
      await fs.mkdir(this.userDataPath, { recursive: true });

      // Load existing consents
      try {
        const data = await fs.readFile(this.consentFilePath, 'utf8');
        const parsed = JSON.parse(data);
        this.consents = parsed.consents || {};
      } catch (err) {
        if (err.code !== 'ENOENT') {
          console.error('Error loading consents:', err);
        }
        // Initialize with empty consents
        this.consents = {};
        await this._saveConsents();
      }

      this.initialized = true;
    } catch (error) {
      console.error('Failed to initialize consent manager:', error);
      throw error;
    }
  }

  /**
   * Request consent for an operation
   * @param {Object} request - Consent request details
   * @returns {Promise<Object>} Consent decision
   */
  async requestConsent(request) {
    const {
      type,           // 'download', 'update_check', 'telemetry', 'external_api'
      purpose,        // Human-readable purpose
      url,            // Optional URL being accessed
      duration,       // 'once', 'session', 'always'
      metadata = {}   // Additional context
    } = request;

    // Validate request
    if (!type || !purpose || !duration) {
      throw new Error('Invalid consent request: missing required fields');
    }

    // Generate consent key
    const consentKey = this._generateConsentKey(type, url);

    // Check existing consent
    const existing = this.consents[consentKey];
    if (existing && this._isConsentValid(existing)) {
      return {
        granted: existing.granted,
        duration: existing.duration,
        grantedAt: existing.grantedAt,
        fromCache: true
      };
    }

    // Create prompt
    const promptId = crypto.randomBytes(16).toString('hex');
    const prompt = {
      id: promptId,
      type,
      purpose,
      url,
      duration,
      metadata,
      requestedAt: new Date().toISOString()
    };

    // Store pending prompt
    this.pendingPrompts.set(promptId, {
      ...prompt,
      resolve: null,
      reject: null
    });

    // Return prompt for UI display
    return {
      requiresPrompt: true,
      promptId,
      prompt
    };
  }

  /**
   * Respond to a consent prompt
   * @param {string} promptId - Prompt identifier
   * @param {boolean} granted - Whether consent was granted
   * @param {string} duration - Duration of consent
   * @returns {Promise<Object>} Updated consent
   */
  async respondToPrompt(promptId, granted, duration = 'once') {
    const pending = this.pendingPrompts.get(promptId);
    if (!pending) {
      throw new Error(`No pending prompt found: ${promptId}`);
    }

    const { type, url, purpose, metadata } = pending;
    const consentKey = this._generateConsentKey(type, url);

    // Create consent record
    const consent = {
      type,
      purpose,
      url,
      granted,
      duration,
      grantedAt: new Date().toISOString(),
      metadata
    };

    // Store consent
    this.consents[consentKey] = consent;
    await this._saveConsents();

    // Remove pending prompt
    this.pendingPrompts.delete(promptId);

    return consent;
  }

  /**
   * Get all consent records
   */
  getAllConsents() {
    return Object.entries(this.consents).map(([key, consent]) => ({
      key,
      ...consent,
      valid: this._isConsentValid(consent)
    }));
  }

  /**
   * Revoke consent for a specific operation
   * @param {string} consentKey - Consent key to revoke
   */
  async revokeConsent(consentKey) {
    if (!this.consents[consentKey]) {
      throw new Error(`Consent not found: ${consentKey}`);
    }

    delete this.consents[consentKey];
    await this._saveConsents();

    return { revoked: true, key: consentKey };
  }

  /**
   * Revoke all consents of a specific type
   * @param {string} type - Consent type to revoke
   */
  async revokeConsentsByType(type) {
    const keys = Object.keys(this.consents).filter(key =>
      this.consents[key].type === type
    );

    keys.forEach(key => delete this.consents[key]);
    await this._saveConsents();

    return { revoked: keys.length, keys };
  }

  /**
   * Clear all consents
   */
  async clearAllConsents() {
    this.consents = {};
    await this._saveConsents();
    return { cleared: true };
  }

  /**
   * Get consent statistics
   */
  getConsentStats() {
    const all = this.getAllConsents();
    const byType = {};

    all.forEach(consent => {
      if (!byType[consent.type]) {
        byType[consent.type] = { total: 0, granted: 0, denied: 0, valid: 0 };
      }
      byType[consent.type].total++;
      if (consent.granted) byType[consent.type].granted++;
      else byType[consent.type].denied++;
      if (consent.valid) byType[consent.type].valid++;
    });

    return {
      total: all.length,
      byType,
      pendingPrompts: this.pendingPrompts.size
    };
  }

  /**
   * Export consents for backup
   */
  async exportConsents() {
    return {
      version: '1.0',
      exportedAt: new Date().toISOString(),
      consents: this.consents
    };
  }

  /**
   * Import consents from backup
   * @param {Object} data - Export data
   * @param {boolean} merge - Whether to merge or replace
   */
  async importConsents(data, merge = false) {
    if (!data.consents) {
      throw new Error('Invalid consent export data');
    }

    if (merge) {
      this.consents = { ...this.consents, ...data.consents };
    } else {
      this.consents = data.consents;
    }

    await this._saveConsents();

    return {
      imported: Object.keys(data.consents).length,
      merge
    };
  }

  /**
   * Generate consent key from type and URL
   */
  _generateConsentKey(type, url = '') {
    const normalized = url ? new URL(url).origin : '';
    return `${type}:${normalized || 'local'}`;
  }

  /**
   * Check if consent is still valid
   */
  _isConsentValid(consent) {
    if (!consent.granted) return false;
    if (consent.duration === 'always') return true;
    if (consent.duration === 'once') return false;
    if (consent.duration === 'session') {
      // Session consents are cleared on restart
      // In current session, they remain valid
      return true;
    }
    return false;
  }

  /**
   * Save consents to disk
   */
  async _saveConsents() {
    const data = {
      version: '1.0',
      updatedAt: new Date().toISOString(),
      consents: this.consents
    };

    try {
      await fs.writeFile(
        this.consentFilePath,
        JSON.stringify(data, null, 2),
        'utf8'
      );
    } catch (error) {
      console.error('Failed to save consents:', error);
      throw error;
    }
  }

  /**
   * Clear session consents (call on app restart)
   */
  async clearSessionConsents() {
    const keys = Object.keys(this.consents).filter(key =>
      this.consents[key].duration === 'session'
    );

    keys.forEach(key => delete this.consents[key]);

    if (keys.length > 0) {
      await this._saveConsents();
    }

    return { cleared: keys.length };
  }

  /**
   * Get pending prompts for UI
   */
  getPendingPrompts() {
    return Array.from(this.pendingPrompts.values()).map(p => ({
      id: p.id,
      type: p.type,
      purpose: p.purpose,
      url: p.url,
      duration: p.duration,
      metadata: p.metadata,
      requestedAt: p.requestedAt
    }));
  }
}

module.exports = { ConsentDialogManager };
