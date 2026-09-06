# Borrow, then move

Inspect a String through a shared reference, then transfer ownership.

```rust
fn label(text: &str) -> usize {
    text.len()
}
fn main() {
    let original = String::from("WARN retry");
    let bytes = label(&original);
    let stored = original;
    assert_eq!(bytes, 10);
    assert_eq!(stored, "WARN retry");
}

```

**Concepts:** borrowing, moves, assertions

The example passes assertions and produces no stdout on Rust 1.98.1.

---

Borrow to inspect. Move to transfer ownership. Run this example, then change it and read the compiler.

Study lesson 03 in the free Rust course.
