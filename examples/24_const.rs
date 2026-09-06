fn first<const N: usize>(values: &[u8; N]) -> Option<u8> {
    values.first().copied()
}
fn main() {
    assert_eq!(first(&[3, 4]), Some(3));
    assert_eq!(first(&[]), None);
}
