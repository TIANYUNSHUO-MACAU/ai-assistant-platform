"""周报生成器"""
import streamlit as st
import llm_client
import prompts
import ui
import theme

theme.apply()
force_mock = ui.safety_toggle()
theme.page_header("周报生成器", "把零散的工作记录，整理成条理清晰的周报")

EXAMPLE = (
    "周一装环境，建了仓库\n"
    "周二和组里讨论框架，选了 Streamlit\n"
    "做了翻译和文案两个工具\n"
    "周四合并到主页面，写了 README\n"
    "还差测试清单没写完"
)
if st.button("填入示例"):
    st.session_state["weekly_input"] = EXAMPLE

raw = st.text_area(
    "把这周做的事一条条写下来（随便写，不用工整）",
    key="weekly_input",
    placeholder="例如：\n周一装环境\n周二选框架\n做了翻译工具…",
    height=200,
)

ui.show_prompt(prompts.WEEKLY_REPORT)

if st.button("生成周报", type="primary"):
    if not raw.strip():
        st.warning("请先写几条本周做的事。")
    else:
        st.markdown("##### 周报")
        result = st.write_stream(
            llm_client.chat_stream(prompts.WEEKLY_REPORT, raw,
                                   temperature=0.5, force_mock=force_mock)
        )
        ui.status_badge(llm_client.is_real_mode() and not force_mock)
        st.download_button("下载周报", result, file_name="周报.txt")
        ui.push_history("weekly", raw, result)

ui.show_history("weekly")
