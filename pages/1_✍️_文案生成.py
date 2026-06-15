"""文案生成工具"""
import streamlit as st
import llm_client
import prompts

st.set_page_config(page_title="文案生成", page_icon="✍️")
st.title("✍️ 文案生成")
st.caption("输入场景或主题，生成 3 条不同风格的短文案")

scene = st.text_area(
    "描述你的场景 / 产品 / 主题",
    placeholder="例如：为一家新开的社区咖啡店写开业宣传文案",
    height=120,
)

col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("偏好风格（可选）", ["不限", "正式商务", "活泼年轻", "走心温暖"])
with col2:
    temp = st.slider("创意度", 0.0, 1.0, 0.8, 0.1)

if st.button("生成文案", type="primary"):
    if not scene.strip():
        st.warning("请先输入场景或主题。")
    else:
        user_input = scene if style == "不限" else f"{scene}\n（风格要求：{style}）"
        with st.spinner("正在生成…"):
            result = llm_client.chat(prompts.COPYWRITING, user_input, temperature=temp)
        st.markdown("### 生成结果")
        st.write(result)
