---
name: awesome-opensin-design
description: Design-System Skill für ALLE OpenSIN-AI Webseiten und Webapps. Shopify-basiertes Dark-First Design mit Neon-Green Accent, ultra-light Display Type und cinematischem Layout. PFLICHT für opensin.ai, my.opensin.ai, blog.opensin.ai und alle weiteren Frontends.
metadata:
  audience: frontend-agents
  workflow: design-enforcement
---

# Awesome OpenSIN Design

**Shopify-inspiriertes Design-System für ALLE OpenSIN-AI Frontends.**

Dieser Skill erzwingt ein einheitliches, professionelles Design über alle OpenSIN-Webseiten und Webapps. Keine Ausnahmen. Kein Agent darf ein Frontend ohne dieses Design bauen.

---

## 🚨 ABSOLUTES MANDAT

**JEDE OpenSIN-AI Webseite MUSS dieses Design-System verwenden:**

- ✅ `opensin.ai` — Hauptwebsite
- ✅ `my.opensin.ai` — Dashboard & Marketplace
- ✅ `blog.opensin.ai` — Engineering Blog
- ✅ `opensin.ai/simone-mcp` — Simone MCP Landing Page
- ✅ ALLE zukünftigen Frontends

**VERBOTEN:**
- ❌ Eigenmächtige Design-Entscheidungen ohne Bezug zu diesem Skill
- ❌ Helle Themes (dunkel-first ist Pflicht)
- ❌ Andere Akzentfarben als das definierte Grün
- ❌ Schwere Font-Weights (>500) für Headings

---

## 🎨 Design System

**Quelle:** `Delqhi/awesome-OpenSIN-design` (GitHub)
**Lokal:** `~/.config/opencode/skills/awesome-opensin-design/DESIGN.md`

### Color Palette

| Token | Hex | Verwendung |
|-------|-----|------------|
| `--background` | `#0a0a0a` | Seitenhintergrund, Canvas |
| `--surface-1` | `#141414` | Cards, elevated surfaces |
| `--surface-2` | `#1a1a1a` | Secondary cards, modals |
| `--surface-3` | `#222222` | Input backgrounds |
| `--accent` | `#008060` | Primary CTA, Links |
| `--accent-hover` | `#006e52` | Hover states |
| `--accent-glow` | `#00ff9e` | Neon-Glow für Hero, Badges |
| `--text-primary` | `#f5f5f5` | Headlines, Body |
| `--text-secondary` | `#a0a0a0` | Labels, descriptions |
| `--text-muted` | `#666666` | Placeholder, disabled |
| `--border` | `#2a2a2a` | Borders, Divider |
| `--error` | `#e04f5f` | Error States |
| `--success` | `#00cc88` | Success States |
| `--warning` | `#ffcc00` | Warning States |

### Typography

| Level | Size | Weight | Line Height | Use |
|-------|------|--------|-------------|-----|
| display-1 | 72px | 100 | 1.1 | Hero Headlines |
| display-2 | 56px | 100 | 1.15 | Section Hero |
| h1 | 48px | 500 | 1.2 | Page Titles |
| h2 | 36px | 500 | 1.25 | Section Titles |
| h3 | 28px | 500 | 1.3 | Subsections |
| h4 | 22px | 500 | 1.35 | Card Titles |
| body-lg | 18px | 400 | 1.6 | Lead Paragraphs |
| body | 16px | 400 | 1.6 | Body Text |
| body-sm | 14px | 400 | 1.5 | Captions |
| code | 14px | 400 | 1.5 | Code Blocks |

**Fonts:**
- Display/Headings/Body: `Inter`, system-ui
- Code: `JetBrains Mono`, `Fira Code`

### Komponenten

#### Buttons
- Primary: `#008060` background, `#ffffff` text, 8px radius
- Secondary: transparent, `1px solid #2a2a2a` border
- Ghost: transparent, no border
- Destructive: `#e04f5f` background

#### Cards
- Background: `#141414`
- Border: `1px solid #2a2a2a`
- Hover: `border-color: #008060`, `box-shadow: 0 0 20px rgba(0,128,96,0.1)`
- Radius: 12px

#### Navigation
- Sticky, `backdrop-filter: blur(12px)`
- Background: `rgba(10,10,10,0.8)`
- Active: green left border + green text
- Hover: text `#a0a0a0` → `#f5f5f5`

### Layout

- Max content width: 1200px
- Grid: 12 columns (desktop), 4 (tablet), 1 (mobile)
- Section padding: 96px vertical (desktop), 64px (mobile)
- Card gap: 24px

### Responsive Breakpoints

| Breakpoint | Width | Changes |
|------------|-------|---------|
| xl | 1440px+ | 12-col, 48px padding |
| lg | 1024px | 8-col, 32px padding |
| md | 768px | 4-col, 24px padding, mobile nav |
| sm | 640px | 1-col, touch targets 44px |

---

## 📐 Do's and Don'ts

### Do
- ✅ Dark surfaces als primäres Canvas
- ✅ Neon-Grün (`#00ff9e`) NUR für kritische Aktionen
- ✅ Ultra-light display type (100-200) für Hero Headlines
- ✅ Full-bleed Imagery in Hero Sections
- ✅ Generous Whitespace (96px+ zwischen Sections)
- ✅ Subtle green border-glow on card hover

### Don't
- ❌ Weiße Hintergründe für Primärseiten
- ❌ Multiple Akzentfarben in derselben Section
- ❌ Schwere Font-Weights (>500) für Headings
- ❌ Zu viele CTAs in Hero (max 2)
- ❌ Scharfe Ecken (min 8px border-radius)
- ❌ Light text auf light backgrounds

---

## 🔧 AI Agent Prompt Guide

Wenn ein AI Agent eine OpenSIN-Seite bauen soll:

> "Baue eine Dark-First Landing Page im Shopify-Stil. Verwende #0a0a0a Hintergrund, #008060 Green Accent, ultra-light Inter 100 für Hero Text bei 72px. Cards mit #141414 Background, #2a2a2a Border, Green Glow on Hover. Navigation sticky mit backdrop-blur. Responsive mit Mobile Drawer."

**Quick Color Reference:**
```
Background:  #0a0a0a
Surface:     #141414
Accent:      #008060
Neon:        #00ff9e
Text:        #f5f5f5
Muted:       #666666
Border:      #2a2a2a
```

---

## 📁 Dateien

| Datei | Zweck |
|-------|-------|
| `DESIGN.md` | Vollständiges Design System (vom `awesome-OpenSIN-design` Repo) |
| `preview.html` | Visuelle Vorschau aller Komponenten |
| `SKILL.md` | Dieser Skill (Enforcement + Quick Reference) |

---

## 🔗 Verknüpfte Repos

- **Design System:** `Delqhi/awesome-OpenSIN-design` (GitHub)
- **opensin.ai:** `OpenSIN-AI/website-opensin.ai`
- **my.opensin.ai:** `OpenSIN-AI/website-my.opensin.ai`
- **blog.opensin.ai:** Teil von `website-opensin.ai`

---

## ⚠️ Enforcement

Dieser Skill MUSS in AGENTS.md jedes OpenSIN-Frontend-Repos referenziert werden:

```markdown
## Design Enforcement

ALLE Frontend-Arbeit MUSS dem `awesome-opensin-design` Skill folgen.
Siehe: ~/.config/opencode/skills/awesome-opensin-design/SKILL.md
```

Wer ein OpenSIN-Frontend ohne dieses Design baut, verstößt gegen das Protokoll.
