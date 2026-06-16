"""
LLM 客户端：多提供商 BYOK（Bring Your Own Key，自带密钥）。

支持 OpenAI / Claude / 智谱GLM / DeepSeek / 千问 / Kimi。
- Claude 走 anthropic SDK；其余走 openai 兼容 SDK（统一处理）。
- 配置来自 st.session_state（用户在「模型设置」页填写），每个访客独立、
  刷新或关闭页面即清空，绝不写入服务器或仓库。
- 未填 key 时走「模拟返回」，不消耗任何人的额度。
"""

import time
import streamlit as st

# 提供商配置表：sdk 类型、兼容端点、预置模型、获取 key 的地址
PROVIDERS = {
    "智谱 GLM": {
        "sdk": "openai",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "models": ["glm-4.6", "glm-4.5", "glm-4-plus", "glm-4-flash"],
        "key_url": "https://open.bigmodel.cn/usercenter/apikeys",
    },
    "OpenAI": {
        "sdk": "openai",
        "base_url": None,  # 用 SDK 默认官方端点
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "o4-mini"],
        "key_url": "https://platform.openai.com/api-keys",
    },
    "Claude": {
        "sdk": "anthropic",
        "base_url": None,
        "models": ["claude-sonnet-4-5", "claude-3-5-sonnet-latest", "claude-3-5-haiku-latest"],
        "key_url": "https://console.anthropic.com/settings/keys",
    },
    "DeepSeek": {
        "sdk": "openai",
        "base_url": "https://api.deepseek.com",
        "models": ["deepseek-chat", "deepseek-reasoner"],
        "key_url": "https://platform.deepseek.com/api_keys",
    },
    "千问 Qwen": {
        "sdk": "openai",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "models": ["qwen-plus", "qwen-turbo", "qwen-max"],
        "key_url": "https://bailian.console.aliyun.com/",
    },
    "Kimi": {
        "sdk": "openai",
        "base_url": "https://api.moonshot.cn/v1",
        "models": ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"],
        "key_url": "https://platform.moonshot.cn/console/api-keys",
    },
}

DEFAULT_PROVIDER = "智谱 GLM"


def _ss_get(key, default=""):
    """安全读取 session_state（在非 Streamlit 运行环境如 pytest 下不报错）。"""
    try:
        return st.session_state.get(key, default)
    except Exception:
        return default


def get_provider() -> str:
    p = _ss_get("llm_provider", DEFAULT_PROVIDER)
    return p if p in PROVIDERS else DEFAULT_PROVIDER


def get_key() -> str:
    return str(_ss_get("llm_key", "")).strip()


def get_model() -> str:
    m = str(_ss_get("llm_model", "")).strip()
    return m or PROVIDERS[get_provider()]["models"][0]


def is_real_mode() -> bool:
    """填了 key 才算真实模式。"""
    return bool(get_key())


def current_model() -> str:
    return get_model()


# ---------- 模拟返回（无 key / 安全模式 / 调用失败 兜底）----------

def _mock_reply(user: str) -> str:
    preview = user.strip().replace("\n", " ")
    if len(preview) > 60:
        preview = preview[:60] + "…"
    return (
        "【模拟返回 · 占位结果】\n"
        f"收到你的输入：{preview}\n\n"
        "这是用于演示流程的占位文本。在「模型设置」里选择提供商并填入你自己的 "
        "API Key 后，这里会显示真实模型的输出。"
    )


def _mock_multi(messages) -> str:
    last_user = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user = m.get("content", "")
            break
    return _mock_reply(last_user)


def _fake_stream(text: str):
    """把整段文本切成小块逐步产出，模拟打字效果。"""
    for i in range(0, len(text), 4):
        yield text[i:i + 4]
        time.sleep(0.012)


# ---------- 真实调用：两条 SDK 路径 ----------

def _stream_openai(cfg, key, model, system, messages, temperature, max_tokens):
    from openai import OpenAI
    kwargs = {"api_key": key}
    if cfg["base_url"]:
        kwargs["base_url"] = cfg["base_url"]
    client = OpenAI(**kwargs)
    full = [{"role": "system", "content": system}] + list(messages)
    stream = client.chat.completions.create(
        model=model, messages=full, temperature=temperature,
        max_tokens=max_tokens, stream=True,
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta


def _stream_anthropic(key, model, system, messages, temperature, max_tokens):
    from anthropic import Anthropic
    client = Anthropic(api_key=key)
    with client.messages.stream(
        model=model, max_tokens=max_tokens, temperature=temperature,
        system=system, messages=list(messages),
    ) as stream:
        for chunk in stream.text_stream:
            yield chunk


def _stream_core(system, messages, temperature, max_tokens, force_mock):
    """统一的流式入口：按提供商路由，失败兜底模拟。"""
    if force_mock or not is_real_mode():
        yield from _fake_stream(_mock_multi(messages))
        return
    cfg = PROVIDERS[get_provider()]
    key, model = get_key(), get_model()
    try:
        if cfg["sdk"] == "anthropic":
            yield from _stream_anthropic(key, model, system, messages, temperature, max_tokens)
        else:
            yield from _stream_openai(cfg, key, model, system, messages, temperature, max_tokens)
    except Exception as e:
        yield from _fake_stream(f"{_mock_multi(messages)}\n\n（真实调用失败，已回退模拟。原因：{e}）")


# ---------- 对外接口（签名保持兼容）----------

def chat_messages_stream(system, messages, temperature=0.7, max_tokens=1024, force_mock=False):
    """多轮对话流式接口。messages=[{role,content},...]。"""
    yield from _stream_core(system, messages, temperature, max_tokens, force_mock)


def chat_stream(system, user, temperature=0.7, max_tokens=1024, force_mock=False):
    """单轮流式接口。"""
    yield from _stream_core(system, [{"role": "user", "content": user}],
                            temperature, max_tokens, force_mock)


def chat(system, user, temperature=0.7, max_tokens=1024, force_mock=False):
    """单轮非流式，返回 (文本, 是否真实输出)。"""
    if force_mock or not is_real_mode():
        return _mock_reply(user), False
    text = "".join(_stream_core(system, [{"role": "user", "content": user}],
                                temperature, max_tokens, force_mock))
    return text, ("【模拟返回" not in text)
