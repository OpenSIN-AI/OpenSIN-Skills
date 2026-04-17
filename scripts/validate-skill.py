#!/usr/bin/env python3
"""Validates SKILL.md files against the OpenSIN Skill Authoring Standard.
Usage: python3 validate-skill.py path/to/SKILL.md
       python3 validate-skill.py --all skills/
Stdlib-only. Author: OpenSIN-AI. License: MIT."""
import argparse, json, os, re, sys

REQUIRED_FIELDS = ["name","description","version","author","category","source","status"]

def extract_frontmatter(content):
    lines = content.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---": return {}
    end = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---": end = i; break
    if end == -1: return {}
    result = {}
    for line in lines[1:end]:
        s = line.strip()
        if not s or s.startswith("#") or ":" not in s: continue
        k, _, v = s.partition(":")
        v = v.strip().strip('"').strip("'")
        if v: result[k.strip()] = v
    return result

def validate(fp):
    errs, warns = [], []
    if not os.path.isfile(fp): return {"path":fp,"valid":False,"errors":["Not found"],"warnings":[]}
    sz = os.path.getsize(fp)
    if sz > 10240: warns.append(f"Size {sz}B > 10KB")
    with open(fp) as f: content = f.read()
    fm = extract_frontmatter(content)
    if not fm: errs.append("Missing YAML frontmatter")
    else:
        for field in REQUIRED_FIELDS:
            if field not in fm: errs.append(f"Missing: {field}")
    if not re.search(r"^#{1,3}\s+Related Skills", content, re.M|re.I):
        warns.append("Missing: ## Related Skills")
    return {"path":fp,"valid":len(errs)==0,"errors":errs,"warnings":warns,"size":sz}

def find_skills(d):
    r = []
    for root,dirs,files in os.walk(d):
        dirs[:] = [x for x in dirs if not x.startswith(".")]
        for f in files:
            if f == "SKILL.md": r.append(os.path.join(root,f))
    return sorted(r)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("path", help="SKILL.md or directory")
    p.add_argument("--all", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    fs = find_skills(a.path) if a.all else [a.path]
    if not fs: print("No SKILL.md found",file=sys.stderr); sys.exit(1)
    results = [validate(f) for f in fs]
    ok = sum(1 for r in results if r["valid"])
    if a.json: print(json.dumps({"total":len(results),"valid":ok,"invalid":len(results)-ok,"results":results},indent=2))
    else:
        for r in results:
            print(f"[{\"PASS\" if r[\"valid\"] else \"FAIL\"}] {r[\"path\"]}")
            for e in r["errors"]: print(f"  ERR: {e}")
            for w in r["warnings"]: print(f"  WARN: {w}")
        print(f"\nTotal: {len(results)} | Pass: {ok} | Fail: {len(results)-ok}")
    sys.exit(0 if ok==len(results) else 1)

if __name__=="__main__": main()
