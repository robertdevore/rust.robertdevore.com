{"title":"Stage build: the first event counter","stage":1,"minutes":70,"summary":"Combine control flow and borrowed text into a small working program.","example":"08_stage_one"}
---
## Build brief

Write a program that counts the three event levels in a fixed, trusted multiline string. Print the counts in INFO, WARN, ERROR order. This stage is deliberately small: you should be able to explain every line without hiding the algorithm behind a framework.

Before reading the reference, write down the input, the output, and the boundary cases. Our fixture has exactly three records. A production parser is not required yet, but an unknown level must not be accidentally counted as INFO.

{{example}}

## Walk through the state

The input is borrowed static text. `lines()` gives views into it, so the loop does not need to allocate one string per record. The array stores three counters. `split_once(' ')` separates the first token from the rest. The match increments one count or panics on an invalid built-in fixture.

The panic is acceptable only because the input is part of this test-like example and a malformed fixture is a programmer mistake. Do not copy that policy into a tool that reads user files. Stage two replaces it with a typed error and a bounded reader.

Counters are `u32` here because the fixture is tiny. That does not establish a production overflow policy. The completed library uses checked `u64` counts. Labeling those differences matters: a small teaching example can simplify an assumption without claiming the assumption holds for arbitrary inputs.

## Acceptance criteria

1. The original fixture prints `[1, 1, 1]` and its assertion passes.
2. Adding a second WARN line changes only the middle count.
3. An unknown level is visibly rejected.
4. The parser does not clone the full input or individual records.
5. You can identify the lifetime of the input and of each line view.

## Exercise

Start from a blank example file and rebuild the counter. Add an empty-input case and repeated levels. Then replace array positions with a local struct containing `info`, `warn`, and `error`. Explain whether the names improve reviewability enough to justify the extra definition.

<details><summary>Solution and acceptance check</summary>

Initialize every count to zero before iterating. Empty input visits no records and keeps the counts zero. Each level updates exactly one field. A struct avoids remembering what index 1 means; for an interface used by several functions, that clarity usually wins. Compare with `Summary` in the capstone core after finishing your version.

</details>

## Review before moving on

Can your program distinguish an empty file from a blank record? `lines()` handles line terminators but a blank line within the input is still a record with no level. Decide whether it should be rejected. Can a level contain spaces? Our format says no. Can a message contain spaces? Yes: splitting once preserves the remainder.

This is also a good moment to practice a meaningful commit: include the working stage and its tests, and describe the behavior it adds. Generated binaries and your entire `target` directory do not belong in history. The reference source remains available through the repository if an experiment goes wrong.

Read the contracts for [`str::lines`](https://doc.rust-lang.org/std/primitive.str.html#method.lines) and [`split_once`](https://doc.rust-lang.org/std/primitive.str.html#method.split_once) to check your assumptions.
