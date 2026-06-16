"""翻译助手（对话式）"""
import ui
import prompts
import theme
import chat_tool

theme.apply()
force_mock = ui.safety_toggle()
theme.page_header("翻译助手", "中英互译，自动判断方向，可继续要求润色或调整语气")
ui.show_prompt(prompts.TRANSLATE)

chat_tool.render(
    "translate",
    prompts.TRANSLATE,
    examples=[
        "人工智能正在改变世界。",
        "The early bird catches the worm.",
        "请把这句翻得更口语：我们尽快给您答复。",
    ],
    quick_actions=[
        ("更口语", "把上面的译文改得更口语、更自然一些"),
        ("更正式", "把上面的译文改得更正式书面一些"),
        ("解释难点", "解释上面译文里的用词或语法难点"),
    ],
    input_placeholder="输入要翻译的中文或英文…",
    temperature=0.3,
    force_mock=force_mock,
)
