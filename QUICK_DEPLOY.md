# 🚀 一键部署指南

## 最简单的部署方法

### 方法1: 全自动部署（推荐）
```bash
./deploy.sh
```
这个脚本会自动：
- ✅ 安装GitHub CLI（如果没有）
- ✅ 登录您的GitHub账户
- ✅ 创建仓库
- ✅ 推送代码
- ✅ 配置GitHub Actions
- ✅ 触发首次运行

### 方法2: 手动部署（3步）

#### 步骤1: 创建GitHub仓库
访问: https://github.com/new
- Repository name: `Awesome-GenAI-Healthcare`
- Public
- 不要添加README

#### 步骤2: 推送代码
```bash
git remote add origin https://github.com/[您的用户名]/Awesome-GenAI-Healthcare.git
git push -u origin main
```

#### 步骤3: 启用Actions
1. 访问您的仓库
2. Settings → Actions → General
3. 选择 "Read and write permissions"
4. 保存

## ✅ 部署完成后

访问您的仓库查看：
- 📚 论文列表（已有49篇）
- 📊 数据仪表板
- 📝 AI生成的综述
- ⚡ 每日自动更新

## 🆘 需要帮助？

如果遇到问题，运行：
```bash
cat DEPLOYMENT_GUIDE.md
```

---
**重要**: 请不要分享您的GitHub密码！使用GitHub网页或CLI工具进行安全认证。