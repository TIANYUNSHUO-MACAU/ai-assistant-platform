"""
页面共用的 UI 小工具。
对话式改版后只保留两个仍在使用的组件：演示安全模式开关、提示词查看框。
"""

import streamlit as st
import llm_client


def safety_toggle() -> bool:
    """侧边栏的「演示安全模式」开关。返回是否强制走模拟。"""
    with st.sidebar:
        st.divider()
        force = st.toggle(
            "演示安全模式",
            value=st.session_state.get("force_mock", False),
            help="打开后所有 AI 工具强制走模拟返回：瞬间出结果、零网络风险，适合彩排和验收兜底。",
            key="force_mock",
        )
        if force:
            st.caption("当前：模拟返回（安全）")
        elif llm_client.is_real_mode():
            st.caption(f"当前：{llm_client.get_provider()} · {llm_client.current_model()}")
        else:
            st.caption("当前：模拟返回（未配置 Key，去「模型设置」填入）")
    return force


def show_prompt(system_prompt: str):
    """可展开查看当前工具使用的系统提示词（验收加分项：提示词可见）。"""
    with st.expander("查看本工具使用的提示词"):
        st.code(system_prompt, language="text")
