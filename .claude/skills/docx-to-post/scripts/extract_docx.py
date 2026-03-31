"""
从 .docx 文件提取完整 Markdown 内容（保留代码块、表格、ASCII 图）

用法：python extract_docx.py <docx_path> <output_path>
"""
import sys
import re
import zipfile
import xml.etree.ElementTree as ET

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

LANG_PREFIXES = [
    'Bash', 'PowerShell', 'JSON', 'YAML', 'Plaintext', 'Plain Text',
    'Python', 'JavaScript', 'TypeScript', 'Markdown', 'TOML', 'Shell',
    'Text', 'Java', 'Kotlin', 'XML', 'HTML', 'CSS', 'SQL', 'Go', 'Rust',
    'C++', 'C#', 'Ruby', 'Swift', 'Dockerfile', 'Groovy',
]


def get_para_text(p):
    """提取段落文本，保留换行符"""
    parts = []
    for child in p.iter():
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag == 'br':
            parts.append('\n')
        elif tag == 't':
            parts.append(child.text or '')
    return ''.join(parts)


def get_cell_text(cell):
    """提取单元格文本，段落间用换行分隔"""
    paras = cell.findall('.//w:p', NS)
    return '\n'.join(get_para_text(p) for p in paras)


def get_style(p):
    """获取段落样式 ID"""
    pPr = p.find('w:pPr', NS)
    if pPr is not None:
        pStyle = pPr.find('w:pStyle', NS)
        if pStyle is not None:
            return pStyle.get(
                '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '')
    return ''


def get_num_info(p):
    """获取段落的编号信息（numId, ilvl），用于识别编号标题"""
    pPr = p.find('w:pPr', NS)
    if pPr is not None:
        numPr = pPr.find('w:numPr', NS)
        if numPr is not None:
            ilvl_el = numPr.find('w:ilvl', NS)
            numId_el = numPr.find('w:numId', NS)
            ilvl = ilvl_el.get(
                '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '') if ilvl_el is not None else ''
            numId = numId_el.get(
                '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val', '') if numId_el is not None else ''
            return numId, ilvl
    return '', ''


def detect_lang(text):
    """从代码块首行检测语言标记并剥离"""
    for prefix in LANG_PREFIXES:
        if text.startswith(prefix):
            lang = prefix.lower().replace(' ', '')
            text = text[len(prefix):].lstrip('\n')
            if lang in ('plaintext', 'plaintext', 'text'):
                lang = ''
            return lang, text
    return '', text


def process_table(tbl):
    """处理表格：单行表格 → 代码块，多行表格 → Markdown 表格"""
    rows = tbl.findall('.//w:tr', NS)
    if len(rows) == 1:
        cells = rows[0].findall('.//w:tc', NS)
        text = '\n'.join(get_cell_text(c) for c in cells).strip()
        lang, text = detect_lang(text)
        return f'\n```{lang}\n{text}\n```\n'
    else:
        result = []
        for i, row in enumerate(rows):
            cells = row.findall('.//w:tc', NS)
            cell_texts = [get_cell_text(c).strip().replace('\n', '<br>') for c in cells]
            result.append('| ' + ' | '.join(cell_texts) + ' |')
            if i == 0:
                result.append('| ' + ' | '.join(['---'] * len(cell_texts)) + ' |')
        return '\n' + '\n'.join(result) + '\n'


def is_short_title_like(text):
    """判断文本是否像标题（较短、非普通段落）"""
    return len(text) < 80 and not text.endswith(('。', '，', '；', '.', ',', ';'))


# 记录已出现的 numId，用于判断编号标题层级
_seen_num_ids = {}
_num_id_counter = [0]


def process_paragraph(p):
    """处理段落：识别标题级别（pStyle 或 numPr 编号），保留内联代码"""
    text = get_para_text(p).strip()
    if not text:
        return ''

    style = get_style(p)

    # 按样式映射标题
    heading_map = {'1': '#', '2': '##', '3': '###', '4': '####'}
    if style in heading_map:
        return f'{heading_map[style]} {text}'

    # 已有 Markdown 标题格式的直接保留
    if re.match(r'^#{1,4}\s', text):
        return text

    # 编号段落：numPr 且 ilvl=0 且内容像标题 → 视为 ## 章节标题
    numId, ilvl = get_num_info(p)
    if numId and ilvl == '0' and is_short_title_like(text):
        if numId not in _seen_num_ids:
            _seen_num_ids[numId] = _num_id_counter[0]
            _num_id_counter[0] += 1
        # 仅前几个独立 numId（每章一个 numId）识别为章节标题
        if _seen_num_ids[numId] < 20:
            return f'## {text}'

    return text


def extract(docx_path):
    """从 docx 提取 Markdown 内容"""
    _seen_num_ids.clear()
    _num_id_counter[0] = 0
    with zipfile.ZipFile(docx_path) as z:
        xml_content = z.read('word/document.xml')

    root = ET.fromstring(xml_content)
    body = root.find('.//w:body', NS)

    lines = []
    for elem in body:
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'tbl':
            lines.append(process_table(elem))
        elif tag == 'p':
            lines.append(process_paragraph(elem))

    content = '\n\n'.join(lines)
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    return content


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f'用法: python {sys.argv[0]} <docx_path> <output_path>')
        sys.exit(1)

    sys.stdout.reconfigure(encoding='utf-8')
    docx_path = sys.argv[1]
    output_path = sys.argv[2]

    content = extract(docx_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'提取完成：{len(content)} 字符 → {output_path}')
