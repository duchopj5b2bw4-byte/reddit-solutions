# Cloudflare Pages 一键部署指南

## 1. 登录 Cloudflare Dashboard
打开 https://dash.cloudflare.com

## 2. 进入 Pages → 创建项目
点击左侧 "Workers & Pages" → "Pages" → "创建" → "连接到 Git"

## 3. 选择仓库
选择 `duchopj5b2bw4-byte/reddit-solutions`

## 4. 配置构建
- 项目名称：`reddit-solutions`
- 生产分支：`master`
- 构建命令：**留空**
- 构建输出目录：`.` (一个点)
- 根目录：**留空**

## 5. 点击 "保存并部署"
等待约 30 秒部署完成。

## 6. 完成！
你的站点将在 `https://reddit-solutions.pages.dev` 上线。
之后每次 `git push` 到 master 都会自动重新部署。
