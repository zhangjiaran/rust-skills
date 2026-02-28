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

**在 VS Code 中使用：**

1. 安装 [GitHub Copilot 插件](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
2. 将本仓库的 `.github/copilot-instructions.md` 放入你的项目中（或直接 fork/clone 本仓库）
3. Copilot Chat 会自动将该文件作为上下文，在对话中提供符合 Rust 最佳实践的建议

**在 GitHub.com 中使用：**

1. 打开仓库页面，点击右上角 **Copilot** 图标，进入 Copilot Chat
2. 直接向 Copilot 提问 Rust 相关问题，它会结合 `.github/copilot-instructions.md` 中的规则回答

---

### Cursor

`.cursorrules` 文件会被 Cursor IDE 自动加载为项目级别规则。

**使用步骤：**

1. 将本仓库的 `.cursorrules` 文件复制到你的 Rust 项目根目录
2. 使用 Cursor 打开该项目，规则会自动生效
3. 在 Cursor Chat（`Ctrl+L` / `Cmd+L`）或 Composer（`Ctrl+I` / `Cmd+I`）中提问时，AI 会遵循这些 Rust 规范

**针对特定场景补充上下文：**

在 Cursor Chat 中，可以用 `@file` 引用 `skills/` 目录下的文档，例如：

```text
@skills/03-unit-testing.md 帮我为这个函数写单元测试
```

---

### Windsurf

1. 将 `.cursorrules` 文件重命名或复制为项目根目录下的 `.windsurfrules`
2. Windsurf 会自动加载该规则文件，在 Cascade AI 对话中应用 Rust 编码规范

---

### Cline / Continue（VS Code 插件）

1. 在插件设置中找到 **System Prompt** 或 **Custom Instructions** 配置项
2. 将 `.github/copilot-instructions.md` 或 `skills/` 下对应文件的内容粘贴为系统提示词
3. 之后在该插件的对话窗口中提问，AI 会按照规则辅助 Rust 开发

---

### Claude / 其他 AI 对话工具

将 `skills/` 目录下对应场景的 Markdown 文件内容粘贴到对话上下文中，或作为系统提示词使用。

**推荐使用方式：**

- **按需引入**：只粘贴与当前任务相关的文档，减少无关上下文干扰  
  例如：只需要写测试时，粘贴 `skills/03-unit-testing.md`
- **全量引入**：将所有 `skills/` 文档合并后作为系统提示词，适合需要覆盖完整 Rust 工作流的场景
- **对话开头声明**：在每次新对话开始时，告知 AI "请参考以下 Rust 开发规范" 并附上文档内容

**快速复制命令（合并所有 skills）：**

```bash
cat skills/*.md | pbcopy        # macOS
cat skills/*.md | xclip         # Linux
cat skills/*.md | clip          # Windows
```

---

### 通用建议

| AI 工具 | 推荐配置方式 |
| ------- | ------------ |
| GitHub Copilot | 自动读取 `.github/copilot-instructions.md` |
| Cursor | 自动读取 `.cursorrules`，可配合 `@file` 引用 skills 文档 |
| Windsurf | 自动读取 `.windsurfrules`（将 `.cursorrules` 重命名） |
| Cline / Continue | 在插件 System Prompt 中粘贴文档内容 |
| Claude / ChatGPT / 其他 | 在对话开头粘贴对应 skills 文档内容 |
