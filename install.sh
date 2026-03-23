#!/usr/bin/env bash
set -euo pipefail

# Effective Python — Claude Code Skill Installer
# Usage: curl -sSL https://raw.githubusercontent.com/DaehunGwak/effective-python-skill/main/install.sh | bash

SKILL_NAME="effective-python-3e"
REPO_URL="https://github.com/DaehunGwak/effective-python-skill.git"

# Determine install location
if [ -d ".claude" ]; then
    INSTALL_DIR=".claude/skills/${SKILL_NAME}"
    SCOPE="project"
else
    INSTALL_DIR="${HOME}/.claude/skills/${SKILL_NAME}"
    SCOPE="global"
fi

echo "🐍 Installing Effective Python skill (${SCOPE})..."
echo "   Target: ${INSTALL_DIR}"

# Create parent directory if needed
mkdir -p "$(dirname "${INSTALL_DIR}")"

# Clone or update
if [ -d "${INSTALL_DIR}" ]; then
    echo "   Updating existing installation..."
    cd "${INSTALL_DIR}" && git pull --quiet
else
    echo "   Cloning skill..."
    git clone --quiet "${REPO_URL}" "${INSTALL_DIR}"
fi

echo ""
echo "✅ Effective Python skill installed!"
echo ""
echo "Usage:"
echo "  • Auto mode: Just write Python — principles apply automatically"
echo "  • Review:    /effective-python src/"
echo "  • Refactor:  /effective-python refactor path/to/file.py"
echo "  • Scan:      python ${INSTALL_DIR}/scripts/check_patterns.py src/"
