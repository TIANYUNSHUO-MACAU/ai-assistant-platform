"""文案生成（对话式）"""
import ui
import prompts
import theme
import chat_tool

theme.apply()
force_mock = ui.safety_toggle()
theme.page_header("文案生成", "输入场景，生成多风格短文案，可继续追问调整")
ui.show_prompt(prompts.COPYWRITING)

chat_tool.render(
    "copywriting",
    prompts.COPYWRITING,
    examples=[
        "社区咖啡店开业文案",
        "新款无线耳机促销文案",
        "读书分享活动招募文案",
    ],
    quick_actions=[
        ("更正式", "把上面的文案改得更正式商务一些"),
        ("更活泼", "把上面的文案改得更活泼年轻一些"),
        ("再短一点", "把上面每条文案压缩到 20 字以内"),
    ],
    input_placeholder="描述你的场景 / 产品 / 主题…",
    temperature=0.8,
    force_mock=force_mock,
)
