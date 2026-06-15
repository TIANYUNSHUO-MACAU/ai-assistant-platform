"""
多功能智能助手平台 —— 主入口页面
运行方式：在项目目录下执行  streamlit run app.py
左侧边栏会自动出现各个工具页面（来自 pages/ 目录）。
"""

import streamlit as st
import llm_client

st.set_page_config(page_title="多功能智能助手平台", page_icon="🤖", layout="wide")

st.title("🤖 多功能智能助手平台")
st.caption("零基础项目实训 · Streamlit Demo · 6/1 - 6/5")

# 顶部状态：当前是真实模式还是模拟模式
if llm_client.is_real_mode():
    st.success(f"✅ 已接入真实模型：{llm_client.current_model()}")
else:
    st.warning("⚠️ 当前为「模拟返回」模式：未检测到 API key，所有 AI 工具会返回占位结果，"
               "流程依然可以完整演示。配置 .env 后即自动切换为真实调用。")

st.divider()

st.subheader("👈 从左侧选择一个工具")

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        "#### ✍️ 文案生成\n输入场景，生成多风格短文案\n\n"
        "#### 🌐 翻译助手\n中英互译，自动判断方向"
    )
with col2:
    st.markdown(
        "#### 📄 简历优化\n输入简历片段，输出修改建议\n\n"
        "#### 📊 CSV 预览\n上传表格，自动统计与说明（纯本地，不需要联网）"
    )

st.divider()
st.markdown(
    "**本周目标**：完成一个可演示的 AI 工具集 Demo + 一份框架选型说明。\n\n"
    "**使用提示**：AI 工具需要联网和 API key；CSV 预览完全本地运行，"
    "任何情况下都能演示。"
)
