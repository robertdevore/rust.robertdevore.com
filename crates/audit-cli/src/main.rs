use std::{
    env,
    fs::File,
    io::{self, BufReader, Write},
    process::ExitCode,
};
fn run() -> Result<(), Box<dyn std::error::Error>> {
    let mut args = env::args_os().skip(1);
    let path = args.next().ok_or("usage: audit-cli <file|->")?;
    if args.next().is_some() {
        return Err("usage: audit-cli <file|->".into());
    }
    let summary = if path == "-" {
        audit_core::summarize(io::stdin().lock())?
    } else {
        audit_core::summarize(BufReader::new(File::open(path)?))?
    };
    writeln!(
        io::stdout().lock(),
        "INFO={} WARN={} ERROR={}",
        summary.info,
        summary.warn,
        summary.error
    )?;
    Ok(())
}
fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(e) => {
            let _ = writeln!(io::stderr().lock(), "audit: {e}");
            ExitCode::FAILURE
        }
    }
}
