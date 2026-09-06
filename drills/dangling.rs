fn label() -> &'static str {
    let text = String::from("record");
    &text
}
fn main() { println!("{}", label()); }
