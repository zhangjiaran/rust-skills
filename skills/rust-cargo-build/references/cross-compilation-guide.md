# 跨平台编译配置参考

本文档提供详细的跨平台编译配置和常见问题解决方案。

## 目标平台配置

### Linux目标

#### x86_64 Linux (静态链接)

```bash
# 安装目标
rustup target add x86_64-unknown-linux-musl

# 编译
cargo build --target x86_64-unknown-linux-musl --release
```

配置 `.cargo/config.toml`:

```toml
[target.x86_64-unknown-linux-musl]
linker = "x86_64-linux-musl-gcc"
```

#### ARM64 Linux

```bash
rustup target add aarch64-unknown-linux-gnu

# 需要安装交叉编译工具链
# Ubuntu: sudo apt install gcc-aarch64-linux-gnu
```

配置:

```toml
[target.aarch64-unknown-linux-gnu]
linker = "aarch64-linux-gnu-gcc"
```

### Windows目标

#### 从Linux编译到Windows

```bash
rustup target add x86_64-pc-windows-gnu

# 安装MinGW-w64
# Ubuntu: sudo apt install mingw-w64
```

配置:

```toml
[target.x86_64-pc-windows-gnu]
linker = "x86_64-w64-mingw32-gcc"
ar = "x86_64-w64-mingw32-ar"
```

编译:

```bash
cargo build --target x86_64-pc-windows-gnu --release
```

### macOS目标

#### 从Linux编译到macOS (需要额外工具)

```bash
rustup target add x86_64-apple-darwin
rustup target add aarch64-apple-darwin
```

需要使用 `osxcross` 或其他工具链。

### WebAssembly目标

#### Web (浏览器)

```bash
rustup target add wasm32-unknown-unknown

cargo build --target wasm32-unknown-unknown --release
```

#### WASI (WebAssembly System Interface)

```bash
rustup target add wasm32-wasi

cargo build --target wasm32-wasi --release
```

### 移动平台

#### Android

```bash
rustup target add aarch64-linux-android
rustup target add armv7-linux-androideabi
rustup target add i686-linux-android

# 需要配置NDK
export NDK_HOME=/path/to/ndk
```

配置:

```toml
[target.aarch64-linux-android]
linker = "aarch64-linux-android21-clang"

[target.armv7-linux-androideabi]
linker = "armv7a-linux-androideabi21-clang"
```

#### iOS

```bash
rustup target add aarch64-apple-ios
rustup target add aarch64-apple-ios-sim
rustup target add x86_64-apple-ios
```

## 条件编译

### 平台特定代码

```rust
#[cfg(target_os = "linux")]
fn platform_specific() {
    // Linux代码
}

#[cfg(target_os = "windows")]
fn platform_specific() {
    // Windows代码
}

#[cfg(target_os = "macos")]
fn platform_specific() {
    // macOS代码
}

#[cfg(target_arch = "x86_64")]
fn arch_specific() {
    // x86_64架构代码
}

#[cfg(target_arch = "aarch64")]
fn arch_specific() {
    // ARM64架构代码
}
```

### 依赖平台特定库

```toml
[target.'cfg(target_os = "linux")'.dependencies]
libc = "0.2"

[target.'cfg(target_os = "windows")'.dependencies]
winapi = { version = "0.3", features = ["winuser"] }

[target.'cfg(target_os = "macos")'.dependencies]
cocoa = "0.25"
```

## 常见问题解决

### 链接器找不到

**问题**: `linker 'x86_64-linux-musl-gcc' not found`

**解决**:

```bash
# Ubuntu/Debian
sudo apt install musl-tools

# Arch Linux
sudo pacman -S musl
```

### 静态链接C库

在 `.cargo/config.toml` 中:

```toml
[target.x86_64-unknown-linux-musl]
rustflags = ["-C", "target-feature=+crt-static"]
```

### 交叉编译OpenSSL依赖

```bash
# 设置OpenSSL路径
export OPENSSL_DIR=/usr/local/ssl
export OPENSSL_STATIC=1

# 或使用vendored版本
# Cargo.toml:
# openssl = { version = "0.10", features = ["vendored"] }
```

## 构建脚本示例

### 自动选择目标

```rust
// build.rs
fn main() {
    let target = std::env::var("TARGET").unwrap();
    
    if target.contains("linux") {
        println!("cargo:rustc-cfg=linux");
    } else if target.contains("windows") {
        println!("cargo:rustc-cfg=windows");
    } else if target.contains("apple") {
        println!("cargo:rustc-cfg=macos");
    }
}
```

## Docker交叉编译

### 使用cross工具

```bash
# 安装cross
cargo install cross

# 使用Docker进行交叉编译
cross build --target aarch64-unknown-linux-gnu
cross build --target armv7-unknown-linux-gnueabihf
```

### Dockerfile示例

```dockerfile
FROM rust:latest

RUN apt update && apt install -y \
    gcc-aarch64-linux-gnu \
    gcc-arm-linux-gnueabihf \
    musl-tools

RUN rustup target add aarch64-unknown-linux-gnu
RUN rustup target add armv7-unknown-linux-gnueabihf
RUN rustup target add x86_64-unknown-linux-musl

WORKDIR /app
COPY . .

CMD ["cargo", "build", "--release"]
```
