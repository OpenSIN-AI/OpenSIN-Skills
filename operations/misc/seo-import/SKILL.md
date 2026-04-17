---
name: "seo-import"
description: "**Ultimate Workflow for Maximum Reach (SEO, GEO & AEO)**"
version: "1.0.0"
author: "OpenSIN-AI"
category: "misc"
source: "opensin-native"
status: "active"
triggers:
  - "use seo-import"
related_skills: []
---

# SKILL: /seo-import

**Ultimate Workflow for Maximum Reach (SEO, GEO & AEO)**

## OVERVIEW

This skill defines the absolute mandatory standard for **Search Engine Optimization (SEO)**, **Generative Engine Optimization (GEO)**, and **Answer Engine Optimization (AEO)** across all OpenSIN web projects. 

No agent is permitted to manually write scattered meta tags, generic robots.txt files, or basic sitemaps anymore. **EVERY new website or major update MUST use the automated Auto-Injector from `Delqhi/seo-import`.** This ensures maximum visibility in Google, ChatGPT, Perplexity, and Claude.

## TRIGGERS

- "Optimize website for search engines"
- "Add SEO"
- "Generate sitemap and robots.txt"
- "Add llms.txt"
- "Add JSON-LD or structured data"
- "Run /seo-import"

## MANDATES (STRICT RULES)

1. **NO MANUAL SEO SETUP:** You must use the `seo-import` Auto-Injector CLI. Do not manually copy/paste meta tags or create `.txt` files from scratch unless augmenting the injected baseline.
2. **JSON-LD IS MANDATORY:** Every page MUST use structured data. At a minimum: `WebSite`, `Organization`, `FAQPage`, `Article`/`TechArticle`, and `SoftwareApplication` (if applicable).
3. **AI CRAWLERS MUST BE ALLOWED:** `robots.txt` must explicitly allow `GPTBot`, `ClaudeBot`, `PerplexityBot`, etc.
4. **CORS FOR LLMS:** Cloudflare `_headers` must allow `Access-Control-Allow-Origin: *` for `/llms.txt`, `/llms-full.txt`, and `/.well-known/*`.
5. **SEMANTIC HTML ONLY:** Stop using `<div>` for everything. Use `<main>`, `<article>`, `<section>`, `<nav>`, `<header>`, `<footer>`. AI scrapers rely on semantic tags.

## WORKFLOW: THE AUTO-INJECTION PROCESS

When asked to optimize a repository for SEO/GEO/AEO, execute the following steps exactly:

### Step 1: Prepare the Toolkit
Check if `/Users/jeremy/dev/seo-import` exists. If not, clone it:
\`\`\`bash
cd /Users/jeremy/dev && git clone https://github.com/Delqhi/seo-import.git
\`\`\`

### Step 2: Run the Auto-Injector
Run the CLI injector against the target project directory:
\`\`\`bash
node /Users/jeremy/dev/seo-import/cli.js inject /path/to/target-project
\`\`\`

This will automatically:
- Create `public/_headers`, `public/_redirects`, `public/robots.txt`, and `public/.well-known/security.txt`.
- Copy React/Vue SEO components into `src/components/seo/`.
- Copy the build scripts `build-llms-txt.mjs` and `generate-sitemap.mjs` into `scripts/seo/`.
- Update `package.json` to inject the `seo:sitemap` and `seo:llms` commands into the build pipeline.

### Step 3: Update `package.json` Domain
Open the target project's `package.json` and replace `YOUR_DOMAIN_HERE` in the newly injected `seo:sitemap` and `seo:llms` scripts with the actual production domain (e.g., `https://my.opensin.ai`).

### Step 4: Implement the SEO Components in Code
Open the main layout (e.g., `App.tsx` or `index.html`) and individual page components.
Import and use the injected `<SeoHead />` and `<StructuredData />` components.

**Example Implementation (React):**
\`\`\`tsx
import { SeoHead, StructuredData } from './components/seo/SeoHelpers';

const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'What is OpenSIN?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'OpenSIN is an open-source AI agent platform.'
      }
    }
  ]
};

export default function MyPage() {
  return (
    <>
      <SeoHead 
        title="My Page | OpenSIN" 
        description="The ultimate guide to AI agents." 
        canonicalUrl="https://opensin.ai/my-page"
      />
      <StructuredData data={jsonLd} />
      <main>
        {/* Page Content */}
      </main>
    </>
  );
}
\`\`\`

### Step 5: Verify the Build Pipeline
Run the project's build command (e.g., `npm run build` or `bun run build`).
Verify that the `dist/` or `out/` folder now contains:
- `sitemap.xml`
- `llms.txt`
- `llms-full.txt`
- `_headers`
- `_redirects`
- `robots.txt`

If they are missing, ensure the build tool (like Vite) copies files from `public/` to `dist/`, or adjust the build script accordingly.

## TROUBLESHOOTING

- **Vite isn't copying `llms.txt` to `dist/` during build?** 
  Vite copies the `public/` directory *before* the post-build scripts run. If `llms.txt` is generated *after* Vite builds, it will end up in `public/` but not `dist/`. Modify the `package.json` script to output directly to `./dist` instead of `./public` for `build-llms-txt.mjs` and `generate-sitemap.mjs`, or add a copy step.
- **JSON-LD isn't showing up?** 
  Ensure the `<StructuredData />` component is mounted and that the `data` prop receives a valid JavaScript object (not a string).


## Related Skills
- See [Skill Catalog](../../README.md) for related skills
