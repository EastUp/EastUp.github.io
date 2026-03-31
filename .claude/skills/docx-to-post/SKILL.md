---
name: docx-to-post
description: 将 Word 文档（.docx）转换为 Hexo 博客文章，完整保留代码块、表格、ASCII 图等富文本元素
user_invocable: true
---

# docx-to-post：Word 文档转博客文章

## 触发条件

用户提供一个 .docx 文件路径，要求发布为博客文章。

## 必要参数

- **docx_path**：Word 文档的绝对路径
- **categories**：文章分类（如 claude、android）
- **tags**：文章标签列表

## 可选参数

- **title**：自定义文章标题（默认从文档内容提取）
- **remove_author**：是否去除原作者个人信息（默认 false）

## 工作流

### 第一步：提取文档内容

使用 Python 脚本解析 docx 的 XML 结构，不使用简单的段落文本提取，而是：

1. 解析 `word/document.xml` 的完整 XML 结构
2. **单行表格** → 识别为代码块，提取语言标记（Bash/JSON/YAML 等），保留换行
3. **多行表格** → 转为 Markdown 表格
4. **段落样式** → style=1/2/3/4 映射为 h1-h4，自动检测章节标题模式
5. **内联代码** → 检测 Consolas/monospace 字体 + shading 标记的 run，包裹为 `` `code` ``

关键 Python 脚本结构：

```python
import zipfile, xml.etree.ElementTree as ET
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# 读取 docx（本质是 zip）中的 word/document.xml
with zipfile.ZipFile(docx_path) as z:
    xml_content = z.read('word/document.xml')

# 遍历 body 下的元素：
# - <w:tbl> 表格元素：rows==1 为代码块，rows>1 为普通表格
# - <w:p> 段落元素：按 pStyle 判断标题级别
# 提取文本时用 iter() 遍历所有子元素，遇到 <w:br> 插入换行，遇到 <w:t> 拼接文本
```

### 第二步：去除作者信息（如需要）

若 `remove_author=true`：
- 用 Grep 搜索文档中的作者名、邮箱、微信号、GitHub 个人链接等
- 列出找到的内容，确认后替换为通用占位符或删除
- 移除文末署名段落

### 第三步：创建 Hexo 文章

1. 执行 `npx hexo new "文章标题"` 创建文章文件
2. 组装 front matter（title、date、tags、categories）
3. 在 `<!-- more -->` 标记前添加文章摘要（从文档副标题或简介提取）
4. 将提取的 Markdown 内容写入文章文件

### 第四步：验证

1. 执行 `npx hexo generate` 确认无报错
2. 确认生成了对应的分类和标签页面

### 第五步：提交（需用户确认）

```
git add source/_posts/新文章.md
git commit -m "feat:[博客]新增XXX文章"
```

## 注意事项

- 需要 `python-docx` 和 `lxml` 库（首次使用时自动安装）
- docx 中的图片无法自动提取（讯飞文档导出的 docx 通常不含内嵌图片）
- 代码块的语言标记从单行表格首个单词推断（Bash/JSON/YAML/Python 等），`Plaintext`/`Text` 映射为无标记
