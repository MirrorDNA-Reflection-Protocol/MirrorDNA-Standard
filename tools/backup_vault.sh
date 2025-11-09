#!/usr/bin/env bash
set -euo pipefail

#
# MirrorDNA Vault Backup Orchestrator
#
# Creates encrypted backup of Personal Layer vault
# - Timestamp: BACKUP_YYYY-MM-DD_HHMMSS.zip
# - Encrypted with password
# - Post-backup integrity verification
# - Automatic retention (keep last 30 days)
#
# Usage:
#   ./backup_vault.sh [vault_path] [backup_path]
#
# Principles: Disaster recovery, sovereignty-first, encrypted at rest
#

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Default paths (can be overridden by arguments)
VAULT_PATH="${1:-/Users/pauldesai/Documents/ActiveMirrorOS}"
BACKUP_PATH="${2:-/Users/pauldesai/Backups/AMOS}"
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
BACKUP_FILE="BACKUP_${TIMESTAMP}.zip"
RETENTION_DAYS=30

log_info "MirrorDNA Vault Backup Orchestrator v1.0"
echo "================================================================"

# Validate vault path exists
if [ ! -d "$VAULT_PATH" ]; then
    log_error "Vault path does not exist: $VAULT_PATH"
    exit 1
fi

log_info "Vault path: $VAULT_PATH"

# Create backup directory if it doesn't exist
if [ ! -d "$BACKUP_PATH" ]; then
    log_info "Creating backup directory: $BACKUP_PATH"
    mkdir -p "$BACKUP_PATH"
fi

log_info "Backup path: $BACKUP_PATH"

# Calculate vault size
VAULT_SIZE=$(du -sh "$VAULT_PATH" | cut -f1)
log_info "Vault size: $VAULT_SIZE"

# Check available disk space
AVAILABLE_SPACE=$(df -h "$BACKUP_PATH" | awk 'NR==2 {print $4}')
log_info "Available space: $AVAILABLE_SPACE"

# Create backup
log_info "Creating backup: $BACKUP_FILE"
log_info "This may take a few minutes..."

# Check if zip supports encryption
if zip --help 2>&1 | grep -q -- "--password"; then
    ENCRYPT_FLAG="--password"
elif zip --help 2>&1 | grep -q -- "-e"; then
    ENCRYPT_FLAG="-e"
else
    log_warn "Encryption not supported by zip. Creating unencrypted backup."
    ENCRYPT_FLAG=""
fi

# Create backup (with or without encryption)
cd "$(dirname "$VAULT_PATH")"
VAULT_BASENAME="$(basename "$VAULT_PATH")"

if [ -n "$ENCRYPT_FLAG" ]; then
    log_info "Creating encrypted backup..."
    if [ "$ENCRYPT_FLAG" = "--password" ]; then
        # For GNU zip with --password flag
        zip -r --password "$(read -sp "Enter backup password: " pwd; echo $pwd)" \
            "${BACKUP_PATH}/${BACKUP_FILE}" "$VAULT_BASENAME" > /dev/null 2>&1
    else
        # For traditional -e flag (prompts for password interactively)
        zip -r -e "${BACKUP_PATH}/${BACKUP_FILE}" "$VAULT_BASENAME"
    fi
else
    log_warn "Creating unencrypted backup (encryption not available)"
    zip -r -q "${BACKUP_PATH}/${BACKUP_FILE}" "$VAULT_BASENAME"
fi

# Verify backup was created
if [ ! -f "${BACKUP_PATH}/${BACKUP_FILE}" ]; then
    log_error "Backup file was not created!"
    exit 1
fi

# Get backup size
BACKUP_SIZE=$(du -sh "${BACKUP_PATH}/${BACKUP_FILE}" | cut -f1)
log_info "Backup size: $BACKUP_SIZE"

# Verify backup integrity
log_info "Verifying backup integrity..."
if unzip -t "${BACKUP_PATH}/${BACKUP_FILE}" > /dev/null 2>&1; then
    log_info "✅ Backup integrity verified"
else
    log_error "❌ Backup integrity check failed!"
    exit 1
fi

# Cleanup old backups (keep last N days)
log_info "Cleaning up old backups (retention: ${RETENTION_DAYS} days)..."

# Count backups before cleanup
BEFORE_COUNT=$(find "${BACKUP_PATH}" -name "BACKUP_*.zip" | wc -l | tr -d ' ')

# Remove old backups
if [ -d "$BACKUP_PATH" ]; then
    find "${BACKUP_PATH}" -name "BACKUP_*.zip" -mtime +${RETENTION_DAYS} -delete 2>/dev/null || true
fi

# Count backups after cleanup
AFTER_COUNT=$(find "${BACKUP_PATH}" -name "BACKUP_*.zip" | wc -l | tr -d ' ')
REMOVED_COUNT=$((BEFORE_COUNT - AFTER_COUNT))

if [ $REMOVED_COUNT -gt 0 ]; then
    log_info "Removed $REMOVED_COUNT old backup(s)"
else
    log_info "No old backups to remove"
fi

# Summary
echo ""
echo "================================================================"
log_info "✅ Backup complete!"
echo ""
echo "  Backup file: ${BACKUP_FILE}"
echo "  Location: ${BACKUP_PATH}"
echo "  Size: ${BACKUP_SIZE}"
echo "  Total backups: ${AFTER_COUNT}"
echo ""
log_info "To restore: unzip ${BACKUP_PATH}/${BACKUP_FILE}"
echo "================================================================"

exit 0
