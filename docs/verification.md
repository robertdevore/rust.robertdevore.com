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

## Production browser gate — pending

The full browser suite passes in CI against the built application. Running it against the public hostname exposed Cloudflare Zaraz scripts inherited from the parent zone. Their third-party tracking requests violate the application’s intentional `connect-src` policy and cause console errors. Production HTTP checks above pass, but the public browser console gate is not yet satisfied.

The narrow remediation is a Cloudflare Configuration Rule matching only `http.host eq "rust.robertdevore.com"`, with `disable_zaraz: true` and `disable_rum: true`. No other hostname or security setting should change. The connected API rejected creation with authentication error 10000; local browser control is unavailable. After the rule is applied, rerun `BASE_URL=https://rust.robertdevore.com BROWSER_CHANNEL=chrome npm run test:browser` and production verification, then replace this pending status with the result. See [Cloudflare settings documentation](https://developers.cloudflare.com/rules/configuration-rules/settings/).

## Deployment

Cloudflare Workers Static Assets, Worker `rust-course`, custom domain `rust.robertdevore.com`, production version `5d294a51-f88a-4386-a603-55c57c394203`. Wrangler manages the attached custom domain; no manual duplicate DNS record was created. Production has no application Worker handler or dynamic backend. Local OAuth deployment is operational. The optional manual GitHub deployment workflow requires scoped repository secrets if the maintainer elects to use it.

## Limits

Tests and Miri are evidence, not a proof of all behavior. Automated accessibility checks cover selected rules and pages; the layout and keyboard checks supplement them. The FFI example does not link an external C library. The timing example is not a performance benchmark claim. Feature statuses are accurate to the stated freshness point, not a promise they remain unchanged.
