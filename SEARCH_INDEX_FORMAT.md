# TechSpecsHub 搜索索引 JSON 格式说明

## 概述

TechSpecsHub 使用内置搜索索引进行前端全文搜索，无需后端支持。索引数据直接嵌入在 `main.js` 文件的 `SEARCH_INDEX` 数组中。

## 数据格式

```javascript
{
  "title": "页面标题",
  "description": "简短描述，用于搜索匹配",
  "type": "页面类型",
  "url": "相对于域名的URL路径",
  "keywords": ["关键词1", "关键词2", "..."]
}
```

## 字段说明

| 字段 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `title` | 是 | string | 页面标题，用于搜索匹配和显示 |
| `description` | 是 | string | 简短描述，会被搜索匹配 |
| `type` | 是 | string | 页面类型：`spec`, `error`, `tool`, `guide` |
| `url` | 是 | string | 相对于域名的URL路径 |
| `keywords` | 否 | array | 额外关键词数组，增强搜索匹配 |

## 页面类型 (type)

| 类型 | 图标 | 说明 | 示例 |
|------|------|------|------|
| `spec` | file-text | 规格页面 | EcoFlow Delta Pro 3 Specs |
| `error` | alert-circle | 错误代码页面 | P0A80 Hybrid Battery |
| `tool` | wrench | 工具页面 | Runtime Calculator |
| `guide` | book-open | 故障排除指南 | How to Fix E1 Overload |

## 搜索算法

搜索按以下优先级排序：

1. **精确匹配** - 标题中包含完整搜索词
2. **部分匹配** - 标题中包含搜索词的一部分
3. **描述匹配** - 仅在描述中找到匹配
4. **关键词匹配** - 在 keywords 数组中找到匹配

结果按优先级排序，同优先级内按字母顺序排列。

## 添加新页面

在 `main.js` 中找到 `SEARCH_INDEX` 数组，添加新条目：

```javascript
var SEARCH_INDEX = [
  // 现有条目...
  {
    title: 'New Page Title | TechSpecsHub',
    description: 'Brief description of the page content',
    type: 'spec', // 或 'error', 'tool', 'guide'
    url: 'pages/specs/new-page.html',
    keywords: ['keyword1', 'keyword2', 'related-term']
  },
];
```

## URL 路径规则

- 首页: `index.html`
- pages 目录下的文件: `pages/filename.html`
- specs 子目录: `pages/specs/filename.html`
- troubleshooting 子目录: `pages/troubleshooting/filename.html`

## 文件大小

当前索引包含约 50 个条目，文件大小约 15KB。

如需扩展到 100+ 条目，建议：
1. 按类别拆分索引（power-stations.json, hybrids.json, drones.json）
2. 使用分片加载（懒加载）
3. 实现缓存机制

## 性能优化

- 索引在页面加载时初始化
- 搜索使用内存过滤，无需网络请求
- 结果限制为 10 条，避免 DOM 过度渲染
- 支持键盘导航（↑↓ Enter Esc）

## 示例条目

```javascript
// 规格页面
{
  title: 'EcoFlow Delta Pro 3 | Full Specs',
  description: '4096 Wh LFP 4000 cycles Split-Phase New',
  type: 'spec',
  url: 'pages/specs/ecoflow-delta-pro-3.html',
  keywords: ['ecoflow', 'delta pro 3', '4096wh', '4000w', 'solar']
}

// 错误代码页面
{
  title: 'P0A80 Hybrid Battery Replacement Guide',
  description: 'Toyota Prius hybrid battery module replacement',
  type: 'guide',
  url: 'pages/troubleshooting/p0a80-replace-hybrid-battery.html',
  keywords: ['p0a80', 'hybrid battery', 'prius', 'replacement']
}

// 工具页面
{
  title: 'Runtime Calculator',
  description: 'Calculate power station runtime',
  type: 'tool',
  url: 'pages/tools/runtime-calculator.html',
  keywords: ['runtime', 'calculator', 'wh', 'wattage']
}
```
