fn main() {
    let input = "INFO started\nWARN retry\nERROR stopped";
    let mut counts = [0u32; 3];
    for line in input.lines() {
        match line.split_once(' ') {
            Some(("INFO", _)) => counts[0] += 1,
            Some(("WARN", _)) => counts[1] += 1,
            Some(("ERROR", _)) => counts[2] += 1,
            _ => panic!("invalid built-in fixture"),
        }
    }
    assert_eq!(counts, [1, 1, 1]);
    println!("{counts:?}");
}
