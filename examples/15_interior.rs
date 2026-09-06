use std::{cell::RefCell, rc::Rc};
fn main() {
    let data = Rc::new(RefCell::new(vec![1]));
    let other = Rc::clone(&data);
    {
        let mut guard = other.borrow_mut();
        guard.push(2);
        assert!(data.try_borrow().is_err());
    }
    assert_eq!(*data.borrow(), [1, 2]);
    assert_eq!(Rc::strong_count(&data), 2);
}
