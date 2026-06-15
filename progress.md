# 项目进度：多功能智能助手平台（Streamlit）

> 一周实训交付物。框架：Streamlit。LLM：智谱 GLM（Anthropic 兼容端点），双模式（真实 API + mock 兜底）。

## 任务清单

- [x] 1. 项目骨架 + Git 初始化 + .gitignore
- [x] 2. LLM 客户端（双模式：智谱真实调用 / mock 兜底，含503重试）
- [x] 3. 主入口页面 app.py（菜单 + 首页说明）
- [x] 4. 工具：文案生成
- [x] 5. 工具：翻译助手
- [x] 6. 工具：简历优化
- [x] 7. 工具：CSV 预览（纯本地，不依赖 API）
- [x] 8. 提示词集合 prompts.py
- [x] 9. requirements.txt
- [x] 10. README.md（安装/运行/功能说明）
- [x] 11. 框架选型说明.md
- [x] 12. 测试清单.md（验收逐项打勾）
- [x] 13. 实测 API 跑通 + 本地启动验证（HTTP 200，4页面识别正常）

## 全部完成 ✅

- 启动命令：`streamlit run app.py`
- 真实模型：智谱 glm-4.6（曾成功返回；端点偶发503，已由双模式自动兜底）
- 待办（可选）：端点稳定时复测真实输出；push 到远程仓库

## 关键决策

- 4 个工具：文案生成、翻译助手、简历优化、CSV 预览
- CSV 预览为"保命功能"，无网无 key 也能演示
- API key 放 .env，不进 git
- 智谱端点：https://open.bigmodel.cn/api/anthropic ，模型名实测后确定
