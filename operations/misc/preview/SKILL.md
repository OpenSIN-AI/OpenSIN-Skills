---
name: preview
description: Öffnet ein Bild (Screenshot etc.) sofort und direkt in der macOS Vorschau-App (Preview).
---

# /preview Skill

Verwende diesen Skill, um dem User Bilder oder Screenshots direkt auf dem Bildschirm anzuzeigen. 
Dieser Skill erzwingt das Öffnen der Datei in der macOS Preview.app. Es ist strengstens verboten, den User aufzubordern, eine Bilddatei manuell im Dateisystem zu suchen.

**Aufruf-Parameter:**
- `file`: Der absolute Pfad zur Bilddatei (z.B. `/tmp/screenshot.png`).

**Ausführung:**
Führe den folgenden Befehl im Bash-Tool aus:
`open -a Preview "<pfad_zur_datei>"`
