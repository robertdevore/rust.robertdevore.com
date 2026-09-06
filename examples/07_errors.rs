fn main() -> Result<(), Box<dyn std::error::Error>> {
    let event = audit_core::parse("WARN retry")?;
    assert_eq!(event.message, "retry");
    assert!(audit_core::parse("???").is_err());
    Ok(())
}
