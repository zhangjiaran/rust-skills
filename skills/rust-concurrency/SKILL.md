---
name: rust-concurrency
description: Write concurrent Rust programs. Use when you need to spawn threads, share state between threads, use channels for message passing, or leverage parallel iterators with Rayon.
---

# Rust 并发编程 (Concurrency in Rust)

本文档介绍 Rust 中安全并发的核心机制：线程、通道、共享状态及并行迭代器。

---

## 线程基础

### 创建线程

```rust
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        println!("子线程运行中");
    });

    // 等待线程完成
    handle.join().unwrap();
    println!("主线程");
}
```

### 传值到线程（move 闭包）

```rust
use std::thread;

fn main() {
    let data = vec![1, 2, 3];

    // move 将所有权转移给线程
    let handle = thread::spawn(move || {
        println!("{:?}", data);
    });

    handle.join().unwrap();
}
```

### 线程配置

```rust
use std::thread;

let handle = thread::Builder::new()
    .name("worker".to_string())
    .stack_size(4 * 1024 * 1024) // 4MB 栈
    .spawn(|| {
        println!("线程名: {:?}", thread::current().name());
    })
    .unwrap();

handle.join().unwrap();
```

---

## 消息传递（Channel）

### mpsc — 多生产者单消费者

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel::<String>();

    // 克隆发送端，支持多个生产者
    let tx2 = tx.clone();

    thread::spawn(move || {
        tx.send("来自线程1".to_string()).unwrap();
    });
    thread::spawn(move || {
        tx2.send("来自线程2".to_string()).unwrap();
    });

    // 接收（blocking）
    for msg in rx {
        println!("收到: {}", msg);
    }
}
```

### 同步 Channel（有界缓冲）

```rust
use std::sync::mpsc;

// sync_channel(N)：缓冲区满时 send 会阻塞
let (tx, rx) = mpsc::sync_channel::<i32>(10);
```

---

## 共享状态

### Arc — 跨线程引用计数

```rust
use std::sync::Arc;
use std::thread;

fn main() {
    let data = Arc::new(vec![1, 2, 3]);

    let handles: Vec<_> = (0..3).map(|_| {
        let data = Arc::clone(&data);
        thread::spawn(move || println!("{:?}", data))
    }).collect();

    for h in handles { h.join().unwrap(); }
}
```

### Mutex — 互斥锁（可变共享状态）

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0u32));

    let handles: Vec<_> = (0..10).map(|_| {
        let counter = Arc::clone(&counter);
        thread::spawn(move || {
            let mut lock = counter.lock().unwrap();
            *lock += 1;
        })
    }).collect();

    for h in handles { h.join().unwrap(); }
    println!("最终计数: {}", *counter.lock().unwrap()); // 10
}
```

### RwLock — 读写锁（多读单写）

```rust
use std::sync::{Arc, RwLock};
use std::thread;

fn main() {
    let data = Arc::new(RwLock::new(vec![1, 2, 3]));

    // 多个读锁可同时持有
    let r1 = Arc::clone(&data);
    let r2 = Arc::clone(&data);
    let reader1 = thread::spawn(move || println!("{:?}", r1.read().unwrap()));
    let reader2 = thread::spawn(move || println!("{:?}", r2.read().unwrap()));

    // 写锁独占
    let w = Arc::clone(&data);
    let writer = thread::spawn(move || w.write().unwrap().push(4));

    reader1.join().unwrap();
    reader2.join().unwrap();
    writer.join().unwrap();
}
```

### 原子类型（无锁操作）

```rust
use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::thread;

fn main() {
    let count = Arc::new(AtomicUsize::new(0));

    let handles: Vec<_> = (0..10).map(|_| {
        let count = Arc::clone(&count);
        thread::spawn(move || {
            count.fetch_add(1, Ordering::SeqCst);
        })
    }).collect();

    for h in handles { h.join().unwrap(); }
    println!("计数: {}", count.load(Ordering::SeqCst)); // 10
}
```

---

## 线程池（Rayon — 数据并行）

适用于 CPU 密集型计算，基于工作窃取（work-stealing）调度。

```toml
[dependencies]
rayon = "1"
```

### 并行迭代器

```rust
use rayon::prelude::*;

fn main() {
    let nums: Vec<i64> = (1..=1_000_000).collect();

    // par_iter() 替换 iter() 即可并行化
    let sum: i64 = nums.par_iter().sum();
    println!("sum = {}", sum);

    // 并行 map + filter + collect
    let evens: Vec<i64> = nums.par_iter()
        .filter(|&&n| n % 2 == 0)
        .map(|&n| n * n)
        .collect();
    println!("偶数平方数量: {}", evens.len());

    // 并行排序
    let mut data = vec![5, 3, 1, 4, 2];
    data.par_sort();
    println!("{:?}", data);
}
```

### 并行 for_each

```rust
use rayon::prelude::*;

fn main() {
    (0..100u32).into_par_iter().for_each(|i| {
        // 每个 i 在不同线程上并行处理
        println!("处理 {}", i);
    });
}
```

### 自定义线程池

```rust
use rayon::ThreadPoolBuilder;

fn main() {
    let pool = ThreadPoolBuilder::new()
        .num_threads(4)
        .build()
        .unwrap();

    pool.install(|| {
        use rayon::prelude::*;
        let sum: i64 = (1..=100).into_par_iter().sum();
        println!("sum = {}", sum);
    });
}
```

---

## 同步原语

### Barrier — 等待所有线程到达同一点

```rust
use std::sync::{Arc, Barrier};
use std::thread;

fn main() {
    let barrier = Arc::new(Barrier::new(5));

    let handles: Vec<_> = (0..5).map(|i| {
        let barrier = Arc::clone(&barrier);
        thread::spawn(move || {
            println!("线程 {} 准备就绪", i);
            barrier.wait(); // 所有 5 个线程都到达后继续
            println!("线程 {} 开始执行", i);
        })
    }).collect();

    for h in handles { h.join().unwrap(); }
}
```

### Once — 只执行一次的初始化

```rust
use std::sync::Once;

static INIT: Once = Once::new();
static mut CONFIG: Option<String> = None;

fn get_config() -> &'static str {
    INIT.call_once(|| unsafe {
        CONFIG = Some("已初始化配置".to_string());
    });
    unsafe { CONFIG.as_deref().unwrap() }
}
```

---

## 常见问题与最佳实践

### 避免死锁

```rust
// ❌ 不好：持有锁的同时调用可能也要获取锁的函数
{
    let _lock = mutex.lock().unwrap();
    some_function_that_might_lock_same_mutex(); // 死锁风险
}

// ✅ 好：限制锁的作用域
{
    let _lock = mutex.lock().unwrap();
    // 只做必要的操作
} // 锁在此处释放
```

### 恐慌（panic）时锁中毒

```rust
use std::sync::Mutex;

let m = Mutex::new(0);
let result = m.lock();
match result {
    Ok(guard) => { /* 正常 */ let _ = guard; }
    Err(poisoned) => {
        // 其他线程 panic 时锁中毒，可以恢复
        let guard = poisoned.into_inner();
        let _ = guard;
    }
}
```

### Send 和 Sync Trait

```rust
// 可跨线程转移所有权
// T: Send    —— Arc<T> 要求 T: Send + Sync
// 可跨线程共享引用
// T: Sync    —— &T: Send 等价于 T: Sync

// Rc<T>、RefCell<T>、裸指针：既不 Send 也不 Sync
// Arc<T>：T: Send + Sync 时，Arc<T>: Send + Sync
// Mutex<T>：T: Send 时，Mutex<T>: Send + Sync
```
