use std::{
    future::Future,
    pin::Pin,
    task::{Context, Poll, Waker},
};
fn main() {
    let mut future = std::pin::pin!(async { 21 * 2 });
    let mut context = Context::from_waker(Waker::noop());
    assert_eq!(Pin::as_mut(&mut future).poll(&mut context), Poll::Ready(42));
}
