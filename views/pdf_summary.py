"""与 PDF 对话：上传文档后可针对内容提问（带页码引用），或一键结构化抽取成表格。"""
import streamlit as st
import prompts
import ui
import theme
import chat_tool
import pdf_utils
import llm_client

theme.apply()
force_mock = ui.safety_toggle()
theme.page_header("与 PDF 对话", "上传 PDF 后，可针对内容提问（回答带页码引用），或抽取成结构化表格")

uploaded = st.file_uploader("选择 PDF 文件", type=["pdf"])

if uploaded is None:
    st.info("先上传一个 PDF。上传后即可针对文档内容提问，或一键抽取关键信息成表格。")
    st.stop()

# 换文件时重新解析并清空对话
if st.session_state.get("pdf_name") != uploaded.name:
    with st.spinner("正在解析 PDF…"):
        try:
            st.session_state["pdf_pages"] = pdf_utils.extract_pages(uploaded)
        except Exception as e:
            st.session_state["pdf_pages"] = []
            st.error(f"PDF 解析失败：{e}")
    st.session_state["pdf_name"] = uploaded.name
    st.session_state["chat_pdf"] = []

pages = st.session_state.get("pdf_pages", [])
if not pages or pdf_utils.total_chars(pages) == 0:
    st.warning("没有提取到文本。可能是扫描版 PDF（图片），本工具暂不支持 OCR。")
    st.stop()

marked, included = pdf_utils.build_marked_text(pages)
st.caption(f"已加载《{uploaded.name}》· 共 {len(pages)} 页 · "
           f"约 {pdf_utils.total_chars(pages)} 字 · 已纳入分析 {included} 页")
with st.expander("查看带页码标记的正文（前 1200 字）"):
    st.text(marked[:1200])

# 一键结构化抽取（独立于对话，直接出表格）
if st.button("结构化抽取为表格", type="primary"):
    st.markdown("##### 抽取结果")
    st.write_stream(
        llm_client.chat_messages_stream(
            prompts.PDF_EXTRACT + "\n\n以下是文档正文：\n\n" + marked,
            [{"role": "user", "content": "请抽取这份文档的关键信息成表格。"}],
            temperature=0.2, force_mock=force_mock,
        )
    )

st.divider()
st.markdown("##### 针对文档提问")

# 对话式问答，把带页码的正文作为附加系统提示
extra = "以下是文档正文（含页码标记）：\n\n" + marked

chat_tool.render(
    "pdf",
    prompts.PDF_QA,
    examples=[
        "用要点总结这份文档",
        "这份文档的结论是什么？",
        "提取文档里的关键数据和日期",
    ],
    quick_actions=[
        ("更简短", "把上面的回答压缩得更简短"),
        ("列要点", "把上面的内容整理成条目要点"),
        ("标出处", "为上面回答里的每个要点补上来源页码"),
    ],
    input_placeholder="针对这份 PDF 提问…",
    temperature=0.3,
    force_mock=force_mock,
    extra_system=extra,
)
