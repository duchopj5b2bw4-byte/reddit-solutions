#!/usr/bin/env python3
"""
Reddit 需求爬取 + 产品更新脚本
每 24 小时运行一次，自动爬取 Reddit 热门帖子，
分析需求并更新到网站 products.json 数据。

用法:
    python crawl_reddit.py              # 爬取并更新 products.json
    python crawl_reddit.py --dry-run    # 只打印但不写入
    python crawl_reddit.py --serve      # 启动本地服务预览

依赖:
    pip install requests beautifulsoup4
"""

import json
import re
import os
import sys
import time
import urllib.request
import urllib.parse
import html

REDDIT_API_BASE = "https://www.reddit.com"
TARGET_SUBREDDITS = [
    "Entrepreneur",
    "SaaS",
    "startups",
    "webdev",
    "SideProject",
    "SomebodyMakeThis",
    "freelance",
    "programming",
    "marketing",
    "productivity",
    "socialmedia",
    "devops",
    "podcasting",
    "PartneredYoutube",
]
USER_AGENT = "RedditSolutionsBot/1.0 (Windows; +https://reddit-solutions.pages.dev)"
OUTPUT_FILE = "products_data.json"

# 缓存用于增量更新
KNOWN_POSTS_FILE = "known_posts.json"


def fetch_subreddit_hot(subreddit, limit=15):
    """获取子版块热门帖子"""
    url = f"{REDDIT_API_BASE}/r/{subreddit}/hot.json?limit={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return [
                {
                    "id": post["data"]["id"],
                    "title": post["data"]["title"],
                    "score": post["data"]["score"],
                    "num_comments": post["data"]["num_comments"],
                    "selftext": post["data"].get("selftext", "")[:500],
                    "url": post["data"]["url"],
                    "permalink": f"https://www.reddit.com{post['data']['permalink']}",
                    "created_utc": post["data"]["created_utc"],
                    "subreddit": subreddit,
                }
                for post in data["data"]["children"]
                if not post["data"].get("stickied")
            ]
    except Exception as e:
        print(f"  [WARN] r/{subreddit} 获取失败: {e}")
        return []


def is_pain_point_post(post):
    """判断帖子是否包含需求/痛点信号"""
    text = (post["title"] + " " + post["selftext"]).lower()
    pain_signals = [
        "i need", "i wish", "looking for", "any tool", "is there a",
        "problem", "pain point", "frustrated", "annoying", "hate",
        "difficult", "hard to", "takes forever", "nightmare",
        "missing", "lack of", "wish there was", "does anyone know",
        "how do you", "recommend", "suggestion", "idea for",
        "why isn't there", "needs a", "would be great if",
    ]
    return any(signal in text for signal in pain_signals)


def post_to_product(post):
    """将 Reddit 帖子转换为产品数据（AI 分析版）"""
    # 模拟 AI 分析结果
    title = post["title"]
    sub = post["subreddit"]

    # 智能分类
    category_map = {
        "Entrepreneur": "saas",
        "SaaS": "saas",
        "startups": "marketing",
        "webdev": "dev",
        "SideProject": "dev",
        "SomebodyMakeThis": "saas",
        "freelance": "productivity",
        "programming": "dev",
        "marketing": "marketing",
        "productivity": "productivity",
        "socialmedia": "marketing",
        "devops": "dev",
        "podcasting": "ai",
        "PartneredYoutube": "marketing",
    }
    category = category_map.get(sub, "saas")

    # 生成标签
    keyword_tags = []
    ai_keywords = ["ai", "automate", "automatic", "generat", "intellig"]
    dev_keywords = ["code", "api", "dev", "deploy", "git", "database"]
    mkt_keywords = ["market", "traffic", "lead", "conversion", "social"]
    prod_keywords = ["time", "track", "manage", "organize", "productiv"]

    title_lower = title.lower()
    if any(k in title_lower for k in ai_keywords):
        keyword_tags.append("AI")
    if any(k in title_lower for k in dev_keywords):
        keyword_tags.append("开发者工具")
    if any(k in title_lower for k in mkt_keywords):
        keyword_tags.append("营销")
    if any(k in title_lower for k in prod_keywords):
        keyword_tags.append("效率")
    if not keyword_tags:
        keyword_tags.append("SaaS")

    # 清理标题
    clean_title = re.sub(r'\[.*?\]|\(.*?\)', '', title).strip()
    # 缩短长标题
    if len(clean_title) > 60:
        clean_title = clean_title[:57] + "..."

    return {
        "id": f"reddit_{post['id']}",
        "title": f"{clean_title} — 解决方案",
        "category": category,
        "tags": keyword_tags[:3],
        "painPoint": f'"{title}" — r/{sub} ({post["score"]}+ upvotes, {post["num_comments"]} 条评论)',
        "solution": "基于 Reddit 社区的真实需求设计的解决方案。结合 AI 分析和行业最佳实践，提供可落地的 MVP 方案。点击查看完整产品详情。",
        "price": "$19",
        "period": "/月",
        "url": post["permalink"],
        "redditSource": f"r/{sub}",
        "sourceId": post["id"],
        "score": post["score"],
        "comments": post["num_comments"],
        "created": post["created_utc"],
    }


def load_known():
    """加载已知帖子 ID"""
    if os.path.exists(KNOWN_POSTS_FILE):
        with open(KNOWN_POSTS_FILE) as f:
            return set(json.load(f))
    return set()


def save_known(ids):
    """保存已知帖子 ID"""
    with open(KNOWN_POSTS_FILE, "w") as f:
        json.dump(list(ids), f)


def crawl(dry_run=False):
    """主爬取流程"""
    print(f"🚀 开始爬取 {len(TARGET_SUBREDDITS)} 个子版块...")
    new_posts = []
    total_posts = 0

    for i, sub in enumerate(TARGET_SUBREDDITS, 1):
        print(f"  [{i}/{len(TARGET_SUBREDDITS)}] r/{sub}...", end=" ")
        posts = fetch_subreddit_hot(sub)
        total_posts += len(posts)
        pain_posts = [p for p in posts if is_pain_point_post(p)]
        new_posts.extend(pain_posts)
        print(f"{len(posts)} 帖子, {len(pain_posts)} 含需求信号")

        # Reddit rate limit
        time.sleep(0.5)

    print(f"\n📊 共获取 {total_posts} 帖子，其中 {len(new_posts)} 包含需求信号")

    # 去重
    seen = set()
    unique_posts = []
    for p in new_posts:
        if p["id"] not in seen:
            seen.add(p["id"])
            unique_posts.append(p)

    # 转换为产品数据
    products = [post_to_product(p) for p in unique_posts]
    # 按热度排序
    products.sort(key=lambda x: x.get("score", 0), reverse=True)
    # 取前 20
    products = products[:20]

    print(f"✅ 生成 {len(products)} 个产品方案")

    if dry_run:
        print("\n=== Dry Run 预览 ===")
        for p in products:
            print(f"  [{p['category']}] {p['title']} ({p['redditSource']})")
        return

    # 写入文件
    output = {
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sources": len(TARGET_SUBREDDITS),
        "total_products": len(products),
        "products": products,
        "subreddits": TARGET_SUBREDDITS,
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"💾 已保存到 {OUTPUT_FILE}")
    return products


def serve_local():
    """启动本地预览服务器"""
    import http.server
    import socketserver

    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌐 本地预览: http://localhost:{PORT}")
        print("按 Ctrl+C 停止")
        httpd.serve_forever()


if __name__ == "__main__":
    if "--serve" in sys.argv:
        serve_local()
    else:
        dry = "--dry-run" in sys.argv
        crawl(dry_run=dry)
