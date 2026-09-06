extern "C" fn record_length(_bytes: *const u8, len: usize) -> usize {
    // This function never dereferences or retains the pointer.
    len
}
fn main() {
    let record = b"INFO ready";
    assert_eq!(record_length(record.as_ptr(), record.len()), 10);
}
