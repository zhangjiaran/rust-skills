---
name: rust-async
description: Write async Rust code with async/await and Tokio runtime. Use when you need to implement async functions, manage async tasks, work with futures, use async I/O, or integrate Tokio-based libraries.
---

# Rust 异步编程 (Async Programming in Rust)

本文档介绍如何在 Rust 中使用 `async/await` 语法和 Tokio 运行时进行异步编程。

## 添加 Tokio 依赖

```toml
# Cargo.toml
[dependencies]
tokio = { version = "1", features = ["full"] }
```

常用 feature 组合：

```toml
# 最小化引入（仅 runtime + I/O + 时间）
tokio = { version = "1", features = ["rt-multi-thread", "io-util", "time"] }

# 仅单线程运行时
tokio = { version = "1", features = ["rt", "macros"] }
```

---

## 基础 async/await

### 定义和调用异步函数

```rust
use tokio::time::{sleep, Duration};

// 定义异步函数
async fn fetch_data(url: &str) -> String {
    // 模拟网络延迟
    sleep(Duration::from_millis(100)).await;
    format!("data from {}", url)
}

// 主函数使用 #[tokio::main] 宏
#[tokio::main]
async fn main() {
    let result = fetch_data("https://example.com").await;
    println!("{}", result);
}
```

### 单线程运行时

```rust
#[tokio::main(flavor = "current_thread")]
async fn main() {
    // 适合嵌入式或对并发需求低的场景
}
```

---

## 并发执行任务

### tokio::join! — 并发等待多个 Future

```rust
use tokio::time::{sleep, Duration};

async fn task_a() -> &'static str { sleep(Duration::from_millis(50)).await; "A" }
async fn task_b() -> &'static str { sleep(Duration::from_millis(30)).await; "B" }

#[tokio::main]
async fn main() {
    // 并发运行，等所有都完成
    let (a, b) = tokio::join!(task_a(), task_b());
    println!("{} {}", a, b); // "A B"
}
```

### tokio::select! — 竞争等待，取最先完成的

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    tokio::select! {
        result = task_a() => println!("A 先完成: {}", result),
        result = task_b() => println!("B 先完成: {}", result),
    }
}
```

### tokio::spawn — 派生后台任务

```rust
use tokio::task::JoinHandle;

#[tokio::main]
async fn main() {
    let handle: JoinHandle<u32> = tokio::spawn(async {
        // 在单独任务中运行
        42
    });

    let result = handle.await.unwrap(); // 等待任务完成
    println!("result = {}", result);
}
```

### futures::join_all — 并发等待 Vec 中的 Future

```toml
[dependencies]
futures = "0.3"
```

```rust
use futures::future::join_all;

#[tokio::main]
async fn main() {
    let urls = vec!["url1", "url2", "url3"];
    let futures: Vec<_> = urls.iter().map(|u| fetch_data(u)).collect();
    let results = join_all(futures).await;
    for r in results {
        println!("{}", r);
    }
}
```

---

## 异步 I/O

### 文件读写

```rust
use tokio::fs;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::main]
async fn main() -> std::io::Result<()> {
    // 读取文件
    let content = fs::read_to_string("file.txt").await?;

    // 写入文件
    fs::write("output.txt", b"hello async").await?;

    // 低层次读写
    let mut file = fs::File::open("file.txt").await?;
    let mut buf = Vec::new();
    file.read_to_end(&mut buf).await?;

    Ok(())
}
```

### TCP 网络

```rust
use tokio::net::{TcpListener, TcpStream};
use tokio::io::{AsyncReadExt, AsyncWriteExt};

// 服务端
#[tokio::main]
async fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:8080").await?;
    loop {
        let (mut socket, _addr) = listener.accept().await?;
        tokio::spawn(async move {
            let mut buf = [0u8; 1024];
            let n = socket.read(&mut buf).await.unwrap();
            socket.write_all(&buf[..n]).await.unwrap(); // echo
        });
    }
}
```

---

## 超时控制

```rust
use tokio::time::{timeout, Duration};

#[tokio::main]
async fn main() {
    match timeout(Duration::from_secs(5), fetch_data("https://example.com")).await {
        Ok(data) => println!("成功: {}", data),
        Err(_) => println!("超时"),
    }
}
```

---

## 异步 Channel（消息传递）

### mpsc — 多生产者单消费者

```rust
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel::<String>(32); // 缓冲区大小 32

    // 生产者
    let tx2 = tx.clone();
    tokio::spawn(async move {
        tx.send("消息1".to_string()).await.unwrap();
    });
    tokio::spawn(async move {
        tx2.send("消息2".to_string()).await.unwrap();
    });

    // 消费者
    while let Some(msg) = rx.recv().await {
        println!("收到: {}", msg);
    }
}
```

### oneshot — 单次响应

```rust
use tokio::sync::oneshot;

#[tokio::main]
async fn main() {
    let (tx, rx) = oneshot::channel::<u32>();
    tokio::spawn(async move { tx.send(42).unwrap(); });
    let value = rx.await.unwrap();
    println!("got {}", value);
}
```

---

## 异步 Mutex / RwLock

```rust
use tokio::sync::{Mutex, RwLock};
use std::sync::Arc;

#[tokio::main]
async fn main() {
    // Mutex
    let counter = Arc::new(Mutex::new(0u32));
    let c = counter.clone();
    tokio::spawn(async move {
        let mut lock = c.lock().await;
        *lock += 1;
    }).await.unwrap();

    // RwLock（多读单写）
    let data = Arc::new(RwLock::new(vec![1, 2, 3]));
    let r = data.read().await;
    println!("{:?}", *r);
}
```

---

## 异步 Trait（Rust 1.75+）

```rust
use std::future::Future;

// Rust 1.75+ 起，async fn 可直接用于 trait
trait Fetcher {
    async fn fetch(&self, url: &str) -> String;
}

// 老版本或需要 dyn Trait 时，用 async-trait 库
// cargo add async-trait
use async_trait::async_trait;

#[async_trait]
trait FetcherDyn {
    async fn fetch(&self, url: &str) -> String;
}
```

---

## 常见问题

### Future 不是 Send 导致无法 spawn

```rust
// 错误：non-Send future
// tokio::spawn 要求 Future: Send
// 解决：确保所有跨 .await 持有的值实现 Send
// 避免在 .await 点持有 Rc、RefCell 或裸指针

use std::sync::Arc; // 用 Arc 替代 Rc
```

### 阻塞操作放在 spawn_blocking

```rust
#[tokio::main]
async fn main() {
    // CPU 密集或阻塞型同步代码放到专用线程池
    let result = tokio::task::spawn_blocking(|| {
        // 耗时的同步计算
        (0..1_000_000u64).sum::<u64>()
    }).await.unwrap();
    println!("{}", result);
}
```
