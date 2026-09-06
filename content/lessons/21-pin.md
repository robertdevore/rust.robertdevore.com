{"title":"Pin and async trait boundaries","stage":4,"minutes":65,"summary":"Understand address-sensitive values and stable alternatives to native async dyn dispatch.","example":"21_pin","drill":"async_dyn"}
---
## Pin is a promise about a pointee

Some values become address-sensitive, including futures that may contain references into their own suspended state. `Pin<P>` constrains how the pointee accessed through pointer `P` may be moved. It does not mean the pointer handle itself cannot move, and it does not automatically allocate anything.

For `T: Unpin`, moving the value does not violate a pinning invariant, so many pin restrictions become irrelevant. For a `!Unpin` value, safe APIs prevent operations that would violate the pin contract. The contract also involves destruction and storage validity; it is stronger than “do not call mem::swap right now”.

## Use safe constructors first

`pin!` pins a value in local storage. `Box::pin` owns a pinned allocation whose handle can move. Most async application code can use these or runtime helpers without implementing unsafe projection. Accessing a pinned struct's fields requires knowing which fields are structurally pinned. Do not use `get_unchecked_mut` just to bypass a compiler error.

{{example}}

The interface returns a boxed, pinned, erased future. Its lifetime is connected to `&self`, so the result can borrow the service. The example uses a local executor and does not require `Send`. An API intended for movable spawned tasks may need `Send` on the returned future and appropriate bounds on the captured data.

## Stable async traits are not every async trait feature

Native `async fn` in traits works on stable Rust for supported static-dispatch cases. That does not imply those methods can be dispatched directly through `dyn Trait`. Returning an explicitly erased future is a stable alternative, with allocation and indirection costs. The `async-trait` crate automates a related transformation; it should be chosen for a needed boundary, not added to every async trait by habit.

{{drill}}

The drill captures the current direct-dyn rejection. Its existence is an implementation and language capability boundary at this verification date, not a declaration that Rust will never support the pattern. Current async and field-projection initiatives aim to improve these awkward edges.

## Exercise

Explain why moving the `Box` handle is compatible with pinning its allocated future. Then remove the trait object entirely and call a concrete async method. Compare what the two designs require from allocation and the public signature.

<details><summary>Solution and acceptance check</summary>

The pointee stays in its allocation when the owning pointer moves. A concrete async method can return its compiler-generated future without the explicit box and vtable used here. Prefer that simpler design unless callers actually need runtime heterogeneity or an erased interface. Do not claim a speedup without measuring the relevant workload.

</details>

Sources: [`std::pin`](https://doc.rust-lang.org/std/pin/), [trait rules](https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility), and [the async trait RFC](https://rust-lang.github.io/rfcs/3185-static-async-fn-in-trait.html).
