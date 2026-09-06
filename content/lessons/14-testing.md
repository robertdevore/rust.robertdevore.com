{"title":"Tests, compiler errors, and verification tools","stage":2,"minutes":60,"summary":"Test expected behavior and failures, then use compiler checks and Clippy to catch more mistakes.","example":"14_testing","headingIds":{"Test what callers need":"test-the-promise-a-caller-relies-on"}}
---
## Test what callers need

A test that repeats the implementation can miss a mistake in what the function is supposed to do. Our reader promises to handle records split across arbitrary buffering boundaries. Testing many tiny buffer capacities challenges that promise directly. One test with a large input buffer would not check those splits.

{{example}}

Unit tests sit close to private implementation details. Integration tests exercise the public surface as a separate crate or process. Documentation tests make public examples executable. Use each kind of test to catch different mistakes.

## A useful verification sequence

```sh
cargo fmt --all -- --check
cargo check --workspace --all-targets --locked
cargo test --workspace --locked
cargo clippy --workspace --all-targets --locked -- -D warnings
npm run verify:rust
```

Formatting produces consistent layout. The compiler checks types, ownership constraints, and other static rules. Tests exercise selected behavior. Clippy identifies suspicious patterns and suggests improvements. You still need to review the requirements and rules those tools cannot check.

Clippy cannot decide whether your design fits the problem. The default useful lints are a starting point; enabling every restriction lint can create contradictory advice. If a suppression is needed, scope it narrowly and explain the non-obvious reason. This repository treats warnings as failures for its pinned validation toolchain, so compiler upgrades include an intentional lint review.

## Intentionally rejected programs

The drill runner invokes rustc on each small input, captures structured diagnostics, and checks that exactly the intended error code appears. It also stores rustc's actual rendered explanation. This catches an example that still fails but for the wrong reason. Absolute temporary paths are avoided by invoking the compiler from the repository root.

A diagnostic snapshot describes one compiler version. Wording may change while the language rule remains the same. Do not promise every learner's editor displays identical text. Ask them to compare the error code, source spans, and ownership relationship first.

## Exercise

Add a test for an error on the second record, then a test for an invalid UTF-8 final record. Make each fail by temporarily breaking the relevant behavior; restore the code afterward. Explain what observing a failure tells you about the test.

<details><summary>Solution and acceptance check</summary>

The second-line syntax failure must carry line 2. Invalid UTF-8 must produce the dedicated error, not replacement characters or a panic. A mutation that breaks the behavior should fail the corresponding test; otherwise the test may not actually inspect the claimed contract. Temporarily breaking the code helps you check that the test can catch the mistake it claims to cover.

</details>

Concurrency later adds schedule-sensitive behavior, and unsafe code adds obligations that ordinary tests cannot exhaust. Miri and deterministic async time tests complement this baseline. None proves all possible executions correct.

Sources: [Cargo test](https://doc.rust-lang.org/cargo/commands/cargo-test.html), [rustc JSON diagnostics](https://doc.rust-lang.org/rustc/json.html), and [Clippy usage](https://doc.rust-lang.org/stable/clippy/usage.html).
