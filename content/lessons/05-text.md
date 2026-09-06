{"title":"Strings, slices, and collections","stage":1,"minutes":45,"summary":"Use UTF-8 deliberately and choose ownership at collection boundaries.","example":"05_text"}
---
## Text is not an array of letters

A `String` owns text. A `str` is a dynamically sized sequence of UTF-8 bytes, usually accessed through `&str`. Our parser will accept `&str` because it only reads a record. A caller can pass a string literal, a slice of an owned string, or other borrowed text without first allocating another string.

{{example}}

The final character in `café` occupies two UTF-8 bytes. `len()` reports bytes, while `chars()` iterates Unicode scalar values. Neither necessarily reports user-perceived grapheme clusters: combining marks and multi-scalar emoji make that distinction visible. A byte range must end at UTF-8 boundaries. `get` returns `None` for an invalid range; direct slicing can panic. There is no general constant-time “character at index” operation on UTF-8 text.

## Select storage from the operations

`Vec<T>` owns a growable contiguous sequence. `[T; N]` has a fixed length as part of its type. `&[T]` borrows a sequence without requiring a particular owning container. An interface taking a slice is often more useful than one taking `&Vec<T>`.

A `HashMap` provides key-based lookup without a stable iteration order. A `BTreeMap` maintains keys in sorted order. If output must be deterministic, make ordering explicit instead of relying on the incidental order of a hash table. Our three severity counters do not need any map at all: three named fields make their meaning clear.

`iter()` borrows elements, `iter_mut()` allows mutation of elements under an exclusive collection borrow, and `into_iter()` consumes the value on which it is called. The receiver matters: consuming an owned vector yields its elements, while iterating a borrowed collection yields references. Look at the iterator's `Item` type when unsure.

## Bound growth at the input boundary

`read_to_string` is convenient when inputs are intentionally small. It is not a bounded-memory solution for arbitrary files. Likewise, “read one line at a time” can still allocate an enormous buffer if an input contains no newline. The capstone will enforce a byte limit while accumulating a record, before constructing an unbounded string.

A vector's capacity is reserved storage, not initialized elements. Its length describes initialized values available to safe callers. Never treat spare capacity as initialized data. Increasing the length unsafely introduces obligations far beyond avoiding an index panic; we will not use that technique for this application.

## Exercise

Collect only records beginning with `WARN `, using borrowed slices rather than new `String` values. Test with `WARNING ignored` to prove the separator matters. Then explain what must stay alive while your collected slices are used.

<details><summary>Solution and acceptance check</summary>

Use an iterator over the input records and filter with `starts_with("WARN ")`. Collect `&str` items. Only `WARN retry` should match among `INFO ok`, `WARN retry`, and `WARNING ignored`. The backing input strings must remain valid and cannot be mutated in ways conflicting with those borrows. If the result must outlive the input, owning strings may be the correct design.

</details>

Sources: [`str`](https://doc.rust-lang.org/std/primitive.str.html), [`Vec`](https://doc.rust-lang.org/std/vec/struct.Vec.html), and [collections](https://doc.rust-lang.org/std/collections/index.html).
