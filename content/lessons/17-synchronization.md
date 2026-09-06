{"title":"Channels, locks, and shutdown","stage":3,"minutes":55,"summary":"Pass work through channels, protect shared data, and shut down without deadlocks.","example":"17_sync","headingIds":{"What each layer controls":"distinguish-the-guarantees"}}
---
## Give the state a clear owner

A producer creates work; a consumer receives it and keeps the running total. A channel transfers each message to the consumer. This avoids multiple workers mutating the same summary and makes the shutdown condition visible.

{{example}}

The synchronous channel has capacity two. Sending can block when the queue is full. The consumer keeps receiving until every sender is dropped. Here the producer's sender is dropped on return, so iteration ends and joining is safe.

If the main thread retained an unused sender clone, the receiver could wait forever. If the main thread joined a blocked producer before draining the full channel, the program could deadlock. Both bugs can occur in fully safe Rust. Write down who closes the queue and who drains it before choosing the order of waits.

## When a mutex is appropriate

A short update to a genuinely shared data structure can fit `Arc<Mutex<T>>`. The lock stays held for as long as its guard lives. Copy or move out the small result you need and release the guard before unrelated slow work. Avoid calling arbitrary callbacks while holding a lock unless the contract explicitly covers reentrancy and lock ordering.

Standard mutex poisoning indicates that a panic may have interrupted a protected operation. It is advisory and not a soundness mechanism. Recovery must examine application invariants; blindly calling `into_inner` is not evidence the state is usable. Likewise, an unpoisoned mutex is not proof that the algorithm is correct.

Acquire multiple locks in a consistent order where possible. A read-write lock can help some read-heavy patterns, but it is not automatically faster and can introduce different contention behavior. Draw who owns the data and measure contention before choosing a more complex lock.

## What each layer controls

The language and standard library describe what data can be safely accessed and what synchronization establishes. The OS chooses which runnable threads execute. Hardware may reorder operations within constraints imposed by the language memory model. Application architecture decides whether messages can be retried or discarded. A program that works under one schedule may still fail under another.

## Exercise

Draw the channel's close-and-drain sequence. Add a producer error path that returns early and confirm the consumer still terminates. Then describe how you would report an error without treating a partial aggregate as complete.

<details><summary>Solution and acceptance check</summary>

An early return drops that sender; if no senders remain, receiving eventually ends after queued messages drain. Joining the producer reveals whether it completed successfully. Return a status with the partial total, or reject the result. A disconnected channel alone does not prove the producer processed every intended item.

</details>

Sources: [`sync_channel`](https://doc.rust-lang.org/std/sync/mpsc/fn.sync_channel.html), [`Mutex`](https://doc.rust-lang.org/std/sync/struct.Mutex.html), and [message-passing concurrency](https://doc.rust-lang.org/book/ch16-02-message-passing.html).
