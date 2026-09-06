{"title":"Borrowing and reborrowing","stage":1,"minutes":55,"summary":"Reason about permitted access over time instead of treating references as spare owners.","example":"04_borrowing","drill":"alias"}
---
## Access has a duration

A reference gives access to another value without taking ownership of that value. `&T` provides shared access; `&mut T` provides exclusive access subject to reborrowing. These are access disciplines, not merely a distinction between methods that happen to mutate and methods that happen to read.

When a shared reference remains usable, mutation of the referenced ordinary data must not invalidate what it observes. When an exclusive reference grants access, conflicting access through independent paths is restricted. Later lessons refine this with interior mutability and unsafe aliasing rules; “exactly one pointer exists” is not the model.

{{example}}

The last use of `view` occurs before `append`. The compiler therefore permits the mutation without waiting for the closing brace of `main`. This is the practical effect of non-lexical lifetime analysis: borrow requirements follow uses and control flow, not simply the textual scope of a variable.

The second call passes `&mut *exclusive`. It temporarily **reborrows** through the exclusive reference. During that smaller borrow, the original reference cannot be used for conflicting access. After the call, the original reference becomes usable again. Function calls commonly insert reborrows implicitly; writing one explicitly helps you see the relationship.

## Why a push can invalidate a reference

A vector or string may need a larger allocation when it grows. A reference into its old allocation could then point at freed storage. But the access rules do more than prevent reallocation: even a mutation that fits in existing capacity may conflict with a live shared borrow. Reserving capacity is not permission to violate a reference's access contract.

The borrow checker reasons about places with varying precision. It can understand disjoint struct fields and many slice splits exposed through safe APIs. A pair of arbitrary indices requires a check that they differ; use a library method that expresses this fact rather than assuming that a failed proof means the algorithm is fundamentally impossible in Rust.

## Compiler drill

{{drill}}

Read the spans in order: creation of the shared borrow, attempted conflicting mutation, and later use keeping the shared borrow live. Moving the print earlier may end the borrow requirement before mutation. Cloning changes ownership and allocation; it is often unnecessary here.

## Exercise

Fix the drill by changing operation order. Then take a mutable slice of `[1, 2, 3, 4]`, call `split_at_mut(2)`, and change both halves. Explain why the two returned slices can coexist.

<details><summary>Solution and acceptance check</summary>

Print `shared` before `text.push('!')`. The earlier print reads `record`, and the owned string ends as `record!`. For the slice, bind `(left, right)` from `split_at_mut(2)`, then update `left[0]` and `right[0]`. The function's contract and implementation establish nonoverlapping element ranges; no element has two independent exclusive access paths. The unsafe lab later examines that boundary.

</details>

Sources: [borrowing](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html), [borrow-checking internals](https://rustc-dev-guide.rust-lang.org/borrow_check.html), and [`split_at_mut`](https://doc.rust-lang.org/std/primitive.slice.html#method.split_at_mut).
