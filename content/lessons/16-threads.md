{"title":"Threads, Send, and Sync","stage":3,"minutes":55,"summary":"Move or borrow data across threads, then handle completion and failure.","example":"16_threads","drill":"send","headingIds":{"Pass data to a thread":"ownership-crosses-a-boundary","What Send and Sync mean":"the-two-marker-traits-answer-different-questions"}}
---
## Pass data to a thread

A thread can outlive the function that started it. Ordinary `thread::spawn` therefore requires a closure and result satisfying `Send + 'static`. Owned data can satisfy that bound without living forever. A borrowed local cannot simply be sent into a potentially longer-lived thread.

Scoped threads give a different guarantee: they finish before the scope returns. This permits borrowing data that remains valid for that scope.

{{example}}

Two threads read disjoint ranges of the same immutable array. They return counts, and the parent combines them. No lock is needed because there is no shared mutation. `join` also reports a worker panic. The example uses `unwrap` so a panic fails the example. In an application, decide how to report that failure.

## What Send and Sync mean

`Send` means a value can safely be transferred to another thread. `Sync` means a shared reference to the type can safely be transferred between threads. More precisely, `T: Sync` relates to `&T: Send`. These are unsafe traits to implement manually; normally let their automatic derivation from fields describe your type.

`Rc` is not `Send` because its reference count is not synchronized. `Arc` synchronizes ownership bookkeeping. Sharing mutable inner data still needs an appropriate mechanism and trait bounds. Using `Arc` alone does not make access to the data safe.

## Compiler drill

{{drill}}

The compiler traces the requirement from the thread closure to the captured `Rc`. For immutable shared data, `Arc` may be the right correction. If the parent no longer needs the data, moving an ordinary owned value may be simpler. Do not add a mutex when no thread mutates anything.

## Correctness extends beyond data races

Rust's type system and sound libraries rule out many data races in safe code, but not deadlocks, starvation, lost application updates, or wrong ordering of business events. The OS or runtime schedules threads. Rust does not promise that a new thread runs immediately or that threads run in creation order.

Parallel work can also be slower. Thread creation, communication, cache effects, and small inputs can dominate useful computation. Our tiny fixture demonstrates ownership, not a performance win. Benchmark a realistic workload before choosing worker counts.

## Exercise

Repair the drill twice: once by moving a plain integer owner, and once by using `Arc` for immutable sharing. Then explain why the scoped example requires neither an atomic reference count nor a mutex.

<details><summary>Solution and acceptance check</summary>

The move-only version captures an owned value. The shared version clones an `Arc` handle before spawning and joins the thread. Scoped borrows are valid because the scope waits for workers, and shared immutable access does not require a lock. Each version should terminate and produce the same value without ignoring a join result.

</details>

Sources: [`thread::scope`](https://doc.rust-lang.org/std/thread/fn.scope.html), [`Send`](https://doc.rust-lang.org/std/marker/trait.Send.html), and [`Sync`](https://doc.rust-lang.org/std/marker/trait.Sync.html).
