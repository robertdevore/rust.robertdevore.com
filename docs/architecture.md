# Architecture and content contract

The existing Python site was inspected as a read-only reference for staged learning, a documentation sidebar, search, and previous/next navigation. This new repository shares no code, build artifact, or runtime dependency with it. Naming follows the adjacent domain-named repositories. Visual design uses a warm paper background, rust-colored accents, a compact terminal panel, and responsive documentation layouts.

## Static site

A small Node SSG renders Markdown with markdown-it and highlights tested Rust source with highlight.js. This content-only site needs no server framework, database, client router, or hydration. The build emits directory-index HTML for every route. The site works without JavaScript except for search, progress, copy buttons, and the mobile lesson drawer; the curriculum remains reachable through the footer/source links and homepage with JS off.

Lesson metadata is one JSON line followed by a `---` separator and Markdown. Required fields are title, stage, minutes, summary. An example/source/drill pointer embeds actual repository files at build time. Every exercise has acceptance criteria and a disclosed solution. `docs/curriculum.json` is a generated inventory; edit lessons, then rebuild it. The build must fail on a missing source or unexpanded include.

Search content is a local JSON index; results use DOM textContent. Progress stores only lesson slugs locally. No analytics, external fonts, or account service. The social card is a reproducible typographic PNG rendered by Playwright, not a borrowed image.

## Rust workspace

- Root package: runnable examples and deterministic async tests; Tokio is confined here.
- audit-core: parser and bounded BufRead summarizer; std only, unsafe forbidden.
- audit-cli: arguments/files/stdin/output; depends only on audit-core, unsafe forbidden.
- unsafe-lab: study-only checked slice partition; never linked into the application.

Stages are immutable reference programs rather than sequentially mutating one codebase. Learners create a branch/scratch target for exercises. Reference solutions and tests remain available for comparison.

## Deployment decision

Workers Static Assets supports this directory-index SSG directly, with custom domains, asset headers, and real 404 handling. No Worker script is needed. Current official documentation, rather than the older skill-reference Pages decision tree, guided this choice. `wrangler.jsonc` forces trailing-slash HTML routes, serves a proper 404 page, disables workers.dev previews, and binds only rust.robertdevore.com. All production metadata uses that hostname.

Deploy from the documented local CLI with existing OAuth, or configure the optional GitHub workflow's scoped Cloudflare secrets. Neither secrets nor a local credential file are committed. No unrelated DNS or Worker changes are required. Cloudflare manages the DNS/certificate through the Worker custom-domain flow.
