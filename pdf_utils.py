"""
PDF 处理工具（与界面解耦，方便测试）。
- 按页抽取文本，给每页打上「第N页」标记，让模型回答时能引用页码
- 构建带页码标记的合并正文，并按预算截断
"""


def extract_pages(file):
    """
    从 PDF 抽取每页文本，返回 [(页码, 文本), ...]（页码从 1 开始）。
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader
    reader = PdfReader(file)
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        pages.append((i, (page.extract_text() or "").strip()))
    return pages


def build_marked_text(pages, char_budget=8000):
    """
    把分页文本拼成带页码标记的正文，总长不超过 char_budget。
    返回 (正文字符串, 实际纳入的页数)。
    """
    parts = []
    used = 0
    included = 0
    for num, text in pages:
        if not text:
            continue
        block = f"【第{num}页】\n{text}\n"
        if used + len(block) > char_budget:
            remain = char_budget - used
            if remain > 50:  # 还能塞下有意义的一段
                parts.append(block[:remain])
                included += 1
            break
        parts.append(block)
        used += len(block)
        included += 1
    return "\n".join(parts).strip(), included


def total_chars(pages) -> int:
    """所有页文本的总字符数。"""
    return sum(len(t) for _, t in pages)
