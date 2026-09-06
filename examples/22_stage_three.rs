#[tokio::main(flavor = "current_thread")]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let (tx, mut rx) = tokio::sync::mpsc::channel(2);
    let producer = tokio::spawn(async move {
        for line in ["INFO ready", "WARN retry", "ERROR stop"] {
            tx.send(String::from(line)).await?;
        }
        Ok::<_, tokio::sync::mpsc::error::SendError<String>>(())
    });
    let mut summary = audit_core::Summary::default();
    while let Some(line) = rx.recv().await {
        summary.record(&audit_core::parse(&line)?)?;
    }
    producer.await??;
    assert_eq!((summary.info, summary.warn, summary.error), (1, 1, 1));
    Ok(())
}
