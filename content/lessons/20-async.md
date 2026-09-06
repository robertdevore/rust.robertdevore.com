{"title":"Tokio tasks, blocking, and cancellation","stage":3,"minutes":70,"summary":"Run Tokio tasks, limit queued work, and handle blocking calls and cancellation.","example":"20_async","headingIds":{"What Tokio provides":"five-layers-five-responsibilities","Limit queued work":"bound-the-work-that-can-accumulate","Check what cancellation leaves behind":"cancellation-needs-an-operation-specific-contract"}}
---
## What Tokio provides

Rust supplies async syntax. `Future` defines polling. An executor schedules tasks. Tokio supplies an executor plus timers, channels, and I/O integration. Your application defines limits, retries, state ownership, and shutdown. Tokio is one runtime for Rust async code; it does not define the language feature.

{{example}}

The macro builds a current-thread Tokio runtime. A producer task sends four values into a bounded channel. The consumer drains it, and the producer's sender is dropped at completion. The join handle reports whether the task failed and contains the producer's own result. In `await??`, the first `?` checks the task result; the second checks the producer's result.

## Limit queued work

A channel with capacity two creates backpressure: a send can wait for space. This bounds queued messages, not the size of each message or the total number of tasks elsewhere in the program. A production design must bound those separately.

Tokio schedules cooperatively. A long computation or blocking filesystem call inside a task can occupy the runtime thread and prevent other tasks from progressing. Async syntax alone does not make a function nonblocking. Use an appropriate async API, a dedicated worker, or `spawn_blocking` with a deliberate concurrency limit. A started blocking task generally cannot be aborted just by aborting its async handle.

## Check what cancellation leaves behind

Selecting between two futures drops a losing future in common patterns. Ask what progress it may have made and whether retrying loses or duplicates work. Tokio's `mpsc::Receiver::recv` has documented cancellation behavior useful in select loops. Other operations, such as reading an exact number of bytes, may have consumed partial input before cancellation.

A timeout is not rollback. Dropping a `JoinHandle` detaches the task; call `abort` when appropriate and await the handle to observe completion. Abortion takes effect when the task yields control, and destructors are part of cleanup. If cleanup needs async work, write a shutdown step that awaits it. Ordinary `Drop` cannot await.

## Exercise

Write a deterministic timeout test using Tokio's paused test clock. Make a receiver wait on an empty channel while a sender still exists; advance time and assert a timeout. Then drop the sender and assert that `recv` returns `None`. Use the repository's async tests as a reference after trying it.

<details><summary>Solution and acceptance check</summary>

Use `#[tokio::test(start_paused = true)]` with a current-thread test runtime and `tokio::time::timeout`. Paused time lets the runtime advance to the next timer when idle, avoiding fragile wall-clock sleeps. Retaining a sender prevents “channel closed” from winning first. Once the final sender is dropped, the receiver terminates. These are different outcomes and should have separate assertions.

</details>

Sources: [Tokio channels](https://tokio.rs/tokio/tutorial/channels), [shutdown](https://tokio.rs/tokio/topics/shutdown), [JoinHandle](https://docs.rs/tokio/latest/tokio/task/struct.JoinHandle.html), and Alice Ryhl's [blocking explanation](https://ryhl.io/blog/async-what-is-blocking/).
