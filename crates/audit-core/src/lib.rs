//! A bounded, line-oriented event summarizer. No filesystem or runtime dependency.
use std::{fmt, io::BufRead};

/// The largest accepted record, including its newline when present.
pub const MAX_LINE_BYTES: usize = 4096;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Level {
    Info,
    Warn,
    Error,
}

/// Borrows its message; the input buffer must remain alive while this value is used.
#[derive(Debug, PartialEq, Eq)]
pub struct Event<'a> {
    pub level: Level,
    pub message: &'a str,
}

#[derive(Debug, PartialEq, Eq)]
pub enum ParseError {
    MissingSeparator,
    UnknownLevel,
    EmptyMessage,
}
impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(match self {
            Self::MissingSeparator => "expected LEVEL message",
            Self::UnknownLevel => "expected INFO, WARN, or ERROR",
            Self::EmptyMessage => "message is empty",
        })
    }
}
impl std::error::Error for ParseError {}

/// Parse one record. Accepts CRLF/LF terminators; preserves message whitespace.
///
/// ```
/// use audit_core::{parse, Level};
/// let event = parse("WARN disk almost full\n").unwrap();
/// assert_eq!(event.level, Level::Warn);
/// assert_eq!(event.message, "disk almost full");
/// ```
pub fn parse(line: &str) -> Result<Event<'_>, ParseError> {
    let line = line.strip_suffix('\n').unwrap_or(line);
    let line = line.strip_suffix('\r').unwrap_or(line);
    let (level, message) = line.split_once(' ').ok_or(ParseError::MissingSeparator)?;
    let level = match level {
        "INFO" => Level::Info,
        "WARN" => Level::Warn,
        "ERROR" => Level::Error,
        _ => return Err(ParseError::UnknownLevel),
    };
    if message.trim().is_empty() {
        return Err(ParseError::EmptyMessage);
    }
    Ok(Event { level, message })
}

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub struct Summary {
    pub info: u64,
    pub warn: u64,
    pub error: u64,
}
impl Summary {
    pub fn record(&mut self, event: &Event<'_>) -> Result<(), AuditError> {
        let counter = match event.level {
            Level::Info => &mut self.info,
            Level::Warn => &mut self.warn,
            Level::Error => &mut self.error,
        };
        *counter = counter.checked_add(1).ok_or(AuditError::CountOverflow)?;
        Ok(())
    }
}

#[derive(Debug)]
pub enum AuditError {
    Io(std::io::Error),
    InvalidRecord { line: u64, source: ParseError },
    LineTooLong { line: u64 },
    InvalidUtf8 { line: u64 },
    CountOverflow,
}
impl fmt::Display for AuditError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Io(e) => write!(f, "input error: {e}"),
            Self::InvalidRecord { line, source } => write!(f, "line {line}: {source}"),
            Self::LineTooLong { line } => write!(f, "line {line}: exceeds {MAX_LINE_BYTES} bytes"),
            Self::InvalidUtf8 { line } => write!(f, "line {line}: invalid UTF-8"),
            Self::CountOverflow => f.write_str("record count overflow"),
        }
    }
}
impl std::error::Error for AuditError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Io(e) => Some(e),
            Self::InvalidRecord { source, .. } => Some(source),
            _ => None,
        }
    }
}
impl From<std::io::Error> for AuditError {
    fn from(e: std::io::Error) -> Self {
        Self::Io(e)
    }
}

/// Summarize records with bounded retained line storage; fail at the first bad record.
/// Empty input succeeds. No partial summary is returned on failure.
pub fn summarize(mut reader: impl BufRead) -> Result<Summary, AuditError> {
    let mut summary = Summary::default();
    let mut bytes = Vec::with_capacity(MAX_LINE_BYTES);
    let mut number = 1u64;
    loop {
        let buffer = reader.fill_buf()?;
        if buffer.is_empty() {
            break;
        }
        let end = buffer
            .iter()
            .position(|b| *b == b'\n')
            .map_or(buffer.len(), |i| i + 1);
        if end > MAX_LINE_BYTES - bytes.len() {
            return Err(AuditError::LineTooLong { line: number });
        }
        bytes.extend_from_slice(&buffer[..end]);
        let complete = buffer[end - 1] == b'\n';
        reader.consume(end);
        if complete {
            record_bytes(&bytes, number, &mut summary)?;
            bytes.clear();
            number = number.checked_add(1).ok_or(AuditError::CountOverflow)?;
        }
    }
    if !bytes.is_empty() {
        record_bytes(&bytes, number, &mut summary)?;
    }
    Ok(summary)
}
fn record_bytes(bytes: &[u8], line: u64, summary: &mut Summary) -> Result<(), AuditError> {
    let text = std::str::from_utf8(bytes).map_err(|_| AuditError::InvalidUtf8 { line })?;
    let event = parse(text).map_err(|source| AuditError::InvalidRecord { line, source })?;
    summary.record(&event)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::{BufReader, Cursor};
    #[test]
    fn levels_and_borrowing() {
        let input = String::from("INFO café\n");
        assert_eq!(
            parse(&input).unwrap(),
            Event {
                level: Level::Info,
                message: "café"
            }
        );
        assert_eq!(parse("WARN x\r\n").unwrap().level, Level::Warn);
        assert_eq!(parse("ERROR x").unwrap().level, Level::Error);
    }
    #[test]
    fn rejects_invalid() {
        assert_eq!(parse("INFO"), Err(ParseError::MissingSeparator));
        assert_eq!(parse("info x"), Err(ParseError::UnknownLevel));
        assert_eq!(parse("INFO  "), Err(ParseError::EmptyMessage));
    }
    #[test]
    fn chunks_and_final_line() {
        for capacity in 1..16 {
            let reader = BufReader::with_capacity(
                capacity,
                Cursor::new(b"INFO a\r\nWARN caf\xc3\xa9\nERROR c"),
            );
            assert_eq!(
                summarize(reader).unwrap(),
                Summary {
                    info: 1,
                    warn: 1,
                    error: 1
                }
            );
        }
        assert_eq!(summarize(Cursor::new(b"")).unwrap(), Summary::default());
    }
    #[test]
    fn bounds_and_line_numbers() {
        let exact = format!("INFO {}\n", "a".repeat(MAX_LINE_BYTES - 6));
        assert_eq!(summarize(Cursor::new(exact)).unwrap().info, 1);
        let huge = format!("INFO {}", "a".repeat(MAX_LINE_BYTES));
        assert!(matches!(
            summarize(Cursor::new(huge)),
            Err(AuditError::LineTooLong { line: 1 })
        ));
        assert!(matches!(
            summarize(Cursor::new(b"INFO a\nBAD b\n")),
            Err(AuditError::InvalidRecord { line: 2, .. })
        ));
        assert!(matches!(
            summarize(Cursor::new(b"INFO \xff")),
            Err(AuditError::InvalidUtf8 { line: 1 })
        ));
    }
    #[test]
    fn overflow_is_explicit() {
        let mut summary = Summary {
            info: u64::MAX,
            ..Summary::default()
        };
        assert!(matches!(
            summary.record(&Event {
                level: Level::Info,
                message: "x"
            }),
            Err(AuditError::CountOverflow)
        ));
    }
    #[test]
    fn preserves_io_failure() {
        struct Broken;
        impl std::io::Read for Broken {
            fn read(&mut self, _: &mut [u8]) -> std::io::Result<usize> {
                Err(std::io::Error::other("fixture"))
            }
        }
        assert!(matches!(
            summarize(BufReader::new(Broken)),
            Err(AuditError::Io(_))
        ));
    }
}
