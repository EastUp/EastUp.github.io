# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

基于 Hexo 4.2 的个人技术博客，使用 NexT 主题，部署到 GitHub Pages（EastUp.github.io）。博客内容涵盖 Android/C/C++/JNI/OpenCV/FFmpeg/数据结构与算法/Linux 等技术领域，当前共 93 篇文章。

## 常用命令

```bash
# 本地开发预览（默认 http://localhost:4000）
npx hexo server

# 生成静态文件到 public/
npx hexo generate

# 清除缓存和已生成文件（db.json + public/）
npx hexo clean

# 新建文章（会在 source/_posts/ 下创建 md 文件及同名资源目录）
npx hexo new "文章标题"

# 部署到 GitHub Pages
npx hexo deploy

# 清除后重新生成并部署
npx hexo clean && npx hexo generate && npx hexo deploy
```

## 项目结构

```
_config.yml          # Hexo 主配置（站点信息、URL、部署等）
themes/next/         # NexT 主题（含独立 _config.yml）
source/_posts/       # 所有博客文章（Markdown）
source/images/       # 全局图片资源
source/about/        # "关于"页面
source/categories/   # 分类页
source/tags/         # 标签页
scaffolds/           # 文章/页面/草稿模板
public/              # 生成的静态站点（勿手动编辑）
.deploy_git/         # hexo-deployer-git 的部署缓存
```

## 文章规范

- 文章使用 Front Matter 格式，必须包含 `title`、`date`、`tags`、`categories` 字段
- `post_asset_folder: true` 已启用 — 每篇文章可有同名资源目录存放图片等
- 文章文件名格式：`编号.分类-标题.md`（如 `83.FFmpeg-音乐播放器1.md`）
- Markdown 渲染使用 hexo-renderer-kramed（支持 LaTeX 数学公式，配合 hexo-renderer-mathjax）

## 关键配置

- **主题**：NexT（`themes/next/`），主题配置在 `themes/next/_config.yml`
- **部署**：Git 方式部署到 `https://github.com/EastUp/EastUp.github.io.git` 的 master 分支
- **RSS**：通过 hexo-generator-feed 生成 atom.xml
- **搜索**：hexo-generator-searchdb 生成 search.xml
- **语言**：zh-Hans（简体中文）
- **永久链接**：`:title/` 格式（无日期前缀）

## 注意事项

- 修改主题配置时编辑 `themes/next/_config.yml`，而非根目录的 `_config.yml`
- `db.json` 是 Hexo 的数据库缓存文件，遇到生成异常时先 `hexo clean` 清除
- 部署前确保 `hexo generate` 无报错
