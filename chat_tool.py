"""
对话式工具组件：把"填表单 → 单次输出"升级为"对话式 + 结果可操作"。
对标 Poe / ChatGPT / Notion AI 的核心交互。

每个工具只需调用 render(...) 并传入：工具标识、系统提示词、空状态示例、快捷追问。
组件负责：历史气泡、空状态引导、流式回复、复制/下载/重新生成、快捷追问、清空对话。
"""

import streamlit as st
import llm_client


def _msgs_key(tool: str) -> str:
    return f"chat_{tool}"


def _get_msgs(tool: str):
    return st.session_state.setdefault(_msgs_key(tool), [])


def render(tool: str, system: str, *, examples=None, quick_actions=None,
           input_placeholder="输入你的内容…", temperature: float = 0.7,
           force_mock: bool = False, extra_system: str = ""):
    """
    渲染一个对话式工具。
    tool:          唯一标识（用于隔离各工具的历史）
    system:        系统提示词
    examples:      空状态示例列表（点击直接发送）
    quick_actions: 已有回复后的快捷追问 [(按钮文字, 实际发送内容), ...]
    extra_system:  附加到 system 后的动态内容（如 PDF 正文）
    """
    examples = examples or []
    quick_actions = quick_actions or []
    full_system = system + ("\n\n" + extra_system if extra_system else "")
    msgs = _get_msgs(tool)

    # —— 空状态：没有对话时，给出示例引导（像成品首屏）——
    if not msgs:
        st.markdown("###### 试试这些，或在下方直接输入")
        cols = st.columns(len(examples) if examples else 1)
        for i, ex in enumerate(examples):
            with cols[i % len(cols)]:
                if st.button(ex, key=f"ex_{tool}_{i}", use_container_width=True):
                    _send(tool, ex)
                    st.rerun()

    # —— 渲染历史对话 ——
    for m in msgs:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # —— 如果最后一条是用户消息且没有回复，生成回复（流式）——
    if msgs and msgs[-1]["role"] == "user":
        with st.chat_message("assistant"):
            api_msgs = [{"role": m["role"], "content": m["content"]} for m in msgs]
            reply = st.write_stream(
                llm_client.chat_messages_stream(
                    full_system, api_msgs, temperature=temperature, force_mock=force_mock
                )
            )
        msgs.append({"role": "assistant", "content": reply})
        st.rerun()  # 重渲染以显示操作按钮

    # —— 已有回复：操作区（复制/下载/重新生成 + 快捷追问）——
    if msgs and msgs[-1]["role"] == "assistant":
        last = msgs[-1]["content"]
        is_real = llm_client.is_real_mode() and not force_mock
        st.caption("· 真实模型输出" if is_real else "· 模拟返回（演示占位）")

        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("重新生成", key=f"regen_{tool}", use_container_width=True):
                msgs.pop()  # 删掉最后的回复，留下用户消息→自动重生成
                st.rerun()
        with c2:
            st.download_button("下载", last, file_name=f"{tool}.txt",
                               key=f"dl_{tool}", use_container_width=True)
        with c3:
            if st.button("清空对话", key=f"clr_{tool}", use_container_width=True):
                st.session_state[_msgs_key(tool)] = []
                st.rerun()

        with st.expander("复制结果（纯文本）"):
            st.code(last, language="text")

        if quick_actions:
            st.markdown("###### 继续调整")
            qcols = st.columns(len(quick_actions))
            for i, (label, payload) in enumerate(quick_actions):
                with qcols[i]:
                    if st.button(label, key=f"qa_{tool}_{i}", use_container_width=True):
                        _send(tool, payload)
                        st.rerun()

    # —— 底部输入框（对话式）——
    if prompt := st.chat_input(input_placeholder):
        _send(tool, prompt)
        st.rerun()


def _send(tool: str, content: str):
    """追加一条用户消息。"""
    _get_msgs(tool).append({"role": "user", "content": content})
