"""
统一的 LLM 客户端，支持双模式：
1. 真实模式：读取 .env 中的智谱 GLM 配置（Anthropic 兼容端点），调用真实模型。
2. 模拟模式（mock）：未配置 key 或调用失败时，返回模拟结果，保证整个 Demo 流程可演示。

零基础提示：你不需要懂下面所有细节。只要 .env 填了 key，就会走真实调用；
否则自动走 mock，页面照样能用、能演示。
"""

import os
from dotenv import load_dotenv

load_dotenv()  # 从 .env 读取环境变量

# 读取配置
BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "").strip()
AUTH_TOKEN = os.getenv("ANTHROPIC_AUTH_TOKEN", "").strip()
MODEL = os.getenv("LLM_MODEL", "glm-4.6").strip()

# 判断是否具备真实调用的条件
_REAL_READY = bool(BASE_URL and AUTH_TOKEN and "填入" not in AUTH_TOKEN)


def is_real_mode() -> bool:
    """当前是否处于真实 API 模式。"""
    return _REAL_READY


def current_model() -> str:
    return MODEL


def _mock_reply(system: str, user: str) -> str:
    """没有 key 或调用失败时的模拟返回。仅用于跑通流程。"""
    preview = user.strip().replace("\n", " ")
    if len(preview) > 60:
        preview = preview[:60] + "…"
    return (
        "【模拟返回 · 未接真实模型】\n"
        f"收到你的输入：{preview}\n\n"
        "这是占位结果，用于演示流程。配置 .env 中的智谱 key 后，"
        "这里会显示真实的 GLM 模型输出。"
    )


def chat(system: str, user: str, temperature: float = 0.7, max_tokens: int = 1024) -> str:
    """
    向模型发送一次对话请求，返回纯文本。
    system: 系统提示词（设定角色/任务）
    user:   用户输入
    任何异常都会回退到 mock，避免 Demo 当场报错。
    """
    if not _REAL_READY:
        return _mock_reply(system, user)

    import time
    from anthropic import Anthropic

    client = Anthropic(base_url=BASE_URL, auth_token=AUTH_TOKEN)
    last_err = None
    # 智谱端点偶发 503（瞬时无可用账户），对临时错误重试几次
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            # 拼接返回的文本块
            parts = [block.text for block in resp.content if getattr(block, "type", "") == "text"]
            text = "\n".join(parts).strip()
            return text or _mock_reply(system, user)
        except Exception as e:  # 网络/额度/模型名等任何问题都兜底
            last_err = e
            if attempt < 2:
                time.sleep(1.2 * (attempt + 1))  # 退避后重试
    return f"{_mock_reply(system, user)}\n\n（调用真实模型失败，已回退模拟返回。原因：{last_err}）"
