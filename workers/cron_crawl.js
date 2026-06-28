// Cloudflare Workers 脚本 — 定时爬取 Reddit 更新
// 部署方式: wrangler deploy
// 定时触发: 每天 8:00 UTC
export default {
  async scheduled(event, env, ctx) {
    // 这个 worker 会通知外部服务器执行爬取
    // 或者直接内联爬取逻辑（但需要 subrequest 到 reddit）
    console.log('Scheduled crawl triggered:', event.cron);
    await crawlAndUpdate(env);
  },

  async fetch(request, env) {
    const url = new URL(request.url);

    // GET /crawl — 手动触发爬取
    if (request.method === 'GET' && url.pathname === '/crawl') {
      try {
        await crawlAndUpdate(env);
        return new Response(JSON.stringify({ status: 'ok', message: '爬取完成' }), {
          headers: { 'Content-Type': 'application/json' },
        });
      } catch (e) {
        return new Response(JSON.stringify({ status: 'error', message: e.message }), { status: 500 });
      }
    }

    // GET / — 返回网站
    return env.ASSETS.fetch(request);
  },
};

async function crawlAndUpdate(env) {
  const subreddits = [
    'Entrepreneur', 'SaaS', 'startups', 'webdev',
    'SideProject', 'SomebodyMakeThis', 'freelance',
    'programming', 'marketing', 'productivity',
  ];

  const results = [];
  const userAgent = 'CFRedditBot/1.0 (Cloudflare Worker)';

  for (const sub of subreddits) {
    try {
      const url = `https://www.reddit.com/r/${sub}/hot.json?limit=10`;
      const resp = await fetch(url, { headers: { 'User-Agent': userAgent } });
      if (!resp.ok) continue;

      const data = await resp.json();
      const posts = data.data.children.map(c => c.data).filter(p => !p.stickied);

      for (const post of posts) {
        const text = (post.title + ' ' + (post.selftext || '')).toLowerCase();
        const painSignals = ['i need', 'i wish', 'looking for', 'any tool', 'is there a',
          'problem', 'pain point', 'frustrated', 'hate', 'difficult'];
        const hasPain = painSignals.some(s => text.includes(s));

        if (hasPain) {
          results.push({
            id: post.id,
            title: post.title,
            score: post.score,
            comments: post.num_comments,
            subreddit: sub,
            url: `https://www.reddit.com${post.permalink}`,
            created: post.created_utc,
          });
        }
      }
    } catch (e) {
      console.error(`Failed r/${sub}:`, e.message);
    }
  }

  // 存储到 KV
  if (env.REDDIT_KV) {
    const data = {
      updated_at: new Date().toISOString(),
      count: results.length,
      products: results.sort((a, b) => b.score - a.score).slice(0, 50),
    };
    await env.REDDIT_KV.put('latest_crawl', JSON.stringify(data));
    // 更新 HTML 中的产品数据（通过 API endpoint 让前端读取）
    await env.REDDIT_KV.put('products_json', JSON.stringify(data.products));
  }

  console.log(`Crawl complete: ${results.length} pain-point posts found`);
  return results;
}
