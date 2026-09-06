# Practical Rust

Understand it. Build with confidence.

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

---

A free practical Rust course with 28 lessons, compiler drills, and an installable CLI capstone.

Start at rust.robertdevore.com.
