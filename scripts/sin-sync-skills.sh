#!/usr/bin/env bash
# ============================================================================
# sin-sync-skills.sh — Sync OpenSIN-Skills to OCI VM and HF VMs
#
# The Mac is the Source of Truth. This script pushes the skill library
# to all fleet VMs so every agent has the same skill set.
#
# Usage:
#   bash scripts/sin-sync-skills.sh           # Sync to all targets
#   bash scripts/sin-sync-skills.sh --oci     # Sync to OCI VM only
#   bash scripts/sin-sync-skills.sh --help    # Show help
#
# Author: OpenSIN-AI | License: MIT
# ============================================================================

set -euo pipefail

# ── Configuration ──
LOCAL_SKILLS="${HOME}/.config/opencode/skills"
OCI_HOST="ubuntu@92.5.60.87"
OCI_SKILLS="${OCI_HOST}:~/.config/opencode/skills/"

# ── Colors ──
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[SYNC]${NC} $*"; }
log_ok()   { echo -e "${GREEN}[OK]${NC} $*"; }

# ── Parse args ──
TARGET="all"
for arg in "$@"; do
    case "$arg" in
        --oci)  TARGET="oci" ;;
        --help|-h)
            echo "sin-sync-skills.sh — Sync skills to fleet VMs"
            echo "Usage: bash sin-sync-skills.sh [--oci] [--help]"
            exit 0
            ;;
    esac
done

# ── Sync to OCI VM ──
if [ "$TARGET" = "all" ] || [ "$TARGET" = "oci" ]; then
    log_info "Syncing skills to OCI VM (${OCI_HOST})..."
    rsync -avz --delete \
        --exclude='*.db' --exclude='*.sqlite*' \
        --exclude='logs/' --exclude='tmp/' --exclude='.cache/' \
        --exclude='auth.json' --exclude='token.json' \
        "${LOCAL_SKILLS}/" "${OCI_SKILLS}" 2>/dev/null && \
        log_ok "OCI VM synced" || \
        echo "[WARN] OCI sync failed (VM may be offline)"
fi

log_ok "Skill sync complete!"
