---
title: Claude Code实战分享 - 从会用到高效
date: 2026-03-31 18:30:00
tags:
  - Claude Code
  - AI开发
  - 实战经验
categories:
  - claude
copyright:
---

> Claude Code 实战分享：从"会用"到"高效"，涵盖 CLAUDE.md 配置、开发工作流、Bug 调试、代码审查、Agent Team 多智能体协作等 7 大实战场景。

<!-- more -->

Claude Code 从"会用"到"高效"

目录

[为什么值得深入使用 Claude Code](#1-为什么值得深入使用-claude-code)

[我的工作台全景](#2-我的工作台全景)（含 Serena 插件详解、Git Worktree、Vibe Kanban）

[场景 1：CLAUDE.md — 给 AI 一份项目说明书](#3-场景-1claudemd--给-ai-一份项目说明书)

[场景 2：完整开发工作流 — 从想法到落地](#4-场景-2完整开发工作流--从想法到落地)

[场景 3：Bug 调试 — 系统化根因分析](#5-场景-3bug-调试--系统化根因分析)

[场景 4：代码审查 — AI 辅助 Code Review](#6-场景-4代码审查--ai-辅助-code-review)

[场景 5：跨项目管理 — 批量检查代码变更](#7-场景-5跨项目管理--批量检查代码变更)

[场景 6：Agent Team — 多智能体并行协作](#8-场景-6agent-team--多智能体并行协作)

[场景 7：多 Session 多模型协作](#9-场景-7多-session-多模型协作)

[安全风险](#10-使用前需要建立的意识)

[成本控制](#11-Token 消耗比你想象的快)

[我踩过的坑与最佳实践](#12-我踩过的坑与最佳实践)

[彩蛋：这篇文章是怎么诞生的](#彩蛋这篇文章是怎么诞生的)


1. 为什么值得深入使用 Claude Code

我和 Claude Code 的故事

我第一次接触 Claude Code 是在 2025 年 7-8 月。当时刚出不久，试用了一段时间后就被它的能力震撼了——不是那种"AI 能帮你补全代码"的小惊喜，而是"它真的在理解我的项目，像一个靠谱的同事在帮我干活"的感觉。

核心认知转变

大多数人把 Claude Code 当"AI 问答工具"——问一句答一句。但它真正的定位是一个可深度定制的开发工作台。


```
Plain Text
初级用法：问答式
  你："这段代码什么意思？"
  AI："这段代码的作用是..."

中级用法：任务式
  你："帮我实现 XX 功能"
  AI：读代码 → 分析 → 写代码 → 测试

高级用法：工作台式（本次分享重点）
  - CLAUDE.md 让 AI 永远了解你的项目
  - 自定义 Agent 让 AI 扮演不同角色（审查员/调试员/规划师）
  - 自定义 Skill 让重复操作一键完成
  - MCP Server 让 AI 直连数据库/外部服务
  - 插件生态让 AI 拥有更多超能力
  - Agent Team 让多个 AI 并行协作
  - 多 Session 让不同模型各司其职
```


2. 我的工作台全景

2.1 目录结构总览


```
Plain Text
~/.claude/
├── settings.json          # 全局配置（插件开关、环境变量等）
├── agents/                # 自定义 Agent（5 个）
│   ├── code-reviewer.md   # 代码审查专家
│   ├── bug-analyzer.md    # Bug 根因分析专家
│   ├── dev-planner.md     # 开发规划师
│   ├── story-generator.md # 用户故事生成器
│   ├── claude-md-sync.md  # Claude.MD自动同步
│   └── ui-sketcher.md     # UI 草图设计师
├── skills/                # 自定义 Skill（3 个）
│   ├── check-recent-code-changes/  # 跨项目变更检查
│   ├── git-merge-workflow/         # Git 合并工作流
│   └── merge-sql-files/           # SQL 文件合并
├── plugins/               # 插件生态（10 个）
├── projects/              # 项目级配置（10+ 项目）
│   └── {project-hash}/
│       ├── CLAUDE.md      # 项目级说明
│       └── memory/        # AI 记忆文件
└── teams/                 # Agent Team 配置
```


首先，可以放弃传统的IDEA、VS Code，Cursor等代码IDE了，视角从写代码、改代码转向功能设计，功能实现，功能验证。除非必要，后面会极少关心代码细节。

我的工作台：3个Claude-code Session，分别进行功能设计，功能实现，功能Review，并且可以互相review对方的输出给出结论。


2.2 我的插件清单


点击图片可查看完整电子表格

2.3 重点插件：Serena — 大型项目的 Token 救星

在大型项目中（比如我们的 Java 微服务有 53 种任务类型、数百个类），AI 最大的 token 消耗来自读代码。没有 Serena 的时候，AI 要理解一个类的用法，需要：


```
Plain Text
没有 Serena（暴力读文件）：
  1. Read AbstractTaskHandler.java（400 行）→ 全量注入上下文
  2. Grep "extends AbstractTaskHandler" → 获得 30+ 匹配结果
  3. Read EngCompositionTaskHandler.java（200 行）→ 又是全量
  4. Read 其他相关文件...
  总计：轻松消耗 3000-5000 token，且大部分是"噪音"

有 Serena（符号级精确查询）：
  1. find_symbol("AbstractTaskHandler", type="class") → 返回精确位置
  2. get_symbols_overview("AbstractTaskHandler.java") → 只返回方法签名列表（非全文）
  3. find_referencing_symbols(...) → 只返回所有子类的名称列表
  4. 只读需要的那一个方法体
  总计：消耗 300-500 token，全是"信号"
```


Serena 的核心能力：


| 能力 | 说明 | 等价于 IDE 的 |
| --- | --- | --- |
| find_symbol | 按名称/类型搜索符号 | Ctrl+Shift+F（但更精确） |
| find_referencing_symbols | 找到谁引用了某个符号 | Find Usages |
| get_symbols_overview | 获取文件的符号概览（不读全文） | Structure 面板 |
| replace_symbol_body | 精确替换某个方法/类的定义 | 重构 → 替换 |
| rename_symbol | 跨文件重命名符号 | Shift+F6 全局重命名 |


实质：Serena 是通过 Language Server Protocol（LSP）给 AI 提供了和 IDE 一样的代码理解能力。AI 不再需要"读整个文件然后自己理解结构"，而是直接"查符号表"。

配置方式：安装后在项目根目录创建 `   `：


```javascript
# .serena/project.yml
languages:
- java          # 告诉 Serena 用 Java LSP 分析本项目
encoding: "utf-8"
ignore_all_files_in_gitignore: true
project_name: "job-tifenbao-gen-pdf"
```


首次使用时 Serena 会构建符号缓存（.serena/cache/），后续查询都走缓存，速度很快。

我的体感：在这个 Java 项目上，装了 Serena 后 AI 的"探索代码"阶段明显变快，上下文消耗也更少。对于大型项目（尤其是 Java 这种强类型语言），Serena 的收益非常显著。

注：配置好的serena经常会自动打开浏览器：http://127.0.0.1:24283/dashboard/index.html，可以通过配置~/.serena/serena_config.yml  web_dashboard_open_on_launch: false 来关闭这个烦人的东西


2.4 Git Worktree — 多人/多 Agent 并行的安全网

当你需要让多个 Claude Code Session 或 Agent Team 并行修改代码时，最大的风险是文件冲突——两个 Agent 同时改同一个文件，结果互相覆盖。

Git Worktree 解决这个问题：


```
Plain Text
普通模式（危险）：
  所有 Session 共享同一份文件
  → Agent A 改了 TaskHandler.java
  → Agent B 也在改 TaskHandler.java
  → 💥 冲突或覆盖

Worktree 模式（安全）：
  每个 Session 在独立的目录副本中工作
  → Agent A 在 .claude/worktrees/feature-a/ 里改
  → Agent B 在 .claude/worktrees/feature-b/ 里改
  → 各改各的，互不干扰
  → 完成后 merge 或 cherry-pick
```


使用方式：


```bash
# 方式一：在 Claude Code 中直接说
"请在 worktree 中工作"  # AI 自动调用 EnterWorktree

# 方式二：Agent Team 中指定隔离
# AI 启动 Teammate 时设置 isolation: "worktree"

# 方式三：手动创建
git worktree add .claude/worktrees/my-feature -b my-feature
cd .claude/worktrees/my-feature && claude
```


核心价值：搞砸了直接 `git worktree remove`，零风险。不影响你的主工作目录。

2.5    — AI 编码代理的可视化指挥中心

当你同时跑 2-3 个 Claude Code Session 或 Agent Team 时，终端窗口之间来回切换很痛苦——哪个任务在跑、哪个卡住了、哪个该审查了，全凭记忆。Vibe Kanban 就是解决这个问题的工具：一个给 AI 编码代理用的看板式任务管理平台。

一句话定义：Vibe Kanban 不写代码，它是 AI 编码代理的"调度中心"——用可视化看板管理多个 Agent 的任务状态、代码审查和工作流编排。


```
Plain Text
你（人类工程师）
    │
    ▼
┌──────────────────────────────────────────┐
│  Vibe Kanban（浏览器看板界面）              │
│                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ 待处理    │ │ 进行中    │ │ 已完成    │ │
│  │          │ │          │ │          │ │
│  │ Issue #3 │ │ Issue #1 │ │ Issue #2 │ │
│  │ 重构API  │ │ 加登录页  │ │ 修复BUG  │ │
│  │          │ │ Agent:   │ │ ✅ 已审查 │ │
│  │          │ │ Claude   │ │          │ │
│  └──────────┘ └──────────┘ └──────────┘ │
│                    │                     │
│     ┌──────────────┼──────────────┐      │
│     ▼              ▼              ▼      │
│  Claude Code   Gemini CLI     Codex     │
│  (worktree A)  (worktree B)  (worktree C)│
└──────────────────────────────────────────┘
```


核心能力：


```
Plain Text
能力                        说明
──────────────────────      ──────────────────────────────────────────────────────────
多代理统一管理              Claude Code、Gemini CLI、Codex、Cursor 等一个界面切换
可视化看板                  Issue 卡片在 待处理/进行中/已完成 之间流转，状态一目了然
自动 Worktree 隔离          每个 Workspace 自动创建 Git Worktree，Agent 之间互不干扰
并行 + 串行编排             多个 Agent 可以并行处理不同 Issue，也可以设置依赖顺序执行
内置代码审查                Diff 视图直接在浏览器中审查 Agent 的代码变更
一键启动 Dev Server          审查完直接在浏览器预览效果，不用手动起服务
集中式 MCP 配置             统一管理所有 Agent 的模型参数和工具配置
```


Vibe Kanban vs Claude Code 原生 Agent Team 的区别：


```
Plain Text
维度              Vibe Kanban                    Claude Code Agent Team
──────────        ────────────────────────       ──────────────────────────────
界面              浏览器可视化看板                终端文字交互
多代理支持        Claude/Gemini/Codex/Cursor 等  仅 Claude Code 内部 Agent
任务管理          Issue + 看板 + 子任务           TaskList + TaskUpdate
代码审查          内置 Diff 视图 + 浏览器预览     依赖 git diff 或自定义 Agent
适合场景          多个独立 Issue 并行推进          单个复杂任务的内部分工
安装成本          需额外安装，有浏览器 UI          Claude Code 原生，零安装
```


我的建议：如果你主要用 Claude Code 做开发，Agent Team 够用了。但如果你同时使用多种 AI 编码工具（比如白天用 Claude Code 做架构，晚上用 Gemini CLI 跑批量任务），或者你更喜欢可视化界面管理任务状态，Vibe Kanban 值得一试。GitHub 上 21k+ Star，社区很活跃。


3. 场景 1：CLAUDE.md — 给 AI 一份项目说明书

痛点：每次开新会话，Claude Code 不知道你的项目是什么、用了什么技术栈、代码组织方式、构建命令、测试方法。你得反复解释同样的上下文。更痛的是——即使解释了，AI 给出的代码可能用错 Java 版本、用错构建工具、用错设计模式，因为它不知道你的项目"偏好"。

解法：在项目根目录执行 `/init`，Claude 会自动读取项目，为你创建 `CLAUDE.md`，描述项目的主要功能、技术栈等信息。Claude Code 每次启动都会自动加载这个文件。但是注意的是，自带的 /init 是一个一次性的起步工具，后续不会自动更新：

扫描项目文件，检测技术栈、构建系统、测试框架

生成一个基础 CLAUDE.md 作为起点

单次运行，后续需要手动维护

CLAUDE.md 的本质：不只是项目说明书

很多人以为 CLAUDE.md 就是写一段项目介绍。但实际上，它是你和 AI 之间的契约——不只告诉 AI "项目是什么"，更关键的是告诉它"怎么做"和"不要做什么"。


```
Plain Text
CLAUDE.md 的三层价值：

第一层：项目上下文（减少解释成本）
  → AI 知道项目是什么、用了什么技术栈

第二层：行为约束（减少返工成本）
  → AI 知道"不要用 Java 11+ API""Spring 用 XML 不要建议改注解"

第三层：领域知识（减少理解成本）
  → AI 知道"PhaseCode 6009 表示错题本阶段""TemplateHandler.genTemplateData()
    以上是业务逻辑，以下是渲染逻辑"
```


我的 CLAUDE.md 实践

我为 10+

成，然后在实际使用中持续补充——每次 AI 犯的错就是一个应该写进 CLAUDE.md 的提醒。为了让claude.md可以持续自动更新，可以实现了一个agent：通过hook实现进入一个session后，让claude自动检查最近的git提交记录，然后根据功能变化同步到claude.md中（此功能可以直接描述，让claude帮你实现）。


```
yaml
---
name: claude-md-synchronizer
description: 后台维护代理，根据项目变更自动维护和更新 CLAUDE.md 文件。在会话开始和重要里程碑（功能完成、重构、新增依赖、架构变更）时触发。独立运行，不中断其他代理。
permissions:
  allow:
    - Bash
    - Read
    - Write
    - Edit
    - Grep
    - Glob
    - Skill
model: haiku
color: purple
field: documentation
expertise: intermediate
fork_safe: true
hooks:
  - event: SessionStart
    commands:
      - echo "Synchronizer: 正在检查 CLAUDE.md 是否需要更新..."
    once: false
  - event: PreToolUse
    matcher: Write
    commands:
      - echo "Synchronizer: 正在验证 CLAUDE.md 变更..."
  - event: PostToolUse
    matcher: Write
    commands:
      - echo "Synchronizer: CLAUDE.md 更新完成"
---

# CLAUDE.md 同步代理

我是 CLAUDE.md 同步者 - 一个后台维护代理，负责让项目的 CLAUDE.md 文件与实际代码变更保持同步。

## 触发时机

**自动触发**（SessionStart 钩子）：
- 每次 Claude Code 会话开始时
- 检查上次更新以来的 git 变更
- 无重大变更时静默退出

**手动触发**（里程碑节点）：
- 功能开发完成
- 重大重构
- 新增依赖
- 架构变更

后面省略一万字~~~
```


核心结构（不是模板——每个项目应该不同）：


```
Plain Text
CLAUDE.md

项目概述
  一句话说明这是什么项目，做什么用的。
  （关键：写清楚项目的业务上下文，不只是技术描述）

技术栈
  - 语言/框架版本（Java 8，不是 Java 11+）
  - 构建工具（Maven，profile 有 development/test/product）
  - 关键依赖及版本约束

构建命令
  mvn clean package -P development  // 不是 gradle，不是 spring boot

架构说明
  核心设计模式、数据流、服务间通信方式。
  （关键：写出"天然的分界线"，比如哪个方法以上是业务逻辑，以下是渲染逻辑）

重要提醒（"不要做什么"清单）
  - 本项目使用 Java 8，不要使用 Java 11+ 的 API
  - Spring 配置使用 XML，不要建议改成注解方式
  - 前端构建必须区分 Node 14（Vue2）和 Node 18（Vue3）
```


真实案例：不同项目的 CLAUDE.md 侧重点完全不同

Java 微服务项目（job-tifenbao-gen-pdf）—— 侧重架构和配置映射：

包含 53 种任务类型到 Handler 的完整映射关系

标注了 8 个 XML 配置文件各自覆盖哪些任务类型

说明了 Template Method / Factory / Strategy 三种设计模式的使用位置

解释了 Nacos 配置中心和 Dubbo 服务的集成方式

列出了文档生成库的版本清单（iText 4.2.1, Playwright 1.10.0, PDFBox 2.0.23）

这份 CLAUDE.md 之所以写这么详细，是因为这个项目有 53 种任务类型分散在 9 个 XML 配置文件中——不写清楚，AI 每次都要花 5-10 分钟重新探索。

Vue 2 前端项目（web-tifenbao-campus-report）—— 侧重业务域知识：

包含 PhaseCode 业务域知识（6001=考试报告、6009=错题本、各阶段的数据流）

标注了 Template Studio 的 Monaco 编辑器集成和 iframe 预览机制

说明了 Element UI 的定制方式和主题变量

列出了各子路由和功能模块的对应关系

这份 CLAUDE.md 的重点是业务术语——因为前端代码本身不复杂，但不理解 PhaseCode 的含义就写不出正确的业务逻辑。

效果：AI 理解项目上下文的时间从"每次 5-10 分钟解释"→"0 秒"；不再出现"让我先了解一下你的项目结构"这种空转；AI 给出的代码直接符合项目规范（用对 Java 版本、用对设计模式、用对构建命令）。持续进化：每次 AI 犯错，补一条提醒到 CLAUDE.md，下次就不会再犯。

进阶技巧：Memory 目录 — AI 的长期记忆

CLAUDE.md 解决的是"项目级上下文"，但还有一类信息是"会话级经验"——比如"上次调试发现 fontfaceonload.js 必须从 gen-pdf 项目复制过来"。这类信息适合放在 Memory 目录：


```
Plain Text
~/.claude/projects/{project-hash}/memory/
├── MEMORY.md        # 每次会话自动加载（保持 200 行内）
├── debugging.md     # 调试经验沉淀
└── patterns.md      # 项目特有的代码模式
```


CLAUDE.md 是手动维护的"宪法"，Memory 是 AI 自动积累的"经验库"。两者配合使用效果最好。你也可以主动让claude将你的习惯保存到memory中。

** 可以把CLAUDE.md 理解为与项目代码有关的规则，MEMORY.MD是和项目代码无关的规则，是保存你自己使用claude时想让claude记住的习惯与经验。**

比如每次让claude review时，他都是直接输出到终端，就可以让他输出到指定目录下，后面再review时，他就会直接写到md文档中。


```

```


📝 真实对话案例：用 /init 自动生成 CLAUDE.md（点击展开）


```
以下是首次使用 /init 命令让 AI 自动分析项目并生成 CLAUDE.md 的真实记录。
```


```
Plain Text
👤 用户:
/init 更新CLAUDE.md

🤖 AI (glm-4.7):
[自动注入系统指令：分析代码库，创建/更新 CLAUDE.md]
[开始深度探索项目...]

工具调用序列：
  1. Read pom.xml → 获取依赖、构建配置、环境 profile
  2. Glob **/applicationContext_job.xml → 发现 8 个任务配置文件
  3. Read AbstractTaskHandler.java → 理解 Template Method 模式
  4. Read task-services-mapping.md → 获取 53 种任务类型映射
  5. Read AbstractTest.java → 获取测试基类和 Spring 上下文配置
  6. Glob **/dubbo*.xml → 发现 Dubbo 消费者配置

分析完成，更新 CLAUDE.md：

新增内容：
  1. Package Structure — 6 个核心包的职责说明
  2. Task System Architecture — 8 个 XML 配置文件覆盖 53 种任务类型
  3. Document Generation Libraries — 完整依赖版本清单
     (iText 4.2.1, Playwright 1.10.0, PDFBox 2.0.23...)
  4. Running Tests — AbstractTest.getTask() 辅助方法
  5. Dubbo Service Integration — 消费者配置位置
  6. Configuration Sources — Nacos + env properties + Spring XML 三层配置
  7. Common Issues — 模板构建和任务处理器选择的已知坑

[自动 commit: "docs: update CLAUDE.md with comprehensive project documentation"]
```


亮点：AI 通过 6 次工具调用，自动从 `pom.xml`、Java 源码、XML 配置、测试类中提取关键信息，生成了一份覆盖构建、测试、架构、配置、已知问题的完整项目说明。后续每次开新会话，AI 都自动加载这份文档。但这只是起点——后续在使用过程中又陆续补充了"不要做什么"清单和业务术语表。


4. 场景 2：完整开发工作流 — 从想法到落地

痛点：传统开发流程：想法 → 口头讨论 → 直接写代码 → 发现遗漏 → 返工。缺少系统化的设计和规划环节，或者有但全靠人工写文档。

解法：通过 superpowers 插件提供的三个 Skill，形成完整的想法 → 设计 → 计划 → 执行闭环，每个阶段自动产出文档。


```
Plain Text
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  阶段一：Brainstorm │──→│  阶段二：Write Plan │──→│  阶段三：Execute   │
│  /brainstorm      │    │  /write-plan      │    │  /execute-plan    │
│                    │    │                    │    │                    │
│  输入：一个想法     │    │  输入：设计文档     │    │  输入：实施计划     │
│  产出：设计文档     │    │  产出：实施计划     │    │  产出：代码+报告    │
│                    │    │                    │    │                    │
│  docs/desgins/       │    │  docs/plans/       │    │  docs/review/      │
│  *-design.md      │    │  *-plan.md         │    │  *-review.md       │
│                    │    │                    │    │  docs/reports/     │
│                    │    │                    │    │  *-report.md       │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```


阶段一：Brainstorming — 把模糊想法变成设计方案

触发方式：


```
Plain Text
/superpowers:brainstorm 我想做一个效果图自动生成模板的功能
```


AI 会做什么：

先探索项目上下文（读 CLAUDE.md、相关代码、历史文档）

2. 一次问一个问题（不会一次抛出 10 个问题让你头大）

提出 2-3 个方案并附带 trade-off 分析和推荐

分段呈现设计方案，每段确认后再继续

最终输出 docs/plans/YYYY-MM-DD-xxx-design.md 并 git commit

真实案例（本次对话的实际过程）：


```
Plain Text
我：/brainstorm 业务方能否直接上传效果图，自动生成模板？

AI 的提问过程：
  Q1: 效果图是什么形式？→ 我答：任意图片
  Q2: AI 生成的结果是什么？→ 我答：混合模式（preset 组件 + 自定义）
  Q3: 使用者是谁？→ 我答：产品经理 + 开发者都要支持
  Q4: AI 能力用什么实现？→ 我答：外部大模型 API
  Q5: 输出格式？→ 我答：先 PDF，后扩展 Word

AI 提出 3 个方案：
  A: AI 生成 Vue SFC 代码（推荐）
  B: AI 生成 JSON DSL + 可视化编排
  C: 多轮对话式迭代

我选了 A，AI 分 5 段展示设计：
  1. 整体架构图
  2. AI 生成核心流程（Component Catalog + 两阶段 Prompt）
  3. 前端交互设计（用户操作流程图）
  4. API 设计（SSE 流式接口）
  5. 边界条件与扩展路径

最终产出：docs/plans/2026-03-03-image-to-template-ai-generation-design.md
```


关键价值：

强制你在写代码前想清楚设计

AI 帮你考虑了你可能忽略的 trade-off

自动产出可分享的设计文档，不用自己写


📝 真实对话案例：渲染平台架构设计 Brainstorming（点击展开）


```
以下是 2026-02-28 一次真实的 brainstorming 对话记录，目标是重构 PDF 渲染项目的架构。
```


```
Plain Text
👤 用户:
我现在想重构这个项目，这个组件给很多业务提供了渲染能力，但是每次都需要对方业务
的人来这个组件来开发，写数据和渲染模板。现在想从架构层面重新设计下，打造一个公共
的渲染平台，提供PDF渲染能力，但是如何剥离业务，或者说如何让业务逻辑和渲染逻辑
分离，这是个挑战。请帮我深入思考，给出方案设计。

🤖 AI:
[启用 brainstorming 技能，创建任务列表追踪设计过程]
[深度探索代码库：53个任务类型、8个XML配置、100+ BaseTemplate类...]

分析完成。核心发现：

**问题本质**
当前53种任务类型全部耦合在一个项目里。每个 TaskHandler.genTaskHandlerConfigs()
同时做了三件事：数据获取、业务规则判断、模板实例化。TemplateHandler 和 100+ 个
BaseTemplate 类让业务方必须深入理解渲染内部实现。

**解耦切面**
关键发现：TemplateHandler.genTemplateData() 是天然的分界线。
这个方法以上是业务逻辑，以下是纯渲染逻辑。重构就是沿着这条线切开。

**推荐方案 C：混合渐进式架构**

三步走：
- Phase 1（2~3周）：抽取 RenderEngine 接口，渲染逻辑从 TaskHandler 独立，不改外部行为
- Phase 2（3~4周）：构建统一 RenderService Dubbo API + 模板注册中心
  新业务直接调 render(templateId, data, format)
- Phase 3（持续）：存量53种任务按 preview → writebook → eng → conf → layer 逐步迁移

最大的变化：
  Before: 业务方 → 在渲染项目写 Java + Vue → 发版部署
  After:  业务方 → 自己服务里组装 JSON → 调渲染 API → 拿 PDF URL

👤 用户:
模板可以使用数据库，任务队列复用轮询，可以提供 REST API 给非 Java 业务方，
模板统一 Vue2，存量可以抽成公共 SDK，暂时放在当前组件。

🤖 AI:
好的，我把你的决策整合进设计文档...
[更新设计文档，纳入用户的技术选型偏好]

👤 用户:
/superpowers:brainstorm 是否可以提供一个在线编辑模板功能（类似低代码平台，
提供默认的组件模块）让业务可以快速创建模板，也可以让业务自定义模板
（用户输入 Vue 代码，可以在线预览）。请帮我思考这个是否可以嵌入刚才的文档。

🤖 AI:
[开始第二轮 brainstorming，探索 Template Studio 在线编辑模板的可行性]
[分析现有 60+ preset 组件、Monaco 编辑器集成、iframe 预览机制...]
[最终产出：docs/plans/2026-02-28-rendering-platform-design.md，1,324 行]
```


这次 brainstorming 的成果：从一个"想重构"的模糊想法，经过深度代码分析，产出了一份 1,324 行的完整架构设计文档，覆盖了 Phase 1-4 的详细设计和迁移路径。

📝 真实对话案例：拖拽组件插入功能设计（点击展开）


```
以下是 2026-03-03 一次 brainstorming 中 AI 系统化分析需求的对话片段。
```


```
Plain Text
👤 用户:
[讨论 Template Studio 组件拖拽插入功能]

🤖 AI:
先回答你的问题：**可以支持**，但需要明确"拖动到哪"——因为右侧是两个区域：
Monaco 代码编辑器 + 预览 iframe。

你期望拖动组件时，插入的目标是哪里？

  A. 代码编辑器（Monaco）— 拖到编辑器区域，在光标位置插入组件代码片段
  B. 可视化预览区（右侧 iframe）— 拖到预览中，可视化放置
  C. 两者都支持

> 目前系统已有"点击组件→弹出详情→点击插入代码"的流程。
> 预览区拖放实现复杂度高很多——iframe 沙箱隔离，需要跨 frame 通信协议
> + 解析 HTML 反写，工程量约是 A 的 5-10 倍。

👤 用户: A

🤖 AI:
方案 A：HTML5 原生 Drag & Drop ⭐ 推荐
  - component-item 加 draggable="true" + dragstart 事件传递代码片段
  - Monaco 外层 div 监听 dragover / drop
  - editor.getTargetAtClientPoint() 计算插入行列
  - 无额外依赖，实现简单，兼容性好

方案 B：第三方拖拽库（Vue Draggable / Sortable.js）
  - ❌ Monaco 不是普通 DOM 列表，库对它的支持有限

架构改动涉及 3 个文件：
  1. ComponentPanel.vue — 加 draggable 属性
  2. MonacoEditor.vue — 加 insertAtLine 方法，处理 dragover/drop
  3. 样式调整 — 插入线的实时计算与显示

[随后 AI 直接实现，产出详细的代码改动说明]
```


亮点：AI 在推荐方案时不只是说"推荐 A"，而是给出了工程量的量化对比（5-10 倍差距），帮助你快速做出决策。

阶段二：Write Plan — 把设计方案拆成实施步骤

触发方式：


```
Plain Text
/superpowers:writing-plans
```


AI 会做什么：

阅读设计文档

拆分成有依赖关系的实施步骤

识别关键文件和需要修改的代码位置

标注每步的验证标准

输出 docs/plans/YYYY-MM-DD-xxx-plan.md

产出示例：


```
Plain Text
实施计划

Step 1: 创建 ComponentCatalog 数据结构
  - 文件：src/types/component-catalog.ts
  - 内容：定义 Component 接口 + 序列化方法
  - 验证：单元测试通过

Step 2: 编写组件信息提取脚本
  - 文件：scripts/extract-component-catalog.js
  - 依赖：Step 1
  - 验证：能从 templatemanager/components/ 提取 60+ 组件信息

Step 3: 实现 LLM Gateway
  - 文件：src/services/llm-gateway.ts
  - 依赖：Step 1
  - 验证：能调用 Vision API 并返回结构化结果
  ...
```


阶段三：Execute Plan — 按计划执行并产出报告

触发方式：


```
Plain Text
/superpowers:executing-plans
```


AI 会做什么：

读取实施计划

按步骤执行，每步完成后 checkpoint

遇到问题时暂停，等你确认

过程中产出审查文档 docs/review/ 和实施报告 docs/reports/ （使用MEMORY.MD)

文档产出矩阵：


| 阶段 | 文档路径 | 内容 |
| --- | --- | --- |
| Brainstorm | docs/plans/YYYY-MM-DD-xxx-design.md | 设计方案、架构图、方案对比 |
| Write Plan | docs/plans/YYYY-MM-DD-xxx-plan.md | 实施步骤、依赖关系、验证标准 |
| Execute | docs/review/YYYY-MM-DD-xxx-review.md | 实施过程审查、代码质量检查 |
| Execute | docs/reports/YYYY-MM-DD-xxx-report.md | 实施结果报告、测试覆盖、遗留问题 |


效果：每个功能开发都有完整的文档链：设计 → 计划 → 审查 → 报告。文档是 AI 在过程中自动产出的，不是事后补的。新同事接手时可以从 `docs/` 目录完整了解每个功能的来龙去脉。


5. 场景 3：Bug 调试 — 系统化根因分析

痛点：调 bug 最怕"凭感觉猜"——改了一个地方不对，再猜另一个，循环往复。

解法：用 bug-analyzer 自定义 Agent + systematic-debugging Skill，让 AI 做系统化分析而不是瞎猜。

工作流


```
Plain Text
触发：/superpowers:systematic-debugging

第一步：收集信息
  - 错误现象、堆栈、输入数据
  - AI 自动读取相关代码文件

第二步：构建执行链
  - AI 画出完整的调用链路
  - 标记每个节点的状态变化

第三步：定位根因
  - 反向推理：从错误现象往源头追
  - 状态差异分析：期望 vs 实际

第四步：提出修复方案
  - 具体到文件名和行号
  - 附带测试建议
```


我的 bug-analyzer Agent 配置


```
Plain Text
文件位置: ~/.claude/agents/bug-analyzer.md

Model: Claude Opus（用最强模型做深度分析）

角色：Expert debugger
核心能力：
  - 执行流构建和分析
  - 控制流图分析
  - 数据流全生命周期追踪
  - 调用链分析

输出格式：
  Bug 根因分析报告
    问题摘要（错误现象、触发条件、影响范围）
    执行流分析（关键执行路径、状态变化序列）
    根因定位（根因描述、错误位置 File:Line、推理过程、证据代码）
    解决方案（推荐修复、修复后执行流验证、测试建议）
```


创建自定义 Agent 的方法


```
Plain Text
在 ~/.claude/agents/ 目录下创建 .md 文件即可，文件名就是 Agent 名称。

文件内容格式：
  ---
  model: opus          // 可选 opus/sonnet/haiku
  description: 我的自定义 Agent 描述
  color: blue          // 终端显示颜色
  tools:               // 可用工具列表
    - read_file
    - search_files
    - run_bash_command
  ---

  (下面写 Agent 的系统提示)

  你的角色是...
  你的工作流程是...
  你的输出格式是...
```


效果：从"猜 3-4 次才找到根因"→"一次分析到位"。修复方案精确到具体文件行号，附带回归测试建议。

📝 真实对话案例：OSS 上传失败 — XML Parser 依赖冲突排查


```
以下是一次真实的 systematic-debugging 对话。用户贴了一个 OSS 上传报错的堆栈，AI 系统化追踪到了根因。
```


```
Plain Text
👤 用户:
[贴出完整堆栈]
com.aliyun.oss.OSSException: Failed to parse the response result.
[ErrorCode]: InvalidResponse
http://xml.org/sax/features/external-general-entities feature not recognized
for SAX driver org.gjt.xpp.sax2.Driver

🤖 AI:
[启用 systematic-debugging 技能]

第一步：收集事实
  - 错误发生在 Aliyun OSS SDK 解析 XML 响应时
  - 报错的 SAX driver 是 org.gjt.xpp.sax2.Driver（XPP3 库）
  - 正常情况下应该用 JDK 内置的 SAX parser

第二步：构建调用链
  OSSClient.putObject()
    → ResponseParser.parse()
      → SAXParserFactory.newInstance()
        → 加载了 xpp3 的 SAX driver（而非 JDK 默认）
          → xpp3 不支持 external-general-entities feature
            → 抛出异常

第三步：根因定位
  项目依赖 jdom2 → jdom2 传递依赖了 xpp3（XML Pull Parser 3）
  xpp3 是一个 2009 年后就没更新的库，它注册了自己的 SAXParserFactory
  导致 classpath 上的 SAX 实现被替换为不兼容的版本

  根因：依赖冲突。jdom2 引入的 xpp3 覆盖了 JDK 的 SAX parser。

第四步：修复方案
  在 pom.xml 中排除 xpp3 和 xmlpull 的传递依赖：

  <dependency>
      <groupId>com.iflytek.edu</groupId>
      <artifactId>ZX-filecloud-service-api</artifactId>
      <exclusions>
          <exclusion>
              <groupId>xmlpull</groupId>
              <artifactId>xmlpull</artifactId>
          </exclusion>
          <exclusion>
              <groupId>xpp3</groupId>
              <artifactId>xpp3</artifactId>
          </exclusion>
      </exclusions>
  </dependency>

  验证方式：mvn dependency:tree | grep xpp3 确认已排除
```


亮点：AI 没有猜测"可能是网络问题"或"可能是配置错误"，而是从堆栈的 SAX driver 类名入手，反向追踪依赖链，精确定位到 jdom2 → xpp3 这条传递依赖路径。整个分析过程有清晰的推理链条。


6. 场景 4：代码审查 — AI 辅助 Code Review

痛点：人工 Review 容易遗漏安全漏洞、性能问题、边界条件。

解法：用 code-reviewer 自定义 Agent 做提交前的 AI 审查。

我的 code-reviewer 配置


```
Plain Text
文件位置: ~/.claude/agents/code-reviewer.md

Model: Claude Opus

能力矩阵：
  - AI 代码分析（SonarQube、CodeQL 规则级别）
  - 安全审查（OWASP Top 10、输入校验、认证鉴权）
  - 性能分析（N+1 查询、内存泄漏、并发问题）
  - 配置审查（敏感信息暴露、权限配置）
  - 多语言支持（JS/TS、Python、Java、Go 等）

审查流程：
  1. 分析代码上下文和变更范围
  2. 自动化工具初步扫描
  3. 手动审查逻辑和架构
  4. 评估安全影响
  5. 评估性能影响
  6. 按严重程度分级输出反馈
  7. 附带改进代码示例
```


使用方式：在 Claude Code 中直接让 AI 审查（它会自动读取 git diff），或者用 `/superpowers:requesting-code-review` 触发。

效果：提交前多了一道 AI 安全网，能发现人工容易遗漏的 SQL 注入、XSS 等安全问题，审查报告可以作为 PR 描述的一部分。

📝 真实对话案例：英语词汇报告功能分支 Code Review（点击展开）


```
以下是一次真实的代码审查对话。用户让 AI 对比 feature 分支和 master，审查英语词汇报告页面的代码变更。
```


```
Plain Text
👤 用户:
当前分支是给英语词汇作文实现一个独立的报告页面，请查看当前分支的修改，
并与 master 进行比较后，进行代码 review，给出 review 结果。

🤖 AI:
[启用 code-reviewer，执行 git diff master...HEAD]

## Code Review 报告

### 变更概览
- 新增文件：3 个 Vue 组件 + 1 个 API 模块
- 修改文件：路由配置、Store 模块
- 总变更：+487 行 / -12 行

### 🔴 Critical（需要修复）

1. **API 响应未做空值防御** — `report-api.js:34`
   `response.data.wordList` 直接访问，如果接口返回 null 会导致页面白屏。
   建议：`const wordList = response?.data?.wordList || []`

2. **路由守卫缺失** — `router/index.js:89`
   新增页面没有加登录状态校验，未登录用户可以直接访问报告页。

### 🟡 Important（建议修复）

3. **组件命名不符合项目规范** — `EngWordReport.vue`
   项目其他页面都用 kebab-case 命名（如 `exam-analysis.vue`），
   建议重命名为 `eng-word-report.vue`。

4. **Store mutation 存在副作用** — `store/report.js:28`
   mutation 内部调用了 localStorage.setItem()，
   应该放到 action 中处理。

### 🟢 Minor（可选优化）

5. **CSS 硬编码颜色值** — `EngWordReport.vue:156`
   `color: #3366ff` 应使用项目主题变量 `$--color-primary`。

6. **console.log 未清理** — `report-api.js:22`

### 总结
整体实现逻辑清晰，组件拆分合理。主要问题是空值防御和路由守卫，
建议修复 Critical 级别后再合并。
```


亮点：AI 按严重程度分级（Critical → Important → Minor），每个问题都精确到文件名和行号，并给出具体的修复建议，而不只是指出问题。


7. 场景 5：跨项目管理 — 批量检查代码变更(自定义skill)

痛点：发版前要确认"过去 N 天改了哪些项目的哪些文件"，手动一个个项目去 `git log` 很低效。

解法：创建自定义 Skill：`check-recent-code-changes`。


```
Plain Text
文件位置: ~/.claude/skills/check-recent-code-changes/SKILL.md

用途：检查指定时间段内，指定作者在多个 Git 仓库中的代码变更。

参数：
  - author: 作者名（默认为你的用户名）
  - days: 天数（默认 20 天）
  - path: 扫描路径（默认当前工作区父目录）

执行逻辑：
  遍历所有子目录 → 检查是否 Git 仓库 → git log 过滤 → 汇总输出

输出格式：
  === 项目名称 ===
  commit hash | 日期 | 提交信息
  修改文件列表
```


使用方式：在 Claude Code 中输入 `/check-recent-code-changes` 即可。

创建自定义 Skill 的方法


```
Plain Text
在 ~/.claude/skills/ 下创建目录 + SKILL.md

目录结构：
  ~/.claude/skills/my-skill/SKILL.md

文件内容格式：
  ---
  name: my-skill
  description: 描述这个 Skill 做什么
  ---

  Skill 标题

  触发条件
    什么时候应该使用这个 Skill

  执行步骤
    1. 第一步做什么
    2. 第二步做什么

  注意事项
    需要注意的坑
```


📝 真实对话案例：跨项目上线前变更审计 + Skill 自动化


```
以下是 2026-02-25 一次真实的跨项目操作。用户在父级 Git 目录下，让 AI 扫描所有子项目的近期改动，用于上线前核查。
```


```
Plain Text
👤 用户:
当前目录是我在公司工作的所有项目，我现在想查下最近20天我改过哪些组件的代码，
明天准备上线，防止漏组件

🤖 AI:
[遍历所有子目录，检测 .git 仓库，执行 git log --since="20 days ago" --author="<your-name>"]

根据检查结果，以下是你最近20天修改过的组件（按项目分类）：

## 需要上线的组件列表

### 前端项目
1. html-paperfresh-pc — 星火英语词汇相关功能
2. web-tifenbao-campus-report — 英语作文报告工具（批量导入/创建题目）
3. tfb-wowbook-web — 星火单词PK功能

### 后端 API 项目
4. api-tifenbao-pqbp — 星火英语报告分数率计算逻辑

### 业务服务项目
5. service-tifenbao-pqbp — 星火英语词汇资源服务（翻译、语音合成）
...
14. job-tifenbao-gen-pdf — 英语单词导出资源补全
...

**总计：17 个组件**

👤 用户:
帮我把刚才这个功能实现成一个 skill，可以指定多少天内的

🤖 AI:
[创建 ~/.claude/skills/check-recent-code-changes/SKILL.md]

Skill 创建完成！以后直接用 /check-recent-code-changes 就能执行了。
支持参数：author（默认为你的用户名）、days（默认 20 天）、path（默认当前目录）。
```


另一个跨项目场景：可以通过/add-dir 把其他项目地址添加到当前session或者当前项目，这样就可以同时让claude操作多个项目工程，也可以让claude对整个工作流，数据流有更深的了解，此时就可以直接让claude-code设计全链路的架构设计、实现计划和代码修改，然后可以用agent-teams，让不同的agent去不同的项目里干活。此时假如在 `job-tifenbao-gen-pdf` 项目中工作时，用户突然收到 `web-tifenbao-campus-report` 的报错：


```
Plain Text
👤 用户:
web-tifenbao-campus-report 控制台报错：
fontfaceonload.js 404 (Not Found)
Cannot set properties of null (setting 'innerHTML')

🤖 AI:
[同时读取两个项目的文件进行交叉比对]

Read: /Users/admin/Company/Web/Git/web-tifenbao-campus-report/static/zx-html-templates/
Read: /Users/admin/Company/Web/Git/job-tifenbao-gen-pdf/src/main/resources/zx-html-templates/

## 根因分析
web-tifenbao-campus-report 的 static/zx-html-templates/ 缺少 fontfaceonload.js，
这个文件应该从 job-tifenbao-gen-pdf 构建产物中复制过来。

## 修复
cp job-tifenbao-gen-pdf/.../fontfaceonload.js → web-tifenbao-campus-report/static/...
```


亮点：AI 可以直接用绝对路径读取任何项目的文件，实现跨项目的根因分析。同时，用户把一次性操作沉淀为可复用的 Skill，后续一键执行。

Skill vs Agent 的区别


| 维度 | Skill | Agent |
| --- | --- | --- |
| 定义 | 一套工作流程指令 | 一个具有特定角色的 AI 人格 |
| 触发 | /skill-name 或 AI 自动匹配 | 被 AI 作为子任务分派 |
| 执行者 | 当前 AI 会话 | 新启动的独立 AI 进程 |
| 文件 | ~/.claude/skills/{name}/SKILL.md | ~/.claude/agents/{name}.md |
| 适合 | 固定流程、可重复操作 | 需要特定专业角色的深度分析 |


8. 场景 6：Agent Team — 多智能体并行协作

什么是 Agent Team

Agent Team 是 Claude Code 的多智能体协作能力。你可以创建一个"团队"，包含多个具有不同角色的 AI Agent，它们可以：

并行处理不同任务

通过消息互相通信

共享任务列表协调进度

在独立的 Git Worktree 中隔离工作


```
Plain Text
架构：
┌──────────────────────────────────────────┐
│  Team Lead（你的主 Claude Code 会话）      │
│  - 创建任务、分配任务、协调进度             │
├──────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ Agent A  │ │ Agent B  │ │ Agent C  │ │
│  │ 前端开发  │ │ 后端开发  │ │ 测试工程师│ │
│  │          │ │          │ │          │ │
│  │ worktree │ │ worktree │ │ 主分支    │ │
│  │ A        │ │ B        │ │          │ │
│  └──────────┘ └──────────┘ └──────────┘ │
│       ↕             ↕             ↕      │
│  ┌──────────────────────────────────┐    │
│  │  共享任务列表 (TaskList)          │    │
│  │  ~/.claude/tasks/{team-name}/    │    │
│  └──────────────────────────────────┘    │
└──────────────────────────────────────────┘
```


适合使用 Agent Team 的场景


```
场景
为什么适合
示例
```


| 多文件并行重构 | 各 Agent 改不同文件，互不冲突 | "前端改组件，后端改 API，测试写用例" |

| 多角度分析 | 不同 Agent 从不同视角分析同一问题 | "安全审查 + 性能审查 + 架构审查" |

| 研究 + 实现分离 | 一个 Agent 调研，另一个实现 | "Agent A 研究最佳实践，Agent B 写代码" |

| 代码审查流水线 | 一个写完另一个立即审查 | "开发 Agent 写完 → 审查 Agent 检查" |

不适合使用 Agent Team 的场景

| 简单的单文件修改 | 开销太大，不如直接做 |

| 强依赖顺序的任务 | Agent 之间等待反而更慢 |

| 需要频繁交互确认 | 通信成本高 |

创建和使用流程

步骤 1：启用 Agent Team 功能


```json
// ~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```


步骤 2：创建团队 — 在 Claude Code 对话中告诉 AI 你想用 agent-teams来完成任务，AI 会自动执行 TeamCreate → TaskCreate → Agent 启动 → TaskUpdate 分配 → SendMessage 协调。

步骤 3：监控进度 — AI 会自动收到 Teammate 的消息通知，可以通过 TaskList 查看整体进度，Teammate 完成后会自动汇报。

重要注意事项


```
Plain Text
1. 成本控制
   每个 Agent 都是独立的 API 会话，会消耗 token。尤其不要在plan模式用agent-teams，是普通模型的7倍消耗。
   broadcast（群发消息）的成本 = N × 单次成本，推荐用 message（点对点）代替。

2. Worktree 隔离
   推荐让写代码的 Agent 在独立 worktree 中工作，避免同时修改同一文件。
   Agent 完成后可以 merge 或 cherry-pick，搞砸了直接删除 worktree。
   设置方式：在 Agent 工具调用时指定 isolation: "worktree"

3. 团队规模建议
   推荐 2-4 个 Agent，不要超过 5 个。
   通信复杂度随人数指数增长，协调 overhead 会抵消并行收益。

4. Claude code会自动创建合适的agent队员（不同角色）来完成你给的任务。
   如果你对他创建的角色不满意，你可以明确指定让他为了创建合适的agent。
```


实战示例


```
Plain Text
目标：分析 templatemanager 组件库的复用性，输出多角度报告

Team 配置：
  - Agent A (Sonnet): 从前端开发者视角分析组件 API 设计
  - Agent B (Sonnet): 从 PDF 渲染需求视角分析组件完整性
  - Agent C (Sonnet): 从 Template Studio 集成视角分析组件可嵌入性

结果：三个 Agent 并行工作，各输出了独立分析报告，
主 Session 汇总成最终的多角度分析文档。
```


📝 真实对话案例：多 Agent 并行审查架构设计文档


```
以下是 2026-03-02 一次真实的 Agent Team 使用记录。用户要求从多个角度评审渲染平台的架构设计。
```


```
Plain Text
👤 用户:
可以使用 team-agents 从不同角度分析下
@docs/plans/2026-02-28-rendering-platform-design.md 这个架构设计文档，
尤其是 Phase4 的设计，是否可以达到渲染平台和业务解绑的目标。
我已经安装了 tmux，你可以在不同的窗口里展示 agent 的思考过程。

🤖 AI:
好的，我来创建一个分析团队，从 5 个维度并行审查这份架构设计。

[TeamCreate: "arch-review-team"]
[创建 5 个任务，分配给 5 个 Agent]

Agent 分工：
  🔹 Agent 1 — 系统架构视角：审查整体分层是否合理，API 边界是否清晰
  🔹 Agent 2 — 业务解耦视角：Phase 4 能否真正让业务方不再碰渲染代码
  🔹 Agent 3 — 代码实现视角：现有代码能否按设计平滑迁移
  🔹 Agent 4 — 性能与扩展性视角：新架构是否能承载更多业务方接入
  🔹 Agent 5 — 团队维护成本视角：长期维护负担是增还是减

[5 个 Agent 在独立 tmux 窗口中并行工作]
[Agent 1 正在分析 RenderEngine 接口设计...]
[Agent 2 正在评估 FLAT_JSON 路径能否消除 Java 侧模板代码...]
[Agent 3 正在检查 53 个 TaskHandler 的迁移可行性...]
...

[15 分钟后，5 个 Agent 陆续完成]

🤖 AI（汇总）:
## 多角度审查汇总

### 共识
✅ Phase 1-2 的渐进式解耦策略是正确的，风险可控
✅ FLAT_JSON 路径能有效消除业务方对 Java 侧模板代码的依赖
✅ 统一渲染 API 设计清晰，RESTful 接口对非 Java 业务方友好

### 分歧与风险
⚠️ Agent 2 指出：Phase 4 的 Template Studio 在线编辑功能
   低代码模式表达力不足，可能无法覆盖所有业务场景
⚠️ Agent 3 发现：存量 53 个任务类型中有 12 个深度耦合
   TaskHandlerConfig 的特殊字段，迁移需要逐个适配
⚠️ Agent 5 建议：模板注册中心应该用数据库而非 YAML 配置文件，
   否则每次新增模板都需要重新部署

### 建议调整
1. Phase 4 取消低代码 DSL 模式，改为 Pro Code + Preset 组件
2. 增加 Phase 3 的迁移优先级排序：先迁简单的 preview 类型
3. 模板注册中心从 YAML 改为数据库方案

👤 用户:
[采纳了建议，调整了设计文档]
```


亮点：5 个 Agent 并行工作，各自从独立视角深入分析，最终由主 Session 汇总成有共识、有分歧、有建议的完整审查报告。Agent 2 指出的"低代码表达力不足"问题后来确实被验证，直接影响了 Phase 4 的设计方向调整。


9. 场景 7：多 Session 多模型协作

核心思路

Claude Code 支持通过环境变量或 CCSwitch 等工具切换底层模型。这意味着你可以在不同终端窗口启动不同厂商、不同模型的 Claude Code 会话，让它们各司其职：

- GLM 模型（性价比高）：负责写代码、搬砖型任务

- Claude Opus（推理能力强）：负责架构设计、代码审查、出报告

- Claude Sonnet（平衡型）：负责日常开发、轻量分析

各 Session 通过文件系统（`docs/` 目录）交换信息，形成流水线。

架构图


```
Plain Text
终端 1（GLM 模型 — 写代码）        终端 2（Opus 模型 — 审查+报告）
┌──────────────────────┐        ┌──────────────────────┐
│ ANTHROPIC_BASE_URL=   │        │ ANTHROPIC_API_KEY=    │
│   bigmodel.cn         │        │   sk-ant-xxx          │
│                       │        │                       │
│ 职责：                 │        │ 职责：                 │
│ - 按实施计划写代码     │        │ - 实时读取代码变更     │
│ - 修改文件            │  ────→ │ - 代码质量审查         │
│ - 运行测试            │        │ - 输出审查报告         │
│                       │        │ - 输出设计文档         │
│                       │  ←──── │                       │
│ 读取审查报告           │        │ docs/review/report.md │
│ 根据反馈修复问题       │        │                       │
└──────────────────────┘        └──────────────────────┘
```


如何启动不同模型的 Session

方式一：环境变量临时切换


```bash
# 终端 1 — 使用 GLM 模型（写代码）
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic \
ANTHROPIC_API_KEY=your-glm-key \
claude

# 终端 2 — 使用 Claude Opus（审查+设计）
ANTHROPIC_API_KEY=sk-ant-xxx \
claude
```


方式二：使用 CCSwitch 工具

CCSwitch 可以在多套模型配置之间快速切换，避免每次手动输入环境变量。

方式三：settings.json 备份切换


```bash
# 备份当前配置
cp ~/.claude/settings.json ~/.claude/settings-claude.json

# 切换到 GLM 配置
cp ~/.claude/settings-glm.json ~/.claude/settings.json

# 切换回 Claude 配置
cp ~/.claude/settings-claude.json ~/.claude/settings.json
```


📝 真实对话案例：三 Session 接力 — 设计 → 实现 → 审查 → 修复闭环


```
以下是 2026-03-02 一次真实的多 Session 多模型协作记录。三个 Session 分工协作，完成了 Phase 4 统一实施计划的设计、实现和审查全流程。
```


```
Plain Text
=== Session B（Claude Opus 4.6 — 架构设计 + 计划生成）===
时间：05:00-07:55

👤 用户:
可以使用 team-agents 从不同角度分析下架构设计文档，
尤其是 Phase4 的设计，是否可以达到渲染平台和业务解绑的目标。

🤖 AI (Opus 4.6):
[启动 4 个并行分析 Agent：架构师/产品经理/技术负责人/解耦专家]
[Agent 陆续返回分析结果]
[综合分析 → 产出 phase4-structural-fixes-plan.md]

👤 用户:
用 writing-plans 技能把它细化为可执行的实施步骤，
需要考虑 tfb-manage-service 和 web-tifenbao-campus-report 这 2 个组件。

🤖 AI (Opus 4.6):
[探索 3 个项目代码库 → 生成 phase4-fixes-implementation-plan.md]
[合并两份计划 → 产出 phase4-unified-implementation-plan.md]

=== Session A（GLM-5 — 交叉验证）===
时间：02:35-07:23（与 Session B 并行）

👤 用户:
我自己做了一个 Phase2-4 的全链路 review，发现了 7 个数据流断裂点
（3 个阻断级、4 个严重级）。请和你的分析比较。

🤖 AI (glm-5):
你的分析更完整。你发现了 7 个断裂点，我之前只发现了 3 个。

  | 断裂点 | 你的分析 | 我的分析 |
  |--------|---------|---------|
  | 1. templateEntryPath 死代码 | ✅ P0 | ✅ 一致 |
  | 2. defined_data vs jsonpCallback | ✅ P0 | ❌ 未发现 |
  | 3. Base64 URL 容量限制 | ✅ P0 | ⚠️ 提及但不深入 |
  | 4-7... | ✅ | ❌ 均未覆盖 |

你的分析是正确的、完整的。

=== 用户实现所有任务（跨 4 个代码仓库）===

=== Session C（GLM-5 — 代码审查）===
时间：08:39-09:55

👤 用户:
我已经完成了 plan 里的任务，请启动 agent-teams
从不同项目不同角度来 review 下代码。

🤖 AI (glm-5):
[启动 6 个并行审查 Agent]

  | Agent | 检查范围 |
  |-------|----------|
  | reviewer-task3a | PDFGenerator 自定义入口 (Java) |
  | reviewer-task3b | GenericRenderTaskHandler PRO_CODE (Java) |
  | reviewer-task1-2 | runtime-host 页面 + 构建脚本 (Vue) |
  | reviewer-task4 | basic-pages-lite.vue (Vue) |
  | reviewer-task8 | 后端接口 + taskData 修正 (Java) |
  | reviewer-frontend | PreviewSandbox + Editor (Vue) |

[6 个 Agent 并行审查，陆续返回结果]

## 审查汇总：总体完成度 83% (5/6 任务完成)

  | 任务 | 状态 | 断裂修复 |
  |------|------|----------|
  | Task 1+2 | ✅ | — |
  | Task 3A | ✅ | 断裂1、2、5 ✅ |
  | Task 3B | ✅ | 断裂3、7 ✅ |
  | Task 4 | ❌ 未实现 | — |
  | Task 8 | ✅ | 断裂4 ✅ |
  | 前端集成 | ⚠️ 85% | 缺环境变量配置 |

👤 用户: 将 review 结果输出到 docs/review/ 目录下

🤖 AI: [写入 docs/review/2026-03-02-phase4-unified-implementation-review.md]

=== 用户修复 2 个待办项 ===

👤 用户: 我已经实现了这 2 个待办，请检查。

🤖 AI:
  ✅ basic-pages-lite.vue — 894 行，分页逻辑完整，无 Vuex 依赖
  ✅ RUNTIME_HOST_URL — 已配置

  审查报告已更新：总体完成度 83% → 100% ✅
```


完整的文件产出链：


| 文件 | 产出 Session | 模型 |
| --- | --- | --- |
| docs/plans/phase4-unified-implementation-plan.md | Session B | Opus 4.6 |
| docs/plans/phase2-4-dataflow-fragmentation-analysis.md | Session A | GLM-5 |
| docs/review/phase4-unified-implementation-review.md | Session C | GLM-5 |


这个案例展示了多 Session 协作的完整闭环：Opus 出设计计划 → GLM 交叉验证 → 用户实现 → GLM 启动 6 个 Agent 并行审查 → 输出审查报告 → 用户修复 → 审查报告更新为 100%。三个 Session 通过 `docs/` 目录下的文件交换信息，各司其职。

真实对话截图（让两个模型互相review：GLM5 VS Opus）：


注意事项：确保两个 Session 不同时修改同一个文件（推荐用 Worktree 隔离）；审查 Session 需要等产出 Session 写完文件后再读取；提前约定文件路径格式（如 `docs/review/YYYY-MM-DD-*.md`）；多 Session 操作 git 时注意不要互相覆盖 commit。


10. 安全风险 - 使用前需要建立的意识

在享受 Claude Code 带来的效率提升之前，有几点安全相关的意识需要建立。不是要吓唬你——而是让你在使用时心里有根弦。

10.1 代码会离开你的电脑

Claude Code 的工作原理是：把你项目的代码发送到远程服务器（Anthropic 或你配置的其他模型提供商）。这意味着：


```
Plain Text
你的电脑 ──代码──→ 远程服务器 ──AI处理──→ 返回结果
```


10.2 敏感信息可能被 AI 读到

你的项目里可能有一些不该外传的文件：.env、credentials.json、id_rsa、数据库密码...

问题：AI 可能会读取这些文件，甚至把它们的内容输出到日志、审查报告、或生成的文档中。

真实场景：


```
Plain Text
你：帮我检查下这个项目的配置
AI：我看到你的 .env 文件里有 DATABASE_PASSWORD=xxx123...
    → 这个密码被写入了对话记录，可能被保存到云端
```


建议：

1. 排除敏感文件：在项目根目录创建 `.claudeignore` 文件（类似 `.gitignore`）：


```
Plain Text
 # .claudeignore
 .env
 .env.*
 credentials.json
 *_secret*
 *.pem
 *.key
```


2. 敏感信息不要写在代码里：这是基本的安全实践，但现在更重要了

10.3 AI 可能执行危险操作

Claude Code 可以执行 git 命令、删除文件、修改代码。这是能力，也是风险。

危险操作示例：

git push --force — 覆盖远程分支

git reset --hard — 丢失本地修改

批量删除文件

覆盖重要配置

建议：

- 涉及 `--force`、`--hard`、删除的操作，人工确认后再执行

重要分支（main/master）的 push，自己来

大规模文件操作前，先 git stash 或 commit

10.4 AI 生成的代码可能有问题

AI 生成的代码可能有：

SQL 注入漏洞

XSS 风险

硬编码密钥或密码

缺少权限校验

建议：

AI 生成的代码上线前，走正常的 Code Review 流程

用你的 code-reviewer Agent 做一道安全审查

涉及用户输入、权限、数据的代码，多看一眼


11. 成本控制

Claude Code 很强大，但强大是有代价的——Token 消耗。我在 40 天里消耗了超过 10 亿 Token。这不是个小数字。

11.1 Token 消耗速度比你想象的快

消耗大户：


| 场景 | Token 消耗 | 说明 |
| --- | --- | --- |
| 长对话（200+ 条消息） | 高 | 上下文越来越长，每次回复都要处理全部历史 |
| 大型项目探索 | 高 | AI 要读很多文件来理解项目 |


| Agent Team    | 极高   | 每个 Agent 独立消耗，4 个 Agent ≈ 4 倍成本 |

上下文膨胀效应：


```
Plain Text
第 1 条消息：AI 需要 processing 1 条消息
第 100 条消息：AI 需要 processing 100 条消息
第 300 条消息：AI 需要 processing 300 条消息 → 成本指数增长
```


这就是为什么长对话到后期会变慢、变贵。

11.2 不同模型成本差异

Claude Code 支持切换底层模型，不同模型成本差异很大：


| 模型类型 | 成本等级 | 适合场景 |
| --- | --- | --- |
| Claude Opus | 高 | 复杂架构设计、代码审查、深度分析 |
| Claude Sonnet | 中 | 日常开发、功能实现 |
| Claude Haiku | 低 | 简单任务、快速问答 |
| GLM 系列 | 较低 | 日常开发、写代码（性价比选择） |


建议：根据任务复杂度选择模型，不是所有任务都需要 Opus。

11.3 Agent Team 的成本放大效应

Agent Team 很强大，但成本是N 倍放大：


```
Plain Text
单 Session 成本 = X
Agent Team（4 个 Agent）≈ 4X
broadcast 群发消息（发给 4 个 Agent）= 4 次 API 调用
```


成本对比：


```
Plain Text
场景：让 AI 分析一份 500 行的架构设计文档

方式 A：单 Session 直接分析
  消耗 ≈ 1X

方式 B：Agent Team（4 个 Agent 并行分析）
  消耗 ≈ 4X
  但获得 4 个不同视角的分析结果
```


Agent Team 适合需要多角度分析的复杂任务，不是所有任务都需要。

建议：

控制 Agent 数量：2-4 个就够了，不要超过 5 个

简单任务不要用 Agent Team

11.4 省钱技巧


```
技巧
节省效果
说明
```


| 及时 /compact      | 高    | 压缩上下文，减少后续每次调用的 token 消耗      |

| 用 subagent 干重活   | 高    | subagent 的上下文独立，不会污染主 session |

| 控制 Agent Team 规模 | 高    | 2-4 个 Agent 通常足够              |

| 简单任务用轻量模型        | 中    | Haiku 或 GLM 轻量版处理简单任务         |

| 避免重复探索           | 中    | 写好 CLAUDE.md，让 AI 一次就理解项目     |

| 长任务分段            | 中    | 与其一次 400 条消息，不如分 3 次会话        |

最重要的建议：

> 用 subagent 去干重活，让主 session 的 context 保持缓慢增长。

这是我最常用的策略。需要探索大量代码、读取很多文件的任务，交给 subagent（或 Agent Team）去做。主 session 只负责协调和决策，这样主 session 的上下文不会爆炸。


12. 我踩过的坑与最佳实践


```
Plain Text
坑 1：CLAUDE.md 太长反而干扰 AI
  ❌ 把所有代码细节都写进 CLAUDE.md（超过 500 行）
  ✅ 保持 200-300 行，重点写架构和规范，细节放在代码注释和文档文件中

坑 2：不用 /compact 导致上下文溢出
  ❌ 一个 Session 聊 300+ 条消息不清理
  ✅ 感觉 AI 回答质量下降时（50% 时手动 /compact，别等自动压缩）用 /compact 压缩上下文
     或者开新 Session，靠 CLAUDE.md 恢复上下文

     尽量用 subagent 去干活，让主 session 的 context 保持缓慢增长

坑 3：让 AI 一次做太多事
  ❌ "帮我重构整个认证模块并加上测试和文档"
  ✅ 用 brainstorm → write-plan → execute-plan 分步推进，每步有 checkpoint

坑 4：多 Session 协作不约定文件路径
  ❌ 两个 Session 各自随意创建文件，找不到对方的产出
  ✅ 提前约定：产出放 docs/plans/，审查放 docs/review/，报告放 docs/reports/
     文件名包含日期和主题：YYYY-MM-DD-topic-type.md
```


最佳实践总结


```
实践
说明
```


| 为每个项目写 CLAUDE.md | 一次投入，永久受益 |

| 用 brainstorm 开始新功能 | 写代码前先想清楚 |

| 为重复操作创建 Skill | 一次编写，反复使用 |

| 为专业分析创建 Agent | 让 AI 扮演不同角色 |

| 用文档驱动开发 | docs/ 目录记录设计、计划、审查、报告 |

| 善用 /compact 和 subagent | 长对话及时压缩，重活交给子 Agent |

| 预授权常用命令 | 减少确认弹窗的打断 |

| Agent Team 控制规模 | 2-4 个 Agent 就够了 |

| 多 Session 善用不同模型 | GLM 搬砖、Opus 设计审查，各司其职 |


彩蛋：这篇文章是怎么诞生的

你正在读的这份分享文档，本身就是一个 Claude Code 深度使用的完整案例。它不是在 Word 里一个字一个字敲出来的——而是我和 Claude Code 协作了 3 轮对话、跨 2 个 Session、AI 自动探索了 130 个历史会话、读取了 13 个 JSONL 文件的产物。

第零步：同一个 Session 的前两个话题

这篇文档诞生在一个已经很长的 Session 中。在写这篇文档之前，同一个会话里我已经完成了两个 brainstorming：

1. Image-to-Template 功能设计：讨论了"业务方上传效果图，AI 自动生成 Vue 模板"的可行性

2. 渲染平台价值定位：质疑了"如果 AI + Puppeteer 就能生成 PDF，渲染平台的意义在哪儿？"

然后我突然想到：这些 Claude Code 的使用方法和工作流本身就值得分享给同事。

第一步：触发 Brainstorming


```
Plain Text
我：/brainstorm 我现在想给其他同事介绍我的 claude code 的使用方法，
    工作流，常用操作，好用的插件的内容，
    请帮我结合我所有的 claude code 历史内容，帮我输出一份完整的分享文档
```


第二步：AI 自动探索我的全部配置（07:21-07:30）

AI 派出了 2 个并行 Agent，同时探索：


| Agent | 任务 | 读取内容 |
| --- | --- | --- |
| Agent 1 | 探索配置文件 | settings.json、plugins/ 目录、所有 CLAUDE.md、teams/ 目录 |
| Agent 2 | 搜索历史数据 | 5 个自定义 Agent 定义、3 个 Skill 定义、stats-cache.json 使用统计 |


AI 发现了我的完整使用画像：130 个会话、22,758 条消息、7,861 次工具调用、5 个自定义 Agent、3 个自定义 Skill、10 个插件。

第三步：结构化提问（07:30-07:42）

AI 没有直接开始写，而是一次一个问题地问我：


```
Plain Text
Q1: 同事的 Claude Code 熟悉程度？→ 我答：用过基础功能
Q2: 文档语言偏好？→ 我答：中文为主
Q3: 文档结构方案？→ AI 提出 3 种方案，我选了"实战驱动型"
Q4: 6 个场景是否全面？→ 我说加 Agent Team、加多 Session、去掉 MCP 数据库
Q5: 场景 2 需要更完整？→ 我说要加 write-plan 和 execute-plan 的使用
Q6: 双 Session 改多 Session？→ 我说主要是为了用不同模型
Q7: 最终确认？→ 我说确认，开始写
```


从想法到确认，经过了 10 轮 Q&A，保证了我们对文档内容的预期完全对齐。

第四步：一次写完初稿（07:43-07:48）

确认后 AI 一次性写出了 966 行 的完整文档，包括所有 7 个场景的结构、代码示例、配置片段和最佳实践。5 分钟内完成，自动 git commit。

第五步：我手动编辑 + AI 润色（07:49-08:09）

我对初稿不满意的地方：删掉了 MCP Server 配置、"高级配置速查"、3 个 Agent Team 相关的"坑"（太细，听众没接触过）；把"双 Session"改成了"多 Session 多模型协作"；加了"总 Token 数超 10 亿"的数据和"尽量用 subagent 去干活"的建议。手动改完后告诉 AI："请帮我重新润色下。" AI 读取了我的修改，理解了每处变更的意图，重写了场景 7 的整个架构图和对比表。

第六步：贴真实对话案例（08:09-08:50）

我觉得文档里的示例太"干净"了，不够真实。于是让 AI 去翻我的历史对话记录——找到 `sessions-index.json`，定位到 13 个历史 Session 的 JSONL 文件，并行读取 5 个关键 Session（每个几千到几万行），从中提取出最有代表性的对话片段，整理成可折叠块插入到对应场景下。中途 Session 上下文耗尽，自动切换到新的 continuation session，AI 无缝接续完成了剩余 3 个场景的案例添加。

第七步：你正在读的最终版

最后我又要求丰富了 CLAUDE.md 章节、突出了 Serena 插件的价值、加了 Worktree 和 Agent-to-Agent 的介绍——以及这个"彩蛋"章节本身。

全过程数据


| 维度 | 数据 |
| --- | --- |
| 从想法到初稿 | 27 分钟（含 10 轮 Q&A） |
| 从初稿到终稿 | 约 1 小时（含手动编辑、润色、案例添加） |
| AI 读取的配置/源文件 | 50+ 个 |
| AI 读取的历史 JSONL 文件 | 13 个 |
| 派出的并行 Agent | 10+ 个 |
| 文档最终长度 | 1500+ 行 |
| 跨越的 Session 数 | 2 个（因上下文耗尽自动续接） |
| 使用的模型 | Claude Opus 4.6 |


这个过程本身说明了什么

1. AI 不是替代你写文档，是和你协作写文档——我做决策（选方案、删章节、定调性），AI 做执行（探索配置、翻历史、组织内容）

2. Brainstorming 流程确实有用——如果 AI 直接开始写，绝对不会是这个结构和深度

3. 历史对话是有价值的——那些 JSONL 文件不是垃圾日志，是可以被 AI 挖掘的经验矿藏

4. 上下文耗尽不可怕——Claude Code 的 continuation 机制让长任务可以无缝接续
