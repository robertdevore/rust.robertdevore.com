fn append(text: &mut String) {
    text.push('!');
}
fn main() {
    let mut text = String::from("ready");
    let view = &text;
    assert_eq!(view, "ready");
    append(&mut text);
    let exclusive = &mut text;
    append(&mut *exclusive);
    assert_eq!(exclusive, "ready!!");
}
