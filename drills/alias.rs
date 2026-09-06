fn main() {
    let mut text = String::from("record");
    let shared = &text;
    text.push('!');
    println!("{shared}");
}
