"""
llm_client 的单元测试。
重点测试「模拟模式」的纯逻辑（不依赖网络/真实 key），保证：
- force_mock 一定走模拟，不发起真实调用
- 流式接口产出的内容拼起来等于完整文本
- 多轮接口能正确取到最后一条用户输入
"""

import llm_client


def test_chat_force_mock_returns_tuple():
    """force_mock=True 时返回 (文本, False)，且不真实调用。"""
    text, is_real = llm_client.chat("系统提示", "你好", force_mock=True)
    assert is_real is False
    assert isinstance(text, str)
    assert "模拟返回" in text


def test_chat_mock_contains_input_preview():
    """模拟返回里应包含用户输入的预览。"""
    text, _ = llm_client.chat("系统", "翻译这句话", force_mock=True)
    assert "翻译这句话" in text


def test_chat_stream_join_equals_full_text():
    """流式产出的分片拼接后应是完整文本。"""
    chunks = list(llm_client.chat_stream("系统", "测试输入", force_mock=True))
    joined = "".join(chunks)
    assert "测试输入" in joined
    assert len(chunks) > 1  # 确实被切成了多片


def test_chat_messages_stream_uses_last_user():
    """多轮模拟应基于最后一条 user 消息。"""
    messages = [
        {"role": "user", "content": "第一个问题"},
        {"role": "assistant", "content": "第一个回答"},
        {"role": "user", "content": "最后一个问题"},
    ]
    out = "".join(llm_client.chat_messages_stream("系统", messages, force_mock=True))
    assert "最后一个问题" in out
    assert "第一个问题" not in out


def test_long_input_is_truncated_in_preview():
    """超长输入在预览里应被截断并加省略号。"""
    long_text = "字" * 200
    text, _ = llm_client.chat("系统", long_text, force_mock=True)
    assert "…" in text


def test_providers_table_complete():
    """6 个提供商都在，且每个都有必要字段。"""
    expected = {"OpenAI", "Claude", "智谱 GLM", "DeepSeek", "千问 Qwen", "Kimi"}
    assert expected.issubset(set(llm_client.PROVIDERS.keys()))
    for name, cfg in llm_client.PROVIDERS.items():
        assert cfg["sdk"] in ("openai", "anthropic")
        assert cfg["models"], f"{name} 缺少预置模型"
        assert cfg["key_url"].startswith("http")


def test_no_key_means_not_real_mode():
    """没填 key 时不是真实模式（不会消耗任何额度）。"""
    # pytest 环境下 session_state 不可用，get_key() 返回空
    assert llm_client.is_real_mode() is False


def test_claude_uses_anthropic_sdk():
    """Claude 走 anthropic SDK，其余走 openai 兼容。"""
    assert llm_client.PROVIDERS["Claude"]["sdk"] == "anthropic"
    assert llm_client.PROVIDERS["DeepSeek"]["sdk"] == "openai"
