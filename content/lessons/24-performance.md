{"title":"Measure performance and resource use","stage":4,"minutes":60,"summary":"Build a reproducible experiment before changing allocation, dispatch, or build profiles.","example":"23_performance"}
---
## A measurement starts with a question

Does parsing allocate? Does input reading dominate runtime? Does parallelism help on representative files? These are different questions requiring different evidence. “Rust is fast” does not answer any of them.

{{example}}

The example demonstrates timing and `black_box`, but its single number is not a benchmark conclusion. Startup, optimization, CPU frequency, background work, and tiny sample size can dominate. `black_box` is a best-effort optimization barrier useful in experiments, not a mathematical guarantee about generated code.

## Design the experiment

Run optimized builds when evaluating optimized production behavior. Record compiler version, target, profile, input distribution, hardware, and sample count. Compare equivalent outputs and error policies. Include empty input, typical records, long records near the limit, and malformed data if those occur in the workload.

Separate warm-up from samples where appropriate. Report a distribution rather than one favorable run. Change one significant variable at a time. If you claim lower memory use, measure it or prove a specific bound and state precisely which allocations the bound covers.

Our parser borrows message text rather than allocating a new string. That is visible in its interface and implementation. The reader keeps one bounded record vector, while the caller's buffering layer can have its own allocation. A borrowed design still pays for reading, validation, and counting; avoiding one allocation does not mean the whole program is zero-cost.

## Optimize the bottleneck

A profile may show that filesystem I/O dominates, in which case replacing an iterator with a loop is unlikely to matter. It may show formatting costs, in which case current standard-library APIs deserve review before adding a crate. Rust 1.98 introduced integer buffer formatting APIs, but our three-line-sized summary does not justify optimizing that path without evidence.

Monomorphization can improve inlining and also increase compile time or code size. Dynamic dispatch has indirection costs and can reduce duplication. `Arc::clone` updates an atomic count; `String::clone` copies text. Treat these as different operations. Use explicit ownership reasoning to remove accidental work before introducing low-level unsafe code.

## Exercise

Compare parsing borrowed records with a version that creates a new owned message for each record. Preserve outputs and error handling. Record at least several repeated optimized runs and explain which part of the measurement is noisy. Do not commit a machine-specific speed claim as a universal fact.

<details><summary>Solution and acceptance check</summary>

Keep input bytes and loop counts identical, consume results so they cannot trivially disappear, and record toolchain/profile. The owned version should demonstrate an additional allocation policy, but timing may vary. A useful conclusion states the tested workload and uncertainty. If the difference is below noise, report that rather than selecting the fastest run.

</details>

Sources: [`black_box`](https://doc.rust-lang.org/std/hint/fn.black_box.html), [Cargo profiles](https://doc.rust-lang.org/cargo/reference/profiles.html), and [Rust 1.98 release notes](https://blog.rust-lang.org/2026/08/20/Rust-1.98.0/).
