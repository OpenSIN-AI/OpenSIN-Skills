---
name: "thumbnail-optimizer"
description: "This skill is kept only for backward compatibility."
version: "1.0.0"
author: "OpenSIN-AI"
category: "media"
source: "opensin-native"
status: "active"
triggers:
  - "use thumbnail-optimizer"
related_skills: []
---

# /thumbnail-optimizer (deprecated)

This skill is kept only for backward compatibility.
Use `/gen-thumbnail` instead.

`/gen-thumbnail` now contains the full thumbnail pipeline, the brand bootstrap, the A/B preview generator, and the CTR learning loop.

If you still need the record-keeping command, use:
`node ~/.config/opencode/skills/gen-thumbnail/scripts/track_ctr.js <Winner_A_or_B> <Winner_CTR> <Loser_CTR>`


## Related Skills
- See [Skill Catalog](../../README.md) for related skills
