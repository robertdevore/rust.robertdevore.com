{"title":"Tokio tasks, blocking, and cancellation","stage":3,"minutes":70,"summary":"Use a runtime with bounded queues, explicit task results, and deliberate shutdown.","example":"20_async"}
---
## Five layers, five responsibilities

Rust supplies async syntax. `Future` defines polling. An executor schedules tasks. Tokio supplies an executor plus timers, channels, and I/O integration. Your application defines limits, retries, state ownership, and shutdown. Learning Tokio is useful, but Tokio is not the language's definition of async.

{{example}}

The macro builds a current-thread Tokio runtime. A producer task sends four values into a bounded channel. The consumer drains it, and the producer's sender is dropped at completion. The join handle returns a task result containing the producer's own result; `await??` checks both failure layers.

## Bound the work that can accumulate

A channel with capacity two creates backpressure: a send can wait for space. This bounds queued messages, not the size of each message or the total number of tasks elsewhere in the program. A production design must bound those separately.

Tokio schedules cooperatively. A long computation or blocking filesystem call inside a task can occupy the runtime thread and prevent other tasks from progressing. Async syntax alone does not make a function nonblocking. Use an appropriate async API, a dedicated worker, or `spawn_blocking` with a deliberate concurrency limit. A started blocking task generally cannot be aborted just by aborting its async handle.

## Cancellation needs an operation-specific contract

Selecting between two futures drops a losing future in common patterns. Ask what progress it may have made and whether retrying loses or duplicates work. Tokio's `mpsc::Receiver::recv` has documented cancellation behavior useful in select loops. Other operations, such as reading an exact number of bytes, may have consumed partial input before cancellation.

A timeout is not rollback. Dropping a `JoinHandle` detaches the task; call `abort` when appropriate and await the handle to observe completion. Abortion takes effect when the task yields control, and destructors are part of cleanup. If cleanup needs asynchronous work, implement an explicit shutdown protocol rather than assuming ordinary `Drop` can await.

## Exercise

Write a deterministic timeout test using Tokio's paused test clock. Make a receiver wait on an empty channel while a sender still exists; advance time and assert a timeout. Then drop the sender and assert that `recv` returns `None`. Use the repository's async tests as a reference after trying it.

<details><summary>Solution and acceptance check</summary>

Use `#[tokio::test(start_paused = true)]` with a current-thread test runtime and `tokio::time::timeout`. Paused time lets the runtime advance to the next timer when idle, avoiding fragile wall-clock sleeps. Retaining a sender prevents “channel closed” from winning first. Once the final sender is dropped, the receiver terminates. These are different outcomes and should have separate assertions.

</details>

Sources: [Tokio channels](https://tokio.rs/tokio/tutorial/channels), [shutdown](https://tokio.rs/tokio/topics/shutdown), [JoinHandle](https://docs.rs/tokio/latest/tokio/task/struct.JoinHandle.html), and Alice Ryhl's [blocking explanation](https://ryhl.io/blog/async-what-is-blocking/).
