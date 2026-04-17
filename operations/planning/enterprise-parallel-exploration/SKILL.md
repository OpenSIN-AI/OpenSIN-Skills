---
name: "enterprise-parallel-exploration"
description: "> **ZWECK:** Bei grossen Codebases (100k+ Zeilen, 1000+ Dateien) liefert EIN ein"
version: "1.0.0"
author: "OpenSIN-AI"
category: "planning"
source: "opensin-native"
status: "active"
triggers:
  - "use enterprise-parallel-exploration"
related_skills: []
---

# Enterprise Parallel Exploration Protocol

> **ZWECK:** Bei grossen Codebases (100k+ Zeilen, 1000+ Dateien) liefert EIN einzelner explore/librarian-Agent nur 20% Abdeckung. Diese Skill stellt sicher, dass IMMER 5-10 explore + 5-10 librarian-Agenten PARALLEL gestartet werden, um 100% Abdeckung zu erreichen.

---

## 🚨 DAS PROBLEM

Ein einzelner `task(subagent_type="explore")` auf einem grossen Projekt:
- Analysiert nur ~20% der relevanten Dateien
- Uebersieht Abhaengigkeiten zwischen Modulen
- Liefert Zusammenfassungen auf Basis von 80% fehlendem Wissen
- Fuehrt zu falschen Architektur-Entscheidungen

**LOESUNG:** Immer 5-10 parallele explore + 5-10 parallele librarian-Agenten starten.

---

## 📐 DIE REGEL: IMMER PARALLEL, NIE SEQUENTIELL

```
❌ FALSCH (einzelner Agent):
task(subagent_type="explore", prompt="Finde alle API-Endpunkte")
→ Analysiert vielleicht 3 von 15 Dateien → 80% fehlen!

✅ RICHTIG (parallele Schwarm-Exploration):
// 7 Explore-Agenten fuer verschiedene Bereiche
task(subagent_type="explore", run_in_background=true, load_skills=[],
  description="Find API routes",
  prompt="[CONTEXT]: Grosse Codebase. [GOAL]: Finde ALLE API-Endpunkte in src/api/routes/. [REQUEST]: Liste jede Route mit HTTP-Methode, Handler, Middleware.")

task(subagent_type="explore", run_in_background=true, load_skills=[],
  description="Find controllers",
  prompt="[CONTEXT]: Grosse Codebase. [GOAL]: Finde ALLE Controller in src/controllers/. [REQUEST]: Liste jeden Controller mit Methoden, Dependencies, importierten Services.")

task(subagent_type="explore", run_in_background=true, load_skills=[],
  description="Find services",
  prompt="[CONTEXT]: Grosse Codebase. [GOAL]: Finde ALLE Services in src/services/. [REQUEST]: Liste jeden Service mit oeffentlichen Methoden, Abhaengigkeiten, DB-Queries.")

task(subagent_type="explore", run_in_background=true, load_skills=[],
  description="Find middleware",
  prompt="[CONTEXT]: Grosse Codebase. [GOAL]: Finde ALLE Middleware in src/middleware/. [REQUEST]: Liste jede Middleware mit Zweck, Reihenfolge, betroffenen Routes.")

task(subagent_type="explore", run_in_background=true, load_skills=[],
  description="Find models/schemas",
  prompt="[CONTEXT]: Grosse Codebase. [GOAL]: Finde ALLE Daten-Modelle und Schemas. [REQUEST]: Liste jedes Model mit Feldern, Validierungen, Beziehungen.")

task(subagent_type="explore", run_in_background=true, load_skills=[],
  description="Find utils/helpers",
  prompt="[CONTEXT]: Grosse Codebase. [GOAL]: Finde ALLE Utility-Funktionen die von API-Code genutzt werden. [REQUEST]: Liste jede util mit Zweck, Aufrufern, Side-Effects.")

task(subagent_type="explore", run_in_background=true, load_skills=[],
  description="Find config/constants",
  prompt="[CONTEXT]: Grosse Codebase. [GOAL]: Finde ALLE Konfigurationsdateien und Constants. [REQUEST]: Liste jede Config mit Zweck, Environment-Variablen, Defaults.")

// 5 Librarian-Agenten fuer externe Recherche
task(subagent_type="librarian", run_in_background=true, load_skills=[],
  description="Find API framework docs",
  prompt="[GOAL]: Offizielle Doku fuer das genutzte API-Framework finden. [REQUEST]: Best Practices, Routing-Patterns, Middleware-Ordering, Error-Handling.")

task(subagent_type="librarian", run_in_background=true, load_skills=[],
  description="Find DB best practices",
  prompt="[GOAL]: Datenbank-Best-Practices fuer das genutzte ORM/DB finden. [REQUEST]: Query-Optimierung, Connection-Pooling, Migration-Patterns.")

task(subagent_type="librarian", run_in_background=true, load_skills=[],
  description="Find auth patterns",
  prompt="[GOAL]: Authentifizierungs-Best-Practices finden. [REQUEST]: OAuth2, JWT, Session-Management, Security-Headers, CORS.")

task(subagent_type="librarian", run_in_background=true, load_skills=[],
  description="Find error handling patterns",
  prompt="[GOAL]: Error-Handling-Best-Practices finden. [REQUEST]: HTTP-Status-Codes, Error-Response-Format, Retry-Logic, Circuit-Breaker.")

task(subagent_type="librarian", run_in_background=true, load_skills=[],
  description="Find testing strategies",
  prompt="[GOAL]: Testing-Strategien fuer API-Projekte finden. [REQUEST]: Unit vs Integration, Mocking-Strategien, Test-Data-Management.")
```

**Ergebnis:** 12 Agenten analysieren gleichzeitig verschiedene Bereiche → 95%+ Abdeckung statt 20%.

---

## 🔧 DIE FORMEL: WIEVIELE AGENTEN?

| Projekt-Groesse | Explore-Agenten | Librarian-Agenten | Gesamt |
|-----------------|-----------------|-------------------|--------|
| Klein (< 50 Dateien) | 3 | 2 | 5 |
| Mittel (50-500 Dateien) | 5 | 3 | 8 |
| Gross (500-2000 Dateien) | 7 | 5 | 12 |
| Enterprise (2000+ Dateien) | 10 | 10 | 20 |

---

## 📋 EXPLORATION-CHECKLISTE (fuer jeden explore-Agent)

Jeder explore-Agent MUSS diesen Prompt-Aufbau verwenden:

```
[CONTEXT]: Projekt ist sehr gross (>X Dateien). Einzelne Agenten liefern unvollstaendige Ergebnisse.
[GOAL]: [Was genau soll gefunden werden]
[SCOPE]: [Welche Ordner/Dateien durchsuchen]
[REQUEST]: [Konkrete Ausgabe: Dateipfade + kurze Beschreibung]
[EXCLUDE]: [Was NICHT durchsuchen (tests, node_modules, etc.)]
[TOOLS]: lsp_find_references, ast_grep_search, grep, glob
```

---

## 🔗 ERGEBNISSE ZUSAMMENFUEHREN

Nachdem ALLE background-Agenten fertig sind (system notification):

```python
# Ergebnisse sammeln
explore_results = []
for task_id in explore_task_ids:
    result = background_output(task_id=task_id)
    explore_results.append(result)

librarian_results = []
for task_id in librarian_task_ids:
    result = background_output(task_id=task_id)
    librarian_results.append(result)

# Zusammenfuehren
all_findings = deduplicate(explore_results + librarian_results)
```

---

## 🚨 WARNUNG: WAS NICHT TUN

| ❌ VERBOTEN | ✅ STATDESSEN |
|:---|:---|
| 1 explore-Agent fuer ganzes Projekt | 5-10 parallele Agenten mit spezifischem Fokus |
| `run_in_background=false` | IMMER `run_in_background=true` |
| Generischer Prompt "erkunde das Projekt" | Spezifischer Prompt mit [CONTEXT], [GOAL], [SCOPE] |
| `load_skills=["some-skill"]` | IMMER `load_skills=[]` fuer explore/librarian |
| Ergebnisse sofort nutzen ohne auf alle zu warten | WARTEN bis ALLE background-Agenten fertig sind |

---

## 📝 VORDEFINIERTE EXPLORATION-TEMPLATES

### Template: API-Exploration (7 Agenten)
```
1. "Finde ALLE API-Endpunkte in src/api/"
2. "Finde ALLE Controller in src/controllers/"
3. "Finde ALLE Services in src/services/"
4. "Finde ALLE Middleware"
5. "Finde ALLE Daten-Modelle/ORM-Schemas"
6. "Finde ALLE DTOs/Interfaces/Types"
7. "Finde ALLE Error-Handler/Exception-Klassen"
```

### Template: Architektur-Exploration (8 Agenten)
```
1. "Finde Einstiegspunkte (main, index, app)"
2. "Finde Dependency-Injection/Service-Container"
3. "Finde Event-Handler/Observer/Listeners"
4. "Finde Repository-Pattern/Data-Access-Layer"
5. "Finde Config/Environment-Handling"
6. "Finde Logging/Monitoring/Telemetry"
7. "Finde Auth/Authorization-Implementierung"
8. "Finde External-API-Clients/Integrations"
```

### Template: Feature-Exploration (6 Agenten)
```
1. "Finde ALLE Dateien die [FEATURE-NAME] implementieren"
2. "Finde ALLE Tests fuer [FEATURE-NAME]"
3. "Finde ALLE Dependencies die [FEATURE-NAME] nutzt"
4. "Finde ALLE UI-Komponenten fuer [FEATURE-NAME]"
5. "Finde ALLE API-Endpunkte die [FEATURE-NAME] exponiert"
6. "Finde ALLE Datenbank-Tables/Queries fuer [FEATURE-NAME]"
```

### Template: Librarian-Recherche (5 Agenten)
```
1. "Offizielle Doku fuer [TECHNOLOGIE] - API Reference"
2. "Best Practices fuer [TECHNOLOGIE] in Production"
3. "Open-Source Beispiele fuer [USE-CASE] (1000+ Stars)"
4. "Bekannte Fallstricke/Anti-Patterns fuer [TECHNOLOGIE]"
5. "Performance-Optimierung fuer [TECHNOLOGIE]"
```

---

## ⚡ PERFORMANCE-OPTIMIERUNG

**Regel:** Alle `task()` calls im SELBEN Tool-Call-Block machen = PARALLEL.

```
✅ PARALLEL (alle gleichzeitig):
task(subagent_type="explore", run_in_background=true, prompt="...")
task(subagent_type="explore", run_in_background=true, prompt="...")
task(subagent_type="librarian", run_in_background=true, prompt="...")

❌ SEQUENTIELL (einer nach dem anderen):
task(subagent_type="explore", run_in_background=false, prompt="...")
// wartet auf Ergebnis
task(subagent_type="explore", run_in_background=false, prompt="...")
```

---

## 🔍 QUALITAETS-KONTROLLE

Nachdem alle Ergebnisse da sind, pruefe:
- [ ] Wurden ALLE relevanten Ordner durchsucht?
- [ ] Gibt es Luecken (Dateien die niemand gefunden hat)?
- [ ] Sind die Ergebnisse konsistent (keine Widersprueche)?
- [ ] Wurden sowohl Code ALS AUCH externe Doku gefunden?

Wenn ja → Weiter mit Implementation.
Wenn nein → Zusaetzliche explore-Agenten fuer die Luecken starten.


## Related Skills
- See [Skill Catalog](../../README.md) for related skills
