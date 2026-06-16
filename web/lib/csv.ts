"use client";

import Papa from "papaparse";

export type CsvData = {
  headers: string[];
  rows: string[][];
  rowCount: number;
};

export function parseCsv(file: File): Promise<CsvData> {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      skipEmptyLines: true,
      complete: (res) => {
        const data = res.data as string[][];
        if (!data.length) return reject(new Error("空文件"));
        const [headers, ...rows] = data;
        resolve({ headers, rows, rowCount: rows.length });
      },
      error: (err) => reject(err),
    });
  });
}

// 把 CSV 概要 + 前若干行拼成模型上下文
export function buildCsvContext(csv: CsvData, sampleRows = 20): string {
  const head = csv.headers.join(" | ");
  const sample = csv.rows
    .slice(0, sampleRows)
    .map((r) => r.join(" | "))
    .join("\n");
  return `表格共 ${csv.rowCount} 行，${csv.headers.length} 列。\n列名：${head}\n\n前 ${Math.min(sampleRows, csv.rowCount)} 行：\n${sample}`;
}
