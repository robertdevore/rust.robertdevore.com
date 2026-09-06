# Methodology

Audit executed 2026-09-06 against the repository, generated dist, and the public Cloudflare custom domain. Baseline captured before edits; after inventory uses the identical sitemap URL set. Tools are committed alongside receipts.

Full source HTML crawl: 32 canonical pages (home, curriculum, practice, about, 28 lessons), every anchor and local fragment, unique external HTTP destinations, headings, descriptions, authors, canonicals, schema, graph depth and images. Live HTML/status fetched for each canonical page, with public DNS/TLS/redirect/404 and supplemental Markdown hash verification separately. Metadata/content columns describe generated HTML; live responses are retained independently in compressed JSON. This avoids representing source markup as observed production markup. Browser suite renders all 32 desktop routes and 28 mobile lessons, checks interactions and axe accessibility.

robots, sitemap, home and ownership lesson probed with nine crawler user agents. Spoofed UAs test edge responses from one client, not verified bot IPs, crawl frequency, indexing, or policy guarantees. Existing permissive robots policy and owner-requested analytics are unchanged. Missing nested www hostname is recorded, not treated as a required advertised route.

Lighthouse 13.4.1 / Chrome 152, default mobile simulation, one run per home/lesson before and after; exploratory lab measurements, no field INP claim. Resource summary transfer bytes differ from filesystem totals. Public CDN scripts remain enabled. No rank/citation attribution is inferred from performance.

Structured data is parsed and checked against factual content with semantic relationship assertions; this is not Google Rich Results Test certification. Course Info rich-result display is retired. Breadcrumb markup may be eligible subject to Google requirements; no appearance is guaranteed. Static JSON-LD does not require an execution API. llms.txt and Markdown exports improve portability, not a promised search-engine protocol.

Direct first-party competitors reviewed: learningrust.org ownership lesson and rust-exercises.com/100-exercises. Both emphasize practice; this course already offers executable examples, failing diagnostics and a CLI capstone. Avoid unsupported claims of superiority. Two exploratory web searches provide discovery observations only; controlled search/AI benchmarks require the access described in data-availability.md.

Severity: P0 outage/index removal; P1 widespread broken canonical/crawl/content behavior; P2 meaningful quality or measurement gap; P3 optional enrichment. Resolved means code and public behavior verified. Recommendations requiring platform access are not silently treated as completed.
