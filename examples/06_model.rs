#[derive(Debug, PartialEq, Eq)]
enum Job {
    Queued,
    Running { attempt: u32 },
    Finished { bytes: usize },
}
fn describe(job: &Job) -> String {
    match job {
        Job::Queued => "queued".into(),
        Job::Running { attempt } => format!("attempt {attempt}"),
        Job::Finished { bytes } => format!("{bytes} bytes"),
    }
}
fn main() {
    assert_eq!(describe(&Job::Queued), "queued");
    assert_eq!(describe(&Job::Running { attempt: 2 }), "attempt 2");
    assert_eq!(describe(&Job::Finished { bytes: 8 }), "8 bytes");
}
