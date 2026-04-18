#!/usr/bin/env python3
"""
============================================================
SIN Skill Router — Intent-to-Agent Routing Engine
============================================================
Maps natural language user requests to the optimal combination
of A2A agents from the fleet registry. Zero external dependencies.

Usage:
    python3 skill-router.py "build me a landing page with auth"
    python3 skill-router.py --json "post our launch on all platforms"
    python3 skill-router.py --domains "find security vulnerabilities in our api"

How it works:
    1. Tokenize the user request into lowercase words
    2. Score each agent by keyword overlap with the request
    3. Group matching agents by domain
    4. Return the optimal dispatch plan (agents + domains + teams)

This is a LOCAL routing heuristic. The God Agent uses this as a
first-pass filter, then refines with LLM-based intent classification
via opencode CLI for ambiguous requests.
============================================================
"""

import json
import os
import sys
import re


def load_registry():
    """
    Load fleet-registry.json from the same directory as this script.
    Falls back to a parent directory search if not found directly.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    registry_path = os.path.join(script_dir, "fleet-registry.json")

    if not os.path.exists(registry_path):
        # Search parent directories (for when called from repo root)
        for parent in [".", "orchestration"]:
            alt = os.path.join(parent, "fleet-registry.json")
            if os.path.exists(alt):
                registry_path = alt
                break

    if not os.path.exists(registry_path):
        print("ERROR: fleet-registry.json not found", file=sys.stderr)
        sys.exit(1)

    with open(registry_path) as f:
        return json.load(f)


def tokenize(text):
    """
    Break text into lowercase tokens, stripping punctuation.
    Keeps hyphenated words intact (e.g., 'tiktok-shop' stays as one token).
    """
    text = text.lower()
    # Split on whitespace and common delimiters, keep hyphens within words
    tokens = re.findall(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", text)
    return set(tokens)


def route(query, registry):
    """
    Route a natural language query to the best matching agents.

    Algorithm:
      - For each agent in every domain, count keyword matches
      - Score = number of matching keywords (higher = better fit)
      - Return all agents with score > 0, sorted by score descending
      - Group by domain for the dispatch plan

    Returns dict with:
      - domains: list of matched domain names
      - agents: list of {name, domain, score, keywords_matched}
      - teams: list of team managers to coordinate
      - dispatch_plan: ready-to-use dispatch instructions
    """
    tokens = tokenize(query)
    matches = []

    for domain_name, domain_data in registry.get("domains", {}).items():
        agents = domain_data.get("agents", [])
        for agent in agents:
            agent_keywords = set(agent.get("keywords", []))
            matched = tokens & agent_keywords
            if matched:
                matches.append({
                    "name": agent["name"],
                    "domain": domain_name,
                    "score": len(matched),
                    "keywords_matched": sorted(matched),
                    "capabilities": agent.get("capabilities", []),
                    "team": domain_data.get("team", ""),
                })

    # Sort by score (highest first), then by domain for grouping
    matches.sort(key=lambda x: (-x["score"], x["domain"]))

    # Extract unique domains and teams
    domains = sorted(set(m["domain"] for m in matches))
    teams = sorted(set(m["team"] for m in matches if m["team"]))

    # Build dispatch plan — top agent per domain
    dispatch_plan = []
    seen_domains = set()
    for m in matches:
        if m["domain"] not in seen_domains:
            seen_domains.add(m["domain"])
            dispatch_plan.append({
                "agent": m["name"],
                "domain": m["domain"],
                "team": m["team"],
                "reason": f"Matched keywords: {', '.join(m['keywords_matched'])}",
            })

    return {
        "query": query,
        "domains": domains,
        "teams": teams,
        "agents": matches,
        "dispatch_plan": dispatch_plan,
        "parallel_possible": len(dispatch_plan) > 1,
    }


def main():
    """
    CLI entry point. Accepts a query string and prints the routing result.

    Flags:
      --json     Output full JSON result
      --domains  Output only matched domain names
      --agents   Output only matched agent names
      --plan     Output the dispatch plan (default)
    """
    if len(sys.argv) < 2:
        print("Usage: skill-router.py [--json|--domains|--agents|--plan] \"your request\"")
        print("Example: skill-router.py \"build a website and post on twitter\"")
        sys.exit(1)

    # Parse flags
    output_mode = "plan"
    args = sys.argv[1:]
    if args[0].startswith("--"):
        output_mode = args[0].lstrip("-")
        args = args[1:]

    query = " ".join(args)
    registry = load_registry()
    result = route(query, registry)

    if output_mode == "json":
        print(json.dumps(result, indent=2))
    elif output_mode == "domains":
        for d in result["domains"]:
            print(d)
    elif output_mode == "agents":
        for a in result["agents"]:
            print(f"{a['score']:2d}  {a['name']}  ({', '.join(a['keywords_matched'])})")
    else:
        # Default: dispatch plan
        if not result["dispatch_plan"]:
            print(f"No agents matched for: \"{query}\"")
            print("The God Agent will use LLM-based intent classification as fallback.")
            return

        print(f"Query: {query}")
        print(f"Parallel dispatch: {'YES' if result['parallel_possible'] else 'NO (single agent)'}")
        print(f"Domains: {', '.join(result['domains'])}")
        print(f"Teams: {', '.join(result['teams']) if result['teams'] else 'none'}")
        print()
        print("DISPATCH PLAN:")
        for i, d in enumerate(result["dispatch_plan"], 1):
            print(f"  [{i}] {d['agent']}")
            print(f"      Domain: {d['domain']}")
            print(f"      Team:   {d['team'] or 'N/A'}")
            print(f"      {d['reason']}")
            print()


if __name__ == "__main__":
    main()
