# 项目进度：多功能智能助手平台（Streamlit）

> 一周实训交付物。框架：Streamlit。LLM：智谱 GLM（Anthropic 兼容端点），双模式（真实 API + mock 兜底）。

## 任务清单

- [ ] 1. 项目骨架 + Git 初始化 + .gitignore
- [ ] 2. LLM 客户端（双模式：智谱真实调用 / mock 兜底）
- [ ] 3. 主入口页面 app.py（菜单 + 首页说明）
- [ ] 4. 工具：文案生成
- [ ] 5. 工具：翻译助手
- [ ] 6. 工具：简历优化
- [ ] 7. 工具：CSV 预览（纯本地，不依赖 API）
- [ ] 8. 提示词集合 prompts/
- [ ] 9. requirements.txt
- [ ] 10. README.md（安装/运行/功能说明）
- [ ] 11. 框架选型说明.md
- [ ] 12. 测试清单.md（验收逐项打勾）
- [ ] 13. 实测 API 跑通 + 本地启动验证

## 关键决策

- 4 个工具：文案生成、翻译助手、简历优化、CSV 预览
- CSV 预览为"保命功能"，无网无 key 也能演示
- API key 放 .env，不进 git
- 智谱端点：https://open.bigmodel.cn/api/anthropic ，模型名实测后确定
