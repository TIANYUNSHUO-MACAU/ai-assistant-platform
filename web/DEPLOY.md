# 部署到 Vercel（图文步骤）

本项目是 monorepo：仓库根目录是旧的 Streamlit 版，**Next.js 新版在 `web/` 子目录**。
所以部署时最关键的一步是把 **Root Directory 设成 `web`**。

## 一、前置

- 代码已推到 GitHub：`TIANYUNSHUO-MACAU/ai-assistant-platform`
- 准备好梯子（Vercel 是海外服务）

## 二、Dashboard 部署（推荐，全程网页点击）

1. 打开 https://vercel.com → 点 **Sign Up / Log In** → 选 **Continue with GitHub**，授权登录。

2. 进入后点 **Add New…** → **Project**。

3. 在仓库列表里找到 **ai-assistant-platform** → 点 **Import**。
   （首次使用要先点 *Install* 授权 Vercel 访问你的 GitHub 仓库）

4. **关键一步——配置 Root Directory：**
   - 找到 **Root Directory** 一栏，点 **Edit**
   - 选择 / 输入 **`web`**
   - 选对后，Vercel 会自动识别为 Next.js 项目（Framework Preset 显示 Next.js）

5. 其余保持默认：
   - Build Command：`next build`（自动）
   - Output：自动
   - **Environment Variables：留空**（本项目是 BYOK，密钥由用户在前端填，服务端不需要任何环境变量）

6. 点 **Deploy**，等 1–3 分钟。

7. 部署完成后会给一个网址，形如：
   `https://ai-assistant-platform-xxxx.vercel.app`
   点 **Visit** 打开。

## 三、上线后自测

1. 打开网址，进入对话界面。
2. 右上角「未配置 API Key · 点此设置」→ 填一个 Key 测试。
3. **重要**：Vercel 在海外，调智谱国内端点（open.bigmodel.cn）可能不稳。
   - 若智谱报超时/连接错误 → 改用 **Gemini / DeepSeek / OpenAI / Claude** 等海外可达的提供商
   - 或用「自定义」提供商接一个海外可达的端点

## 四、以后更新

只要 `git push` 到 main，Vercel 会**自动重新部署**，无需手动操作。

## 备选：CLI 部署

若想用命令行：
```bash
npm i -g vercel
cd web
vercel        # 首次会让你登录 + 关联项目，按提示选 web 为根目录
vercel --prod # 部署到生产
```
