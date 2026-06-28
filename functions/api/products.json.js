// Cloudflare Pages Function — API 端点
// 为前端提供动态 Reddit 数据（如果配置了 KV）
// 路径: /api/products.json

export async function onRequest(context) {
  const { env, request } = context;

  // 尝试从 KV 获取最新数据
  if (env.REDDIT_KV) {
    const cached = await env.REDDIT_KV.get('products_json');
    if (cached) {
      return new Response(cached, {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'public, max-age=300',
        },
      });
    }

    const latest = await env.REDDIT_KV.get('latest_crawl');
    if (latest) {
      const parsed = JSON.parse(latest);
      return new Response(JSON.stringify(parsed.products), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'public, max-age=300',
        },
      });
    }
  }

  // 回退到静态数据
  const fallback = [
    { id: 'demo-1', title: 'Demo: Reddit API 数据将在配置 KV 后自动加载', score: 100, subreddit: 'Entrepreneur' },
  ];
  return new Response(JSON.stringify(fallback), {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    },
  });
}
