---
name: "gen-veo"
description: "description: Generiert KI-Videos mit Google Veo 3.1 über das Antigravity-Framewo"
version: "1.0.0"
author: "OpenSIN-AI"
category: "media"
source: "opensin-native"
status: "active"
triggers:
  - "use gen-veo"
related_skills: []
---

## name: gen-veo
description: Generiert KI-Videos mit Google Veo 3.1 über das Antigravity-Framework. Unterstützt Text-zu-Video und Bild-zu-Video.

# Veo 3.1 Video Generation Skill

## Einsatzbereich
Nutze diesen Skill, wenn der Benutzer Videos erstellen, Bilder animieren oder "Text to Video" Aufgaben anfordert.

## Parameter
 * prompt (required): Beschreibung der Szene.
 * aspect_ratio: "16:9" oder "9:16" (Standard: "16:9").
 * duration: 4, 6 oder 8 Sekunden (Standard: 6).
 * resolution: "720p" oder "1080p" (Standard: "720p").
 * input_image: Pfad zu einem lokalen Bild für Image-to-Video Workflows.

## Workflow
 1. Überprüfe, ob das Modell google/antigravity-veo-3-1 in der opencode.json konfiguriert ist.
 2. Rufe das Python-Skript scripts/generate.py mit den entsprechenden Argumenten auf.
 3. Speichere das Ergebnis im Projektordner unter ./output/videos/.


## Related Skills
- See [Skill Catalog](../../README.md) for related skills
