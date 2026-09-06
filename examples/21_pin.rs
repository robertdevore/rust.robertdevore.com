use std::{future::Future, pin::Pin};
trait Lookup {
    fn get(&self) -> Pin<Box<dyn Future<Output = usize> + '_>>;
}
struct Fixed(usize);
impl Lookup for Fixed {
    fn get(&self) -> Pin<Box<dyn Future<Output = usize> + '_>> {
        Box::pin(async move { self.0 })
    }
}
#[tokio::main(flavor = "current_thread")]
async fn main() {
    let lookup = Fixed(42);
    let service: &dyn Lookup = &lookup;
    assert_eq!(service.get().await, 42);
}
