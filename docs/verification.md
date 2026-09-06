# Release verification · 2026-09-06

Baseline: Rust 1.98.1, edition 2024. Source pin and compiler snapshots are committed. The Rust site is independent from adjacent projects.

## Passed

- cargo fmt --all -- --check
- cargo check --workspace --all-targets --locked
- cargo test --workspace --locked: 6 core tests, 2 async lifecycle tests, 4 unsafe tests, 1 documentation test
- cargo clippy --workspace --all-targets --locked -- -D warnings
- All 25 runnable examples executed successfully
- Six intentionally failing compiler drills verified for their intended error codes and actual rendered diagnostics
- Ten CLI contract scenarios (valid stdin/file, empty input, errors, UTF-8, bounds, arguments)
- cargo test --release --workspace --locked
- cargo install --locked --path crates/audit-cli --root target/install-check; installed executable processed stdin successfully
- Miri on nightly-2026-09-05: four isolated unsafe-lab tests passed locally and on GitHub's Linux runner
- 32 public static pages plus 404, 28 lesson contracts, 1,308 local links/anchors and production metadata
- 93 external lesson-source links resolved successfully
- GitHub CI on the contrast-corrected source: Rust, Miri, build, static checks, full browser suite passed (see ci-verification.json)
- Production DNS/TLS, certificate validation, HTTP→HTTPS, all 32 routes, CSS/JS/social/favicon/search assets, sitemap, robots, canonical/OG URLs, trailing slash and real 404 checks (see production-verification.json)

Browser checks include desktop routes, every mobile lesson, search, persisted progress with reload/undo, compiler disclosure, deep refresh, mobile navigation, console/request failures, and selected axe WCAG A/AA checks. Screenshots were visually inspected for the homepage and a mobile lesson. Local Playwright's browser download timed out; installed Chrome was used through the documented BROWSER_CHANNEL fallback. CI installed its matched Chromium successfully.

An initial axe failure for sidebar/TOC contrast was fixed and CI passed afterward. Chrome search Escape required explicit dialog closing. A transient mobile layout measurement was changed to an eventual assertion that still rejects sustained overflow. Initial Miri setup hit local process limits; two build jobs resolved that setup failure. No application soundness failure was observed.

## Production browser gate — passed

The complete suite passed against `https://rust.robertdevore.com` after matching the Python course’s inherited Cloudflare analytics setup. All 32 desktop routes, 28 mobile lessons, search, persisted progress, compiler disclosure, deep refresh, menus, and selected axe checks passed with no console errors or unexpected failed requests (see browser-verification.json).

The owner explicitly requested traffic tracking like python.robertdevore.com. Both sites load Cloudflare Web Analytics and Zaraz/Google Analytics. The Rust CSP now permits the Cloudflare beacon plus the two observed Google connection origins. The About page discloses the analytics. No disable rule or unrelated Cloudflare setting was changed. Separate fresh-browser verification observed the Zaraz and beacon scripts returning 200, Google collection returning 204/200, and Rust’s `/cdn-cgi/rum` returning 204 (see analytics-verification.json). Dashboard aggregation was not inspected.

The route sweep records `net::ERR_ABORTED` separately only for the two known background Google analytics endpoints, because rapid navigation cancels them. Console errors, CSP failures, application asset failures, and all other network failures still fail the suite. Waiting for global network idle was inappropriate: the Google audience request can remain open after its successful 200 response. The dedicated analytics checks prove successful delivery independently of navigation cancellation.

This resolves the earlier production blocker. The initial suggestion to disable analytics was superseded by the owner’s explicit preference to preserve it. Reference: [Cloudflare CSP requirements](https://developers.cloudflare.com/fundamentals/reference/policies-compliances/content-security-policies/).

## Deployment

Cloudflare Workers Static Assets, Worker `rust-course`, custom domain `rust.robertdevore.com`, production version `d03191ec-ef09-49ef-a7d3-c6b62a0e6fbc`. Wrangler manages the attached custom domain; no manual duplicate DNS record was created. Production has no application Worker handler or dynamic backend. Local OAuth deployment is operational. The optional manual GitHub deployment workflow requires scoped repository secrets if the maintainer elects to use it.

## Limits

Tests and Miri are evidence, not a proof of all behavior. Automated accessibility checks cover selected rules and pages; the layout and keyboard checks supplement them. The FFI example does not link an external C library. The timing example is not a performance benchmark claim. Feature statuses are accurate to the stated freshness point, not a promise they remain unchanged.

## SiteKit visual update · 2026-09-06

Vendored Kujo SiteKit 1.0.0 from upstream commit c0d199e06bc926e29de87b7cd983ee3d54db9cda; all distribution manifest checksums match. Departure Mono is self-hosted and verified loaded in production, with body/control/code font families using the SiteKit font token. Removed the header symbol and themed all scroll containers, including dark code panels, through standard and WebKit scrollbar rules. Native forced-colors behavior remains available.

Build/static checks passed. Full local and public desktop/mobile browser suites passed, including selected axe checks and no console errors or unexpected failed requests. Desktop homepage and mobile lesson screenshots were visually reviewed. Computed production code-scrollbar colors are thumb rgb(184,121,92), track rgb(38,41,35). Public DNS/TLS/routes/assets/metadata verification passed.

## Reading typography correction · 2026-09-06

User revised the all-mono preference: Inter now covers paragraphs/general reading text; Departure Mono remains for headings, navigation, labels, controls, and code. Inter 400/700 is self-hosted with its OFL license. Build/static checks and the full local browser suite passed. Production computed-font inspection confirms Inter on prose and Departure Mono on h1/h2/code; the lesson was visually reviewed. Public DNS/TLS/routes/assets/metadata checks passed.
