---
name: rust-installation
description: Install and manage Rust toolchain using rustup. Use when you need to install Rust, manage toolchains, add components, or configure cross-compilation targets.
---

# Rust 安装指南 (Rust Installation Guide)

本文档介绍如何安装和管理 Rust 工具链。

## 相关资源

- [镜像配置参考](references/mirror-configuration.md) - 中国大陆用户镜像配置指南

## 使用 rustup 安装 Rust

`rustup` 是 Rust 官方工具链管理器，推荐使用它来安装和管理 Rust。

### Linux / macOS

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

安装完成后，将 Cargo 的 bin 目录添加到 PATH：

```bash
source "$HOME/.cargo/env"
```

### Windows

访问 [https://rustup.rs](https://rustup.rs) 下载 `rustup-init.exe` 并运行。

或使用 winget：

```powershell
winget install Rustlang.Rustup
```

### 验证安装

```bash
rustc --version   # 查看 Rust 编译器版本
cargo --version   # 查看 Cargo 版本
rustup --version  # 查看 rustup 版本
```

---

## 工具链管理

### 安装特定版本

```bash
rustup install stable          # 最新稳定版
rustup install nightly         # 每日构建版
rustup install 1.75.0          # 指定版本
rustup install beta            # beta 版本
```

### 设置默认工具链

```bash
rustup default stable          # 设置 stable 为默认
rustup default nightly         # 设置 nightly 为默认
```

### 在项目中指定工具链

在项目根目录创建 `rust-toolchain.toml` 文件：

```toml
[toolchain]
channel = "stable"      # 或 "nightly", "1.75.0"
components = ["rustfmt", "clippy"]
targets = ["wasm32-unknown-unknown"]
```

### 更新工具链

```bash
rustup update              # 更新所有已安装的工具链
rustup update stable       # 只更新 stable
```

### 查看已安装的工具链

```bash
rustup toolchain list
```

---

## 组件管理

Rust 工具链包含多个可选组件。

### 安装常用组件

```bash
rustup component add rustfmt        # 代码格式化工具
rustup component add clippy         # 代码检查工具（Linter）
rustup component add rust-src       # Rust 标准库源码（IDE 支持）
rustup component add rust-analyzer  # 语言服务器（IDE 支持）
rustup component add llvm-tools-preview  # LLVM 工具（代码覆盖率等）
```

### 查看已安装的组件

```bash
rustup component list --installed
```

---

## 跨平台编译目标管理

### 添加编译目标

```bash
# WebAssembly
rustup target add wasm32-unknown-unknown
rustup target add wasm32-wasi

# Linux 静态链接
rustup target add x86_64-unknown-linux-musl
rustup target add aarch64-unknown-linux-musl

# Windows（在 Linux 上交叉编译）
rustup target add x86_64-pc-windows-gnu

# macOS（在 Linux 上交叉编译，需要额外配置）
rustup target add x86_64-apple-darwin

# Android
rustup target add aarch64-linux-android
rustup target add armv7-linux-androideabi

# iOS
rustup target add aarch64-apple-ios
```

### 查看已安装的目标

```bash
rustup target list --installed
```

### 为指定目标编译

```bash
cargo build --target wasm32-unknown-unknown
cargo build --target x86_64-unknown-linux-musl
```

---

## 常用 Cargo 工具安装

```bash
# 代码安全审计
cargo install cargo-audit

# 自动更新依赖
cargo install cargo-edit

# 检查未使用的依赖
cargo install cargo-udeps

# 查看扩展后的宏代码
cargo install cargo-expand

# 性能分析
cargo install cargo-flamegraph

# 监视文件变化并自动重新构建
cargo install cargo-watch

# 生成变更日志
cargo install git-cliff

# 代码覆盖率
cargo install cargo-tarpaulin   # Linux only
cargo install cargo-llvm-cov    # 跨平台

# 二进制体积分析
cargo install cargo-bloat

# 依赖许可证检查
cargo install cargo-deny
```

---

## 卸载 Rust

```bash
rustup self uninstall
```

---

## 常见问题

### 更新后命令找不到

确保 `~/.cargo/bin` 在 `PATH` 中：

```bash
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 公司网络下安装（配置代理）

```bash
export HTTPS_PROXY=http://proxy.example.com:8080
export HTTP_PROXY=http://proxy.example.com:8080
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### 使用国内镜像（中国大陆用户）

在 `~/.cargo/config.toml` 中配置镜像：

```toml
[source.crates-io]
replace-with = "ustc"

[source.ustc]
registry = "sparse+https://mirrors.ustc.edu.cn/crates.io-index/"

# 或使用字节跳动镜像
[source.rsproxy]
registry = "sparse+https://rsproxy.cn/index/"
```

设置 rustup 镜像：

```bash
export RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static
export RUSTUP_UPDATE_ROOT=https://mirrors.ustc.edu.cn/rust-static/rustup
```
