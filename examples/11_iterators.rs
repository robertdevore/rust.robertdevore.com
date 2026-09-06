fn main() {
    let rows = ["INFO a", "WARN b", "WARN c"];
    let warnings: Vec<_> = rows
        .iter()
        .copied()
        .filter(|row| row.starts_with("WARN "))
        .collect();
    assert_eq!(warnings, ["WARN b", "WARN c"]);
    let parsed: Result<Vec<_>, _> = rows.iter().map(|row| audit_core::parse(row)).collect();
    assert_eq!(parsed.unwrap().len(), 3);
}
