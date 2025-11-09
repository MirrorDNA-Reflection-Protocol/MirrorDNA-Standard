const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const crypto = require('crypto');
const { EventEmitter } = require('events');

/**
 * MirrorDNA Model Downloader
 *
 * Manages downloading, verification, and management of LLM models
 * from Hugging Face and other sources.
 */
class ModelDownloader extends EventEmitter {
  constructor(modelsPath) {
    super();
    this.modelsPath = modelsPath;
    this.activeDownloads = new Map();
    this.modelRegistry = this.getModelRegistry();
  }

  /**
   * Get registry of available models
   */
  getModelRegistry() {
    return {
      'phi3-mini-4k': {
        name: 'Phi-3 Mini 4K',
        provider: 'Microsoft',
        size: '2.3 GB',
        sizeBytes: 2469606195, // Approximate
        quantization: 'Q4_K_M',
        url: 'https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf',
        filename: 'phi3-mini-4k.Q4_K_M.gguf',
        checksum: null, // Will be updated from Hugging Face
        description: 'Best balance of quality and speed for reflection',
        recommended: true,
        contextSize: 4096,
        requirements: {
          ram: '4 GB',
          storage: '3 GB'
        }
      },
      'llama-3.2-3b': {
        name: 'Llama 3.2 3B',
        provider: 'Meta',
        size: '2.0 GB',
        sizeBytes: 2147483648,
        quantization: 'Q4_K_M',
        url: 'https://huggingface.co/lmstudio-community/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf',
        filename: 'llama-3.2-3b-instruct.Q4_K_M.gguf',
        checksum: null,
        description: 'Alternative to Phi-3, similar quality',
        recommended: false,
        contextSize: 4096,
        requirements: {
          ram: '4 GB',
          storage: '3 GB'
        }
      },
      'mistral-7b': {
        name: 'Mistral 7B Instruct',
        provider: 'Mistral AI',
        size: '4.1 GB',
        sizeBytes: 4402341478,
        quantization: 'Q4_K_M',
        url: 'https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf',
        filename: 'mistral-7b-instruct-v0.2.Q4_K_M.gguf',
        checksum: null,
        description: 'Higher quality, requires more RAM',
        recommended: false,
        contextSize: 8192,
        requirements: {
          ram: '8 GB',
          storage: '5 GB'
        }
      }
    };
  }

  /**
   * Get list of available models
   */
  getAvailableModels() {
    return Object.entries(this.modelRegistry).map(([id, model]) => ({
      id,
      ...model,
      installed: this.isModelInstalled(model.filename),
      installedPath: this.isModelInstalled(model.filename)
        ? path.join(this.modelsPath, model.filename)
        : null
    }));
  }

  /**
   * Check if a model is installed
   */
  isModelInstalled(filename) {
    const modelPath = path.join(this.modelsPath, filename);
    return fs.existsSync(modelPath);
  }

  /**
   * Get installed models
   */
  getInstalledModels() {
    if (!fs.existsSync(this.modelsPath)) {
      return [];
    }

    const files = fs.readdirSync(this.modelsPath);
    const installedModels = [];

    for (const file of files) {
      if (file.endsWith('.gguf')) {
        const filePath = path.join(this.modelsPath, file);
        const stats = fs.statSync(filePath);

        // Find matching model in registry
        const registryEntry = Object.entries(this.modelRegistry).find(
          ([id, model]) => model.filename === file
        );

        installedModels.push({
          filename: file,
          path: filePath,
          size: stats.size,
          sizeFormatted: this.formatBytes(stats.size),
          installedDate: stats.mtime,
          registryMatch: registryEntry ? {
            id: registryEntry[0],
            ...registryEntry[1]
          } : null
        });
      }
    }

    return installedModels;
  }

  /**
   * Download a model
   * @param {string} modelId - Model ID from registry
   * @param {Object} options - Download options
   */
  async downloadModel(modelId, options = {}) {
    const model = this.modelRegistry[modelId];

    if (!model) {
      throw new Error(`Model not found: ${modelId}`);
    }

    // Check if already downloading
    if (this.activeDownloads.has(modelId)) {
      throw new Error(`Model ${modelId} is already being downloaded`);
    }

    // Check if already installed
    if (this.isModelInstalled(model.filename) && !options.force) {
      throw new Error(`Model ${modelId} is already installed`);
    }

    // Ensure models directory exists
    if (!fs.existsSync(this.modelsPath)) {
      fs.mkdirSync(this.modelsPath, { recursive: true });
    }

    const targetPath = path.join(this.modelsPath, model.filename);
    const tempPath = `${targetPath}.download`;

    // Create download state
    const downloadState = {
      modelId,
      model,
      targetPath,
      tempPath,
      startTime: Date.now(),
      bytesDownloaded: 0,
      totalBytes: model.sizeBytes,
      speed: 0,
      progress: 0,
      status: 'downloading',
      error: null,
      cancelled: false,
      request: null
    };

    this.activeDownloads.set(modelId, downloadState);

    return new Promise((resolve, reject) => {
      try {
        const fileStream = fs.createWriteStream(tempPath);
        const url = new URL(model.url);
        const protocol = url.protocol === 'https:' ? https : http;

        const request = protocol.get(model.url, {
          headers: {
            'User-Agent': 'MirrorDNA-Portable/1.0'
          }
        }, (response) => {
          // Handle redirects
          if (response.statusCode === 301 || response.statusCode === 302) {
            const redirectUrl = response.headers.location;
            console.log(`Following redirect to: ${redirectUrl}`);

            // Clean up current request
            request.destroy();
            fileStream.destroy();

            // Update URL and retry
            model.url = redirectUrl;
            this.downloadModel(modelId, options).then(resolve).catch(reject);
            return;
          }

          if (response.statusCode !== 200) {
            const error = new Error(`Download failed: HTTP ${response.statusCode}`);
            this.handleDownloadError(modelId, error);
            reject(error);
            return;
          }

          const totalBytes = parseInt(response.headers['content-length'], 10);
          downloadState.totalBytes = totalBytes || model.sizeBytes;

          let lastUpdate = Date.now();
          let lastBytes = 0;

          response.on('data', (chunk) => {
            if (downloadState.cancelled) {
              request.destroy();
              fileStream.destroy();
              return;
            }

            downloadState.bytesDownloaded += chunk.length;

            // Calculate speed and progress
            const now = Date.now();
            const timeDiff = (now - lastUpdate) / 1000; // seconds

            if (timeDiff >= 0.5) { // Update every 500ms
              const bytesDiff = downloadState.bytesDownloaded - lastBytes;
              downloadState.speed = bytesDiff / timeDiff; // bytes/sec
              downloadState.progress = (downloadState.bytesDownloaded / downloadState.totalBytes) * 100;

              this.emit('download-progress', {
                modelId,
                bytesDownloaded: downloadState.bytesDownloaded,
                totalBytes: downloadState.totalBytes,
                progress: downloadState.progress,
                speed: downloadState.speed,
                speedFormatted: this.formatSpeed(downloadState.speed),
                eta: this.calculateETA(downloadState)
              });

              lastUpdate = now;
              lastBytes = downloadState.bytesDownloaded;
            }
          });

          response.pipe(fileStream);

          fileStream.on('finish', async () => {
            fileStream.close();

            // Verify download
            try {
              const fileSize = fs.statSync(tempPath).size;

              if (totalBytes && fileSize !== totalBytes) {
                throw new Error(`Download incomplete: ${fileSize} bytes (expected ${totalBytes})`);
              }

              // Compute checksum if we have one to verify against
              if (model.checksum && options.verify !== false) {
                console.log('⟡ Verifying checksum...');
                const actualChecksum = await this.computeFileChecksum(tempPath);

                if (actualChecksum !== model.checksum) {
                  throw new Error('Checksum verification failed');
                }
                console.log('✓ Checksum verified');
              }

              // Move from temp to final location
              if (fs.existsSync(targetPath)) {
                fs.unlinkSync(targetPath);
              }
              fs.renameSync(tempPath, targetPath);

              downloadState.status = 'completed';
              this.activeDownloads.delete(modelId);

              this.emit('download-complete', {
                modelId,
                model,
                path: targetPath,
                size: fileSize,
                duration: Date.now() - downloadState.startTime
              });

              resolve({
                success: true,
                modelId,
                path: targetPath,
                size: fileSize
              });

            } catch (error) {
              // Clean up temp file on error
              if (fs.existsSync(tempPath)) {
                fs.unlinkSync(tempPath);
              }

              this.handleDownloadError(modelId, error);
              reject(error);
            }
          });

          fileStream.on('error', (error) => {
            this.handleDownloadError(modelId, error);
            reject(error);
          });
        });

        request.on('error', (error) => {
          this.handleDownloadError(modelId, error);
          reject(error);
        });

        downloadState.request = request;

      } catch (error) {
        this.handleDownloadError(modelId, error);
        reject(error);
      }
    });
  }

  /**
   * Cancel a download
   */
  cancelDownload(modelId) {
    const download = this.activeDownloads.get(modelId);

    if (!download) {
      return { success: false, error: 'Download not found' };
    }

    download.cancelled = true;

    if (download.request) {
      download.request.destroy();
    }

    // Clean up temp file
    if (fs.existsSync(download.tempPath)) {
      fs.unlinkSync(download.tempPath);
    }

    this.activeDownloads.delete(modelId);

    this.emit('download-cancelled', { modelId });

    return { success: true };
  }

  /**
   * Delete a model
   */
  deleteModel(filename) {
    try {
      const modelPath = path.join(this.modelsPath, filename);

      if (!fs.existsSync(modelPath)) {
        return { success: false, error: 'Model not found' };
      }

      fs.unlinkSync(modelPath);

      this.emit('model-deleted', { filename });

      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Verify model checksum
   */
  async verifyModel(filename, expectedChecksum) {
    try {
      const modelPath = path.join(this.modelsPath, filename);

      if (!fs.existsSync(modelPath)) {
        return { valid: false, error: 'Model not found' };
      }

      const actualChecksum = await this.computeFileChecksum(modelPath);

      if (!expectedChecksum) {
        return { valid: true, checksum: actualChecksum, verified: false };
      }

      const valid = actualChecksum === expectedChecksum;

      return {
        valid,
        checksum: actualChecksum,
        expected: expectedChecksum,
        verified: true
      };
    } catch (error) {
      return { valid: false, error: error.message };
    }
  }

  /**
   * Compute SHA-256 checksum of a file
   */
  computeFileChecksum(filePath) {
    return new Promise((resolve, reject) => {
      const hash = crypto.createHash('sha256');
      const stream = fs.createReadStream(filePath);

      stream.on('data', (chunk) => hash.update(chunk));
      stream.on('end', () => resolve(hash.digest('hex')));
      stream.on('error', reject);
    });
  }

  /**
   * Get active downloads
   */
  getActiveDownloads() {
    const downloads = [];

    for (const [modelId, state] of this.activeDownloads) {
      downloads.push({
        modelId,
        modelName: state.model.name,
        bytesDownloaded: state.bytesDownloaded,
        totalBytes: state.totalBytes,
        progress: state.progress,
        speed: state.speed,
        speedFormatted: this.formatSpeed(state.speed),
        eta: this.calculateETA(state),
        status: state.status
      });
    }

    return downloads;
  }

  /**
   * Handle download error
   */
  handleDownloadError(modelId, error) {
    const download = this.activeDownloads.get(modelId);

    if (download) {
      download.status = 'failed';
      download.error = error.message;

      // Clean up temp file
      if (fs.existsSync(download.tempPath)) {
        try {
          fs.unlinkSync(download.tempPath);
        } catch (e) {
          console.error('Failed to clean up temp file:', e);
        }
      }

      this.emit('download-error', {
        modelId,
        error: error.message
      });

      this.activeDownloads.delete(modelId);
    }
  }

  /**
   * Calculate estimated time to completion
   */
  calculateETA(downloadState) {
    if (downloadState.speed === 0) {
      return 'Calculating...';
    }

    const remaining = downloadState.totalBytes - downloadState.bytesDownloaded;
    const secondsRemaining = remaining / downloadState.speed;

    return this.formatDuration(secondsRemaining);
  }

  /**
   * Format bytes to human-readable string
   */
  formatBytes(bytes) {
    if (bytes === 0) return '0 B';

    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  /**
   * Format speed to human-readable string
   */
  formatSpeed(bytesPerSecond) {
    return this.formatBytes(bytesPerSecond) + '/s';
  }

  /**
   * Format duration to human-readable string
   */
  formatDuration(seconds) {
    if (seconds < 60) {
      return `${Math.round(seconds)}s`;
    } else if (seconds < 3600) {
      const minutes = Math.floor(seconds / 60);
      const secs = Math.round(seconds % 60);
      return `${minutes}m ${secs}s`;
    } else {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      return `${hours}h ${minutes}m`;
    }
  }
}

module.exports = ModelDownloader;
