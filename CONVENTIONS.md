# OpenSIN Coding Conventions

## Package Manager: Bun ONLY
- **bun install** / **bun run build** / **bunx** — NEVER npm/npx

## LLM Calls: opencode CLI ONLY
All agents call LLMs via `opencode run "prompt" --format json`

## Python Scripts: stdlib-only
Zero pip installs. Every script supports `--help`.

## Code Comments: EXTENSIVE
Every function, every step MUST be commented.

## Browser Automation: nodriver ONLY
BANNED: Playwright, Puppeteer, Selenium, Camoufox

## Vision Gate: MANDATORY
Screenshot + vision model check after EVERY browser action.

## Git: Conventional Commits
`feat:` / `fix:` / `docs:` / `refactor:` / `test:` / `chore:`

## Branding
Brand as OpenSIN/sincode. Credit upstream authors where applicable.
