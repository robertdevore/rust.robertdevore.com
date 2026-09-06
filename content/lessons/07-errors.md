{"title":"Errors as part of the interface","stage":1,"minutes":50,"summary":"Distinguish malformed input, missing values, broken assumptions, and operational failure.","example":"07_errors"}
---
## Four different situations

A parser can successfully find no optional value, reject malformed input, fail to read its source, or encounter an internal programming bug. Those are different outcomes. `Option<T>` represents a value or absence. `Result<T, E>` represents success or an error with information. A panic is appropriate for some violated programmer assumptions, not as the default response to a bad line in a user file.

{{example}}

The `?` operator returns early on error, converting it through the relevant `From` implementation when the surrounding result uses a different error type. On success it extracts the value. It does not log, retry, or decide whether the operation should be attempted again.

## Give callers useful distinctions

The parser defines `MissingSeparator`, `UnknownLevel`, and `EmptyMessage`. A caller can match those variants without parsing an English sentence. `Display` provides a human-facing description. `std::error::Error` connects nested causes: the final reader error includes a line number and keeps the parser error as its source.

A concrete error enum often fits a reusable library. A boxed error can be convenient at an application boundary where the main job is reporting and exiting. `thiserror` can derive repetitive error implementations, while application-oriented libraries can add context. Neither changes the need to choose which failures are meaningful. Our capstone implements its small error types directly to keep that choice visible and its core dependency-free.

Avoid returning only “operation failed”. Useful context includes which operation failed and, where appropriate, which record. Do not echo secret input or entire untrusted records into logs. A line number and error category are sufficient for our tool.

## Failure should have a defined effect

The capstone returns no partial summary on the first invalid record. That is a product decision: users should not mistake partial counts for complete counts. An alternative “skip bad records” mode would need explicit counts of rejected rows, documentation, and tests. Silently ignoring errors changes the meaning of the result.

`unwrap` and `expect` are reasonable in tests when failure must fail the test. In application paths, justify why the error is impossible or handle it. An `expect` message describes the violated invariant; it should not pretend an operational failure cannot occur. File creation, network reads, and output writes can fail after earlier work has succeeded.

## Exercise

Run the example with an empty message, an unknown level, and a missing separator. Inspect the actual `ParseError` variants. Add a test asserting each variant. Explain why a retry will not fix malformed record syntax.

<details><summary>Solution and acceptance check</summary>

`WARN ` yields `EmptyMessage`, `DEBUG x` yields `UnknownLevel`, and `WARN` yields `MissingSeparator`. Retrying the same bytes leaves the syntax unchanged. A read interruption may merit a different policy, but that is an I/O decision. Keep parser tests independent from filesystem behavior so failure categories stay clear.

</details>

Sources: [`Result`](https://doc.rust-lang.org/std/result/), [`Error`](https://doc.rust-lang.org/std/error/trait.Error.html), and [thiserror's maintainer documentation](https://github.com/dtolnay/thiserror).
