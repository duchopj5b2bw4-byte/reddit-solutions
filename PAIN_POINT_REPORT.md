# Reddit 痛点自动化抓取分析报告

生成时间：2026-06-29
抓取方式：本地 Chrome CDP + Playwright（绕过 Reddit JSON API 403）
数据范围：14 个 subreddit 的月榜页面，共抓取 335 个帖子。

## 抓取过的社区

- r/SomebodyMakeThis
- r/SideProject
- r/SaaS
- r/Entrepreneur
- r/startups
- r/webdev
- r/freelance
- r/productivity
- r/marketing
- r/programming
- r/devops
- r/podcasting
- r/PartneredYoutube
- r/socialmedia

## 最值得做的 7 个痛点

### 1. FaceCue — 观影人物识别助手

来源：https://www.reddit.com/r/SomebodyMakeThis/comments/1ue69lu/a_tool_to_help_those_with_prosopagnosia_facial/

痛点：脸盲/人物识别困难用户看真人电影和剧集时分不清角色，导致剧情理解困难，甚至影响同伴观影体验。

为什么值得做：
- 痛点非常具体，不是泛泛的“AI 工具”。
- 目标用户明确：Prosopagnosia、轻度脸盲、复杂剧集观众。
- 可做成浏览器扩展 / 本地播放器助手 / 截图识别工具。

MVP：用户截图或暂停视频，工具识别当前角色并显示角色名、近期剧情、人物关系。

定价建议：$9/月 或 $29 一次性。

### 2. TabLater — 定时重开标签页

来源：https://www.reddit.com/r/SomebodyMakeThis/comments/1u6d2jh/tab_reminder_reopens_a_tab_at_a_set_time_opposite/

痛点：用户不想把标签页一直开着，也不想收藏后遗忘；现有扩展时间选项少或卡在付费墙。

MVP：Chrome/Firefox 扩展，右键标签页选择“30 分钟后 / 明早 / 每周一 / 自定义时间”重新打开。

定价建议：免费基础版 + $4/月 Pro（重复提醒、同步、多设备）。

### 3. TrialGuard — 免费试用扣费提醒

来源：https://www.reddit.com/r/SomebodyMakeThis/comments/1u8h066/an_app_that_reminds_you_before_a_free_trial/

痛点：用户经常忘记取消免费试用而被扣费，但不愿把银行账户授权给订阅管理工具。

MVP：不用绑银行卡。用户转发订阅确认邮件或手动输入试用结束日期，系统在扣费前 7/3/1 天提醒并给取消链接。

定价建议：$2/月 或 $12/年。

### 4. DelayAlarm — 通勤延误智能闹钟

来源：https://www.reddit.com/r/SomebodyMakeThis/comments/1u3o9nl/thinking_of_building_an_app_for_this_would_you/

痛点：固定闹钟无法感知公交/地铁延误；用户醒来后才发现通勤出问题，已经来不及调整。

MVP：设置通勤路线 + 到达时间，早上检查实时交通；如有延误则提前叫醒并给替代路线。

定价建议：$3/月。难点在城市实时交通数据覆盖。

### 5. PlainMonth — 极简整月墙历

来源：https://www.reddit.com/r/SomebodyMakeThis/comments/1tzoh32/a_big_wall_calendar_software_or_site_thats/

痛点：用户只是想像看实体墙历一样看整月日期，但现代数字日历塞满事件、节日、账号同步和通知。

MVP：大屏整月视图，无登录、无同步、无默认节日，支持打印、桌面壁纸、简单便签。

定价建议：$5 一次性 / 免费广告版。

### 6. ReadNote AI — Kindle + NotebookLM 阅读器

来源：https://www.reddit.com/r/SomebodyMakeThis/comments/1ugrwis/an_aipowered_ereader_app_think_kindle_meets/

痛点：电子书阅读、AI 问答、笔记管理被割裂；用户想在阅读器里直接对书提问和沉淀知识。

MVP：导入 EPUB/PDF，章节摘要、人物/概念卡、对当前章节提问、高亮生成复习卡。

定价建议：$12/月。

### 7. KickstarterProof — 众筹演示可信度检查

来源：https://www.reddit.com/r/SomebodyMakeThis/comments/1ubjoaz/why_i_dont_trust_youtube_demos_of_upcoming/

痛点：用户被众筹硬件演示视频吸引，但担心视频剪辑只展示理想片段，没有第三方风险分析。

MVP：输入 Kickstarter/YouTube 链接，生成风险报告：剪辑跳跃、缺失镜头、评论质疑、团队历史、承诺风险。

定价建议：$19/次报告。

## 优先级建议

如果目标是最快做出能上线的 MVP：
1. TabLater：最简单，浏览器扩展，功能边界清晰。
2. TrialGuard：也简单，隐私卖点强，但需要邮件解析/提醒系统。
3. PlainMonth：最快上线，但付费意愿可能较弱。

如果目标是更有差异化和传播性：
1. FaceCue：痛点尖锐、故事性强、容易做成单产品落地页。
2. KickstarterProof：付费场景明确，买众筹产品前愿意花一次性报告钱。

## 已生成文件

- reddit_browser_posts.json：原始抓取结果，335 条帖子。
- products_data.json：精选产品数据，7 条痛点产品。
- functions/api/products.json.js：Cloudflare Pages API，返回精选产品。
- crawl_reddit_browser.js：通过本地 Chrome 抓 Reddit 页面的脚本。
