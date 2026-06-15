"""
页面共用的 UI 小工具，避免每个工具页重复写。
包含：演示安全模式开关、真实/模拟状态徽章、提示词查看框、会话历史记录。
"""

import streamlit as st
import llm_client


def safety_toggle() -> bool:
    """侧边栏的「演示安全模式」开关。返回是否强制走模拟。"""
    with st.sidebar:
        st.divider()
        force = st.toggle(
            "🛡️ 演示安全模式",
            value=st.session_state.get("force_mock", False),
            help="打开后所有 AI 工具强制走模拟返回：瞬间出结果、零网络风险，适合彩排和验收兜底。",
            key="force_mock",
        )
        if force:
            st.caption("当前：模拟返回（安全）")
        elif llm_client.is_real_mode():
            st.caption(f"当前：真实模型 {llm_client.current_model()}")
        else:
            st.caption("当前：模拟返回（未配置 key）")
    return force


def status_badge(is_real: bool):
    """在结果上方显示这次输出是真实还是模拟。"""
    if is_real:
        st.success("✅ 本次为真实模型输出", icon="✅")
    else:
        st.info("🟡 本次为模拟返回（演示占位）", icon="🟡")


def show_prompt(system_prompt: str):
    """可展开查看当前工具使用的系统提示词（验收加分项：提示词可见）。"""
    with st.expander("🔍 查看本工具使用的提示词"):
        st.code(system_prompt, language="text")


def push_history(tool: str, user_input: str, output: str):
    """记录一次会话到 session_state。"""
    key = f"history_{tool}"
    st.session_state.setdefault(key, [])
    st.session_state[key].insert(0, {"input": user_input, "output": output})
    st.session_state[key] = st.session_state[key][:10]  # 最多留 10 条


def show_history(tool: str):
    """展示该工具的历史记录，可往回翻。"""
    key = f"history_{tool}"
    records = st.session_state.get(key, [])
    if not records:
        return
    with st.expander(f"🕘 本次会话历史（{len(records)} 条）"):
        for i, r in enumerate(records, 1):
            st.markdown(f"**#{i} 输入**：{r['input'][:60]}")
            st.markdown(f"**输出**：{r['output'][:200]}")
            st.divider()
