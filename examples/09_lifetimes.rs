fn message(line: &str) -> Option<&str> {
    line.split_once(' ').map(|(_, message)| message)
}
fn choose<'a>(left: &'a str, right: &'a str) -> &'a str {
    if left.len() >= right.len() {
        left
    } else {
        right
    }
}
fn main() {
    let input = String::from("INFO ready");
    assert_eq!(message(&input), Some("ready"));
    assert_eq!(choose(&input, "WARN x"), "INFO ready");
}
