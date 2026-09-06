use std::sync::atomic::{AtomicUsize, Ordering};
fn main() {
    let count = AtomicUsize::new(0);
    std::thread::scope(|s| {
        for _ in 0..4 {
            s.spawn(|| {
                for _ in 0..100 {
                    count.fetch_add(1, Ordering::Relaxed);
                }
            });
        }
    });
    assert_eq!(count.load(Ordering::Relaxed), 400);
}
