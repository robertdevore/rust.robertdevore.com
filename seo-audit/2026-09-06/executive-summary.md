# SEO and AI-search audit · 2026-09-06

**PASS WITH RECOMMENDATIONS.** All 32 canonical pages audited and updated, including all 28 lessons. Baseline and after evidence are preserved. P0/P1 findings: 0/0 before and after.

The baseline already had unique titles/descriptions, canonical URLs, coherent navigation, accessible server-rendered lessons and no broken links. It lacked structured entity markup, explicit author metadata, complete downloadable lesson text, permanent slash aliases and source-verified showcase artifacts.

Implemented factual schema and visible breadcrumbs/bylines, 28 complete Markdown exports with canonical headers and hash index, minified/versioned assets, permanent redirects and deterministic Howl source cards. Typography, SiteKit, scrollbars and analytics are preserved. All canonical routes remain indexable; duplicate Markdown downloads use noindex and canonical Link headers.

After crawl: 32 canonical / 32 indexable pages; 32 pages with parseable schema; 0 broken internal links; 0 broken external destinations; 0 orphans. Browser, production, discovery and Howl checks passed; full receipts and limitations are linked by filename in this folder. Internal heuristic health scores omitted; measured Lighthouse results are in before-after.md and performance.csv.

Production still carries CDN-script performance cost, and default Python clients are blocked by the edge on tested content/export routes (EDGE-01); named crawler probes and browser clients succeed. Search ranks, AI citations, field CWV and analytics totals: NOT AVAILABLE — DATA ACCESS REQUIRED. These are measurement limitations, not claims of zero visibility. Technical readiness does not guarantee ranking or citation. The optional nested www alias remains unavailable; canonical hostname is healthy.

Start with data-availability.md and the 7/28/60/90-day plan in recommendations.md. See issues.csv for root causes/status, changes.md for implementation files and before-after.md for actual comparisons.
