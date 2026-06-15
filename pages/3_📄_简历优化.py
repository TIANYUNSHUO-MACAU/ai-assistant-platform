"""简历优化工具"""
import streamlit as st
import llm_client
import prompts
import ui

st.set_page_config(page_title="简历优化", page_icon="📄")
force_mock = ui.safety_toggle()

st.title("📄 简历优化")
st.caption("输入一段简历内容，得到问题诊断 + 优化版本")

EXAMPLE = "负责公司微信公众号的日常运营和文章撰写，平时也帮忙做一些活动。"
if st.button("📝 填入示例"):
    st.session_state["resume_input"] = EXAMPLE

resume = st.text_area(
    "粘贴你的简历片段",
    key="resume_input",
    placeholder="例如：负责公司微信公众号的日常运营和文章撰写。",
    height=180,
)

ui.show_prompt(prompts.RESUME)

if st.button("优化简历", type="primary"):
    if not resume.strip():
        st.warning("请先输入简历内容。")
    else:
        st.markdown("### 优化建议")
        result = st.write_stream(
            llm_client.chat_stream(prompts.RESUME, resume,
                                   temperature=0.5, force_mock=force_mock)
        )
        ui.status_badge(llm_client.is_real_mode() and not force_mock)
        st.download_button("⬇️ 下载结果", result, file_name="简历优化.txt")
        ui.push_history("resume", resume, result)

ui.show_history("resume")