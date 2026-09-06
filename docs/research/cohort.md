# Reference cohort · verified 2026-09-06

These are review perspectives grounded in public work, **not actual reviewers, quotations, or endorsements**. Current membership was checked rather than inferred from historical reputation.

| Perspective | Current evidence | Application |
|---|---|---|
| Niko Matsakis, Tyler Mandry | [Language team](https://rust-lang.org/governance/teams/lang/) lists both, Tyler as lead; 2026 roadmaps connect Niko to async/borrowing and Tyler to Beyond & | Ownership relationships, borrow precision, async separation, field projection context |
| Jack Huey, lcnr, Types Team | [team source](https://raw.githubusercontent.com/rust-lang/team/main/teams/types.toml) lists both as leads; members include Boxy, Rémy Rakic, Niko, Oli Scherer, Santiago Pastorino | Do not teach conservative trait/borrow analysis as an eternal language limit |
| Ralf Jung, operational semantics and Miri | [Language governance](https://rust-lang.org/governance/teams/lang/) lists opsem lead; [compiler governance](https://rust-lang.org/governance/teams/compiler/) lists Miri leads Ralf and Oli | Soundness argument, aliasing caveats, ZST and destruction tests |
| Mara Bos, Amanieu d'Antras | [Library team](https://rust-lang.org/governance/teams/library/) lists both, Amanieu as lead | Atomics vs synchronization, runtime/OS/hardware distinction, precise APIs |
| David Tolnay | Current Library and Library FCP membership; [thiserror](https://github.com/dtolnay/thiserror), [Serde](https://serde.rs/) | Error ergonomics and restrained dependency choices |
| Esteban Kuber and compiler maintainers | [Compiler team](https://rust-lang.org/governance/teams/compiler/) lists Esteban as maintainer and FCP member | Actual diagnostic capture and intended-code checking |
| Current Cargo Team | [Dev tools](https://rust-lang.org/governance/teams/dev-tools/): leads Jacob Finkelman, Weihang Lo; members Poe, Arlo Siemsen, Ed Page, Josh Triplett, Scott Schafer, Ross Sullivan | Current resolver, lints, feature graph, semver and packaging |
| Current Book Team | [Language governance](https://rust-lang.org/governance/teams/lang/): Carol Nichols and Chris Krycho, both leads | Values → ownership → borrowing → structs/lifetimes → concurrency, with progressive refinements |
| Alice Ryhl and Tokio maintainers | Alice is a current language advisor and library member; [her blocking article](https://ryhl.io/blog/async-what-is-blocking/) and Tokio docs | Cooperative scheduling, bounded messages, cancellation contracts |
| Andrew Gallant | Current Library FCP and regex team leadership | Concrete types and minimal abstractions; no performance folklore |
| Benno Lossin | [current field-projection design comparison](https://bennolossin.github.io/field-projections-designs/) linked by August Inside Rust update | Designs labeled active vs legacy; no unstable syntax in core |

The old design-meeting-minutes directory contains historical material, so it is not presented as current meeting evidence. Current language-team meeting guidance, current goal tracking, the August Inside Rust report, and the field-projection design comparison supplied the contemporary design context. The August report specifically superseded assumptions about two discontinued goals and a completed Cargo goal.
