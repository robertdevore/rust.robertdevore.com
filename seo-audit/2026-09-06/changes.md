# Implemented changes

- scripts/seo.mjs and build.mjs: truthful Person/WebSite/WebPage/Course/LearningResource/BreadcrumbList graphs, author metadata, visible author/breadcrumb context, canonical text exports, JSON index and full text. No fabricated dates/credentials/reviews.
- scripts/build.mjs, package.json/lock: esbuild 0.28.1, minified content-hashed CSS/JS, immutable asset cache headers, explicit permanent URL aliases, canonical/noindex headers for duplicate Markdown.
- howl.json, scripts/howl.mjs, showcase/: Howl 1.1.0 actual-source manifest and deterministic render/hash verification. scripts/social.mjs and assets/social.png derive the social card from Howl. Practice card has alt text, dimensions and lazy loading.
- content/about.md and assets/site.css: factual author/export explanations and compact lesson source row. Inter body, Departure Mono headings/code, SiteKit licensing, themed scrollbars and symbol-free header preserved.
- scripts/test-discovery.mjs, scripts/verify-production.mjs, CI, README and AGENTS.md: source/diagnostic completeness and hashes, schema relationships, production Markdown headers, drift gates, maintainer contracts.

No DNS/WAF/training crawler/analytics changes. No Rust curriculum rewrite. Howl does not compile Rust: its source remains covered by the Rust workspace verification.
