"""
pdf_utils 的测试：页码标记、预算截断、总字数统计。
不依赖真实 PDF，直接用 (页码, 文本) 列表测纯逻辑。
"""

import pdf_utils


def test_build_marked_text_has_page_markers():
    """合并正文里应带「第N页」标记。"""
    pages = [(1, "第一页内容"), (2, "第二页内容")]
    marked, included = pdf_utils.build_marked_text(pages)
    assert "【第1页】" in marked
    assert "【第2页】" in marked
    assert included == 2


def test_build_marked_text_skips_empty_pages():
    """空白页应被跳过。"""
    pages = [(1, "有内容"), (2, ""), (3, "也有内容")]
    marked, included = pdf_utils.build_marked_text(pages)
    assert included == 2
    assert "【第2页】" not in marked


def test_build_marked_text_respects_budget():
    """超过字符预算时应截断，不会无限增长。"""
    pages = [(i, "字" * 1000) for i in range(1, 21)]  # 20页各1000字
    marked, included = pdf_utils.build_marked_text(pages, char_budget=2000)
    assert len(marked) <= 2200  # 含标记的少量冗余
    assert included < 20


def test_total_chars():
    pages = [(1, "abc"), (2, "de")]
    assert pdf_utils.total_chars(pages) == 5


def test_empty_pages():
    marked, included = pdf_utils.build_marked_text([])
    assert marked == ""
    assert included == 0
