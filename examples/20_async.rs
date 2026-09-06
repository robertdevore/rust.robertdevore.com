#[tokio::main(flavor = "current_thread")]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let (sender, mut receiver) = tokio::sync::mpsc::channel(2);
    let producer = tokio::spawn(async move {
        for id in 0..4 {
            sender.send(id).await?;
        }
        Ok::<(), tokio::sync::mpsc::error::SendError<i32>>(())
    });
    let mut sum = 0;
    while let Some(id) = receiver.recv().await {
        sum += id;
    }
    producer.await??;
    assert_eq!(sum, 6);
    Ok(())
}
