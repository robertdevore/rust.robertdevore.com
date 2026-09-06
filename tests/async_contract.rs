use std::time::Duration;
#[tokio::test(start_paused = true)]
async fn timeout_differs_from_channel_close() {
    let (sender, mut receiver) = tokio::sync::mpsc::channel::<u8>(1);
    assert!(
        tokio::time::timeout(Duration::from_secs(5), receiver.recv())
            .await
            .is_err()
    );
    drop(sender);
    assert_eq!(receiver.recv().await, None);
}
#[tokio::test]
async fn abort_is_observed_and_drops_resources() {
    let (sender, mut receiver) = tokio::sync::mpsc::channel::<u8>(1);
    let task = tokio::spawn(async move {
        let _held = sender;
        std::future::pending::<()>().await;
    });
    tokio::task::yield_now().await;
    task.abort();
    assert!(task.await.unwrap_err().is_cancelled());
    assert_eq!(receiver.recv().await, None);
}
