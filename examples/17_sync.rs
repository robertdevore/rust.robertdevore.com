use std::{sync::mpsc::sync_channel, thread};
fn main() {
    let (sender, receiver) = sync_channel(2);
    let worker = thread::spawn(move || {
        for value in [1, 2, 3] {
            sender.send(value).unwrap();
        }
    });
    let total: i32 = receiver.iter().sum();
    worker.join().unwrap();
    assert_eq!(total, 6);
}
