{"title":"Cargo, modules, and dependency boundaries","stage":2,"minutes":55,"summary":"Understand packages, modules, features, and the dependencies your program builds.","example":"13_cargo","headingIds":{"Update dependencies with care":"lock-and-update-deliberately"}}
---
## Package, crate, module, workspace

A package has a manifest and may contain multiple targets. A crate is a compilation unit, such as a library or binary target. Modules organize names inside a crate; adding `mod parser` is not the same as adding a package dependency. A workspace coordinates packages, shares a lockfile and target directory, and can inherit selected metadata.

Our workspace has a lesson package, a core library, a CLI, and an unsafe lab. The CLI depends on the core through a path dependency. The core does not depend on the website, Tokio, or the examples. You can test and install the CLI without building the website.

{{example}}

## Resolver and feature decisions

The workspace explicitly selects resolver `3`, appropriate for this edition-2024 course. Virtual workspaces should declare their resolver because there may be no root package edition from which to infer one. The resolver considers compiler compatibility, but you still need to test on the oldest compiler you support.

Features should usually add capabilities. Dependency features are unified in relevant parts of the graph, so a feature that disables safety checks or removes functionality can surprise a downstream user when another dependency enables it. Test default features, no default features, and supported combinations when a library actually offers those configurations.

The lesson package enables only Tokio's runtime, macros, channels, time, and test utilities. The synchronous CLI has no Tokio dependency. `cargo tree -e features` shows why a feature is enabled; guessing from one manifest is insufficient when multiple dependency paths exist.

## Update dependencies with care

Commit the lockfile for this course and application. Run `cargo update` intentionally, inspect the diff and release notes, and rerun checks. `--locked` prevents an unnoticed re-resolution during verification. It does not make source registries permanently available or guarantee that dependencies have no vulnerabilities.

Build scripts and procedural macros execute on the build machine. Review the code and maintenance status of dependencies, including the dependencies they bring in. A small handwritten error enum is appropriate here; Serde becomes useful when a real structured format is introduced. Add a dependency when it solves a problem your project has.

## Exercise

Run `cargo metadata --no-deps --format-version 1` and identify the CLI's library dependency. Run `cargo tree -p audit-cli` and `cargo tree -p rust-course-examples -e features`. Explain why building the CLI need not bring Tokio into its binary.

<details><summary>Solution and acceptance check</summary>

The CLI graph contains the CLI and local core. Tokio belongs to the example package's graph. Packages in the same workspace do not automatically depend on each other. A shared lockfile may list packages a particular target does not use.

</details>

For release profiles, begin with Cargo defaults. Benchmark before adding LTO, reducing codegen units, or changing panic behavior. Build caching is an optimization; cache keys need to account for toolchains and dependencies, and correctness must not depend on a warm cache.

Sources: [workspaces](https://doc.rust-lang.org/cargo/reference/workspaces.html), [resolver](https://doc.rust-lang.org/cargo/reference/resolver.html), [features](https://doc.rust-lang.org/cargo/reference/features.html), and [profiles](https://doc.rust-lang.org/cargo/reference/profiles.html).
