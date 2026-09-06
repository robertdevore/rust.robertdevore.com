# Before and after · 2026-09-06

Same 32 canonical URLs in both inventories; 28 lessons. Baseline commit `e4e66f64128455f17dc2d3258e7e3c6d221b2613` is sealed in raw/baseline-site.tar.gz; its SHA-256 and member hashes are in raw/baseline-seal.json. Report generation verifies the archive checksum. Original CSVs are preserved under raw/baseline/.

| Metric | Before | After |
|---|---:|---:|
| canonical_pages | 32 | 32 |
| indexable_pages | 32 | 32 |
| missing_titles | 0 | 0 |
| missing_descriptions | 0 | 0 |
| duplicate_titles | 0 | 0 |
| duplicate_descriptions | 0 | 0 |
| missing_canonicals | 0 | 0 |
| h1_problems | 0 | 0 |
| broken_internal_links | 0 | 0 |
| broken_external_destinations | 0 | 0 |
| indeterminate_external_destinations | 0 | 0 |
| orphans | 0 | 0 |
| deeper_than_three | 0 | 0 |
| schema_pages | 0 | 32 |
| schema_parse_errors | 0 | 0 |
| missing_author_metadata | 32 | 0 |
| missing_alt | 0 | 0 |
| missing_dimensions | 0 | 0 |
| external_destinations | 120 | 121 |
| assets_bytes | 486981 | 937291 |

P0: 0 → 0. P1: 0 → 0. No URL removed. All 32 page templates gain factual metadata/schema and bundled assets; 28 gain bylines, breadcrumbs and Markdown downloads. About/practice gain factual project information and a real source card. No lesson claims or Rust examples rewritten.

| Phase | Template | Performance /100 | LCP ms | TBT ms | CLS |
|---|---|---:|---:|---:|---:|
| baseline | home | 57 | 4131 | 1562 | 0 |
| baseline | lesson | 75 | 1710 | 1279 | 0 |
| after | home | 73 | 1750 | 1636 | 0.001526094530906357 |
| after | lesson | 72 | 1756 | 1896 | 0 |

One lab run per template/phase, default mobile simulation. Shared-host timing and CDN injections vary. These values do not demonstrate field CWV improvement, rank growth, or causal impact. Repository asset totals include new downloadable exports/cards and retained source assets; they are not page-load transfer size. See performance.csv for actual transferred resource totals.

Internal scores are deliberately omitted: partial access and heuristic weighting would add apparent precision. Concrete coverage and lab scores above are reproducible. Search ranking and AI citation before/after: NOT AVAILABLE — DATA ACCESS REQUIRED.
