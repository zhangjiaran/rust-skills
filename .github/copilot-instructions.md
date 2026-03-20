# GitHub Copilot Instructions for Rust Development

This repository provides general-purpose skills for Rust development. When assisting with Rust projects, follow the guidelines below.

## General Principles

- Always prefer safe Rust over unsafe code unless performance or FFI requirements demand it.
- Follow Rust idioms: use `Option`/`Result` for error handling, leverage iterators, and favor ownership patterns.
- Use `cargo` as the primary build and package management tool.
- Format code with `rustfmt` and lint with `clippy` before committing.

## Rust Installation

When a user needs to install Rust:

```bash
# Install rustup (the Rust toolchain installer)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Add to PATH (or restart shell)
source "$HOME/.cargo/env"

# Verify installation
rustc --version
cargo --version

# Install a specific toolchain
rustup install stable           # Latest stable
rustup install nightly          # Nightly build
rustup install 1.75.0           # Specific version

# Set default toolchain
rustup default stable

# Add compilation targets (e.g., cross-compilation)
rustup target add wasm32-unknown-unknown
rustup target add x86_64-unknown-linux-musl

# Add useful components
rustup component add rustfmt    # Code formatter
rustup component add clippy     # Linter
rustup component add rust-src   # Source code for IDE support
```

## Project Creation & Development

When creating new Rust projects:

```bash
# Create a new binary project
cargo new my-app

# Create a new library project
cargo new my-lib --lib

# Initialize in an existing directory
cargo init

# Build the project
cargo build             # Debug build
cargo build --release   # Optimized release build

# Run the project
cargo run
cargo run --release

# Check for errors without producing a binary (faster)
cargo check
```

## Unit Testing

When writing or running Rust tests:

```bash
# Run all tests
cargo test

# Run tests with output shown
cargo test -- --nocapture

# Run a specific test by name
cargo test test_function_name

# Run tests in a specific module
cargo test module_name::

# Run doc tests only
cargo test --doc

# Run tests in release mode
cargo test --release

# Run tests with multiple threads control
cargo test -- --test-threads=1
```

Test code structure:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        assert_eq!(2 + 2, 4);
    }

    #[test]
    #[should_panic(expected = "overflow")]
    fn test_panic() {
        panic!("overflow");
    }
}
```

## Code Checking & Linting

When checking Rust code quality:

```bash
# Format code
cargo fmt                       # Format all files
cargo fmt -- --check            # Check formatting without modifying

# Run Clippy linter
cargo clippy                    # Basic lint check
cargo clippy -- -D warnings     # Treat warnings as errors
cargo clippy --all-targets      # Lint all targets including tests
cargo clippy --fix              # Auto-fix lint suggestions

# Audit dependencies for security vulnerabilities
cargo audit                     # Requires: cargo install cargo-audit

# Check for unused dependencies
cargo udeps                     # Requires: cargo install cargo-udeps
```

## Cargo Build & Dependencies

When managing Cargo builds and dependencies:

```bash
# Add a dependency
cargo add serde                         # Latest version
cargo add serde --features derive       # With features
cargo add tokio --features full         # Async runtime

# Remove a dependency
cargo remove serde

# Update dependencies
cargo update                    # Update all
cargo update serde              # Update specific crate

# Build with features
cargo build --features "feature1,feature2"
cargo build --no-default-features

# Generate documentation
cargo doc
cargo doc --open                # Open in browser
cargo doc --no-deps             # Only document this crate

# Publish to crates.io
cargo publish --dry-run         # Verify before publishing
cargo publish

# Show dependency tree
cargo tree
cargo tree --duplicates         # Show duplicate dependencies

# Clean build artifacts
cargo clean
```

## Workspace Management

For multi-crate projects:

```toml
# Cargo.toml (workspace root)
[workspace]
members = [
    "crates/my-lib",
    "crates/my-app",
]
```

```bash
# Build all workspace members
cargo build --workspace

# Test all workspace members
cargo test --workspace

# Run a specific workspace member
cargo run -p my-app
```

## Async Programming

When writing async Rust code with Tokio:

```toml
[dependencies]
tokio = { version = "1", features = ["full"] }
```

```rust
// Async main entry point
#[tokio::main]
async fn main() {
    let result = fetch_data("https://example.com").await;
    println!("{}", result);
}

// Run futures concurrently
let (a, b) = tokio::join!(task_a(), task_b());

// Race futures — use the first to complete
tokio::select! {
    result = task_a() => println!("A won: {}", result),
    result = task_b() => println!("B won: {}", result),
}

// Spawn a background task
let handle = tokio::spawn(async { 42 });
let value = handle.await.unwrap();

// Put blocking/CPU-heavy work on a dedicated thread pool
let result = tokio::task::spawn_blocking(|| expensive_computation()).await.unwrap();
```

## Error Handling

When handling errors in Rust:

```toml
[dependencies]
thiserror = "2"   # For library error types
anyhow = "1"      # For application-level error handling
```

```rust
// Library code: define precise error types with thiserror
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    #[error("User {id} not found")]
    UserNotFound { id: u32 },
}

// Application code: use anyhow for flexible error handling
use anyhow::{bail, Context, Result};

fn run() -> Result<()> {
    let content = std::fs::read_to_string("config.toml")
        .context("failed to read config.toml")?;
    if content.is_empty() {
        bail!("config file is empty");
    }
    Ok(())
}
```

## Concurrency

When writing concurrent Rust code:

```rust
use std::sync::{Arc, Mutex};
use std::thread;

// Share data across threads with Arc + Mutex
let counter = Arc::new(Mutex::new(0u32));
let handles: Vec<_> = (0..10).map(|_| {
    let c = Arc::clone(&counter);
    thread::spawn(move || { *c.lock().unwrap() += 1; })
}).collect();
for h in handles { h.join().unwrap(); }

// Message passing with channels
use std::sync::mpsc;
let (tx, rx) = mpsc::channel::<String>();
thread::spawn(move || tx.send("hello".into()).unwrap());
println!("{}", rx.recv().unwrap());
```

For data-parallel workloads, use Rayon:

```toml
[dependencies]
rayon = "1"
```

```rust
use rayon::prelude::*;
// Replace .iter() with .par_iter() to parallelise automatically
let sum: i64 = (1..=1_000_000i64).into_par_iter().sum();
```

## CLI Development

When building command-line applications:

```toml
[dependencies]
clap = { version = "4", features = ["derive"] }
```

```rust
use clap::Parser;

/// My CLI tool
#[derive(Parser, Debug)]
#[command(version, about)]
struct Cli {
    /// Input file
    input: String,

    /// Verbose output
    #[arg(short, long)]
    verbose: bool,
}

fn main() {
    let cli = Cli::parse();
    println!("input: {}", cli.input);
}
```
