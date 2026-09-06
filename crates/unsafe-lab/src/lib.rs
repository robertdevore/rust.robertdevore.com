//! Study-only unsafe boundary. In application code prefer `slice::split_at_mut`.
/// Split at a checked index, preserving exclusive access to disjoint elements.
///
/// Panics if `mid > slice.len()`. Safe callers have no extra obligations.
pub fn split<T>(slice: &mut [T], mid: usize) -> (&mut [T], &mut [T]) {
    let len = slice.len();
    assert!(mid <= len, "split index exceeds length");
    let ptr = slice.as_mut_ptr();
    // SAFETY: ptr comes from a valid exclusive slice. mid <= len keeps the
    // offset in the allocation or one-past. Both ranges contain initialized T,
    // are aligned/non-null even when empty, and partition the original range.
    // Returned lifetimes are tied to slice; the original borrow cannot be used
    // while these reborrows are live. ZSTs have disjoint logical elements even
    // when their addresses coincide. No ownership or destructor is duplicated.
    unsafe {
        (
            std::slice::from_raw_parts_mut(ptr, mid),
            std::slice::from_raw_parts_mut(ptr.add(mid), len - mid),
        )
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn partitions() {
        for mid in 0..=4 {
            let mut data = [0; 4];
            let (a, b) = split(&mut data, mid);
            a.fill(1);
            b.fill(2);
            assert_eq!(data[..mid], vec![1; mid]);
            assert_eq!(data[mid..], vec![2; 4 - mid]);
        }
    }
    #[test]
    fn empty_and_zst() {
        let mut empty: [u8; 0] = [];
        assert!(split(&mut empty, 0).0.is_empty());
        let mut z = [(); 4];
        let (a, b) = split(&mut z, 2);
        assert_eq!((a.len(), b.len()), (2, 2));
    }
    #[test]
    fn drops_once() {
        use std::rc::Rc;
        let token = Rc::new(());
        {
            let mut data = [token.clone(), token.clone()];
            let (a, b) = split(&mut data, 1);
            std::mem::swap(&mut a[0], &mut b[0]);
        }
        assert_eq!(Rc::strong_count(&token), 1);
    }
    #[test]
    #[should_panic(expected = "split index exceeds length")]
    fn rejects_oob() {
        split(&mut [1], 2);
    }
}
