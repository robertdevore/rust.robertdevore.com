fn main() {
    assert_eq!(env!("CARGO_PKG_NAME"), "rust-course-examples");
    println!(
        "package={} version={}",
        env!("CARGO_PKG_NAME"),
        env!("CARGO_PKG_VERSION")
    );
}
