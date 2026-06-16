"""简历优化（对话式）"""
import ui
import prompts
import theme
import chat_tool

theme.apply()
force_mock = ui.safety_toggle()
theme.page_header("简历优化", "输入简历片段，得到诊断与优化，可继续追问改写")
ui.show_prompt(prompts.RESUME)

chat_tool.render(
    "resume",
    prompts.RESUME,
    examples=[
        "负责公司微信公众号的日常运营和文章撰写。",
        "做过几个前端项目，用 React。",
        "在校期间参加过创业比赛拿了奖。",
    ],
    quick_actions=[
        ("量化成果", "把上面的优化结果再补充一些可量化的成果表达"),
        ("更精简", "把上面的优化结果压缩成一两句话"),
        ("换个角度", "从另一个角度再优化一版上面的内容"),
    ],
    input_placeholder="粘贴你的简历片段…",
    temperature=0.5,
    force_mock=force_mock,
)
