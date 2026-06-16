"""
全局视觉主题：深蓝商务风。
通过注入 CSS 实现：引入精致网页字体、隐藏 Streamlit 自带控件、
重做按钮/卡片/提示框/输入框样式，大留白、低饱和、克制点缀色。
每个页面开头调用 apply() 即可。
"""

import streamlit as st

_CSS = """
<style>
/* 字体：思源/Inter 系，商务无衬线 */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap');

:root{
  --navy:#1E3A5F;
  --navy-soft:#2B4E7E;
  --ink:#1A2230;
  --muted:#5B6675;
  --line:#E8ECF1;
  --bg:#FFFFFF;
  --bg-soft:#F5F7FA;
}

html, body, [class*="css"]{
  font-family:'Inter','Noto Sans SC',system-ui,sans-serif;
  color:var(--ink);
}

/* 隐藏 Streamlit 自带控件：顶栏、菜单、页脚、Deploy */
#MainMenu{visibility:hidden;}
header[data-testid="stHeader"]{background:transparent; height:0;}
footer{visibility:hidden;}
[data-testid="stToolbar"]{display:none;}
[data-testid="stDecoration"]{display:none;}

/* 主内容区：更大留白、限制行宽更易读 */
.block-container{
  padding-top:3.2rem; padding-bottom:4rem;
  max-width:1080px;
}

/* 标题层次：去掉花哨，靠字重和字距 */
h1{font-weight:700; letter-spacing:-.02em; color:var(--ink); font-size:2rem;}
h2{font-weight:600; letter-spacing:-.01em; color:var(--ink);}
h3{font-weight:600; color:var(--ink);}
h4{font-weight:600; color:var(--ink);}

/* 说明文字统一中性灰 */
[data-testid="stCaptionContainer"]{color:var(--muted);}

/* 分割线更细更淡 */
hr{border-color:var(--line); margin:1.6rem 0;}

/* 侧边栏：纯净浅底 + 细右边线 */
[data-testid="stSidebar"]{
  background:var(--bg-soft);
  border-right:1px solid var(--line);
}
[data-testid="stSidebarNav"]{padding-top:.5rem;}

/* 主按钮：深蓝实心，克制圆角，hover 微深 */
.stButton>button, .stDownloadButton>button{
  border-radius:7px;
  border:1px solid var(--line);
  font-weight:500;
  padding:.45rem 1.1rem;
  transition:all .15s ease;
}
.stButton>button[kind="primary"], .stDownloadButton>button[kind="primary"]{
  background:var(--navy); border-color:var(--navy); color:#fff;
}
.stButton>button[kind="primary"]:hover{
  background:var(--navy-soft); border-color:var(--navy-soft);
}
.stButton>button:hover{border-color:var(--navy); color:var(--navy);}

/* 输入框：细边、圆角、聚焦深蓝 */
.stTextArea textarea, .stTextInput input{
  border-radius:7px; border:1px solid var(--line);
}
.stTextArea textarea:focus, .stTextInput input:focus{
  border-color:var(--navy); box-shadow:0 0 0 1px var(--navy);
}

/* 卡片容器：极淡边框 + 轻微悬浮，无重阴影 */
[data-testid="stVerticalBlockBorderWrapper"]{
  border-radius:10px;
}
div[data-testid="stContainer"]:has(>div){border-color:var(--line);}

/* 提示框：去高饱和，统一成低调中性条 */
[data-testid="stAlert"]{
  border-radius:8px;
  border:1px solid var(--line);
  box-shadow:none;
}

/* expander：扁平 */
[data-testid="stExpander"]{
  border:1px solid var(--line); border-radius:8px;
}
[data-testid="stExpander"] summary{font-weight:500;}

/* metric：紧凑商务 */
[data-testid="stMetricValue"]{color:var(--navy); font-weight:700;}

/* 链接/page_link：低调，hover 深蓝 */
[data-testid="stPageLink"] a{color:var(--navy); font-weight:500;}

/* 代码块 */
.stCodeBlock{border-radius:8px;}

/* 对话气泡：克制留白、细边、用户与助手区分 */
[data-testid="stChatMessage"]{
  background:transparent;
  padding:.4rem .2rem;
}
[data-testid="stChatMessageContent"]{
  border-radius:10px;
}
/* 底部对话输入框：聚焦深蓝 */
[data-testid="stChatInput"] textarea:focus{
  border-color:var(--navy);
}
[data-testid="stChatInput"]{
  border-color:var(--line);
}
/* 示例/快捷按钮：做成轻量胶囊，hover 描深蓝边 */
.stButton>button{font-size:.9rem;}

</style>
"""


def apply():
    """注入全局样式。在每个页面文件开头调用一次。"""
    st.markdown(_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    """统一的页面头部：标题 + 副标题 + 细分割线。无 emoji。"""
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)
    st.markdown("<hr>", unsafe_allow_html=True)
