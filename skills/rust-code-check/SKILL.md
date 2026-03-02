---
name: rust-code-check
description: Format, lint, and audit Rust code. Use when you need to run rustfmt, clippy, cargo audit, or set up CI/CD code quality checks.
---

# Rust 代码检查 (Code Checking & Linting)

本文档介绍如何使用 Rust 工具链进行代码格式化、静态分析和安全审计。

## 辅助脚本

运行完整的代码质量检查流程：

```bash
python scripts/check_all.py
```

该脚本会依次运行：
- 代码格式化检查 (rustfmt)
- Clippy静态分析
- 类型检查
- 单元测试
- 安全审计 (cargo audit)

## rustfmt — 代码格式化

`rustfmt` 是 Rust 官方代码格式化工具，确保代码风格一致。

### 安装

```bash
rustup component add rustfmt
```

### 使用

```bash
# 格式化当前项目所有文件
cargo fmt

# 仅检查格式，不修改文件（用于 CI）
cargo fmt -- --check

# 格式化单个文件
rustfmt src/main.rs

# 显示哪些文件需要格式化
cargo fmt -- --check --verbose
```

### 配置 rustfmt

在项目根目录创建 `rustfmt.toml`：

```toml
# rustfmt.toml
edition = "2021"
max_width = 100                  # 每行最大字符数（默认 100）
tab_spaces = 4                   # 缩进空格数（默认 4）
newline_style = "Unix"           # 换行符风格
use_small_heuristics = "Default" # 启发式布局选项

# 导入分组
imports_granularity = "Crate"    # 合并同 crate 的 use 语句
group_imports = "StdExternalCrate"  # 分组: std, external, crate

# 其他选项
format_code_in_doc_comments = true
wrap_comments = true
comment_width = 80
```

---

## Clippy — 静态分析（Linter）

`clippy` 是 Rust 官方 linter，检测常见错误、不规范代码和性能问题。

### 安装

```bash
rustup component add clippy
```

### 基本使用

```bash
# 运行 clippy（默认检查）
cargo clippy

# 检查所有目标（包括测试、示例）
cargo clippy --all-targets

# 检查所有 features
cargo clippy --all-features

# 将警告视为错误（推荐用于 CI）
cargo clippy -- -D warnings

# 自动修复某些问题
cargo clippy --fix
cargo clippy --fix --allow-dirty        # 有未提交更改时允许修复
cargo clippy --fix --allow-staged       # 有已暂存更改时允许修复

# 工作空间中所有成员
cargo clippy --workspace -- -D warnings
```

### 常见 Clippy 警告及修复

```rust
// ❌ 不推荐：使用 .clone() 克隆可以借用的值
let s = String::from("hello");
let len = s.clone().len();

// ✅ 推荐：直接借用
let len = s.len();

// ❌ 不推荐：使用 if let 可以更简洁的 match
match value {
    Some(x) => use(x),
    None => {}
}

// ✅ 推荐：
if let Some(x) = value {
    use(x);
}

// ❌ 不推荐：collect 后立即迭代
let v: Vec<_> = iter.collect();
for item in v.iter() { ... }

// ✅ 推荐：直接迭代
for item in iter { ... }

// ❌ 不推荐：将 bool 转换为 Option 再使用
if condition { Some(value) } else { None }

// ✅ 推荐：
condition.then(|| value)
condition.then_some(value)  // Rust 1.62+
```

### 配置 Clippy

在 `Cargo.toml` 或代码中配置：

```toml
# .clippy.toml 或 clippy.toml
# 目前 clippy 不支持 toml 配置文件，使用代码属性配置
```

```rust
// 在代码中允许/禁止特定 lint
#![allow(clippy::needless_return)]       // 文件级别
#![deny(clippy::unwrap_used)]            // 禁止使用 unwrap

// 函数级别
#[allow(clippy::too_many_arguments)]
fn complex_function(...) {}

// 单行允许
let x = some_option.unwrap(); // #[allow(clippy::unwrap_used)] 已知安全
```

---

## cargo check — 快速类型检查

比完整编译快，用于快速反馈。

```bash
# 检查代码是否能编译（不生成可执行文件）
cargo check

# 检查所有目标
cargo check --all-targets

# 检查特定包（工作空间）
cargo check -p my-lib
```

---

## cargo audit — 安全审计

检查依赖中是否存在已知安全漏洞。

### 安装

```bash
cargo install cargo-audit
```

### 使用

```bash
# 审计当前项目依赖
cargo audit

# 更新漏洞数据库后审计
cargo audit --update

# 输出 JSON 格式（用于 CI 集成）
cargo audit --json

# 忽略特定漏洞（需要说明原因）
cargo audit --ignore RUSTSEC-2021-0001
```

---

## cargo deny — 依赖策略检查

检查依赖的许可证、安全漏洞、重复依赖等。

### 安装

```bash
cargo install cargo-deny
```

### 配置 deny.toml

```toml
# deny.toml
[advisories]
db-path = "~/.cargo/advisory-db"
db-urls = ["https://github.com/rustsec/advisory-db"]
vulnerability = "deny"
unmaintained = "warn"
yanked = "deny"

[licenses]
unlicensed = "deny"
allow = [
    "MIT",
    "Apache-2.0",
    "Apache-2.0 WITH LLVM-exception",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
    "Unicode-DFS-2016",
]
copyleft = "warn"

[bans]
multiple-versions = "warn"
wildcards = "deny"
deny = [
    { name = "openssl" },  # 禁止使用 OpenSSL（改用 rustls）
]

[sources]
unknown-registry = "deny"
unknown-git = "deny"
allow-registry = ["https://github.com/rust-lang/crates.io-index"]
```

```bash
# 运行所有检查
cargo deny check

# 只检查安全漏洞
cargo deny check advisories

# 只检查许可证
cargo deny check licenses
```

---

## cargo udeps — 检查未使用依赖

```bash
# 安装（需要 nightly）
cargo install cargo-udeps
rustup override set nightly    # 或使用 +nightly

# 检查未使用的依赖
cargo +nightly udeps
cargo +nightly udeps --all-targets
```

---

## 在 CI/CD 中集成代码检查

### GitHub Actions 示例

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: rustfmt, clippy

      - name: Check formatting
        run: cargo fmt -- --check

      - name: Run Clippy
        run: cargo clippy --all-targets -- -D warnings

      - name: Run tests
        run: cargo test

      - name: Security audit
        run: |
          cargo install cargo-audit
          cargo audit
```

---

## 推荐的代码检查流程

```bash
# 开发时的完整检查流程
cargo fmt                              # 1. 格式化代码
cargo check                            # 2. 快速类型检查
cargo clippy --all-targets -- -D warnings  # 3. Lint 检查
cargo test                             # 4. 运行测试
cargo audit                            # 5. 安全审计（可选，视需要运行）
```

---

## IDE 集成

使用 `rust-analyzer` 获得实时的代码检查反馈：

```bash
# 安装 rust-analyzer
rustup component add rust-analyzer

# 在 VS Code 中安装 "rust-analyzer" 扩展
# 在 Cursor 中内置支持
# 在 IntelliJ IDEA 中安装 "Rust" 插件
```

`rust-analyzer` 提供：

- 实时错误提示
- 自动补全
- 跳转到定义
- 重构支持
- Clippy 集成（可配置为实时显示 clippy 警告）
