# KickstarterProof — 定价与付款接入方案

## 当前商业策略

目标不是立刻做完整 SaaS 后台，而是先验证：陌生用户是否愿意为“众筹硬件买前风险报告”付费。

推荐顺序：
1. 先用 Payment Link 收款。
2. 人工/半自动交付前 20 份报告。
3. 有真实订单后再做自动化视频分析和后台。

## 定价

### 1. Launch 验证价：$19 / 单次报告

适合第一批用户。

交付内容：
- Kickstarter / Indiegogo / YouTube 链接风险摘要
- 演示视频疑点：硬切、缺失镜头、只展示理想片段
- 评论区质疑聚类：耐久、发货、售后、价格、团队可信度
- 页面承诺风险：功能承诺、时间线、保修、退款风险
- 最终建议：Buy / Wait / Avoid
- 24 小时内邮件交付

为什么 $19 合理：
- 用户要避免的是 $200-$1000 的众筹踩坑损失。
- 一次性买前决策比月订阅更自然。
- 足够低摩擦，可用于 Reddit / YouTube 评论区冷启动。

### 2. Standard：$29 / 单次报告

当出现 5-10 个付费订单后，把价格从 $19 提到 $29。

### 3. Pro：$49 / 月

只给重度用户：硬件测评博主、众筹买手、科技 newsletter 作者。

包含：
- 每月 5 份完整报告
- 关注项目变更提醒
- 高风险评论新增提醒
- 可导出公开评测摘要

## 付款接入最快方案

### Stripe Payment Link

1. Stripe Dashboard → Product Catalog → Add product
2. Product name: KickstarterProof Risk Report
3. Price: $19 one-time
4. Create payment link
5. 收集字段：
   - Email
   - Custom field: Campaign URL
6. 复制 Payment Link
7. 修改 `index.html`：

```js
const PAYMENT_LINK = 'https://buy.stripe.com/你的链接';
```

部署：

```bash
set -a; source .env.local; set +a
npx wrangler pages deploy . --project-name reddit-solutions --branch main
```

### PayPal 备选

如果 Stripe 还没开通：
1. PayPal → Create payment link / PayPal.Me
2. 固定金额 $19
3. 页面 CTA 暂时跳转 PayPal
4. 用户付款后通过邮箱提交 Campaign URL

## 线索记录表字段

用 Google Sheets / Notion 表即可：

| 字段 | 说明 |
|---|---|
| Submitted At | 提交时间 |
| Email | 用户邮箱 |
| Campaign URL | 众筹/视频链接 |
| Source | Reddit / YouTube / X / V2EX |
| Paid | Yes / No |
| Payment ID | Stripe / PayPal ID |
| Status | New / In Review / Delivered |
| Risk Score | 0-100 |
| Recommendation | Buy / Wait / Avoid |
| Report URL | 交付链接 |

## 首份报告模板

标题：KickstarterProof Risk Report — {Project Name}

结构：
1. Executive summary
2. Final recommendation: Buy / Wait / Avoid
3. Risk score: 0-100
4. Video demo red flags
5. Comment concerns
6. Creator/team credibility
7. Fulfillment and refund risks
8. What would change the recommendation

## 付款后交付流程

1. 用户付款并提交链接。
2. 抓取项目页、视频页、评论区。
3. 用 AI 生成初稿。
4. 人工复核风险评分和最终建议。
5. 邮件交付报告。
6. 询问是否允许匿名展示为样例。

## 上线前检查

- [ ] 创建 Stripe / PayPal Payment Link
- [ ] 把 `PAYMENT_LINK` 替换为真实付款链接
- [ ] 提交一个测试链接，确认表单文案可读
- [ ] 测试付款流程
- [ ] 准备 1 份样例报告截图
- [ ] 在 Reddit 发帖前，先准备好人工交付流程
