{"title":"Iterators and closures without hidden ownership","stage":2,"minutes":45,"summary":"Read item types, captures, laziness, and short-circuiting results.","example":"11_iterators"}
---
## An iterator describes a sequence of steps

An iterator produces an `Option<Item>` each time `next` is called. Many adaptors, including `map` and `filter`, are lazy: constructing them does not perform the whole computation. A consumer such as `collect`, `sum`, or a `for` loop drives the steps.

{{example}}

`rows.iter()` yields references to array elements, so each item is `&&str`. `copied()` copies the small shared reference to give `&str`; it does not duplicate the text allocation. `filter` itself passes a reference to its item to the predicate. Checking these layers explicitly is more reliable than trying random dereferences until the compiler accepts them.

Collecting an iterator of `Result` values into `Result<Vec<_>, _>` stops at the first error. This implements one particular failure policy. Collecting all errors requires a different design and often a different output type. A concise iterator chain is good only when its policy remains clear.

## Closures capture what they need

A closure is an anonymous function-like value that can capture its environment. It may borrow shared data, borrow it mutably, or consume captured values depending on its body. `move` requests ownership capture; it does not by itself imply the closure can only be called once. The operations performed by the body determine whether it implements `Fn`, `FnMut`, or only `FnOnce`.

A closure that consumes a captured string by returning it can generally run only once. A closure that owns a string but only reads its length can run repeatedly. This distinction matters when passing closures to iterators and spawning tasks.

## Prefer understandable data flow

A loop is often clearer when you must update several counters, attach a line number to an error, and maintain a record-size limit. Iterator chains are not morally superior to loops. Both can compile efficiently; neither establishes performance without measurement.

Avoid collecting merely to iterate immediately again when a streaming consumer would do. Conversely, collecting is sensible when you need random access or multiple passes. If a borrow makes your chain hard to express, inspect the ownership boundary before cloning the entire input collection.

## Exercise

Change the fixture to include `BOGUS bad` between two valid records. Show that collecting into `Result<Vec<_>, _>` returns the parser error. Then implement an explicit loop that counts valid records and errors separately, and write down how that changes the tool's contract.

<details><summary>Solution and acceptance check</summary>

The first version returns `UnknownLevel`, with no successful vector. The second can retain two valid records and one rejection count. Its report must identify the rejection; silently reporting two records as if the input were wholly valid is misleading. Use a `match` on each result to make that policy visible.

</details>

Sources: [`Iterator`](https://doc.rust-lang.org/std/iter/trait.Iterator.html), [closure capture](https://doc.rust-lang.org/reference/types/closure.html), and [`FromIterator` for `Result`](https://doc.rust-lang.org/std/result/enum.Result.html#impl-FromIterator%3CResult%3CA,+E%3E%3E-for-Result%3CV,+E%3E).
