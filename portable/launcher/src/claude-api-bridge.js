/**
 * Claude API Bridge
 *
 * Connects to Claude API for cloud-enhanced reflection.
 * Implements consent-based API access with fallback to local LLM.
 *
 * Part of MirrorDNA Portable Launcher - Phase 3
 */

const https = require('https');
const { EventEmitter } = require('events');

class ClaudeAPIBridge extends EventEmitter {
  constructor(options = {}) {
    super();
    this.apiKey = null;
    this.model = options.model || 'claude-sonnet-4-20250514';
    this.baseUrl = 'api.anthropic.com';
    this.apiVersion = '2023-06-01';
    this.maxTokens = options.maxTokens || 4096;
    this.temperature = options.temperature || 1.0;

    // Statistics
    this.stats = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      totalInputTokens: 0,
      totalOutputTokens: 0,
      lastRequestTime: null
    };
  }

  /**
   * Set API key
   * @param {string} apiKey - Anthropic API key
   */
  setApiKey(apiKey) {
    if (!apiKey || !apiKey.startsWith('sk-ant-')) {
      throw new Error('Invalid API key format. Must start with "sk-ant-"');
    }
    this.apiKey = apiKey;
  }

  /**
   * Check if API key is configured
   * @returns {boolean}
   */
  hasApiKey() {
    return !!this.apiKey;
  }

  /**
   * Generate reflection using Claude API
   * @param {string} prompt - User prompt
   * @param {Object} context - Additional context (Master Citation, session state)
   * @param {Object} options - Generation options
   * @returns {Promise<Object>} Response with reflection
   */
  async generateReflection(prompt, context = {}, options = {}) {
    if (!this.hasApiKey()) {
      return {
        success: false,
        error: 'No API key configured',
        requiresApiKey: true
      };
    }

    const {
      stream = false,
      systemPrompt = null,
      sessionHistory = []
    } = options;

    try {
      this.stats.totalRequests++;
      this.stats.lastRequestTime = new Date().toISOString();

      // Build system prompt
      const system = this._buildSystemPrompt(systemPrompt, context);

      // Build messages
      const messages = this._buildMessages(prompt, sessionHistory);

      // Make API request
      const response = await this._makeRequest({
        model: this.model,
        max_tokens: this.maxTokens,
        temperature: this.temperature,
        system,
        messages,
        stream
      });

      this.stats.successfulRequests++;

      // Update token stats
      if (response.usage) {
        this.stats.totalInputTokens += response.usage.input_tokens || 0;
        this.stats.totalOutputTokens += response.usage.output_tokens || 0;
      }

      return {
        success: true,
        content: response.content[0].text,
        model: response.model,
        usage: response.usage,
        stopReason: response.stop_reason
      };
    } catch (error) {
      this.stats.failedRequests++;

      return {
        success: false,
        error: error.message,
        code: error.code,
        type: error.type
      };
    }
  }

  /**
   * Generate reflection with streaming
   * @param {string} prompt - User prompt
   * @param {Object} context - Additional context
   * @param {Object} options - Generation options
   * @returns {Promise<void>} Emits 'stream-start', 'stream-chunk', 'stream-end', 'stream-error'
   */
  async generateReflectionStream(prompt, context = {}, options = {}) {
    if (!this.hasApiKey()) {
      this.emit('stream-error', { error: 'No API key configured' });
      return;
    }

    const {
      systemPrompt = null,
      sessionHistory = []
    } = options;

    try {
      this.stats.totalRequests++;
      this.stats.lastRequestTime = new Date().toISOString();

      // Build system prompt and messages
      const system = this._buildSystemPrompt(systemPrompt, context);
      const messages = this._buildMessages(prompt, sessionHistory);

      // Make streaming request
      await this._makeStreamingRequest({
        model: this.model,
        max_tokens: this.maxTokens,
        temperature: this.temperature,
        system,
        messages,
        stream: true
      });

      this.stats.successfulRequests++;
    } catch (error) {
      this.stats.failedRequests++;
      this.emit('stream-error', { error: error.message });
    }
  }

  /**
   * Get usage statistics
   */
  getStats() {
    return {
      ...this.stats,
      averageInputTokens: this.stats.successfulRequests > 0
        ? Math.round(this.stats.totalInputTokens / this.stats.successfulRequests)
        : 0,
      averageOutputTokens: this.stats.successfulRequests > 0
        ? Math.round(this.stats.totalOutputTokens / this.stats.successfulRequests)
        : 0,
      successRate: this.stats.totalRequests > 0
        ? (this.stats.successfulRequests / this.stats.totalRequests * 100).toFixed(2)
        : 0
    };
  }

  /**
   * Reset statistics
   */
  resetStats() {
    this.stats = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      totalInputTokens: 0,
      totalOutputTokens: 0,
      lastRequestTime: null
    };
  }

  /**
   * Test API connection
   */
  async testConnection() {
    if (!this.hasApiKey()) {
      return { success: false, error: 'No API key configured' };
    }

    try {
      const response = await this.generateReflection(
        'Respond with "Connection successful" only.',
        {},
        { systemPrompt: 'You are a connection test. Be brief.' }
      );

      return {
        success: response.success,
        message: response.success ? 'API connection verified' : response.error,
        model: response.model
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Build system prompt from context
   */
  _buildSystemPrompt(customPrompt, context) {
    let prompt = '';

    // Add Master Citation if available
    if (context.masterCitation) {
      prompt += `${context.masterCitation}\n\n`;
    }

    // Add session state if available
    if (context.sessionState) {
      prompt += `## Current Session State\n\n`;
      prompt += `Session: ${context.sessionState.sessionNumber || 'Unknown'}\n`;
      if (context.sessionState.predecessor) {
        prompt += `Previous: ${context.sessionState.predecessor}\n`;
      }
      prompt += '\n';
    }

    // Add custom system prompt
    if (customPrompt) {
      prompt += customPrompt;
    } else {
      // Default MirrorDNA system prompt
      prompt += `You are a reflective AI assistant following the MirrorDNA protocol. `;
      prompt += `Provide thoughtful, constitutive reflections that help users explore their thinking. `;
      prompt += `Honor the Tri-Twin Architecture: respect sovereignty, maintain continuity, embrace transparency.`;
    }

    return prompt;
  }

  /**
   * Build messages array for API
   */
  _buildMessages(prompt, sessionHistory = []) {
    const messages = [];

    // Add session history if provided
    sessionHistory.forEach(msg => {
      if (msg.role && msg.content) {
        messages.push({
          role: msg.role, // 'user' or 'assistant'
          content: msg.content
        });
      }
    });

    // Add current prompt
    messages.push({
      role: 'user',
      content: prompt
    });

    return messages;
  }

  /**
   * Make HTTPS request to Claude API
   */
  async _makeRequest(body) {
    return new Promise((resolve, reject) => {
      const bodyData = JSON.stringify(body);

      const options = {
        hostname: this.baseUrl,
        path: '/v1/messages',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.apiKey,
          'anthropic-version': this.apiVersion,
          'Content-Length': Buffer.byteLength(bodyData)
        }
      };

      const req = https.request(options, (res) => {
        let data = '';

        res.on('data', (chunk) => {
          data += chunk;
        });

        res.on('end', () => {
          try {
            const response = JSON.parse(data);

            if (res.statusCode === 200) {
              resolve(response);
            } else {
              reject({
                message: response.error?.message || 'API request failed',
                type: response.error?.type,
                code: res.statusCode
              });
            }
          } catch (error) {
            reject({
              message: 'Failed to parse API response',
              code: res.statusCode
            });
          }
        });
      });

      req.on('error', (error) => {
        reject({
          message: `Network error: ${error.message}`,
          code: 'NETWORK_ERROR'
        });
      });

      req.write(bodyData);
      req.end();
    });
  }

  /**
   * Make streaming HTTPS request to Claude API
   */
  async _makeStreamingRequest(body) {
    return new Promise((resolve, reject) => {
      const bodyData = JSON.stringify(body);

      const options = {
        hostname: this.baseUrl,
        path: '/v1/messages',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.apiKey,
          'anthropic-version': this.apiVersion,
          'Content-Length': Buffer.byteLength(bodyData)
        }
      };

      const req = https.request(options, (res) => {
        let buffer = '';
        let fullContent = '';
        let usage = null;

        this.emit('stream-start', { model: this.model });

        res.on('data', (chunk) => {
          buffer += chunk.toString();
          const lines = buffer.split('\n');

          // Keep last incomplete line in buffer
          buffer = lines.pop() || '';

          lines.forEach(line => {
            if (line.startsWith('data: ')) {
              const data = line.slice(6);

              if (data === '[DONE]') {
                return;
              }

              try {
                const event = JSON.parse(data);

                if (event.type === 'content_block_delta') {
                  const text = event.delta?.text || '';
                  fullContent += text;
                  this.emit('stream-chunk', { text, fullContent });
                } else if (event.type === 'message_delta') {
                  usage = event.usage;
                } else if (event.type === 'message_stop') {
                  this.emit('stream-end', {
                    content: fullContent,
                    usage,
                    model: this.model
                  });
                }
              } catch (error) {
                // Skip invalid JSON lines
              }
            }
          });
        });

        res.on('end', () => {
          resolve();
        });
      });

      req.on('error', (error) => {
        reject({
          message: `Network error: ${error.message}`,
          code: 'NETWORK_ERROR'
        });
      });

      req.write(bodyData);
      req.end();
    });
  }
}

module.exports = { ClaudeAPIBridge };
