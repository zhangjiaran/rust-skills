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
