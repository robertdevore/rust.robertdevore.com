{"title":"Values, functions, and control flow","stage":1,"minutes":45,"summary":"Write functions, choose between cases, and handle numbers that reach their limits.","example":"02_values","headingIds":{"Write your first function":"start-with-a-question-the-program-answers"}}
---
## Write your first function

Our first question is whether a request took less than 100 milliseconds. A function gives that rule a name. `milliseconds: u32` names a parameter and its unsigned 32-bit integer type. `-> &'static str` says the result is a reference to text stored for the duration of the program; here both answers are string literals. We will unpack references later.

{{example}}

`if` produces a value, so both branches must agree on its type. The final expression in the function has no semicolon: its value is returned. Add a semicolon and the block instead evaluates to `()`, the unit value, unless an explicit return supplies the function result. This is a common first compiler error.

`let samples = [12, 100, 340]` creates an array. A `for` loop visits its values. Formatting captures `value` by name; `{}` receives the following expression. `assert_eq!` checks a fact and panics if it is false. These assertions check that the example does what we expect.

## Bindings and changes

A binding is immutable unless declared `mut`. Use `mut` when you intend to change the binding. Shadowing with another `let` creates a new binding; it can have a different type. Mutation updates an existing place and preserves its type. Neither operation is an ownership workaround: moving a non-`Copy` value still matters, as the next lesson shows.

Booleans are `true` and `false`; conditions do not treat arbitrary integers as booleans. Use `&&`, `||`, and `!` to combine predicates. A range `0..3` excludes 3; `0..=3` includes it. A `match` chooses among patterns and must cover every possible input, either explicitly or with a fallback. Prefer it when several distinct cases deserve separate handling.

## Choose a numeric policy

An integer type has a finite range. Do not write a production counter assuming overflow can never happen. Ordinary arithmetic can panic when overflow checks are enabled, while unchecked release arithmetic generally wraps. Select `checked_add` for an explicit failure, `saturating_add` for a deliberate upper bound, or `wrapping_add` for modular arithmetic. Choose the behavior your program needs. A passing debug build does not settle that choice.

`usize` is useful for indexing and sizes in memory; its width depends on the target. It is not automatically the right type for a portable file format. Floating-point values cannot represent many real numbers exactly. If you use them, decide how to handle equality, rounding during sums, infinity, and NaN. Our capstone uses integer counts.

## Exercise

Change the classifier to return `fast` below 100, `acceptable` from 100 through 499, and `slow` at 500 or above. Add assertions for 99, 100, 499, and 500. Then deliberately put a semicolon after the final `if` expression and read the error before removing it.

<details><summary>Solution and acceptance check</summary>

Use `if milliseconds < 100 { "fast" } else if milliseconds < 500 { "acceptable" } else { "slow" }`. The four tests exercise both sides of each boundary. The return annotation demands text; the extra semicolon produces unit. Fix the value-producing expression, not the return type, because the function's job is to classify.

</details>

See [primitive numeric types](https://doc.rust-lang.org/std/primitive.u32.html), [control flow](https://doc.rust-lang.org/book/ch03-05-control-flow.html), and [statements and expressions](https://doc.rust-lang.org/reference/statements-and-expressions.html).
