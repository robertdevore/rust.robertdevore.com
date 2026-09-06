trait Fetch { async fn get(&self) -> usize; }
fn consume(_: &dyn Fetch) {}
fn main() {}
