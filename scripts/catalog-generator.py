#!/usr/bin/env python3
"""Generates catalog.json from all SKILL.md files.
Usage: python3 catalog-generator.py . --output catalog.json
Stdlib-only. Author: OpenSIN-AI. License: MIT."""
import argparse, json, os, re, sys
from datetime import datetime

def extract_fm(fp):
    try:
        with open(fp) as f: content = f.read()
    except: return {}
    lines = content.splitlines()
    if len(lines)<3 or lines[0].strip()!="---": return {}
    end=-1
    for i in range(1,len(lines)):
        if lines[i].strip()=="---": end=i; break
    if end==-1: return {}
    r={}
    for line in lines[1:end]:
        s=line.strip()
        if not s or s.startswith("#") or ":" not in s: continue
        k,_,v=s.partition(":")
        v=v.strip().strip('"').strip("'")
        if v: r[k.strip()]=v
    return r

def scan(root):
    cat=[]
    for dp,dns,fns in os.walk(root):
        dns[:]=[d for d in dns if not d.startswith(".") and d!="node_modules"]
        if "SKILL.md" not in fns: continue
        fp=os.path.join(dp,"SKILL.md")
        m=extract_fm(fp)
        parts=os.path.relpath(dp,root).split(os.sep)
        tools=[f"scripts/{f}" for f in sorted(os.listdir(os.path.join(dp,"scripts"))) if f.endswith(".py")] if os.path.isdir(os.path.join(dp,"scripts")) else []
        cat.append({"name":m.get("name",os.path.basename(dp)),"description":m.get("description",""),"version":m.get("version","1.0.0"),"author":m.get("author","OpenSIN-AI"),"category":m.get("category",parts[0]),"source":m.get("source","unknown"),"status":m.get("status","active"),"domain":parts[0],"path":os.path.relpath(dp,root),"tools":tools})
    cat.sort(key=lambda x:(x["domain"],x["name"]))
    return cat

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("root",help="Root directory to scan")
    p.add_argument("--output","-o",help="Output file")
    p.add_argument("--stats",action="store_true")
    a=p.parse_args()
    if not os.path.isdir(a.root): print(f"Not a dir: {a.root}",file=sys.stderr); sys.exit(1)
    cat=scan(a.root)
    if not cat: print("No skills found",file=sys.stderr); sys.exit(1)
    if a.stats:
        doms={}
        for s in cat: doms[s["domain"]]=doms.get(s["domain"],0)+1
        print(f"Total: {len(cat)}")
        for d,c in sorted(doms.items()): print(f"  {d}: {c}")
    else:
        out={"generated":datetime.utcnow().isoformat()+"Z","total_skills":len(cat),"skills":cat}
        js=json.dumps(out,indent=2,ensure_ascii=False)
        if a.output:
            with open(a.output,"w") as f: f.write(js+"\n")
            print(f"Written: {a.output} ({len(cat)} skills)",file=sys.stderr)
        else: print(js)

if __name__=="__main__": main()
