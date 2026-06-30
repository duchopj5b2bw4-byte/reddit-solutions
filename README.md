# Reddit 需求解决方案站

从 Reddit 社区挖掘真实用户需求，自动生成 SaaS 产品方案并部署独立站。

## 🚀 快速部署（Cloudflare Pages）

### 方式一：通过 Wrangler CLI 部署

```bash
# 1. 安装依赖
npm install

# 2. 登录 Cloudflare
npx wrangler login

# 3. 部署
npx wrangler pages deploy . --project-name reddit-solutions

# 4. （可选）创建 KV 并绑定用于动态数据
npx wrangler kv:namespace create REDDIT_KV
```

### 方式二：通过 Cloudflare Dashboard（无需 CLI）

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 进入 **Workers & Pages** → **创建** → **Pages** → **直接上传**
3. 上传本目录的 ZIP 包
4. 设置项目名: `reddit-solutions`
5. 部署后会自动获得 `https://kickstarterproof.pages.dev` 域名

### 方式三：连接 Git 仓库自动部署

1. 将此目录推送到 GitHub/GitLab
2. 在 Cloudflare Pages 中选择"连接到 Git"
3. 选择仓库，构建命令留空，输出目录填 `.`
4. 保存后自动部署，每次 push 自动更新

## ⚙️ 定时爬取配置（可选）

### 基础版（本地定时任务）

```bash
# Windows 计划任务（每 24 小时运行一次）
python crawl_reddit.py
```

### 进阶版（Cloudflare Workers + KV）

1. 创建 KV Namespace:
```bash
npx wrangler kv:namespace create REDDIT_KV
```

2. 部署 Worker:
```bash
npx wrangler deploy workers/cron_crawl.js
```

3. 设置定时触发器：
```bash
npx wrangler secret put CLOUDFLARE_API_TOKEN
npx wrangler deploy --cron "0 8 * * *"
```

## 📁 项目结构

```
reddit-solutions-site/
├── index.html              # 主页面（含 18 个静态产品方案）
├── wrangler.toml           # Cloudflare Pages 配置
├── crawl_reddit.py         # Python 爬取脚本
├── functions/
│   └── api/
│       └── products.json.js  # Cloudflare Functions API 端点
└── workers/
    └── cron_crawl.js       # Cloudflare Workers 定时爬取
```

## 📊 产品方案清单

| # | 产品名称 | 分类 | Reddit 来源 |
|---|---------|------|------------|
| 1 | SubredditInsight | SaaS | r/Entrepreneur |
| 2 | LeadFlow | SaaS | r/SaaS |
| 3 | ChurnGuard | SaaS | r/SaaS |
| 4 | ReviewPulse | SaaS | r/Entrepreneur |
| 5 | APIForge | 开发者工具 | r/webdev |
| 6 | EnvSync | 开发者工具 | r/devops |
| 7 | LogLens | 开发者工具 | r/programming |
| 8 | BioLink Pro | 营销增长 | r/socialmedia |
| 9 | ViralHook | 营销增长 | r/PartneredYoutube |
| 10 | RedditReply | 营销增长 | r/Entrepreneur |
| 11 | WaitlistWizard | 营销增长 | r/startups |
| 12 | FocusFlow | 效率提升 | r/freelance |
| 13 | DocuWeave | 效率提升 | r/SideProject |
| 14 | InvoiceBot | 效率提升 | r/freelance |
| 15 | BrandVoice | AI 应用 | r/marketing |
| 16 | PodcastGPT | AI 应用 | r/podcasting |
| 17 | MeetingMuse | AI 应用 | r/productivity |
| 18 | CodeReviewAI | AI 应用 | r/programming |

## 🔧 自定义开发

### 修改产品数据

编辑 `index.html` 中的 `staticProducts` 数组，每个产品的字段：

- `title` - 产品名称
- `category` - 分类 (saas/dev/marketing/productivity/ai)
- `tags` - 标签数组
- `painPoint` - Reddit 痛点原文
- `solution` - 解决方案描述
- `price` - 价格
- `period` - 计费周期
- `url` - 链接
- `redditSource` - 来源子版块

### 添加更多子版块

编辑 `crawl_reddit.py` 中的 `TARGET_SUBREDDITS` 数组。
