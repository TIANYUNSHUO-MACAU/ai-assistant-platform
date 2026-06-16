"""
统一的 LLM 客户端，支持双模式：
1. 真实模式：读取 .env 中的智谱 GLM 配置（Anthropic 兼容端点），调用真实模型。
2. 模拟模式（mock）：未配置 key、开启「演示安全模式」或调用失败时，返回模拟结果，
   保证整个 Demo 流程随时可演示。

零基础提示：你不需要懂下面所有细节。只要 .env 填了 key，就会走真实调用；
否则（或失败时）自动走 mock，页面照样能用、能演示。
"""

import os
import time
from dotenv import load_dotenv

load_dotenv()  # 从 .env 读取环境变量

# 读取配置
BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "").strip()
AUTH_TOKEN = os.getenv("ANTHROPIC_AUTH_TOKEN", "").strip()
MODEL = os.getenv("LLM_MODEL", "glm-4.6").strip()

# 判断是否具备真实调用的条件
_REAL_READY = bool(BASE_URL and AUTH_TOKEN and "填入" not in AUTH_TOKEN)


def is_real_mode() -> bool:
    """是否具备真实 API 调用条件（key 配好了）。"""
    return _REAL_READY


def current_model() -> str:
    return MODEL


def _mock_reply(system: str, user: str) -> str:
    """没有 key、安全模式或调用失败时的模拟返回。仅用于跑通流程。"""
    preview = user.strip().replace("\n", " ")
    if len(preview) > 60:
        preview = preview[:60] + "…"
    return (
        "【模拟返回 · 占位结果】\n"
        f"收到你的输入：{preview}\n\n"
        "这是用于演示流程的占位文本。接入真实模型后，这里会显示 GLM 的实际输出。"
    )


def _get_client():
    from anthropic import Anthropic
    return Anthropic(base_url=BASE_URL, auth_token=AUTH_TOKEN)


def chat(system: str, user: str, temperature: float = 0.7,
         max_tokens: int = 1024, force_mock: bool = False):
    """
    发送一次请求，返回 (文本, 是否真实输出)。
    force_mock=True 时强制走模拟（演示安全模式）。
    任何异常都会回退到 mock，避免 Demo 当场报错。
    """
    if force_mock or not _REAL_READY:
        return _mock_reply(system, user), False

    last_err = None
    client = _get_client()
    # 智谱端点偶发 503（瞬时无可用账户），对临时错误重试几次
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=MODEL, max_tokens=max_tokens, temperature=temperature,
                system=system, messages=[{"role": "user", "content": user}],
            )
            parts = [b.text for b in resp.content if getattr(b, "type", "") == "text"]
            text = "\n".join(parts).strip()
            return (text, True) if text else (_mock_reply(system, user), False)
        except Exception as e:
            last_err = e
            if attempt < 2:
                time.sleep(1.2 * (attempt + 1))
    return (f"{_mock_reply(system, user)}\n\n（真实调用失败，已回退模拟。原因：{last_err}）", False)


def chat_stream(system: str, user: str, temperature: float = 0.7,
                max_tokens: int = 1024, force_mock: bool = False):
    """
    流式版本：逐段产出文本（生成器），供 st.write_stream 实现打字效果。
    无法真实调用时，把 mock 文本切成小段“假装”流式吐出，体验一致。
    """
    if force_mock or not _REAL_READY:
        yield from _fake_stream(_mock_reply(system, user))
        return
    try:
        client = _get_client()
        with client.messages.stream(
            model=MODEL, max_tokens=max_tokens, temperature=temperature,
            system=system, messages=[{"role": "user", "content": user}],
        ) as stream:
            for chunk in stream.text_stream:
                yield chunk
    except Exception as e:
        yield from _fake_stream(
            f"{_mock_reply(system, user)}\n\n（真实调用失败，已回退模拟。原因：{e}）"
        )


def _fake_stream(text: str):
    """把整段文本切成小块逐步产出，模拟打字效果。"""
    for i in range(0, len(text), 4):
        yield text[i:i + 4]
        time.sleep(0.012)


def _mock_multi(messages) -> str:
    """多轮对话的模拟返回。"""
    last_user = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user = m.get("content", "")
            break
    preview = last_user.strip().replace("\n", " ")
    if len(preview) > 60:
        preview = preview[:60] + "…"
    return (
        "【模拟返回 · 占位结果】\n"
        f"收到你的输入：{preview}\n\n"
        "这是用于演示流程的占位文本。接入真实模型后，这里会显示 GLM 的实际输出。"
    )


def chat_messages_stream(system: str, messages, temperature: float = 0.7,
                         max_tokens: int = 1024, force_mock: bool = False):
    """
    多轮对话流式接口。messages 为 [{"role": "user"/"assistant", "content": ...}, ...]。
    用于对话式工具：保留上下文，可追问、可“再来一版”。
    无法真实调用时回退模拟流。
    """
    if force_mock or not _REAL_READY:
        yield from _fake_stream(_mock_multi(messages))
        return
    try:
        client = _get_client()
        with client.messages.stream(
            model=MODEL, max_tokens=max_tokens, temperature=temperature,
            system=system, messages=messages,
        ) as stream:
            for chunk in stream.text_stream:
                yield chunk
    except Exception as e:
        yield from _fake_stream(f"{_mock_multi(messages)}\n\n（真实调用失败，已回退模拟。原因：{e}）")
