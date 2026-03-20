---
name: rust-error-handling
description: Handle errors idiomatically in Rust. Use when you need to define custom error types, propagate errors with ?, use thiserror or anyhow crates, or convert between error types.
---

# Rust 错误处理 (Error Handling in Rust)

本文档介绍 Rust 惯用的错误处理模式，包括 `Result`/`Option`、自定义错误类型以及 `thiserror`/`anyhow` 库的使用。

---

## Result 与 Option 基础

```rust
// Result<T, E>：操作可能失败
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("除数不能为零".to_string())
    } else {
        Ok(a / b)
    }
}

// Option<T>：值可能不存在
fn find_user(id: u32) -> Option<String> {
    if id == 1 { Some("Alice".to_string()) } else { None }
}
```

### 常用组合子方法

```rust
let result: Result<i32, &str> = Ok(42);

// map：对 Ok 值做变换
let doubled = result.map(|v| v * 2);

// map_err：对 Err 值做变换
let mapped = result.map_err(|e| format!("错误: {}", e));

// and_then：链式操作（flatMap）
let chained = result.and_then(|v| if v > 0 { Ok(v) } else { Err("负数") });

// unwrap_or：失败时使用默认值
let val = result.unwrap_or(0);

// unwrap_or_else：失败时执行闭包
let val = result.unwrap_or_else(|_| -1);

// ok()：Result 转 Option（丢弃错误信息）
let opt: Option<i32> = result.ok();

// Option 转 Result
let res: Result<i32, &str> = opt.ok_or("值不存在");
```

---

## ? 运算符（错误传播）

`?` 会在 `Err`/`None` 时提前返回，并自动调用 `From::from` 做类型转换。

```rust
use std::fs;
use std::io;

fn read_username(path: &str) -> Result<String, io::Error> {
    let content = fs::read_to_string(path)?; // 失败则立即返回 Err
    Ok(content.trim().to_string())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let name = read_username("user.txt")?;
    println!("用户名: {}", name);
    Ok(())
}
```

---

## 自定义错误类型

### 手动实现（标准库）

```rust
use std::fmt;

#[derive(Debug)]
pub enum AppError {
    Io(std::io::Error),
    Parse(std::num::ParseIntError),
    Custom(String),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppError::Io(e) => write!(f, "IO 错误: {}", e),
            AppError::Parse(e) => write!(f, "解析错误: {}", e),
            AppError::Custom(msg) => write!(f, "错误: {}", msg),
        }
    }
}

impl std::error::Error for AppError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            AppError::Io(e) => Some(e),
            AppError::Parse(e) => Some(e),
            AppError::Custom(_) => None,
        }
    }
}

// 实现 From 以支持 ? 运算符自动转换
impl From<std::io::Error> for AppError {
    fn from(e: std::io::Error) -> Self { AppError::Io(e) }
}
impl From<std::num::ParseIntError> for AppError {
    fn from(e: std::num::ParseIntError) -> Self { AppError::Parse(e) }
}
```

---

## thiserror — 简化自定义错误

适合库（library）代码，生成明确的错误类型。

```toml
[dependencies]
thiserror = "2"
```

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("IO 错误: {0}")]
    Io(#[from] std::io::Error),

    #[error("解析错误: {0}")]
    Parse(#[from] std::num::ParseIntError),

    #[error("用户 {id} 未找到")]
    UserNotFound { id: u32 },

    #[error("配置项 {key} 缺失，期望值: {expected}")]
    MissingConfig { key: String, expected: String },
}

fn load_config(path: &str) -> Result<String, AppError> {
    let content = std::fs::read_to_string(path)?; // io::Error 自动转换
    Ok(content)
}
```

---

## anyhow — 简化应用层错误处理

适合应用（binary）代码，不需要精确的错误类型匹配。

```toml
[dependencies]
anyhow = "1"
```

```rust
use anyhow::{anyhow, bail, Context, Result};

fn parse_port(s: &str) -> Result<u16> {
    let port: u16 = s.parse().context("端口号必须是 0-65535 的整数")?;
    if port < 1024 {
        bail!("端口号 {} 是特权端口，请使用 >= 1024 的端口", port);
    }
    Ok(port)
}

fn main() -> Result<()> {
    // 所有实现了 std::error::Error 的类型都可以用 ?
    let content = std::fs::read_to_string("config.toml")
        .context("无法读取配置文件 config.toml")?;

    println!("config: {}", content);
    Ok(())
}
```

### anyhow 常用宏和方法

```rust
use anyhow::{anyhow, bail, ensure, Context};

// anyhow!：创建一次性错误
return Err(anyhow!("自定义错误: {}", detail));

// bail!：等同于 return Err(anyhow!(...))
bail!("验证失败: {}", reason);

// ensure!：断言，失败时 bail
ensure!(value > 0, "值必须为正数，实际为 {}", value);

// context / with_context：附加上下文信息
let val = some_result.context("操作 X 失败")?;
let val = some_result.with_context(|| format!("处理 {} 时失败", name))?;

// 向下转型
if let Some(io_err) = err.downcast_ref::<std::io::Error>() {
    println!("IO 错误: {}", io_err);
}
```

---

## thiserror vs anyhow 选择指南

| 场景 | 推荐库 | 原因 |
| ---- | ------ | ---- |
| 编写库（lib crate） | **thiserror** | 调用方需要精确匹配错误类型 |
| 编写应用（binary crate） | **anyhow** | 关注错误上下文，不需要细分类型 |
| 库的内部实现 | 视情况 | 内部可用 anyhow，公开 API 用 thiserror |

---

## 常见模式

### 多错误类型统一处理（Box<dyn Error>）

```rust
fn run() -> Result<(), Box<dyn std::error::Error>> {
    let n: i32 = "42".parse()?;        // ParseIntError
    let _f = std::fs::File::open("x")?; // io::Error
    println!("{}", n);
    Ok(())
}
```

### 忽略错误（仅在确认安全时使用）

```rust
// 使用 let _ 明确忽略
let _ = std::fs::remove_file("tmp.txt");

// 使用 ok() 将 Result 转为 Option 再忽略
std::fs::remove_file("tmp.txt").ok();
```

### 在测试中处理错误

```rust
#[cfg(test)]
mod tests {
    #[test]
    fn test_parse() -> Result<(), std::num::ParseIntError> {
        let n: i32 = "42".parse()?;
        assert_eq!(n, 42);
        Ok(())
    }
}
```
