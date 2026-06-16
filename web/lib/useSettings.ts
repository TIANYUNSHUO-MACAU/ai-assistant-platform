"use client";

import { useState, useEffect, useCallback } from "react";
import { DEFAULT_PROVIDER } from "./providers";

// BYOK 配置存 localStorage：providerId / model / 各 provider 的 key
// key 仅存在用户本地浏览器，不上传服务器。

export type Settings = {
  providerId: string;
  model: string;
  keys: Record<string, string>; // providerId -> apiKey
  models: Record<string, string>; // providerId -> 选中/自定义的模型名
  dark: boolean;
  // 「自定义」提供商专用
  customBaseURL: string;
  customSdk: "openai" | "anthropic";
};

const STORAGE_KEY = "ai-assistant-settings";

const DEFAULTS: Settings = {
  providerId: DEFAULT_PROVIDER,
  model: "",
  keys: {},
  models: {},
  dark: false,
  customBaseURL: "",
  customSdk: "openai",
};

export function useSettings() {
  const [settings, setSettings] = useState<Settings>(DEFAULTS);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) setSettings({ ...DEFAULTS, ...JSON.parse(raw) });
    } catch {}
    setLoaded(true);
  }, []);

  useEffect(() => {
    if (!loaded) return;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
    } catch {}
    document.documentElement.classList.toggle("dark", settings.dark);
  }, [settings, loaded]);

  const update = useCallback((patch: Partial<Settings>) => {
    setSettings((s) => ({ ...s, ...patch }));
  }, []);

  const setKey = useCallback((providerId: string, key: string) => {
    setSettings((s) => ({ ...s, keys: { ...s.keys, [providerId]: key } }));
  }, []);

  // 每个 provider 记住各自选中的模型
  const setModel = useCallback((providerId: string, model: string) => {
    setSettings((s) => ({ ...s, models: { ...s.models, [providerId]: model } }));
  }, []);

  const currentKey = settings.keys[settings.providerId] || "";
  const currentModel = settings.models[settings.providerId] || "";

  return { settings, update, setKey, setModel, currentKey, currentModel, loaded };
}
