{"title":"Stage build: an async ingestion pipeline","stage":4,"minutes":80,"summary":"Keep one owner of the aggregate while producers hand over bounded work.","example":"22_stage_three"}
---
## Build brief

Adapt the parsing core to an async ingestion demonstration. One producer sends owned records through a queue. One consumer owns the summary. At normal completion, the queue closes, the consumer drains it, and the producer's result is checked. Keep the synchronous file CLI as the final product: async is useful to study, but it does not automatically improve sequential local file processing.

{{example}}

Each `String` moves into the queue. The consumer borrows it to parse an `Event`, updates the summary, and then drops the record. The event never escapes the record's lifetime. No shared mutable aggregate, reference-counted record, or mutex is required.

## Explain the limits honestly

The queue holds at most two pending messages. This fixture also has a fixed number and size of messages. If you replace it with network input, a bounded queue alone does not cap individual record size, number of connections, or producer-side accumulation. Apply the byte limit before a producer allocates an arbitrarily large record.

The example stops on a parse error through `?`. At that point the receiver is dropped, pending sends fail, and the short-lived runtime shuts down on return. That is enough for a finite teaching fixture. A long-running service needs an explicit supervisor that observes every task outcome and decides whether to drain, cancel, or restart. Do not mistake this demonstration for a complete production server.

## Cancellation exercise

Extend the pipeline so the producer can wait for a shutdown signal. Specify whether already accepted messages are drained. Use a `JoinSet` or explicit task handles to observe completion; do not detach tasks by losing their handles. Add a test in which a shutdown arrives while the queue is full.

<details><summary>Solution and acceptance check</summary>

A valid policy closes admission, drops all producers' senders, drains already queued work, and awaits producer completion. A different policy may discard queued work, but the result must say it is incomplete. In the full-queue test, the consumer must keep making progress or cancellation must release the blocked send. Use deterministic synchronization rather than hoping a sleep creates the intended state.

</details>

## Review the ownership graph

The producer owns each record before sending; the channel owns it while queued; the consumer owns it while parsing. The summary remains local to the consumer. The parser has no runtime dependency and is reused unchanged. This is the benefit of choosing a capability boundary at `&str` and `BufRead` earlier.

If you introduce multiple consumers, decide how totals are merged and how failures affect completeness. A mutex is one possible choice, but local summaries returned to an aggregator can keep the critical path simpler. The right architecture follows workload and failure semantics.

Sources: [Tokio shared state](https://tokio.rs/tokio/tutorial/shared-state), [bounded mpsc](https://docs.rs/tokio/latest/tokio/sync/mpsc/), and [JoinSet](https://docs.rs/tokio/latest/tokio/task/struct.JoinSet.html).
