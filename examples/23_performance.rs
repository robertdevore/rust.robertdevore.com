use std::{hint::black_box, time::Instant};
fn main() {
    let input = "INFO small message";
    let start = Instant::now();
    for _ in 0..10_000 {
        black_box(audit_core::parse(black_box(input)).unwrap());
    }
    println!(
        "10,000 parses: {:?}; one sample, not a benchmark conclusion",
        start.elapsed()
    );
}
