"use client";

import { useState, useRef, useEffect } from "react";
import { useChat } from "ai/react";
import * as Icons from "lucide-react";
import { MODES, getMode } from "@/lib/modes";
import { PROVIDERS } from "@/lib/providers";
import { useSettings } from "@/lib/useSettings";
import { SettingsPanel } from "@/components/SettingsPanel";
import { MessageBubble } from "@/components/MessageBubble";
import { cn } from "@/lib/utils";

export default function Home() {
  const { settings, update, setKey, currentKey, loaded } = useSettings();
  const [modeId, setModeId] = useState("chat");
  const [showSettings, setShowSettings] = useState(false);
  const mode = getMode(modeId);
  const scrollRef = useRef<HTMLDivElement>(null);
  const hasKey = !!currentKey;

  const { messages, input, handleInputChange, handleSubmit, isLoading, setMessages, setInput, append, error } =
    useChat({
      api: "/api/chat",
      body: {
        system: mode.system,
        providerId: settings.providerId,
        model: settings.model || PROVIDERS[settings.providerId]?.models[0] || "",
        apiKey: currentKey,
      },
    });

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  // 切换模式时清空对话
  function switchMode(id: string) {
    setModeId(id);
    setMessages([]);
  }

  // 点示例：直接发送（没 key 则先打开设置）
  function submitExample(text: string) {
    if (!hasKey) {
      setShowSettings(true);
      return;
    }
    append({ role: "user", content: text });
  }

  // 表单提交：没 key 拦截并打开设置
  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;
    if (!hasKey) {
      setShowSettings(true);
      return;
    }
    handleSubmit(e);
  }

  return (
    <div className="flex h-screen">
      {/* 侧边栏：模式列表（工具入口） */}
      <aside className="w-60 shrink-0 border-r border-border bg-surface flex flex-col">
        <div className="px-4 py-4 font-semibold text-[15px]">智能助手</div>
        <nav className="flex-1 px-2 space-y-0.5 overflow-y-auto">
          {MODES.map((m) => {
            const Icon = (Icons as any)[m.icon] ?? Icons.Circle;
            return (
              <button
                key={m.id}
                onClick={() => switchMode(m.id)}
                className={cn(
                  "w-full flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm text-left transition-colors",
                  modeId === m.id ? "bg-bg text-ink font-medium" : "text-muted hover:bg-bg/60"
                )}
              >
                <Icon size={16} /> {m.label}
              </button>
            );
          })}
        </nav>
        <button
          onClick={() => setShowSettings(true)}
          className="m-2 flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm text-muted hover:bg-bg"
        >
          <Icons.Settings size={16} /> 设置
        </button>
      </aside>

      {/* 主区：对话 */}
      <main className="flex-1 flex flex-col">
        <header className="h-14 shrink-0 border-b border-border flex items-center justify-between px-5">
          <span className="font-medium">{mode.label}</span>
          {hasKey ? (
            <span className="text-xs text-muted">
              {PROVIDERS[settings.providerId]?.label} · {settings.model || PROVIDERS[settings.providerId]?.models[0]}
            </span>
          ) : (
            <button
              onClick={() => setShowSettings(true)}
              className="text-xs rounded-full bg-accent/10 text-accent px-3 py-1 font-medium hover:bg-accent/20"
            >
              未配置 API Key · 点此设置
            </button>
          )}
        </header>

        <div ref={scrollRef} className="flex-1 overflow-y-auto">
          <div className="mx-auto max-w-chat px-4 py-6 space-y-4">
            {messages.length === 0 ? (
              <EmptyState mode={mode} onPick={submitExample} hasKey={hasKey} onOpenSettings={() => setShowSettings(true)} />
            ) : (
              messages.map((m, i) => (
                <MessageBubble
                  key={m.id}
                  role={m.role}
                  content={m.content}
                  streaming={isLoading && i === messages.length - 1 && m.role === "assistant"}
                />
              ))
            )}
            {error && (
              <div className="rounded-xl border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
                <div className="font-medium mb-1">⚠ 调用出错</div>
                <div className="break-words">{error.message}</div>
                <div className="mt-1.5 text-red-600/80 text-xs">
                  常见原因：API Key 无效或额度不足、模型名不对、网络/端点不通。
                  可在「设置」检查 Key 和模型；智谱端点偶发 503，可重试。
                </div>
              </div>
            )}
          </div>
        </div>

        {/* 输入区 */}
        <div className="shrink-0 px-4 pb-5 pt-2">
          <form
            onSubmit={onSubmit}
            className="mx-auto max-w-chat flex items-end gap-2 rounded-2xl border border-border bg-surface p-2 shadow-sm focus-within:border-accent"
          >
            <textarea
              value={input}
              onChange={handleInputChange}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  onSubmit(e as any);
                }
              }}
              rows={1}
              placeholder={hasKey ? mode.placeholder : "请先在「设置」里填入 API Key…"}
              className="flex-1 resize-none bg-transparent px-2 py-1.5 outline-none text-[15px] max-h-40"
            />
            <button
              type="submit"
              disabled={isLoading}
              title={hasKey ? "发送" : "去设置 API Key"}
              className="rounded-xl bg-accent text-accent-fg p-2 disabled:opacity-40 transition-opacity"
            >
              <Icons.ArrowUp size={18} />
            </button>
          </form>
          <p className="mx-auto max-w-chat text-center text-xs text-muted mt-2">
            Enter 发送 · Shift+Enter 换行 · 切换左侧模式开启不同工具
          </p>
        </div>
      </main>

      {showSettings && loaded && (
        <SettingsPanel
          settings={settings}
          update={update}
          setKey={setKey}
          onClose={() => setShowSettings(false)}
        />
      )}
    </div>
  );
}

function EmptyState({
  mode,
  onPick,
  hasKey,
  onOpenSettings,
}: {
  mode: ReturnType<typeof getMode>;
  onPick: (t: string) => void;
  hasKey: boolean;
  onOpenSettings: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center text-center py-20">
      <h1 className="text-2xl font-semibold mb-2">{mode.label}</h1>
      <p className="text-muted mb-6 text-sm max-w-md">
        {hasKey
          ? "在下方输入，或点一个示例开始"
          : "先配置 API Key 才能使用真实模型"}
      </p>
      {!hasKey ? (
        <button
          onClick={onOpenSettings}
          className="rounded-xl bg-accent text-accent-fg px-4 py-2 text-sm"
        >
          去设置 API Key
        </button>
      ) : (
        <div className="flex flex-wrap gap-2 justify-center max-w-md">
          {mode.examples.map((ex) => (
            <button
              key={ex}
              onClick={() => onPick(ex)}
              className="rounded-full border border-border bg-surface px-3.5 py-1.5 text-sm text-muted hover:border-accent hover:text-ink transition-colors"
            >
              {ex}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
