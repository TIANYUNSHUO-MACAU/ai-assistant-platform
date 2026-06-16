/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // 锁定文件追踪根目录为本项目，避免多 lockfile 误判
  outputFileTracingRoot: __dirname,
};

module.exports = nextConfig;
