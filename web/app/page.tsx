"use client";

import { useState, useRef, useEffect } from "react";
import { useChat } from "ai/react";
import * as Icons from "lucide-react";
import { getMode } from "@/lib/modes";
import { PROVIDERS } from "@/lib/providers";
import { useSettings } from "@/lib/useSettings";
import { useSessions } from "@/lib/useSessions";
import { Sidebar } from "@/components/Sidebar";
import { SettingsPanel } from "@/components/SettingsPanel";
import { MessageBubble } from "@/components/MessageBubble";
import { FileBar } from "@/components/FileBar";

export default function Home() {
  const { settings, update, setKey, currentKey, loaded } = useSettings();
  const sess = useSessions();
  const [showSettings, setShowSettings] = useState(false);
  const [fileCtx, setFileCtx] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);
  const hasKey = !!currentKey;

  // 当前会话的模式（无会话时用通用对话）
  const modeId = sess.active?.modeId ?? "chat";
  const mode = getMode(modeId);

  // PDF/CSV 模式：把文件内容拼进 system，让模型基于文档回答
  const systemWithFile = fileCtx
    ? `${mode.system}\n\n以下是用户提供的文档内容：\n${fileCtx}`
    : mode.system;

  const {
    messages, input, handleInputChange, handleSubmit, isLoading,
    setMessages, append, error,
  } = useChat({
    api: "/api/chat",
    body: {
      system: systemWithFile,
      providerId: settings.providerId,
      model: settings.model || PROVIDERS[settings.providerId]?.models[0] || "",
      apiKey: currentKey,
    },
    onFinish: (msg) => {
      // 对话结束：把消息存回会话，并自动命名
      if (!sess.activeId) return;
      const all = [...messages, msg];
      const firstUser = all.find((m) => m.role === "user");
      const autoTitle = firstUser
        ? firstUser.content.slice(0, 20) + (firstUser.content.length > 20 ? "…" : "")
        : "新对话";
      sess.updateSession(sess.activeId, {
        messages: all,
        title: sess.active?.title === "新对话" ? autoTitle : sess.active?.title,
      });
    },
  });

  // 切换会话时，加载该会话的消息到 useChat
  useEffect(() => {
    setMessages(sess.active?.messages ?? []);
    setFileCtx(""); // 换会话清空已加载文件
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sess.activeId]);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  function ensureSession(): string {
    if (sess.activeId) return sess.activeId;
    return sess.newSession(modeId);
  }

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;
    if (!hasKey) { setShowSettings(true); return; }
    ensureSession();
    handleSubmit(e);
  }

  function submitExample(text: string) {
    if (!hasKey) { setShowSettings(true); return; }
    ensureSession();
    append({ role: "user", content: text });
  }

  // 在已有会话里切模式：更新当前会话模式并清空
  function pickMode(id: string) {
    if (sess.activeId) {
      sess.updateSession(sess.activeId, { modeId: id, messages: [], title: "新对话" });
      setMessages([]);
    } else {
      sess.newSession(id);
    }
  }

  return (
    <div className="flex h-screen">
      {loaded && sess.loaded && (
        <Sidebar
          sessions={sess.sessions}
          activeId={sess.activeId}
          modeId={modeId}
          onPickMode={pickMode}
          onNew={() => sess.newSession(modeId)}
          onSelect={sess.setActiveId}
          onDelete={sess.deleteSession}
          onRename={sess.renameSession}
          onOpenSettings={() => setShowSettings(true)}
        />
      )}

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
            {(mode.kind === "pdf" || mode.kind === "csv") && (
              <FileBar kind={mode.kind} onContext={setFileCtx} />
            )}
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
                  常见原因：API Key 无效或额度不足、模型名不对、网络/端点不通。可在「设置」检查。
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="shrink-0 px-4 pb-5 pt-2">
          <form
            onSubmit={onSubmit}
            className="mx-auto max-w-chat flex items-end gap-2 rounded-2xl border border-border bg-surface p-2 shadow-sm focus-within:border-accent"
          >
            <textarea
              value={input}
              onChange={handleInputChange}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); onSubmit(e as any); }
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
            Enter 发送 · Shift+Enter 换行 · 左侧切换工具模式 / 管理历史对话
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
  mode, onPick, hasKey, onOpenSettings,
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
        {hasKey ? "在下方输入，或点一个示例开始" : "先配置 API Key 才能使用真实模型"}
      </p>
      {!hasKey ? (
        <button onClick={onOpenSettings} className="rounded-xl bg-accent text-accent-fg px-4 py-2 text-sm">
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
