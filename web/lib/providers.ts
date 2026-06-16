// 多提供商配置（对应 Python 版 llm_client.PROVIDERS）
// Claude 走 anthropic，其余走 openai 兼容接口。

export type Provider = {
  label: string;
  sdk: "openai" | "anthropic";
  baseURL?: string;
  models: string[];
  keyURL: string;
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
    models: ["gpt-4o", "gpt-4o-mini", "gpt-4.1", "o4-mini"],
    keyURL: "https://platform.openai.com/api-keys",
  },
  anthropic: {
    label: "Claude",
    sdk: "anthropic",
    models: ["claude-sonnet-4-5", "claude-3-5-sonnet-latest", "claude-3-5-haiku-latest"],
    keyURL: "https://console.anthropic.com/settings/keys",
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
    models: ["qwen-plus", "qwen-turbo", "qwen-max"],
    keyURL: "https://bailian.console.aliyun.com/",
  },
  kimi: {
    label: "Kimi",
    sdk: "openai",
    baseURL: "https://api.moonshot.cn/v1",
    models: ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"],
    keyURL: "https://platform.moonshot.cn/console/api-keys",
  },
};

export const DEFAULT_PROVIDER = "zhipu";
