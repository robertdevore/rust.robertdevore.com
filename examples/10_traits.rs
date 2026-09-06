use std::io::{self, Write};
fn report(mut destination: impl Write, count: usize) -> io::Result<()> {
    writeln!(destination, "records={count}")
}
fn main() -> io::Result<()> {
    let mut buffer = Vec::new();
    report(&mut buffer, 3)?;
    assert_eq!(buffer, b"records=3\n");
    let erased: &mut dyn Write = &mut buffer;
    report(erased, 4)?;
    assert!(buffer.ends_with(b"records=4\n"));
    Ok(())
}
