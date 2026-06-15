# 多功能智能助手平台

零基础项目实训 Demo（6/1 - 6/5）。一个网页入口，集成多个简单 AI 小工具。
框架：**Streamlit**。

## 功能

| 工具 | 说明 | 是否需要联网/API |
|------|------|------------------|
| ✍️ 文案生成 | 输入场景，生成多风格短文案 | 需要 |
| 🌐 翻译助手 | 中英互译，自动判断方向 | 需要 |
| 📄 简历优化 | 输入简历片段，输出诊断与优化 | 需要 |
| 📊 CSV 预览 | 上传表格，自动统计说明 | **不需要（纯本地）** |

> 双模式设计：未配置 API key 时，AI 工具自动返回「模拟结果」，流程依然可完整演示；
> 配置 key 后自动切换为真实模型调用。**API 不通绝不会让 Demo 崩溃。**

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API key（可选，不配也能跑）

复制 `.env.example` 为 `.env`，填入你的 key：

```
ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
ANTHROPIC_AUTH_TOKEN=你的智谱key
LLM_MODEL=glm-4.6
```

> 本项目使用智谱 GLM 的 Anthropic 兼容端点。`.env` 已被 `.gitignore` 忽略，不会提交到仓库。

### 3. 启动

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`，左侧边栏可切换各个工具。

## 项目结构

```
.
├── app.py              # 主入口页面
├── llm_client.py       # LLM 客户端（真实/模拟双模式）
├── prompts.py          # 提示词集合（可复用）
├── pages/              # 各工具页面（Streamlit 自动识别）
│   ├── 1_✍️_文案生成.py
│   ├── 2_🌐_翻译助手.py
│   ├── 3_📄_简历优化.py
│   └── 4_📊_CSV预览.py
├── requirements.txt
├── .env.example        # 配置模板
├── 框架选型说明.md
└── 测试清单.md
```

## 常见问题

- **没装 Python？** 需要 Python 3.10+，命令行运行 `python --version` 检查。
- **AI 工具显示"模拟返回"？** 说明没配 key 或 key 无效，属正常兜底。配好 `.env` 重启即可。
- **CSV 中文乱码？** 工具已自动尝试 utf-8 和 gbk 两种编码。
