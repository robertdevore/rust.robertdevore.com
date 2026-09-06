{"title":"Ownership, places, and moves","stage":1,"minutes":55,"summary":"Learn what moves, what gets copied, and when a borrow is enough.","example":"03_ownership","drill":"moved"}
---
## A value and the place holding it

A **place** is a location a program can refer to: a local variable, a field, an indexed element, or a dereferenced pointer. A **value** is what the location currently holds. Moving a value transfers it out of a place. The heap allocation it owns may stay at the same address.

`String` owns and tracks a UTF-8 buffer. If two independent strings both tried to free that buffer, the program could free the same memory twice. Moving a `String` makes the source unavailable until reinitialized. The new owner normally drops the value when its drop scope ends.

{{example}}

`label(&original)` lends access, so it does not take ownership of the string. `let stored = original` does transfer the value. No second character buffer is needed. The compiler may optimize away the move itself. A move in Rust source does not promise a particular machine instruction.

## Copy is a type property

Some types implement `Copy`: using their values in a move-like context implicitly copies them and leaves the source usable. Integers are familiar examples. Heap versus stack is not the rule: references can be copied, and a stack-resident struct can own a non-`Copy` resource. A type implementing `Drop` cannot also implement `Copy`.

`Clone` requests duplication explicitly, but its meaning depends on the type. Cloning a `String` duplicates its text; cloning an `Rc` adds an owner to shared data. Before adding `.clone()` to fix an error, ask what the caller needs: ownership, a temporary borrow, or a separate copy it can change.

## Follow destruction, not just allocation

Values are normally dropped when their drop scope ends; moving transfers that responsibility. Fields can sometimes be moved separately, leaving a partially moved struct whose remaining fields are still usable. A type with a destructor restricts such moves because its destructor expects an intact value. Leaking memory with safe operations is possible: Rust does not promise that every destructor always runs. Never base an unsafe abstraction's soundness solely on a caller eventually calling `drop`.

The early model “one owner” describes ordinary owning values, not a ban on shared ownership. `Rc` and `Arc` coordinate multiple owning handles through a reference count. They do not automatically make the contained data mutable or thread-safe.

## Compiler drill

{{drill}}

The diagnostic identifies the earlier move and the later use. Repair the design before considering duplication. Can the recipient borrow? Can the original caller stop using the value? Are two independently editable strings actually required?

## Exercise

Repair the drill without cloning. Then make a second version in which two independent strings are deliberately required and justify the clone in one sentence. In each version, identify which binding is responsible for dropping which allocation.

<details><summary>Solution and acceptance check</summary>

For shared read-only access, use `let stored = &original`; printing both is then valid. Alternatively print only the new owner after a move. For two independently editable strings, use `let stored = original.clone()` and mutate one to show the other remains unchanged. The two allocations each have an owner and are each dropped once in ordinary execution.

</details>

Sources: [places and moves](https://doc.rust-lang.org/reference/expressions.html#place-expressions-and-value-expressions), [destructors](https://doc.rust-lang.org/reference/destructors.html), and [`Copy`](https://doc.rust-lang.org/std/marker/trait.Copy.html).
