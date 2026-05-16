# TechSpecsHub 部署指南

## 📋 前置准备

### 1. 在 GitHub 上创建新仓库
1. 访问：https://github.com/new
2. 填入以下信息：
   - Repository name: `tech-specs-hub`
   - Description: `Technical specifications database for tech products`
   - 选择 Public
   - ✅ 勾选 "Initialize this repository with a README"
3. 点击 "Create repository"

---

## 🚀 部署步骤（方案 B）

### 2. 上传文件到仓库

你有两个选项：

#### 选项 A：使用 GitHub 网页界面（简单）

1. 打开你刚创建的仓库：https://github.com/zhang1-CPU/tech-specs-hub
2. 点击页面上的 "Add file" → "Upload files"
3. 从本地文件夹 `c:\Users\23028\Desktop\3web\tech-specs-hub` 拖入所有文件
4. 填写 Commit message：`Initial commit - full tech specs database`
5. 点击 "Commit changes"

#### 选项 B：使用 Git（推荐）

```bash
# 进入项目目录
cd c:\Users\23028\Desktop\3web\tech-specs-hub

# 初始化 Git
git init
git add .
git commit -m "Initial commit - full tech specs database"

# 添加远程仓库
git remote add origin https://github.com/zhang1-CPU/tech-specs-hub.git

# 推送到 main 分支
git branch -M main
git push -u origin main
```

---

## 🌐 启用 GitHub Pages

1. 在仓库页面，点击 "Settings"
2. 左侧菜单找到 "Pages"
3. 在 "Build and deployment" 下方：
   - Source: 选择 "Deploy from a branch"
   - Branch: 选择 `main` / `gh-pages` 和 `/ (root)`
4. 点击 "Save"
5. 等待 1-3 分钟，你的网站就部署完成了！

---

## 📌 访问地址

部署完成后，你的网站地址为：

```
https://zhang1-CPU.github.io/tech-specs-hub/
```

---

## 🔍 提交 Sitemap 到 Google

### 1. Google Search Console

1. 访问：https://search.google.com/search-console
2. 点击 "Add property"
3. 输入你的网站 URL：`https://zhang1-CPU.github.io/tech-specs-hub/`
4. 选择验证方式（推荐 "HTML tag"）
5. 在网站首页（index.html）添加 meta 标签

### 2. 提交 Sitemap

1. 左侧菜单找到 "Sitemaps"
2. 在输入框输入：`sitemap.xml`
3. 点击 "Submit"

---

## 📊 已准备好的文件

| 文件 | 作用 |
|------|------|
| `CNAME` | 自定义域名配置（可选） |
| `404.html` | 404 错误页面 |
| `sitemap.xml` | 网站地图 |
| `robots.txt` | 搜索引擎爬虫引导 |
| `ads.txt` | AdSense 配置（可选） |

---

## ⚠️ 重要提示

### 自定义域名（可选）

如果你想用 `techspecshub.com` 域名，需要：

1. 在仓库 Settings → Pages 中设置 Custom domain
2. 在你的域名 DNS 中添加：
   ```
   @  A  185.199.108.153
   @  A  185.199.109.153
   @  A  185.199.110.153
   @  A  185.199.111.153
   ```
3. 勾选 "Enforce HTTPS"

---

## 📞 需要帮助？

如果有问题，访问 GitHub Pages 官方文档：
https://pages.github.com/
