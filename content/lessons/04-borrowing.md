{"title":"Borrowing and reborrowing","stage":1,"minutes":55,"summary":"Use shared and exclusive references, and see when a borrow ends.","example":"04_borrowing","drill":"alias"}
---
## Access has a duration

A reference gives access to another value without taking ownership of that value. `&T` provides shared access; `&mut T` provides exclusive access subject to reborrowing. The distinction controls who may access the value, not just whether a method writes to it.

While a shared reference remains usable, other code cannot change ordinary data in ways that violate that reference. An exclusive reference prevents conflicting access through other paths. This does not mean only one pointer can exist. Later lessons cover interior mutability and the rules unsafe code must follow.

{{example}}

The last use of `view` occurs before `append`. The compiler therefore permits the mutation without waiting for the closing brace of `main`. This is called non-lexical lifetime analysis: the compiler follows where you use a borrow, not just where its variable was declared.

The second call passes `&mut *exclusive`. It temporarily **reborrows** through the exclusive reference. During that smaller borrow, the original reference cannot be used for conflicting access. After the call, the original reference becomes usable again. Function calls commonly insert reborrows implicitly; writing one explicitly helps you see the relationship.

## Why a push can invalidate a reference

A vector or string may need a larger allocation when it grows. A reference into its old allocation could then point at freed storage. But the access rules do more than prevent reallocation: even a mutation that fits in existing capacity may conflict with a live shared borrow. Reserving capacity is not permission to violate a reference's access contract.

The borrow checker reasons about places with varying precision. It can understand disjoint struct fields and many slice splits exposed through safe APIs. For arbitrary indices, it needs to know that they differ. Use a library method that checks this. A borrow-checking error may mean the compiler needs a clearer way to see that the accesses are separate.

## Compiler drill

{{drill}}

Read the spans in order: creation of the shared borrow, attempted conflicting mutation, and later use keeping the shared borrow live. Moving the print earlier may end the borrow requirement before mutation. Cloning changes ownership and allocation; it is often unnecessary here.

## Exercise

Fix the drill by changing operation order. Then take a mutable slice of `[1, 2, 3, 4]`, call `split_at_mut(2)`, and change both halves. Explain why the two returned slices can coexist.

<details><summary>Solution and acceptance check</summary>

Print `shared` before `text.push('!')`. The earlier print reads `record`, and the owned string ends as `record!`. For the slice, bind `(left, right)` from `split_at_mut(2)`, then update `left[0]` and `right[0]`. The function's contract and implementation establish nonoverlapping element ranges; no element has two independent exclusive access paths. The unsafe lab later examines that boundary.

</details>

Sources: [borrowing](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html), [borrow-checking internals](https://rustc-dev-guide.rust-lang.org/borrow_check.html), and [`split_at_mut`](https://doc.rust-lang.org/std/primitive.slice.html#method.split_at_mut).
