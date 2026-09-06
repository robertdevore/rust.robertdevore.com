fn main() {
    for capacity in 1..=16 {
        let input = std::io::BufReader::with_capacity(
            capacity,
            std::io::Cursor::new("INFO café\nWARN retry"),
        );
        let got = audit_core::summarize(input).unwrap();
        assert_eq!((got.info, got.warn), (1, 1));
    }
    assert!(audit_core::parse("WARN ").is_err());
}
