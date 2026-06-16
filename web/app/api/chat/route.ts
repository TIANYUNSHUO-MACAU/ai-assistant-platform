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

  try {
    let modelInstance;
    if (cfg.sdk === "anthropic") {
      const anthropic = createAnthropic({ apiKey });
      modelInstance = anthropic(model || cfg.models[0]);
    } else {
      const openai = createOpenAI({
        apiKey,
        baseURL: cfg.baseURL,
      });
      modelInstance = openai(model || cfg.models[0]);
    }

    const result = streamText({
      model: modelInstance,
      system: system || "你是一个友好的中文 AI 助手。",
      messages,
      temperature: 0.7,
    });

    return result.toDataStreamResponse();
  } catch (e: any) {
    return new Response(
      JSON.stringify({ error: e?.message || "调用失败" }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}
