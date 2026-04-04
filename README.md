# 职前探 - 求职备考助手

> 搜索公司动态 · 解析岗位要求 · 生成面试题 · 优化简历

**🌐 在线访问：** https://offer-xia-production.up.railway.app

---

## 功能介绍

| 功能 | 描述 |
|------|------|
| 🔍 公司动态搜索 | 输入目标公司，实时获取最新动态和新闻 |
| 📋 JD 解析 | 粘贴职位描述，自动提取核心技能要求 |
| 💬 面试题生成 | 根据公司和岗位，生成高频面试题及备考建议 |
| 📄 简历优化 | 针对目标岗位，给出具体的简历改进建议 |

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | HTML / CSS / JavaScript（无框架） |
| 后端 | Python + FastAPI |
| AI 模型 | DeepSeek API |
| 实时搜索 | Tavily Search API |
| 部署 | Railway（后端 + 前端一体） |

## 本地运行

**1. 克隆项目**
```bash
git clone https://github.com/bowu31706-eng/offer-xia.git
cd offer-xia/backend
```

**2. 配置 API Key**

新建 `.env` 文件：
```
DEEPSEEK_API_KEY=your_deepseek_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**3. 安装依赖并启动**
```bash
pip install -r requirements.txt
python main.py
```

访问 http://localhost:8000 即可使用。

## 项目结构

```
offer-xia/
├── backend/
│   ├── main.py          # API 路由 + 前端托管
│   ├── services.py      # DeepSeek / Tavily 调用逻辑
│   ├── static/          # 前端页面
│   ├── requirements.txt
│   └── railway.toml     # Railway 部署配置
└── webapp/              # 前端源文件
    └── index.html
```

## 关于作者

大三在校生，零技术背景，自学从零搭建这个项目，目标方向：AI 产品经理。

---

*Built with DeepSeek API · Tavily Search · FastAPI · Railway*
