"""首页：概览 + 工具入口卡片"""
import streamlit as st
import llm_client
import theme

theme.apply()

st.markdown("# 多功能智能助手平台")
st.caption("零基础项目实训 · Streamlit Demo · 6/1 – 6/5")

# 顶部状态：低调一行，不用彩色大色块
if llm_client.is_real_mode():
    st.caption(f"已接入真实模型 {llm_client.current_model()} · 侧边栏可切换演示安全模式")
else:
    st.caption("当前为模拟返回模式（未配置 key），流程可完整演示")

st.markdown("<hr>", unsafe_allow_html=True)

TOOLS = [
    ("views/copywriting.py", "文案生成", "输入场景，生成多风格短文案"),
    ("views/translate.py", "翻译助手", "中英互译，自动判断方向"),
    ("views/resume.py", "简历优化", "输入简历片段，输出修改建议"),
    ("views/csv_preview.py", "CSV 预览", "上传表格，统计与图表，纯本地"),
    ("views/pdf_summary.py", "PDF 摘要", "上传 PDF，生成结构化要点"),
    ("views/weekly_report.py", "周报生成器", "零散记录整理成周报"),
]

cols = st.columns(3, gap="medium")
for i, (path, title, desc) in enumerate(TOOLS):
    with cols[i % 3]:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(desc)
            st.page_link(path, label="打开")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "**本周目标**：完成一个可演示的 AI 工具集 Demo，并留下一份框架选型说明。\n\n"
    "演示遇到网络问题时，打开侧边栏的「演示安全模式」即可全程稳定跑通。"
)
