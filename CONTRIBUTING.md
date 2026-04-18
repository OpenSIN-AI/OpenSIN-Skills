# Contributing to OpenSIN-Skills

## Adding a New Skill

1. Choose the right directory:
   - Knowledge/expertise skills: `engineering/`, `product-team/`, etc.
   - Operational/action skills: `operations/<category>/`

2. Create your skill folder with a `SKILL.md`:
   ```
   your-skill-name/
     SKILL.md           # Main skill file (<=10KB)
     references/         # Optional reference docs
     scripts/            # Optional Python tools (stdlib-only)
     templates/          # Optional templates
   ```

3. Follow the [Skill Authoring Standard](SKILL-AUTHORING-STANDARD.md)

4. Required YAML frontmatter:
   ```yaml
   ---
   name: "your-skill-name"
   description: "One-line description"
   version: "1.0.0"
   author: "Your Name"
   category: "domain"
   source: "community"
   status: "active"
   triggers:
     - "when to use this skill"
   related_skills:
     - "related-skill-name"
   ---
   ```

5. Validate your skill:
    ```bash
    python3 scripts/validate-skill.py your-skill-name/SKILL.md

    # For new canonical OpenSIN skills, also enforce strict metadata
    python3 scripts/validate-skill.py your-skill-name/SKILL.md --strict
    ```

6. Submit a PR with:
   - Clear title: `feat(domain): add skill-name`
   - Description of what the skill does
   - Example usage

## Code Standards
- See [CONVENTIONS.md](CONVENTIONS.md)
- Python: stdlib-only, support --help
- Package manager: bun (never npm)
- Comments: extensive, explain WHY not just WHAT

## License
All contributions are under the MIT License.
