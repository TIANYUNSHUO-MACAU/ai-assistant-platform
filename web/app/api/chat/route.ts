import { streamText } from "ai";
import { createOpenAI } from "@ai-sdk/openai";
import { createAnthropic } from "@ai-sdk/anthropic";
import { PROVIDERS } from "@/lib/providers";

export const runtime = "edge";

// 接收前端消息 + BYOK 配置，按 provider 路由后流式返回。
// API Key 来自请求头（前端 localStorage），服务端不持久化。
export async function POST(req: Request) {
  const { messages, system, providerId, model, apiKey } = await req.json();

  if (!apiKey) {
    return new Response(
      JSON.stringify({ error: "未配置 API Key，请在设置中填入。" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  const cfg = PROVIDERS[providerId] ?? PROVIDERS.zhipu;
  const modelId = model || cfg.models[0]; // 兜底用该 provider 第一个模型

  try {
    let modelInstance;
    if (cfg.sdk === "anthropic") {
      const anthropic = createAnthropic({ apiKey });
      modelInstance = anthropic(modelId);
    } else {
      const openai = createOpenAI({ apiKey, baseURL: cfg.baseURL });
      modelInstance = openai(modelId);
    }

    const result = streamText({
      model: modelInstance,
      system: system || "你是一个友好的中文 AI 助手。",
      messages,
      temperature: 0.7,
      // 把真实错误透传给前端，方便定位（key 无效/模型名错/网络等）
      onError: ({ error }) => {
        console.error("[chat] stream error:", error);
      },
    });

    return result.toDataStreamResponse({
      getErrorMessage: (error) => {
        const msg = error instanceof Error ? error.message : String(error);
        return `调用失败（${cfg.label} / ${modelId}）：${msg}`;
      },
    });
  } catch (e: any) {
    return new Response(
      JSON.stringify({ error: `调用失败（${cfg.label} / ${modelId}）：${e?.message || e}` }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}
