---
name: "sin-bridge"
description: "NIEMALS darf irgendwas an sin-bridge geraten werden NICHTS NIEMALS !! NUR ECHTE "
version: "1.0.0"
author: "OpenSIN-AI"
category: "browser-automation"
source: "opensin-native"
status: "active"
triggers:
  - "use sin-bridge"
related_skills: []
---

# 🚨 ABSOLUTES VERBOT FÜR BLINDES RATEN BEI BROWSER/SIN-BRIDGE (PRIORITY -8.0) 🚨
NIEMALS darf irgendwas an sin-bridge geraten werden NICHTS NIEMALS !! NUR ECHTE KONTROLLEN !! nur echte erfassungen !! niemals blind oder geraten NIEMALS !!
Jeder CSS-Selektor, jede Koordinate, jede Aktion MUSS vorher durch den DOM Pre-Scan (Accessibility Tree oder JavaScript Element-Scan) zu 100% verifiziert worden sein. Raten führt zum sofortigen permanenten Ban.

# 🚨 TAB-KONTEXT-HYGIENE (PRIORITY -7.9) 🚨
Wenn ein explizit gesetzter tabId-Wert stale oder nicht mehr sichtbar ist, MUSS der Worker ihn sofort verwerfen und nur innerhalb seines gespeicherten Fensters wiederherstellen. Ein allgemeiner activeTab/currentWindow-Fallback ist verboten.

# 🚨 EXAKTE TAB-BINDUNG (PRIORITY -7.85) 🚨
Der Worker MUSS seine eigene Tab-Identität und sein eigenes Fenster persistieren (`CURRENT_TAB_ID` + `CURRENT_WINDOW_ID`) und darf niemals auf den aktiven Browser-Tab ausweichen. Recovery ist nur innerhalb dieses gespeicherten Fensters und nur für den exakt bekannten HeyPiggy-Tab erlaubt. Andere parallel geöffnete Tabs dürfen den Worker niemals beeinflussen.
---
name: sin-bridge
description: "OpenSIN Bridge + Vision Gate: The ONLY authorized browser automation interface for surveys, profiles, and web forms. Enforces mandatory screenshot + Gemini Vision verification after EVERY SINGLE web action. Zero blind clicks. Zero autorun."
license: Apache-2.0
compatibility: opencode
metadata:
  audience: all-agents
  workflow: browser-automation-with-vision-gate
  trigger: bridge, sin-bridge, prolific, survey, web-automation, browser-automation, vision-gate, screenshot-check
  version: v5.0.0-vision-gate
  priority: "-7.0"
---

# SIN-Bridge Skill v5.0 — Vision Gate Edition

> **PRIORITY -7.0 — ABSOLUTE OBERSTE REGEL IM GESAMTEN OPENSIN-ÖKOSYSTEM**
> Kein Agent darf jemals wieder eine einzige Web-Aktion ausführen ohne visuelle Verifikation durch das Vision-Modell.
> 
> **Die wichtigste Entwicklung der OpenSIN-AI Organisation.**
> Eine Chrome Extension mit 39 MCP Tools, die Antigravity und Claude Code in ALLEN Kategorien schlägt.

## 2. VISION GATE — DAS HERZSTÜCK (PFLICHT BEI JEDER AKTION)

### 2.1 Das Problem (warum Vision Gate existiert)

Agenten haben blind drauflosgeklickt:
- Surveys gestartet aber nie Fragen beantwortet
- Modals bestätigt ohne zu lesen was drinsteht
- Tabs geöffnet und Endlosschleifen gestartet
- "Ich dachte es hat funktioniert" ohne Screenshot-Beweis

**Ein LLM SIEHT NICHT was auf dem Bildschirm passiert. Es RÄT. Raten ist VERBOTEN.**

### 2.2 Die Lösung: Screenshot + Vision-Check nach JEDER Aktion

```
SCHRITT 1: Aktion ausführen (URL, Klick, Tastendruck, Scroll, was auch immer)
SCHRITT 2: SOFORT Screenshot des GESAMTEN Bildschirms machen
SCHRITT 3: Screenshot an Vision-Modell senden mit Kontext-Prompt
SCHRITT 4: Vision-Modell-Antwort LESEN und VERSTEHEN
SCHRITT 5: NUR bei "PROCEED" → nächste Aktion erlaubt
           Bei "STOP" oder "RETRY" → Situation analysieren
```

### 2.3 Vision-Modell Spezifikation

**Primär:** `google/antigravity-gemini-3-flash` via OpenCode CLI
**Fallback:** `look-screen` CLI mit 6-Model Gemini REST API Chain

### 2.4 Vision-Prompt Template (PFLICHT bei jedem Check)

```
Du siehst einen Screenshot eines Browsers nach der Aktion: [BESCHREIBUNG DER AKTION].
Erwartetes Ergebnis: [WAS HÄTTE PASSIEREN SOLLEN].

Prüfe GENAU:
1. Ist das erwartete Ergebnis eingetreten? (JA/NEIN mit Begründung)
2. Gibt es Fehler, Warnungen, Captchas oder Popups? (JA/NEIN, wenn JA: welche?)
3. Ist die Seite vollständig geladen? (JA/NEIN)
4. Was zeigt der Bildschirm GENAU? (Beschreibe alle sichtbaren Elemente)
5. Was ist der empfohlene nächste Schritt? (Konkret)

Antworte mit: PROCEED wenn alles OK ist, STOP wenn etwas falsch ist, RETRY wenn die Aktion wiederholt werden sollte.
```

---

## 3. BRIDGE-WORKFLOW (EXAKTER ABLAUF — KEINE ABKÜRZUNGEN)

### 3.1 Vor dem Start: Health Check

```python
import urllib.request, json

# PFLICHT: Bridge Health prüfen BEVOR irgendwas passiert
health = json.loads(
    urllib.request.urlopen(
        "https://openjerro-opensin-bridge-mcp.hf.space/health",
        timeout=15
    ).read()
)
assert health.get("extensionConnected") is True, "Extension NICHT verbunden! STOP!"
```

### 3.2 Der 10-Schritt Vision-Gate-Workflow

```
 1. Bridge Health prüfen → extension_connected: true?
     ↓ FAIL? → Extension installieren (siehe §7)
 2. Tab navigieren: navigate → URL
 3. ★ VISION-GATE: take_screenshot → Vision-Check → PROCEED?
 4. DOM analysieren: get_accessibility_tree oder get_html
 5. ★ VISION-GATE: take_screenshot → Vision-Check → PROCEED?
 6. Element interagieren: click_element / type_text / select_option
 7. ★ VISION-GATE: take_screenshot → Vision-Check → PROCEED?
 8. Ergebnis prüfen: get_text / get_html
 9. ★ VISION-GATE: take_screenshot → Vision-Check → PROCEED?
10. Nächster Schritt NUR bei PROCEED vom Vision-Modell
```

**Jedes ★ ist ein PFLICHT-Checkpoint. Wer einen überspringt: SOFORTIGER PERMANENTER BAN.**

### 3.3 Python-Implementierung des Vision-Gate-Loops

```python
import subprocess, json, base64, urllib.request

# ============================================================================
# CONSTANTS — Bridge + Vision Konfiguration
# ============================================================================
BRIDGE_MCP_URL = "https://openjerro-opensin-bridge-mcp.hf.space/mcp"
BRIDGE_HEALTH_URL = "https://openjerro-opensin-bridge-mcp.hf.space/health"
MAX_STEPS = 40           # Absolute Obergrenze für Aktionen
MAX_RETRIES = 3          # Max aufeinanderfolgende RETRYs bevor STOP
MAX_NO_PROGRESS = 5      # Max Aktionen ohne sichtbaren Fortschritt

# ============================================================================
# VISION GATE — Das Herzstück
# ============================================================================
def vision_check(screenshot_base64: str, action_description: str, expected_result: str) -> str:
    """
    Sendet einen Screenshot an das Vision-Modell und gibt PROCEED/STOP/RETRY zurück.
    
    WHY: Ein LLM sieht nicht was auf dem Bildschirm passiert. 
         Ohne Vision-Check rät der Agent blind — und das ist VERBOTEN.
    
    CONSEQUENCES: Ohne diesen Check darf KEINE weitere Web-Aktion stattfinden.
    """
    prompt = f"""Du siehst einen Screenshot eines Browsers nach der Aktion: {action_description}.
Erwartetes Ergebnis: {expected_result}.

Prüfe GENAU:
1. Ist das erwartete Ergebnis eingetreten? (JA/NEIN mit Begründung)
2. Gibt es Fehler, Warnungen, Captchas oder Popups? (JA/NEIN, wenn JA: welche?)
3. Ist die Seite vollständig geladen? (JA/NEIN)
4. Was zeigt der Bildschirm GENAU? (Beschreibe alle sichtbaren Elemente)
5. Was ist der empfohlene nächste Schritt? (Konkret)

Antworte mit: PROCEED wenn alles OK ist, STOP wenn etwas falsch ist, RETRY wenn die Aktion wiederholt werden sollte."""
    
    # Vision-Modell aufrufen via opencode CLI (EINZIG ERLAUBTER WEG)
    result = subprocess.run(
        ["opencode", "run", prompt, "--format", "json"],
        capture_output=True, text=True, timeout=60,
    )
    
    parts = []
    for line in result.stdout.splitlines():
        try:
            ev = json.loads(line)
            if ev.get("type") == "text":
                parts.append(ev.get("part", {}).get("text", ""))
        except json.JSONDecodeError:
            pass
    
    response = "".join(parts).strip().upper()
    
    # Extraktion des Verdikts
    if "PROCEED" in response:
        return "PROCEED"
    elif "RETRY" in response:
        return "RETRY"
    else:
        return "STOP"


def vision_gate(screenshot_b64: str, action: str, expected: str, 
                step_number: int, retry_count: int) -> tuple[str, int]:
    """
    Führt den vollständigen Vision-Gate-Check durch.
    
    Returns: (verdict, updated_retry_count)
    
    WHY: Zentrale Funktion die den Vision-Gate-Loop steuert.
    CONSEQUENCES: Bei STOP muss der gesamte Workflow anhalten.
    """
    verdict = vision_check(screenshot_b64, action, expected)
    
    if verdict == "RETRY":
        retry_count += 1
        if retry_count >= MAX_RETRIES:
            print(f"[VISION-GATE] ❌ {MAX_RETRIES}x RETRY → FORCE STOP (Step {step_number})")
            return "STOP", retry_count
        print(f"[VISION-GATE] 🔄 RETRY #{retry_count} (Step {step_number})")
        return "RETRY", retry_count
    elif verdict == "STOP":
        print(f"[VISION-GATE] ❌ STOP bei Step {step_number}")
        return "STOP", 0
    else:
        print(f"[VISION-GATE] ✅ PROCEED (Step {step_number})")
        return "PROCEED", 0
```

---

## 4. BRIDGE MCP TOOLS (VERFÜGBARE WERKZEUGE)

### 4.1 Navigation

| Tool | Beschreibung | Vision-Gate danach? |
|------|-------------|---------------------|
| `navigate` | URL öffnen | **JA — PFLICHT** |
| `go_back` | Browser zurück | **JA — PFLICHT** |
| `go_forward` | Browser vorwärts | **JA — PFLICHT** |
| `reload` | Seite neu laden | **JA — PFLICHT** |

### 4.2 DOM-Interaktion

| Tool | Beschreibung | Vision-Gate danach? |
|------|-------------|---------------------|
| `click_element` | CSS-Selektor klicken | **JA — PFLICHT** |
| `type_text` | Text in Element eingeben | **JA — PFLICHT** |
| `select_option` | Dropdown-Option wählen | **JA — PFLICHT** |
| `get_text` | Text auslesen | Nein (read-only) |
| `get_html` | HTML auslesen | Nein (read-only) |
| `get_accessibility_tree` | DOM-Baum auslesen | Nein (read-only) |

### 4.3 Screenshots & Beobachtung

| Tool | Beschreibung | Vision-Gate danach? |
|------|-------------|---------------------|
| `take_screenshot` | Screenshot machen | Nein (IST der Gate-Input) |
| `tabs_list` | Tabs auflisten | Nein (read-only) |
| `tabs_activate` | Tab wechseln | **JA — PFLICHT** |

### 4.4 Tab-Management

| Tool | Beschreibung | Vision-Gate danach? |
|------|-------------|---------------------|
| `tabs_create` | Neuen Tab öffnen | **JA — PFLICHT** |
| `tabs_close` | Tab schließen | **JA — PFLICHT** |
| `tabs_update` | Tab aktualisieren | **JA — PFLICHT** |

**REGEL:** Alles was den Bildschirm VERÄNDERT braucht Vision-Gate. Alles was nur LIEST nicht.

---

## 5. ANTI-ENDLOSSCHLEIFEN-REGELN

```python
# ============================================================================
# ANTI-ENDLOSSCHLEIFEN-SCHUTZ
# ============================================================================
# 1. Nach 3 aufeinanderfolgenden RETRY → SOFORT STOPPEN
# 2. Nach 5 Aktionen ohne sichtbaren Fortschritt → SOFORT STOPPEN  
# 3. Nach MAX_STEPS (40) Gesamtaktionen → SOFORT STOPPEN
# 4. Bei jedem STOP: Screenshot + Kontext loggen, Issue erstellen
# ============================================================================

class VisionGateController:
    """
    Controller der den Vision-Gate-Loop steuert und Endlosschleifen verhindert.
    
    WHY: Ohne diesen Controller laufen Agenten in Endlosschleifen.
    CONSEQUENCES: Controller-Verletzung = SOFORTIGER PERMANENTER BAN.
    """
    
    def __init__(self):
        self.total_steps = 0
        self.consecutive_retries = 0
        self.no_progress_count = 0
        self.last_screenshot_hash = None
    
    def should_continue(self) -> bool:
        """Prüft ob der Agent weitermachen darf."""
        if self.total_steps >= MAX_STEPS:
            print(f"[GATE] ❌ MAX_STEPS ({MAX_STEPS}) erreicht → STOP")
            return False
        if self.consecutive_retries >= MAX_RETRIES:
            print(f"[GATE] ❌ {MAX_RETRIES}x RETRY → STOP")
            return False
        if self.no_progress_count >= MAX_NO_PROGRESS:
            print(f"[GATE] ❌ {MAX_NO_PROGRESS} Aktionen ohne Fortschritt → STOP")
            return False
        return True
    
    def record_step(self, verdict: str, screenshot_hash: str):
        """Zeichnet einen Schritt auf und aktualisiert Zähler."""
        self.total_steps += 1
        
        if verdict == "RETRY":
            self.consecutive_retries += 1
        else:
            self.consecutive_retries = 0
        
        # Fortschritts-Erkennung via Screenshot-Hash
        if screenshot_hash == self.last_screenshot_hash:
            self.no_progress_count += 1
        else:
            self.no_progress_count = 0
            self.last_screenshot_hash = screenshot_hash
```

---

## 6. VISION-CHECK METHODEN (4 WEGE)

### Methode A: Via webauto-nodriver-mcp observe_screen (BEVORZUGT wenn MCP aktiv)

```
1. observe_screen(include_dom="true")  → liefert Screenshot + DOM
2. Screenshot an Vision-Modell senden
3. Ergebnis auswerten
```

### Methode B: Via screencapture + look-screen CLI

```bash
# Screenshot machen
screencapture -x /tmp/opensin_vision_gate_step_XX.png

# Vision-Analyse anfordern
look-screen --screenshot /tmp/opensin_vision_gate_step_XX.png \
  --describe \
  --prompt "KONTEXT: Ich habe gerade [AKTION] ausgeführt. ..."
```

### Methode C: Via OpenSIN-Bridge take_screenshot (BEVORZUGT für Survey/Profil)

```python
# Bridge-Screenshot holen
screenshot_result = bridge_call("take_screenshot", {})
screenshot_b64 = screenshot_result.get("screenshot", "")

# An Vision-Modell senden
verdict = vision_check(screenshot_b64, "Klick auf 'Next'", "Nächste Frage erscheint")
```

### Methode D: Via multimodal-looker Subagent

```python
# task(subagent_type="multimodal-looker", prompt="Analysiere: ...")
```

---

## 6. KLICK-ESKALATION MIT VISION-GATE (ABSOLUT PFLICHT — SOFORTIGER BAN BEI VERSTOSS)

**GILT FÜR JEDES SCRIPT, JEDEN AGENTEN, JEDEN FLOW DER AUCH NUR EINEN BROWSER-KLICK MACHT.**

### Das verbotene Muster (AUTORUN-Eskalation)

```python
# ❌ VERBOTEN — SOFORTIGER BAN
result = await click_element(selector)
if result.get("error"):
    result = await ghost_click(selector)   # ← blind, kein Vision-Check
    if result.get("error"):
        await keyboard_action(["Enter"])   # ← blind, kein Vision-Check
        # ... 5 Aktionen, KEIN einziger Vision-Check
```

### Die Pflicht-Architektur (VISION-GESTEUERTE ESKALATION)

```
Stufe 1: click_element ausführen
         → SOFORT Screenshot → Vision-Check (ask_vision / _vision_gate_inside_escalation)
         PROCEED? → return True (fertig)
         RETRY?   → weiter zu Stufe 2
         ↓
Stufe 2: ghost_click ausführen
         → SOFORT Screenshot → Vision-Check
         PROCEED? → return True
         RETRY?   → weiter zu Stufe 3
         ↓
Stufe 3: keyboard Enter/Space ausführen
         → SOFORT Screenshot → Vision-Check NACH JEDER TASTE
         PROCEED? → return True
         RETRY?   → weiter zu Stufe 4
         ↓
Stufe 4: vision_click ausführen
         → SOFORT Screenshot → Vision-Check
         PROCEED? → return True
         RETRY?   → weiter zu Stufe 5
         ↓
Stufe 5: coord_click ausführen
         → SOFORT Screenshot → Vision-Check
         PROCEED? → return True
         RETRY?   → STOP, alle Methoden erschöpft, Issue erstellen
```

### Pflicht-Implementierung (Referenz: heypiggy_vision_worker.py)

```python
async def _vision_gate_inside_escalation(step_label, action_done, expected):
    """Screenshot + Vision-Check innerhalb der Klick-Eskalationskette."""
    img_path, _ = await take_screenshot(step_num, label=f"esc_{step_label}")
    if not img_path:
        return {"verdict": "RETRY", "next_action": "none"}
    return await ask_vision(img_path, action_done, expected, step_num)

async def escalating_click(selector, description="", x=None, y=None):
    # Stufe 1: click_element
    result = await execute_bridge("click_element", {"selector": selector, **_tab_params()})
    await asyncio.sleep(0.8)
    decision = await _vision_gate_inside_escalation("after_click_element", f"click_element auf {selector}", "Seite hat reagiert")
    if decision.get("verdict") == "PROCEED":
        return True
    # → Stufe 2, 3, 4, 5 — JEDE mit eigenem Vision-Gate
```

### Was KEIN Ersatz für Vision ist

| Ersatz | Status |
|--------|--------|
| DOM-Change-Check (`dom_verify_change`) | ❌ KEIN Ersatz — nur zusätzlich |
| `result.get("success")` von Bridge | ❌ KEIN Ersatz — Bridge sieht DOM, nicht Bildschirm |
| URL-Vergleich vor/nach | ❌ KEIN Ersatz — Survey-Seiten ändern URL nicht |
| "Ich weiß was auf der Seite ist" | ❌ BAN — LLM SIEHT NICHT, Vision SIEHT |

### Gilt absolut für

- Jede `escalating_click` Funktion in jedem Script
- Jeden Helper/Utility der intern Bridge-Clicks ausführt
- Jeden n8n-Node der Browser-Aktionen triggert
- Jede A2A-Funktion mit Web-Interaktion
- Jeden Dashboard-Gatekeeper-Block, Gate-Klick, Onboarding-Bypass
- **KEINE AUSNAHMEN. KEIN "das ist nur ein kleiner Helper".**

---

## 7. EXTENSION INSTALLATION (WENN NICHT VERBUNDEN)

### 7.1 Schnell-Check

```python
import urllib.request, json

def is_bridge_connected() -> bool:
    """Prüft ob die Bridge-Extension verbunden ist."""
    try:
        health = json.loads(
            urllib.request.urlopen(
                "https://openjerro-opensin-bridge-mcp.hf.space/health",
                timeout=10
            ).read()
        )
        return health.get("extensionConnected") is True
    except Exception:
        return False
```

### 7.2 Keyboard-Installation (7 Schritte)

Siehe: `references/install-extension-via-keyboard.md`

**Schnell-Zusammenfassung:**
1. CMD+LEERTASTE (Spotlight öffnen)
2. "chrome" + ENTER (Chrome öffnen)
3. TAB 4x + ENTER (Adressleiste)
4. TAB 3x + LEERTASTE (Extensions-Bereich)
5. TAB 10x + ENTER (Developer Mode aktivieren)
6. TAB 2x + ENTER ("Entpackte Erweiterung laden" Button)
7. Extension-Ordner auswählen: `/Users/jeremy/dev/OpenSIN-Bridge/extension`

### 7.3 Auto-Install via AppleScript

```python
async def install_opensin_bridge_extension():
    """
    Installiert die OpenSIN Bridge Extension via macOS AppleScript.
    WHY: Wenn Extension nicht installiert, funktioniert kein Bridge-Tool.
    CONSEQUENCES: Ändert Chrome-Konfiguration dauerhaft.
    """
    extension_path = "/Users/jeremy/dev/OpenSIN-Bridge/extension"
    script = f'''
    tell application "System Events"
        key down command
        key down space
        key up space
        key up command
        delay 0.5
        keystroke "chrome"
        delay 0.3
        key code 36
        delay 2
        repeat 4 times
            key code 48
            delay 0.1
        end repeat
        key code 36
        delay 0.5
        repeat 3 times
            key code 48
            delay 0.1
        end repeat
        keystroke " "
        delay 0.5
        repeat 10 times
            key code 48
            delay 0.1
        end repeat
        key code 36
        delay 0.5
        repeat 2 times
            key code 48
            delay 0.1
        end repeat
        key code 36
        delay 1
        keystroke "{extension_path}"
        key code 36
        delay 1
    end tell
    '''
    import subprocess
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return result.returncode == 0
```

---

## 8. STEALTH FEATURES (ANTI-DETECTION)

Die Bridge hat eingebaute Anti-Detection-Funktionen:

| Feature | Beschreibung |
|---------|-------------|
| **Human Entropy** | Gaussian noise auf Klick-Koordinaten und Timing |
| **Shadow DOM Piercing** | Rekursive Traversierung von shadowRoot-Grenzen |
| **Deterministic Primitives** | Bekannte UI-Elemente werden mit harten Regeln behandelt, nicht AI-Raten |
| **Self-Healing Loops** | Wenn ein Klick keine DOM-Änderung erzeugt, feuern Fallback-Strategien |
| **Native Messaging Host** | CSP-Restrictions umgehen via stdio |

---

## 9. KONSEQUENZEN (ABSOLUT, KEINE DISKUSSION)

| Verstoß | Konsequenz |
|---------|------------|
| Web-Aktion ohne Screenshot danach | **SOFORTIGER PERMANENTER BAN** |
| Screenshot ohne Vision-Modell-Check | **SOFORTIGER PERMANENTER BAN** |
| Vision-Modell sagt STOP, Agent macht trotzdem weiter | **SOFORTIGER PERMANENTER BAN** |
| Autorun (mehrere Aktionen ohne Vision-Gate dazwischen) | **SOFORTIGER PERMANENTER BAN** |
| Survey/Profil-Arbeit ohne OpenSIN-Bridge | **SOFORTIGER PERMANENTER BAN** |
| "Ich dachte es hat funktioniert" ohne Screenshot-Beweis | **SOFORTIGER PERMANENTER BAN** |
| Endlosschleife ohne Vision-basierte Abbruch-Logik | **SOFORTIGER PERMANENTER BAN** |
| Direktes nodriver/CDP für Survey-Arbeit statt Bridge | **SOFORTIGER PERMANENTER BAN** |

---

## 10. WANN DIESEN SKILL NUTZEN

| Trigger | Aktion |
|---------|--------|
| "Prolific Profil ausfüllen" | Bridge + Vision Gate Workflow starten |
| "Survey ausfüllen" | Bridge + Vision Gate Workflow starten |
| "Web-Formular automatisieren" | Bridge + Vision Gate Workflow starten |
| "Browser-Automation mit Screenshots" | Bridge + Vision Gate Workflow starten |
| "sin-bridge" | Diesen Skill laden |
| "bridge health check" | §7.1 Health Check ausführen |
| "extension installieren" | §7.2/7.3 Extension Installation |

---

## 11. ZUSAMMENFASSUNG IN EINEM SATZ

**KEIN EINZIGER KLICK, KEIN EINZIGER TASTENDRUCK, KEINE EINZIGE URL, KEINE EINZIGE WEB-AKTION OHNE DASS `antigravity-gemini-3-flash` VORHER EINEN SCREENSHOT DES GESAMTEN BILDSCHIRMS ANALYSIERT UND MIT "PROCEED" BESTÄTIGT HAT. PUNKT. KEINE AUSNAHMEN. NIEMALS.**

---

## 12. RESSOURCEN

- [OpenSIN-Bridge Repo](https://github.com/OpenSIN-AI/OpenSIN-Bridge)
- [Bridge HF Space](https://openjerro-opensin-bridge-mcp.hf.space)
- [Vision Gate Mandate in AGENTS.md](~/.config/opencode/AGENTS.md) — Zeile 1
- [Gemini Vision API](https://ai.google.dev/gemini-api/docs/vision)
- Extension Path: `/Users/jeremy/dev/OpenSIN-Bridge/extension`


---

## Architektur

```
AI Agent (via opencode CLI)
        │
        ▼ (WebSocket)
HF MCP Server (immer online)
  wss://openjerro-opensin-bridge-mcp.hf.space
        │
        ▼ (WebSocket)
OpenSIN Bridge v2.6.0 (Chrome Extension)
        │
        ▼ (Chrome APIs)
Chrome Browser (deine Sessions, deine Cookies)
```

## Quick Start

### 1. Extension laden (einmalig)
```bash
# Repo clonen
git clone https://github.com/OpenSIN-AI/OpenSIN-backend.git
cd OpenSIN-backend/services/sin-chrome-extension

# In Chrome laden:
# 1. chrome://extensions/ öffnen
# 2. Entwicklermodus aktivieren
# 3. "Entpackte Erweiterung laden" → extension/ Ordner
```

### 2. MCP Server nutzen (immer online)
Der HF MCP Server läuft bereits und ist immer erreichbar:
- **URL:** https://huggingface.co/spaces/OpenJerro/opensin-bridge-mcp
- **Health:** https://openjerro-opensin-bridge-mcp.hf.space/health
- **WebSocket:** `wss://openjerro-opensin-bridge-mcp.hf.space`

## Verfügbare Tools (39)

### Tab Management (5)
- `tabs_list` — Alle Tabs auflisten
- `tabs_create` — Neuen Tab öffnen
- `tabs_update` — Tab aktualisieren
- `tabs_close` — Tab schließen
- `tabs_activate` — Tab aktivieren

### Navigation (4)
- `navigate` — Zu URL navigieren
- `go_back` — Zurück
- `go_forward` — Vorwärts
- `reload` — Seite neu laden

### DOM Interaction (10)
- `click_element` — Element klicken (Standard)
- `ghost_click` — Element klicken mit vollem Mouse/Pointer-Event-Stack (Für SPA/React Survey-Cards!)
- `click_coordinates` — Klick auf absolute x,y Koordinaten (CDP/DOM-Fallback)
- `type_text` — Text eingeben
- `get_text` — Textinhalt lesen
- `get_html` — HTML lesen
- `get_attribute` — Attribut lesen
- `wait_for_element` — Auf Element warten
- `execute_script` — JavaScript ausführen (CSP-safe)
- `inject_css` — CSS injizieren

### Page Info (3)
- `get_page_info` — Title, URL, readyState
- `get_all_links` — Alle Links extrahieren
- `get_all_inputs` — Alle Formularfelder extrahieren

### Screenshot & Video (5)
- `screenshot` — Screenshot machen
- `screenshot_full` — Vollständiger Screenshot
- `start_recording` — Videoaufnahme starten
- `stop_recording` — Videoaufnahme stoppen
- `recording_status` — Aufnahmestatus prüfen

### Cookies (4)
- `get_cookies` — Cookies lesen
- `set_cookie` — Cookie setzen
- `delete_cookie` — Cookie löschen
- `clear_cookies` — Alle Cookies löschen

### Storage (3)
- `storage_get` — Local Storage lesen
- `storage_set` — Local Storage schreiben
- `storage_clear` — Local Storage löschen

### Network (2)
- `get_network_requests` — Request-Log lesen
- `block_url` — URL blockieren

### Stealth Mode (2)
- `enable_stealth` — Anti-Detection aktivieren
- `stealth_status` — Stealth-Status prüfen

### Prolific (1)
- `extract_prolific_studies` — Verfügbare Studies extrahieren

### System (3)
- `health` — Extension-Status prüfen
- `list_tools` — Alle Tools auflisten
- `offscreen_status` — Offscreen-Dokument-Status

## Beispiele

### Study auf Prolific finden und öffnen
```python
import asyncio, websockets, json

async def find_study():
    async with websockets.connect('wss://openjerro-opensin-bridge-mcp.hf.space/agent') as ws:
        # Navigate to Prolific
        await ws.send(json.dumps({
            'method': 'navigate',
            'params': {'url': 'https://app.prolific.com/studies'},
            'id': 1
        }))
        await asyncio.sleep(15)  # Wait for React SPA
        
        # Extract studies
        await ws.send(json.dumps({
            'method': 'extract_prolific_studies',
            'id': 2
        }))
        resp = await ws.recv()
        result = json.loads(resp)
        print(f"Studies: {result}")

asyncio.run(find_study())
```

### Stealth Mode aktivieren
```python
await ws.send(json.dumps({
    'method': 'enable_stealth',
    'id': 3
}))
```

### Screenshot machen
```python
await ws.send(json.dumps({
    'method': 'screenshot',
    'id': 4
}))
```

## Prolific Worker

Der **A2A-SIN-Worker-Prolific** läuft 24/7 und prüft automatisch alle 5 Minuten auf verfügbare Studies:

```bash
# Worker starten
cd /Users/jeremy/dev/A2A-SIN-Worker-Prolific
python3 src/worker.py

# Production Mode (navigiert zu Plattformen)
TEST_MODE=false python3 src/worker.py
```

## Vergleich: OpenSIN Bridge vs Claude Code

| Feature | Claude Code | OpenSIN Bridge v2.6.0 |
|---------|-------------|----------------------|
| Tools | ~5 | **39** |
| Video Recording | ❌ | ✅ |
| Stealth Mode | ❌ | ✅ |
| Cookie CRUD | ❌ | ✅ |
| Network Logging | ❌ | ✅ |
| URL Blocking | ❌ | ✅ |
| Offscreen Processing | ❌ | ✅ |
| 24/7 Worker | ❌ | ✅ |
| Open Source | ❌ | ✅ |
| Local Privacy | ❌ (Cloud Relay) | ✅ (Unix Socket) |

## Wichtige Hinweise

1. **CSP-Safe execute_script**: Alle Script-Injections nutzen den `code` Parameter, nicht `func`. Das umgeht Chrome's CSP `unsafe-eval` Restriction.

2. **Single Tab Mode**: Der Worker öffnet niemals neue Tabs für dieselbe Plattform. Er reused existierende Tabs, um Ban-Risiken zu minimieren.

3. **Safe Mode**: Standardmäßig läuft der Worker im `TEST_MODE=true`, der keine Navigation zu Plattformen durchführt. Für Production: `TEST_MODE=false`.

4. **Session Detection**: Der Worker erkennt automatisch abgelaufene Sessions (Login-Redirects) und wartet auf manuelles Einloggen, statt zu crashen.

## Links

- 📦 **Repo:** https://github.com/OpenSIN-AI/OpenSIN-backend/tree/main/services/sin-chrome-extension
- 🤖 **Worker:** https://github.com/OpenSIN-AI/A2A-SIN-Worker-Prolific
- 🌐 **HF MCP Server:** https://huggingface.co/spaces/OpenJerro/opensin-bridge-mcp
- 📖 **Dokumentation:** https://opensin.ai/docs/bridges/opensin-bridge-overview
- 📝 **Blog Post:** https://github.com/OpenSIN-AI/OpenSIN-Marketing-Release-Strategie/blob/main/blog-posts/21-opensin-bridge-vs-claude-code.md


## Related Skills
- See [Skill Catalog](../../README.md) for related skills
