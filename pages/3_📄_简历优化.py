"""简历优化工具"""
import streamlit as st
import llm_client
import prompts

st.set_page_config(page_title="简历优化", page_icon="📄")
st.title("📄 简历优化")
st.caption("输入一段简历内容，得到问题诊断 + 优化版本")

resume = st.text_area(
    "粘贴你的简历片段",
    placeholder="例如：负责公司微信公众号的日常运营和文章撰写。",
    height=180,
)

if st.button("优化简历", type="primary"):
    if not resume.strip():
        st.warning("请先输入简历内容。")
    else:
        with st.spinner("正在分析…"):
            result = llm_client.chat(prompts.RESUME, resume, temperature=0.5)
        st.markdown("### 优化建议")
        st.write(result)
