#!/usr/bin/env bash
# install.sh — Install OpenSIN-Skills into OpenCode environment
# Usage: bash scripts/install.sh [--all|--operations|--knowledge|--help]
# Author: OpenSIN-AI | License: MIT
set -euo pipefail
SKILLS_REPO="https://github.com/OpenSIN-AI/OpenSIN-Skills.git"
INSTALL_DIR="${HOME}/.local/share/opensin-skills"
OPENCODE_SKILLS="${HOME}/.config/opencode/skills"
log() { echo "[OpenSIN] $*"; }
MODE="all"
for arg in "$@"; do case "$arg" in --operations) MODE="operations";; --knowledge) MODE="knowledge";; --help|-h) echo "Usage: install.sh [--all|--operations|--knowledge|--help]"; exit 0;; esac; done
mkdir -p "${OPENCODE_SKILLS}"
if [ -d "${INSTALL_DIR}/.git" ]; then
  log "Updating..."; cd "${INSTALL_DIR}" && git pull --ff-only 2>/dev/null || { rm -rf "${INSTALL_DIR}"; git clone --depth 1 "${SKILLS_REPO}" "${INSTALL_DIR}"; }
else
  log "Cloning..."; mkdir -p "$(dirname "${INSTALL_DIR}")"; git clone --depth 1 "${SKILLS_REPO}" "${INSTALL_DIR}"
fi
COUNT=0
link_skills() { local d="$1"; [ -d "${INSTALL_DIR}/${d}" ] || return; while IFS= read -r f; do local sd; sd="$(dirname "$f")"; local n; n="$(basename "$sd")"; ln -sf "$sd" "${OPENCODE_SKILLS}/${n}"; COUNT=$((COUNT+1)); done < <(find "${INSTALL_DIR}/${d}" -name "SKILL.md" -type f 2>/dev/null); }
case "$MODE" in
  all) for d in engineering product-team marketing-skill c-level-advisor project-management ra-qm-team business-growth finance; do link_skills "$d"; done; for c in agent-creation browser-automation deployment media planning documents google misc; do link_skills "operations/$c"; done;;
  operations) for c in agent-creation browser-automation deployment media planning documents google misc; do link_skills "operations/$c"; done;;
  knowledge) for d in engineering product-team marketing-skill c-level-advisor project-management ra-qm-team business-growth finance; do link_skills "$d"; done;;
esac
log "Done! ${COUNT} skills installed to ${OPENCODE_SKILLS}"
