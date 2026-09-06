## What this course teaches

Learn how ownership, borrowing, and lifetimes fit together, then use them to build a command-line tool. The course starts with the basics and works up to concurrency and unsafe code. It is a practical introduction, not a reference to every Rust feature.

The 28 lessons include 25 runnable examples, six compiler drills, three stage builds, and a final tool you can install. Each lesson has an exercise, checks for your answer, and a solution. Allow roughly 25–40 hours with practice, depending on your background. The time shown on each lesson is an estimate.

## Technical freshness

**Verified September 6, 2026. Rust 1.98.1. Edition 2024.** The repository pins the compiler so you can reproduce its code and diagnostics. Only the separate Miri checks for the unsafe lab use nightly Rust.

The [evidence ledger](https://github.com/robertdevore/rust.robertdevore.com/blob/main/docs/research/ledger.md) records sources, dates, recommendations, and affected lessons. The [horizon lesson](/course/25-horizon/) explains which features are stable and which are still in development.

Sources include the Rust Reference, Cargo and standard-library documentation, Rust Project Goals, governance pages, compiler and language-team material, and documentation from library maintainers. The Rust Book guides the order of concepts and terminology. The explanations and project are original to this course.

## How we check the examples

The site inserts lesson code from the same Rust files that our checks compile. Compiler drills include actual rustc diagnostics, and tests check that they fail with the expected error code. The capstone tests malformed input, record limits, UTF-8 boundaries, I/O errors, and overflow. The unsafe lab has a written safety argument and Miri checks.

Formatting, Clippy, tests, and compiler checks help catch mistakes. They cannot prove every concurrent algorithm or unsafe program correct. We use maintainers' public work as references; we do not claim they reviewed or endorsed this course.

## Your progress and privacy

Lesson completion is saved in this browser's local storage. It does not sync across devices, and the course does not send it to analytics. Search also runs in your browser using the site's lesson index.

We measure traffic with Cloudflare Web Analytics and Google Analytics through Cloudflare Zaraz. These services process visit and browser information; Google Analytics may use cookies. The course has no accounts and loads fonts locally. Hosting providers also process request logs.

Clear your saved lesson progress here:

<button type="button" class="button secondary" id="reset-progress">Reset local progress</button>
<p id="reset-status" role="status"></p>

## Source and contributions

Read the [source repository](https://github.com/robertdevore/rust.robertdevore.com), run its checks, or [report a correction](https://github.com/robertdevore/rust.robertdevore.com/issues). Include the lesson URL, compiler version, and a small example that shows the problem when possible.

The code and original course text use the MIT license. Cited third-party material keeps its own terms.

## Author

[Robert DeVore](https://robertdevore.com) created and maintains this course. It is an independent project, not an official Rust Project publication.

## Portable course text

Download any lesson as Markdown, including its explanations, source code, exercises, and compiler diagnostics. The [course index](https://rust.robertdevore.com/course-index.json) links each page to its download. The [complete text](https://rust.robertdevore.com/llms-full.txt) is also available for offline study or retrieval tools. Both exports come from the same lesson source as the website.
