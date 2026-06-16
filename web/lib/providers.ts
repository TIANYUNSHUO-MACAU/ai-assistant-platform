// 多提供商配置（对应 Python 版 llm_client.PROVIDERS）
// sdk: openai 兼容 / anthropic 兼容。custom 提供商由用户自填 URL/Key/模型。
//
// 注意：模型 ID 更新很快，预置列表仅为常用快捷项，可能过时。
// 每家都支持「自定义模型…」手填，永远能用最新模型。

export type Provider = {
  label: string;
  sdk: "openai" | "anthropic";
  baseURL?: string;
  models: string[];
  keyURL: string;
  custom?: boolean; // true = 用户自填 URL/Key/模型
};

export const PROVIDERS: Record<string, Provider> = {
  zhipu: {
    label: "智谱 GLM",
    sdk: "anthropic",
    baseURL: "https://open.bigmodel.cn/api/anthropic/v1",
    models: ["glm-4.6", "glm-4.5", "glm-4-plus", "glm-4-flash"],
    keyURL: "https://open.bigmodel.cn/usercenter/apikeys",
  },
  openai: {
    label: "OpenAI",
    sdk: "openai",
    models: ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-mini", "o3", "o4-mini"],
    keyURL: "https://platform.openai.com/api-keys",
  },
  anthropic: {
    label: "Claude",
    sdk: "anthropic",
    models: [
      "claude-sonnet-4-5",
      "claude-opus-4-1",
      "claude-3-5-sonnet-latest",
      "claude-3-5-haiku-latest",
    ],
    keyURL: "https://console.anthropic.com/settings/keys",
  },
  gemini: {
    label: "Gemini",
    sdk: "openai", // Google 的 OpenAI 兼容端点
    baseURL: "https://generativelanguage.googleapis.com/v1beta/openai",
    models: ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"],
    keyURL: "https://aistudio.google.com/app/apikey",
  },
  deepseek: {
    label: "DeepSeek",
    sdk: "openai",
    baseURL: "https://api.deepseek.com",
    models: ["deepseek-chat", "deepseek-reasoner"],
    keyURL: "https://platform.deepseek.com/api_keys",
  },
  qwen: {
    label: "千问 Qwen",
    sdk: "openai",
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    models: ["qwen-max", "qwen-plus", "qwen-turbo", "qwen3-max"],
    keyURL: "https://bailian.console.aliyun.com/",
  },
  kimi: {
    label: "Kimi",
    sdk: "openai",
    baseURL: "https://api.moonshot.cn/v1",
    models: ["kimi-k2-0905-preview", "moonshot-v1-128k", "moonshot-v1-32k", "moonshot-v1-8k"],
    keyURL: "https://platform.moonshot.cn/console/api-keys",
  },
  custom: {
    label: "自定义（自填 URL/Key/模型）",
    sdk: "openai",
    models: [],
    keyURL: "",
    custom: true,
  },
};

export const DEFAULT_PROVIDER = "zhipu";

// 自定义模型选项的标记值
export const CUSTOM_MODEL = "__custom__";
