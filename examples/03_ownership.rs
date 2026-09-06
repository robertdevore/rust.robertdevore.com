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
