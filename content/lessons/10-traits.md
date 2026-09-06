{"title":"Traits and reusable interfaces","stage":2,"minutes":55,"summary":"Use standard traits, associated types, and static or dynamic dispatch.","example":"10_traits","headingIds":{"Write to more than one destination":"start-from-a-useful-boundary"}}
---
## Write to more than one destination

A report should write to a file, terminal, or test buffer without duplicating formatting logic. `std::io::Write` already describes that capability. The destination changes, but the formatting code stays the same.

{{example}}

`impl Write` in a parameter is a convenient way to accept a concrete type implementing the trait. It uses static dispatch in this setting. A generic `W: Write` with a named parameter is useful when several arguments or return positions need to refer to the same type. Use a named type parameter when you need to refer to it elsewhere in the signature.

The second call goes through `&mut dyn Write`. A trait object erases the concrete implementation behind a reference and dispatches through a vtable. The reference itself does not require a heap allocation; `Box<dyn Write>` would introduce an owning allocation. Static dispatch may enable inlining but can increase generated code across instantiations. Dynamic dispatch can reduce duplication but introduces indirection. Measure where those tradeoffs matter.

## Associated types carry a relationship

`Iterator` has an associated `Item` type. Each iterator implementation specifies what one step yields. A trait parameter instead permits the same implementing type to participate in different instantiations of the trait when the rules allow it. Select the design that matches the relationship rather than treating associated types as interchangeable syntax.

Trait implementations obey coherence rules, including restrictions on implementing an external trait for external types. A local wrapper, often called a newtype, lets you define an implementation for your own type. Give the wrapper a clear purpose; unnecessary wrappers make callers do more work.

## Dyn compatibility is a checked contract

Not every trait can form a trait object. A method with generic type parameters or a hidden return type can need information that the object interface does not provide. The Reference calls this **dyn compatibility**; older material often says object safety. Native async trait methods support static dispatch on the stable compiler used here. Calling them directly through `dyn Trait` is still a separate limitation.

A compiler's inability to prove a bound is not automatically a mathematical impossibility. The next-generation trait solver is evolving. Keep a minimal reproduction and a pinned compiler when explaining a limitation; do not turn it into a timeless rule about Rust.

## Exercise

Use `report` with two counts and assert the exact bytes in a `Vec<u8>`. Add a writer that deliberately returns an I/O error and verify that `report` propagates it. Explain why a custom `ReportSink` trait adds no useful capability to this example.

<details><summary>Solution and acceptance check</summary>

The buffer must contain `records=3\nrecords=4\n`. A failing `Write::write` implementation should make `report` return `Err`; do not swallow it. The standard trait already supports the real variation and integrates with existing types. Add a new trait only if it describes behavior that `Write` does not.

</details>

Sources: [`Write`](https://doc.rust-lang.org/std/io/trait.Write.html), [dyn compatibility](https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility), and [coherence](https://doc.rust-lang.org/reference/items/implementations.html#trait-implementation-coherence).
