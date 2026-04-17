---
name: imagegen
description: "Use when the user asks to generate or edit images with Antigravity image generation and layered thumbnail composition (for example: ad creatives, hero images, product shots, concept art, covers, image edits, or batch variants). Prefer the Antigravity image plugin and the `generate-image` workflow."
---

> OpenCode mirror: sourced from `~/.config/opencode/skills/imagegen` and mirrored for OpenCode CLI usage.

# Skill-SIN-ImageGen

Generates or edits images for the current project (for example website assets, campaign creatives, product mockups, UI mockups, wireframes, logo explorations, photorealistic images, infographics). Uses Antigravity image generation and deterministic, reproducible layer composition.

Machine invocation compatibility stays `imagegen`, but the human-facing skill name is now `Skill-SIN-ImageGen`.

**CRITICAL RULE (AIometrics Enterprise Standard):**
ALL images generated using this skill MUST be ultra best-practice, enterprise CEO level. No childish, playful, or amateur illustrations. Every image (mindmaps, workflows, architecture diagrams, tech stacks) must be minimalist, clean, professional, and visually appealing to top-tier investors (e.g., OpenAI). 

**CRITICAL RULE (Hexagon Topology):**
Whenever A2A agents, workflows, or structures are requested, they MUST be visualized as interconnected hexagons, similar to a structural node graph.

14. Save/return final outputs and note the final prompt + flags used.

## Temp and output conventions
- Use `tmp/imagegen/` for intermediate files; delete when done.
- Write final artifacts under `output/imagegen/` when working in this repo.
- Use `generate_image` with `output_path` / `file_name` to control output paths; keep filenames stable and descriptive.

## Dependencies (install if missing)
Prefer the OpenCode Antigravity plugins:
- `opencode-antigravity-auth`
- `opencode-antigravity-image`

If the plugin is missing, install it in `~/.config/opencode/opencode.json` and re-run OpenCode.

## Environment
- Antigravity image generation uses Google OAuth via the auth plugin.
- Do not ask for or persist direct Gemini API keys.
- If the plugin is missing, tell the user which plugin is missing and how to install it locally.

- ## Defaults & rules
- Use the Antigravity image plugin unless the user explicitly asks for a different provider order.
- Assume the user wants a new image unless they explicitly ask for an edit.
- Prefer the `generate-image` command over writing one-off runners.
- Use `opencode auth login` and the plugin's quota/health commands when you need a fast env/status check before live runs.
- Keep `scripts/image_gen.py` as legacy OpenAI-only tooling; do not use it unless the user explicitly requests OpenAI.
- For edits, stay on the Antigravity image tool first. If a fallback is needed, keep it explicit and local.
- If a provider fails or is not configured, stop and report the missing plugin or credential rather than silently switching providers.
- If the result isn’t clearly relevant or doesn’t satisfy constraints, iterate with small targeted prompt changes; only ask a question if a missing detail blocks success.

## Prompt augmentation
Reformat user prompts into a structured, production-oriented spec. Only make implicit details explicit; do not invent new requirements.

**AIOMETRICS CEO-LEVEL AUGMENTATION RULES:**
- All prompts must include strong stylistic constraints: "ultra minimalist, clean corporate style, dark-mode friendly, high-end enterprise tech, sharp lines, CEO-level presentation, professional data visualization, vector art style, abstract geometric shapes, no clutter, highly polished."
- FORBIDDEN concepts: "no childish drawings, no messy sketches, no playful cartoons, no messy backgrounds, no amateur layouts."
- A2A Agent Constraints: Whenever an A2A agent, workflow, or architectural diagram is requested, explicitly include "interconnected 3D hexagons, overlapping rings, technical nodes, deep blue and purple hues, tech node graph, centralized orchestration structure".

## Use-case taxonomy (exact slugs)
Classify each request into one of these buckets and keep the slug consistent across prompts and references.

Generate:
- photorealistic-natural — candid/editorial lifestyle scenes with real texture and natural lighting.
- product-mockup — product/packaging shots, catalog imagery, merch concepts.
- ui-mockup — app/web interface mockups that look shippable.
- infographic-diagram — diagrams/infographics with structured layout and text.
- logo-brand — logo/mark exploration, vector-friendly.
- illustration-story — comics, children’s book art, narrative scenes.
- stylized-concept — style-driven concept art, 3D/stylized renders.
- historical-scene — period-accurate/world-knowledge scenes.

Edit:
- text-localization — translate/replace in-image text, preserve layout.
- identity-preserve — try-on, person-in-scene; lock face/body/pose.
- precise-object-edit — remove/replace a specific element (incl. interior swaps).
- lighting-weather — time-of-day/season/atmosphere changes only.
- background-extraction — transparent background / clean cutout.
- style-transfer — apply reference style while changing subject/scene.
- compositing — multi-image insert/merge with matched lighting/perspective.
- sketch-to-render — drawing/line art to photoreal render.

Quick clarification (augmentation vs invention):
- If the user says “a hero image for a landing page”, you may add *layout/composition constraints* that are implied by that use (e.g., “generous negative space on the right for headline text”).
- Do not introduce new creative elements the user didn’t ask for (e.g., adding a mascot, changing the subject, inventing brand names/logos).

Template (include only relevant lines):
```
Use case: <taxonomy slug>
Asset type: <where the asset will be used>
Primary request: <user's main prompt>
Scene/background: <environment>
Subject: <main subject>
Style/medium: <photo/illustration/3D/etc>
Composition/framing: <wide/close/top-down; placement>
Lighting/mood: <lighting + mood>
Color palette: <palette notes>
Materials/textures: <surface details>
Quality: <low/medium/high/auto>
Input fidelity (edits): <low/high>
Text (verbatim): "<exact text>"
Constraints: <must keep/must avoid>
Avoid: <negative constraints>
```

Augmentation rules:
- Keep it short; add only details the user already implied or provided elsewhere.
- Always classify the request into a taxonomy slug above and tailor constraints/composition/quality to that bucket. Use the slug to find the matching example in `references/sample-prompts.md`.
- If the user gives a broad request (e.g., "Generate images for this website"), use judgment to propose tasteful, context-appropriate assets and map each to a taxonomy slug.
- For edits, explicitly list invariants ("change only X; keep Y unchanged").
- If any critical detail is missing and blocks success, ask a question; otherwise proceed.

## Examples

### Generation example (hero image)
```
Use case: stylized-concept
Asset type: landing page hero
Primary request: a minimal hero image of a ceramic coffee mug
Style/medium: clean product photography
Composition/framing: centered product, generous negative space on the right
Lighting/mood: soft studio lighting
Constraints: no logos, no text, no watermark
```

### Edit example (invariants)
```
Use case: precise-object-edit
Asset type: product photo background replacement
Primary request: replace the background with a warm sunset gradient
Constraints: change only the background; keep the product and its edges unchanged; no text; no watermark
```

## Prompting best practices (short list)
- Structure prompt as scene -> subject -> details -> constraints.
- Include intended use (ad, UI mock, infographic) to set the mode and polish level.
- Use camera/composition language for photorealism.
- Quote exact text and specify typography + placement.
- For tricky words, spell them letter-by-letter and require verbatim rendering.
- For multi-image inputs, reference images by index and describe how to combine them.
- For edits, repeat invariants every iteration to reduce drift.
- Iterate with single-change follow-ups.
- For latency-sensitive runs, prefer the Flash fallback or Imagen Fast only after the primary Gemini Pro pass is unavailable or clearly too slow for the task.
- If results feel “tacky”, add a brief “Avoid:” line (stock-photo vibe; cheesy lens flare; oversaturated neon; harsh bloom; oversharpening; clutter) and specify restraint (“editorial”, “premium”, “subtle”).

More principles: `references/prompting.md`. Copy/paste specs: `references/sample-prompts.md`.

## Guidance by asset type
Asset-type templates (website assets, game assets, wireframes, logo) are consolidated in `references/sample-prompts.md`.

## CLI + environment notes
- CLI commands + examples: `references/cli.md`
- API parameter quick reference: `references/image-api.md`
- If network approvals / sandbox settings are getting in the way: `references/codex-network.md`

## Reference map
- **`references/cli.md`**: how to *run* image generation/edits/batches via the Antigravity image plugin and `generate-image` command.
- **`references/image-api.md`**: current plugin requirements, tool arguments, and environment expectations.
- **`references/prompting.md`**: prompting principles (structure, constraints/invariants, iteration patterns).
- **`references/sample-prompts.md`**: copy/paste prompt recipes (generate + edit workflows; examples only).
- **`references/codex-network.md`**: environment/sandbox/network-approval troubleshooting.
