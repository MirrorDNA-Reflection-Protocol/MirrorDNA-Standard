/**
 * Checksum Verifier
 *
 * Provides checksum verification for vault files with UI feedback.
 * Validates file integrity and displays verification results.
 *
 * Part of MirrorDNA Portable Launcher - Phase 2
 */

const fs = require('fs').promises;
const crypto = require('crypto');
const path = require('path');
const { glob } = require('glob');

class ChecksumVerifier {
  constructor(vaultPath) {
    this.vaultPath = vaultPath;
    this.verificationCache = new Map();
  }

  /**
   * Verify checksum for a single file
   * @param {string} filePath - Absolute path to file
   * @param {string} expectedChecksum - Expected SHA-256 checksum (optional)
   * @returns {Promise<Object>} Verification result
   */
  async verifyFile(filePath, expectedChecksum = null) {
    try {
      // Read file
      const content = await fs.readFile(filePath, 'utf8');

      // Check for frontmatter
      const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);

      let actualChecksum, bodyContent, frontmatter = null;

      if (frontmatterMatch) {
        const frontmatterText = frontmatterMatch[1];
        bodyContent = frontmatterMatch[2];

        // Parse frontmatter for checksum
        const checksumMatch = frontmatterText.match(/checksum_sha256:\s*["']?([a-f0-9]{64})["']?/i);

        if (checksumMatch && !expectedChecksum) {
          expectedChecksum = checksumMatch[1];
        }

        frontmatter = this._parseFrontmatter(frontmatterText);
      } else {
        bodyContent = content;
      }

      // Calculate actual checksum (body only, excluding frontmatter)
      actualChecksum = this._calculateChecksum(bodyContent);

      const valid = expectedChecksum ? actualChecksum === expectedChecksum : null;
      const relativePath = path.relative(this.vaultPath, filePath);

      const result = {
        filePath: relativePath,
        absolutePath: filePath,
        actualChecksum,
        expectedChecksum,
        valid,
        hasFrontmatter: !!frontmatter,
        frontmatter,
        verifiedAt: new Date().toISOString()
      };

      // Cache result
      this.verificationCache.set(filePath, result);

      return result;
    } catch (error) {
      return {
        filePath: path.relative(this.vaultPath, filePath),
        absolutePath: filePath,
        error: error.message,
        valid: false,
        verifiedAt: new Date().toISOString()
      };
    }
  }

  /**
   * Verify all markdown files in vault
   * @param {Object} options - Verification options
   * @returns {Promise<Object>} Verification results
   */
  async verifyVault(options = {}) {
    const {
      pattern = '**/*.md',
      excludePatterns = ['node_modules/**', '.git/**'],
      includeNoChecksum = false
    } = options;

    try {
      // Find all markdown files
      const files = await glob(pattern, {
        cwd: this.vaultPath,
        ignore: excludePatterns,
        absolute: true
      });

      const results = [];
      let stats = {
        total: files.length,
        verified: 0,
        valid: 0,
        invalid: 0,
        noChecksum: 0,
        errors: 0
      };

      // Verify each file
      for (const file of files) {
        const result = await this.verifyFile(file);

        if (result.error) {
          stats.errors++;
        } else if (result.expectedChecksum === null) {
          stats.noChecksum++;
          if (includeNoChecksum) {
            results.push(result);
          }
        } else {
          stats.verified++;
          if (result.valid) {
            stats.valid++;
          } else {
            stats.invalid++;
          }
          results.push(result);
        }
      }

      return {
        success: true,
        results,
        stats,
        verifiedAt: new Date().toISOString()
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        results: [],
        stats: {}
      };
    }
  }

  /**
   * Verify specific session files
   * @param {Array<string>} sessionPaths - Paths to session files
   * @returns {Promise<Object>} Verification results
   */
  async verifySessions(sessionPaths) {
    const results = [];

    for (const sessionPath of sessionPaths) {
      const absolutePath = path.isAbsolute(sessionPath)
        ? sessionPath
        : path.join(this.vaultPath, sessionPath);

      const result = await this.verifyFile(absolutePath);
      results.push(result);
    }

    const stats = {
      total: results.length,
      valid: results.filter(r => r.valid === true).length,
      invalid: results.filter(r => r.valid === false && !r.error).length,
      errors: results.filter(r => r.error).length
    };

    return {
      success: true,
      results,
      stats
    };
  }

  /**
   * Update checksum in file frontmatter
   * @param {string} filePath - Path to file
   * @returns {Promise<Object>} Update result
   */
  async updateChecksum(filePath) {
    try {
      const content = await fs.readFile(filePath, 'utf8');

      // Check for frontmatter
      const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);

      if (!frontmatterMatch) {
        return {
          success: false,
          error: 'No frontmatter found in file'
        };
      }

      const frontmatterText = frontmatterMatch[1];
      const bodyContent = frontmatterMatch[2];

      // Calculate correct checksum
      const correctChecksum = this._calculateChecksum(bodyContent);

      // Update checksum in frontmatter
      let updatedFrontmatter;
      if (frontmatterText.includes('checksum_sha256:')) {
        // Replace existing checksum
        updatedFrontmatter = frontmatterText.replace(
          /checksum_sha256:\s*["']?[a-f0-9]{64}["']?/i,
          `checksum_sha256: ${correctChecksum}`
        );
      } else {
        // Add checksum field
        updatedFrontmatter = frontmatterText + `\nchecksum_sha256: ${correctChecksum}`;
      }

      // Write updated content
      const updatedContent = `---\n${updatedFrontmatter}\n---\n${bodyContent}`;
      await fs.writeFile(filePath, updatedContent, 'utf8');

      // Clear cache
      this.verificationCache.delete(filePath);

      return {
        success: true,
        filePath: path.relative(this.vaultPath, filePath),
        checksum: correctChecksum,
        updatedAt: new Date().toISOString()
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Batch update checksums for multiple files
   * @param {Array<string>} filePaths - Paths to files
   * @returns {Promise<Object>} Batch update results
   */
  async batchUpdateChecksums(filePaths) {
    const results = [];
    let stats = {
      total: filePaths.length,
      updated: 0,
      failed: 0
    };

    for (const filePath of filePaths) {
      const absolutePath = path.isAbsolute(filePath)
        ? filePath
        : path.join(this.vaultPath, filePath);

      const result = await this.updateChecksum(absolutePath);
      results.push(result);

      if (result.success) {
        stats.updated++;
      } else {
        stats.failed++;
      }
    }

    return {
      success: true,
      results,
      stats
    };
  }

  /**
   * Get verification cache
   */
  getCache() {
    return Array.from(this.verificationCache.entries()).map(([path, result]) => result);
  }

  /**
   * Clear verification cache
   */
  clearCache() {
    this.verificationCache.clear();
  }

  /**
   * Generate verification report
   * @param {Array<Object>} results - Verification results
   * @returns {string} Markdown report
   */
  generateReport(results) {
    const stats = {
      total: results.length,
      valid: results.filter(r => r.valid === true).length,
      invalid: results.filter(r => r.valid === false && !r.error).length,
      errors: results.filter(r => r.error).length,
      noChecksum: results.filter(r => r.expectedChecksum === null && !r.error).length
    };

    let report = `# Checksum Verification Report\n\n`;
    report += `**Generated:** ${new Date().toISOString()}\n\n`;
    report += `## Statistics\n\n`;
    report += `- **Total Files:** ${stats.total}\n`;
    report += `- **Valid:** ${stats.valid} ✅\n`;
    report += `- **Invalid:** ${stats.invalid} ❌\n`;
    report += `- **No Checksum:** ${stats.noChecksum} ⚠️\n`;
    report += `- **Errors:** ${stats.errors} 🚫\n\n`;

    if (stats.invalid > 0) {
      report += `## Invalid Checksums\n\n`;
      results
        .filter(r => r.valid === false && !r.error)
        .forEach(r => {
          report += `### ${r.filePath}\n\n`;
          report += `- **Expected:** \`${r.expectedChecksum}\`\n`;
          report += `- **Actual:** \`${r.actualChecksum}\`\n\n`;
        });
    }

    if (stats.errors > 0) {
      report += `## Errors\n\n`;
      results
        .filter(r => r.error)
        .forEach(r => {
          report += `- **${r.filePath}:** ${r.error}\n`;
        });
      report += `\n`;
    }

    return report;
  }

  /**
   * Calculate SHA-256 checksum
   */
  _calculateChecksum(content) {
    return crypto.createHash('sha256').update(content, 'utf8').digest('hex');
  }

  /**
   * Parse frontmatter into object
   */
  _parseFrontmatter(text) {
    const lines = text.split('\n');
    const parsed = {};

    for (const line of lines) {
      const match = line.match(/^(\w+):\s*(.+)$/);
      if (match) {
        const [, key, value] = match;
        parsed[key] = value.replace(/^["']|["']$/g, '');
      }
    }

    return parsed;
  }
}

module.exports = { ChecksumVerifier };
