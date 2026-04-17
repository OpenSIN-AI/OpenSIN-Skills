---
name: stealth-browser-operator
description: Autonomer Browser-Operator mit Stealth-Proxy, automatischer Videoaufzeichnung, TTS-Vertonung und FFmpeg-Watermarking. Nutzt browser-use fuer Browser-Automatisierung, edge-tts/Kokoro fuer Sprachausgabe und FFmpeg fuer Post-Production.
---

# Stealth Browser Operator SKILL

## Zweck

Dieser Skill befähigt Agenten, Webseiten vollständig autonom zu steuern, Firewalls/Cloudflare zu umgehen, alle Aktionen als Video aufzuzeichnen, mit TTS zu vertonen und mit Logo/Text zu versehen.

## Architektur-Übersicht

```
┌─────────────────────────────────────────────────────────────┐
│                    Stealth Browser Operator                   │
├────────────┬──────────────┬──────────────┬──────────────────┤
│ Phase 1    │ Phase 2      │ Phase 3      │ Phase 4          │
│ Proxy +    │ Browser      │ TTS +        │ FFmpeg           │
│ Browser    │ Navigation   │ Voiceover    │ Watermarking     │
│ Recording  │ + Recording  │ Generation   │ + Merge          │
└────────────┴──────────────┴──────────────┴──────────────────┘
```

## Phase 1: Browser-Vorbereitung

**WICHTIG:** Nutze IMMER das eingeloggte Chrome-Profil. Niemals leere Profile!

```bash
# Prüfe ob browser-use installiert ist
python3 -c "import browser_use; print('browser-use OK')" || bun add browser-use

# Recording-Verzeichnis erstellen
mkdir -p ~/.config/opencode/tools/recordings/$(date +%Y%m%d_%H%M%S)
```

## Phase 2: Browser-Automatisierung mit Videoaufzeichnung

Führe das browser-use Python-Skript aus:

```bash
python3 ~/.config/opencode/tools/browser-recorder.py \
  --url "<ZIEL-URL>" \
  --task "<BESCHREIBUNG DER AKTION>" \
  --output-dir "~/.config/opencode/tools/recordings/$(date +%Y%m%d_%H%M%S)" \
  --profile "Default"
```

**Parameter:**
- `--url`: Die Ziel-Webseite
- `--task`: Natürlichsprachige Beschreibung was der Agent tun soll
- `--output-dir`: Verzeichnis für das .mp4-Video
- `--profile`: Chrome-Profil-Name (Default, Geschäftlich, etc.)

**Das Skript:**
- Startet Chrome mit echtem Profil (eingeloggte Sessions)
- Zeichnet ALLE Aktionen als .mp4 auf (save_recording_path)
- Navigiert zur URL und führt die beschriebene Aufgabe aus
- Speichert Video + Screenshots im output-dir

## Phase 3: TTS-Vertonung (Sprachausgabe)

### Option A: edge-tts (kostenlos, schnell)

```bash
python3 ~/.config/opencode/tools/tts-generator.py \
  --text "<ZU SPRECHENDER TEXT>" \
  --output "~/.config/opencode/tools/recordings/$(date +%Y%m%d_%H%M%S)/voiceover.mp3" \
  --voice "de-DE-KatjaNeural"
```

### Option B: Kokoro-82M (lokal, CPU-freundlich)

```bash
python3 ~/.config/opencode/tools/tts-generator.py \
  --text "<ZU SPRECHENDER TEXT>" \
  --output "~/.config/opencode/tools/recordings/$(date +%Y%m%d_%H%M%S)/voiceover.wav" \
  --engine kokoro
```

**Verfügbare edge-tts Stimmen (Deutsch):**
- `de-DE-KatjaNeural` — Weiblich, natürlich (EMPFOHLEN)
- `de-DE-ConradNeural` — Männlich
- `de-DE-AmalaNeural` — Weiblich, warm
- `de-DE-BerndNeural` — Männlich, tief
- `de-DE-ChristophNeural` — Männlich, professionell
- `de-DE-ElkeNeural` — Weiblich, freundlich
- `de-DE-GiselaNeural` — Weiblich, reif
- `de-DE-KasperNeural` — Männlich, jung
- `de-DE-KillianNeural` — Männlich, kräftig
- `de-DE-KlarissaNeural` — Weiblich, klar
- `de-DE-KlausNeural` — Männlich, seriös
- `de-DE-LouisaNeural` — Weiblich, jugendlich
- `de-DE-MajaNeural` — Weiblich, sanft
- `de-DE-RalfNeural` — Männlich, energisch
- `de-DE-TanjaNeural` — Weiblich, professionell

## Phase 4: FFmpeg Post-Production (Custom Tool)

Verschmelze Video + Audio + Logo + Text:

```bash
python3 ~/.config/opencode/tools/video-processor.py \
  --input-video "~/.config/opencode/tools/recordings/<DATUM>/recording.mp4" \
  --audio "~/.config/opencode/tools/recordings/<DATUM>/voiceover.mp3" \
  --output "~/.config/opencode/tools/recordings/<DATUM>/final.mp4" \
  --logo "/path/to/opensin-logo.png" \
  --logo-pos "top-right" \
  --text "OpenSIN AI — Autonomous Agent Demo" \
  --text-pos "bottom-center"
```

**FFmpeg Complex Filter:**
```
-logo (overlay=main_w-overlay_w-10:10) +
-text (drawtext=text='...':x=(w-text_w)/2:y=h-th-10) +
-audio (-c:a copy)
= fertiges Video
```

## Phase 5: Ein-Befehl-Master (Alles kombiniert)

Für maximale Effizienz — EIN Befehl, alles automatisch:

```bash
python3 ~/.config/opencode/tools/master-operator.py \
  --url "https://example.com" \
  --task "Klicke auf Login, gehe zu Dashboard, öffne Einstellungen" \
  --tts-text "Willkommen bei OpenSIN AI. Ich zeige dir jetzt die autonome Browser-Steuerung." \
  --logo "/Users/jeremy/dev/OpenSIN-documentation/docs/public/logo.png" \
  --output-dir "~/.config/opencode/tools/recordings/$(date +%Y%m%d_%H%M%S)" \
  --chrome-profile "Default"
```

## Wichtige Regeln

### Vision-Gate (PRIORITY -7.0)
- NACH jeder Browser-Aktion MUSS ein Screenshot gemacht werden
- Der Screenshot MUSS durch ein Vision-Modell geprüft werden
- NUR bei PROCEED darf die nächste Aktion erfolgen

### DevTools-First (PRIORITY -1.0)
- CSS-Selektoren NIEMALS raten
- IMMER via DevTools/CDP verifizieren
- `document.querySelector()` in Console ausführen

### Technologie-Souveränität (PRIORITY -2.0)
- NUR browser-use + Chrome Profil
- KEIN Playwright, Puppeteer, Selenium, Camoufox
- Chrome-basiert, kein WebDriver

### Bun-Only (PRIORITY -1.5)
- Installation: `bun add browser-use`
- KEIN `npm install`

## Output-Struktur

Jede Session erzeugt:

```
recordings/<DATUM_UHRZEIT>/
├── recording.mp4          # Roh-Aufnahme der Browser-Session
├── screenshots/           # Einzel-Screenshots pro Schritt
│   ├── step_001.png
│   ├── step_002.png
│   └── ...
├── voiceover.mp3          # Generierte TTS-Audio
├── final.mp4              # Fertiges Video mit Wasserzeichen
└── metadata.json          # Session-Metadaten (URL, Task, Datum)
```

## Troubleshooting

### "browser-use not found"
```bash
bun add browser-use
# oder
pip3 install browser-use[video]
```

### "edge-tts nicht installiert"
```bash
bun add edge-tts
# oder
pip3 install edge-tts
```

### "ffmpeg nicht gefunden"
```bash
brew install ffmpeg
```

### Video zu groß
```bash
# Komprimieren
ffmpeg -i final.mp4 -vcodec libx264 -crf 28 compressed.mp4
```

## Verwandte Skills
- [browser-automation](/best-practices/browser-automation) — Best Practices
- [video-tutorial-operator](../video-tutorial-operator/SKILL.md) — Master-Skill für Tutorials
