---
name: create-a2a-sin-agent
description: ULTIMATE A2A creation skill — creates SIN Agents, SIN Teams, and SIN Coders from a single unified workflow. Merges create-a2a, create-a2a-team, and create-a2a-sin-coder into one ultimate skill. Use for ANY new A2A Agent, Team Manager, or Coder Agent.
---

# 👑 ULTIMATE A2A SIN Factory — Agents + Teams + Coders

> **OpenCode mirror:** sourced from `~/.config/opencode/skills/create-a2a-sin-agent`
> **Dieser Skill ersetzt:** `/create-a2a`, `/create-a2a-team`, `/create-a2a-sin-coder`

---

## 📋 Was dieser Skill kann

| Erstelle | Zweck | Workflow |
|:---|:---|:---|
| **SIN Agent** | Einzelner A2A Agent (z.B. `A2A-SIN-Google-Docs`) | Template-SIN-Agent |
| **SIN Team** | Team Manager (z.B. `Team-SIN-Survey`) | Template-SIN-Team |
| **SIN Coder** | Entwickler-Agent (z.B. `A2A-SIN-Frontend`) | Template-SIN-Agent + Coder-Mandate |

**Alle drei nutzen jetzt EIN Template:** Template-SIN-Agent (fusioniert aus Template-SIN-Agent, Template-SIN-Agent-Worker, Template-SIN-Worker).

---

## 🧠 Agent Configuration System (v5)

Jeder neue Agent wird dem richtigen **A2A Team** zugeordnet und erbt dessen Modell-Konfiguration:

### Team-Register (oh-my-sin.json)

| Team | Manager | Config-Datei | Primaer-Modell |
|:---|:---|:---|:---|
| **Team Coding** | A2A-SIN-Zeus | `my-sin-team-code.json` | `claude-sonnet-4-6` |
| **Team Worker** | A2A-SIN-Team-Worker | `my-sin-team-worker.json` | `gemini-3-flash` |
| **Team Infrastructure** | A2A-SIN-Team-Infrastructure | `my-sin-team-infrastructure.json` | `gpt-5.4` |

### Subagenten-Modelle (oh-my-openagent.json)

| Subagent | Modell | Fallback-Kette |
|:---|:---|:---|
| **explore** | `nvidia-nim/stepfun-ai/step-3.5-flash` | gemini-3-flash → gpt-5.4 → gemini-3.1-pro → claude-sonnet → qwen |
| **librarian** | `nvidia-nim/stepfun-ai/step-3.5-flash` | gemini-3-flash → gpt-5.4 → gemini-3.1-pro → claude-sonnet → qwen |

### PARALLEL-EXPLORATION MANDATE (PRIORITY -4.5)

Bei grossen Codebases (100k+ Zeilen) MUSS der Agent **5-10 parallele explore + 5-10 librarian-Agenten** starten. Ein einzelner Agent liefert nur ~20% Abdeckung.

---

## 🛠️ Workflow 1: SIN Agent erstellen

```bash
# 1. Spec erstellen
cp agent-spec.example.json my-agent-spec.json
# Bearbeite: name, slug, team, manager, description, capabilities

# 2. Agent generieren
node /Users/jeremy/dev/OpenSIN-backend/scripts/create-sin-a2a-agent.mjs --spec /abs/path/to/my-agent-spec.json

# 3. Dashboard Page scaffolen
node /Users/jeremy/dev/OpenSIN-backend/scripts/scaffold-a2a-agent-page.mjs --slug sin-<agentname>

# 4. Consumer Auth einrichten
~/.config/opencode/skills/create-a2a-sin-agent/scripts/setup_consumer_auth.sh /abs/path/to/new-agent-root

# 5. MCP Surface generieren
MCP_SCRIPTS=~/.config/opencode/skills/create-a2a-mcp/scripts
node $MCP_SCRIPTS/mcp-scaffold.mjs --agent-root /abs/path/to/new-agent-root --slug sin-<agentname>

# 6. Dependencies pruefen
node ~/.config/opencode/skills/create-a2a-sin-agent/scripts/a2a-preflight.mjs --agent-root /abs/path/to/new-agent-root --targets deps,install,assets,hf
```

### Pflicht-Dateien (jeder SIN Agent)

| Datei | Zweck |
|:---|:---|
| `agent.json` | Identitaet, capabilities, marketplace object |
| `A2A-CARD.md` | Agent Card fuer Discovery |
| `mcp-config.json` | MCP Server Konfiguration |
| `clients/opencode-mcp.json` | OpenCode MCP Client |
| `src/runtime.ts` | Runtime mit opencode CLI Integration |
| `src/mcp-server.ts` | MCP Server Oberflaeche |
| `src/a2a-http.ts` | A2A HTTP Endpoint |
| `src/metadata.ts` | Metadata mit marketplace object |
| `src/cli.ts` | Native CLI Entry Point |
| `scripts/hf_pull_script.py` | Token Pull Script (Producer-Consumer) |
| `scripts/complete-install.sh` | Idempotenter Installations-Script |
| `governance/repo-governance.json` | Repo Governance |
| `governance/pr-watcher.json` | PR Watcher Contract |
| `platforms/registry.json` | Platform Registry |
| `n8n-workflows/inbound-intake.json` | Inbound Work Intake |
| `docs/03_ops/inbound-intake.md` | Inbound Intake Doku |
| `scripts/watch-pr-feedback.sh` | PR Feedback Watcher |

---

## 🛠️ Workflow 2: SIN Team erstellen

```bash
# Team generieren (CLI-first, 90% weniger Tokens!)
~/.config/opencode/skills/create-a2a-sin-agent/scripts/generate-team.sh \
  sin-team-<name> \
  "Team - <Name>" \
  "SIN-Team-<Name>" \
  "Beschreibung des Teams"
```

### Team Manager Pflicht-Dateien

| Datei | Zweck |
|:---|:---|
| `agent.json` | Team Manager Identitaet |
| `A2A-CARD.md` | Team Card |
| `src/manager.ts` | Hermes Dispatch Logik |
| `src/cli.ts` | Native CLI |

---

## 🛠️ Workflow 3: SIN Coder erstellen

Coder Agents nutzen denselben Workflow wie SIN Agents, ZUSAETZLICH mit:

### Coder-spezifische Mandate

1. **GitHub App Bot Lane:** `githubBot.enabled=true` mit eigenem Bot-Persona
2. **LangGraph.js Supervisor:** Multi-Agent Graph mit CodeGenerationNode, TestingNode, IntegrationNode
3. **Master Boss Coder Prompt:** CEO-level Identitaet mit 10 Millionen Developer-Wissen
4. **Browser + GUI Testing:** sinInChrome + sin-computer-use Integration
5. **7-Layer Security Hardening:** Pre-commit/pre-push hooks, leak prevention CI
6. **Inbound-Work + PR-Watcher Contract:** Ab Tag 1

### Coder-spezifische Dateien

| Datei | Zweck |
|:---|:---|
| `config/github-app-routing.example.json` | GitHub App Bot Routing |
| `governance/coder-dispatch-matrix.json` | Coder Spezialisierungs-Matrix |
| `.githooks/pre-commit` | Secret + External Code Detection |
| `.githooks/pre-push` | Commit Message Leak Detection |
| `.secrets.baseline` | Detect-Secrets Baseline |
| `.github/workflows/leak-prevention.yml` | CI Security Scanning |

---

## 🚨 LLM-AUFRUF PFLICHT-ARCHITEKTUR

**JEDER A2A Agent ruft LLMs AUSSCHLIESSLICH ueber die `opencode` CLI auf:**

```python
import subprocess, json

def call_llm(prompt: str, timeout: int = 120) -> str:
    result = subprocess.run(
        ["opencode", "run", prompt, "--format", "json"],
        capture_output=True, text=True, timeout=timeout,
    )
    parts = []
    for line in result.stdout.splitlines():
        try:
            ev = json.loads(line)
            if ev.get("type") == "text":
                parts.append(ev.get("part", {}).get("text", ""))
        except json.JSONDecodeError:
            pass
    return "".join(parts).strip()
```

**REGELN — SOFORTIGER BAN BEI VERSTOSS:**
- `opencode run --format json` = EINZIG ERLAUBT
- OCI-Proxy direkt = VERBOTEN
- Gemini API direkt = PERMANENT VERBOTEN
- Anthropic API direkt = PERMANENT VERBOTEN
- **Modell:** `openai/gpt-5.4` + `--fallback nvidia/minimaxai/minimax-m2.7`

---

## 🏗️ Unified Template: Template-SIN-Agent

**Drei Templates wurden zu EINEM fusioniert:**
- `Template-SIN-Agent` (Basis)
- `Template-SIN-Agent-Worker` (Worker)
- `Template-SIN-Worker` (Minimal)

**→ Jetzt: `Template-SIN-Agent` (all-in-one)**

Jeder neue Agent nutzt dieses eine Template und konfiguriert sich via `agent.json`:
- `type: "agent"` — Standard Agent
- `type: "worker"` — Worker Agent (minimal)
- `type: "coder"` — Coder Agent (mit LangGraph + Security)
- `type: "team-manager"` — Team Manager (mit Hermes Dispatch)

---

## 🛡️ Required Validations

Vor "complete" MUessen ALLE bestehen:

```bash
npm --prefix /abs/path/to/agent-root run build
node /abs/path/to/agent-root/dist/src/cli.js run-action '{"action":"agent.help"}'
node /abs/path/to/agent-root/dist/src/cli.js print-card
cd /Users/jeremy/dev/OpenSIN-backend && npm run test:a2a:fleet
cd /Users/jeremy/dev/OpenSIN-backend && npm run sync:a2a:control-plane-projection
node ~/.config/opencode/skills/create-a2a-sin-agent/scripts/a2a-verify-hf-vm-readiness.mjs \
  --agent-root /abs/path/to/agent-root \
  --health-url https://<public>/health
```

---

## 📦 Vollstaendige Dokumentation

→ [Agent Configuration Guide](https://github.com/OpenSIN-AI/OpenSIN-documentation/blob/main/docs/guide/agent-configuration.md)

---

*Letzte Aktualisierung: 2026-04-14 | ULTIMATE SKILL v1.0*
