# Rust 项目模板参考

本文档提供常用Rust项目类型的Cargo.toml模板和项目结构建议。

## 应用程序项目模板

### 基础CLI应用

```toml
[package]
name = "my-cli-app"
version = "0.1.0"
edition = "2021"
authors = ["Your Name <you@example.com>"]
description = "A CLI application"
license = "MIT"

[dependencies]
clap = { version = "4", features = ["derive"] }
anyhow = "1"
thiserror = "1"

[dev-dependencies]
assert_cmd = "2"
predicates = "3"
```

### Web服务应用

```toml
[package]
name = "my-web-service"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1", features = ["full"] }
axum = "0.7"
tower = "0.4"
tower-http = { version = "0.5", features = ["trace", "cors"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
anyhow = "1"

[dev-dependencies]
reqwest = { version = "0.11", features = ["json"] }
```

### 异步应用

```toml
[package]
name = "my-async-app"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1", features = ["full"] }
futures = "0.3"
async-trait = "0.1"

[dev-dependencies]
tokio-test = "0.4"
```

## 库项目模板

### 通用库

```toml
[package]
name = "my-lib"
version = "0.1.0"
edition = "2021"
license = "MIT OR Apache-2.0"
repository = "https://github.com/username/my-lib"
description = "A Rust library"
keywords = ["rust", "library"]
categories = ["development-tools"]

[dependencies]
serde = { version = "1", features = ["derive"], optional = true }

[features]
default = ["std"]
std = []
serde-support = ["dep:serde"]

[dev-dependencies]
tokio = { version = "1", features = ["macros", "rt"] }
```

### WASM库

```toml
[package]
name = "my-wasm-lib"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib", "rlib"]

[dependencies]
wasm-bindgen = "0.2"
js-sys = "0.3"
web-sys = { version = "0.3", features = ["Window", "Document"] }

[dev-dependencies]
wasm-bindgen-test = "0.3"

[profile.release]
opt-level = "s"
lto = true
```

## 项目结构模板

### 标准应用结构

```text
my-app/
├── Cargo.toml
├── Cargo.lock
├── .gitignore
├── README.md
├── src/
│   ├── main.rs
│   ├── lib.rs
│   ├── config.rs
│   ├── error.rs
│   └── commands/
│       ├── mod.rs
│       └── build.rs
├── tests/
│   └── integration_test.rs
├── benches/
│   └── benchmark.rs
└── examples/
    └── example.rs
```

### 库项目结构

```text
my-lib/
├── Cargo.toml
├── README.md
├── src/
│   ├── lib.rs
│   ├── error.rs
│   ├── types.rs
│   └── module/
│       ├── mod.rs
│       └── submodule.rs
├── tests/
│   └── integration_test.rs
└── examples/
    └── basic_usage.rs
```

## 常用依赖组合

### 日志和追踪

```toml
[dependencies]
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

### 序列化

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
serde_json = "1"
toml = "0.8"
```

### 错误处理

```toml
[dependencies]
anyhow = "1"          # 应用程序
thiserror = "1"       # 库
```

### 测试工具

```toml
[dev-dependencies]
pretty_assertions = "1"
tempfile = "3"
mockall = "0.12"
tokio-test = "0.4"
```

## Profile配置模板

### 优化发布版本

```toml
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true
panic = "abort"
```

### 快速开发构建

```toml
[profile.dev]
opt-level = 0
debug = true
incremental = true

[profile.dev.package."*"]
opt-level = 2  # 优化依赖
```

### 性能分析构建

```toml
[profile.profiling]
inherits = "release"
debug = true
strip = false
```
