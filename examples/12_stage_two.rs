use std::io::Cursor;
fn main() -> Result<(), audit_core::AuditError> {
    let summary = audit_core::summarize(Cursor::new("INFO started\nWARN retry\nERROR stopped\n"))?;
    assert_eq!((summary.info, summary.warn, summary.error), (1, 1, 1));
    println!("{summary:?}");
    Ok(())
}
