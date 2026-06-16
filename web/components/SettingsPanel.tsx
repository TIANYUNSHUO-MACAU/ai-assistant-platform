"use client";

import { PROVIDERS } from "@/lib/providers";
import { Settings } from "@/lib/useSettings";
import { X, Moon, Sun, ExternalLink } from "lucide-react";

export function SettingsPanel({
  settings,
  update,
  setKey,
  onClose,
}: {
  settings: Settings;
  update: (p: Partial<Settings>) => void;
  setKey: (provider: string, key: string) => void;
  onClose: () => void;
}) {
  const cfg = PROVIDERS[settings.providerId];
  const models = cfg?.models ?? [];

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-md rounded-2xl bg-surface border border-border shadow-xl p-6"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-5">
          <h2 className="text-lg font-semibold">设置</h2>
          <button onClick={onClose} className="text-muted hover:text-ink">
            <X size={20} />
          </button>
        </div>

        {/* 提供商 */}
        <label className="block text-sm font-medium mb-1.5">AI 提供商</label>
        <select
          value={settings.providerId}
          onChange={(e) => update({ providerId: e.target.value, model: "" })}
          className="w-full rounded-lg border border-border bg-bg px-3 py-2 mb-4 outline-none focus:border-accent"
        >
          {Object.entries(PROVIDERS).map(([id, p]) => (
            <option key={id} value={id}>{p.label}</option>
          ))}
        </select>

        {/* API Key */}
        <label className="block text-sm font-medium mb-1.5">
          {cfg?.label} API Key
        </label>
        <input
          type="password"
          value={settings.keys[settings.providerId] || ""}
          onChange={(e) => setKey(settings.providerId, e.target.value)}
          placeholder="粘贴你的 API Key…"
          className="w-full rounded-lg border border-border bg-bg px-3 py-2 mb-1.5 outline-none focus:border-accent"
        />
        <a
          href={cfg?.keyURL}
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-1 text-xs text-muted hover:text-accent mb-4"
        >
          没有 Key？去申请 <ExternalLink size={12} />
        </a>

        {/* 模型 */}
        <label className="block text-sm font-medium mb-1.5">模型</label>
        <select
          value={settings.model || models[0]}
          onChange={(e) => update({ model: e.target.value })}
          className="w-full rounded-lg border border-border bg-bg px-3 py-2 mb-5 outline-none focus:border-accent"
        >
          {models.map((m) => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>

        {/* 主题 + 提示 */}
        <div className="flex items-center justify-between pt-4 border-t border-border">
          <span className="text-xs text-muted">
            Key 仅存于本机浏览器，不上传服务器
          </span>
          <button
            onClick={() => update({ dark: !settings.dark })}
            className="flex items-center gap-1.5 text-sm rounded-lg px-3 py-1.5 hover:bg-bg"
          >
            {settings.dark ? <Sun size={16} /> : <Moon size={16} />}
            {settings.dark ? "浅色" : "深色"}
          </button>
        </div>
      </div>
    </div>
  );
}
