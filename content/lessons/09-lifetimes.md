{"title":"Lifetimes describe relationships","stage":2,"minutes":55,"summary":"Design borrowed results without pretending annotations extend storage.","example":"09_lifetimes","drill":"dangling"}
---
## A borrowed result needs a source

Our parser returns a message slice inside its input. The return value does not own the message bytes. Its validity therefore depends on the input remaining available. A lifetime annotation expresses a relationship between borrows; it does not allocate storage, keep an owner alive, or change how long a local variable exists.

{{example}}

`message` needs no written lifetime parameter because the elision rules connect its single borrowed input to its borrowed output. `choose` has two possible sources, so its signature gives both inputs and the output a named relationship. At a call, the compiler can select a duration over which both inputs are valid. It does not require their owners to have identical scopes.

The function's implementation still has to meet its signature. Writing `'static` on a return type cannot make a local string immortal. The compiler rejects returning a reference to the local allocation that will be dropped at function exit.

## References inside structs

`Event<'a>` stores `&'a str`. The struct is useful while the input borrow is valid. If events need to be stored after reusing the input buffer, choose owned text or a representation with an owner that remains alive. Do not scatter lifetimes over a data model before deciding whether borrowing is appropriate for its actual usage.

A `'static` bound on a type means the type does not contain borrows that expire sooner; it does not mean a value must live forever. An owned `String` can satisfy such a bound and still be dropped at the end of a short task. A `&'static str` specifically refers to text valid for the program's duration, such as a string literal.

Variance and higher-ranked bounds become relevant when you build more sophisticated generic interfaces. For now, explain an API by naming the owner and the places from which every returned reference can originate. This catches many errors before annotations enter the conversation.

## Compiler drill

{{drill}}

Repair it by returning an owned `String`, or by taking text from a caller and returning a view of that text. Choose based on where ownership should reside. Leaking the string to obtain a static reference is not an ordinary parser design.

## Exercise

Write a function that returns the part before the first space as `Option<&str>`. Test no separator, a leading space, and a normal record. Then explain why returning this view from a temporary input string to a longer-lived caller must be rejected.

<details><summary>Solution and acceptance check</summary>

Use `line.split_once(' ').map(|(level, _)| level)`. No separator gives `None`; a leading space gives an empty slice; `INFO ready` gives `Some("INFO")`. The empty slice is a parsing choice to validate later. The returned reference cannot remain usable after the input allocation is dropped, and annotations cannot change that fact.

</details>

Sources: [lifetime elision](https://doc.rust-lang.org/reference/lifetime-elision.html), [trait and lifetime bounds](https://doc.rust-lang.org/reference/trait-bounds.html), and [lifetime syntax](https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html).
