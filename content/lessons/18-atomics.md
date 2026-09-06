{"title":"Atomics and memory ordering","stage":3,"minutes":60,"summary":"Separate an indivisible counter update from publication of other data.","example":"18_atomics"}
---
## What the counter actually promises

Several threads increment one atomic counter. Each read-modify-write is atomic, so updates to that counter are not lost. We do not use the counter to announce that unrelated memory is ready.

{{example}}

`Relaxed` is enough for the count's own atomic updates in this example. The scoped threads finish before the final assertion, giving the necessary completion synchronization. If the main thread read while workers were still running, it could observe an intermediate count. The counter does not mean “all workers are finished” by itself.

## Publication is a different problem

Imagine one thread writes a payload and then sets a ready flag. Another waits for ready and reads the payload. A relaxed flag does not, by itself, establish the ordering needed to publish unrelated non-atomic memory safely. A release operation paired with an acquire operation that observes it, or an appropriate release sequence, can establish a happens-before relationship. The payload's access pattern still needs a complete proof.

`SeqCst` adds a global order for sequentially consistent atomic operations, subject to the model's rules. It does not turn a multi-step algorithm into a transaction, prevent deadlocks, or make ordinary conflicting memory accesses acceptable. Stronger ordering can simplify a proof, but it does not replace one.

We deliberately do not build a hand-written lock-free queue here. Such a queue also requires reasoning about ownership, allocation reclamation, ABA-like situations, progress, and every interleaving—not just selecting an ordering enum.

## Keep layers separate

The Rust atomic API specifies language-level behavior and follows a memory-model framework documented by the standard library. Supported atomic widths depend on the target. OS scheduling and hardware instructions affect performance and progress in ways that are not synonymous with Rust's safety guarantees.

An algorithm can be data-race-free and still produce an incorrect result. Two individually atomic operations may interleave with another thread between them. “Atomic” modifies an operation, not the whole surrounding business rule. Even a sequence of atomics may need a mutex to implement the intended invariant simply.

## Exercise

Change the number of workers and increments, compute the expected total, and assert it after joining. Then explain why replacing a future payload-ready flag with `Relaxed` would require a different argument from this counter.

<details><summary>Solution and acceptance check</summary>

With six workers and 250 increments, the final count is 1500. Choose a size that cannot wrap the target's `usize`. The result follows from atomic updates and completion synchronization. Publishing a payload asks whether other memory writes become visible and whether conflicting access is excluded; the count-only proof does not answer that question.

</details>

For a deeper treatment, read the [standard atomic documentation](https://doc.rust-lang.org/std/sync/atomic/) and Mara Bos's [memory-ordering chapter](https://mara.nl/atomics/memory-ordering.html). These support the distinction between atomicity and synchronization; they do not constitute an endorsement of this course.
