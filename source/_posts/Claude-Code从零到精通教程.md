---
title: Claude Code从零到精通教程
date: 2026-03-31 17:41:18
tags:
  - Claude Code
  - AI开发
  - Agent
categories:
  - claude
copyright:
---

> 基于一线开发者实战经验，结合官方文档与社区最佳实践整理
> 适用版本：Claude Code + Claude Opus 4.6（2026年3月）

<!-- more -->

# Claude Code 从零到精通：多Agent协作开发完全教程

基于一线开发者实战经验，结合官方文档与社区最佳实践整理

适用版本：Claude Code + Claude Opus 4.6（2026年3月）

文档更新：第七章、第九章、第十二章、第十三章 0311更新


## 目录

## 第一章：认识AI开发的演进之路

## 第二章：Claude Code 安装与入门

## 第三章：CLAUDE.md — 你的开发规范圣经

## 第四章：Skills 技能系统

## 第五章：Plugins 插件系统

## 第六章：MCP Servers — 连接外部世界

## 第七章：Hooks 事件钩子

## 第八章：Subagents 子Agent

## 第九章：Agent Teams — 多Agent协作开发

## 第十章：上下文管理 — 核心中的核心

## 第十一章：开发范式与实战案例

## 第十二章：OpenClaw — 用手机遥控 Claude Code 7×24 小时工作

## 第十三章：常见问题与进阶技巧


## 第一章：认识AI开发的演进之路

在学习 Claude Code 之前，了解 AI 辅助开发的演进历程，能帮你理解为什么今天的工具如此强大。

### 1.1 AI开发工具的四个阶段


```
┌─────────────────────────────────────────────────────────────────┐
│                    AI 开发工具演进路线图                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  阶段1: 网页版大模型 (2023-)                                     │
│  ┌──────────────┐                                               │
│  │  ChatGPT 等   │ → 复制粘贴代码，需要行业背景才能用好            │
│  │  网页对话框    │ → 无法访问本地文件，无法操作终端                 │
│  └──────────────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  阶段2: IDE内嵌助手 (2023-2024)                                  │
│  ┌──────────────┐                                               │
│  │  Copilot      │ → 只能在当前文件内辅助，写写排序等简单功能       │
│  │  当前文件级    │ → 无法理解项目整体架构                         │
│  └──────────────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  阶段3: 项目级AI工具 (2024-2025)                                 │
│  ┌──────────────┐                                               │
│  │  Cursor 等    │ → 可以访问项目目录下所有文件                    │
│  │  项目目录级    │ → 能发现代码中隐藏的关联和问题                  │
│  │              │ → 但无法探索外部世界，多窗口不能通信              │
│  └──────────────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  阶段4: Agent级开发工具 (2025-2026) ← 我们在这里！               │
│  ┌──────────────┐                                               │
│  │  Claude Code  │ → 可操作终端、SSH远程机器、访问外部世界          │
│  │  + Agent Teams│ → 多Agent并行开发、互相通信纠错                 │
│  │  终端+多Agent │ → 可持续数小时自主工作                          │
│  └──────────────┘                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```


### 1.2 为什么现在能做到如此大的提效？

根据实战经验，有三个关键变化推动了 AI 开发的质变：


| 变化 | 说明 | 影响 |
| --- | --- | --- |
| 模型能力跃升 | Claude Opus 4.6 对外部世界的探索和理解能力大幅增强 | 可以 SSH 远程机器、理解复杂终端工具、持续探索 |
| Agent Teams 协作 | 多个 Agent 可以并行工作且互相通信 | 原来3小时的任务，6个Agent并行半小时完成 |
| Agent间互相纠错 | Agent之间可以发现彼此的问题并纠正 | 减少人工干预，提高代码质量 |


实战数据：一个复杂的科创实验制作工具项目，使用 Agent Teams 6小时完成了整体框架搭建，综合提效约 5倍。


## 第二章：Claude Code 安装与入门

### 2.1 安装 Claude Code

📖 官方安装文档：https://docs.anthropic.com/en/docs/claude-code/quickstart方式一：官方脚本安装（推荐，支持自动更新）macOS / Linux / WSL：


```bash
curl -fsSL https://claude.ai/install.sh | bash
```


Windows PowerShell：


```powershell
irm https://claude.ai/install.ps1 | iex
```


方式二：Homebrew 安装（macOS）


```bash
brew install --cask claude-code
```


方式三：npm 安装（备选，环境兼容性最好）

⚠️ 官方脚本安装可能因为网络环境、权限问题、代理配置等原因失败。如果你遇到安装卡住或报错，可以直接用 npm 安装，效果完全一样。

前提：已安装 Node.js v18+。

📖 如果你是零基础，安装过程中遇到任何问题，推荐阅读这篇保姆级教程：小白如何从0到1安装上Claude Code，涵盖环境准备、常见报错解决等。


```bash
npm install -g @anthropic-ai/claude-code
```


安装完成后，终端输入 `claude` 即可启动。方式四：WinGet 安装（Windows）


```powershell
winget install Anthropic.ClaudeCode
```


💡 安装方式对比：


| 方式 | 自动更新 | 适用场景 |
| --- | --- | --- |
| 官方脚本 | ✅ 自动 | 网络畅通时首选 |
| npm | ❌ 需手动 npm update -g @anthropic-ai/claude-code | 官方脚本装不上时用 |
| Homebrew | ❌ 需手动 brew upgrade claude-code | macOS 用户习惯 brew |
| WinGet | ❌ 需手动 winget upgrade | Windows 用户 |


### 2.2 登录账号


```bash
claude          # 首次使用会提示登录
/login          # 在会话中切换账号
```


支持的账号类型：

Claude Pro/Max/Teams/Enterprise（推荐，Max 计划可用 Opus 模型）

Claude Console（API 按量付费）

Amazon Bedrock / Google Vertex AI（企业云服务商）

### 2.3 第一次使用


```bash
cd /path/to/your/project    # 进入你的项目目录
claude                       # 启动 Claude Code
```


试试这些命令：


```
这个项目是做什么的？           # 让 Claude 分析项目
这个项目用了哪些技术栈？        # 了解技术栈
帮我解释一下 src/ 目录结构      # 理解项目结构
```


### 2.4 核心命令速查表


| 命令 | 作用 | 示例 |
| --- | --- | --- |
| claude | 启动交互模式 | claude |
| claude "任务" | 执行一次性任务 | claude "修复构建错误" |
| claude -p "查询" | 单次查询后退出 | claude -p "解释这个函数" |
| claude -c | 继续最近会话 | claude -c |
| claude -r | 恢复历史会话 | claude -r |
| /clear | 清空上下文 | 任务切换时使用 |
| /compact | 压缩上下文 | /compact 保留API变更 |
| /help | 查看帮助 | /help |
| Esc | 停止当前操作 | 发现方向错误时按 |
| Esc + Esc | 打开回滚菜单 | 恢复到之前的状态 |


### 2.5 工具生态全景


```
┌──────────────────────────────────────────────────────────┐
│                Claude Code 工具生态全景                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │  CLAUDE.md   │  │   Skills    │  │  Plugins    │      │
│  │  项目规范     │  │   技能/工作流│  │  插件集合    │      │
│  │  .claude/md  │  │  .claude/   │  │  社区市场    │      │
│  │              │  │  skills/    │  │             │      │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      │
│         │                │                │              │
│  ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐      │
│  │   Hooks     │  │  Subagents  │  │ MCP Servers │      │
│  │   事件钩子   │  │   子Agent   │  │  外部工具    │      │
│  │  settings   │  │  .claude/   │  │  settings   │      │
│  │  .json      │  │  agents/    │  │  .json      │      │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘      │
│         │                │                │              │
│         └────────────────┼────────────────┘              │
│                          │                               │
│                  ┌───────┴───────┐                       │
│                  │  Agent Teams  │                       │
│                  │  多Agent协作   │                       │
│                  │  团队开发模式  │                       │
│                  └───────────────┘                       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```


### 2.6 设置指令白名单 — 告别反复确认

刚开始用 Claude Code 你会发现，它每次读文件、改文件、跑命令都要弹窗问你"是否允许"。频繁确认非常打断心流。通过设置权限白名单，你可以让常用操作自动放行。

#### 方式一：交互式添加（最简单）

在 Claude Code 中运行：


```
/permissions
```


会打开权限管理界面，你可以直接添加允许的工具和命令。或者，当 Claude 弹出确认时，选择 "Always allow"（始终允许），该操作会被自动加入白名单。

#### 方式二：编辑 settings.json（推荐，一次配齐）

编辑项目级配置 `.claude/settings.json`（仅当前项目生效）：


```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm test)",
      "Bash(npm run *)",
      "Bash(npx *)",
      "Bash(node *)",
      "Bash(ls *)",
      "Bash(cat *)",
      "Bash(mkdir *)",
      "Bash(cp *)",
      "Read",
      "Write",
      "Edit",
      "Glob",
      "Grep"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)"
    ]
  }
}
```


或编辑全局配置 `~/.claude/settings.json`（所有项目生效）。

#### 白名单语法说明


| 语法 | 含义 | 示例 |
| --- | --- | --- |
| Read | 允许读取任意文件 | 不再弹确认 |
| Edit | 允许编辑任意文件 | 不再弹确认 |
| Write | 允许创建新文件 | 不再弹确认 |
| Bash(命令 *) | 允许匹配的 bash 命令 | Bash(git *) 允许所有 git 命令 |
| Bash(精确命令) | 允许特定命令 | Bash(npm test) 只允许 npm test |
| WebFetch | 允许抓取网页 | 不再弹确认 |
| deny 列表优先级高于 allow，用于拦截危险操作。 |  |  |


#### 方式三：命令行参数（临时生效）

启动时指定白名单，仅本次会话有效：


```bash
claude --allowedTools "Edit,Bash(git *),Bash(npm test)"
```


适合批量脚本或 CI 场景。

#### 方式四：直接跳过所有权限（谨慎使用）


```bash
claude --dangerously-skip-permissions
```


⚠️ 这会跳过所有权限检查，Claude 可以执行任意命令。仅建议在容器/沙箱环境中使用，或搭配 OpenClaw 做无人值守任务时使用。

#### 推荐的白名单配置

日常开发（安全 + 高效）：


```json
{
  "permissions": {
    "allow": [
      "Read", "Edit", "Write", "Glob", "Grep",
      "Bash(git *)",
      "Bash(npm *)", "Bash(npx *)", "Bash(node *)",
      "Bash(ls *)", "Bash(cat *)", "Bash(mkdir *)",
      "Bash(python *)", "Bash(pip *)",
      "Bash(cargo *)", "Bash(go *)"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(sudo *)",
      "Bash(chmod 777 *)"
    ]
  }
}
```


无人值守模式（搭配 OpenClaw 使用）：


```json
{
  "permissions": {
    "allow": [
      "Read", "Edit", "Write", "Glob", "Grep",
      "Bash(*)"
    ],
    "deny": [
      "Bash(rm -rf /)",
      "Bash(sudo rm *)",
      "Bash(:(){ :|:& };:)"
    ]
  }
}
```


💡 小技巧：你也可以直接跟 Claude Code 说"帮我配置权限白名单，允许所有 git、npm、文件读写操作，但禁止 rm -rf 和 sudo"，它会帮你生成 settings.json。

#### 让 Claude Code 帮你配置白名单（推荐）

很多同学看到上面的 JSON 配置可能会头疼——其实你根本不需要手写。配置好 Claude Code 之后，很多事情都可以直接让它帮你完成，白名单配置就是一个典型例子。直接用自然语言告诉 Claude Code 你想要什么，它会帮你生成并写入配置文件：示例对话：


```
👤 你：帮我配置权限白名单，我是前端开发，常用 git、npm、pnpm、node，
       需要读写文件权限，但禁止删除根目录和 sudo

🤖 Claude Code：好的，我来帮你配置 .claude/settings.json...
   （自动创建文件并写入合适的 allow/deny 规则）
```


```
👤 你：我要跑 Python 项目，帮我把 python、pip、pytest 的命令都加到白名单里

🤖 Claude Code：已更新 settings.json，新增了 Python 相关命令的白名单...
```


```
👤 你：把 docker 和 docker-compose 命令也加到白名单

🤖 Claude Code：已添加 Bash(docker *) 和 Bash(docker-compose *) 到 allow 列表...
```


核心理念：Claude Code 不仅是写代码的工具，它也是配置自身的最佳助手。当你学会配置好 Claude Code 后，后续的环境搭建、插件安装、权限调整、CLAUDE.md 编写……这些统统可以用自然语言让它帮你完成。不要手动去改配置文件，告诉 Claude Code 你要什么，让它来做。这种"用 AI 配置 AI"的思路贯穿整个 Claude Code 的使用过程：


| 你想做的事 | 直接告诉 Claude Code |
| --- | --- |
| 配置权限白名单 | "帮我配置白名单，允许 git 和 npm 命令" |
| 创建 CLAUDE.md | "帮我生成项目的 CLAUDE.md 规范文件" |
| 安装 MCP 服务器 | "帮我安装 Playwright MCP" |
| 安装插件/Skills | "帮我安装 superpowers 插件" |
| 配置 Hooks | "帮我配置一个 pre-commit hook 自动跑 lint" |
| 初始化项目结构 | "帮我创建一个 React + TypeScript 项目" |
| 配置 Git | "帮我初始化 git 仓库并做第一次提交" |
| 🎯 记住这个原则：当你不知道怎么配置时，先问 Claude Code。 它既是工具，也是你的配置向导。 |  |


## 第三章：CLAUDE.md — 你的开发规范圣经

CLAUDE.md 是 Claude Code 最核心的配置文件，它决定了 AI 的行为边界和开发质量。规范先行是多 Agent 开发的第一原则。

### 3.1 CLAUDE.md 的层级结构


```
  ~/.claude/CLAUDE.md           ← 全局规范（所有项目生效）
       │
       ▼ (被覆盖)
  项目根目录/CLAUDE.md          ← 项目级规范（当前项目生效）
       │
       ▼ (被覆盖)
  子目录/CLAUDE.md              ← 模块级规范（该目录下生效）
```


📌 覆盖规则：离你越近的 CLAUDE.md 优先级越高。子目录的规范会覆盖上层规范。

### 3.2 全局 CLAUDE.md 配置

位置：`~/.claude/CLAUDE.md`适合放置跨项目通用的规范：


```markdown
# 全局开发规范
## Agent Team 管理
NEVER auto-shutdown teammates after task completion.
Keep them idle and reusable indefinitely within the session.
只有用户明确要求关闭时才发送 shutdown_request。

## 通用编码规范
- 优先使用 TypeScript
- 使用 ESLint + Prettier 格式化代码
- 所有公开 API 必须有类型注解

## 沟通语言
Always respond in 中文。技术术语保留英文原文。
```


### 3.3 项目级 CLAUDE.md 完整模板

以下是根据实战经验总结的完整模板（你需要根据自己的项目调整）：


```markdown
# 项目名称 - 开发规范
## 一、项目概述
描述项目的核心功能和目标。
- 本项目是一个 [简要描述]
- 核心用户是 [目标用户]
- 主要解决的问题是 [问题描述]

## 二、技术栈约束
### 必须使用的技术
| 模块 | 技术栈 |
|------|--------|
| 前端 | React 18 + TypeScript + Vite |
| 后端 | Node.js + Express + PostgreSQL |
| 测试 | Jest + Playwright |

### 禁止使用的技术
- ❌ 不要使用 jQuery
- ❌ 不要使用 var 声明变量
- ❌ 不要使用 any 类型（除非确有必要并注释原因）
- ❌ 不要引入未经确认的第三方库

## 三、整体架构图
┌──────────────────────────────────────┐
│              前端应用                  │
│  ┌──────┐  ┌──────┐  ┌──────┐       │
│  │ 页面  │  │ 组件  │  │ 状态  │       │
│  └──┬───┘  └──┬───┘  └──┬───┘       │
│     └─────────┼─────────┘            │
│               │ HTTP/WebSocket        │
├───────────────┼──────────────────────┤
│              API 层                   │
│  ┌──────┐  ┌──────┐  ┌──────┐       │
│  │ 路由  │  │ 中间件│  │ 控制器│       │
│  └──┬───┘  └──┬───┘  └──┬───┘       │
│     └─────────┼─────────┘            │
│               │                      │
├───────────────┼──────────────────────┤
│             数据层                    │
│  ┌──────┐  ┌──────┐                  │
│  │ 模型  │  │ 数据库│                  │
│  └──────┘  └──────┘                  │
└──────────────────────────────────────┘

## 四、架构红线（不可违反）
1. 前后端必须通过 API 通信，禁止直接数据库操作
2. 所有 API 必须经过认证中间件
3. 敏感数据必须加密存储
4. 组件间通信必须通过状态管理，禁止直接 DOM 操作

## 五、通信协议
- RESTful API 规范
- 请求体使用 camelCase
- URL 路径使用 kebab-case
- 响应格式统一为：`{ code, message, data }`

## 六、目录组织规范

project/
├── CLAUDE.md              # 项目规范（你正在看的这个）
├── src/
│   ├── frontend/          # 前端代码
│   │   ├── components/    # 通用组件
│   │   ├── pages/         # 页面
│   │   ├── hooks/         # 自定义 hooks
│   │   └── utils/         # 工具函数
│   ├── backend/           # 后端代码
│   │   ├── routes/        # 路由定义
│   │   ├── controllers/   # 控制器
│   │   ├── models/        # 数据模型
│   │   └── middleware/     # 中间件
│   └── shared/            # 前后端共享代码
├── tests/                 # 测试文件
├── docs/                  # 文档
│   ├── api.md             # API 文档
│   └── dsl-spec.md        # DSL 规范
└── scripts/               # 脚本工具

## 七、编码规范
- 函数长度不超过 50 行
- 文件长度不超过 300 行，超过需拆分
- 每个模块必须有 index.ts 导出
- 命名规范：组件 PascalCase，函数 camelCase，常量 UPPER_SNAKE_CASE

## 八、Git 提交规范
- feat: 新功能
- fix: 修复 bug
- refactor: 重构
- test: 测试相关
- docs: 文档更新
- 每次提交必须附带有意义的描述

## 九、Agent 协作规范
- 主 Agent 不干重活，只负责统筹和分发任务
- 架构师 Agent 负责审查 git 提交记录，确保符合规范
- DSL 相关修改必须全局广播给所有相关 Agent
- 发现 bug 时先通知相关 Agent，确认后再修复

## 十、测试规范
- 所有新功能必须附带单元测试
- 接口测试覆盖率 > 80%
- 测试必须有明确的输入输出和反馈
- 测试命令：`npm test`（运行后查看输出即可知道对错）

## 十一、上下文管理要求
- compact 后必须重新读取本文件（CLAUDE.md 会被自动注入系统提示，但 compact 后细节可能丢失，需强制重读）
- 分阶段干活，每个阶段有明确的输入、目标和验收标准
- 当上下文超过 150K tokens 时主动执行 `/compact`
- 主 Agent 绝不自己读代码/写代码，只统筹分发，避免上下文膨胀
- 使用 subagent 做代码探索和调研，结果以摘要形式回传，不污染主上下文
- 约束文件读取范围：在提示词中明确"只读 src/xxx/ 目录"，禁止无目的全局搜索
- 不相关任务之间执行 `/clear` 清空上下文
- 在 CLAUDE.md 中加入 compact 保留指令：`"compact 时务必保留：已修改文件列表、测试命令、当前阶段进度"`
- 配合 `.claudeignore` 排除 node_modules/、dist/、vendor/ 等目录，减少 40-60% 搜索噪音
```


### 3.4 编写 CLAUDE.md 的核心原则


```
┌─────────────────────────────────────────────────┐
│           CLAUDE.md 编写黄金法则                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  ✅ DO                    ❌ DON'T               │
│  ─────────────            ─────────────          │
│  精确具体的约束            模糊的描述              │
│  "用 React 18"            "用现代框架"            │
│                                                 │
│  必要的信息               冗长的废话              │
│  模型注意力有限！          注意力会被分散！         │
│                                                 │
│  可验证的规则              无法验证的建议           │
│  "函数不超过50行"          "代码要简洁"            │
│                                                 │
│  架构红线和边界            面面俱到的指南           │
│  "禁止直接DB操作"          大量教程性内容           │
│                                                 │
│  经过多轮迭代优化          一次性写完不再更新        │
│  几小时反复打磨            只花10分钟               │
│                                                 │
└─────────────────────────────────────────────────┘
```


⚠️ 实战经验：CLAUDE.md 的质量直接决定了 AI 开发的效果。构思一个好的 CLAUDE.md 可能需要小半天时间，但这是值得的投资。它就像给员工的 Onboarding 文档——写得越清楚，员工干活越靠谱。


## 第四章：Skills 技能系统

Skills 是 Claude Code 的工作流定义，用自然语言描述一系列操作步骤。可以理解为"给 AI 的标准操作流程（SOP）"。

### 4.1 Skills 是什么？


```
┌─────────────────────────────────────────────────────┐
│                    Skills 概念图                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Skill = 一个可复用的工作流定义                        │
│                                                     │
│  举例：                                              │
│  ┌───────────────┐  ┌───────────────┐               │
│  │  fix-issue     │  │  brainstorming│               │
│  │  修复GitHub    │  │  头脑风暴      │               │
│  │  Issue的流程   │  │  需求分析流程  │               │
│  └───────────────┘  └───────────────┘               │
│  ┌───────────────┐  ┌───────────────┐               │
│  │  code-review   │  │  deploy       │               │
│  │  代码审查流程   │  │  部署发布流程  │               │
│  └───────────────┘  └───────────────┘               │
│                                                     │
│  类比：就像公司的 SOP 文档                             │
│  - 保洁的"扫地"是一个 skill                           │
│  - 保洁的"擦桌子"是另一个 skill                       │
│  - "保洁"这个角色 = Plugin（多个 skill 的集合）        │
│                                                     │
└─────────────────────────────────────────────────────┘
```


### 4.2 Skill 的存放位置与来源

Skill 可以从三种途径获得：


| 来源 | 路径 | 适用范围 |
| --- | --- | --- |
| 个人自定义 | ~/.claude/skills/<skill-name>/SKILL.md | 你的所有项目 |
| 项目级自定义 | 项目/.claude/skills/<skill-name>/SKILL.md | 仅当前项目 |
| 通过插件安装 | 安装插件后自动获得，以 plugin-name:skill-name 命名 | 启用该插件的项目 |
| 查看当前可用的 Skills： |  |  |


```
/help                    # 查看所有可用命令和 Skills 列表
What skills are available?   # 直接问 Claude
```


在交互模式中输入 `/` 会弹出所有可用的 skill 列表，选择即可调用。

### 4.3 创建你的第一个 Skill

目录结构：


```
.claude/
└── skills/
    └── my-first-skill/
        └── SKILL.md
```


SKILL.md 文件格式：


```markdown
---
name: api-conventions
description: REST API design conventions for our services
---
# API 设计规范
- URL 路径使用 kebab-case
- JSON 属性使用 camelCase
- 列表接口必须支持分页
- API 版本号放在 URL 路径中 (/v1/, /v2/)
```


带工作流步骤的 Skill：


```markdown
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
分析并修复 GitHub Issue: $ARGUMENTS

1. 使用 `gh issue view` 获取 issue 详情
2. 理解问题描述
3. 在代码库中搜索相关文件
4. 实现修复代码
5. 编写并运行测试验证修复
6. 确保代码通过 lint 和类型检查
7. 创建描述性的 commit message
8. 推送并创建 PR
```


### 4.4 Skill 的两种调用方式

自动调用：Claude 识别到上下文匹配 skill 描述时自动使用。手动调用：使用斜杠命令：


```
/fix-issue 1234          # 调用 fix-issue skill，传入参数 1234
/api-conventions          # 查看 API 规范
```


### 4.5 Skill 的高级配置


| 字段 | 说明 | 示例 |
| --- | --- | --- |
| name | Skill 名称 | fix-issue |
| description | Skill 描述，用于自动匹配 | Fix a GitHub issue |
| disable-model-invocation | 设为 true 则只能手动 / 触发 | 有副作用的工作流应设为 true |
| user-invocable | 设为 true 表示用户可通过 / 命令调用 | 默认 true |
| context | 设为 fork 可在子agent中独立运行 | 避免污染主上下文 |
| $ARGUMENTS | 调用时传入的参数占位符 | /fix-issue 1234 中的 1234 |
| 动态上下文注入：Skill 中可以使用反引号执行命令，将结果注入上下文： |  |  |


```markdown
---
name: check-status
description: 检查项目当前状态
---
# 项目状态
当前 Git 状态：
!`git status --short`

最近的提交：
!`git log --oneline -5`

根据以上信息为用户总结项目状态。
```


### 4.6 实用 Skill 示例

头脑风暴 Skill：


```markdown
---
name: brainstorming
description: 在开始新功能开发前进行头脑风暴
---
# 头脑风暴工作流
1. 使用 AskUserQuestion 询问用户要开发什么功能
2. 探索当前代码库上下文
3. 提出 3-5 个关键设计问题
4. 展示 2-3 个可选方案及其优劣对比
5. 等待用户确认方案后，生成完整的需求规格
6. 将规格写入 SPEC.md
```


代码审查 Skill：


```markdown
---
name: code-review
description: 审查最近的代码变更
disable-model-invocation: true
---
审查代码变更：

1. 运行 `git diff` 查看所有变更
2. 检查代码是否符合 CLAUDE.md 中的编码规范
3. 检查是否有安全漏洞（SQL注入、XSS等）
4. 检查是否有性能问题
5. 检查测试覆盖率
6. 以列表形式输出发现的问题和建议
```


### 4.7 用 skill-creator 快速创建 Skill

Claude Code 内置了一个**元技能（Meta-Skill）**叫 `skill-creator`，专门用来帮你创建新的 skill。你不需要手写 SKILL.md，只需用自然语言描述工作流，它会引导你完成整个过程。使用方式：


```
/skill-creator 帮我创建一个"每日站会总结"的 skill
```


skill-creator 的工作流程：


```
┌──────────────────────────────────────────────────┐
│          skill-creator 工作流程                    │
├──────────────────────────────────────────────────┤
│                                                  │
│  1. 交互式问答                                    │
│     skill-creator 会问你：                        │
│     - 这个 skill 要解决什么问题？                   │
│     - 输入是什么？输出是什么？                      │
│     - 有哪些步骤？                                │
│     - 什么时候应该自动触发？                        │
│              │                                   │
│              ▼                                   │
│  2. 自动生成                                      │
│     - 创建文件夹结构                               │
│     - 生成 SKILL.md（含 frontmatter + 步骤）       │
│     - 整理所需的参考文件和脚本                      │
│              │                                   │
│              ▼                                   │
│  3. 评估与迭代                                    │
│     - 定义测试提示和预期结果                        │
│     - 运行评估验证 skill 是否正常                   │
│     - 优化 description 减少误触发                   │
│                                                  │
└──────────────────────────────────────────────────┘
```


skill-creator 的高级功能：


| 功能 | 说明 |
| --- | --- |
| 评估框架 | 定义测试提示 + 预期结果，自动验证 skill 是否达标 |
| 基准模式 | 追踪 eval 通过率、耗时、token 使用量 |
| A/B 对比 | 用对比代理盲评输出，判断改动是否真的改进了 |
| 描述优化 | 分析 description 与示例提示的匹配度，建议优化 |


💡 核心理念：你不需要记住 SKILL.md 的语法格式，只需要清晰描述你的工作流程，skill-creator 会帮你把它变成一个可复用的 skill。


## 第五章：Plugins 插件系统

### 5.1 Plugin vs Skill 的关系


```
┌──────────────────────────────────────────────────┐
│            Plugin 和 Skill 的关系                  │
├──────────────────────────────────────────────────┤
│                                                  │
│  Plugin（插件）= 多个 Skill 的集合 + 配置          │
│                                                  │
│  ┌─────────────────────────────────┐             │
│  │       superpowers (插件)         │             │
│  │  ┌───────────┐ ┌───────────┐   │             │
│  │  │brainstorm │ │write-plan │   │             │
│  │  │头脑风暴    │ │写计划      │   │             │
│  │  └───────────┘ └───────────┘   │             │
│  │  ┌───────────┐ ┌───────────┐   │             │
│  │  │code-review│ │   TDD     │   │             │
│  │  │代码审查    │ │测试驱动    │   │             │
│  │  └───────────┘ └───────────┘   │             │
│  │  ┌───────────┐ ┌───────────┐   │             │
│  │  │ debugging │ │verify     │   │             │
│  │  │ 系统调试  │  │完成验证   │   │             │
│  │  └───────────┘ └───────────┘   │             │
│  └─────────────────────────────────┘             │
│                                                  │
│  类比：                                           │
│  - Plugin = 角色（如"保洁"）                       │
│  - Skill  = 技能（如"扫地"、"擦桌子"、"拖地"）      │
│                                                  │
└──────────────────────────────────────────────────┘
```


### 5.2 插件市场：浏览、安装、管理

📖 官方文档：Discover and install plugins

#### 打开插件管理器

在 Claude Code 交互模式中输入：


```
/plugin
```


会打开一个带四个标签页的管理界面（用 Tab 键切换）：


| 标签页 | 功能 |
| --- | --- |
| Discover | 浏览所有可用插件，支持搜索筛选 |
| Installed | 查看和管理已安装的插件 |
| Marketplaces | 添加、删除、更新市场源 |
| Errors | 查看插件加载错误 |


Anthropic 官方市场（`claude-plugins-official`）是内置的，无需手动添加，直接在 Discover 标签页浏览即可。

#### 安装插件

方式一：交互式安装（推荐新手）


```
/plugin
```


→ 进入 Discover 标签 → 选中插件按 Enter → 选择安装范围（User/Project/Local）方式二：命令行直接安装


```
/plugin install plugin-name@marketplace-name
```


例如：


```
/plugin install commit-commands@claude-plugins-official
```


安装范围说明：


| 范围 | 说明 | 适用场景 |
| --- | --- | --- |
| User | 安装到个人级别，所有项目可用 | 个人常用工具 |
| Project | 写入 .claude/settings.json，团队共享 | 团队统一工具 |
| Local | 仅当前仓库、仅自己可用 | 试用或个人偏好 |
| 用 CLI 指定范围： |  |  |


```
claude plugin install formatter@your-org --scope project
```


#### 添加第三方市场

除了官方市场，你还可以添加第三方或团队私有市场：


```bash
# 从 GitHub 添加（最常用）
/plugin marketplace add owner/repo

# 从 GitLab 等平台添加
/plugin marketplace add https://gitlab.com/company/plugins.git

# 从本地路径添加（开发自己的插件时用）
/plugin marketplace add ./my-marketplace
```


简写：`/plugin market` 等同于 `/plugin marketplace`

#### 管理已安装的插件


```bash
/plugin                                          # 打开管理界面，切到 Installed 标签
/plugin disable plugin-name@marketplace-name     # 暂时禁用（不卸载）
/plugin enable plugin-name@marketplace-name      # 重新启用
/plugin uninstall plugin-name@marketplace-name   # 卸载
/plugin marketplace list                         # 查看所有已配置的市场源
/plugin marketplace update marketplace-name      # 更新某个市场的插件列表
```


#### 官方市场中的热门插件


| 分类 | 插件示例 | 说明 |
| --- | --- | --- |
| 代码智能（LSP） | typescript-lsp、pyright-lsp、rust-analyzer-lsp、gopls-lsp | 给 Claude 精确的代码导航能力 |
| 外部集成 | github、gitlab、slack、figma、notion、sentry | 连接第三方服务 |
| 开发工作流 | commit-commands、pr-review-toolkit | Git 提交和 PR 审查增强 |
| 插件开发 | plugin-dev | 开发自己的插件时用 |


### 5.3 Superpowers 插件详解

Superpowers 是最流行的开发流程插件之一，它提供了一套完整的软件开发工作流：


```
┌─────────────────────────────────────────────────────┐
│              Superpowers 工作流                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  用户输入需求                                         │
│       │                                             │
│       ▼                                             │
│  ┌──────────────┐                                   │
│  │ Brainstorming │  ← 头脑风暴：探索需求、提问、确认    │
│  └──────┬───────┘                                   │
│         │                                           │
│         ▼                                           │
│  ┌──────────────┐                                   │
│  │ Writing Plans │  ← 写计划：输出详细实施方案          │
│  └──────┬───────┘                                   │
│         │                                           │
│         ▼                                           │
│  ┌──────────────┐                                   │
│  │ Task Setting  │  ← 任务设定：拆分为可执行的子任务     │
│  └──────┬───────┘                                   │
│         │                                           │
│         ▼ (清空上下文，隔离)                           │
│  ┌──────────────┐                                   │
│  │ Executing     │  ← 执行计划：按步骤编码实现          │
│  └──────┬───────┘                                   │
│         │                                           │
│         ▼                                           │
│  ┌──────────────┐                                   │
│  │ Code Review   │  ← 代码审查：检查质量和规范          │
│  └──────┬───────┘                                   │
│         │                                           │
│         ▼                                           │
│  ┌──────────────┐                                   │
│  │ Verification  │  ← 验证：运行测试确认功能正确        │
│  └──────────────┘                                   │
│                                                     │
│  核心价值：隔离上下文，分阶段工作，避免上下文爆炸         │
│                                                     │
└─────────────────────────────────────────────────────┘
```


使用方式：


```
使用 superpowers 帮我开发一个笔记应用
```


Claude 会自动触发 superpowers 的头脑风暴流程，然后逐步推进。安装方式：


```
/plugin marketplace add obra/superpowers-marketplace
```


然后在 Discover 标签页中找到 superpowers 并安装。

📖 Superpowers GitHub（42k+ stars）：https://github.com/obra/superpowers

### 5.4 插件管理命令速查


| 操作 | 命令 |
| --- | --- |
| 打开插件管理器 | /plugin |
| 安装插件 | /plugin install 插件名@市场名 |
| 卸载插件 | /plugin uninstall 插件名@市场名 |
| 暂时禁用 | /plugin disable 插件名@市场名 |
| 重新启用 | /plugin enable 插件名@市场名 |
| 添加市场源 | /plugin marketplace add owner/repo |
| 查看市场列表 | /plugin marketplace list |
| 更新市场 | /plugin marketplace update 市场名 |
| 删除市场 | /plugin marketplace remove 市场名 |
| 验证插件 | /plugin validate . |


### 5.5 创建自定义插件

你完全可以让 Claude Code 帮你写插件：


```
帮我创建一个 Claude Code 插件，功能包括：
1. 管理我的 Agent 团队成员
2. 自动分配任务
3. 监控团队进度
```


### 5.6 动手练习

以下练习由浅入深，建议逐个完成。每个练习都可以直接在 Claude Code 中用自然语言完成。

#### 练习 1：安装你的第一个插件

在 Claude Code 中执行 `/plugin`，浏览插件市场，选一个感兴趣的插件安装并体验。


```
/plugin
```


安装后试着用自然语言触发它，观察它做了什么、调用了哪些 skill。

#### 练习 2：用 Superpowers 完成一个小项目

选择一个简单的目标（比如"一个 Todo List 网页应用"），体验完整的 superpowers 工作流：


```
使用 superpowers 帮我开发一个 Todo List 网页应用
```


重点观察：

头脑风暴阶段它问了你哪些问题？

它是如何拆分任务的？

上下文是怎么在阶段之间隔离的？

#### 练习 3：写你的第一个 Skill

创建一个"每日代码检查"skill，每次调用时自动：

查看 git 状态

列出最近的修改

跑一遍 lint

输出今日工作摘要提示：在 `.claude/skills/daily-check/SKILL.md` 中编写，然后用 `/daily-check` 调用。


```markdown
<!-- .claude/skills/daily-check/SKILL.md -->
---
name: daily-check
description: 每日代码健康检查
disable-model-invocation: true
---
执行每日代码健康检查：

1. 运行 `git status` 查看工作区状态
2. 运行 `git log --oneline -10` 查看最近提交
3. 运行项目的 lint 命令检查代码规范
4. 用一段简短的中文总结今日代码状态，包括：
   - 有多少未提交的变更
   - 最近做了哪些工作
   - 有没有 lint 警告需要处理
```


#### 练习 4：创建一个自定义插件

挑战自己——让 Claude Code 帮你从零写一个插件：


```
帮我创建一个 Claude Code 插件叫 "quick-notes"，包含以下 skills：
1. /note-add：快速记录一条开发笔记到 .claude/notes.md
2. /note-list：列出所有笔记
3. /note-search <关键词>：搜索笔记内容
```


完成后检查 `.claude/skills/` 下生成的文件结构，理解插件是怎么组织的。

学习要点：通过这些练习你会发现——你不需要手写每一行配置，只需要用自然语言描述你想要的工作流，Claude Code 自己就能帮你生成 skill 文件。核心能力是清晰地定义需求，而不是记住语法。


## 第六章：MCP Servers — 连接外部世界

MCP (Model Context Protocol) 是让 Claude Code 连接外部工具和服务的协议。

### 6.1 MCP 的作用


```
┌───────────────────────────────────────────────────┐
│                 MCP 连接示意图                      │
├───────────────────────────────────────────────────┤
│                                                   │
│                 Claude Code                       │
│                     │                             │
│           ┌─────────┼─────────┐                   │
│           │         │         │                   │
│           ▼         ▼         ▼                   │
│     ┌─────────┐ ┌────────┐ ┌──────────┐          │
│     │Playwright│ │MasterGo│ │ GitHub   │          │
│     │浏览器测试│ │UI设计稿 │ │代码仓库  │          │
│     └─────────┘ └────────┘ └──────────┘          │
│           │         │         │                   │
│           ▼         ▼         ▼                   │
│     ┌─────────┐ ┌────────┐ ┌──────────┐          │
│     │ Docker  │ │数据库   │ │ Slack    │          │
│     │容器管理  │ │查询工具 │ │消息通知  │          │
│     └─────────┘ └────────┘ └──────────┘          │
│                                                   │
│  本质：让 Claude Code 能使用你定义的外部工具         │
│                                                   │
└───────────────────────────────────────────────────┘
```


### 6.2 配置 MCP Server

在项目根目录创建 `.claude/settings.json`：


```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-server-playwright"],
      "description": "浏览器自动化测试"
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "@anthropic-ai/mcp-server-filesystem",
        "--root", "/path/to/allowed/directory"
      ],
      "description": "文件系统访问"
    },
    "github": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token-here"
      },
      "description": "GitHub 操作"
    }
  }
}
```


### 6.3 实战场景：Playwright MCP 做自动化测试


```
# 安装 Playwright MCP
npm install @anthropic-ai/mcp-server-playwright

# 在 Claude Code 中使用
帮我用 Playwright 打开浏览器，访问我们的应用，
模拟用户在画布上写字，然后截图对比写字前后的效果
```


实战案例：开发者用 Playwright MCP 让模型自动唤起浏览器、模拟笔记书写操作，然后截图对比写字过程中和结束后的像素差异，发现了"笔迹回缩"的 bug 并自动修复。

### 6.4 实战场景：SSH 远程开发


```
# 让 Claude Code 连接远程 Linux 服务器
我有一台远程 Linux 服务器，地址是 192.168.1.248
用户名 dev，你可以 SSH 连上去帮我编译和测试代码
我本地是 macOS，但代码需要在 Linux 上运行
```


这就是模型"探索外部世界"能力的体现——它不仅能访问本地文件，还能组网访问其他机器。


## 第七章：Hooks 事件钩子

Hooks 让你在 Claude Code 的特定事件发生时自动执行操作。

### 7.1 Hook 的作用


```
┌──────────────────────────────────────────────┐
│               Hooks 工作原理                   │
├──────────────────────────────────────────────┤
│                                              │
│  Claude Code 事件   →   触发 Hook   →   执行   │
│                                              │
│  例如：                                       │
│  - 会话开始时      →   读取配置文件              │
│  - 工具调用前      →   检查权限                  │
│  - 工具调用后      →   记录日志                  │
│  - 提交代码前      →   运行 lint 检查            │
│  - 发送通知        →   同步到 Slack              │
│                                              │
└──────────────────────────────────────────────┘
```


### 7.2 Hook 的四种类型


| 类型 | 说明 | 适用场景 |
| --- | --- | --- |
| command | 执行 shell 命令 | 运行 lint、格式化、通知 |
| http | 发送 HTTP 请求 | 通知外部服务、记录日志 |
| prompt | 注入提示词到上下文 | 动态添加规范、提醒 |
| agent | 触发子agent | 自动代码审查 |


### 7.3 配置 Hooks

在 `.claude/settings.json` 中配置（支持三个层级：用户全局、项目共享、项目本地）：


```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "cat .claude/welcome.md",
        "description": "显示欢迎信息和项目概览"
      }
    ],
    "PreToolUse": [
      {
        "tool": "Bash",
        "type": "command",
        "command": "echo '准备执行命令...'",
        "description": "命令执行前的提示"
      }
    ],
    "PostToolUse": [
      {
        "tool": "Edit",
        "type": "command",
        "command": "npx eslint --fix $FILE",
        "description": "编辑文件后自动 lint"
      }
    ],
    "PreCompact": [
      {
        "type": "prompt",
        "prompt": "压缩时请务必保留：1.所有修改过的文件列表 2.测试命令 3.当前进度",
        "description": "压缩前注入保留指令（减少信息丢失30%）"
      }
    ]
  }
}
```


💡 PreToolUse hook 的特殊能力：可以返回 `allow`（允许）、`deny`（拒绝）、`ask`（询问用户）来控制工具执行，非常适合做安全防护。

### 7.4 常见 Hook 场景


| Hook 事件 | 用途 | 示例 |
| --- | --- | --- |
| SessionStart | 会话开始时注入上下文 | 读取项目配置、显示最近变更 |
| PreToolUse | 工具调用前检查/拦截 | 权限检查、危险操作拦截 |
| PostToolUse | 工具调用后处理 | 自动格式化、运行测试 |
| PreCompact | 压缩上下文前 | 指定必须保留的信息 |
| Stop | Agent 停止时 | 保存进度、发送通知 |
| Notification | 通知事件 | 推送到 Slack/微信 |


### 7.5 Hook 执行生命周期与数据流

理解 Hook 的完整执行流程，是掌握"怎么生效"的关键：


```
┌─────────────────────────────────────────────────────────────┐
│               Hook 执行生命周期                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ① 事件触发（如 SessionStart / PreToolUse）                   │
│       │                                                     │
│       ▼                                                     │
│  ② 查找匹配的 Hook 配置                                      │
│     - 按配置层级合并（managed > local > project > user）       │
│     - 检查 matcher 是否匹配（正则匹配工具名等）                 │
│       │                                                     │
│       ▼                                                     │
│  ③ 构建 stdin JSON 输入                                      │
│     {                                                       │
│       "session_id": "abc-123",                              │
│       "cwd": "/path/to/project",                            │
│       "hook_event_name": "PreToolUse",                      │
│       "tool_name": "Bash",           ← 仅工具相关事件         │
│       "tool_input": { "command": "..." }                    │
│     }                                                       │
│       │                                                     │
│       ▼                                                     │
│  ④ 执行 Hook（command / http / prompt / agent）              │
│       │                                                     │
│       ▼                                                     │
│  ⑤ 处理输出                                                  │
│     - command 类型：stdout 作为反馈/上下文                     │
│     - command 类型：exit code 控制流程（0=继续, 2=阻止）       │
│     - prompt 类型：注入文本到 Claude 对话上下文                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```


关键点：Hook 的 stdin 会自动注入事件的上下文信息（JSON 格式），你的脚本可以读取并据此做出决策。

### 7.6 上下文注入机制详解

这是 Hooks 最强大的能力之一——在对话中动态注入信息，让 Claude 自动获取额外上下文。

#### 方式一：prompt 类型 Hook（直接注入）

`prompt` 类型 Hook 会将指定文本直接注入到 Claude 的对话上下文中：


```json
{
  "hooks": {
    "PreCompact": [
      {
        "type": "prompt",
        "prompt": "压缩时请保留所有修改过的文件路径和测试命令",
        "description": "压缩前注入保留指令"
      }
    ],
    "SessionStart": [
      {
        "type": "prompt",
        "prompt": "当前项目使用 TypeScript + React，测试框架为 Vitest",
        "description": "会话开始注入技术栈信息"
      }
    ]
  }
}
```


`prompt` 字段支持 `$ARGUMENTS` 占位符，会被替换为事件的实际参数。

#### 方式二：command 类型 Hook 的 stdout 注入

对于 `SessionStart` 和 `UserPromptSubmit` 事件，command 类型 Hook 的标准输出（stdout）会被直接添加到 Claude 的上下文中：


```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "echo '## 项目状态' && git log --oneline -5 && echo '## 待修复问题' && cat .claude/todo.md",
        "description": "注入项目状态和待办事项"
      }
    ],
    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "echo '当前分支: '$(git branch --show-current) && echo '未提交变更: '$(git status --short | wc -l)' 个文件'",
        "description": "每次对话时注入 git 状态"
      }
    ]
  }
}
```


```
┌──────────────────────────────────────────────────────────┐
│            上下文注入方式对比                               │
├──────────────┬───────────────────────────────────────────┤
│              │  prompt 类型          command 类型          │
├──────────────┼───────────────────────────────────────────┤
│ 注入内容      │  固定文本              脚本 stdout 输出     │
│ 是否动态      │  静态（或用 $ARGUMENTS）完全动态             │
│ 适用场景      │  固定规范、提醒          实时状态、环境信息   │
│ 注入时机      │  事件触发时             事件触发时           │
│ 执行开销      │  无                    有（执行脚本）        │
└──────────────┴───────────────────────────────────────────┘
```


💡 实用技巧：`SessionStart` 的 stdout 注入非常适合做"项目上下文预加载"——Claude 一启动就知道项目状态、最近改动、待办事项等。

### 7.7 PreToolUse 权限控制详解

`PreToolUse` 是最强大的 Hook 事件，可以在工具执行前拦截、允许或询问用户：

#### 控制方式：Exit Code + JSON 输出


```
┌──────────────────────────────────────────────────────────┐
│         PreToolUse 控制流程                                │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  工具调用请求 (如: Bash "rm -rf /")                        │
│       │                                                  │
│       ▼                                                  │
│  PreToolUse Hook 执行                                     │
│       │                                                  │
│       ├── exit 0 → ✅ 允许执行（默认）                     │
│       │                                                  │
│       ├── exit 2 → 🚫 阻止执行（静默拦截）                 │
│       │                                                  │
│       └── stdout JSON → 精细控制                          │
│           {                                              │
│             "hookSpecificOutput": {                      │
│               "permissionDecision": "allow" | "deny" | "ask"
│             }                                            │
│           }                                              │
│           - "allow": 允许执行，跳过用户确认                 │
│           - "deny":  阻止执行，告知 Claude                 │
│           - "ask":   弹出确认框，让用户决定                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```


#### 实战示例：危险命令拦截器


```bash
#!/bin/bash
# .claude/hooks/safety-guard.sh
# 读取 stdin 中的工具调用信息
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
# 拦截危险命令
if [[ "$TOOL_NAME" == "Bash" ]]; then
  if echo "$COMMAND" | grep -qE 'rm\s+-rf|drop\s+table|--force|reset\s+--hard'; then
    echo '{"hookSpecificOutput":{"permissionDecision":"deny"}}'
    exit 0
  fi
fi
# 其他情况允许
exit 0
```


```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": { "tool": "Bash" },
        "type": "command",
        "command": "bash .claude/hooks/safety-guard.sh",
        "description": "拦截危险 shell 命令"
      }
    ]
  }
}
```


### 7.8 Matcher 匹配器

Matcher 用于精确控制 Hook 在哪些条件下触发，避免不必要的执行：


```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": {
          "tool": "Bash"
        },
        "type": "command",
        "command": "bash .claude/hooks/check-bash.sh",
        "description": "仅匹配 Bash 工具调用"
      }
    ],
    "PostToolUse": [
      {
        "matcher": {
          "tool": "Edit|Write"
        },
        "type": "command",
        "command": "npx prettier --write $FILE",
        "description": "匹配 Edit 或 Write 工具（正则语法）"
      }
    ]
  }
}
```


| 匹配字段 | 说明 | 示例 |
| --- | --- | --- |
| tool | 匹配工具名（支持正则） | "Bash", "Edit|Write", ".*" |


没有设置 matcher 的 Hook 会在每次对应事件触发时执行。建议总是设置 matcher 以避免性能损耗。

### 7.9 Hook 可用的环境变量

Hook 脚本可以通过 stdin JSON 获取丰富的上下文信息：


| 字段 | 说明 | 示例值 |
| --- | --- | --- |
| session_id | 当前会话 ID | "abc-123-def" |
| cwd | Claude Code 工作目录 | "/Users/dev/myproject" |
| hook_event_name | 触发的事件名 | "PreToolUse" |
| tool_name | 工具名（仅工具事件） | "Bash", "Edit" |
| tool_input | 工具输入参数（仅工具事件） | {"command": "npm test"} |
| transcript_path | 对话记录文件路径 | "/path/to/transcript.jsonl" |
| 读取方式示例（Bash）： |  |  |


```bash
#!/bin/bash
INPUT=$(cat)  # 从 stdin 读取 JSON
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
CWD=$(echo "$INPUT" | jq -r '.cwd')
echo "工具: $TOOL, 目录: $CWD"
```


### 7.10 配置层级与优先级

Hook 可以在四个层级配置，高优先级的层级覆盖低优先级：


```
┌─────────────────────────────────────────────────┐
│           配置层级（优先级从高到低）                │
├─────────────────────────────────────────────────┤
│                                                 │
│  ① managed (企业管理)   最高优先级                │
│     ~/.claude/settings.managed.json             │
│     → 企业 IT 统一下发，用户无法覆盖              │
│                                                 │
│  ② local (项目本地)                              │
│     .claude/settings.local.json                 │
│     → 个人本地配置，不提交到 Git                  │
│                                                 │
│  ③ project (项目共享)                            │
│     .claude/settings.json                       │
│     → 团队共享规范，提交到 Git                    │
│                                                 │
│  ④ user (用户全局)      最低优先级                │
│     ~/.claude/settings.json                     │
│     → 个人全局默认配置                            │
│                                                 │
├─────────────────────────────────────────────────┤
│  合并规则：同一事件的 Hook 数组跨层级合并           │
│  （不是覆盖，而是拼接执行）                        │
└─────────────────────────────────────────────────┘
```


⚠️ 注意：不同层级的同一事件 Hook 会合并执行（数组拼接），而不是高优先级覆盖低优先级。优先级主要影响的是权限设置等其他配置项。

### 7.11 完整 Hook 配置示例

一个综合了多种 Hook 能力的实际项目配置：


```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "echo '📋 最近 5 条提交:' && git log --oneline -5 && echo '📌 当前分支:' $(git branch --show-current)",
        "description": "会话启动时注入项目上下文"
      }
    ],
    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "echo '⚡ 未暂存变更:' $(git diff --stat --shortstat 2>/dev/null || echo '无')",
        "description": "每次用户发送消息时注入 git 状态"
      }
    ],
    "PreToolUse": [
      {
        "matcher": { "tool": "Bash" },
        "type": "command",
        "command": "bash .claude/hooks/safety-guard.sh",
        "description": "拦截危险 shell 命令"
      }
    ],
    "PostToolUse": [
      {
        "matcher": { "tool": "Edit|Write" },
        "type": "command",
        "command": "npx prettier --write $FILE 2>/dev/null; exit 0",
        "description": "文件编辑后自动格式化"
      }
    ],
    "PreCompact": [
      {
        "type": "prompt",
        "prompt": "压缩时务必保留：1.所有修改过的文件完整路径 2.测试运行命令 3.当前任务进度 4.已知问题",
        "description": "压缩前注入保留指令"
      }
    ],
    "Notification": [
      {
        "type": "command",
        "command": "osascript -e 'display notification \"Claude Code 有新消息\" with title \"CC 通知\"'",
        "description": "macOS 系统通知"
      }
    ]
  }
}
```


## 第八章：Subagents 子Agent

### 8.1 什么是 Subagent？

Subagent 是在独立上下文中运行的专业 Agent，用于保护主对话的上下文不被污染。


```
┌──────────────────────────────────────────────────┐
│              Subagent 工作模式                     │
├──────────────────────────────────────────────────┤
│                                                  │
│  主对话 (上下文有限且珍贵)                          │
│  ┌────────────────────────────────────┐          │
│  │  用户: "帮我了解认证系统怎么工作的"    │          │
│  │                                    │          │
│  │  Claude: 启动 subagent 去调研...    │          │
│  │            │                       │          │
│  │            ▼                       │          │
│  │  ┌──────────────────────┐         │          │
│  │  │  Subagent (独立上下文) │         │          │
│  │  │  - 读取 auth 相关文件  │         │          │
│  │  │  - 分析 token 刷新逻辑 │         │          │
│  │  │  - 检查 OAuth 工具     │         │          │
│  │  │  - 生成总结报告        │         │          │
│  │  └──────────┬───────────┘         │          │
│  │             │                      │          │
│  │             ▼ (只返回总结)          │          │
│  │  Claude: "认证系统使用 JWT..."      │          │
│  │  (主上下文保持干净！)                │          │
│  └────────────────────────────────────┘          │
│                                                  │
│  好处：                                           │
│  ✅ 调研过程不占用主上下文                           │
│  ✅ 可以读大量文件而不会让主会话变臃肿                │
│  ✅ 天然隔离，任务失败不影响主对话                    │
│                                                  │
└──────────────────────────────────────────────────┘
```


### 8.2 创建自定义 Subagent

在 `.claude/agents/` 目录下创建：


```markdown
<!-- .claude/agents/security-reviewer.md -->
---
name: security-reviewer
description: 审查代码中的安全漏洞
tools: Read, Grep, Glob, Bash
model: opus
---
你是一位资深安全工程师。审查代码时关注：
- 注入漏洞（SQL注入、XSS、命令注入）
- 认证和授权缺陷
- 代码中的密钥或凭证
- 不安全的数据处理

提供具体的行号引用和修复建议。
```


使用方式：


```
使用 security-reviewer 子agent 审查最近的代码变更
```


### 8.3 使用 Subagent 的最佳场景


| 场景 | 说明 |
| --- | --- |
| 代码库调研 | 探索大型代码库时不污染主上下文 |
| 代码审查 | 独立的上下文做更客观的审查 |
| 方案研究 | 同时调研多个方案不互相干扰 |
| 测试验证 | 验证实现是否正确 |


## 第九章：Agent Teams — 多Agent协作开发

这是 Claude Code 最强大也最前沿的功能。根据实战经验，Agent Teams 可以像真实开发团队一样协作。

### 9.1 Agent Teams 架构


```
┌──────────────────────────────────────────────────────────┐
│                  Agent Teams 协作架构                      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│                    ┌───────────────┐                     │
│                    │   主 Agent     │                     │
│                    │   (Team Lead) │                     │
│                    │   只统筹不干活 │ ← 核心原则！         │
│                    └───────┬───────┘                     │
│                            │                             │
│              ┌─────────────┼─────────────┐               │
│              │             │             │               │
│       ┌──────┴──────┐ ┌───┴────┐ ┌──────┴──────┐       │
│       │  产品经理     │ │ 架构师  │ │  测试工程师  │       │
│       │  Agent       │ │ Agent  │ │  Agent      │       │
│       │  - 需求定义   │ │- 审查   │ │ - 写测试    │       │
│       │  - 功能验收   │ │  代码   │ │ - 运行测试   │       │
│       │             │ │- 审查   │ │ - 报告结果   │       │
│       │             │ │  git   │ │             │       │
│       └─────────────┘ └────────┘ └─────────────┘       │
│              │             │             │               │
│       ┌──────┴──────┐ ┌───┴────┐ ┌──────┴──────┐       │
│       │  前端工程师   │ │ 后端   │ │ AI 助手     │       │
│       │  Agent       │ │ Agent  │ │ Agent       │       │
│       │  - 页面开发   │ │- API   │ │ - 提示词    │       │
│       │  - 组件开发   │ │- 数据库 │ │ - 工具链    │       │
│       │  - 样式调整   │ │- 逻辑  │ │ - 编排     │       │
│       └─────────────┘ └────────┘ └─────────────┘       │
│                                                          │
│  所有 Agent 可以互相发消息、纠错、协调                       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```


### 9.2 启用和启动 Agent Teams

⚠️ Agent Teams 目前是实验性功能，需要手动启用：


```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```


或在 `.claude/settings.json` 中设置。

推荐团队大小：3-5 个 teammates，每个分配 5-6 个任务。

显示模式：支持 in-process（默认）和 split-pane（tmux/iTerm2 分屏）两种。


```
启动：claude --teammate-mode tmux
```


方式一：自然语言启动


```
使用 Agent Teams 帮我开发一个笔记应用。
需要以下角色：
1. 产品经理 - 负责需求定义和功能验收
2. 架构师 - 负责审查代码质量和规范
3. 前端工程师 - 负责页面开发
4. 后端工程师 - 负责 API 开发
5. 测试工程师 - 负责编写和运行测试
```


方式二：通过 superpowers 工作流启动


```
使用 superpowers 和 agent teams 帮我开发一个笔记应用
```


### 9.3 Agent 角色设计指南

#### 主 Agent（Team Lead）的关键约束

⚠️ 最重要的原则：主 Agent 绝对不能干重活！


```markdown
# 在 CLAUDE.md 中约束主 Agent
## 主 Agent 行为约束
- 你是团队领导，只负责：
  1. 理解用户需求并分发给团队成员
  2. 监控各 Agent 的工作进度
  3. 协调 Agent 之间的沟通
  4. 向用户汇报进度
- 你绝对不要：
  1. 自己写代码（看到 bug 也不要自己改！）
  2. 自己读大量代码文件
  3. 自己做探索性工作
- 原因：你的上下文大约 200K tokens，约 1.5 万行代码，
  一旦被代码占满就会触发压缩，导致丢失关键约束信息。
```


实战趣事：有开发者约束主 Agent 不干活，但主 Agent 看到 bug 还是忍不住自己改了，然后说"这个 bug 比较小，顺手就改了，下次不会了" 😄

#### 架构师 Agent


```
- 只做两件事：
  1. 审查每个人的 git 提交记录
  2. 检查代码是否符合 CLAUDE.md 中的规范
- 发现 DSL 或接口变更时，必须全局广播通知
```


#### 测试 Agent


```
- 不要去读源代码（避免上下文膨胀）
- 只通过接口文档和测试用例进行测试
- 测试有反馈有输入有输出（这很关键！）
- 发现 bug 后报告给主 Agent
```


### 9.4 Agent 间通信机制


```
┌────────────────────────────────────────────────────┐
│              Agent 通信示例                          │
├────────────────────────────────────────────────────┤
│                                                    │
│  后端 Agent → 前端 Agent:                           │
│  "API 对齐确认：POST /api/experiments               │
│   请求体: { name, dslConfig, metadata }             │
│   响应: { id, status, createdAt }                   │
│   SSE 流格式: event: progress, data: {...}"          │
│                                                    │
│  架构师 Agent → 全体广播:                            │
│  "DSL 规范已更新：pin 字段改名为 puzzle，              │
│   所有使用 DSL 的模块需要同步修改"                     │
│                                                    │
│  前端 Agent → 主 Agent:                             │
│  "test3 的指令方向与引擎实际情况冲突，                  │
│   需要确认后再执行。等待确认的同时，                    │
│   我先从 test4 开始做。"                              │
│                                                    │
│  主 Agent → 前端 Agent:                             │
│  "之前方向确实反了，任务描述已更新，                    │
│   请按新方向继续。"                                   │
│                                                    │
└────────────────────────────────────────────────────┘
```


### 9.5 Agent Teams 的已知限制与应对


| 限制 | 说明 | 应对方案 |
| --- | --- | --- |
| 消息不实时 | Agent 干完活才看消息 | 在 CLAUDE.md 中约束检查频率 |
| 默认自动关闭 | 每轮对话后会关闭成员 | 全局 CLAUDE.md 写明"不要自动关闭" |
| 并发写入冲突 | 多个 Agent 同时编辑同一文件 | 模块分工要清晰，减少文件交叉 |
| 无打断机制 | Agent 长时间工作时无法中途通知 | 可通过 Hooks 或自研插件解决 |
| 闷头干活 | Agent 不主动同步进度 | 在规范中约束定期汇报 |


### 9.6 多人协作时的代码管理


```
┌──────────────────────────────────────────────┐
│            多人 + 多Agent 协作模式              │
├──────────────────────────────────────────────┤
│                                              │
│  开发者A              开发者B    开发者C       │
│  (AI助手模块)         (编辑器)   (DSL引擎)    │
│     │                   │          │         │
│     ▼                   ▼          ▼         │
│  ┌──────┐           ┌──────┐  ┌──────┐      │
│  │ CC + │           │ CC + │  │ CC + │      │
│  │多Agent│           │多Agent│  │多Agent│      │
│  └──┬───┘           └──┬───┘  └──┬───┘      │
│     │                   │          │         │
│     ▼                   ▼          ▼         │
│  feature/ai-agent   feature/editor feature/  │
│  (独立分支)          (独立分支)    dsl-engine │
│     │                   │          │         │
│     └───────────────────┼──────────┘         │
│                         │                    │
│                    主分支合并                   │
│                    (解决冲突)                  │
│                         │                    │
│                    全量回归测试                 │
│                                              │
│  原则：                                       │
│  - 模块划分清楚，每人负责独立模块               │
│  - 大功能用不同分支，合并时处理冲突             │
│  - 个人并行任务可用 git worktree               │
│                                              │
└──────────────────────────────────────────────┘
```


### 9.7 Cowork 速览：不用终端的 AI Agent

Cowork 是 Anthropic 于 2026 年 1 月推出的桌面智能代理工具，内置于 Claude Desktop，以独立标签页的形式存在。核心定位：让不写代码的人也能使用 Agent 能力。

#### Cowork 能做什么？


| 能力 | 说明 |
| --- | --- |
| 文件操作 | 读取、编辑、创建本地文档（Word、PDF、表格、PPT 等） |
| 多步骤自动化 | 分解复杂任务为子任务，并行执行，实时展示进度 |
| 跨应用联动 | Excel 数据自动流入 PPT 摘要，输入变化时自动更新 |
| 浏览器操作 | 通过 Chrome 扩展做网页研究、表单填写、数据抓取 |
| 外部工具连接 | 通过 MCP 连接 Slack、Notion、Figma、Google Workspace 等 |


#### Cowork vs Claude Code


```
┌──────────────────────────────────────────────────┐
│          Cowork 与 Claude Code 对比                │
├─────────────────────┬────────────────────────────┤
│       Cowork        │      Claude Code           │
├─────────────────────┼────────────────────────────┤
│ 面向知识工作者       │ 面向开发者                  │
│ GUI 图形界面        │ Terminal 终端命令行          │
│ ❌ 不能执行代码      │ ✅ 可执行代码、跑测试        │
│ 操作文档和应用       │ 操作代码和项目               │
│ 沙盒 VM 隔离运行    │ 直接在本地终端运行            │
│ 任务前需确认计划     │ 可在会话内自主运行            │
│ 连接办公类工具       │ 连接开发类工具               │
├─────────────────────┴────────────────────────────┤
│                                                  │
│  一句话：Claude Code 改变了程序员的工作方式，       │
│  Cowork 要改变其余所有人的工作方式。                │
│                                                  │
└──────────────────────────────────────────────────┘
```


#### 使用方式

打开 Claude Desktop → 切换到 Cowork 标签页

授权文件夹：指定允许 Claude 访问的本地文件夹

安装插件：根据岗位选择对应插件（产品管理、财务、法务、市场等 11 类官方插件）

描述任务：用自然语言说清想要的结果

Claude 展示执行计划，确认后自动执行，实时显示进度

⚠️ 需要 Claude Pro（$20/月）或以上订阅。Cowork 目前仍处于 Research Preview 阶段。

#### 什么时候用 Cowork？


| 场景 | 选择 |
| --- | --- |
| 写代码、跑测试、调试 | Claude Code |
| 分析报表、整理文档、做 PPT | Cowork |
| 调研竞品、抓取网页数据 | Cowork |
| 部署项目、CI/CD | Claude Code |
| 管理 Slack/Notion/Figma | Cowork |


### 9.8 一张图看清四者的关系与边界

Skills、Subagents、Plugins、Agent Teams 这四个概念容易混淆，下面用一张图理清它们的关系：


```
┌────────────────────────────────────────────────────────────────────┐
│        Skills · Subagents · Plugins · Agent Teams 全景关系图        │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌─ Agent Teams ──────────────────────────────────────────────┐   │
│  │                                                            │   │
│  │  Team Leader（主 Agent）                                    │   │
│  │  ┌────────────────────────────────────┐                   │   │
│  │  │  可加载 Skills    可调用 Subagents   │                   │   │
│  │  │  可使用 Plugins   可安装 MCP        │                   │   │
│  │  └────────────────────────────────────┘                   │   │
│  │       │ 分发任务           │ 分发任务                      │   │
│  │       ▼                   ▼                               │   │
│  │  ┌──────────┐       ┌──────────┐                          │   │
│  │  │ Teammate │       │ Teammate │   ← 每个都是独立 Agent    │   │
│  │  │ 前端工程师│       │ 后端工程师│     有自己的上下文         │   │
│  │  │ (可加载   │       │ (可加载   │     可加载 Skills        │   │
│  │  │  Skills)  │       │  Skills)  │     可调用 Subagents    │   │
│  │  └──────────┘       └──────────┘                          │   │
│  │                                                            │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌─ Skill ─────────┐  ┌─ Subagent ────┐  ┌─ Plugin ──────────┐  │
│  │                  │  │               │  │                    │  │
│  │ 一张"任务卡片"   │  │ 独立上下文的   │  │ Skills 的打包集合  │  │
│  │                  │  │ 专业 Agent    │  │                    │  │
│  │ 注入到当前Agent  │  │               │  │ 方便团队分发复用   │  │
│  │ 的上下文中执行   │  │ 执行完只返回   │  │                    │  │
│  │                  │  │ 总结给调用者   │  │ 一个 Plugin 可包含 │  │
│  │ 共享调用者的     │  │               │  │ 多个 Skills       │  │
│  │ 上下文（会占用） │  │ 不污染调用者   │  │                    │  │
│  │                  │  │ 的上下文      │  │ 支持 marketplace  │  │
│  └──────────────────┘  └───────────────┘  └────────────────────┘  │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  快速选型判断：                                                     │
│                                                                    │
│  "我需要一套固定工作流"         → Skill                             │
│  "我需要调研但不想污染上下文"   → Subagent                           │
│  "我要把多个 Skill 分享给团队"  → Plugin                            │
│  "我要多人并行干大活"           → Agent Teams                       │
│  "任务简单，不涉及代码"         → Cowork                            │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```


| 维度 | Skill | Subagent | Plugin | Agent Teams |
| --- | --- | --- | --- | --- |
| 本质 | 任务卡片/工作流 | 独立上下文的 Agent | Skills 的打包集合 | 多 Agent 并行协作 |
| 上下文 | 共享调用者上下文 | 独立上下文 | 同 Skill | 每个成员独立上下文 |
| 触发方式 | /命令 或自动匹配 | Claude 自主决定 | 安装后同 Skill | 用户指令或自动 |
| 适合场景 | 重复性工作流 | 调研、探索、分析 | 团队共享标准化流程 | 复杂项目并行开发 |
| 文件位置 | .claude/skills/ | 无独立文件 | .claude/plugins/ | 运行时动态创建 |
| 复用性 | 项目内复用 | 一次性 | 跨项目/跨团队复用 | 按需组建 |


## 第十章：上下文管理 — 核心中的核心

"上下文管理是使用多 Agent 编程中最重要的事情。一旦上下文爆炸触发压缩，模型就会忘掉你的约束细节，返工明显变多。" —— 实战经验

### 10.1 理解上下文限制


```
┌──────────────────────────────────────────────────┐
│               上下文窗口示意图                      │
├──────────────────────────────────────────────────┤
│                                                  │
│  ┌─────────────────────────────────────────┐     │
│  │          上下文窗口 (~200K tokens)        │     │
│  │                                         │     │
│  │  ┌───────────────────────────┐          │     │
│  │  │ 系统提示 + CLAUDE.md       │ ← 始终保持│     │
│  │  └───────────────────────────┘          │     │
│  │  ┌───────────────────────────┐          │     │
│  │  │ Skills + Hooks 注入        │ ← 始终保持│     │
│  │  └───────────────────────────┘          │     │
│  │  ┌───────────────────────────┐          │     │
│  │  │ 对话历史                   │ ← 越来越长│     │
│  │  │ 代码文件内容               │          │     │
│  │  │ 工具调用结果               │          │     │
│  │  │ ...                       │          │     │
│  │  └───────────────────────────┘          │     │
│  │                                         │     │
│  │  ⚠️ 超过限制 → 触发压缩 → 丢失细节！     │     │
│  │                                         │     │
│  └─────────────────────────────────────────┘     │
│                                                  │
│  约 200K tokens ≈ 约 1.5 万行代码                 │
│  主 Agent 约 10 分钟就容易触发压缩                  │
│                                                  │
└──────────────────────────────────────────────────┘
```


### 10.2 .claudeignore — 减少上下文噪音

在项目根目录创建 `.claudeignore` 文件（语法同 `.gitignore`），可以减少 40-60% 的搜索空间：


```
# .claudeignore
node_modules/
dist/
build/
.git/
*.min.js
*.map
vendor/
coverage/
__pycache__/
*.pyc
```


💡 核心作用：不让 Claude 读取这些目录的文件，避免无关代码污染上下文。

### 10.3 上下文管理策略


```
┌─────────────────────────────────────────────────────┐
│              上下文管理七大策略                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1️⃣ 主 Agent 不干活                                 │
│     不读代码、不写代码，只统筹分发                      │
│     → 保持上下文清洁                                  │
│                                                     │
│  2️⃣ 任务间 /clear                                   │
│     不相关任务之间清空上下文                            │
│     → 避免"厨房水槽"式会话                            │
│                                                     │
│  3️⃣ 用 subagent 做调研                              │
│     探索代码库时使用子agent                            │
│     → 调研结果不污染主上下文                           │
│                                                     │
│  4️⃣ compact 时重读规范                              │
│     在 CLAUDE.md 中写明：                            │
│     "compact 后必须重新读取此文件"                     │
│     → 压缩后不丢失关键约束                            │
│                                                     │
│  5️⃣ 分阶段干活                                      │
│     每个阶段有明确目标和边界                           │
│     → 避免一次性给太多任务                             │
│                                                     │
│  6️⃣ 精确的指令                                      │
│     上下文给不够会引起歧义                             │
│     上下文给太多会分散注意力                            │
│     → 只提供必要且精确的信息                           │
│                                                     │
│  7️⃣ 约束文件读取范围                                  │
│     "不要读 vendor/ 目录的代码"                       │
│     "只读 src/auth/ 目录"                            │
│     → 减少不必要的上下文消耗                           │
│                                                     │
└─────────────────────────────────────────────────────┘
```


### 10.4 上下文管理命令


```bash
/clear                          # 完全清空上下文（任务切换时用）
/compact                        # 压缩上下文（保留重要信息）
/compact 保留 API 变更记录       # 带指引的压缩
Esc + Esc                       # 回滚到之前的检查点
/rewind                         # 打开回滚菜单
```


自动压缩触发时机：当上下文达到约 80% 容量（~160K tokens）时自动触发压缩。压缩后约 70K tokens 可压缩到约 4K tokens 的摘要。

### 10.5 模型的"大海捞针"问题

模型有注意力限制——即使上下文足够大，也不一定能注意到所有信息：


```
  上下文中有 200K tokens 的内容...

  ┌─────────────────────────────────────┐
  │  开头部分 ← 注意力强                  │
  │  ...                                │
  │  ...                                │
  │  重要约束（写在中间位置）← 可能被忽略！ │
  │  ...                                │
  │  ...                                │
  │  最近的对话 ← 注意力强                │
  └─────────────────────────────────────┘
```


应对方法：重要的约束多次强调、放在 CLAUDE.md 开头、compact 时指定保留。


## 第十一章：开发范式与实战案例

### 11.1 规范驱动 vs 测试驱动


```
┌────────────────────────────────────────────────────┐
│         两种开发驱动方式的对比                        │
├──────────────────────┬─────────────────────────────┤
│    规范驱动开发        │     测试驱动开发              │
├──────────────────────┼─────────────────────────────┤
│ 重点：定义清楚架构、   │ 重点：测试通过即可，          │
│ 编码规范、行为约束     │ 不管内部代码结构              │
│                      │                             │
│ 优点：                │ 优点：                       │
│ - 代码人类可读        │ - 自动化验证                  │
│ - 架构清晰可维护      │ - 模型可自主迭代修复          │
│ - 减少返工            │ - 黑盒方式更高效              │
│                      │                             │
│ 缺点：                │ 缺点：                       │
│ - 前置投入大          │ - 测试覆盖不全               │
│ - 规范需要持续迭代    │ - 代码可能不可读              │
│                      │ - 无法穷尽所有场景            │
├──────────────────────┴─────────────────────────────┤
│                                                    │
│  ✅ 实战结论：两者都需要！                            │
│                                                    │
│  - 规范保证代码可读、架构合理                         │
│  - 测试保证功能正确、模型可自主迭代                    │
│  - 规范在前置制定，测试要有反馈有输入有输出             │
│                                                    │
└────────────────────────────────────────────────────┘
```


### 11.2 整体到局部的开发模式


```
┌──────────────────────────────────────────────────────┐
│              推荐的开发流程                             │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Phase 1: 构思规范（小半天）                            │
│  ┌──────────────────────────────────┐                │
│  │ - 编写 CLAUDE.md                  │                │
│  │ - 定义技术栈、架构、红线           │                │
│  │ - 准备 DSL/接口规范               │                │
│  │ - 配置 Skills 和工具链             │                │
│  └───────────────┬──────────────────┘                │
│                  │                                   │
│  Phase 2: 整体搭建（2-6小时）                          │
│  ┌───────────────┴──────────────────┐                │
│  │ - 多 Agent 并行开发所有模块        │                │
│  │ - 主流程先不阻塞（先通再调）       │                │
│  │ - 搭建基本框架和接口              │                │
│  │ - 确保主流程跑通                  │                │
│  └───────────────┬──────────────────┘                │
│                  │                                   │
│  Phase 3: 局部精调（持续迭代）                          │
│  ┌───────────────┴──────────────────┐                │
│  │ - 分模块精细化调整                │                │
│  │ - 每人负责一个模块的细节           │                │
│  │ - 100+轮交互打磨复杂交互          │                │
│  │ - 修复 bug、优化体验              │                │
│  └───────────────┬──────────────────┘                │
│                  │                                   │
│  Phase 4: 合并验证                                    │
│  ┌───────────────┴──────────────────┐                │
│  │ - 合并各模块代码                   │                │
│  │ - 跑主流程全量回归                 │                │
│  │ - 发现问题用 Agent 修复            │                │
│  │ - 测试 Agent 做端到端验证          │                │
│  └──────────────────────────────────┘                │
│                                                      │
└──────────────────────────────────────────────────────┘
```


### 11.3 实战案例：科创实验制作工具

这是一个真实的复杂项目案例，展示了完整的多 Agent 开发流程：项目背景：

原来每个实验需要 20-28 个工作日人工开发

目标：用 AI 将 UI 稿和脚本描述自动转换为可交互的 Cocos 实验项目架构：


```
┌──────────────────────────────────────────────────────┐
│            科创实验制作工具 架构图                       │
├──────────────────────────────────────────────────────┤
│                                                      │
│  输入                     处理                输出    │
│  ┌──────┐               ┌──────┐          ┌──────┐  │
│  │MasterGo│    模块1     │  AI  │          │ Cocos│  │
│  │UI设计稿├──→│ UI+脚本  ├─→│ 助手 ├─→DSL──→│ 渲染 │  │
│  └──────┘   │ → DSL    │  │(Agent)│       │ 引擎 │  │
│  ┌──────┐   └──────────┘  └──────┘       └──────┘  │
│  │实验脚本│                                          │
│  │自然语言│        模块2                              │
│  └──────┘   ┌──────────────┐                        │
│             │  DSL 引擎     │                        │
│             │  DSL → Cocos  │                        │
│             │  游戏画面渲染  │                        │
│             └──────────────┘                        │
│                                                      │
│                    模块3                              │
│             ┌──────────────┐                        │
│             │  实验编辑器   │                         │
│             │  人工精细调整 │                         │
│             │  (类似IDE)   │                         │
│             └──────────────┘                        │
│                                                      │
│  关键创新：                                           │
│  - 让模型通读 96 个已有实验代码，自动归纳出 DSL 规范     │
│  - DSL 完成度 80%+，大幅减少人工                       │
│  - 同时做了 H5 和 Cocos 两个版本"赛马"                 │
│                                                      │
└──────────────────────────────────────────────────────┘
```


开发过程：


| 阶段 | 工作内容 | 耗时 |
| --- | --- | --- |
| 规范制定 | 编写 CLAUDE.md、定义 DSL、配置技术栈 | ~小半天 |
| 整体搭建 | 6 个 Agent 并行开发全部模块 | ~6 小时 |
| 细节调优 | 3 人各负责一个模块精调 | 100+ 轮交互 |
| 综合提效 | 对比传统开发模式 | 约 5 倍 |
| Agent 团队配置： |  |  |
| Agent 角色 | 职责 | 关键约束 |
| ------------ | ------ | ---------- |
| 主 Agent | 统筹全局，分发任务 | 绝不自己写代码 |
| 产品经理 | 定义需求，功能验收 | 会主动降级非关键需求到 v1.1 |
| 架构师 | 审查 git 提交，维护规范 | 发现规范变更时全局广播 |
| 前端工程师 | 编辑器页面开发 | 专注于交互和样式 |
| 后端工程师 | API 和数据逻辑 | 主动与前端对齐接口 |
| AI 助手开发 | 提示词调优，LangChain 编排 | 使用 Skills 指导 DSL 生成 |


### 11.4 自动化测试的关键作用


```
┌──────────────────────────────────────────────────────┐
│            自动化测试让模型自主迭代                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  关键洞察：一旦有自动化测试，模型就能自己迭代！          │
│                                                      │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐       │
│  │  写代码  │ ──→ │  跑测试  │ ──→ │ 有报错？ │       │
│  └─────────┘     └─────────┘     └────┬────┘       │
│       ▲                               │             │
│       │              是               │ 否           │
│       │               │               │             │
│       │          ┌────┴────┐     ┌────┴────┐       │
│       └──────────│ 修复代码 │     │  完成！  │       │
│                  └─────────┘     └─────────┘       │
│                                                      │
│  实战案例：                                           │
│  - 吴老师的项目：有编译错误反馈 → 持续运行1-2天          │
│  - 笔记引擎：Playwright 截图对比 → 自动发现笔迹回缩bug  │
│  - 服务端测试：批量脚本跑接口 → 全自动回归              │
│                                                      │
│  测试的关键要求：                                      │
│  ✅ 有明确的输入和输出                                  │
│  ✅ 报错信息模型可读                                    │
│  ✅ 成功/失败状态明确                                   │
│  ✅ 可以重复执行                                       │
│                                                      │
└──────────────────────────────────────────────────────┘
```


## 第十二章：让 AI 帮你测 —— Claude Code 测试全链路落地


```
让 AI 帮你测 —— Claude Code 测试全链路落地
```


## 第十三章：OpenClaw — 用手机遥控 Claude Code 7×24 小时工作

想象一下：你在通勤路上打开飞书，发一条消息"帮我把 src/auth 模块的单元测试补全"，家里的电脑就自动开始干活，干完了把结果发回你手机。这就是 OpenClaw + Claude Code 的威力。

### 12.1 OpenClaw 是什么？

OpenClaw（开源，MIT 协议）是一个自主 AI 代理，它的核心理念是：把消息应用变成 AI 的操控界面。它能做到：

连接飞书、微信、Telegram、Slack、WhatsApp 等几乎所有消息平台

以 7×24 小时守护进程运行在你的电脑上

通过 MCP 协议调用 Claude Code 执行编程任务

你在手机上发消息 → AI 在电脑上干活 → 结果发回手机


| 信息 | 内容 |
| --- | --- |
| 官网 | https://openclaw.ai/ |
| GitHub | https://github.com/openclaw/openclaw |
| 官方文档 | https://docs.openclaw.ai/ |
| 中文教程（社区） | Claude Code x OpenClaw 中文指南 |


### 12.2 核心配置文件体系

OpenClaw 使用 Markdown 文件作为 Agent 的"操作系统"，所有文件存放于 `~/.openclaw/workspace/`。每次对话开始时自动注入系统提示词，形成 Agent 的持久化上下文。


```
~/.openclaw/workspace/
├── AGENTS.md          ← 主指令合约（优先级最高）
├── SOUL.md            ← 灵魂与人格定义
├── IDENTITY.md        ← 身份档案
├── USER.md            ← 用户偏好层
├── TOOLS.md           ← 工具使用说明
├── MEMORY.md          ← 长期记忆
├── HEARTBEAT.md       ← 心跳任务清单
├── BOOT.md            ← 启动仪式脚本
└── memory/
    └── 2026-03-05.md  ← 每日记忆日志
```


八大核心文件速查表：


| 文件 | 定位 | 作用 |
| --- | --- | --- |
| AGENTS.md | 主指令合约 | 定义工作优先级、行为边界、质量标准。最顶层规则，优先级最高 |
| SOUL.md | 灵魂人格层 | 定义声音风格、性情、价值观和不可违背约束。保持长期稳定 |
| IDENTITY.md | 身份档案 | Agent 的名字、角色、目标、声音风格。首次 Bootstrap 时自动生成 |
| USER.md | 用户偏好 | 语言偏好、沟通风格、输出格式习惯。让 Agent 记住"你想要什么" |
| TOOLS.md | 工具说明 | 记录本地工具信息（SSH 别名、设备昵称等），仅指导不控制可用性 |
| MEMORY.md | 长期记忆 | 跨日对话的持久事实、重大决策。手动维护，保持精简 |
| HEARTBEAT.md | 心跳清单 | 定义心跳触发时的检查项。保持极简避免 prompt 膨胀 |
| BOOT.md | 启动脚本 | Agent 启动时的仪式提示词，需在 openclaw.json 中启用 |


💡 类比 Claude Code：AGENTS.md 类似 CLAUDE.md，SOUL.md 是 OpenClaw 独有的"人格层"。你可以用 `soul-md` skill 让 Claude Code 分析你的数据自动生成个性化 SOUL.md。

### 12.3 会话概念与工作机制

OpenClaw 的会话由 Gateway 管理，Session Key 格式为 `agent:<agentId>:<mainKey>`。


```
┌──────────────────────────────────────────────────┐
│              OpenClaw 会话路由                     │
├──────────────────────────────────────────────────┤
│                                                  │
│  飞书对话 ──→ agent:main:feishu_user123          │
│  微信对话 ──→ agent:main:wechat_user123          │
│  WebUI   ──→ agent:main:webui                   │
│  CLI     ──→ agent:main:cli                     │
│                                                  │
│  同一用户、不同频道 = 不同 Session                  │
│  ✅ 防止跨上下文数据泄露                            │
│                                                  │
│  所有频道通过 Gateway 统一路由                      │
│  Gateway = 单一 Node.js 进程（hub-and-spoke）     │
│                                                  │
└──────────────────────────────────────────────────┘
```


### 12.4 记忆机制详解

OpenClaw 的记忆系统采用"Markdown 文件 + 混合搜索索引"架构，是其核心能力之一。

可以让 Claude Code 帮你配置Ollama 向量搜索模型。双层记忆结构：


| 层级 | 文件 | 特点 |
| --- | --- | --- |
| 长期记忆 | MEMORY.md | 手动维护，精简稳定，跨日加载 |
| 每日日志 | memory/YYYY-MM-DD.md | 自动写入，记录当天发生的事、学到的知识 |
| 混合搜索检索： |  |  |


| 搜索类型 | 权重 | 技术 | 特点 |
| --- | --- | --- | --- |
| 向量语义搜索 | 70% | SQLite + sqlite-vec | 基于含义匹配，词不同也能找到 |
| BM25 全文搜索 | 30% | SQLite FTS5 | 基于关键词精确匹配 |


时间衰减：旧记忆自动降权，近期记忆优先

Agent 工具：通过 `memory_search`（语义召回）和 `memory_get`（定向读取）访问记忆

这就是"让 AI 助理越用越聪明"的秘密——每天的对话都在积累经验，下次遇到类似问题它会自动检索历史。

### 12.5 心跳机制 — 让 AI 主动工作

心跳机制将 OpenClaw 从"被动响应"变成"主动感知"。工作原理：


```
每隔 X 分钟（默认 30 min）
      │
      ▼
Gateway 发送心跳提示词 → Agent 读取 HEARTBEAT.md
      │
      ├── 无需处理 → 回复 HEARTBEAT_OK（静默）
      │
      └── 发现待办 → 主动发消息通知用户
```


配置示例（openclaw.json）：


```json
{
  "heartbeat": {
    "enabled": true,
    "interval": 30,
    "target": "last",
    "activeHours": {
      "start": "08:00",
      "end": "22:00"
    }
  }
}
```


省钱技巧：

用 Haiku（最便宜的模型）做心跳检查，只在真正需要关注时升级到 Sonnet/Opus

`HEARTBEAT.md` 保持极简（短 checklist），避免 prompt 膨胀

如果 `HEARTBEAT.md` 为空，OpenClaw 会自动跳过该次心跳，节省 API 调用

### 12.6 WebUI 控制台

OpenClaw 自带 Web 控制界面，默认运行在本地端口 18789。访问地址： `http://127.0.0.1:18789`


| 功能模块 | 说明 |
| --- | --- |
| Web 聊天 | 无需配置频道即可直接对话，适合测试 |
| 调试工具 | 查看 Agent 执行日志、工具调用记录 |
| 模型配置 | 添加 AI 提供商（Anthropic、OpenAI 等） |
| 安全管理 | 审批授权设备 |
| 会话历史 | 查看完整对话记录（JSONL 格式） |


```
控制平面架构：
┌──────────────────────┐
│  Gateway (:18789)    │
├──────────────────────┤
│  ├── Web UI（浏览器） │
│  ├── CLI 客户端       │
│  ├── macOS App       │
│  └── 移动端节点       │
└──────────────────────┘
```


### 12.7 安全注意事项与 Token 管理

#### 安全风险速览


| 风险 | 说明 | 防护 |
| --- | --- | --- |
| 提示词注入 | 恶意邮件/网页中的指令可能被 Agent 执行 | 工具策略 + 沙箱隔离 + 频道白名单 |
| 恶意 Skills | 社区 skill 中约 36% 存在安全缺陷 | 只使用官方或可信来源的 skill |
| 数据泄露 | 群聊中工具可能读取环境变量和 API Key | 限制工具权限 + 环境变量隔离 |


💡 可安装 clawsec 安全 skill 套件，提供漂移检测、自动审计、skill 完整性验证。

#### Token 费用管理

三层模型策略（推荐）：


| 任务类型 | 推荐模型 | 说明 |
| --- | --- | --- |
| 心跳检查、简单查询 | Claude Haiku | 70-80% 任务可用此层 |
| 日常工作流 | Claude Sonnet | 平衡能力与成本 |
| 复杂分析、架构决策 | Claude Opus | 仅在必要时使用 |
| 省钱技巧： |  |  |


将上下文窗口从默认 400K 限制到 50K-100K

精简注入文件（减少 1000 token × Opus 100 次/天 ≈ 省 $45/月）

利用 Prompt Cache 降低重复内容成本

心跳间隔配置为略小于缓存 TTL，保持缓存"温热"

### 12.8 前置准备

在安装之前，你需要准备以下东西：1. 一台常开的电脑OpenClaw 运行在你的本地电脑上（很多人用 Mac Mini 当"家庭服务器"）。关机 = AI 下班。2. Node.js 22+OpenClaw 要求 Node.js 22 以上版本。检查你的版本：


```bash
node --version
```


如果版本太低或未安装，用以下方式安装最新版：


```bash
# macOS (Homebrew)
brew install node
# 或使用 nvm 管理多版本
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
nvm install 22
nvm use 22
```


📖 Node.js 官网下载：https://nodejs.org/

3. Anthropic API KeyOpenClaw 需要一个 AI 模型的 API Key 来驱动对话。推荐使用 Anthropic（Claude 的官方 API）。获取步骤：

访问 Anthropic Console

注册或登录账号

进入 API Keys 页面

点击 Create Key，复制保存（格式为 `sk-ant-api03-...`）

在 Billing 页面充值余额（按量付费）

⚠️ API Key 是付费的，和 Claude Code Max 订阅是两套独立的付费体系。API 按 token 用量计费，建议先充 $5-10 试用。

4. 飞书开放平台应用（如果要连飞书）后面的飞书章节会详细讲。

### 12.9 用 Claude Code 安装 OpenClaw

这是最酷的部分——你不需要自己折腾安装，直接让 Claude Code 帮你装：


```
帮我安装 OpenClaw，要求：
1. 检查我的 Node.js 版本是否 >= 22，不够的话帮我升级
2. 用 npm 全局安装 openclaw
3. 运行 openclaw onboard 帮我完成初始化
4. 把它注册为系统守护进程，开机自启
```


Claude Code 会自动执行以下操作：


```bash
# 1. 检查 Node.js 版本
node --version
# 2. 安装 OpenClaw
npm install -g openclaw@latest
# 3. 初始化并注册守护进程
openclaw onboard --install-daemon
```


初始化向导会引导你完成：

Gateway 网关配置

AI 模型和 API Key 设置

消息渠道连接

守护进程注册（macOS 用 launchd，Linux 用 systemd）

当然你也可以用官方一行命令安装：`curl -fsSL https://get.openclaw.ai | bash`

### 12.10 配置 AI 模型和 API Key

安装完成后需要配置 AI 模型。推荐 Anthropic Claude：方式一：让 Claude Code 帮你配置


```
帮我配置 OpenClaw 的 AI 模型，使用 Anthropic Claude，
我的 API Key 是 sk-ant-api03-xxxxx
```


方式二：手动命令


```bash
# 设置默认模型
openclaw models set anthropic/claude-sonnet-4-20250514
# API Key 会在 onboard 过程中设置，也可以用环境变量
export ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```


方式三：编辑配置文件配置文件位置：`~/.openclaw/openclaw.json`


```json
{
  "models": {
    "default": "anthropic/claude-sonnet-4-20250514"
  }
}
```


⚠️ 安全提醒：不要把 API Key 硬编码在配置文件中，推荐使用环境变量。

### 12.11 连接飞书（Feishu）

📖 官方飞书文档：https://docs.openclaw.ai/zh-CN/channels/feishu

#### 第一步：创建飞书应用

登录 飞书开放平台

点击"创建企业自建应用"，填写名称（如"AI 编程助手"）

在"凭证与基本信息"页面，记下 App ID（格式 `cli_xxx`）和 App Secret

添加应用能力 → 启用"机器人"

配置事件订阅 → 选择"使用 WebSocket 长连接"→ 添加 `im.message.receive_v1` 事件

配置权限：添加消息收发、文件读取等权限

发布应用

#### 第二步：安装飞书插件并配置

你可以直接让 Claude Code 帮你完成：


```
帮我给 OpenClaw 安装飞书插件并配置，
我的飞书 App ID 是 cli_xxx，App Secret 是 xxx
```


或者手动操作：


```bash
# 安装飞书插件
openclaw plugins install @openclaw/feishu
# 交互式配置（推荐）
openclaw channels add
# 选择 Feishu → 输入 App ID 和 App Secret
```


#### 第三步：启动并测试


```bash
# 启动网关
openclaw gateway
# 在飞书中找到你的机器人，发送一条消息测试
# 首次需要批准配对
openclaw pairing approve feishu <配对码>
```


配对完成后，你就可以在飞书中和 AI 对话了！

### 12.12 安装 Claude Code Skill — 打通编程能力

默认的 OpenClaw 只有通用对话能力。要让它能操控 Claude Code 写代码，需要安装 Claude Code Skill：

📖 GitHub：https://github.com/Enderfga/openclaw-claude-code-skill

让 Claude Code 帮你安装：


```
帮我安装 openclaw-claude-code-skill，步骤：
1. git clone https://github.com/Enderfga/openclaw-claude-code-skill.git
2. 进入目录，npm install 然后 npm run build
3. npm link 全局链接
```


安装完成后，你可以通过飞书发送编程指令：


```
# 在飞书中给机器人发消息
在 ~/my-project 目录下帮我创建一个 Express API 项目，
包含用户注册和登录接口，使用 JWT 认证
```


OpenClaw 收到消息后会调用 Claude Code 执行，完成后把结果发回飞书。

### 12.13 实现 7×24 小时自动工作

#### 守护进程（已在安装时配置）

如果安装时用了 `--install-daemon`，OpenClaw 已经注册为系统守护进程：


```bash
# 检查网关状态
openclaw gateway status
# 重启网关
openclaw gateway restart
# 查看实时日志
openclaw logs --follow
```


macOS：注册为 launchd 服务，开机自启

Linux：注册为 systemd 服务，开机自启

#### 典型的 7×24 工作流


```
你的手机（飞书/微信/Telegram）
    │
    │  "帮我修复 issue #42"
    ▼
OpenClaw Gateway（家里电脑，7×24 运行）
    │
    │  解析指令，调用 Claude Code Skill
    ▼
Claude Code CLI（执行编程任务）
    │
    │  读代码、改代码、跑测试
    ▼
执行结果返回
    │
    │  "已修复，测试全部通过，已提交到 fix/issue-42 分支"
    ▼
你的手机（收到结果通知）
```


你可以在这些场景使用：

通勤路上：发消息让 AI 做方案研究

午休时：发消息让 AI 修 bug

睡觉前：发消息让 AI 跑一个大任务，第二天早上看结果

开会时：发消息让 AI 准备技术方案

### 12.14 完整流程速查


| 步骤 | 操作 | 说明 |
| --- | --- | --- |
| 1 | 准备 Node.js 22+ | node --version 检查 |
| 2 | 获取 Anthropic API Key | console.anthropic.com |
| 3 | 安装 OpenClaw | npm install -g openclaw@latest |
| 4 | 初始化 | openclaw onboard --install-daemon |
| 5 | 配置模型 | openclaw models set anthropic/claude-sonnet-4-20250514 |
| 6 | 创建飞书应用 | open.feishu.cn |
| 7 | 安装飞书插件 | openclaw plugins install @openclaw/feishu |
| 8 | 配置飞书 | openclaw channels add |
| 9 | 安装 Claude Code Skill | clone + build + link |
| 10 | 启动 | openclaw gateway |
| 11 | 飞书发消息测试 | 给机器人发"你好"验证连通 |


一句话总结：安装 OpenClaw → 配 API Key → 连飞书 → 装 Claude Code Skill → 手机发消息就能让电脑上的 AI 干活，7×24 不停歇。第十三章：常见问题与进阶技巧

## 第十四章：学习路径总结


```
┌──────────────────────────────────────────────────────┐
│          从零到精通的学习路径                            │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Level 1: 入门（1-2天）                               │
│  ┌──────────────────────────────────────┐            │
│  │ ✅ 安装 Claude Code                   │            │
│  │ ✅ 学会基本对话和命令                  │            │
│  │ ✅ 用自然语言让 Claude 写简单功能       │            │
│  │ ✅ 学会用 /clear、/compact 管理上下文  │            │
│  └──────────────────────────────────────┘            │
│         │                                            │
│         ▼                                            │
│  Level 2: 进阶（1周）                                 │
│  ┌──────────────────────────────────────┐            │
│  │ ✅ 编写项目级 CLAUDE.md               │            │
│  │ ✅ 创建和使用 Skills                   │            │
│  │ ✅ 配置 MCP Servers（如 Playwright）   │            │
│  │ ✅ 使用 subagent 做代码调研            │            │
│  │ ✅ 掌握上下文管理技巧                  │            │
│  └──────────────────────────────────────┘            │
│         │                                            │
│         ▼                                            │
│  Level 3: 高级（2-4周）                               │
│  ┌──────────────────────────────────────┐            │
│  │ ✅ 安装和使用 Superpowers 等插件       │            │
│  │ ✅ 配置 Hooks 自动化工作流             │            │
│  │ ✅ 创建自定义 subagent                 │            │
│  │ ✅ 使用 Agent Teams 多agent协作        │            │
│  │ ✅ 设计 Agent 角色和协作规范            │            │
│  └──────────────────────────────────────┘            │
│         │                                            │
│         ▼                                            │
│  Level 4: 精通（持续实践）                             │
│  ┌──────────────────────────────────────┐            │
│  │ ✅ 自研 Claude Code 插件               │            │
│  │ ✅ 多人 + 多 Agent 复杂项目协作         │            │
│  │ ✅ 自动化测试驱动的持续开发             │            │
│  │ ✅ OpenCode + Claude Code 联合使用      │            │
│  │ ✅ 从需求到上线的全流程 AI 辅助          │            │
│  │ ✅ 编写团队级别的开发范式和规范          │            │
│  └──────────────────────────────────────┘            │
│                                                      │
└──────────────────────────────────────────────────────┘
```


### 13.2 常见问题解答

**Q: 模型写的代码敢不敢上线？**

实战经验：功能正确、测试通过的代码是可以上线的。有开发者全年使用模型写的 C++ 引擎已在生产环境运行。但建议：

服务端接口代码：风险较低，测试通过即可

基础设施代码：需要更谨慎的人工 review

关键路径代码：必须有完善的自动化测试


**Q: 模型老是跑偏怎么办？**

约束更精确的 CLAUDE.md

纠正超过两次就 `/clear` 重新来

使用 superpowers 分阶段隔离上下文

让 Agent 之间互相纠错


**Q: 存量项目怎么用 Claude Code？**

先在 CLAUDE.md 描述项目各模块的功能

告诉模型哪些目录做什么（减少探索时间）

约束只读取相关模块的代码

按模块逐步接入，不要一次性全交给模型

**Q: 颗粒度怎么把控？太小浪费时间，太大模型理解不了？**

按模块/功能点提供

信息越精确，模型干得越好

怎么跟研发讲话，就怎么跟 Claude 讲话

关键信息不够时，模型会反问你

**Q: Claude Code 太贵了怎么办？**

Claude Code Max 计划可以大量使用 Opus 模型

可以多人共用账号（但注意额度限制）

简单任务用 Sonnet/Haiku 降低成本（Claude 会自动切换）

考虑 OpenCode + Codex 作为补充（可互相修复）

### 13.3 思想转变清单


```
┌──────────────────────────────────────────────────────┐
│              AI 开发时代的思维转变                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ❌ 旧思维                    ✅ 新思维               │
│  ─────────────                ─────────────          │
│  遇到问题先问同事              遇到问题先问模型        │
│                                                      │
│  代码必须自己写                代码让模型写，自己审    │
│                                                      │
│  一个人闷头写代码              指挥多个 Agent 并行     │
│                                                      │
│  写完代码手动测试              自动化测试让模型自迭代  │
│                                                      │
│  需求文档给人看                需求文档也要模型可读    │
│                                                      │
│  测试用例人工执行              测试要有输入输出反馈    │
│                                                      │
│  不敢用模型写的代码            测试通过就可以信任      │
│                                                      │
│  每个功能从零开发              先整体后局部，MVP先行   │
│                                                      │
│  用垃圾模型省钱                用最好的模型省时间      │
│                                                      │
└──────────────────────────────────────────────────────┘
```


### 13.4 工具组合推荐


```
┌──────────────────────────────────────────────────────┐
│              推荐的工具组合                              │
├──────────────────────────────────────────────────────┤
│                                                      │
│  核心工具：                                            │
│  ┌────────────────────────────────────┐              │
│  │ Claude Code (Max 计划 + Opus 模型)  │ ← 主力开发   │
│  └────────────────────────────────────┘              │
│                                                      │
│  补充工具：                                            │
│  ┌────────────────────────────────────┐              │
│  │ OpenClaw                            │ ← 7×24运行  │
│  │ 可以在手机上发消息让电脑干活          │              │
│  └────────────────────────────────────┘              │
│  ┌────────────────────────────────────┐              │
│  │ Codex                               │ ← 精细修改  │
│  │ 改动范围小，适合存量代码微调          │              │
│  └────────────────────────────────────┘              │
│  ┌────────────────────────────────────┐              │
│  │ Cursor                              │ ← 可视化    │
│  │ 有文件级别的可视化，精细调整 UI       │              │
│  └────────────────────────────────────┘              │
│                                                      │
│  插件：                                               │
│  ┌────────────────────────────────────┐              │
│  │ Superpowers                         │ ← 开发工作流│
│  │ Playwright MCP                      │ ← 浏览器测试│
│  │ 自研团队管理插件                     │ ← 定制需求  │
│  └────────────────────────────────────┘              │
│                                                      │
│  互相救场：                                            │
│  CC 挂了 → OpenClaw 继续                              │
│  OpenClaw 挂了 → CC、codex 继续                              │
│  只要有一个活着，另外两个就永远活着 😄                   │
│                                                      │
└──────────────────────────────────────────────────────┘
```


## 附录

### A. 快速参考卡


```
═══════════════════════════════════════════════════
             Claude Code 快速参考卡
═══════════════════════════════════════════════════

📁 关键文件位置：
  ~/.claude/CLAUDE.md          全局规范
  项目/CLAUDE.md               项目规范
  项目/.claude/settings.json   MCP + Hooks 配置
  项目/.claude/skills/         Skills 定义
  项目/.claude/agents/         Subagents 定义

⌨️ 核心快捷键：
  Esc           停止当前操作
  Esc + Esc     回滚菜单
  Tab           命令补全
  ↑             历史命令
  ?             查看所有快捷键

💬 常用命令：
  /clear        清空上下文
  /compact      压缩上下文
  /help         查看帮助
  /plugin       插件市场
  /rewind       回滚
  /rename       重命名会话

🚀 启动模式：
  claude                  交互模式
  claude -c               继续上次会话
  claude -r               选择历史会话
  claude -p "prompt"      非交互模式
  claude --dangerously-skip-permissions  自主模式

═══════════════════════════════════════════════════
```


### B. 相关资源链接


| 资源 | 说明 |
| --- | --- |
| Claude Code 官方文档 | 最权威的完整参考 |
| 快速入门 | 官方 Quickstart 教程 |
| 最佳实践 | 官方推荐的使用方式 |
| CLAUDE.md 指南 | 如何写好 CLAUDE.md |
| Skills 文档 | Skills 创建与配置 |
| Hooks 参考 | Hooks 事件钩子详解 |
| MCP 文档 | MCP Server 配置与使用 |
| Subagent 文档 | 子 Agent 创建与使用 |
| Agent Teams 文档 | 多 Agent 协作（实验性） |
| CLI 命令参考 | 所有命令行参数 |
| 扩展功能总览 | Skills/Hooks/MCP/Plugins 选型指南 |
| 社区与工具： |  |
| 资源 | 说明 |
| ------ | ------ |
| Claude Code GitHub | 开源仓库、Issue 反馈 |
| Anthropic Discord | 官方社区交流 |
| Superpowers 插件 | 最流行的开发工作流插件（42k+ stars） |
| Awesome Claude Skills | 社区精选 Skills 合集 |
| Claude Code Plugins Hub | 第三方插件索引站 |
| Claude Code 中文指南 | 中文社区教程 |
| Node.js 下载 | npm 安装 Claude Code 的前提 |
| Claude 订阅计划 | 查看 Pro/Max/Teams 价格 |
| 推荐阅读： |  |
| 资源 | 说明 |
| ------ | ------ |
| Writing a Good CLAUDE.md | 社区总结的 CLAUDE.md 写作技巧 |
| SFEIR Claude Code 教程 | 结构化的入门到进阶教程 |
| Anthropic 官方博客 | Anthropic 工程团队博客 |


# 📝 最后的话：

"现在是 2026 年，这是模型最差的时候。它往后只会越来越厉害。"

AI 开发的关键不在于你会不会写代码，而在于你会不会定义规范、管理上下文、编排 Agent 协作。掌握了这些能力，你就从"写代码的人"变成了"指挥 AI 写代码的人"。

路径依赖先别依赖人，先依赖模型。遇到问题优先问 Claude Code，实在解决不了再问人。

祝你在 AI 开发之路上越走越远！

