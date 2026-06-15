"""PDF 摘要工具"""
import streamlit as st
import llm_client
import prompts
import ui

st.set_page_config(page_title="PDF 摘要", page_icon="📑")
force_mock = ui.safety_toggle()

st.title("📑 PDF 摘要")
st.caption("上传 PDF，自动提取文本并生成结构化要点")


def extract_text(file) -> str:
    """从 PDF 提取文本，优先 pypdf，回退 PyPDF2。"""
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader
    reader = PdfReader(file)
    pages = [p.extract_text() or "" for p in reader.pages]
    return "\n".join(pages).strip()


uploaded = st.file_uploader("选择 PDF 文件", type=["pdf"])

if uploaded is not None:
    with st.spinner("正在解析 PDF…"):
        try:
            text = extract_text(uploaded)
        except Exception as e:
            text = ""
            st.error(f"PDF 解析失败：{e}")

    if text:
        st.success(f"提取到约 {len(text)} 个字符")
        with st.expander("查看提取到的原文（前 1000 字）"):
            st.text(text[:1000])

        ui.show_prompt(prompts.PDF_SUMMARY)

        if st.button("生成摘要", type="primary"):
            # 控制长度，避免超长输入
            content = text[:6000]
            st.markdown("### 摘要")
            result = st.write_stream(
                llm_client.chat_stream(prompts.PDF_SUMMARY, content,
                                       temperature=0.4, force_mock=force_mock)
            )
            ui.status_badge(llm_client.is_real_mode() and not force_mock)
            st.download_button("⬇️ 下载摘要", result, file_name="PDF摘要.txt")
            ui.push_history("pdf", uploaded.name, result)
    elif uploaded is not None:
        st.warning("没有提取到文本。可能是扫描版 PDF（图片），本工具暂不支持 OCR。")

ui.show_history("pdf")