---
title: Hexo+Next配置
date:  2018-02-12 08:12:43
tags:  [Hexo,Next]
categories: 博客搭建
---

# 1.博客中图片的显示问题：
markdown中使用相对路径访问图片，博客上面不会显示。：原因为生成的html文件和图片的相对位置不对了。

解决：

**在Hexo根目录的`source`目录下创建`images`文件夹，将图片放在 `source/images` 文件夹中。然后通过类似于 `![](/images/image.jpg)` 的方法访问它们。**

# 2.添加分类和标签

## 2.1.添加分类

新建一个页面，命名为categories,命令如下：

```
hexo new page categories
```

在进入`source/categories`目录下，编辑`index.md`文件，将页面的类型设置为categories,主题将自动为这个页面显示所有分类

```
---
title: 分类
date: 2014-12-22 12:39:04
type: "categories"
---
```

如果集成了评论，这里需要关闭

```
---
title: 分类
date: 2014-12-22 12:39:04
type: "categories"
comments: false
---
```

## 2.2.添加标签

```
hexo new page tags
```

在进入`source/tags`目录下，编辑`index.md`文件，将页面的类型设置为categories,主题将自动为这个页面显示所有分类

```
---
title: 分类
date: 2014-12-22 12:39:04
type: "tags"
---
```

如果集成了评论，这里需要关闭

```
---
title: 分类
date: 2014-12-22 12:39:04
type: "tags"
comments: false
---
```
## 2.3.配置菜单

修改`hexo目录/theme/next/_config.yml`如下

```
menu:
  home: /|| home
  #about: /about/ || user
  #tags: /tags/ || tags
  #categories: /categories/ || th
  archives: /archives/|| archive
  tags: /tags/|| tag
  categories: /categories/|| th
  about: /about/|| user  
  #schedule: /schedule/ || calendar
  #sitemap: /sitemap.xml || sitemap
  commonweal: /404.html|| heartbeat
```

然后跑去 language 文件夹 zh-Hans.yml 修改中文名字，菜单就以中文显示了。
```
menu:
  home: 首&emsp;&emsp;页
  archives: 归&emsp;&emsp;档
  categories: 分&emsp;&emsp;类
  schedule: 日程表
  sitemap: 站点地图
  tags: 标&emsp;&emsp;签
  about: 关于博主
  search: 站内搜索
  top: 最受欢迎
  # commonweal: 公益404
```


我们发表文章使用「tags」「categories」只需在文章开头添加如下代码：

```
---
title: 利用GitHub和HEXO免费搭建个人博客高级 美化篇
date: 2019-01-29 22:58:56
tags: [hexo建站,hexo部署,github部署,个人博客]      #添加的标签
categories: hexo博客                              #添加的分类
---
```

如此即可在菜单栏里的「tags」「categories」看见相应的效果。但是实际上打开是空白页面 本文的重点来了。
小tips：每次的手输入 categories 我们可以在`hexo目录\scaffolds\post.md` 添加如下代码，这样每次新建文章，就自动有了。

```
---
title: {{ title }}
date: {{ date }}
tags:           #新加
categories:     #新加
---
```

# <span id="评论">3.添加评论</span>

这里我们使用`Valine`评论，我们的评论系统其实是放在Leancloud上的，因此首先需要去注册一个账号

[Leancloud官网，点我注册](https://www.leancloud.cn/)

注册完以后需要创建一个应用，名字可以随便起，然后**进入应用->设置->应用key**,获取`appid` 和 `appkey` 

打开`hexo目录/theme/next/_config.yml`,搜索 `valine`，填入`appid` 和 `appkey`

```
valine:
  enable: true
  appid:  your app id
  appkey: your app key
  notify: false # mail notifier , https://github.com/xCss/Valine/wiki
  verify: false # Verification code
  placeholder: ヾﾉ≧∀≦)o来啊，快活啊! 
  guest_info: nick,mail,link
  pageSize: 10
```

最后记得在**Leancloud -> 设置 -> 安全中心 -> Web 安全域名**把你的域名加进去

# 4.添加阅读次数
使用[3.添加评论](#评论)中应用的`appid` 和 `appkey` ，打开`hexo目录/theme/next/_config.yml`,搜索 `leancloud_visitors`，填入`appid` 和 `appkey`。

```
leancloud_visitors:
  enable: true
  app_id: nGS6I8Lhxl6RuW9rWHtlzQgi-gzGzoHsz
  app_key: osxkNrrnKC4USSNpLUJyfsCb
  security: false
  betterPerformance: false
```


