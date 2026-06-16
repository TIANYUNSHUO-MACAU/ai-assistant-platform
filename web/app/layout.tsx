import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "智能助手",
  description: "多功能 AI 助手 · 多模型 BYOK",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
      <body suppressHydrationWarning>{children}</body>
    </html>
  );
}
