"""模型设置：选择提供商、填入自己的 API Key、选择模型（BYOK）。"""
import streamlit as st
import theme
import llm_client

theme.apply()
theme.page_header("模型设置", "选择一个 AI 提供商，填入你自己的 API Key（自带密钥，仅本次会话有效）")

st.info(
    "本平台不内置任何付费额度。请填入你自己的 API Key 才能使用真实模型；"
    "不填则所有工具走「模拟返回」，流程依然可完整体验。",
    icon=":material/info:",
)

providers = list(llm_client.PROVIDERS.keys())
cur_provider = llm_client.get_provider()
provider = st.selectbox(
    "AI 提供商",
    providers,
    index=providers.index(cur_provider),
    key="llm_provider",
)

cfg = llm_client.PROVIDERS[provider]

# API Key 输入（密码框，不回显）
st.text_input(
    f"{provider} API Key",
    type="password",
    key="llm_key",
    placeholder="粘贴你的 API Key…",
    help="仅保存在当前浏览器会话中，刷新或关闭页面即清除，不会上传或写入仓库。",
)
st.caption(f"还没有 Key？前往 {provider} 申请： {cfg['key_url']}")

# 模型选择：可下拉可手填（各家模型 ID 更新快，留手填口）
models = cfg["models"]
choice = st.selectbox("模型", models + ["自定义…"], key=f"model_sel_{provider}")
if choice == "自定义…":
    st.text_input("自定义模型 ID", key="llm_model", placeholder="手动输入模型名")
else:
    st.session_state["llm_model"] = choice

st.divider()

# 当前状态
if llm_client.is_real_mode():
    st.success(f"已就绪：{provider} · {llm_client.get_model()}", icon=":material/check_circle:")
else:
    st.warning("未填写 Key，当前为模拟返回模式。", icon=":material/warning:")

with st.expander("各提供商说明 / 兼容性"):
    st.markdown(
        "- **智谱 GLM / DeepSeek / 千问 / Kimi / OpenAI**：走 OpenAI 兼容接口。\n"
        "- **Claude**：走 Anthropic 官方接口。\n"
        "- Key 只在你当前会话内存中，不持久化、不外发、不入库。\n"
        "- 模型 ID 如有更新，可在「模型」里选「自定义…」手动填写。"
    )
