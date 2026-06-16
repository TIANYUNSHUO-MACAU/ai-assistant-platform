"use client";

import { useState } from "react";
import * as Icons from "lucide-react";
import { MODES } from "@/lib/modes";
import type { Session } from "@/lib/useSessions";
import { cn } from "@/lib/utils";

export function Sidebar({
  sessions,
  activeId,
  modeId,
  onPickMode,
  onNew,
  onSelect,
  onDelete,
  onRename,
  onOpenSettings,
}: {
  sessions: Session[];
  activeId: string;
  modeId: string;
  onPickMode: (id: string) => void;
  onNew: () => void;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
  onRename: (id: string, title: string) => void;
  onOpenSettings: () => void;
}) {
  const [editing, setEditing] = useState<string>("");
  const [draft, setDraft] = useState("");

  function startRename(s: Session) {
    setEditing(s.id);
    setDraft(s.title);
  }
  function commitRename() {
    if (editing && draft.trim()) onRename(editing, draft.trim());
    setEditing("");
  }

  return (
    <aside className="w-64 shrink-0 border-r border-border bg-surface flex flex-col">
      <div className="px-3 py-3">
        <div className="px-1 pb-3 font-semibold text-[15px]">智能助手</div>

        {/* 模式选择 */}
        <label className="block text-[11px] text-muted px-1 mb-1">工具模式</label>
        <select
          value={modeId}
          onChange={(e) => onPickMode(e.target.value)}
          className="w-full rounded-lg border border-border bg-bg px-2.5 py-1.5 text-sm mb-2 outline-none focus:border-accent"
        >
          {MODES.map((m) => (
            <option key={m.id} value={m.id}>{m.label}</option>
          ))}
        </select>

        {/* 新建对话 */}
        <button
          onClick={onNew}
          className="w-full flex items-center justify-center gap-1.5 rounded-lg bg-accent text-accent-fg py-2 text-sm font-medium hover:opacity-90"
        >
          <Icons.Plus size={16} /> 新对话
        </button>
      </div>

      {/* 历史会话 */}
      <div className="flex-1 overflow-y-auto px-2">
        <div className="text-[11px] text-muted px-2 py-1">历史对话</div>
        {sessions.length === 0 ? (
          <div className="text-xs text-muted px-2 py-3">还没有对话，点上方「新对话」开始</div>
        ) : (
          sessions.map((s) => {
            const Mode = MODES.find((m) => m.id === s.modeId);
            return (
              <div
                key={s.id}
                onClick={() => onSelect(s.id)}
                className={cn(
                  "group flex items-center gap-2 rounded-lg px-2.5 py-2 text-sm cursor-pointer mb-0.5",
                  s.id === activeId ? "bg-bg text-ink" : "text-muted hover:bg-bg/60"
                )}
              >
                <Icons.MessageSquare size={14} className="shrink-0" />
                {editing === s.id ? (
                  <input
                    autoFocus
                    value={draft}
                    onChange={(e) => setDraft(e.target.value)}
                    onBlur={commitRename}
                    onKeyDown={(e) => e.key === "Enter" && commitRename()}
                    onClick={(e) => e.stopPropagation()}
                    className="flex-1 bg-transparent outline-none border-b border-accent"
                  />
                ) : (
                  <span className="flex-1 truncate">{s.title}</span>
                )}
                <button
                  onClick={(e) => { e.stopPropagation(); startRename(s); }}
                  className="opacity-0 group-hover:opacity-100 text-muted hover:text-ink"
                  title="重命名"
                >
                  <Icons.Pencil size={13} />
                </button>
                <button
                  onClick={(e) => { e.stopPropagation(); onDelete(s.id); }}
                  className="opacity-0 group-hover:opacity-100 text-muted hover:text-red-500"
                  title="删除"
                >
                  <Icons.Trash2 size={13} />
                </button>
              </div>
            );
          })
        )}
      </div>

      <button
        onClick={onOpenSettings}
        className="m-2 flex items-center gap-2.5 rounded-lg px-3 py-2 text-sm text-muted hover:bg-bg"
      >
        <Icons.Settings size={16} /> 设置
      </button>
    </aside>
  );
}
