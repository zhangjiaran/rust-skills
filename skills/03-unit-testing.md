# Rust 单元测试 (Unit Testing in Rust)

本文档介绍如何在 Rust 中编写和运行单元测试、集成测试及文档测试。

## 测试基础

### 单元测试

Rust 的单元测试直接写在源码文件中，用 `#[cfg(test)]` 标注的模块包裹。

```rust
// src/lib.rs 或 src/main.rs

pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

pub fn divide(a: f64, b: f64) -> Option<f64> {
    if b == 0.0 {
        None
    } else {
        Some(a / b)
    }
}

#[cfg(test)]
mod tests {
    use super::*;  // 引入当前模块的所有内容

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(add(-1, 1), 0);
        assert_eq!(add(0, 0), 0);
    }

    #[test]
    fn test_divide_normal() {
        assert_eq!(divide(10.0, 2.0), Some(5.0));
    }

    #[test]
    fn test_divide_by_zero() {
        assert_eq!(divide(5.0, 0.0), None);
    }
}
```

### 断言宏

```rust
// 相等断言
assert_eq!(left, right);
assert_eq!(left, right, "自定义错误消息: {} vs {}", left, right);

// 不等断言
assert_ne!(left, right);

// 布尔断言
assert!(condition);
assert!(condition, "条件 {} 不满足", value);

// 使用 pretty_assertions 获得更清晰的差异输出
// [dev-dependencies]
// pretty_assertions = "1"
use pretty_assertions::assert_eq;
```

### 预期 panic 的测试

```rust
#[test]
#[should_panic]
fn test_should_panic() {
    panic!("this should panic");
}

#[test]
#[should_panic(expected = "divide by zero")]
fn test_panic_with_message() {
    let _ = 1 / 0;
}
```

### 返回 Result 的测试

```rust
#[test]
fn test_with_result() -> Result<(), Box<dyn std::error::Error>> {
    let result = parse_number("42")?;
    assert_eq!(result, 42);
    Ok(())
}
```

---

## 集成测试

集成测试放在 `tests/` 目录中，每个文件是独立的测试 crate。

```text
my-project/
├── src/
│   └── lib.rs
└── tests/
    ├── integration_test.rs
    └── api_test.rs
```

```rust
// tests/integration_test.rs
use my_project::add;

#[test]
fn test_add_integration() {
    assert_eq!(add(100, 200), 300);
}
```

---

## 文档测试

文档注释中的代码示例会被 `cargo test --doc` 自动运行。

```rust
/// 将两个整数相加并返回结果。
///
/// # Examples
///
/// ```
/// use my_crate::add;
///
/// let result = add(2, 3);
/// assert_eq!(result, 5);
/// ```
///
/// 负数也同样适用：
///
/// ```
/// use my_crate::add;
/// assert_eq!(add(-1, -2), -3);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

---

## 异步测试

需要在 `Cargo.toml` 中添加 `tokio` 依赖（启用 `macros` feature）。

```toml
[dev-dependencies]
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

```rust
#[cfg(test)]
mod tests {
    #[tokio::test]
    async fn test_async_function() {
        let result = async_add(1, 2).await;
        assert_eq!(result, 3);
    }

    #[tokio::test(flavor = "multi_thread", worker_threads = 2)]
    async fn test_concurrent() {
        // 多线程异步测试
    }
}
```

---

## 运行测试

### 基本命令

```bash
# 运行所有测试（单元 + 集成 + 文档）
cargo test

# 只运行单元测试
cargo test --lib

# 只运行集成测试
cargo test --tests

# 只运行文档测试
cargo test --doc

# 运行指定名称的测试（模糊匹配）
cargo test test_add

# 运行指定模块的测试
cargo test tests::

# 运行 release 模式的测试
cargo test --release

# 工作空间中所有成员的测试
cargo test --workspace
```

### 控制测试输出

```bash
# 显示 println! 的输出（默认被捕获）
cargo test -- --nocapture

# 串行执行（避免并发问题）
cargo test -- --test-threads=1

# 显示测试执行时间
cargo test -- --report-time

# 列出所有测试而不运行
cargo test -- --list

# 跳过某些测试
cargo test -- --skip slow_test
```

### 过滤测试

```bash
# 只运行包含 "network" 的测试
cargo test network

# 精确匹配测试名称
cargo test -- --exact test_add
```

---

## 测试辅助工具

### 使用 mockall 进行 Mock

```toml
[dev-dependencies]
mockall = "0.12"
```

```rust
use mockall::{automock, predicate::*};

#[automock]
trait Database {
    fn get_user(&self, id: u32) -> Option<String>;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_with_mock() {
        let mut mock = MockDatabase::new();
        mock.expect_get_user()
            .with(eq(1))
            .returning(|_| Some("Alice".to_string()));

        assert_eq!(mock.get_user(1), Some("Alice".to_string()));
    }
}
```

### 使用 tempfile 创建临时文件

```toml
[dev-dependencies]
tempfile = "3"
```

```rust
#[cfg(test)]
mod tests {
    use tempfile::NamedTempFile;
    use std::io::Write;

    #[test]
    fn test_file_operations() {
        let mut temp_file = NamedTempFile::new().unwrap();
        writeln!(temp_file, "test content").unwrap();
        // 测试完成后自动删除
    }
}
```

---

## 代码覆盖率

### 使用 cargo-tarpaulin（Linux）

```bash
cargo install cargo-tarpaulin
cargo tarpaulin --out Html
cargo tarpaulin --out Lcov --output-dir coverage/
```

### 使用 cargo-llvm-cov（跨平台）

```bash
cargo install cargo-llvm-cov
cargo llvm-cov                          # 运行测试并显示覆盖率
cargo llvm-cov --html                   # 生成 HTML 报告
cargo llvm-cov --lcov --output-path lcov.info  # 生成 LCOV 格式
```

---

## 测试最佳实践

1. **测试名称要描述行为**：`test_add_returns_sum_of_two_numbers` 优于 `test1`
2. **每个测试只测试一件事**：保持测试的单一职责
3. **使用 Given-When-Then 结构**组织测试代码
4. **测试边界条件**：零值、最大值、空输入、无效输入
5. **避免在测试中使用 `unwrap()`**：使用 `?` 或更有意义的错误处理
6. **测试应该独立**：不依赖其他测试的执行顺序或状态
7. **不要测试实现细节**：测试公共 API 行为，而非内部实现

```rust
#[cfg(test)]
mod tests {
    use super::*;

    // Given-When-Then 结构示例
    #[test]
    fn test_user_registration_with_valid_email() {
        // Given: 有效的用户信息
        let email = "user@example.com";
        let password = "secure_password123";

        // When: 尝试注册用户
        let result = register_user(email, password);

        // Then: 注册成功
        assert!(result.is_ok());
        let user = result.unwrap();
        assert_eq!(user.email, email);
    }
}
```
