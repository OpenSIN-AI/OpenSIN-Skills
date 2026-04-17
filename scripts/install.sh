#!/usr/bin/env bash
# ============================================================================
# install.sh — Install OpenSIN-Skills into your OpenCode environment
#
# This script clones the OpenSIN-Skills repository and symlinks all skills
# into ~/.config/opencode/skills/ so OpenCode can discover and use them.
#
# Usage:
#   bash scripts/install.sh              # Install all skills
#   bash scripts/install.sh --operations # Install only operational skills
#   bash scripts/install.sh --knowledge  # Install only knowledge skills
#   bash scripts/install.sh --help       # Show help
#
# Requirements: git, bash 4+
# Package manager: bun (NEVER npm)
# Author: OpenSIN-AI | License: MIT
# ============================================================================

set -euo pipefail

# ── Configuration ──
SKILLS_REPO="https://github.com/OpenSIN-AI/OpenSIN-Skills.git"
INSTALL_DIR="${HOME}/.local/share/opensin-skills"
OPENCODE_SKILLS_DIR="${HOME}/.config/opencode/skills"
VERSION="1.0.0"

# ── Colors for output ──
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ── Helper functions ──
log_info()  { echo -e "${BLUE}[INFO]${NC} $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

show_help() {
    echo "OpenSIN-Skills Installer v${VERSION}"
    echo ""
    echo "Usage: bash install.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --all          Install all skills (default)"
    echo "  --operations   Install only operational skills"
    echo "  --knowledge    Install only knowledge/expertise skills"
    echo "  --update       Update existing installation"
    echo "  --uninstall    Remove all installed skills"
    echo "  --help         Show this help message"
    echo ""
    echo "Skills are installed to: ${OPENCODE_SKILLS_DIR}"
    echo "Repository cached at:    ${INSTALL_DIR}"
}

# ── Parse arguments ──
MODE="all"
for arg in "$@"; do
    case "$arg" in
        --operations) MODE="operations" ;;
        --knowledge)  MODE="knowledge" ;;
        --update)     MODE="update" ;;
        --uninstall)  MODE="uninstall" ;;
        --help|-h)    show_help; exit 0 ;;
        --all)        MODE="all" ;;
        *) log_error "Unknown option: $arg"; show_help; exit 1 ;;
    esac
done

# ── Uninstall ──
if [ "$MODE" = "uninstall" ]; then
    log_info "Removing OpenSIN-Skills symlinks from ${OPENCODE_SKILLS_DIR}..."
    find "${OPENCODE_SKILLS_DIR}" -type l -lname "${INSTALL_DIR}/*" -delete 2>/dev/null || true
    log_ok "Symlinks removed. Repository cache kept at ${INSTALL_DIR}"
    exit 0
fi

# ── Ensure opencode skills directory exists ──
mkdir -p "${OPENCODE_SKILLS_DIR}"

# ── Clone or update repository ──
if [ -d "${INSTALL_DIR}/.git" ]; then
    log_info "Updating existing repository..."
    cd "${INSTALL_DIR}" && git pull --ff-only origin main 2>/dev/null || {
        log_warn "Pull failed, re-cloning..."
        rm -rf "${INSTALL_DIR}"
        git clone --depth 1 "${SKILLS_REPO}" "${INSTALL_DIR}"
    }
else
    log_info "Cloning OpenSIN-Skills repository..."
    mkdir -p "$(dirname "${INSTALL_DIR}")"
    git clone --depth 1 "${SKILLS_REPO}" "${INSTALL_DIR}"
fi

log_ok "Repository ready at ${INSTALL_DIR}"

# ── Collect skill directories to install ──
# Each skill is a directory containing a SKILL.md file
SKILL_COUNT=0

install_skills_from() {
    local base_dir="$1"
    local label="$2"

    if [ ! -d "${INSTALL_DIR}/${base_dir}" ]; then
        log_warn "Directory ${base_dir} not found, skipping"
        return
    fi

    # Find all SKILL.md files and symlink their parent directories
    while IFS= read -r skill_md; do
        local skill_dir
        skill_dir="$(dirname "$skill_md")"
        local skill_name
        skill_name="$(basename "$skill_dir")"

        # Create symlink in opencode skills directory
        local target="${OPENCODE_SKILLS_DIR}/${skill_name}"
        if [ -L "$target" ] || [ -d "$target" ]; then
            rm -rf "$target"  # Remove existing symlink or directory
        fi
        ln -sf "$skill_dir" "$target"
        SKILL_COUNT=$((SKILL_COUNT + 1))
    done < <(find "${INSTALL_DIR}/${base_dir}" -name "SKILL.md" -type f 2>/dev/null)

    log_info "Installed ${label} skills from ${base_dir}"
}

# ── Install based on mode ──
case "$MODE" in
    all|update)
        # Knowledge domains
        for domain in engineering product-team marketing-skill c-level-advisor \
                       project-management ra-qm-team business-growth finance; do
            install_skills_from "$domain" "$domain"
        done
        # Operational categories
        for category in agent-creation browser-automation deployment media \
                         planning documents google misc; do
            install_skills_from "operations/$category" "operations/$category"
        done
        # Personas and orchestration
        install_skills_from "agents/personas" "personas"
        ;;
    operations)
        for category in agent-creation browser-automation deployment media \
                         planning documents google misc; do
            install_skills_from "operations/$category" "operations/$category"
        done
        ;;
    knowledge)
        for domain in engineering product-team marketing-skill c-level-advisor \
                       project-management ra-qm-team business-growth finance; do
            install_skills_from "$domain" "$domain"
        done
        ;;
esac

# ── Summary ──
echo ""
log_ok "=========================================="
log_ok "  OpenSIN-Skills v${VERSION} installed!"
log_ok "  ${SKILL_COUNT} skills linked to OpenCode"
log_ok "=========================================="
echo ""
log_info "Skills available at: ${OPENCODE_SKILLS_DIR}"
log_info "Run 'python3 ${INSTALL_DIR}/scripts/validate-skill.py --all ${INSTALL_DIR}' to validate"
