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
    st.success(f"✅ 已接入真实模型：{llm_client.current_model()}（每个工具侧边栏可切换「演示安全模式」）")
else:
    st.warning("⚠️ 当前为「模拟返回」模式：未检测到 API key，AI 工具返回占位结果，"
               "流程依然可完整演示。配置 .env 后自动切换为真实调用。")

st.divider()
st.subheader("选择一个工具开始")

# 可点击的工具卡片（st.page_link 直接跳转到对应页面）
TOOLS = [
    ("pages/1_✍️_文案生成.py", "✍️ 文案生成", "输入场景，生成多风格短文案"),
    ("pages/2_🌐_翻译助手.py", "🌐 翻译助手", "中英互译，自动判断方向"),
    ("pages/3_📄_简历优化.py", "📄 简历优化", "输入简历片段，输出修改建议"),
    ("pages/4_📊_CSV预览.py", "📊 CSV 预览", "上传表格，自动统计+图表（纯本地）"),
    ("pages/5_📑_PDF摘要.py", "📑 PDF 摘要", "上传 PDF，生成结构化要点"),
    ("pages/6_🗓️_周报生成器.py", "🗓️ 周报生成器", "零散记录整理成周报"),
    ("pages/7_📋_项目说明.py", "📋 项目说明", "框架选型 / 分工 / 验收一页讲清"),
]

cols = st.columns(3)
for i, (path, title, desc) in enumerate(TOOLS):
    with cols[i % 3]:
        with st.container(border=True):
            st.markdown(f"#### {title}")
            st.caption(desc)
            st.page_link(path, label="打开 →")

st.divider()
st.markdown(
    "**本周目标**：完成一个可演示的 AI 工具集 Demo + 一份框架选型说明。\n\n"
    "**提示**：AI 工具需要联网和 API key；CSV 预览完全本地运行，任何情况下都能演示。"
    "演示遇到网络问题时，打开侧边栏的「🛡️ 演示安全模式」即可全程稳定跑通。"
)
