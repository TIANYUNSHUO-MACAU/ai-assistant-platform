"""文案生成"""
import streamlit as st
import llm_client
import prompts
import ui
import theme

theme.apply()
force_mock = ui.safety_toggle()
theme.page_header("文案生成", "输入场景或主题，生成多种风格的短文案")

EXAMPLE = "为一家新开的社区咖啡店写开业宣传文案，主打手冲和安静的工作氛围"
if st.button("填入示例"):
    st.session_state["copy_input"] = EXAMPLE

scene = st.text_area(
    "描述你的场景 / 产品 / 主题",
    key="copy_input",
    placeholder="例如：为一家新开的社区咖啡店写开业宣传文案",
    height=120,
)

col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("偏好风格（可选）", ["不限", "正式商务", "活泼年轻", "走心温暖"])
with col2:
    temp = st.slider("创意度", 0.0, 1.0, 0.8, 0.1)

ui.show_prompt(prompts.COPYWRITING)

if st.button("生成文案", type="primary"):
    if not scene.strip():
        st.warning("请先输入场景或主题。")
    else:
        user_input = scene if style == "不限" else f"{scene}\n（风格要求：{style}）"
        st.markdown("##### 生成结果")
        result = st.write_stream(
            llm_client.chat_stream(prompts.COPYWRITING, user_input,
                                   temperature=temp, force_mock=force_mock)
        )
        ui.status_badge(llm_client.is_real_mode() and not force_mock)
        st.download_button("下载结果", result, file_name="文案.txt")
        ui.push_history("copy", user_input, result)

ui.show_history("copy")
