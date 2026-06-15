"""
多功能智能助手平台 —— 应用入口
运行：streamlit run app.py
使用 st.navigation 自定义侧边栏导航，配单色线性图标（Material Symbols）。
"""

import streamlit as st

st.set_page_config(
    page_title="多功能智能助手平台",
    page_icon=":material/dashboard:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 用单色线性图标（Material Symbols），整体克制商务
pages = {
    "概览": [
        st.Page("views/home.py", title="首页", icon=":material/home:", default=True),
        st.Page("views/about.py", title="项目说明", icon=":material/description:"),
    ],
    "AI 工具": [
        st.Page("views/copywriting.py", title="文案生成", icon=":material/edit_note:"),
        st.Page("views/translate.py", title="翻译助手", icon=":material/translate:"),
        st.Page("views/resume.py", title="简历优化", icon=":material/contract:"),
        st.Page("views/pdf_summary.py", title="PDF 摘要", icon=":material/picture_as_pdf:"),
        st.Page("views/weekly_report.py", title="周报生成器", icon=":material/calendar_month:"),
    ],
    "本地工具": [
        st.Page("views/csv_preview.py", title="CSV 预览", icon=":material/table_chart:"),
    ],
}

nav = st.navigation(pages, position="sidebar")
nav.run()
