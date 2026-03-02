---
name: Cargo 构建指南
description: Cargo 构建系统的使用方法，包括构建配置、Features 条件编译、跨平台编译、工作空间和发布流程。
---

# Cargo 构建指南 (Cargo Build Guide)

本文档介绍 Cargo 构建系统的使用方法，包括构建配置、跨平台编译、性能优化等。

## 基本构建命令

```bash
# 调试构建（快速编译，包含调试信息）
cargo build

# Release 构建（优化编译，适合生产环境）
cargo build --release

# 检查是否可以编译（不生成二进制，最快）
cargo check

# 运行（调试模式）
cargo run
cargo run -- --arg1 value1        # 传递程序参数

# 运行（release 模式）
cargo run --release
cargo run --release -- --arg1 value1

# 构建并输出到指定目录
cargo build --target-dir /path/to/output
```

---

## 构建 Profile 配置

在 `Cargo.toml` 中自定义构建配置：

```toml
# 调试构建（cargo build）
[profile.dev]
opt-level = 0          # 优化级别：0-3，s（体积优化），z（最小体积）
debug = true           # 包含调试信息
debug-assertions = true
overflow-checks = true
lto = false            # 链接时优化（LTO）
panic = "unwind"       # panic 策略："unwind" 或 "abort"
incremental = true     # 增量编译
codegen-units = 256    # 并行代码生成单元

# Release 构建（cargo build --release）
[profile.release]
opt-level = 3
debug = false
debug-assertions = false
overflow-checks = false
lto = true             # 启用 LTO 提升性能
panic = "abort"        # 减小二进制体积
incremental = false
codegen-units = 1      # 最大化优化机会
strip = true           # 去除调试符号

# 自定义 profile（cargo build --profile profiling）
[profile.profiling]
inherits = "release"
debug = true           # release + 调试信息（性能分析用）
strip = false
```

---

## Features 条件编译

### 定义 Features

```toml
# Cargo.toml
[features]
default = ["std"]                 # 默认启用的 features
std = []                          # 标准库支持
async = ["dep:tokio"]             # 异步支持
logging = ["dep:tracing", "dep:tracing-subscriber"]
full = ["async", "logging"]       # 启用所有功能

[dependencies]
tokio = { version = "1", features = ["full"], optional = true }
tracing = { version = "0.1", optional = true }
```

### 使用 Features

```rust
// 条件编译
#[cfg(feature = "async")]
pub mod async_api {
    // 异步 API 实现
}

#[cfg(not(feature = "std"))]
extern crate alloc;

// 条件引入
#[cfg(feature = "logging")]
use tracing::info;
```

### 构建时指定 Features

```bash
# 使用指定 features
cargo build --features "async,logging"

# 使用所有 features
cargo build --all-features

# 禁用默认 features
cargo build --no-default-features

# 禁用默认 features 同时启用指定 features
cargo build --no-default-features --features "async"
```

---

## 跨平台编译

### 前提条件

```bash
# 添加目标平台
rustup target add x86_64-unknown-linux-musl    # Linux 静态链接
rustup target add x86_64-pc-windows-gnu        # Windows（在 Linux 上）
rustup target add aarch64-unknown-linux-gnu    # ARM64 Linux
rustup target add wasm32-unknown-unknown       # WebAssembly
```

### 编译到指定目标

```bash
# 编译到 Linux 静态链接版本
cargo build --target x86_64-unknown-linux-musl --release

# 编译到 WebAssembly
cargo build --target wasm32-unknown-unknown --release

# 编译到 Windows（需要安装 MinGW 链接器）
cargo build --target x86_64-pc-windows-gnu --release
```

### 配置 .cargo/config.toml 简化跨编译

```toml
# .cargo/config.toml
[target.x86_64-unknown-linux-musl]
linker = "x86_64-linux-musl-gcc"

[target.aarch64-unknown-linux-gnu]
linker = "aarch64-linux-gnu-gcc"

# 为特定目标设置环境变量
[target.x86_64-pc-windows-gnu]
linker = "x86_64-w64-mingw32-gcc"
ar = "x86_64-w64-mingw32-ar"
```

---

## 工作空间（Workspace）

### 创建工作空间

```toml
# Cargo.toml（工作空间根目录）
[workspace]
members = [
    "crates/my-lib",
    "crates/my-app",
    "tools/codegen",
]
resolver = "2"    # 建议使用 resolver version 2

# 工作空间级别的依赖（在 members 中用 workspace = true 引用）
[workspace.dependencies]
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
anyhow = "1"
```

```toml
# crates/my-lib/Cargo.toml
[package]
name = "my-lib"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { workspace = true }        # 引用工作空间依赖
anyhow = { workspace = true }
```

### 工作空间构建命令

```bash
# 构建所有成员
cargo build --workspace

# 只构建指定成员
cargo build -p my-lib
cargo build -p my-app

# 运行指定成员
cargo run -p my-app

# 测试所有成员
cargo test --workspace

# 发布所有成员（按依赖顺序）
cargo publish -p my-lib
cargo publish -p my-app
```

---

## 构建脚本 (build.rs)

`build.rs` 在编译前运行，用于代码生成、链接本地库等。

```rust
// build.rs
fn main() {
    // 告诉 cargo 如果 build.rs 变化则重新运行
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-changed=src/proto/");

    // 链接本地 C 库
    println!("cargo:rustc-link-lib=mylib");
    println!("cargo:rustc-link-search=native=/usr/local/lib");

    // 设置编译时环境变量
    println!("cargo:rustc-env=BUILD_TIME={}", chrono::Utc::now());

    // 设置 cfg 标志
    let target = std::env::var("CARGO_CFG_TARGET_OS").unwrap();
    if target == "linux" {
        println!("cargo:rustc-cfg=linux_specific");
    }

    // 使用 prost 生成 protobuf 代码
    // prost_build::compile_protos(&["src/proto/service.proto"], &["src/proto/"])?;
}
```

---

## 生成文档

```bash
# 生成文档
cargo doc

# 生成并在浏览器中打开
cargo doc --open

# 只为当前 crate 生成文档（不包含依赖）
cargo doc --no-deps

# 包含私有项
cargo doc --document-private-items

# 生成所有 features 的文档
cargo doc --all-features
```

---

## 分析构建

```bash
# 显示构建时间（各 crate 编译时间）
cargo build --timings
# 生成 cargo-timing-YYYYMMDD-HHMMSS.html

# 查看最终二进制体积分析
cargo install cargo-bloat
cargo bloat --release
cargo bloat --release --crates      # 按 crate 分组

# 查看展开的宏代码
cargo install cargo-expand
cargo expand                        # 展开所有宏
cargo expand my_module              # 展开指定模块
```

---

## 发布到 crates.io

```toml
# Cargo.toml 必填字段
[package]
name = "my-crate"
version = "1.0.0"
edition = "2021"
description = "A brief description of the crate"
license = "MIT OR Apache-2.0"
repository = "https://github.com/username/my-crate"
keywords = ["rust", "utility"]       # 最多 5 个关键词
categories = ["development-tools"]   # crates.io 分类
readme = "README.md"
```

```bash
# 验证发布（不实际发布）
cargo publish --dry-run

# 发布（需要先登录：cargo login）
cargo publish

# 登录 crates.io
cargo login <your-api-token>
```

---

## 常用构建加速技巧

```bash
# 使用 sccache 缓存编译结果
cargo install sccache
export RUSTC_WRAPPER=sccache

# 使用 mold 或 lld 链接器（Linux，更快的链接速度）
# .cargo/config.toml
# [target.x86_64-unknown-linux-gnu]
# linker = "clang"
# rustflags = ["-C", "link-arg=-fuse-ld=mold"]

# 监视文件变化并自动重新构建
cargo install cargo-watch
cargo watch -x build          # 监视并构建
cargo watch -x test           # 监视并测试
cargo watch -x "run -- --port 8080"  # 监视并运行
```
