{"title":"Set up Rust","stage":1,"minutes":35,"summary":"Install Rust, find your way around a Cargo project, and run your first example.","example":"01_setup","headingIds":{"What you will build":"the-work-you-will-build"}}
---
## What you will build

You will build **Fieldnotes**, a command-line tool that reads event records and reports counts. A record looks like `WARN disk almost full`. The final tool accepts a file or standard input, reports malformed records with line numbers, rejects oversized records, and works without loading the entire file. Each stage makes a specific improvement to that program.

You need a terminal and a text editor, but no Rust experience. If you are new to programming, take your time with the next lesson: you will use functions, conditions, and loops throughout the course. Allow roughly 25–40 hours for reading and practice.

Read in sequence on your first pass. Run the example, predict the effect of a change, then try the exercise before opening its solution. Compiler drills are meant to fail. All other examples and checks should pass. Keep your exercise work on a local branch so you can compare it with the reference implementation.

## Install and locate the tools

Install Rust through [the official installer](https://rust-lang.org/tools/install/). On Windows, follow its instructions for the MSVC build tools; on macOS, a missing linker generally means the Xcode command-line tools are absent. Linux distributions may require their compiler/linker package. Use the installer instructions for your platform rather than copying a shell command you have not read.

Clone the [course repository](https://github.com/robertdevore/rust.robertdevore.com), enter it, and run:

```sh
git clone https://github.com/robertdevore/rust.robertdevore.com.git
cd rust.robertdevore.com
rustc --version
cargo --version
cargo run --locked --example 01_setup
```

The repository selects Rust **1.98.1**, edition **2024**, through `rust-toolchain.toml`. Rustup installs the pinned compiler if necessary. The edition selects the language compatibility rules for a package. The compiler version selects the program that compiles it. Choosing an edition does not freeze the standard library. This course does not change your global default toolchain.

## Read the project before editing

`Cargo.toml` describes a package and its dependencies. `Cargo.lock` records the dependency resolution we verified. `src/lib.rs` is the library target; `examples/` holds executable learning targets; `crates/` holds the final application and the isolated unsafe lab. `target/` is generated output and should not be committed.

`cargo check` type-checks quickly without producing a finished executable. `cargo build` creates one. `cargo run` builds and runs a selected target. `--locked` refuses to change dependency resolution, which makes an unexpected dependency update visible.

{{example}}

`fn main()` is the entry point. Braces enclose its body. `println!` is a macro; the exclamation mark distinguishes macro invocation from an ordinary function call. A semicolon ends this statement. You do not need to understand macro implementation to use this one.

## Exercise

Change the greeting, run it, then run `cargo check --workspace --all-targets --locked`. Explain why changing text should not change the lockfile. Create a separate scratch project using `cargo new first-record`; identify the files that Cargo created.

<details><summary>Solution and acceptance check</summary>

Any greeting is valid. The executable must print the new text once and exit successfully. The lockfile stays unchanged because source text is not dependency metadata. A new binary package has a manifest and `src/main.rs`; generated Git files depend on the surrounding repository and Cargo configuration. Never put the scratch project inside another workspace without understanding membership.

</details>

## Check your understanding

If the editor says a name is invalid but `cargo check` succeeds, check that rust-analyzer uses this repository's toolchain and workspace. Start with the compiler output: anyone using the same toolchain can check it. See [Cargo's first steps](https://doc.rust-lang.org/cargo/getting-started/first-steps.html) and the [Edition Guide](https://doc.rust-lang.org/edition-guide/editions/index.html).
