---
name: rust-cli
description: Build command-line interface applications in Rust. Use when you need to parse CLI arguments, define subcommands, handle environment variables, read stdin, or output colored/formatted text.
---

# Rust CLI 开发 (Building CLI Applications in Rust)

本文档介绍如何使用 Rust 构建命令行应用程序，重点介绍 Clap 参数解析库的使用方法。

---

## 添加依赖

```toml
[dependencies]
clap = { version = "4", features = ["derive"] }

# 可选：彩色输出
colored = "2"

# 可选：进度条
indicatif = "0.17"

# 可选：交互式提示
dialoguer = "0.11"
```

---

## Clap — 参数解析

### Derive API（推荐）

```rust
use clap::Parser;

/// 一个简单的文件处理工具
#[derive(Parser, Debug)]
#[command(name = "mytool", version, author, about)]
struct Cli {
    /// 输入文件路径
    input: String,

    /// 输出文件路径（可选，默认输出到 stdout）
    #[arg(short, long)]
    output: Option<String>,

    /// 详细输出模式（可多次指定，如 -vvv）
    #[arg(short, long, action = clap::ArgAction::Count)]
    verbose: u8,

    /// 强制覆盖已存在的文件
    #[arg(short, long, default_value_t = false)]
    force: bool,
}

fn main() {
    let cli = Cli::parse();
    println!("输入: {}", cli.input);
    println!("详细级别: {}", cli.verbose);
}
```

### 子命令（Subcommands）

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "git-like", about = "类似 Git 的 CLI 工具")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// 初始化仓库
    Init {
        /// 仓库路径
        path: Option<String>,
    },
    /// 添加文件
    Add {
        /// 要添加的文件
        #[arg(required = true)]
        files: Vec<String>,
    },
    /// 提交变更
    Commit {
        /// 提交信息
        #[arg(short, long)]
        message: String,
    },
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::Init { path } => {
            println!("初始化: {:?}", path);
        }
        Commands::Add { files } => {
            println!("添加文件: {:?}", files);
        }
        Commands::Commit { message } => {
            println!("提交: {}", message);
        }
    }
}
```

### 参数类型与验证

```rust
use clap::Parser;
use std::path::PathBuf;

#[derive(Parser)]
struct Cli {
    /// 整数参数
    #[arg(short, long, default_value_t = 8080)]
    port: u16,

    /// 文件路径（自动验证存在性）
    #[arg(short, long)]
    config: Option<PathBuf>,

    /// 枚举选项
    #[arg(short, long, value_enum, default_value_t = Format::Json)]
    format: Format,

    /// 数值范围限制
    #[arg(long, value_parser = clap::value_parser!(u32).range(1..=100))]
    threads: Option<u32>,
}

#[derive(clap::ValueEnum, Clone, Debug)]
enum Format {
    Json,
    Yaml,
    Toml,
}
```

### 环境变量支持

```rust
use clap::Parser;

#[derive(Parser)]
struct Cli {
    /// API 密钥（也可通过 APP_API_KEY 环境变量设置）
    #[arg(long, env = "APP_API_KEY")]
    api_key: String,

    /// 服务地址（优先级：命令行参数 > 环境变量 > 默认值）
    #[arg(long, env = "APP_HOST", default_value = "localhost")]
    host: String,
}
```

---

## 读取标准输入

### 逐行读取 stdin

```rust
use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        let line = line.unwrap();
        println!("处理: {}", line);
    }
}
```

### 支持文件或 stdin

```rust
use std::fs::File;
use std::io::{self, BufRead, BufReader};

fn open_input(path: Option<&str>) -> Box<dyn BufRead> {
    match path {
        Some(p) => Box::new(BufReader::new(File::open(p).unwrap())),
        None => Box::new(io::stdin().lock()),
    }
}

fn main() {
    let reader = open_input(std::env::args().nth(1).as_deref());
    for line in reader.lines() {
        println!("{}", line.unwrap());
    }
}
```

---

## 彩色与格式化输出

### colored 库

```toml
[dependencies]
colored = "2"
```

```rust
use colored::Colorize;

fn main() {
    println!("{}", "错误".red().bold());
    println!("{}", "成功".green());
    println!("{}", "警告".yellow());
    println!("{} {}", "INFO:".blue(), "应用已启动");
    println!("{}", "下划线文本".underline());

    // 背景色
    println!("{}", "高亮".on_yellow().black());
}
```

### 格式化表格（comfy-table）

```toml
[dependencies]
comfy-table = "7"
```

```rust
use comfy_table::{Table, presets::UTF8_FULL};

fn main() {
    let mut table = Table::new();
    table.load_preset(UTF8_FULL)
        .set_header(["名称", "版本", "描述"])
        .add_row(["clap", "4.x", "命令行参数解析"])
        .add_row(["tokio", "1.x", "异步运行时"])
        .add_row(["serde", "1.x", "序列化/反序列化"]);
    println!("{table}");
}
```

---

## 进度条（indicatif）

```toml
[dependencies]
indicatif = "0.17"
```

```rust
use indicatif::{ProgressBar, ProgressStyle};
use std::thread::sleep;
use std::time::Duration;

fn main() {
    let pb = ProgressBar::new(100);
    pb.set_style(
        ProgressStyle::with_template(
            "{spinner:.green} [{elapsed_precise}] [{wide_bar:.cyan/blue}] {pos}/{len} ({eta})"
        )
        .unwrap()
        .progress_chars("=>-"),
    );

    for _ in 0..100 {
        pb.inc(1);
        sleep(Duration::from_millis(20));
    }
    pb.finish_with_message("完成");
}
```

---

## 退出码规范

```rust
use std::process;

fn main() {
    match run() {
        Ok(()) => {}
        Err(e) => {
            eprintln!("错误: {}", e);
            process::exit(1);
        }
    }
}

fn run() -> Result<(), Box<dyn std::error::Error>> {
    // 应用逻辑
    Ok(())
}
```

### 标准退出码

| 退出码 | 含义 |
| ------ | ---- |
| `0` | 成功 |
| `1` | 通用错误 |
| `2` | 参数使用错误 |
| `126` | 命令不可执行 |
| `127` | 命令未找到 |

---

## 配置文件支持

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
toml = "0.8"
dirs = "5"
```

```rust
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

#[derive(Debug, Serialize, Deserialize, Default)]
struct Config {
    host: Option<String>,
    port: Option<u16>,
    api_key: Option<String>,
}

impl Config {
    fn load() -> Self {
        let path = config_path();
        if path.exists() {
            let content = std::fs::read_to_string(&path).unwrap_or_default();
            toml::from_str(&content).unwrap_or_default()
        } else {
            Self::default()
        }
    }
}

fn config_path() -> PathBuf {
    dirs::config_dir()
        .unwrap_or_else(|| PathBuf::from("."))
        .join("mytool")
        .join("config.toml")
}
```

---

## 测试 CLI

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use clap::CommandFactory;

    #[test]
    fn verify_cli() {
        // 验证 CLI 定义本身不含错误
        Cli::command().debug_assert();
    }

    #[test]
    fn test_default_args() {
        let cli = Cli::parse_from(["mytool", "input.txt"]);
        assert_eq!(cli.input, "input.txt");
        assert!(!cli.force);
    }
}
```
