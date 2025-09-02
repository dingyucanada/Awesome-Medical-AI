# 🚀 Deployment Guide

## 快速部署到 GitHub

### 1. 初始化 Git 仓库
```bash
cd Awesome-GenAI-Healthcare
git init
git add .
git commit -m "Initial commit: Healthcare AI papers collection system"
```

### 2. 在 GitHub 创建新仓库
1. 访问 https://github.com/new
2. 仓库名称: `Awesome-GenAI-Healthcare`
3. 设为公开(Public)
4. 不要初始化 README (我们已有)

### 3. 推送代码
```bash
git remote add origin https://github.com/dingyucanada/Awesome-GenAI-Healthcare.git
git branch -M main
git push -u origin main
```

### 4. 配置 GitHub Actions
Actions 会自动运行，但需要配置权限：

1. 访问: `Settings` → `Actions` → `General`
2. Workflow permissions: 选择 `Read and write permissions`
3. 保存设置

### 5. (可选) 添加 OpenAI API Key
获得更好的 AI 综述生成：

1. 访问: `Settings` → `Secrets and variables` → `Actions`
2. 点击 `New repository secret`
3. Name: `OPENAI_API_KEY`
4. Value: 你的 OpenAI API key
5. 点击 `Add secret`

### 6. 手动触发首次运行
1. 访问: `Actions` → `Daily Paper Update`
2. 点击 `Run workflow` → `Run workflow`

## 🔧 本地测试

```bash
# 赋予执行权限
chmod +x setup.sh

# 运行设置脚本
./setup.sh
```

## 📅 自动更新时间

- 默认: 每天 UTC 00:00 (北京时间 08:00)
- 修改时间: 编辑 `.github/workflows/daily_update.yml` 中的 cron 表达式

## 🌟 功能特点

✅ **已实现功能:**
- 自动收集 ArXiv, PubMed 论文
- 智能分类到8个研究领域
- 每日自动更新 README
- AI 生成综述文档
- 交互式数据仪表板
- 趋势分析和可视化

⏳ **高级功能 (可扩展):**
- 论文引用关系网络
- 个性化邮件订阅
- 多语言支持
- API 接口服务

## 📊 查看成果

部署后访问:
- 主页: `https://github.com/[你的用户名]/Awesome-GenAI-Healthcare`
- 仪表板: 点击 README 中的 Dashboard 链接
- 综述: 查看 `SURVEY.md`

## ⚠️ 重要提醒

1. **不要在代码中硬编码 API Keys**
2. **定期检查 Actions 运行状态**
3. **社区贡献**: 开启 Issues 和 Discussions

## 🆘 故障排除

### Actions 失败
- 检查 Actions 日志
- 确认 API 限额未超
- 验证仓库权限设置

### 论文收集为空
- ArXiv/PubMed API 可能临时不可用
- 等待下次自动运行
- 或手动触发 workflow

### 可视化不显示
- 确保安装了 matplotlib: `pip3 install matplotlib pandas`
- 检查 `docs/images/` 目录权限

## 💡 定制化

修改关键词和分类:
- 编辑 `scripts/collect_papers.py` 中的 `keywords` 和 `categories`

调整收集频率:
- 修改 `.github/workflows/daily_update.yml` 中的 schedule

## 📧 联系支持

遇到问题? 
- 提交 Issue: https://github.com/[你的用户名]/Awesome-GenAI-Healthcare/issues
- 查看 Actions 日志获取详细错误信息

---
祝您研究顺利! 🚀