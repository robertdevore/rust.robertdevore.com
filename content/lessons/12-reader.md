{"title":"Stage build: a bounded streaming library","stage":2,"minutes":90,"summary":"Separate parsing from I/O and enforce memory limits before input grows.","example":"12_stage_two"}
---
## Build brief

Turn the first counter into a reusable library. It must accept any `BufRead`, preserve structured errors, and retain at most 4096 bytes for an unfinished record. Empty input succeeds. LF and CRLF records are accepted. A final record without a newline is accepted. The first malformed record aborts the operation and no partial summary is returned.

{{example}}

The example calls the completed library with an in-memory cursor. Read `crates/audit-core/src/lib.rs` alongside this lesson; it is the complete reference, not pseudocode.

## Why the reader and parser are separate

`parse(&str)` handles syntax and returns a borrowed `Event`. `summarize(impl BufRead)` owns the reading policy and attaches a line number to parser failures. The parser does not know about files; the reader does not need to own a path. Tests can choose tiny buffer capacities to simulate fragmented input without relying on a real filesystem.

The reader calls `fill_buf` to inspect available bytes, finds the first newline if any, checks whether adding those bytes exceeds the record limit, copies the allowed portion, then calls `consume`. It must stop using the borrowed reader buffer before the next mutable reader operation. This is borrowing in service of a concrete resource boundary.

## Limit before accumulation

Calling `read_line` into a `String` and checking its length afterward can already have allocated excessive memory. Our loop checks `end > MAX_LINE_BYTES - bytes.len()` before extending. The invariant is that `bytes.len()` never exceeds the limit, making the subtraction safe. The input reader may have its own buffer; the guarantee concerns the library's retained record storage, not all memory used by an arbitrary `BufRead` implementation.

UTF-8 can cross buffer boundaries. Decode only after a complete record or final EOF is accumulated. Reject invalid UTF-8 with a line number. The limit includes a newline when present, so the boundary is explicit and testable rather than a vague “roughly 4 KB”.

## Exercise

Implement a simpler version first, then test reader capacities from 1 through 16. Include `INFO café\n`, a final unterminated record, a record exactly at the limit, and one byte beyond it. Inject an I/O failure. Ensure none of those errors produce a successful partial summary.

<details><summary>Solution and acceptance check</summary>

Use `BufReader::with_capacity` over a `Cursor` to force boundary splits. The UTF-8 input must parse regardless of where the two-byte character crosses a read. An exactly 4096-byte record is accepted; 4097 bytes are rejected before extension. A custom failing `Read` wrapped in `BufReader` preserves an `AuditError::Io`. The library's tests provide executable reference cases.

</details>

## Review the API

The generic reader is justified because files, stdin, and test buffers all provide the same capability. The message borrow avoids allocation during parsing. Errors distinguish syntax from I/O. Three counters avoid a dynamic map. No trait framework, async runtime, or shared mutex is necessary for this stage.

Sources: [`BufRead`](https://doc.rust-lang.org/std/io/trait.BufRead.html), [`Cursor`](https://doc.rust-lang.org/std/io/struct.Cursor.html), and [`from_utf8`](https://doc.rust-lang.org/std/str/fn.from_utf8.html).
