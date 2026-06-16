"use client";

import { useState, useEffect, useCallback } from "react";
import type { Message } from "ai";

// 会话存 localStorage：每个会话含 id/标题/模式/消息列表/时间。
// 像 Claude 那样多会话切换、重命名、删除。

export type Session = {
  id: string;
  title: string;
  modeId: string;
  messages: Message[];
  updatedAt: number;
};

const STORAGE_KEY = "ai-assistant-sessions";

function genId() {
  return `s_${Date.now().toString(36)}_${Math.floor(Math.random() * 1e6).toString(36)}`;
}

export function useSessions() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeId, setActiveId] = useState<string>("");
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw) as Session[];
        setSessions(parsed);
        if (parsed.length) setActiveId(parsed[0].id);
      }
    } catch {}
    setLoaded(true);
  }, []);

  useEffect(() => {
    if (!loaded) return;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sessions));
    } catch {}
  }, [sessions, loaded]);

  const active = sessions.find((s) => s.id === activeId) ?? null;

  const newSession = useCallback((modeId: string) => {
    const s: Session = {
      id: genId(),
      title: "新对话",
      modeId,
      messages: [],
      updatedAt: Date.now(),
    };
    setSessions((prev) => [s, ...prev]);
    setActiveId(s.id);
    return s.id;
  }, []);

  const updateSession = useCallback((id: string, patch: Partial<Session>) => {
    setSessions((prev) =>
      prev.map((s) => (s.id === id ? { ...s, ...patch, updatedAt: Date.now() } : s))
    );
  }, []);

  const deleteSession = useCallback(
    (id: string) => {
      setSessions((prev) => {
        const next = prev.filter((s) => s.id !== id);
        if (id === activeId) setActiveId(next[0]?.id ?? "");
        return next;
      });
    },
    [activeId]
  );

  const renameSession = useCallback((id: string, title: string) => {
    setSessions((prev) => prev.map((s) => (s.id === id ? { ...s, title } : s)));
  }, []);

  return {
    sessions,
    active,
    activeId,
    setActiveId,
    newSession,
    updateSession,
    deleteSession,
    renameSession,
    loaded,
  };
}
