"use client";

import { PROVIDERS, CUSTOM_MODEL } from "@/lib/providers";
import { Settings } from "@/lib/useSettings";
import { X, Moon, Sun, ExternalLink } from "lucide-react";

export function SettingsPanel({
  settings,
  update,
  setKey,
  setModel,
  onClose,
}: {
  settings: Settings;
  update: (p: Partial<Settings>) => void;
  setKey: (provider: string, key: string) => void;
  setModel: (provider: string, model: string) => void;
  onClose: () => void;
}) {
  const cfg = PROVIDERS[settings.providerId];
  const isCustom = !!cfg?.custom;
  const models = cfg?.models ?? [];
  const savedModel = settings.models[settings.providerId] || "";

  // 当前模型是否走"自定义手填"：自定义提供商总是手填；
  // 其它提供商若选了 CUSTOM_MODEL 或填的值不在预置列表里，也算手填
  const usingCustomModel =
    isCustom || savedModel === CUSTOM_MODEL ||
    (!!savedModel && !models.includes(savedModel));

  const dropdownValue = usingCustomModel ? CUSTOM_MODEL : (savedModel || models[0] || "");

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-md max-h-[88vh] overflow-y-auto rounded-2xl bg-surface border border-border shadow-xl p-6"
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
          onChange={(e) => update({ providerId: e.target.value })}
          className="w-full rounded-lg border border-border bg-bg px-3 py-2 mb-4 outline-none focus:border-accent"
        >
          {Object.entries(PROVIDERS).map(([id, p]) => (
            <option key={id} value={id}>{p.label}</option>
          ))}
        </select>

        {/* 自定义提供商：Base URL + 协议 */}
        {isCustom && (
          <>
            <label className="block text-sm font-medium mb-1.5">Base URL</label>
            <input
              value={settings.customBaseURL}
              onChange={(e) => update({ customBaseURL: e.target.value })}
              placeholder="如 https://api.example.com/v1"
              className="w-full rounded-lg border border-border bg-bg px-3 py-2 mb-1 outline-none focus:border-accent"
            />
            <p className="text-xs text-muted mb-4">
              OpenAI 兼容填到 /v1；Anthropic 兼容填到 .../anthropic/v1
            </p>

            <label className="block text-sm font-medium mb-1.5">接口协议</label>
            <select
              value={settings.customSdk}
              onChange={(e) => update({ customSdk: e.target.value as "openai" | "anthropic" })}
              className="w-full rounded-lg border border-border bg-bg px-3 py-2 mb-4 outline-none focus:border-accent"
            >
              <option value="openai">OpenAI 兼容</option>
              <option value="anthropic">Anthropic 兼容</option>
            </select>
          </>
        )}

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
        {cfg?.keyURL && (
          <a
            href={cfg.keyURL}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 text-xs text-muted hover:text-accent mb-4"
          >
            没有 Key？去申请 <ExternalLink size={12} />
          </a>
        )}

        {/* 模型 */}
        <label className="block text-sm font-medium mb-1.5 mt-2">模型</label>
        {!isCustom && (
          <select
            value={dropdownValue}
            onChange={(e) => setModel(settings.providerId, e.target.value)}
            className="w-full rounded-lg border border-border bg-bg px-3 py-2 mb-2 outline-none focus:border-accent"
          >
            {models.map((m) => (
              <option key={m} value={m}>{m}</option>
            ))}
            <option value={CUSTOM_MODEL}>自定义模型…（手填最新型号）</option>
          </select>
        )}
        {usingCustomModel && (
          <input
            value={savedModel === CUSTOM_MODEL ? "" : savedModel}
            onChange={(e) => setModel(settings.providerId, e.target.value)}
            placeholder="手动输入模型名，如 glm-4.6 / gpt-4o / claude-sonnet-4-5"
            className="w-full rounded-lg border border-border bg-bg px-3 py-2 mb-1 outline-none focus:border-accent"
          />
        )}
        <p className="text-xs text-muted mb-5">
          模型 ID 以各家官方文档为准；预置列表可能过时，可随时用「自定义模型」手填最新型号。
        </p>

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
