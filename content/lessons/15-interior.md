{"title":"Interior mutability and shared ownership","stage":3,"minutes":50,"summary":"Choose between reference counting, runtime borrow checks, and locks.","example":"15_interior"}
---
## Shared does not always mean unchanging

Ordinary data behind `&T` cannot be mutated while the shared reference's contract applies. Interior-mutability types let you change data through a shared reference under defined rules. They rely on `UnsafeCell` internally, but each safe abstraction supplies its own rules. `UnsafeCell` itself does not prevent data races or allow competing `&mut` references.

{{example}}

`Rc` gives two owning handles to the same allocation. `RefCell` tracks borrows at runtime. While the mutable guard exists, `try_borrow()` reports a conflict. After that guard is dropped, the shared borrow succeeds. Leaving the block drops the guard and ends its borrow.

`borrow()` and `borrow_mut()` panic on a runtime conflict; their `try_` variants return an error. Use the `try_` variants when your program should handle a borrow conflict rather than panic. A runtime check does not mean the compiler has stopped enforcing all safety: the guard types and library implementation cooperate to preserve access rules.

## Pick the narrowest mechanism

`Cell<T>` can replace a value without handing out ordinary references to its interior. `RefCell<T>` supports checked borrows within a thread. `Mutex<T>` coordinates access across threads. `Rc<T>` is not a thread-safe reference counter; `Arc<T>` is, but that does not make every `T` thread-safe. `Arc<RefCell<T>>` is not a substitute for a synchronized mutation abstraction.

Reference-counted cycles can leak memory. Use weak references or redesign ownership where a graph needs back-links. A leak is a resource bug even when it does not violate memory safety. Rust's safety model does not imply every resource is eventually reclaimed.

## Apply this to the course project

The event counter owns its summary and reads records sequentially. It does not need a reference-counted mutable summary. Passing `&mut Summary` to a function already states the intended exclusive update. Add a cell or lock only when a real relationship requires shared access with mutation.

If a compiler error appears because two components both want ownership, first consider transferring ownership at a message boundary. If they only read immutable data, an ordinary borrow or `Arc<T>` may be enough. Each mechanism adds behavior you need to understand and test.

## Exercise

Keep the mutable `RefCell` guard alive and call `try_borrow` from the other handle. Assert failure. Drop the guard explicitly and assert success. Explain why cloning the `Rc` does not create a second vector.

<details><summary>Solution and acceptance check</summary>

The first attempt returns `Err`; the second sees `[1, 2]`. Both handles refer to the same cell and its borrow state. `Rc::clone` increases the owning handle count. To copy the data itself, you would need to clone the vector separately.

</details>

Sources: [`RefCell`](https://doc.rust-lang.org/std/cell/struct.RefCell.html), [`UnsafeCell`](https://doc.rust-lang.org/std/cell/struct.UnsafeCell.html), and [`Rc`](https://doc.rust-lang.org/std/rc/).
