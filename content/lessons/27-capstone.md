{"title":"Capstone: ship Fieldnotes","stage":5,"minutes":150,"summary":"Combine the parser and reader into a command-line tool you can install and use.","source":"crates/audit-cli/src/main.rs","headingIds":{"Check your finished tool":"review-rubric"}}
---
## Product brief

Fieldnotes is the course's completed event-audit tool, packaged as `audit-cli`. It accepts exactly one path argument, with `-` meaning standard input. When it succeeds, it prints one summary line to stdout in a fixed order. Errors go to stderr and produce a nonzero exit code. No partial summary is printed when input is invalid.

The format is one `LEVEL message` record per line. Levels are exactly INFO, WARN, and ERROR. Messages must contain non-whitespace text. Input must be UTF-8. LF, CRLF, and an unterminated final record are supported. Each record may contain at most 4096 bytes including its newline if present. Counts use checked `u64` arithmetic.

## Build and install

```sh
cargo build --release --locked -p audit-cli
cargo install --locked --path crates/audit-cli
printf 'INFO ready\nWARN retry\nERROR stopped\n' | audit-cli -
```

Expected stdout is `INFO=1 WARN=1 ERROR=1`, followed by a newline. For a file, replace `-` with its path. The executable name is `audit-cli`; Fieldnotes is the product name used in this course. `cargo install` places the executable in Cargo's binary directory, which must be on your PATH.

{{source}}

## Why main stays small

Argument parsing uses `args_os`, allowing platform-native paths rather than assuming every filename is Unicode. Opening the file and choosing stdin belong in the CLI. Reading, syntax, record limits, and counts belong in the library. Printing only after the full input succeeds prevents partial counts from appearing as a complete result.

Output writing can fail, including a downstream pipe closing. The program returns a failure in that case. Stderr writing during error reporting is best-effort because another failure cannot be reported indefinitely. Handle these failures even when reading and parsing succeeded.

## Acceptance suite

Run `npm run verify:rust`. It checks the workspace, runs examples and compiler drills, and exercises the CLI with valid stdin, empty input, malformed input, invalid UTF-8, an oversized record, a missing path, and a real file. The library tests independently cover chunk boundaries and count overflow. Run `cargo test --release --workspace --locked` when changing arithmetic or profile settings.

## Your extension

Add `--allow-errors` only after specifying its output contract. Decide how rejected rows are counted, whether oversized input can be skipped without unbounded storage, and how an I/O failure differs from a malformed row. Test each of those cases as well as the new argument.

<details><summary>Reference design and acceptance check</summary>

Represent completeness in the result type rather than silently discarding failures. Keep strict mode's behavior unchanged. A lenient mode should report both accepted and rejected counts and still fail on unreadable input. Discarding an oversized record requires scanning to a terminator while keeping storage bounded. Document whether a rejected final unterminated record is counted.

</details>

## Check your finished tool

Your tool should count correctly, limit its record buffer, report failures clearly, and build with the pinned toolchain. It should not need unsafe code. You should be able to trace each borrow to its owner and each allocation to a reason. Performance claims need measurements. A clean compile is necessary but does not establish every product requirement.

Sources: [`args_os`](https://doc.rust-lang.org/std/env/fn.args_os.html), [Cargo install](https://doc.rust-lang.org/cargo/commands/cargo-install.html), and [`ExitCode`](https://doc.rust-lang.org/std/process/struct.ExitCode.html).
