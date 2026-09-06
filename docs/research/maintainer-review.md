# Maintainer-lens review

Internal structured review, 2026-09-06. No named maintainer participated or endorsed the result. Evidence is the actual source, executable checks, and linked authorities in the ledger. Review was performed locally, without delegated agents.

| Lesson | Review perspectives | Decision / evidence |
|---|---|---|
| 01 | Book, Cargo, learner | Distinguishes edition/compiler/package; no global toolchain change |
| 02 | Language, learner | Branch values and numeric overflow policy explicit; boundary assertions |
| 03 | Language, types, library, learner | Places/values, Copy, Clone, drop, leaks differentiated; E0382 |
| 04 | Borrow-checker, library, learner | Reborrow and last use explain access; capacity not permission; E0502 |
| 05 | Library, input-processing, learner | UTF-8 bytes/scalars/graphemes; Vec capacity not initialized length |
| 06 | Library API, learner | Enum data tied to variants; private-field tradeoff, no unnecessary typestate |
| 07 | Library author, application operator | Concrete errors preserve causes; malformed input not panic/retry |
| 08 | Pedagogy, application | Fixture-only panic/overflow assumptions labeled; stage acceptance contract |
| 09 | Types, API, learner | Annotations do not extend owner lifetime; static bound distinction; E0515 |
| 10 | Types, library, learner | Useful Write abstraction; static/dynamic dispatch and allocation distinguished |
| 11 | Library, learner | Item types and captures explained; collect<Result> failure policy explicit |
| 12 | Systems, library, QA | Limit checked before extension; partial UTF-8 assembly tested across buffer sizes |
| 13 | Cargo, publisher, application, CI | Current resolver 3, additive features, lock and dependency graph; CLI has no Tokio |
| 14 | Diagnostics, QA, learner | Actual JSON/rustc output; expected codes; Clippy not style authority |
| 15 | Operational semantics, library, learner | UnsafeCell not synchronization or competing exclusive access; runtime guards |
| 16 | Language, concurrency, learner | Send/Sync distinction; scoped join before use; no tiny-fixture speed claim |
| 17 | Concurrency, production operator | Closure/drain ordering; deadlock and advisory poisoning discussed |
| 18 | Memory model, library, systems | Relaxed counter only; joins supply completion; no payload publication claim |
| 19 | Language, runtime, learner | No-op waker only immediately ready; await not guaranteed yield; no rollback |
| 20 | Runtime, backend, learner | Bounded messages vs byte limits; detached handle and abort semantics; deterministic tests |
| 21 | Language, types, runtime | Pointee vs handle; no unchecked projection; static async trait vs dyn E0038 |
| 22 | Runtime, backend, learner | One aggregate owner; fixture shutdown limits identified; not mislabeled production server |
| 23 | Operational semantics, library, systems, learner | Five-part safety argument; bounds, ZST, empty, destructors; Miri separate from proof |
| 24 | Performance engineer, learner | Repeatable experiment instructions; black_box caveat; no fabricated speedup |
| 25 | Language/types/Cargo currency | Latest stable point fix, nightly solver rollout, discontinued goals corrected |
| 26 | Systems/FFI, library | Rust-defined C ABI labeled; no foreign-link claim; explicit pointer/unwind contract |
| 27 | Application, library, release | args_os, stderr/stdout/exit code, bounded input, complete-only results |
| 28 | Publisher, CI, learner | publish=false intentional; API + behavioral semver; freshness maintenance loop |

## Revisions made during review

- Replaced the homepage's illustrative incomplete functions with the actual compiled ownership example.
- Corrected two goals to historical/discontinued based on the August 31 update; added ownership-assertion work and completed Cargo lint work.
- Kept unstable allocator documentation's old AllocRef terminology out of recommendations; current Allocator docs used instead.
- Fixed Chrome search-field Escape handling to close the dialog explicitly; the test waits for the closed state.
- Retried Miri with two Cargo jobs after local process-resource exhaustion; this is host capacity, not an unsafe-code result.

## Scope of assurance

This is a substantive introductory-to-practical course, not an exhaustive Rust reference or independent external maintainer certification. Unsafe aliasing models and evolving features retain caveats. FFI demonstrates a Rust-defined C ABI only. The timing example makes no benchmark claim. Automated accessibility checks supplement visual/keyboard inspection and do not certify complete accessibility conformance.

Browser follow-up: axe found sidebar number opacity and the table-of-contents note below AA contrast. Removed the reduced opacity and darkened the note. A mobile overflow check fired during route transition; isolated inspection measured viewport/document/body at 390 px, with only deliberately scrollable code content extending inside its container. The browser contract now waits for layout to settle while still failing sustained overflow.
