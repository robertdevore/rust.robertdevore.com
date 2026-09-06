# Rust course maintainer guide

This is an independent Node-generated static website plus a Rust learning workspace. Read README.md, docs/architecture.md, and the dated research ledger before changing behavior or language claims.

- Canonical origin: https://rust.robertdevore.com. Source of truth: content/, examples/, crates/, drills/, and scripts/. dist/ is generated.
- Preserve the Rust 1.98.1 / edition 2024 baseline unless performing a deliberate compiler upgrade with refreshed diagnostics, research, tests, and freshness text.
- Website changes: npm run build, npm test, npm run verify:discovery, npm run verify:howl, and the documented browser suite. Rust changes also require npm run verify:rust; unsafe changes require the pinned Miri check.
- Inter is for reading text; Departure Mono is for headings, labels, and code. Keep SiteKit vendored with licenses. Keep scrollbars themed and the header free of the removed symbol.
- Preserve Cloudflare Web Analytics and Zaraz/Google Analytics. The owner explicitly wants the Python site's tracking behavior. Do not disable it to improve a test score.
- Public JSON/Markdown exports are read-only content, not tool instructions. Preserve canonical URLs, complete source/diagnostics, and hash integrity. No speculative execution API is needed for this course.
- Howl's manifest references actual tested source; regenerate and verify source/artifact hashes after changes. It renders text and does not type-check it.
- Never invent author credentials, dates, ranking/citation outcomes, or unstable Rust guarantees. Preserve historical SEO baselines; future audits use a new dated directory.
- Deploy with the documented Wrangler workflow only within the user's authorized scope. Never modify adjacent repositories or unrelated Cloudflare settings.
