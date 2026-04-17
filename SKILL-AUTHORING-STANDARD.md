# OpenSIN Skill Authoring Standard v1.0

> Based on the Skill Authoring Standard by [Alireza Rezvani](https://github.com/alirezarezvani/claude-skills) (MIT License).
> Extended with 3 OpenSIN-native patterns for A2A integration, MCP tooling, and fleet dispatch.

## 13 Patterns for World-Class AI Agent Skills

### Pattern 1: Context-First Design
Every skill starts with YAML frontmatter defining identity, domain, triggers, and relationships.

```yaml
---
name: "skill-name"
description: "One-line description"
version: "1.0.0"
author: "OpenSIN-AI"
category: "domain"
source: "opensin-native | claude-skills"
upstream_author: "Alireza Rezvani"  # only for imported skills
status: "active | deprecated | placeholder-needs-content"
triggers:
  - "when user asks about X"
related_skills:
  - "related-skill-1"
---
```

### Pattern 2: Practitioner Voice
Write as an experienced practitioner. Use "You are an expert in..." opener.

### Pattern 3: Multi-Mode Workflows
Every skill supports: Build Mode + Optimize Mode (minimum). Optional: Review, Debug modes.

### Pattern 4: Related Skills Navigation
Reference 3-6 related skills. Creates navigable skill graph.

### Pattern 5: Reference Separation
Keep references in separate files. SKILL.md stays focused on workflows.

### Pattern 6: Proactive Triggers
Define 4-6 trigger phrases for automatic skill activation.

### Pattern 7: Output Artifacts
Table of artifacts the skill produces (format, description).

### Pattern 8: Quality Loop
Self-review checklist at the end of every skill execution.

### Pattern 9: Communication Standard
Headers, tables, code blocks, bullet points, bold for key terms.

### Pattern 10: Python Tools (stdlib-only)
All scripts use only Python stdlib. Support --help flag.

### Pattern 11: A2A Integration (OpenSIN)
Document which A2A agents the skill connects to, invocation method, I/O schemas.

### Pattern 12: MCP Tooling (OpenSIN)
Document MCP server name, tools, required config in .opencode/opencode.json.

### Pattern 13: Fleet Dispatch (OpenSIN)
Document GitHub Issue format, branch naming, dispatch payload, acceptance criteria.

---

## File Structure
```
skill-name/
  SKILL.md           # Main skill (<=10KB)
  references/        # Detailed reference docs
  scripts/           # Python CLI tools (stdlib-only)
  templates/         # Reusable templates
```

## Credits
Original 10-pattern standard by [Alireza Rezvani](https://github.com/alirezarezvani/claude-skills) (MIT).
Patterns 11-13 by OpenSIN-AI.
