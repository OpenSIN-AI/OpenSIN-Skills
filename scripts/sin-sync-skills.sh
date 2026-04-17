#!/usr/bin/env bash
# sin-sync-skills.sh — Sync skills to OCI VM fleet
# Usage: bash scripts/sin-sync-skills.sh [--oci|--help]
# Author: OpenSIN-AI | License: MIT
set -euo pipefail
LOCAL="${HOME}/.config/opencode/skills"
OCI="ubuntu@92.5.60.87:~/.config/opencode/skills/"
case "${1:-all}" in --help|-h) echo "Usage: sin-sync-skills.sh [--oci|--help]"; exit 0;; esac
echo "[SYNC] Syncing to OCI VM..."
rsync -avz --delete --exclude='*.db' --exclude='*.sqlite*' --exclude='logs/' --exclude='tmp/' --exclude='.cache/' --exclude='auth.json' --exclude='token.json' "${LOCAL}/" "${OCI}" 2>/dev/null && echo "[OK] OCI synced" || echo "[WARN] OCI sync failed"
