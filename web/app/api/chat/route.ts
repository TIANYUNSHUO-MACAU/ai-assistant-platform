import { streamText } from "ai";
import { createOpenAI } from "@ai-sdk/openai";
import { createAnthropic } from "@ai-sdk/anthropic";
import { PROVIDERS } from "@/lib/providers";

export const runtime = "nodejs";

// 接收前端消息 + BYOK 配置，按 provider 路由后流式返回。
// API Key 来自请求体（前端 localStorage），服务端不持久化。
// 自定义提供商：baseURL/sdk 由前端传入（customBaseURL / customSdk）。
export async function POST(req: Request) {
  const { messages, system, providerId, model, apiKey, customBaseURL, customSdk } =
    await req.json();

  if (!apiKey) {
    return new Response(
      JSON.stringify({ error: "未配置 API Key，请在设置中填入。" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  const cfg = PROVIDERS[providerId] ?? PROVIDERS.zhipu;
  const isCustom = !!cfg.custom;

  // 解析 sdk / baseURL / 模型（自定义提供商用前端传入值）
  const sdk: "openai" | "anthropic" = isCustom ? (customSdk || "openai") : cfg.sdk;
  const baseURL = isCustom ? customBaseURL : cfg.baseURL;
  const modelId = model || cfg.models[0] || "";
  const label = isCustom ? "自定义" : cfg.label;

  if (isCustom && !baseURL) {
    return new Response(
      JSON.stringify({ error: "自定义提供商需填写 Base URL。" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }
  if (!modelId) {
    return new Response(
      JSON.stringify({ error: "请填写模型名。" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  try {
    let modelInstance;
    if (sdk === "anthropic") {
      const anthropic = createAnthropic({
        apiKey,
        ...(baseURL ? { baseURL } : {}),
      });
      modelInstance = anthropic(modelId);
    } else {
      const openai = createOpenAI({ apiKey, ...(baseURL ? { baseURL } : {}) });
      modelInstance = openai(modelId);
    }

    const result = streamText({
      model: modelInstance,
      system: system || "你是一个友好的中文 AI 助手。",
      messages,
      temperature: 0.7,
      onError: ({ error }) => {
        console.error("[chat] stream error:", error);
      },
    });

    return result.toDataStreamResponse({
      getErrorMessage: (error) => {
        const msg = error instanceof Error ? error.message : String(error);
        return `调用失败（${label} / ${modelId}）：${msg}`;
      },
    });
  } catch (e: any) {
    return new Response(
      JSON.stringify({ error: `调用失败（${label} / ${modelId}）：${e?.message || e}` }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}
