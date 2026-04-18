# Inbound Intake — OpenSIN-Skills Operations Guide

## Overview

The **Inbound Intake** system normalizes incoming work for `OpenSIN-Skills` into a canonical `work_item` shape before issue creation and follow-up dispatch. This repo uses the same governance contract as the wider OpenSIN fleet while staying tailored to skill-library maintenance.

## Architecture

```text
[External Platform] → [Webhook/Poller] → [Normalize] → [Create GitHub Issue] → [PR Watcher / Hermes-ready handoff]
```

## Supported Source

- **GitHub repo events** via `platforms/registry.json`
- Future external sources must be added to the registry before activation

## Workflow: `inbound-intake`

### Trigger

Webhook `POST` to the n8n endpoint configured for `inbound-work`.

### Canonical Fields

```json
{
  "source": "github|telegram|manual|automation",
  "type": "bug|enhancement|docs|ops",
  "title": "Work item title",
  "description": "Detailed description",
  "priority": "low|medium|high|critical",
  "metadata": {}
}
```

### Steps

1. **Webhook** receives incoming payload.
2. **Normalize Work Item** maps the payload to the canonical schema.
3. **Create GitHub Issue** opens or updates the relevant issue in `OpenSIN-AI/OpenSIN-Skills`.
4. **PR Watcher** monitors resulting PR activity via `scripts/watch-pr-feedback.sh`.

## PR Watcher

Run the watcher manually:

```bash
bash scripts/watch-pr-feedback.sh
```

Optional cron example:

```bash
*/5 * * * * /path/to/OpenSIN-Skills/scripts/watch-pr-feedback.sh
```

## Validation

- `python3 - <<'PY' ...` JSON-parse governance files before merge
- `python3 scripts/catalog-generator.py . --output catalog.json --stats`
- `gh pr list --repo OpenSIN-AI/OpenSIN-Skills --state open --limit 20 --json number,title,updatedAt`

## File Map

| File | Path |
|------|------|
| Governance contract | `governance/repo-governance.json` |
| PR watcher contract | `governance/pr-watcher.json` |
| Platform registry | `platforms/registry.json` |
| n8n workflow | `n8n-workflows/inbound-intake.json` |
| PR watcher script | `scripts/watch-pr-feedback.sh` |

## Activation Checklist

1. Keep the governance files on the default branch.
2. Import `n8n-workflows/inbound-intake.json` into n8n if workflow automation is needed.
3. Provide `N8N_CI_WEBHOOK_URL` for the CI dispatch workflow.
4. Ensure `gh` authentication is available wherever `watch-pr-feedback.sh` runs.
