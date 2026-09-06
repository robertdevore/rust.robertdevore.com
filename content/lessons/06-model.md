{"title":"Structs, enums, and useful states","stage":1,"minutes":45,"summary":"Make domain distinctions visible without building an elaborate type architecture.","example":"06_model"}
---
## Model the alternatives you actually have

A struct groups fields that exist together. An enum chooses one of several variants. If a job is either queued, running with an attempt number, or finished with a byte count, an enum associates each piece of data with the state that needs it.

{{example}}

This avoids independent booleans such as `is_running` and `is_finished` that allow contradictory combinations. `match` asks you to consider every variant. Adding a new variant then reveals the places that need a decision. A catch-all arm can be appropriate, but using one everywhere gives up some of that useful compiler feedback.

Pattern matching a borrowed enum lets you inspect it without taking its owned fields. Match ergonomics can insert reference bindings; inspect inferred types before adding `.clone()` to a pattern-related error. Use `if let` when only one alternative matters and the others genuinely require no action.

## Keep invariants close to construction

Methods in an `impl` block operate on the type. A constructor named `new` is a convention, not a special language feature. `&self` borrows the receiver; `&mut self` borrows it exclusively; `self` consumes it. Choose based on the operation. Finishing a builder can consume it; reading a count should not.

Private fields let a constructor validate inputs and keep later code from bypassing checks. Public fields are a promise that callers can construct and change values directly. For a simple data transfer record that may be fine. For a value whose validity matters, use a private representation with intentional methods.

Derived traits such as `Debug`, `PartialEq`, and `Eq` are useful for inspection and tests. `Debug` is not a stable wire format. Changing a debug representation should not corrupt a persisted file because the file should use a deliberately specified encoding.

## Restraint is part of design

Do not invent a generic state-machine framework for three local variants. Typestate can make illegal operations unavailable at compile time, but it also creates more types and can complicate heterogeneous collections. Begin with an enum unless the extra static guarantees solve a demonstrated problem.

Our event parser uses `Level` and `Event<'a>`. `Level` has three variants; the event pairs a level with borrowed text. The parser validates spelling. The summary exposes named counts because callers need to inspect a plain result, not participate in a complex protocol.

## Exercise

Add a `Failed { reason: String }` variant. Update the description without cloning the reason. Then consider whether a public `attempt: u32` can represent an invalid zero attempt for your application.

<details><summary>Solution and acceptance check</summary>

Match `Job::Failed { reason }` through `&Job` and format a message using the borrowed reason. Add an assertion that includes the reason. If attempts start at one, use a validated constructor or a nonzero integer type; if zero means “not attempted”, document it. Types should express a real rule rather than an assumed one.

</details>

Sources: [enums and matching](https://doc.rust-lang.org/book/ch06-00-enums.html), [visibility](https://doc.rust-lang.org/reference/visibility-and-privacy.html), and [API guidelines](https://rust-lang.github.io/api-guidelines/).
