fn classify(milliseconds: u32) -> &'static str {
    if milliseconds < 100 { "fast" } else { "slow" }
}
fn main() {
    let samples = [12, 100, 340];
    for value in samples {
        println!("{value}: {}", classify(value));
    }
    assert_eq!(classify(100), "slow");
    assert_eq!(u8::MAX.checked_add(1), None);
}
