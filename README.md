# Rust Course

A free, independent course at **https://rust.robertdevore.com**: 28 lessons, 25 runnable examples, six compiler drills, three stage builds, and Fieldnotes, an installable event-audit CLI.

Technical freshness: **2026-09-06 · Rust 1.98.1 · edition 2024**. Read the [evidence ledger](docs/research/ledger.md), [reference cohort](docs/research/cohort.md), and [architecture](docs/architecture.md).

## Website

Use Node 24 or newer:

```sh
npm ci
npm run build
npm test
npm run dev
```

Wrangler prints the local address. Edit `content/lessons/`, rerun the build, and refresh. Generated HTML goes into `dist/`. There is no Python/Kujo runtime dependency and no external service required to build.

## Rust application and examples

Rustup reads the pinned toolchain automatically:

```sh
cargo run --locked --example 03_ownership
npm run verify:rust
cargo install --locked --path crates/audit-cli
printf 'INFO ready\nWARN retry\n' | audit-cli -
```

Output: `INFO=1 WARN=1 ERROR=0`. Alternatively pass a file path. Records are UTF-8, begin with INFO/WARN/ERROR and a space, and contain a nonblank message. The 4096-byte per-record limit includes a newline when present. Errors produce no partial summary, explain the line/category on stderr, and exit nonzero. See lesson 27 for the full contract.

## Browser and unsafe verification

```sh
npx playwright install chromium
# In another terminal, after building:
npx wrangler dev --port 4173
npm run test:browser
# Optional installed Chrome fallback:
BROWSER_CHANNEL=chrome npm run test:browser
rustup toolchain install nightly-2026-09-05 --profile minimal --component miri
cargo +nightly-2026-09-05 miri test -p unsafe-lab
```

The browser test checks every lesson on desktop/mobile plus search, progress, deep refresh, menus, assets, console errors, and selected WCAG axe checks. Screenshots and machine reports are written to ignored `work/qa/`. Regenerate `assets/social.png` with `node scripts/social.mjs` (same optional browser variable).

To review a compiler upgrade, change the pin deliberately, run `node scripts/drills.mjs --update`, inspect each diagnostic diff, update the ledger and freshness text, then rerun the full suite. Never update snapshots merely to hide an unrelated compiler error.

## Deploy

```sh
npx wrangler login
npm run deploy
SITE_URL=https://rust.robertdevore.com npm run test:browser
node scripts/verify-production.mjs
```

`wrangler.jsonc` configures Workers Static Assets and the sole custom domain. Initial deployment is authorized to attach that domain; do not overwrite an existing conflicting record without inspecting ownership. Local deployment uses Wrangler OAuth. Optional manual GitHub deployment requires repository secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`; never put credentials in source. The regular CI runs verification on pushes and PRs independently of deployment credentials.

MIT licensed original code and course prose. Independent project by Robert DeVore; no Rust Project or named-maintainer endorsement is claimed.

## Discovery and reproducible showcase assets

The generator emits factual Schema.org entities and breadcrumbs, source-complete Markdown at `/lessons/<slug>.md`, a versioned `/course-index.json` with content hashes, and `/llms-full.txt`. Canonical HTML remains authoritative. These exports support offline readers and retrieval tools; they are not special ranking requirements and do not expose an execution API.

```sh
npm run verify:discovery
npm run verify:howl
# Install Howl 1.1.0 and Kujo separately, then regenerate when source changes:
HOWL_BIN=howl npm run render:howl
BROWSER_CHANNEL=chrome node scripts/social.mjs
npm run build
```

`howl.json` references the actual Rust example. `showcase/` contains reviewed deterministic SVG, Markdown, HTML, and a local gallery; the build publishes selected downloadable cards only. Howl does not compile Rust. Rust checks remain in `verify:rust`. CI detects source/artifact drift without requiring Kujo for ordinary website builds. CSS/JS are minified and content-hashed for immutable caching; the vendored SiteKit source remains unchanged.

The dated SEO audit in `seo-audit/2026-09-06/` includes the sealed baseline, production receipts, before/after data, and a future measurement plan. No ranking or AI-citation improvement is claimed without platform data.

The homepage uses the approved launch artwork at `assets/rust-course-launch.png` for Open Graph and X, with its actual 1536×1024 dimensions. Other pages use the Howl card. Lesson `headingIds` preserve existing section links when headings are edited. Apply the Orwell writing skill to prose while preserving technical meaning and examples.
