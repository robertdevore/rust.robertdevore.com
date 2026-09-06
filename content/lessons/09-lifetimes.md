{"title":"Lifetimes describe relationships","stage":2,"minutes":55,"summary":"Connect borrowed results to their inputs without trying to extend the life of data.","example":"09_lifetimes","drill":"dangling"}
---
## A borrowed result needs a source

Our parser returns a message slice inside its input. The return value does not own the message bytes. You can use the slice only while the input remains valid. A lifetime annotation expresses a relationship between borrows; it does not allocate storage, keep an owner alive, or change how long a local variable exists.

{{example}}

`message` needs no written lifetime parameter because the elision rules connect its single borrowed input to its borrowed output. `choose` has two possible sources, so its signature gives both inputs and the output a named relationship. At a call, the compiler can select a duration over which both inputs are valid. It does not require their owners to have identical scopes.

The function's implementation still has to meet its signature. Adding `'static` to a return type cannot keep a local string alive. The compiler rejects returning a reference to the local allocation that will be dropped at function exit.

## References inside structs

`Event<'a>` stores `&'a str`. The struct is useful while the input borrow is valid. If events need to be stored after reusing the input buffer, choose owned text or a representation with an owner that remains alive. Decide whether the data should be borrowed before adding lifetime parameters.

A `'static` bound on a type means the type does not contain borrows that expire sooner; it does not mean a value must live forever. An owned `String` can satisfy such a bound and still be dropped at the end of a short task. A `&'static str` specifically refers to text valid for the program's duration, such as a string literal.

Variance and higher-ranked bounds become relevant when you build more sophisticated generic interfaces. For now, identify the owner of each value and the source of each returned reference. This often reveals the problem before you write a lifetime annotation.

## Compiler drill

{{drill}}

Repair it by returning an owned `String`, or by taking text from a caller and returning a view of that text. Choose based on which part of the program should own the text. Leaking the string to obtain a static reference is not an ordinary parser design.

## Exercise

Write a function that returns the part before the first space as `Option<&str>`. Test no separator, a leading space, and a normal record. Then explain why returning this view from a temporary input string to a longer-lived caller must be rejected.

<details><summary>Solution and acceptance check</summary>

Use `line.split_once(' ').map(|(level, _)| level)`. No separator gives `None`; a leading space gives an empty slice; `INFO ready` gives `Some("INFO")`. The empty slice is a parsing choice to validate later. The returned reference cannot remain usable after the input allocation is dropped, and annotations cannot change that fact.

</details>

Sources: [lifetime elision](https://doc.rust-lang.org/reference/lifetime-elision.html), [trait and lifetime bounds](https://doc.rust-lang.org/reference/trait-bounds.html), and [lifetime syntax](https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html).
