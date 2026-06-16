"""
chat_tool.trim_history 的测试：验证历史截断与“首条必须是 user”的规则。
"""

import chat_tool


def test_trim_keeps_recent_turns():
    """超过上限时只保留最近 max_turns 条。"""
    msgs = [{"role": "user" if i % 2 == 0 else "assistant", "content": str(i)}
            for i in range(20)]
    out = chat_tool.trim_history(msgs, max_turns=6)
    assert len(out) <= 6


def test_trim_first_message_is_user():
    """截断后首条必须是 user（Anthropic 要求）。"""
    msgs = [{"role": "user" if i % 2 == 0 else "assistant", "content": str(i)}
            for i in range(20)]
    out = chat_tool.trim_history(msgs, max_turns=5)
    assert out[0]["role"] == "user"


def test_trim_short_history_unchanged():
    """历史很短时原样返回（内容一致）。"""
    msgs = [
        {"role": "user", "content": "问题"},
        {"role": "assistant", "content": "回答"},
    ]
    out = chat_tool.trim_history(msgs, max_turns=12)
    assert [m["content"] for m in out] == ["问题", "回答"]


def test_trim_empty():
    """空历史返回空列表。"""
    assert chat_tool.trim_history([], max_turns=12) == []


def test_trim_drops_leading_assistant():
    """若截断窗口以 assistant 开头，应被去掉直到 user。"""
    msgs = [
        {"role": "assistant", "content": "a"},
        {"role": "assistant", "content": "b"},
        {"role": "user", "content": "c"},
    ]
    out = chat_tool.trim_history(msgs, max_turns=3)
    assert out[0]["role"] == "user"
    assert out[0]["content"] == "c"
