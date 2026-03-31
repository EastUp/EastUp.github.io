---
name: docx-to-post
description: 将 Word(.docx) 文档转换为 Hexo 博客文章。触发词：docx、word、文档 + 博客、文章、发布、发到博客、新增文章、补充文章、转成博客。完整保留代码块、表格、ASCII图。支持去除作者信息、自动检测标题层级、验证生成并提交。
user_invocable: true
---

# docx-to-post：Word 文档转博客文章

## 参数收集

开始前确认以下信息，用户未提供的主动询问：

| 参数 | 必要性 | 默认值 | 说明 |
|------|--------|--------|------|
| docx_path | 必须 | - | .docx 文件绝对路径 |
| categories | 必须 | - | 文章分类（如 claude、android） |
| tags | 可选 | 从文档内容推断 | 文章标签列表 |
| title | 可选 | 从文档标题提取 | 自定义文章标题 |
| remove_author | 可选 | false | 是否去除原作者个人信息 |

## 工作流

### 第一步：提取文档内容

使用项目脚本解析 docx 的 XML 结构：

```bash
py .claude/skills/docx-to-post/scripts/extract_docx.py "<docx_path>" "<临时输出路径>"
```

> 若脚本依赖缺失（`lxml`），先执行 `py -m pip install lxml`

脚本解析能力：
- **单行表格** → 代码块（自动检测 Bash/JSON/Python 等语言标记）
- **多行表格** → Markdown 表格
- **pStyle 1-4** → h1-h4 标题
- **numPr 编号段落**（ilvl=0 + 短文本）→ ## 章节标题
- **Consolas/monospace + shading** → 内联代码

### 第二步：检查提取质量

1. 读取提取结果，确认标题层级（`##`/`###`）是否正确
2. 检查代码块是否完整保留换行
3. 若发现编号标题未被识别（纯文本数字开头），手动补充 `##` 标记

### 第三步：去除作者信息（如需要）

若用户要求去除作者信息：
1. 用 Grep 搜索提取内容中的人名、邮箱、微信号、GitHub 个人主页链接
2. 列出找到的内容，确认后替换为通用占位符或删除
3. 移除文末署名段落

### 第四步：创建 Hexo 文章

1. `npx hexo new "文章标题"` 创建文章
2. 写入 front matter + `<!-- more -->` 摘要 + 正文内容
3. front matter 格式：

```yaml
---
title: 文章标题
date: YYYY-MM-DD HH:mm:ss
tags:
  - 标签1
  - 标签2
categories:
  - 分类名
copyright:
---
```

### 第五步：验证

`npx hexo generate` 确认无报错，检查分类和标签页面是否生成

### 第六步：提交（需用户确认）

```bash
git add source/_posts/新文章.md
git commit -m "feat:[博客]新增XXX文章"
```

## 注意事项

- docx 中的图片无法自动提取（在线文档导出的 docx 通常不含内嵌图片）
- 代码块语言标记从单行表格首词推断，`Plaintext`/`Text` 映射为无标记
- 讯飞文档、飞书文档导出的 docx 与标准 Word 结构可能有差异，注意检查提取质量
