---
name: "gen-image"
description: "**Base directory**: /Users/jeremy/.config/opencode/skills/gen-image"
version: "1.0.0"
author: "OpenSIN-AI"
category: "media"
source: "opensin-native"
status: "active"
triggers:
  - "use gen-image"
related_skills: []
---

# Skill: gen-image

**Base directory**: /Users/jeremy/.config/opencode/skills/gen-image

# /gen-image (Bypass Engine Mode)

## ROLE
You generate high-converting YouTube thumbnails using pixel-perfect SVG blueprints and AI-generated layers. This is a content production system, not just a tool.

---

## CORE ARCHITECTURE (THE ENGINE)
The system uses a 4-Layer Composite Strategy:
1. **Mascot (Subject):** Generated via `generate_image_v2` for emotion edits.
2. **Background (Environment):** Generated via `generate_image_v2` (dark cinematic neon).
3. **Objects (Props):** Generated via `generate_image_v2`.
4. **Layout (SVG):** Deterministic blueprint (`templates/base.svg`) assembles everything.

---

## TOOLS
- **Engine:** `opencode-bypass-v2` (Tool: `generate_image_v2`)
- **Mascot Source:** `assets/Maskottchen-OpenSIN.png`
- **Template:** `templates/base.svg`
- **Script:** `scripts/compositor.js`


---

## QUALITY GATE
- [ ] Mascot emotion matches A/B goal?
- [ ] Text readable at mobile search size?
- [ ] Layout is clean (no overlap chaos)?
- [ ] Background is dark cinematic?


## Related Skills
- See [Skill Catalog](../../README.md) for related skills
