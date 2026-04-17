---
name: check-my-dev-in-web
description: Fast web-app verification workflow for local dev, preview deployments, and static builds without heavy browser automation. Prioritizes cheap checks first: diagnostics, build, HTTP smoke, asset verification, webhint, and Lighthouse. Escalate to a real browser only when cheaper signals cannot explain the failure.
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: fast-web-verification
  trigger: web-dev-check
---

# Check My Dev In Web

> Cheap signals first. Heavy browser last.

Use this skill when a user wants to know whether a web app, preview deployment, or local build is actually healthy **without** wasting time on full browser automation too early.

This skill is designed for cases like:
- blank page after deploy
- broken assets or routes
- local preview sanity checks
- "is my dev build actually working?"
- pre-PR web validation

It is **not** the right tool for:
- anti-bot bypass work
- authenticated E2E business flows
- click-every-button UX audits across a huge app
- stealth browsing or CAPTCHA-heavy automation

In those cases use a browser-heavy skill only after this fast lane is exhausted.

---

## Best-Practice Principles

These are the core practices this skill follows:

1. **Build the exact artifact you ship**
   - Validate production build output, not only the dev server.
   - Source: Lighthouse CI / Halodoc guidance emphasizes isolated build validation before merge.

2. **Prefer deterministic HTTP and static checks first**
   - Fetch HTML.
   - Verify referenced JS/CSS/image assets return `200`.
   - Check critical routes and SPA rewrites.
   - Source: webhint local-server workflow and general static-host debugging practice.

3. **Use local-server audits before full browser automation**
   - Run `webhint` against a local server for standards, broken links, headers, manifest, viewport, and related web issues.
   - Source: webhint docs.

4. **Use Lighthouse as a gated quality check, not as your first debugger**
   - Lighthouse is great for best-practices / performance / accessibility / SEO once the app actually boots.
   - Source: Lighthouse CI / Halodoc / Unlighthouse guidance.

5. **Escalate to a real browser only when cheap signals cannot explain the failure**
   - Example: HTML and assets all return `200`, but runtime render is still blank.
   - Then inspect runtime JS errors.

---

## Validation Ladder

Always execute in this order.

### Phase 0 — Repo and runtime basics

1. Inspect project state:

```bash
git status
git diff --stat
```

2. Detect the stack:

```bash
test -f package.json && node -e "const p=require('./package.json'); console.log(JSON.stringify({name:p.name,scripts:p.scripts},null,2))"
```

3. Prefer language-server diagnostics before running anything expensive:

- Use `lsp_diagnostics` on the project root or relevant source directory.

### Phase 1 — Static quality gates

Run the cheapest project-native checks that exist.

Typical order:

```bash
npm run lint
npm run typecheck
npm run build
```

Rules:
- If a script does not exist, skip it.
- Do **not** invent replacement scripts.
- If `build` fails, stop here and fix the build before any browser work.

### Phase 2 — Local HTTP smoke

Serve the built output or preview server and verify plain HTTP behavior.

For static `dist/`:

```bash
python3 -m http.server 4173 --directory dist
```

For framework preview:

```bash
npm run preview -- --host 127.0.0.1 --port 4173
```

Then run the smoke script:

```bash
python3 "$HOME/.config/opencode/skills/check-my-dev-in-web/scripts/check_my_dev_in_web.py" \
  --url http://127.0.0.1:4173 \
  --route / \
  --route /about
```

What this proves:
- HTML is reachable
- referenced JS/CSS assets are reachable
- route responses are not tiny error pages
- the preview host is actually serving what the HTML references

### Phase 3 — Standards and hinting (`webhint`)

If the project is publicly reachable locally and Node is available:

```bash
npx hint http://127.0.0.1:4173
```

Use this when you need fast checks for:
- broken links
- missing viewport / manifest / metadata
- header issues
- basic accessibility and best-practices hints

webhint is ideal here because it is **faster and more structured** than jumping straight into a full browser-debug session.

### Phase 4 — Lighthouse / LHCI

Once the page actually boots, use Lighthouse for scored audits.

For static output:

```bash
npx @lhci/cli autorun --collect.staticDistDir=./dist
```

For a running local server:

```bash
npx @lhci/cli autorun --collect.url=http://127.0.0.1:4173/
```

Recommended assertions:
- accessibility >= 0.90
- best-practices >= 0.90
- SEO >= 0.90
- performance threshold depends on app type; do not overfit marketing-site budgets onto dashboards

### Phase 5 — Browser escalation (last resort)

Only escalate when **all** of the following are true:
- HTML is reachable
- assets return `200`
- build is green
- yet the app still renders blank or obviously broken

Then inspect runtime errors with the cheapest viable browser/devtools path.

Do **not** start here.

---

## Fast Decision Rules

### If the issue is a blank page

Use this order:
1. Build succeeds?
2. HTML returns `200`?
3. Referenced JS/CSS assets return `200`?
4. Route fallback works for SPA paths?
5. If yes to all and still blank → inspect runtime JS exception.

### If the issue is broken routing

Use this order:
1. Fetch the domain with `curl -I` and `curl -L`
2. Confirm the HTML title / canonical / app shell belong to the expected project
3. Confirm asset hostnames match the expected deployment
4. Confirm DNS / host binding / deployment target is the intended project
5. Only then inspect router code or rewrite rules

### If the issue is "works locally, broken after deploy"

Prefer:
1. production build
2. local static server from built output
3. asset + route smoke
4. Lighthouse against the built artifact
5. only then compare to live deployment

---

## Anti-Patterns

Never do these first:

- open a heavyweight browser automation session just to see whether `/assets/*.js` returns `200`
- click around manually before verifying build output and route rewrites
- run Lighthouse before the app can even mount
- debug routing before checking whether the domain is bound to the wrong deployment
- assume a runtime crash is a network issue without checking the JS exception

---

## Minimal Command Pack

These commands cover most cases fast.

### 1. Build

```bash
npm run build
```

### 2. Serve built output

```bash
python3 -m http.server 4173 --directory dist
```

### 3. Smoke-check HTML + assets + routes

```bash
python3 "$HOME/.config/opencode/skills/check-my-dev-in-web/scripts/check_my_dev_in_web.py" \
  --url http://127.0.0.1:4173 \
  --route / \
  --route /pricing \
  --route /docs
```

### 4. webhint

```bash
npx hint http://127.0.0.1:4173
```

### 5. Lighthouse

```bash
npx @lhci/cli autorun --collect.url=http://127.0.0.1:4173/
```

---

## Output Format

When using this skill, report results in this structure:

```md
## check-my-dev-in-web result

### Phase 1 — Build
- PASS/FAIL
- command:
- key output:

### Phase 2 — HTTP smoke
- PASS/WARN/FAIL
- HTML status:
- assets checked:
- broken assets:
- routes checked:

### Phase 3 — webhint
- PASS/WARN/FAIL
- top findings:

### Phase 4 — Lighthouse
- PASS/WARN/FAIL
- performance:
- accessibility:
- best-practices:
- seo:

### Escalation
- was browser debugging needed?
- if yes, why cheaper checks were insufficient

### Verdict
- READY / NOT READY / NEEDS FIXES
```

---

## References

- webhint local-server integration: https://webhint.io/docs/user-guide/development-flow-integration/local-server/
- Lighthouse CI GitHub Actions guide: https://unlighthouse.dev/learn-lighthouse/lighthouse-ci/github-actions
- Halodoc: automated Lighthouse checks in CI/CD: https://blogs.halodoc.io/automating-web-performance-testing-ci-cd-lighthouse/
