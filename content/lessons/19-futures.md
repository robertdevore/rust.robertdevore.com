{"title":"Futures before runtimes","stage":3,"minutes":55,"summary":"Learn how polling and wakeups work before adding an async runtime.","example":"19_futures","headingIds":{"When a future starts running":"creating-a-future-is-not-starting-a-thread"}}
---
## When a future starts running

An `async` block produces a future. Calling an async function also creates a future. Its body runs when the future is polled. A future describes a computation that may be incomplete. The `Future` trait connects it to a poller through `poll`, `Context`, and `Poll`.

{{example}}

This future completes immediately, so one poll with a no-op waker is sufficient. This example has **no executor** to schedule later polls. A future that returns `Pending` must arrange a wakeup when it may make progress. Repeatedly polling it in a tight loop would waste CPU, and never polling it again would stall it. Do not adapt this demonstration into a general runtime.

## Suspension stores state

Conceptually, the compiler transforms an async body into a state machine containing what it needs across suspension points. A future can therefore contain owned values and borrows. Its size and whether it is `Send` depend on the state it may hold. A non-`Send` value retained across an await can prevent moving the future between worker threads.

`.await` drives another future as part of the current task. If it is not ready, the current future may yield `Pending` to its caller. If it is already ready, execution may continue immediately. An `.await` is not a promise of a scheduler yield, a new task, or parallel execution.

After a future returns `Ready`, callers must not assume polling it again is supported. Polling it again may panic or produce no useful result, though it must still obey Rust's safety rules. A runtime tracks completion so ordinary application code need not manually manage this state.

## Cancellation belongs to ownership

Dropping a pending future commonly cancels that instance of the computation by dropping its stored state. It does not undo an external effect that already occurred. A request may have reached a server even if the caller stopped awaiting its response. Decide what cancellation means for your application. A retry may need a request ID or a transaction to avoid repeating an external change.

The runtime manages a spawned task until it finishes or is cancelled. Dropping its join handle is not necessarily the same as dropping the future inside it. Tokio, for example, detaches a task when its handle is dropped. Always read the runtime's contract before treating a handle as a cancellation guard.

## Exercise

Explain why the example's no-op waker is valid for this immediately ready future but not for a timer. Identify what data would have to survive if an async function borrowed a string before a wait and used it afterward.

<details><summary>Solution and acceptance check</summary>

The immediate future needs no later wakeup. A timer may return `Pending` and must notify a real executor when time advances. The borrowed string's owner must remain valid while the future can use the borrow; the future itself carries the reference or equivalent state. Moving work into async syntax does not erase those ownership requirements.

</details>

Sources: [`Future`](https://doc.rust-lang.org/std/future/trait.Future.html), [await expressions](https://doc.rust-lang.org/reference/expressions/await-expr.html), and [async blocks](https://doc.rust-lang.org/reference/expressions/block-expr.html#async-blocks).
