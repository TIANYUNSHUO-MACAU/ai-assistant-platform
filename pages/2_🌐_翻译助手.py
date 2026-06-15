"""翻译助手工具"""
import streamlit as st
import llm_client
import prompts

st.set_page_config(page_title="翻译助手", page_icon="🌐")
st.title("🌐 翻译助手")
st.caption("中英互译，自动判断翻译方向")

text = st.text_area(
    "输入要翻译的文字（中文或英文）",
    placeholder="例如：人工智能正在改变世界。",
    height=140,
)

if st.button("翻译", type="primary"):
    if not text.strip():
        st.warning("请先输入要翻译的文字。")
    else:
        with st.spinner("正在翻译…"):
            result = llm_client.chat(prompts.TRANSLATE, text, temperature=0.3)
        st.markdown("### 译文")
        st.write(result)
