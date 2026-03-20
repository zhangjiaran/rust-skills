# Rust 优质代码仓收藏

全网收集的 Rust 相关高使用度代码仓，按 Star 数量从高到低排列（数据截至 2026-03-20）。

## 目录

- [练习与教程](#练习与教程)
- [参考资料与索引](#参考资料与索引)
- [算法与数据结构](#算法与数据结构)
- [本地镜像仓库](#本地镜像仓库)

---

## 练习与教程

| 仓库 | Stars | 简介 |
| ---- | ----- | ---- |
| [rust-lang/rustlings](https://github.com/rust-lang/rustlings) | ⭐ 62k+ | 官方出品的小练习集，通过读写代码快速熟悉 Rust |
| [google/comprehensive-rust](https://github.com/google/comprehensive-rust) | ⭐ 32k+ | Google Android 团队出品的 Rust 培训课程，覆盖从基础到高级 |
| [sunface/rust-course](https://github.com/sunface/rust-course) | ⭐ 30k+ | 目前最用心的 Rust 中文学习教程，内容全面深入 |
| [sunface/rust-by-practice](https://github.com/sunface/rust-by-practice) | ⭐ 14k+ | 通过实例和练习缩短 Rust 初学者到熟练开发者的距离 |
| [mainmatter/100-exercises-to-learn-rust](https://github.com/mainmatter/100-exercises-to-learn-rust) | ⭐ 9k+ | 自学 Rust 的 100 道练习题，一次一题，循序渐进 |

## 参考资料与索引

| 仓库 | Stars | 简介 |
| ---- | ----- | ---- |
| [rust-unofficial/awesome-rust](https://github.com/rust-unofficial/awesome-rust) | ⭐ 56k+ | Rust 代码与资源精选列表，是发现 Rust 优质项目的最佳入口 |

## 算法与数据结构

| 仓库 | Stars | 简介 |
| ---- | ----- | ---- |
| [TheAlgorithms/Rust](https://github.com/TheAlgorithms/Rust) | ⭐ 25k+ | 所有经典算法的 Rust 实现，涵盖排序、搜索、图算法等 |

---

## 本地镜像仓库

以下仓库已通过 git submodule 克隆到本代码仓的 `resources/rust-repos/` 目录下，可直接离线查阅：

| 本地路径 | 对应远程仓库 |
| -------- | ------------ |
| `resources/rust-repos/rustlings` | [rust-lang/rustlings](https://github.com/rust-lang/rustlings) |
| `resources/rust-repos/comprehensive-rust` | [google/comprehensive-rust](https://github.com/google/comprehensive-rust) |
| `resources/rust-repos/rust-course` | [sunface/rust-course](https://github.com/sunface/rust-course) |
| `resources/rust-repos/rust-by-practice` | [sunface/rust-by-practice](https://github.com/sunface/rust-by-practice) |
| `resources/rust-repos/100-exercises-to-learn-rust` | [mainmatter/100-exercises-to-learn-rust](https://github.com/mainmatter/100-exercises-to-learn-rust) |
| `resources/rust-repos/awesome-rust` | [rust-unofficial/awesome-rust](https://github.com/rust-unofficial/awesome-rust) |
| `resources/rust-repos/algorithms-rust` | [TheAlgorithms/Rust](https://github.com/TheAlgorithms/Rust) |

初次克隆本仓库后，执行以下命令初始化并更新所有子模块：

```bash
git submodule update --init --recursive
```

如需拉取子模块最新内容：

```bash
git submodule update --remote --merge
```
