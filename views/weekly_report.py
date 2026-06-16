"""周报生成器（对话式）"""
import ui
import prompts
import theme
import chat_tool

theme.apply()
force_mock = ui.safety_toggle()
theme.page_header("周报生成器", "把零散记录整理成周报，可继续要求调整详略")
ui.show_prompt(prompts.WEEKLY_REPORT)

EXAMPLE = (
    "周一装环境建仓库；周二讨论选了 Streamlit；"
    "做了翻译和文案两个工具；周四合并写 README；测试清单还没写完"
)

chat_tool.render(
    "weekly",
    prompts.WEEKLY_REPORT,
    examples=[
        EXAMPLE,
        "改了三个 bug，开了两个会，帮同事看了代码",
    ],
    quick_actions=[
        ("更简短", "把上面的周报压缩得更简短"),
        ("更详细", "把上面的周报每条展开说明得更详细"),
        ("加下周计划", "基于上面内容，补充一段更具体的下周计划"),
    ],
    input_placeholder="把这周做的事一条条写下来…",
    temperature=0.5,
    force_mock=force_mock,
)
