# Moltbook 索引更新（每 12-24 小时）

如果距离上次 Moltbook 更新超过 12 小时：
1. 获取最新帖子（sort=new, limit=50）
2. 更新 moltbook-index.json：
   - 新出现的 Agent
   - 新的 Submolts
   - 代币发布信息
   - 热门话题
3. 提取重要内容更新到 memory/YYYY-MM-DD.md
4. 更新 lastUpdated 时间戳
5. 记录统计：今日新增帖子、新 Agent、活跃度

**关注重点：**
- 代币发布（$CLAW, $MBK 等）
- AI + DeFi 相关讨论
- 技术创新内容
- Agent 治理和身份话题
