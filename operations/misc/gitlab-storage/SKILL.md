---
name: "gitlab-storage"
description: "> **ZWECK:** Alle schweren Dateien, Logs, Backups, Docker-Images, Reports und Ag"
version: "1.0.0"
author: "OpenSIN-AI"
category: "misc"
source: "opensin-native"
status: "active"
triggers:
  - "use gitlab-storage"
related_skills: []
---

# GitLab Storage — Unendlicher Speicher für die gesamte SIN-Flotte

> **ZWECK:** Alle schweren Dateien, Logs, Backups, Docker-Images, Reports und Agent-Artefakte werden in private GitLab-Repos (10GB free each, unendlich viele Repos) verlagert. Keine OCI-VM-Disk-Voll-Probleme mehr.

---

## 📁 Skill-Struktur

```
~/.config/opencode/skills/gitlab-storage/
├── SKILL.md                    ← Du bist hier
├── config/
│   ├── storage-registry.json   ← Zentrales Register: WAS liegt WO und WARUM
│   └── machine-links.json      ← Welche Maschine nutzt welche Storage-Repos
└── scripts/
    └── gitlab_storage_manager.py  ← Das Haupttool (baut auf gitlab_logcenter.py auf)
```

---

## 🔑 Token & Auth

| Variable | Pfad | Zweck |
|----------|------|-------|
| `GITLAB_LOGCENTER_TOKEN` | `~/.config/opencode/gitlab_logcenter.env` | GitLab API Token (privat, aus SIN-Passwordmanager) |
| `GITLAB_STORAGE_TOKEN` | `~/.config/opencode/gitlab_logcenter.env` | Gleicher Token, alias |

**Token kommt aus:** `sin-passwordmanager` → `gitlab.com` → `GITLAB_LOGCENTER_TOKEN`

---

## 🛠️ CLI-Befehle (Agent-Pflicht)

### Storage-Management

```bash
# Storage für ein Projekt initialisieren
gitlab_storage_manager.py init --project <name> [--visibility private|public]

# Datei in GitLab-Repo hochladen
gitlab_storage_manager.py upload --project <name> --file <pfad> [--category <kat>] [--tags t1,t2]

# Status aller Storage-Repos prüfen
gitlab_storage_manager.py status --project <name> [--json]

# Dateien suchen
gitlab_storage_manager.py search --project <name> --query <text>

# Dateien auflisten
gitlab_storage_manager.py list --project <name> [--category <kat>] [--date YYYY-MM-DD]

# Datei herunterladen
gitlab_storage_manager.py download --project <name> --path <repo_pfad> --output <lokal>

# Repo-Rotation erzwingen (wenn voll)
gitlab_storage_manager.py rotate --project <name>

# Aktives Repo anzeigen
gitlab_storage_manager.py get-active --project <name>
```

### Kategorien

| Kategorie | Zweck | Beispiele |
|-----------|-------|-----------|
| `logs` | Application Logs, Crash Logs | `runner.log`, `crash.dump` |
| `video` | Screen Recordings, CDP Screencasts | `browser_recording.mp4` |
| `screenshots` | Browser Screenshots, UI Captures | `screenshot.png` |
| `browser` | CDP Console, Network, Performance Logs | `console.log`, `network.har` |
| `reports` | Crash Analysis, RCA Reports | `crash_analysis.json` |
| `docker-images` | Exportierte Docker Images | `supabase_backup.tar` |
| `backups` | Datenbank-Backups, Config-Backups | `supabase_db.sql.gz` |
| `agent-artifacts` | Agent Build-Outputs, Test-Results | `test_results.json` |
| `misc` | Alles andere | `unknown.dat` |

---

## 🏗️ Storage-Register (WAS liegt WO und WARUM)

**Zentrales Register:** `config/storage-registry.json`

Jeder Eintrag enthält:
```json
{
  "project": "sin-solver",
  "repo_name": "sin-solver-logcenter-001",
  "repo_id": 12345678,
  "visibility": "private",
  "purpose": "Logs und Backups für SIN Solver Flotte",
  "owner_machine": "oci-vm-92.5.60.87",
  "categories": ["logs", "video", "screenshots"],
  "created_at": "2026-04-13T16:00:00Z",
  "size_limit_gb": 9,
  "current_size_gb": 0.5,
  "files_count": 142
}
```

### Bekannte Projekte (Stand: 2026-04-13)

| Projekt | Repo-Prefix | Visibility | Zweck |
|---------|-------------|------------|-------|
| `sin-solver` | `sin-solver-logcenter-` | **private** | Alle SIN Solver Logs, Videos, Reports |
| `sin-backend` | `sin-backend-storage-` | **private** | OpenSIN-Backend Dateien, DB-Dumps |
| `oci-vm` | `oci-vm-storage-` | **private** | OCI VM Docker-Images, System-Backups |
| `opencode-stack` | `opencode-stack-logs-` | **private** | OpenCode CLI Logs, Plugin-Logs |
| `sin-code` | `sin-code-artifacts-` | **private** | Build-Artefakte, Test-Results |

---

## 🔗 Machine-Links (Welche Maschine nutzt welche Repos)

**Konfiguration:** `config/machine-links.json`

```json
{
  "oci-vm-92.5.60.87": {
    "projects": ["sin-solver", "sin-backend", "oci-vm"],
    "sync_dirs": {
      "/var/log": "logs",
      "/opt/sin-supabase/backups": "backups",
      "/tmp/agent-artifacts": "agent-artifacts"
    }
  },
  "mac-jeremy": {
    "projects": ["sin-solver", "opencode-stack"],
    "sync_dirs": {
      "/tmp/opencode-logs": "logs",
      "/tmp/screenshots": "screenshots"
    }
  },
  "hf-vm-delqhi-simone-mcp": {
    "projects": ["sin-solver"],
    "sync_dirs": {
      "/tmp/logs": "logs",
      "/tmp/reports": "reports"
    }
  }
}
```

---

## 🔄 Auto-Rotation (wenn Repo voll)

- **Limit:** 9 GB pro Repo (10 GB free - 1 GB Safety)
- **Trigger:** Bei Upload prüft Script automatisch ob Repo voll ist
- **Action:** Erstellt automatisch `-001`, `-002`, `-003`, ... Repos
- **Unendlicher Speicher:** Jedes Repo = 9 GB × unendlich viele Repos

---

## 🌐 Public vs Private Repos

**REGELN:**

| Inhalt | Visibility | Grund |
|--------|------------|-------|
| Logs, Backups, Crash-Dumps | **private** | Enthalten sensible Daten, Secrets, IPs |
| Agent-Artefakte, Test-Results | **private** | Interne Entwicklungsdaten |
| Screenshots, Videos von UIs | **private** | Können User-Daten zeigen |
| Docker-Images | **private** | Enthalten Configs, Secrets |
| **Öffentliche Demos/Showcases** | **public** | Nur wenn explizit gewollt und keine Secrets |

**IMMER private**, es sei denn der User sagt explizit "public".

---

## ⚡ Migration OCI VM → GitLab Storage

### Was muss von der OCI VM migriert werden:

| Datei/Verzeichnis | Ziel-Kategorie | Größe (geschätzt) |
|-------------------|----------------|-------------------|
| `/var/log/*.log` | `logs` | ~440 MB |
| `/opt/sin-supabase/backups/` | `backups` | ~225 MB |
| `/opt/OpenSIN-Code/.git/objects/` | `backups` | ~363 MB |
| Docker-Images (backup) | `docker-images` | ~7 GB |
| `/tmp/agent-artifacts/` | `agent-artifacts` | variabel |
| `~/.cache/` | `misc` | ~144 MB |

### Migration-Befehl:

```bash
# Auf OCI VM ausführen:
cd ~
gitlab_storage_manager.py init --project oci-vm
gitlab_storage_manager.py upload --project oci-vm --file /var/log/syslog --category logs --tags system,boot
# ... für jede Datei
```

---

## 🚨 WICHTIGE REGELN FÜR ALLE AGENTEN

1. **NIEMALS** große Dateien lokal speichern (>1 MB) → IMMEDIATELY nach GitLab uploaden
2. **IMMER** `gitlab_storage_manager.py` nutzen, nicht manuell `git push`
3. **IMMER** `.meta.json` wird automatisch erstellt — nicht manuell bearbeiten
4. **IMMER** Tags setzen für spätere Suche
5. **NIEMALS** Secrets/Tokens in Dateien speichern die nach GitLab gehen
6. **IMMER** `--category` korrekt setzen
7. **IMMER** prüfen ob Repo voll ist vor Upload (Script macht das automatisch)

---

## 📋 Integration mit bestehendem gitlab_logcenter.py

Dieser Skill **erweitert** das bestehende `gitlab_logcenter.py` aus dem `enterprise-deep-debug` Skill:

- **Bestehende Funktion:** Log-Speicherung für Crash-Analyse
- **Neu:** Allgemeine Dateispeicherung, Machine-Links, Storage-Register
- **Kompatibel:** Alle alten Befehle funktionieren weiter
- **Erweitert:** Neue Kategorien (`docker-images`, `backups`, `agent-artifacts`)

---

## 🔍 Quick Reference für Agenten

```
FRAGE: Wo speichere ich eine große Datei?
ANTWORT: gitlab_storage_manager.py upload --project <projekt> --file <pfad> --category <kat>

FRAGE: Wie finde ich eine alte Datei?
ANTWORT: gitlab_storage_manager.py search --project <projekt> --query <suchbegriff>

FRAGE: Ist mein Storage-Repo voll?
ANTWORT: gitlab_storage_manager.py status --project <projekt>

FRAGE: Welches Repo nutze ich?
ANTWORT: gitlab_storage_manager.py get-active --project <projekt>

FRAGE: Neue Maschine anbinden?
ANTWORT: config/machine-links.json erweitern + gitlab_storage_manager.py init --project <name>
```


## Related Skills
- See [Skill Catalog](../../README.md) for related skills
