# Rust 开发实践 (Rust Development Practices)

本文档介绍 Rust 项目开发的最佳实践和常用工作流。

## 创建新项目

### 使用 Cargo 初始化项目

```bash
# 创建二进制项目（可执行程序）
cargo new my-app

# 创建库项目
cargo new my-lib --lib

# 在已有目录中初始化
cd existing-dir
cargo init
cargo init --lib        # 初始化为库项目
```

### 项目结构

```text
my-project/
├── Cargo.toml            # 项目配置（依赖、元数据等）
├── Cargo.lock            # 锁定的依赖版本（提交到版本控制）
├── src/
│   ├── main.rs           # 二进制入口点
│   ├── lib.rs            # 库根模块（如果是库）
│   └── module/
│       ├── mod.rs        # 子模块根
│       └── submodule.rs  # 子模块文件
├── tests/
│   └── integration_test.rs   # 集成测试
├── benches/
│   └── benchmark.rs      # 性能基准测试
├── examples/
│   └── example.rs        # 使用示例
└── build.rs              # 构建脚本（可选）
```

### Cargo.toml 配置示例

```toml
[package]
name = "my-app"
version = "0.1.0"
edition = "2021"
description = "A sample Rust application"
license = "MIT OR Apache-2.0"
authors = ["Your Name <you@example.com>"]
repository = "https://github.com/username/my-app"

# 依赖
[dependencies]
serde = { version = "1", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
anyhow = "1"
tracing = "0.1"

# 仅开发时使用的依赖
[dev-dependencies]
mockall = "0.12"
pretty_assertions = "1"

# 构建脚本依赖
[build-dependencies]
cc = "1"

# 功能开关
[features]
default = ["std"]
std = []
async = ["tokio"]

# 发布优化配置
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true
```

---

## 常用开发命令

```bash
# 编译检查（不生成二进制，速度最快）
cargo check

# 调试构建
cargo build

# 运行程序
cargo run
cargo run -- arg1 arg2     # 传递命令行参数

# Release 构建（优化版本）
cargo build --release
cargo run --release

# 构建指定目标
cargo build --target x86_64-unknown-linux-musl

# 使用 features 构建
cargo build --features "async,logging"
cargo build --no-default-features
cargo build --all-features

# 查看编译警告/错误
cargo check 2>&1 | head -50
```

---

## 依赖管理

### 添加依赖

```bash
# 使用 cargo-edit 工具（推荐）
cargo add serde                         # 添加最新版本
cargo add serde --features derive       # 添加并启用 features
cargo add tokio@1 --features full       # 指定主版本
cargo add --dev mockall                 # 添加开发依赖
cargo add --build cc                    # 添加构建依赖

# 手动编辑 Cargo.toml（不使用 cargo-edit 时）
# [dependencies]
# serde = { version = "1", features = ["derive"] }
```

### 更新依赖

```bash
cargo update            # 更新所有依赖到兼容的最新版本
cargo update serde      # 只更新 serde
```

### 查看依赖树

```bash
cargo tree                  # 完整依赖树
cargo tree -d               # 只显示重复的依赖
cargo tree -i serde         # 查看谁依赖了 serde
cargo tree --depth 2        # 限制显示深度
```

---

## 模块系统

### 声明模块

```rust
// src/lib.rs 或 src/main.rs
mod utils;          // 引用 src/utils.rs 或 src/utils/mod.rs
pub mod api;        // 公开模块

// 内联模块
mod config {
    pub struct Config {
        pub debug: bool,
    }
}
```

### 使用模块

```rust
use crate::utils::helper_function;
use crate::config::Config;
use std::collections::HashMap;

// 引入多个项
use std::io::{self, Read, Write};

// 别名
use std::collections::HashMap as Map;
```

---

## 错误处理最佳实践

### 使用 Result 和 ? 运算符

```rust
use std::fs;
use anyhow::{Context, Result};

fn read_config(path: &str) -> Result<String> {
    let content = fs::read_to_string(path)
        .with_context(|| format!("Failed to read config file: {}", path))?;
    Ok(content)
}
```

### 定义自定义错误类型（库开发）

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Parse error: {message}")]
    Parse { message: String },

    #[error("Not found: {0}")]
    NotFound(String),
}
```

---

## 异步编程

### 配置 tokio 运行时

```rust
// main.rs
#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // 异步代码
    let result = fetch_data("https://api.example.com").await?;
    println!("{}", result);
    Ok(())
}
```

### 并发任务

```rust
use tokio::task;

async fn run_concurrent() {
    let handle1 = task::spawn(async {
        // 并发任务 1
        heavy_computation().await
    });
    let handle2 = task::spawn(async {
        // 并发任务 2
        io_operation().await
    });

    let (result1, result2) = tokio::join!(handle1, handle2);
}
```

---

## 日志与追踪

```rust
// Cargo.toml
// tracing = "0.1"
// tracing-subscriber = { version = "0.3", features = ["env-filter"] }

use tracing::{info, warn, error, debug, instrument};

fn main() {
    tracing_subscriber::fmt()
        .with_env_filter("my_app=debug,warn")
        .init();

    info!("Application started");
    debug!("Debug information: {:?}", some_value);
    warn!("Warning: {}", message);
    error!("Error occurred: {}", err);
}

#[instrument]
fn traced_function(input: &str) -> String {
    info!("Processing input");
    input.to_uppercase()
}
```

---

## 代码组织建议

1. **单一职责**：每个模块专注于一个功能领域
2. **公共 API 最小化**：只暴露必要的公共接口（`pub`）
3. **文档注释**：为所有公共 API 编写 `///` 文档注释
4. **示例代码**：在 `examples/` 目录提供使用示例
5. **错误信息友好**：错误消息要清晰、可操作

```rust
/// 计算两个数的和。
///
/// # Examples
///
/// ```
/// use my_crate::add;
/// assert_eq!(add(2, 3), 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```
