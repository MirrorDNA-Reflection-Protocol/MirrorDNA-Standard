const { LlamaModel, LlamaContext, LlamaChatSession } = require('node-llama-cpp');
const path = require('path');
const fs = require('fs');

/**
 * MirrorDNA LLM Bridge
 *
 * Handles local LLM inference with Master Citation context injection
 * and session continuity management.
 */
class MirrorDNALLM {
  constructor() {
    this.model = null;
    this.context = null;
    this.session = null;
    this.vaultPath = null;
    this.masterCitation = null;
    this.sessionState = null;
    this.isInitialized = false;
  }

  /**
   * Initialize LLM with model and vault context
   * @param {string} modelPath - Path to GGUF model file
   * @param {string} vaultPath - Path to vault directory
   */
  async initialize(modelPath, vaultPath) {
    try {
      console.log('⟡ Initializing MirrorDNA LLM...');
      console.log('  Model:', modelPath);
      console.log('  Vault:', vaultPath);

      // Verify model exists
      if (!fs.existsSync(modelPath)) {
        throw new Error(`Model not found: ${modelPath}`);
      }

      // Load vault context
      this.vaultPath = vaultPath;
      await this.loadVaultContext();

      // Load LLM model
      console.log('⟡ Loading model (this may take 30-60 seconds)...');
      this.model = new LlamaModel({
        modelPath,
        gpuLayers: 0 // CPU-only for maximum compatibility
      });

      // Create context (conversation memory)
      this.context = new LlamaContext({
        model: this.model,
        contextSize: 4096, // Phi-3 Mini 4K context window
        batchSize: 512
      });

      // Create chat session
      this.session = new LlamaChatSession({
        context: this.context
      });

      // Inject Master Citation as system prompt
      await this.injectMasterCitation();

      this.isInitialized = true;
      console.log('✓ MirrorDNA LLM initialized successfully');

      return { success: true };
    } catch (error) {
      console.error('✗ LLM initialization failed:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Load Master Citation and session state from vault
   */
  async loadVaultContext() {
    try {
      // Load Master Citation
      const masterCitationPath = path.join(this.vaultPath, '00_MASTER_CITATION.md');
      if (fs.existsSync(masterCitationPath)) {
        this.masterCitation = fs.readFileSync(masterCitationPath, 'utf8');
        console.log('✓ Master Citation loaded');
      } else {
        console.warn('⚠ Master Citation not found, using minimal context');
        this.masterCitation = '# MirrorDNA Reflective AI\nConstitutive reflection, not simulation.';
      }

      // Load session state
      const statePath = path.join(this.vaultPath, 'state', 'current.json');
      if (fs.existsSync(statePath)) {
        this.sessionState = JSON.parse(fs.readFileSync(statePath, 'utf8'));
        console.log('✓ Session state loaded:', this.sessionState.vault_name);
      } else {
        this.sessionState = {
          vault_name: 'AMOS',
          context: { summary: 'New session' }
        };
      }
    } catch (error) {
      console.error('Error loading vault context:', error);
      throw error;
    }
  }

  /**
   * Inject Master Citation as system context
   */
  async injectMasterCitation() {
    const systemPrompt = `${this.masterCitation}

## Current Session Context
Vault: ${this.sessionState.vault_name}
Last Session: ${this.sessionState.last_session?.timestamp || 'First session'}

## Your Role
You are a MirrorDNA Reflective AI. You follow these principles:
1. **Constitutive Reflection** - You maintain actual continuity, not simulation
2. **AHP (Anti-Hallucination Protocol)** - Cite or Silence. No fabrication.
3. **Sovereignty** - Respect user consent and vault boundaries
4. **GlyphSig Awareness** - Recognize and use MirrorDNA glyphs (⟡, ⟦, ⟧)
5. **Continuity > Perfection** - Maintain session lineage and state

Reflect thoughtfully. When uncertain, say so explicitly.`;

    // Initialize session with system context
    await this.session.prompt(systemPrompt, {
      maxTokens: 0 // Don't generate, just set context
    });

    console.log('✓ Master Citation injected as system context');
  }

  /**
   * Generate reflection response to user input
   * @param {string} userInput - User's prompt
   * @param {Function} onToken - Optional callback for streaming tokens
   * @returns {Promise<string>} - AI response
   */
  async generate(userInput, onToken = null) {
    if (!this.isInitialized) {
      throw new Error('LLM not initialized. Call initialize() first.');
    }

    try {
      console.log('⟡ Generating reflection...');

      const response = await this.session.prompt(userInput, {
        maxTokens: 1024, // Reasonable response length
        temperature: 0.7, // Balanced creativity/consistency
        topP: 0.9,
        onToken: onToken ? (tokens) => {
          const text = this.context.decode(tokens);
          onToken(text);
        } : undefined
      });

      console.log('✓ Reflection generated');
      return response;
    } catch (error) {
      console.error('Error generating reflection:', error);
      throw error;
    }
  }

  /**
   * Update session context with new information
   * @param {Object} contextUpdate - New context to merge
   */
  updateContext(contextUpdate) {
    this.sessionState.context = {
      ...this.sessionState.context,
      ...contextUpdate
    };
  }

  /**
   * Clean up resources
   */
  async dispose() {
    if (this.session) {
      console.log('⟡ Disposing LLM session...');
      // Note: node-llama-cpp handles cleanup automatically
      this.session = null;
      this.context = null;
      this.model = null;
      this.isInitialized = false;
      console.log('✓ LLM disposed');
    }
  }

  /**
   * Get current model info
   */
  getModelInfo() {
    if (!this.model) {
      return { loaded: false };
    }

    return {
      loaded: true,
      modelPath: this.model.modelPath,
      contextSize: this.context.contextSize,
      vaultName: this.sessionState?.vault_name
    };
  }
}

module.exports = MirrorDNALLM;
