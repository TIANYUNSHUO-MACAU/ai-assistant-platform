"""翻译助手工具"""
import streamlit as st
import llm_client
import prompts
import ui

st.set_page_config(page_title="翻译助手", page_icon="🌐")
force_mock = ui.safety_toggle()

st.title("🌐 翻译助手")
st.caption("中英互译，自动判断翻译方向")

EXAMPLE = "人工智能正在深刻地改变我们的工作和生活方式。"
if st.button("📝 填入示例"):
    st.session_state["trans_input"] = EXAMPLE

text = st.text_area(
    "输入要翻译的文字（中文或英文）",
    key="trans_input",
    placeholder="例如：人工智能正在改变世界。",
    height=140,
)

ui.show_prompt(prompts.TRANSLATE)

if st.button("翻译", type="primary"):
    if not text.strip():
        st.warning("请先输入要翻译的文字。")
    else:
        st.markdown("### 译文")
        result = st.write_stream(
            llm_client.chat_stream(prompts.TRANSLATE, text,
                                   temperature=0.3, force_mock=force_mock)
        )
        ui.status_badge(llm_client.is_real_mode() and not force_mock)
        st.download_button("⬇️ 下载译文", result, file_name="译文.txt")
        ui.push_history("trans", text, result)

ui.show_history("trans")