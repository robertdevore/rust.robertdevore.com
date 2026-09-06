fn main() {
    let rows = ["INFO a", "WARN b", "WARN c", "ERROR d"];
    let total = std::thread::scope(|scope| {
        let left = scope.spawn(|| rows[..2].iter().filter(|r| r.starts_with("WARN ")).count());
        let right = scope.spawn(|| rows[2..].iter().filter(|r| r.starts_with("WARN ")).count());
        left.join().unwrap() + right.join().unwrap()
    });
    assert_eq!(total, 2);
}
