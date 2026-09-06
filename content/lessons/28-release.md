{"title":"Release, maintain, and keep learning","stage":5,"minutes":60,"summary":"Check compatibility, release a reproducible build, and keep the course up to date.","example":"13_cargo","headingIds":{"Make the release reproducible":"a-release-is-a-promise-others-can-reproduce","Review the public API":"review-the-public-rust-surface"}}
---
## Make the release reproducible

The course repository is independently buildable with Node 24 and Rust 1.98.1. The website and Rust application have separate build paths. The website is static HTML with local assets; the application is an ordinary Cargo workspace. Neither needs another course repository at runtime or build time.

Before releasing a change, run the documented checks from a clean checkout. Keep generated build artifacts out of the source commit unless they are intentional evidence such as compiler diagnostic snapshots. Review the lockfile diff when updating dependencies. A passing test suite does not excuse an unexplained dependency change.

{{example}}

## Review the public API

Other programs may rely on your public fields, trait bounds, enum variants, and error types. Removing an implementation or adding a required bound can break callers even when your own tests compile. Adding variants to an exhaustive public enum can be breaking. `#[non_exhaustive]` leaves room to add variants or fields later, but limits how callers construct or match values. Decide whether you need it before publishing.

Cargo's semver guidance and tools such as cargo-semver-checks help identify API changes. They do not prove behavioral compatibility, validate a file format, or establish that every performance expectation is preserved. Write release notes around observable effects, including changes to limits and failure behavior.

The course packages set `publish = false` because they are for local study. Publishing a general-purpose crate would require selecting an appropriate name, reviewing metadata and licensing, testing a packaged archive, and establishing a support policy. Learners can install the application with `cargo install --path`; it does not need a registry release.

## A practical maintenance loop

1. Inspect the current stable release and edition guidance.
2. Review source changes for concepts marked evolving.
3. Update the evidence ledger with dates and affected lessons.
4. Compile every runnable example and regenerate intentional failures.
5. Run tests, Clippy, formatting, and the isolated Miri lab.
6. Build the site, check links and metadata, and test keyboard/mobile behavior.
7. Deploy and verify the actual production domain, including deep links.

The ledger records sources and recommendations without claiming that named maintainers reviewed or endorsed the course. Their work informs review questions; our own examples and tests supply reproducible evidence.

## Exercise

Propose a change that would allow lowercase levels. Describe whether it is a parser behavior change, an API signature change, a file-format change, or several of these. Add tests for the intended mixed-case policy and explain how the release notes should describe it.

<details><summary>Solution and acceptance check</summary>

Accepting lowercase broadens the file grammar even if function signatures remain unchanged. Decide whether all case combinations are valid and whether messages remain untouched. Existing strict callers might rely on rejection, so consider compatibility in context. Release notes should state exactly which inputs now succeed and whether strict mode remains available.

</details>

## Where to go next

Choose a real problem: a network service, an embedded peripheral, a library used by another team, or a performance-sensitive tool. Learn what that problem requires. Study new language features as you need them. Revisit ownership, errors, synchronization, and invariants at each boundary. The goal is software whose behavior another developer can understand and maintain.

Sources: [semver compatibility](https://doc.rust-lang.org/cargo/reference/semver.html), [publishing](https://doc.rust-lang.org/cargo/reference/publishing.html), and [cargo-semver-checks](https://github.com/obi1kenobi/cargo-semver-checks).
