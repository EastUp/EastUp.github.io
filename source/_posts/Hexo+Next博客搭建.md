---
title: Hexo+Next博客搭建
date:  2018-02-10 08:12:43
tags:  [Hexo,Next]
categories: 博客搭建
---

这里我们使用 GitHub Pages 来搭建 Hexo 静态博客网站，其最吸引人的莫过于完全免费使用，并且非常稳定。

# 1.原理
## GitHub Pages 是什么？
GitHub Pages 是由 GitHub 官方提供的一种免费的静态站点托管服务，让我们可以在 GitHub 仓库里托管和发布自己的静态网站页面。

## Hexo 是什么？

Hexo 是一个快速、简洁且高效的静态博客框架，它基于 Node.js 运行，可以将我们撰写的 Markdown 文档解析渲染成静态的 HTML 网页。

## Hexo + GitHub 文章发布原理
在本地撰写 Markdown 格式文章后，通过 Hexo 解析文档，渲染生成具有主题样式的 HTML 静态网页，再推送到 GitHub 上完成博文的发布。  

# 2.环境安装
Hexo 基于 `Node.js`，搭建过程中还需要使用 npm（Node.js 已带） 和 `git`，因此先搭建本地操作环境，安装 Node.js 和 Git。

- 下载安装[Node.js](https://nodejs.org/zh-cn)
- 下载安装[Git](https://git-scm.com/downloads)

检查是否安装成功：进入终端，依次输入 `node -v`、`npm -v` 和 `git --version` 并回车，出现程序版本号即可。

# 3.Github配置

## 3.1连接Github

右键 -> Git Bash Here，设置用户名和邮箱：

```
git config --global user.name "GitHub 用户名"
git config --global user.email "GitHub 邮箱"
```

## 3.2创建 SSH 密匙添加到Github上

输入 `ssh-keygen -t rsa -C "GitHub 邮箱"`，然后一路回车。

进入 [C:\Users\用户名\.ssh] 目录（要勾选显示“隐藏的项目”），用记事本打开公钥 id_rsa.pub 文件并复制里面的内容。

登陆 GitHub ，点击用户头像进入 Settings 页面，选择左边栏的 SSH and GPG keys，点击 New SSH key。

Title 随便取个名字，粘贴复制的 id_rsa.pub 内容到 Key 中，点击 Add SSH key 完成添加。

**验证连接**：打开 Git Bash，输入 `ssh -T git@github.com` 出现 `“Are you sure……”`，输入 yes 回车确认。显示 `“Hi xxx! You've successfully……”` 即连接成功。

## 3.3创建 Github Pages 仓库

GitHub 主页右上角加号 -> New repository：

- Repository name 中输入 用户名.github.io
- 勾选 “Initialize this repository with a README”
- Description 选填

填好后点击 Create repository 创建。

创建后默认自动启用 HTTPS，博客地址为：`https://用户名.github.io`

# 4.本地安装 Hexo 博客程序
## 4.1安装 Hexo
使用使用 npm 一键安装 Hexo 博客程序：

```
npm install -g hexo-cli

// linux或mac用户需要管理员权限（sudo），运行这条命令：

sudo npm install -g hexo-cli
```

## 4.2 Hexo 初始化和本地预览
初始化并安装所需组件：

```
hexo init      # 初始化
npm install    # 安装组件
```

完成后依次输入下面命令，启动本地服务器进行预览：

```
hexo g   # 生成页面
hexo s   # 启动预览
```

访问 http://localhost:4000 出现 Hexo 默认页面，本地博客安装成功！

Hexo 博客文件夹目录结构如下：
![](/images/hexo目录结构.jpg)

# 5. 部署 Hexo 到 GitHub Pages

首先安装 hexo-deployer-git：

```
npm install hexo-deployer-git --save
```

然后修改 _config.yml 文件末尾的 Deployment 部分，修改成如下：

```
deploy:
  type: git
  repository: git@github.com:用户名/用户名.github.io.git
  branch: master
```

完成后运行 

```
hexo d #部署到GitHub Pages
```

将网站上传部署到 GitHub Pages。这时访问我们的 GitHub 域名 `https://用户名.github.io` 就可以看到 Hexo 网站了。

# 6.安装Next主题

进入网站目录打开 Git Bash Here 下载主题：

```
git clone https://github.com/iissnan/hexo-theme-next themes/next
```

然后修改 hexo的 `_config.yml` 中的 `theme` 为新主题名称 `next`。

# 7.<font color=red>遇到的问题</color>

```
$ hexo d -g
(node:3908) Warning: Accessing non-existent property 'lineno' of module exports inside circular dependency
(Use `node --trace-warnings ...` to show where the warning was created)
(node:3908) Warning: Accessing non-existent property 'column' of module exports inside circular dependency
(node:3908) Warning: Accessing non-existent property 'filename' of module exports inside circular dependency
(node:3908) Warning: Accessing non-existent property 'lineno' of module exports inside circular dependency
(node:3908) Warning: Accessing non-existent property 'column' of module exports inside circular dependency
(node:3908) Warning: Accessing non-existent property 'filename' of module exports inside circular dependency
INFO  Start processing
INFO  Files loaded in 94 ms
INFO  0 files generated in 22 ms
INFO  Deploying: git
INFO  Clearing .deploy_git folder...
INFO  Copying files from public folder...
FATAL Something's wrong. Maybe you can find the solution here: https://hexo.io/docs/troubleshooting.html
TypeError [ERR_INVALID_ARG_TYPE]: The "mode" argument must be integer. Received an instance of Object
    at copyFile (fs.js:1890:10)
    at tryCatcher (D:\Blog\node_modules\bluebird\js\release\util.js:16:23)
    at ret (eval at makeNodePromisifiedEval (D:\Node\node_global\node_modules\hexo-cli\node_modules\bluebird\js\release\promisify.js:184:12), <anonymous>:13:39)
    at D:\Blog\node_modules\hexo-fs\lib\fs.js:144:39
    at tryCatcher (D:\Blog\node_modules\bluebird\js\release\util.js:16:23)
    at Promise._settlePromiseFromHandler (D:\Blog\node_modules\bluebird\js\release\promise.js:547:31)
    at Promise._settlePromise (D:\Blog\node_modules\bluebird\js\release\promise.js:604:18)
    at Promise._settlePromise0 (D:\Blog\node_modules\bluebird\js\release\promise.js:649:10)
    at Promise._settlePromises (D:\Blog\node_modules\bluebird\js\release\promise.js:729:18)
    at Promise._fulfill (D:\Blog\node_modules\bluebird\js\release\promise.js:673:18)
    at Promise._resolveCallback (D:\Blog\node_modules\bluebird\js\release\promise.js:466:57)
    at Promise._settlePromiseFromHandler (D:\Blog\node_modules\bluebird\js\release\promise.js:559:17)
    at Promise._settlePromise (D:\Blog\node_modules\bluebird\js\release\promise.js:604:18)
    at Promise._settlePromise0 (D:\Blog\node_modules\bluebird\js\release\promise.js:649:10)
    at Promise._settlePromises (D:\Blog\node_modules\bluebird\js\release\promise.js:729:18)
    at Promise._fulfill (D:\Blog\node_modules\bluebird\js\release\promise.js:673:18)
    at Promise._resolveCallback (D:\Blog\node_modules\bluebird\js\release\promise.js:466:57)
    at Promise._settlePromiseFromHandler (D:\Blog\node_modules\bluebird\js\release\promise.js:559:17)
    at Promise._settlePromise (D:\Blog\node_modules\bluebird\js\release\promise.js:604:18)
    at Promise._settlePromise0 (D:\Blog\node_modules\bluebird\js\release\promise.js:649:10)
    at Promise._settlePromises (D:\Blog\node_modules\bluebird\js\release\promise.js:729:18)
    at Promise._fulfill (D:\Blog\node_modules\bluebird\js\release\promise.js:673:18)
```

出现这些是因为node版本太高，切换成低版本的node来安装Hexo就可以了。

我安装的是 `hexo: 4.2.0`  `node: 13.6.0`

```
$ hexo -v
hexo: 4.2.0
hexo-cli: 4.2.0
os: Windows_NT 10.0.18363 win32 x64
node: 13.6.0
v8: 7.9.317.25-node.26
uv: 1.34.0
zlib: 1.2.11
brotli: 1.0.7
ares: 1.15.0
modules: 79
nghttp2: 1.40.0
napi: 5
llhttp: 2.0.1
openssl: 1.1.1d
cldr: 36.0
icu: 65.1
tz: 2019c
unicode: 12.1
```

