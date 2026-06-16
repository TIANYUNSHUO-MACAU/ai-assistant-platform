"use client";

import { useState, useEffect, useCallback } from "react";
import { DEFAULT_PROVIDER } from "./providers";

// BYOK 配置存 localStorage：providerId / model / 各 provider 的 key
// key 仅存在用户本地浏览器，不上传服务器。

export type Settings = {
  providerId: string;
  model: string;
  keys: Record<string, string>; // providerId -> apiKey
  dark: boolean;
};

const STORAGE_KEY = "ai-assistant-settings";

const DEFAULTS: Settings = {
  providerId: DEFAULT_PROVIDER,
  model: "",
  keys: {},
  dark: false,
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

  const currentKey = settings.keys[settings.providerId] || "";

  return { settings, update, setKey, currentKey, loaded };
}
