{"title":"Stable Rust and work in progress","stage":4,"minutes":60,"summary":"Tell stable features apart from nightly experiments and plans that may change.","example":"24_const","drill":"const_trait","headingIds":{"The version this course uses":"a-freshness-point-not-a-prediction"}}
---
## The version this course uses

This course was verified on **2026-09-06** against **Rust 1.98.1**, edition **2024**. The September point release fixes a vtable-generation miscompilation in 1.98.0, so the course pins the corrected version. The compiler version matters when you reproduce the examples and diagnostics.

A feature can have both a stable subset and an active extension. The following table classifies the specific claim being made. A project goal means work is planned. It does not guarantee a stable release or a date you can rely on.

| Area | Today | On the horizon / status |
| --- | --- | --- |
| Async functions in traits | Static-dispatch use is STABLE | Native async dyn dispatch is an ACTIVE PROJECT GOAL; our direct-dyn drill still fails |
| Pin | Safe pinning APIs are STABLE | Field projections and broader pin/reborrow ergonomics are ACTIVE PROJECT GOALS with EXPERIMENTAL work |
| Borrow checking | Stable checks remain the course baseline | Polonius alpha is NIGHTLY work and an ACTIVE PROJECT GOAL; do not assume all lending patterns work on stable |
| Trait solver | Stable compilation is the contract used here | Global next-solver rollout is NIGHTLY; the August 21 announcement is not stable rollout |
| Const generics | Array lengths parameterized by integers are STABLE | Full const generics and const trait capabilities are evolving; const trait implementation support is NIGHTLY |
| Reference counting | Explicit `Rc::clone` and `Arc::clone` are STABLE | Reborrow and smart-pointer ergonomics are ACTIVE PROJECT GOALS |
| Allocation | `GlobalAlloc` and normal collections are STABLE | The general allocator API remains NIGHTLY; Allocators 1.0 is an ACTIVE PROJECT GOAL |
| Unsafe fields | Private fields plus documented invariants are the stable idiom | `unsafe_fields` is NIGHTLY; it does not replace a safety argument |
| Safety contracts | Written invariants and checked unsafe boundaries remain required | Primitive ownership assertions are an ACTIVE PROJECT GOAL, not a stable verification guarantee |
| Formal specification | Reference contracts guide production work | a-mir-formality and executable specification work are EXPERIMENTAL / ACTIVE PROJECT GOALS |
| C/C++ interop | Explicit ABI boundaries and maintained bindings are usable today | Seamless interop and problem-space mapping are ACTIVE PROJECT GOALS |
| Standard-library rebuilding | Normal prebuilt std targets are the baseline | Cargo `-Z build-std` is NIGHTLY |
| Build speed | Stable Cargo profiles and incremental builds are available | Fast Builds is an ACTIVE PROJECT GOAL roadmap; measure local changes |
| Semver tooling | Cargo's compatibility guidance applies today | cargo-semver-checks is ecosystem tooling, not a compiler proof of all compatibility |

{{example}}

This small array example uses stable const generics, which do not let arbitrary trait methods run at compile time.

{{drill}}

The August program update also records two discontinued efforts: the specific **Experimental language specification** goal and **Continue Experimentation with Pin Ergonomics**. Treat those goal labels as HISTORICAL / SUPERSEDED, not active promises. Field-projection work and the newer end-to-end executable specification goal continue on their own terms. Cargo’s linting-system goal is reported complete; this course uses current manifest lints and Clippy rather than describing that completed goal as future work. See the [July–August program update](https://blog.rust-lang.org/inside-rust/2026/08/31/program-management-2026-jul-aug/) and [ownership-contract goal](https://github.com/rust-lang/goals/issues/734).

## How to update an explanation

First reproduce behavior on the exact stable compiler. Then read the Reference, stabilization record, and relevant goal or tracking issue. If the compiler rejects a safe pattern because its analysis is conservative, describe the currently supported expression and the limitation. Distinguish a limit in the compiler's analysis from a rule of the language.

Work on an easier alternative does not make an existing feature deprecated. Historical descriptions need dates. Proposed designs can change or fail to ship. The core exercises avoid nightly language features; only the optional unsafe verification toolchain uses nightly for Miri.

## Exercise

Choose one row, follow its official source, and identify what evidence would justify changing its status to STABLE. Record the compiler release and stabilization reference rather than editing the label based on a social post.

<details><summary>Solution and acceptance check</summary>

A stable release note or merged stabilization record plus a successful minimal stable probe is strong evidence. A goal marked accepted, a nightly demo, or a merged RFC alone is insufficient. Preserve the older verification date in the research history and rerun affected compiler drills.

</details>

Sources: [release fix](https://blog.rust-lang.org/2026/09/03/Rust-1.98.1/), [2026 goals](https://goals.rust-lang.org/2026/goals.html), [Polonius](https://goals.rust-lang.org/2026/polonius.html), [next-solver rollout](https://blog.rust-lang.org/2026/08/21/enabling-next-solver-on-nightly/), [unstable Cargo](https://doc.rust-lang.org/cargo/reference/unstable.html), [unsafe fields](https://doc.rust-lang.org/unstable-book/language-features/unsafe-fields.html), [const traits](https://doc.rust-lang.org/unstable-book/language-features/const-trait-impl.html), and [allocator API](https://doc.rust-lang.org/std/alloc/trait.Allocator.html).
