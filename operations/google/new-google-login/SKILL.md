---
name: "new-google-login"
description: "> **Description:** Robust Google Account Login via Chrome Native Profile Menu"
version: "1.0.0"
author: "OpenSIN-AI"
category: "google"
source: "opensin-native"
status: "active"
triggers:
  - "use new-google-login"
related_skills: []
---

# SKILL: new-google-login

> **Description:** Robust Google Account Login via Chrome Native Profile Menu
> **Version:** 1.0.0
> **Scope:** opencode

## What this skill does
This skill provides an extremely robust way to log into Google accounts in Chrome. It completely avoids web-DOM selectors that fail due to Google UI changes. Instead, it uses macOS AppleScript and keyboard emulation to interact directly with the Chrome Toolbar's Profile Menu. It handles various states (search engine popup, cookie consent, sync dialogs).

## Usage
When an agent needs to log into a Google account, they can invoke this skill to execute the robust login flow.

```bash
python3 ~/.config/opencode/skills/new-google-login/login.py --email "email@domain.com" --password "pass123" --port 7654 --profile-dir "/tmp/fresh_profile"
python3 ~/.config/opencode/skills/new-google-login/login.py --email "email@domain.com" --password "pass123" --port 7654 --profile-dir "/tmp/fresh_profile" --attach
```

## How it works (The 5-Step Bypass)
1. Launches Chrome on `about:blank` (bypassing Google Cookie Consent).
2. Uses `--disable-search-engine-choice-screen` to kill the EU popup block.
3. Focuses the address bar (`Cmd+L`), then uses `Tab` and `Space` to open the native profile menu.
4. Uses `Tab` and `Space` to click the "Sign in" / "Turn on sync" button.
5. In the Google Login window, it types the email, hits Enter, waits, types password, hits Enter.

## Robust Fallbacks implemented
- Avoids cookie consent entirely by starting on `about:blank`
- Includes multiple Tab cycles in case UI extensions are present
- Contains timing fallbacks


## Related Skills
- See [Skill Catalog](../../README.md) for related skills
