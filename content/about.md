## What this course teaches

Rust becomes easier to work with when ownership, borrowing, and lifetimes form one coherent model. This course builds that model in small steps, then uses it to design a real command-line application. It covers foundations through practical systems boundaries; it is not an exhaustive reference to every language feature or a promise of mastery after one reading.

The 28 lessons include 25 executable examples, six compiler drills, three stage builds, and a final installable capstone. Each lesson has an exercise with acceptance criteria and a solution. Plan for roughly 25–40 hours including practice, depending on your background. Lesson times are planning estimates.

## Technical freshness

**Verified September 6, 2026. Rust 1.98.1. Edition 2024.** The compiler is pinned so code and diagnostic snapshots can be reproduced. Nightly is used separately for Miri checks of the unsafe lab, not for the production curriculum.

The [evidence ledger](https://github.com/robertdevore/rust.robertdevore.com/blob/main/docs/research/ledger.md) records authoritative sources, current recommendations, feature status, dates, and affected lessons. The [horizon lesson](/course/25-horizon/) separates stable capabilities from active design work.

Sources include the Rust Reference, Cargo documentation, standard-library contracts, current Rust Project Goals, governance pages, compiler and language-team material, and maintainer-authored ecosystem documentation. The Rust Book informs concept ordering and terminology; this course uses its own explanations and project.

## How the examples stay honest

Lesson code is inserted from the same Rust files that verification compiles. Intentionally failing programs have captured rustc diagnostics and checks for the expected error code. The capstone tests malformed input, record limits, UTF-8 boundaries, I/O failure, and overflow. The isolated unsafe lab has a written invariant argument and Miri checks.

Formatting, Clippy, tests, and compiler checks complement human review. They do not prove that all concurrent algorithms or unsafe programs are correct. Named maintainers provide useful reference perspectives through their public work; none is claimed to have reviewed or endorsed this course.

## Your progress and privacy

Marking a lesson complete saves its identifier in local storage on this browser. Progress does not sync across devices. Search runs locally using the site's generated index. Traffic is measured through Cloudflare Web Analytics and the site's Cloudflare Zaraz integration with Google Analytics. These services process visit and browser information; the Google integration may use cookies. Lesson completion stays in your browser and is not sent by the course to analytics. The course has no account service or third-party font requests. Hosting providers also process ordinary request logs.

You can clear your lesson progress here:

<button type="button" class="button secondary" id="reset-progress">Reset local progress</button>
<p id="reset-status" role="status"></p>

## Source and contributions

Read the [source repository](https://github.com/robertdevore/rust.robertdevore.com), run its checks, and submit a focused correction with a reproducible example. Include the compiler version when reporting a diagnostic difference. Code and original course text are MIT licensed; cited third-party material remains under its own terms.

Created by [Robert DeVore](https://robertdevore.com). This is an independent educational project, not an official Rust Project publication.

## Author

Robert DeVore maintains this independent course. The [source repository](https://github.com/robertdevore/rust.robertdevore.com) contains the original lesson text, runnable examples, tests, and research ledger. [Report a correction](https://github.com/robertdevore/rust.robertdevore.com/issues) with the lesson URL, toolchain version, and a small reproducer where applicable.

## Portable course text

Each lesson provides a Markdown download containing its explanations, included source, exercises, and compiler diagnostics. The [course index](https://rust.robertdevore.com/course-index.json) links canonical pages to those downloads; the [complete text](https://rust.robertdevore.com/llms-full.txt) is available for offline study or retrieval tools. These are read-only exports of the same course, not a separate source of technical truth.
