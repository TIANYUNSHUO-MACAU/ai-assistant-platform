"use client";

// 浏览器端 PDF 文本抽取，按页标记，便于回答时引用页码。
// 用 pdfjs-dist，worker 走 CDN 避免打包配置复杂度。

export type PdfPage = { page: number; text: string };

export async function extractPdf(file: File): Promise<PdfPage[]> {
  const pdfjs = await import("pdfjs-dist");
  // 配置 worker（与已安装版本一致）
  pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.mjs`;

  const buf = await file.arrayBuffer();
  const doc = await pdfjs.getDocument({ data: buf }).promise;
  const pages: PdfPage[] = [];

  for (let i = 1; i <= doc.numPages; i++) {
    const page = await doc.getPage(i);
    const content = await page.getTextContent();
    const text = content.items
      .map((it: any) => ("str" in it ? it.str : ""))
      .join(" ")
      .replace(/\s+/g, " ")
      .trim();
    pages.push({ page: i, text });
  }
  return pages;
}

// 把分页文本拼成带页码标记的上下文，控制总长度避免超 token。
export function buildPdfContext(pages: PdfPage[], maxChars = 12000): string {
  const blocks = pages
    .filter((p) => p.text)
    .map((p) => `【第 ${p.page} 页】\n${p.text}`);
  let ctx = blocks.join("\n\n");
  if (ctx.length > maxChars) ctx = ctx.slice(0, maxChars) + "\n…（内容过长已截断）";
  return ctx;
}
