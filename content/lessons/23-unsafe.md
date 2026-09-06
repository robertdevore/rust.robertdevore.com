{"title":"Unsafe boundaries and soundness","stage":4,"minutes":85,"summary":"Audit one small abstraction with explicit invariants, edge cases, and Miri.","source":"crates/unsafe-lab/src/lib.rs"}
---
## Unsafe does not suspend Rust's rules

Unsafe operations have requirements the compiler cannot completely verify. An unsafe block makes the programmer responsible for meeting those requirements; undefined behavior remains forbidden. A safe API is sound only if every safe caller allowed by its interface is prevented from triggering undefined behavior through that API.

The lab reimplements a tiny slice split for study. Production application code should use the standard `split_at_mut`. Keeping the lab separate lets the application forbid unsafe code while the learning boundary receives dedicated review.

{{source}}

## The safety argument

**What must remain true?** Both returned slices cover initialized elements from the original slice, stay within its allocation, retain valid alignment and provenance, and refer to disjoint logical element ranges. Their references cannot outlive the original borrow.

**Who maintains it?** The caller supplies a valid exclusive slice through a safe Rust type. The function checks the split index before pointer arithmetic. Its implementation constructs exactly the two ranges. Borrow checking relates the returned lifetimes to the input.

**Which safe callers are allowed?** Any valid mutable slice, including empty slices, zero-sized element types, and types with destructors. A split at either endpoint is valid. An out-of-range index must panic before unsafe operations. No extra undocumented obligation is imposed on a safe caller.

**How is the surface contained?** One unsafe block follows a checked boundary. The raw pointer does not escape. No allocation is freed and no element ownership is duplicated. The application never depends on this study implementation.

**What would make it unsound?** Removing the bounds check, overlapping nonempty element ranges, inventing a longer return lifetime, accepting an arbitrary unvalidated pointer, or allowing conflicting access through the original slice while the returned borrows are live.

## Aliasing is more than addresses

Zero-sized elements can share an address without representing overlapping stored bytes. A simplistic “different addresses means safe” argument would fail to cover them. Likewise, `UnsafeCell` relaxes shared-reference immutability for its contents but does not erase exclusive-reference rules or synchronize concurrent accesses.

The Reference explicitly notes that exact aliasing rules remain an active specification area. Miri provides operational checks under its models; passing a run does not establish a universal proof or freeze a model as the final language specification. We test ordinary elements, endpoints, empty input, zero-sized elements, and drop behavior, then inspect the invariant argument separately.

## Exercise

Run the isolated lab under Miri:

```sh
rustup toolchain install nightly-2026-09-05 --profile minimal --component miri
cargo +nightly-2026-09-05 miri test -p unsafe-lab
```

Explain why no destructor may run twice and why a safe caller using `mem::forget` must not invalidate the abstraction. Do not execute deliberately undefined examples in a normal production process.

<details><summary>Solution and acceptance check</summary>

The function returns borrows, not new owners of elements. Dropping a slice reference does not drop its elements. The original owner retains destruction responsibility. Forgetting a reference does not produce conflicting access by itself; the implementation does not rely on its destructor running. The tests check representative paths, and the written proof covers arbitrary safe callers.

</details>

Sources: [undefined behavior](https://doc.rust-lang.org/reference/behavior-considered-undefined.html), [Rustonomicon](https://doc.rust-lang.org/nomicon/), [`from_raw_parts_mut`](https://doc.rust-lang.org/std/slice/fn.from_raw_parts_mut.html), and [Miri](https://github.com/rust-lang/miri).
