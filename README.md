# 🎯 AI 求职备考助手

基于 **DeepSeek AI + 微信小程序** 的智能求职工具。

输入目标公司和岗位 JD，自动完成：公司动态搜索 → JD 深度解析 → 面试题生成 → 简历优化建议。

---

## 项目亮点（给面试官看）

| 技术点 | 说明 |
|--------|------|
| **AI 大模型集成** | 接入 DeepSeek API，实现 JD 解析、面试题生成、简历优化 |
| **实时搜索** | 接入 Tavily Search API，获取目标公司最新动态 |
| **前后端分离架构** | Python FastAPI 后端 + 微信小程序前端 |
| **云端部署** | 后端部署在 Railway，支持公网访问 |
| **Prompt Engineering** | 针对不同功能设计专用提示词，控制 AI 输出格式和质量 |

---

## 项目结构

```
job-prep-agent/
├── backend/                 # 后端（Python）
│   ├── main.py              # FastAPI 主程序，定义所有接口
│   ├── services.py          # 调用 DeepSeek / Tavily 的核心逻辑
│   ├── requirements.txt     # 后端依赖
│   ├── railway.toml         # Railway 部署配置
│   └── .env.example         # API Key 配置示例
└── miniprogram/             # 微信小程序前端
    ├── app.js / app.json / app.wxss   # 全局配置和样式
    ├── utils/api.js         # 封装后端请求
    ├── create_icons.py      # 一次性运行：生成底部导航栏图标
    └── pages/
        ├── index/           # 首页
        ├── jd/              # JD 备考分析页
        └── resume/          # 简历优化页
```

---

# 完整部署教程

## 第一阶段：本地调试

### 第 1 步：安装 Python

如果还没有 Python，从官网下载安装：https://www.python.org/downloads/

> 安装时务必勾选 **"Add Python to PATH"**

验证安装：
```bash
python --version
# 应输出类似 Python 3.11.0
```

### 第 2 步：获取两个 API Key

**DeepSeek API Key**
1. 打开 https://platform.deepseek.com
2. 注册并登录
3. 左侧菜单点击「API Keys」→「创建 API Key」
4. 复制 Key（以 `sk-` 开头），充值约 10 元即可长期使用

**Tavily Search API Key**
1. 打开 https://app.tavily.com
2. 注册并登录
3. 首页直接显示你的 API Key（以 `tvly-` 开头）
4. 免费额度每月 1000 次，够个人使用

### 第 3 步：配置后端 API Key

进入 `backend` 文件夹，将 `.env.example` 复制一份并重命名为 `.env`：

**Windows（在 backend 目录下）：**
```
copy .env.example .env
```

用记事本打开 `.env`，填入真实 Key：
```
DEEPSEEK_API_KEY=sk-你的key
TAVILY_API_KEY=tvly-你的key
```

### 第 4 步：安装后端依赖并启动

```bash
# 进入 backend 目录
cd backend

# 安装依赖（如果很慢，加 -i 参数使用国内镜像）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 启动后端服务
python main.py
```

看到以下输出说明启动成功：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

浏览器打开 http://localhost:8000/docs 可以看到接口文档，并在线测试每个接口。

### 第 5 步：安装微信开发者工具

1. 下载地址：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html
2. 选择「稳定版」下载安装
3. 用微信扫码登录

### 第 6 步：生成小程序图标文件

在 `miniprogram` 目录下运行一次：
```bash
cd miniprogram
python create_icons.py
```

### 第 7 步：用开发者工具打开小程序

1. 打开微信开发者工具
2. 点击「+」新建项目
3. 选择「导入项目」
4. 目录选择 `job-prep-agent/miniprogram` 文件夹
5. AppID 先填 `test`（测试用，正式上线再换）
6. 点击「导入」

### 第 8 步：开启「不校验合法域名」

小程序默认只允许请求已备案的 HTTPS 域名。本地调试时需要关闭这个限制：

微信开发者工具右上角 →「详情」→「本地设置」→ 勾选**「不校验合法域名、web-view（业务域名）、TLS 版本以及 HTTPS 证书」**

### 第 9 步：测试联调

确保后端已经在运行（`python main.py`），然后在开发者工具里：
1. 点击底部「JD备考」
2. 输入公司名：`字节跳动`
3. 粘贴一段 JD 文本
4. 点击「开始分析」

如果看到结果说明联调成功！

---

## 第二阶段：部署到线上（Railway）

### 第 1 步：注册 Railway 账号

1. 打开 https://railway.app
2. 点击「Login」→ 用 GitHub 账号登录（需要先有 GitHub 账号）

### 第 2 步：注册 GitHub 并上传代码

如果还没有 GitHub 账号：
1. 打开 https://github.com，注册账号
2. 点击右上角「+」→「New repository」
3. 仓库名填 `job-prep-agent`，选 Public，点「Create repository」
4. 按页面提示把代码上传（**注意：`.env` 文件不要上传！**）

### 第 3 步：在 Railway 部署后端

1. 打开 Railway，点击「New Project」
2. 选择「Deploy from GitHub repo」
3. 找到并选择你的 `job-prep-agent` 仓库
4. Railway 会问你部署哪个文件夹，选择 `backend`
5. 部署开始，等待约 2 分钟

### 第 4 步：在 Railway 配置环境变量

1. 在 Railway 项目页面，点击你的服务
2. 点击「Variables」标签
3. 添加两个变量：
   - `DEEPSEEK_API_KEY` = 你的 DeepSeek Key
   - `TAVILY_API_KEY` = 你的 Tavily Key
4. 保存后 Railway 会自动重启服务

### 第 5 步：获取后端域名

Railway 部署成功后，点击「Settings」→「Domains」→「Generate Domain」

会生成一个类似 `https://job-prep-agent-xxx.railway.app` 的域名，**复制它**。

### 第 6 步：更新小程序的后端地址

打开 `miniprogram/app.js`，把 `baseUrl` 改为你的 Railway 域名：

```javascript
baseUrl: 'https://job-prep-agent-xxx.railway.app',  // 换成你的真实域名
```

---

## 第三阶段：上线微信小程序

### 第 1 步：注册微信小程序账号

1. 打开 https://mp.weixin.qq.com
2. 右上角「立即注册」→ 选「小程序」
3. 用个人邮箱注册，按提示完成认证
4. 登录后在「开发」→「开发设置」里找到你的 **AppID**，复制它

### 第 2 步：配置服务器域名白名单

小程序正式版只能请求已登记的域名：

1. 登录微信公众平台 → 「开发」→「开发设置」→「服务器域名」
2. 在「request 合法域名」里添加你的 Railway 域名（例如 `https://job-prep-agent-xxx.railway.app`）
3. 保存

### 第 3 步：在开发者工具填入真实 AppID

1. 开发者工具右上角「详情」→「基本信息」
2. 将 AppID 改为你注册的真实 AppID

### 第 4 步：上传代码并提审

1. 开发者工具右上角点击「上传」
2. 填写版本号（如 `1.0.0`）和描述，点确认
3. 登录微信公众平台 → 「版本管理」→ 找到刚上传的开发版
4. 点「提交审核」，填写类目（选「工具-效率」）
5. 等待微信审核（通常 1～3 个工作日）
6. 审核通过后点「发布」即可上线

---

## 常见问题

**Q：后端启动报错 `ModuleNotFoundError`**
A：`pip install -r requirements.txt` 重装依赖

**Q：小程序提示「request:fail`」**
A：检查 app.js 里的 baseUrl 是否正确，本地调试时确认已勾选「不校验合法域名」

**Q：AI 返回内容很慢**
A：DeepSeek 通常需要 10～30 秒，属正常现象

**Q：Railway 部署失败**
A：检查 `backend` 目录下有没有 `requirements.txt` 和 `railway.toml`

---

*Built with DeepSeek API + Tavily Search + FastAPI + 微信小程序*
