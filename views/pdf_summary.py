"""与 PDF 对话：上传文档后，可摘要、可针对内容追问（对标“chat with your PDF”）"""
import streamlit as st
import prompts
import ui
import theme
import chat_tool

theme.apply()
force_mock = ui.safety_toggle()
theme.page_header("与 PDF 对话", "上传 PDF 后，可生成摘要，也可针对文档内容继续提问")


def extract_text(file) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader
    reader = PdfReader(file)
    return "\n".join(p.extract_text() or "" for p in reader.pages).strip()


uploaded = st.file_uploader("选择 PDF 文件", type=["pdf"])

if uploaded is None:
    st.info("先上传一个 PDF。上传后即可摘要或针对内容提问。")
    st.stop()

# 换文件时重置对话与缓存
if st.session_state.get("pdf_name") != uploaded.name:
    with st.spinner("正在解析 PDF…"):
        try:
            st.session_state["pdf_text"] = extract_text(uploaded)
        except Exception as e:
            st.session_state["pdf_text"] = ""
            st.error(f"PDF 解析失败：{e}")
    st.session_state["pdf_name"] = uploaded.name
    st.session_state["chat_pdf"] = []  # 清空对话

text = st.session_state.get("pdf_text", "")
if not text:
    st.warning("没有提取到文本。可能是扫描版 PDF（图片），本工具暂不支持 OCR。")
    st.stop()

st.caption(f"已加载《{uploaded.name}》· 约 {len(text)} 字")
with st.expander("查看提取到的原文（前 1000 字）"):
    st.text(text[:1000])

# 把 PDF 正文作为附加系统提示（控制长度）
extra = f"以下是文档正文：\n\n{text[:6000]}"

chat_tool.render(
    "pdf",
    prompts.PDF_QA,
    examples=[
        "用要点总结这份文档",
        "这份文档的结论是什么？",
        "提取文档里的关键数据",
    ],
    quick_actions=[
        ("更简短", "把上面的回答压缩得更简短"),
        ("列要点", "把上面的内容整理成条目要点"),
        ("译成英文", "把上面的回答翻译成英文"),
    ],
    input_placeholder="针对这份 PDF 提问…",
    temperature=0.4,
    force_mock=force_mock,
    extra_system=extra,
)
