# Rust 镜像配置参考

本文档提供中国大陆用户配置Rust镜像的详细说明。

## Cargo 镜像配置

在 `~/.cargo/config.toml` 中配置镜像源：

### 中国科学技术大学镜像（推荐）

```toml
[source.crates-io]
replace-with = "ustc"

[source.ustc]
registry = "sparse+https://mirrors.ustc.edu.cn/crates.io-index/"
```

### 字节跳动镜像

```toml
[source.crates-io]
replace-with = "rsproxy"

[source.rsproxy]
registry = "sparse+https://rsproxy.cn/index/"
```

### 清华大学镜像

```toml
[source.crates-io]
replace-with = "tuna"

[source.tuna]
registry = "https://mirrors.tuna.tsinghua.edu.cn/git/crates.io-index.git"
```

## Rustup 镜像配置

设置环境变量以使用国内镜像：

### 中科大镜像

```bash
export RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static
export RUSTUP_UPDATE_ROOT=https://mirrors.ustc.edu.cn/rust-static/rustup
```

### 清华镜像

```bash
export RUSTUP_DIST_SERVER=https://mirrors.tuna.tsinghua.edu.cn/rustup
export RUSTUP_UPDATE_ROOT=https://mirrors.tuna.tsinghua.edu.cn/rustup/rustup
```

## 永久配置

将环境变量添加到 shell 配置文件：

### Bash (~/.bashrc)

```bash
echo 'export RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static' >> ~/.bashrc
echo 'export RUSTUP_UPDATE_ROOT=https://mirrors.ustc.edu.cn/rust-static/rustup' >> ~/.bashrc
source ~/.bashrc
```

### Zsh (~/.zshrc)

```bash
echo 'export RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static' >> ~/.zshrc
echo 'export RUSTUP_UPDATE_ROOT=https://mirrors.ustc.edu.cn/rust-static/rustup' >> ~/.zshrc
source ~/.zshrc
```

### PowerShell ($PROFILE)

```powershell
[Environment]::SetEnvironmentVariable("RUSTUP_DIST_SERVER", "https://mirrors.ustc.edu.cn/rust-static", "User")
[Environment]::SetEnvironmentVariable("RUSTUP_UPDATE_ROOT", "https://mirrors.ustc.edu.cn/rust-static/rustup", "User")
```

## 验证配置

```bash
# 测试 cargo 镜像
cargo search serde

# 测试 rustup 镜像
rustup update
```

## 常见问题

### 镜像同步延迟

镜像站同步官方源可能有几小时延迟，如需最新版本可临时切换回官方源。

### sparse 协议支持

Rust 1.68+ 支持 sparse 协议，下载速度更快。旧版本需使用 git 协议镜像。

### 公司代理配置

如需同时使用公司代理和镜像：

```bash
export HTTPS_PROXY=http://proxy.company.com:8080
export RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static
```
