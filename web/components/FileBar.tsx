"use client";

import { useState } from "react";
import * as Icons from "lucide-react";
import { extractPdf, buildPdfContext } from "@/lib/pdf";
import { parseCsv, buildCsvContext, type CsvData } from "@/lib/csv";

// PDF/CSV 上传与解析。解析完把上下文回传给父组件注入对话。
export function FileBar({
  kind,
  onContext,
}: {
  kind: "pdf" | "csv";
  onContext: (ctx: string) => void;
}) {
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const [csv, setCsv] = useState<CsvData | null>(null);
  const [pages, setPages] = useState(0);

  async function onFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setBusy(true); setErr(""); setName(file.name); setCsv(null); setPages(0);
    try {
      if (kind === "pdf") {
        const pg = await extractPdf(file);
        setPages(pg.length);
        onContext(buildPdfContext(pg));
      } else {
        const data = await parseCsv(file);
        setCsv(data);
        onContext(buildCsvContext(data));
      }
    } catch (e: any) {
      setErr(e?.message || "解析失败");
      onContext("");
    } finally {
      setBusy(false);
    }
  }

  const accept = kind === "pdf" ? ".pdf" : ".csv";

  return (
    <div className="mx-auto max-w-chat mb-4">
      <label className="flex items-center gap-2 rounded-xl border border-dashed border-border bg-surface px-4 py-3 cursor-pointer hover:border-accent transition-colors">
        <Icons.Upload size={16} className="text-muted" />
        <span className="text-sm text-muted">
          {busy ? "解析中…" : name ? `已加载：${name}` : `点击上传 ${kind.toUpperCase()} 文件`}
        </span>
        <input type="file" accept={accept} onChange={onFile} className="hidden" />
      </label>

      {err && <div className="text-xs text-red-500 mt-1.5">{err}</div>}

      {kind === "pdf" && pages > 0 && (
        <div className="text-xs text-muted mt-1.5">
          已解析 {pages} 页，可在下方提问，回答会标注页码引用。
        </div>
      )}

      {kind === "csv" && csv && (
        <div className="mt-2 rounded-xl border border-border overflow-hidden">
          <div className="px-3 py-1.5 text-xs text-muted bg-surface border-b border-border">
            {csv.rowCount} 行 · {csv.headers.length} 列
          </div>
          <div className="overflow-x-auto max-h-72">
            <table className="text-xs w-full">
              <thead className="bg-surface sticky top-0">
                <tr>
                  {csv.headers.map((h, i) => (
                    <th key={i} className="px-2.5 py-1.5 text-left font-medium border-b border-border whitespace-nowrap">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {csv.rows.slice(0, 50).map((r, ri) => (
                  <tr key={ri} className="even:bg-bg/40">
                    {r.map((c, ci) => (
                      <td key={ci} className="px-2.5 py-1 border-b border-border/50 whitespace-nowrap">{c}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {csv.rowCount > 50 && (
            <div className="px-3 py-1.5 text-xs text-muted bg-surface border-t border-border">
              仅预览前 50 行
            </div>
          )}
        </div>
      )}
    </div>
  );
}
