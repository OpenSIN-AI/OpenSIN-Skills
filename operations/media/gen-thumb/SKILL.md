---
name: "gen-thumb"
description: "**Name:** gen-thumb"
version: "1.0.0"
author: "OpenSIN-AI"
category: "media"
source: "opensin-native"
status: "active"
triggers:
  - "use gen-thumb"
related_skills: []
---

# gen-thumb Skill

**Name:** gen-thumb  
**Beschreibung:** Erstellt virale YouTube-Thumbnails im Layer-Verfahren. Nutzt das Antigravity Image Plugin für Bildgenerierung und lokale Layer-Compositing-Schritte mit Character-Consistency-Unterstützung.

## YouTube Thumbnail Pro Workflow

Die Most-Best-Practice für Klicks ist ein **Layered Workflow** — nicht alles in einem Prompt generieren, sondern jede Komponente separat und dann sauber compositen.

### Vorgehensweise

1. **Briefing:** Analysiere das Thema und identifiziere die Kern-Emotion (surprised, shocked, excited, angry, curious).
2. **Asset Generation:**
   - **Background:** Generiere einen Hintergrund (16:9) via Antigravity Image, passend zum Thema.
   - **Mascot Source:** Lege Referenzbilder in `assets/mascot/` ab. Der Composer nimmt das jüngste Bild als Source und verarbeitet es lokal mit Emotion/Glow.
   - **Object:** Der Fokus-Objekt-Layer wird separat als eigene Ebene erzeugt.
3. **Text-Design:** Erstelle prägnanten Text (1-3 Wörter, max 4) in kräftigen Farben (weiß/gold) mit dicken Strichen und Schatten. Wird lokal mit Pillow gerendert.
4. **Compositing:** `scripts/composer.py` fügt alle Layer mit professionellen Effekten (Schatten, Kontrast, Tiefenunschärfe) zusammen.

## Parameter

- `topic` (required) — Das Thema des Videos (z.B. "Warum KI-Agenten obsolet werden")
- `emotion` (optional) — Gewünschte Reaktion, z.B. `surprised`, `shocked`, `excited`, `angry`, `curious`. Default: `shocked`
- `text` (optional) — Der Text auf dem Bild (max. 4 Wörter). Default: Wird automatisch aus topic generiert.

## Beispiel-Aufruf

```
/gen-thumb topic="Wie ich in 24h reich wurde" emotion="shocked" text="UNGLAUBLICH!"
```

## Technische Details

- **Bildgenerierung:** `generate_image` via Antigravity OAuth (aktueller Plugin-Release: Gemini 3 Pro Image)
- **Referenzbilder:** Lege bis zu 4 Bilder in `assets/mascot/` ab. Der Composer nutzt den jüngsten Source-Asset-Foto-Stand als Eingabe für die Mascot-Ebene.
- **Green-Screen-/Glow-Trick:** Hintergrund wird KI-generiert; Mascot/Object werden mit lokalen Glow- und Chroma-Key-Filtern sauber integriert.
- **Output:** `outputs/thumbnails/thumbnail_A|B.png` + `outputs/layers/` für alle Ebenen.
- **Preview:** `outputs/previews/preview.html` mit beiden Varianten inline.

## Implementierung

Der Skill besteht aus:
- `SKILL.md` (diese Datei)
- `assets/mascot/` — Hier Deine Referenzbilder des Maskottchens ablegen (PNG, transparent bevorzugt)
- `scripts/`:
  - `composer.py` — Orchestriert den gesamten Workflow, ruft Layer-Generatoren auf, führt Compositing durch.
  - `layer_1_background.py` — Antigravity Image für Hintergrund
  - `layer_2_object_local.py` — Lokaler Objekt-Layer (Pillow)
  - `layer_3_mascot.py` — Lokaler Mascot-Processor (Pillow)
  - `layer_4_text.py` — Pillow-Textebene
  - `compose_thumbnail.py` — Finaler Compositor mit Blenden und Schatten
- `fixtures/` — Rubric, Referenz-Thumbnails, Brand-Config

---

## Warum das besser funktioniert

- **Character Consistency:** Durch Referenzbilder bleibt das Maskottchen immer gleich, nur die Mimik ändert sich.
- **Quality Separation:** Jede Ebene wird einzeln optimiert, nicht im komplexen Multi-Prompt geraten.
- **Local Fast:** Nur die Generierung braucht API; Composition ist rein lokal (Pillow).
- **MrBeast-approved:** Diese Layer-Technik wird von Top-Creatern verwendet.


## Related Skills
- See [Skill Catalog](../../README.md) for related skills
