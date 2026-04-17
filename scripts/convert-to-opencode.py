#!/usr/bin/env python3
"""
convert-to-opencode.py — Convert OpenSIN-Skills for different AI editors.

Generates configuration files for OpenCode, Cursor, Aider, and other
AI coding assistants to load the skill library.

Usage:
    python3 convert-to-opencode.py . --target opencode
    python3 convert-to-opencode.py . --target cursor
    python3 convert-to-opencode.py --help

Stdlib-only. Author: OpenSIN-AI. License: MIT.
"""

import argparse
import json
import os
import sys


def find_skills(root):
    """Find all SKILL.md files and return their paths."""
    skills = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if not d.startswith(".") and d != "node_modules"]
        if "SKILL.md" in fns:
            skills.append(os.path.relpath(dp, root))
    return sorted(skills)


def generate_opencode_config(root, skills):
    """Generate .opencode/opencode.json with skill paths."""
    config = {
        "$schema": "https://opencode.ai/schema/opencode.json",
        "name": "OpenSIN-Skills",
        "description": "280+ AI agent skills",
        "version": "1.0.0",
        "skills": {"path": root},
    }
    return json.dumps(config, indent=2)


def generate_cursor_rules(root, skills):
    """Generate .cursorrules file for Cursor editor."""
    lines = [
        "# OpenSIN-Skills — 280+ AI Agent Skills",
        "",
        "You have access to the following skill library:",
        "",
    ]
    for skill in skills[:50]:  # Cursor rules have size limits
        name = os.path.basename(skill)
        lines.append(f"- {name}: see {skill}/SKILL.md")
    lines.append("")
    lines.append(f"Total: {len(skills)} skills available.")
    lines.append("Use the appropriate skill for each task.")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", help="Root directory of OpenSIN-Skills")
    parser.add_argument("--target", "-t", default="opencode",
                        choices=["opencode", "cursor", "aider"],
                        help="Target editor (default: opencode)")
    parser.add_argument("--output", "-o", help="Output file path")
    args = parser.parse_args()

    if not os.path.isdir(args.root):
        print(f"Error: {args.root} is not a directory", file=sys.stderr)
        sys.exit(1)

    skills = find_skills(args.root)
    print(f"Found {len(skills)} skills", file=sys.stderr)

    if args.target == "opencode":
        result = generate_opencode_config(args.root, skills)
    elif args.target == "cursor":
        result = generate_cursor_rules(args.root, skills)
    elif args.target == "aider":
        result = f"# OpenSIN-Skills ({len(skills)} skills)\n# Load with: aider --read {args.root}/**/SKILL.md"
    else:
        result = ""

    if args.output:
        with open(args.output, "w") as f:
            f.write(result + "\n")
        print(f"Written to {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
