#!/usr/bin/env python3
"""Convert OpenSIN-Skills for different AI editors.
Usage: python3 convert-to-opencode.py . --target opencode
Stdlib-only. Author: OpenSIN-AI. License: MIT."""
import argparse, json, os, sys

def find_skills(root):
    skills = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if not d.startswith(".") and d != "node_modules"]
        if "SKILL.md" in fns: skills.append(os.path.relpath(dp, root))
    return sorted(skills)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("root", help="Root directory")
    p.add_argument("--target", "-t", default="opencode", choices=["opencode","cursor","aider"])
    p.add_argument("--output", "-o")
    a = p.parse_args()
    skills = find_skills(a.root)
    print(f"Found {len(skills)} skills", file=sys.stderr)
    if a.target == "opencode":
        r = json.dumps({"name":"OpenSIN-Skills","skills":{"path":a.root},"total":len(skills)}, indent=2)
    elif a.target == "cursor":
        r = "# OpenSIN-Skills\n" + "\n".join(f"- {os.path.basename(s)}: {s}/SKILL.md" for s in skills[:50])
    else:
        r = f"# OpenSIN-Skills ({len(skills)} skills)"
    if a.output:
        with open(a.output,"w") as f: f.write(r+"\n")
    else: print(r)

if __name__ == "__main__": main()
