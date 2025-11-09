#!/usr/bin/env bash
set -euo pipefail

#
# MirrorDNA Automation Orchestrator
#
# Master script that orchestrates daily/weekly vault automation tasks:
# - Sync report generation
# - Checksum verification
# - Drift auditing
# - Backup operations
#
# Usage:
#   ./run_automations.sh [--daily|--weekly|--all] [--dry-run]
#
# Principles: Automated continuity maintenance, sovereignty-first
#

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

log_section() {
    echo -e "${BLUE}[====]${NC} $1"
}

# Parse arguments
MODE="daily"
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --daily)
            MODE="daily"
            shift
            ;;
        --weekly)
            MODE="weekly"
            shift
            ;;
        --all)
            MODE="all"
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            echo "Usage: $0 [--daily|--weekly|--all] [--dry-run]"
            echo ""
            echo "Options:"
            echo "  --daily     Run daily tasks (sync_report, backup)"
            echo "  --weekly    Run weekly tasks (drift_audit, checksum_verify)"
            echo "  --all       Run all tasks"
            echo "  --dry-run   Show what would run without executing"
            echo "  --help      Show this help message"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config/vault_automation.yaml"
LOG_FILE="${SCRIPT_DIR}/automation.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Ensure log file exists
touch "$LOG_FILE"

log_to_file() {
    echo "[${TIMESTAMP}] $1" >> "$LOG_FILE"
}

# Header
echo "================================================================"
log_info "MirrorDNA Automation Orchestrator v1.0"
echo "================================================================"
log_info "Mode: $MODE"
log_info "Dry run: $DRY_RUN"
log_info "Timestamp: $TIMESTAMP"
echo ""

# Define task lists
DAILY_TASKS=("sync_report" "backup_vault")
WEEKLY_TASKS=("drift_audit" "checksum_verify")

# Select tasks based on mode
if [ "$MODE" = "daily" ]; then
    TASKS=("${DAILY_TASKS[@]}")
elif [ "$MODE" = "weekly" ]; then
    TASKS=("${WEEKLY_TASKS[@]}")
else
    TASKS=("${DAILY_TASKS[@]}" "${WEEKLY_TASKS[@]}")
fi

log_info "Tasks to run: ${TASKS[*]}"
echo ""

# Track results
SUCCESS_COUNT=0
FAILURE_COUNT=0
SKIPPED_COUNT=0

# Execute tasks
for task in "${TASKS[@]}"; do
    log_section "Task: $task"

    if [ "$DRY_RUN" = true ]; then
        log_info "DRY RUN: Would execute $task"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        echo ""
        continue
    fi

    case $task in
        sync_report)
            log_info "Running sync report..."
            if python3 "${SCRIPT_DIR}/sync_report.py" --config "$CONFIG_FILE" 2>&1 | tee -a "$LOG_FILE"; then
                log_info "✅ sync_report completed"
                log_to_file "SUCCESS: sync_report"
                SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
            else
                EXIT_CODE=$?
                if [ $EXIT_CODE -eq 1 ]; then
                    log_warn "⚠️  sync_report completed with warnings (drift detected)"
                    log_to_file "WARNING: sync_report (drift)"
                    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
                elif [ $EXIT_CODE -eq 2 ]; then
                    log_error "❌ sync_report failed (conflicts detected)"
                    log_to_file "FAILURE: sync_report (conflicts)"
                    FAILURE_COUNT=$((FAILURE_COUNT + 1))
                else
                    log_error "❌ sync_report failed"
                    log_to_file "FAILURE: sync_report"
                    FAILURE_COUNT=$((FAILURE_COUNT + 1))
                fi
            fi
            ;;

        backup_vault)
            log_info "Running vault backup..."
            if bash "${SCRIPT_DIR}/backup_vault.sh" 2>&1 | tee -a "$LOG_FILE"; then
                log_info "✅ backup_vault completed"
                log_to_file "SUCCESS: backup_vault"
                SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
            else
                log_error "❌ backup_vault failed"
                log_to_file "FAILURE: backup_vault"
                FAILURE_COUNT=$((FAILURE_COUNT + 1))
            fi
            ;;

        drift_audit)
            log_info "Running drift audit..."
            if python3 "${SCRIPT_DIR}/drift_audit.py" --config "$CONFIG_FILE" 2>&1 | tee -a "$LOG_FILE"; then
                log_info "✅ drift_audit completed"
                log_to_file "SUCCESS: drift_audit"
                SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
            else
                EXIT_CODE=$?
                if [ $EXIT_CODE -eq 1 ]; then
                    log_warn "⚠️  drift_audit completed with warnings (caution level)"
                    log_to_file "WARNING: drift_audit (caution)"
                    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
                elif [ $EXIT_CODE -eq 2 ]; then
                    log_error "❌ drift_audit failed (excessive drift)"
                    log_to_file "FAILURE: drift_audit (excessive)"
                    FAILURE_COUNT=$((FAILURE_COUNT + 1))
                else
                    log_error "❌ drift_audit failed"
                    log_to_file "FAILURE: drift_audit"
                    FAILURE_COUNT=$((FAILURE_COUNT + 1))
                fi
            fi
            ;;

        checksum_verify)
            log_info "Running checksum verification..."
            # For checksum verify, we use verify subcommand
            if python3 "${SCRIPT_DIR}/checksum_verify.py" verify . --config "$CONFIG_FILE" 2>&1 | tee -a "$LOG_FILE"; then
                log_info "✅ checksum_verify completed"
                log_to_file "SUCCESS: checksum_verify"
                SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
            else
                EXIT_CODE=$?
                if [ $EXIT_CODE -eq 1 ]; then
                    log_warn "⚠️  checksum_verify completed with warnings (changes detected)"
                    log_to_file "WARNING: checksum_verify (changes)"
                    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
                else
                    log_error "❌ checksum_verify failed"
                    log_to_file "FAILURE: checksum_verify"
                    FAILURE_COUNT=$((FAILURE_COUNT + 1))
                fi
            fi
            ;;

        *)
            log_error "Unknown task: $task"
            FAILURE_COUNT=$((FAILURE_COUNT + 1))
            ;;
    esac

    echo ""
done

# Summary
echo "================================================================"
log_section "Automation Summary"
echo "================================================================"
log_info "Timestamp: $TIMESTAMP"
log_info "Mode: $MODE"
log_info "Total tasks: ${#TASKS[@]}"
log_info "Successful: $SUCCESS_COUNT"
log_info "Failed: $FAILURE_COUNT"

if [ "$DRY_RUN" = true ]; then
    log_info "Skipped (dry run): $SKIPPED_COUNT"
fi

echo ""

if [ $FAILURE_COUNT -eq 0 ]; then
    log_info "✅ All automations completed successfully"
    log_to_file "SUMMARY: All tasks completed successfully"
    exit 0
else
    log_error "❌ Some automations failed"
    log_to_file "SUMMARY: $FAILURE_COUNT tasks failed"
    exit 1
fi
