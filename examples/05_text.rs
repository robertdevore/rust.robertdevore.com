fn main() {
    let text = "café";
    assert_eq!(text.len(), 5);
    assert_eq!(text.chars().count(), 4);
    assert_eq!(text.get(..3), Some("caf"));
    assert_eq!(text.get(..4), None);
    let mut rows = vec![String::from("INFO ok")];
    rows.push("WARN retry".into());
    let sizes: Vec<_> = rows.iter().map(|row| row.len()).collect();
    assert_eq!(sizes, [7, 10]);
}
