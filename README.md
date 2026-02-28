# rust-skills

该项目由 GitHub Copilot 生成，提供针对 Rust 开发的通用 skills，辅助开发者更好地调度 Rust 工程工具。Skills 可在 AI 编程工具（Cursor、Claude、码道代码智能体等）上直接应用。

## 包含内容

| 文件 | 说明 |
| ------ | ------ |
| [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | GitHub Copilot 自定义指令 |
| [`.cursorrules`](.cursorrules) | Cursor IDE 规则配置 |
| [`skills/01-installation.md`](skills/01-installation.md) | Rust 安装与工具链管理 |
| [`skills/02-development.md`](skills/02-development.md) | Rust 项目开发实践 |
| [`skills/03-unit-testing.md`](skills/03-unit-testing.md) | 单元测试与集成测试 |
| [`skills/04-code-check.md`](skills/04-code-check.md) | 代码检查与静态分析 |
| [`skills/05-cargo-build.md`](skills/05-cargo-build.md) | Cargo 构建与发布 |

## 覆盖场景

- **Rust 安装**：rustup 安装、工具链管理、组件安装、跨平台目标、国内镜像配置
- **项目开发**：Cargo 项目创建、依赖管理、模块系统、错误处理、异步编程
- **UT 测试**：单元测试、集成测试、文档测试、异步测试、Mock、代码覆盖率
- **代码检查**：rustfmt 格式化、Clippy Lint、cargo audit 安全审计、CI 集成
- **Cargo 构建**：构建 Profile、Features、跨平台编译、工作空间、构建脚本、发布

## 如何使用

### GitHub Copilot

`.github/copilot-instructions.md` 会被 GitHub Copilot 自动读取，无需额外配置。

### Cursor

`.cursorrules` 文件会被 Cursor IDE 自动加载为项目级别规则。

### Claude / 其他 AI 工具

将 `skills/` 目录下对应场景的 Markdown 文件内容粘贴到对话上下文中，或作为系统提示词使用。
