{"title":"FFI, serialization, and public contracts","stage":4,"minutes":55,"summary":"Define ownership, data formats, and errors when calling code outside Rust.","source":"examples/25_ffi.rs"}
---
## The other side has its own rules

A foreign function interface (FFI) lets Rust call code that may follow different rules. `extern "C"` selects an ABI; it does not validate pointers, lengths, ownership, or lifetimes. `repr(C)` specifies a C-compatible layout scheme for the annotated type, but does not make every contained Rust type appropriate to expose to C.

The following example calls a C-ABI function defined in the same Rust program. It is a portable ABI-boundary exercise, not a demonstration of building or linking an external C library. The byte pointer is not dereferenced because the function only counts a provided length.

{{source}}

A real external declaration needs an unsafe extern block in edition 2024. When adding an actual C library, consult its headers and platform ABI, specify how memory is allocated and released, and test the build on supported targets. Avoid passing `String`, Rust enums with unspecified layout, or trait objects as if their representation were a stable C contract.

## Write down ownership in both directions

For each pointer parameter, ask whether null is allowed, which allocation it belongs to, how many initialized elements are accessible, whether mutation is permitted, and how long the callee retains it. For each returned pointer, identify who frees it and with which allocator. Two libraries can each be correct on their own but crash when they disagree about these rules.

Unwinding across an ABI boundary needs an explicit contract. A panic must not accidentally unwind through an incompatible foreign frame. Catching a panic works only if it unwinds. It cannot recover from an abort or undefined behavior. Do not use panic catching to make invalid pointers acceptable.

C++ has additional challenges around object lifetimes, exceptions, templates, and ownership. Bridge libraries can enforce some of these rules, but you still need to check the foreign code. Current Rust interop initiatives are improving this space; the course's application deliberately needs no FFI.

## A file format is also an interface

Our plain-text format has exact level spelling, UTF-8 messages, and a record-size rule. Adding JSON should use a maintained serializer such as Serde with an explicitly versioned schema. Derived serialization saves repetitive code. You still need to decide how to handle unknown fields, missing fields, and incompatible changes. Never persist `Debug` output as a stable format.

## Exercise

Write a contract for a hypothetical foreign function receiving bytes. Specify pointer validity, length, retention, mutability, ownership, and error reporting. Then identify which checks a safe wrapper could perform and which require trusting the foreign implementation.

<details><summary>Solution and acceptance check</summary>

A slice can provide initialized byte storage and a valid length for the call. The wrapper can pass its pointer and length without transferring ownership. The contract must forbid retaining the pointer beyond the borrow unless a separate ownership protocol exists. The wrapper cannot prove arbitrary foreign code obeys that promise; implementation review and testing remain necessary.

</details>

Sources: [external blocks](https://doc.rust-lang.org/reference/items/external-blocks.html), [type layout](https://doc.rust-lang.org/reference/type-layout.html), [FFI unwinding](https://doc.rust-lang.org/nomicon/ffi.html#ffi-and-unwinding), [Serde](https://serde.rs/), and [interop work](https://goals.rust-lang.org/2026/interop-problem-map.html).
