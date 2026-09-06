fn main() {
    let value = std::rc::Rc::new(1);
    std::thread::spawn(move || println!("{value}"));
}
