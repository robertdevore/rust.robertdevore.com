#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
cargo fmt --all -- --check
cargo check --workspace --all-targets --locked
cargo test --workspace --locked
cargo clippy --workspace --all-targets --locked -- -D warnings
for example in examples/*.rs; do
  cargo run --quiet --locked --example "$(basename "$example" .rs)"
done
node scripts/drills.mjs
cargo build --locked -p audit-cli
node scripts/test-cli.mjs
