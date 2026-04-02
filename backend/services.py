# services.py
# 封装所有对外 API 的调用：DeepSeek 大模型 + Tavily 搜索
# main.py 里的接口直接调用这里的函数，保持逻辑分离

import os
from openai import OpenAI
from tavily import TavilyClient


def get_deepseek_client() -> OpenAI:
    """
    创建 DeepSeek 客户端。
    DeepSeek 的 API 格式与 OpenAI 完全兼容，只需换 base_url 和 api_key。
    """
    return OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )


def get_tavily_client() -> TavilyClient:
    return TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# ── 功能 1：搜索公司动态 ──────────────────────────────────────────────────────
def search_company(company_name: str) -> str:
    """
    用 Tavily 搜索目标公司的近期动态，返回整理后的文本摘要。
    """
    client = get_tavily_client()
    query = f"{company_name} AI产品 最新动态 2024 2025"

    try:
        results = client.search(query=query, max_results=3)
        items = results.get("results", [])

        if not items:
            return f"未能搜索到 {company_name} 的相关动态，建议手动查阅官网。"

        lines = []
        for i, item in enumerate(items, 1):
            title = item.get("title", "无标题")
            content = item.get("content", "")[:200]  # 截取前 200 字防止太长
            lines.append(f"{i}. {title}\n   {content}...")

        return "\n\n".join(lines)

    except Exception as e:
        return f"搜索失败：{str(e)}，请检查 TAVILY_API_KEY 是否正确。"


# ── 功能 2：解析 JD ───────────────────────────────────────────────────────────
def analyze_jd(jd_text: str) -> str:
    """
    用 DeepSeek 分析 JD 文本，提取核心能力要求和关键信息。
    """
    client = get_deepseek_client()

    prompt = f"""你是一位资深 HR 和职业规划顾问。
请分析以下职位描述（JD），提取关键信息并结构化输出。

JD 内容：
{jd_text}

请按照以下格式输出：

【岗位核心能力要求】
- （列出 5～8 条最重要的能力要求）

【高频关键词】
（用逗号分隔，列出 JD 中反复出现或最重要的词汇）

【岗位侧重点分析】
（2～3 句话概括这个岗位最看重什么）

【给求职者的提示】
（针对这份 JD，应聘者需要特别注意的 2～3 点）"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"JD 解析失败：{str(e)}，请检查 DEEPSEEK_API_KEY 是否正确。"


# ── 功能 3：生成面试题 ────────────────────────────────────────────────────────
def generate_questions(company_name: str, job_type: str) -> str:
    """
    用 DeepSeek 生成针对特定公司和岗位的高频面试题。
    """
    client = get_deepseek_client()

    prompt = f"""你是一位有丰富面试经验的 AI 产品方向面试官。
请为以下岗位生成 10 个高频面试题，覆盖不同题型。

目标公司：{company_name}
目标岗位：{job_type}

要求：
1. 每道题后标注题型：【行为题】【产品题】【技术认知题】【情景题】之一
2. 题目要贴合该公司的业务特点
3. 难度适中，偏向校招/应届生水平

输出格式：

【高频面试题】
1. （题目内容）【题型】
2. （题目内容）【题型】
...
10. （题目内容）【题型】

【备考建议】
（针对以上题目，给出 3～5 条具体的备考建议）"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"面试题生成失败：{str(e)}，请检查 DEEPSEEK_API_KEY 是否正确。"


# ── 功能 4：优化简历 ──────────────────────────────────────────────────────────
def optimize_resume(resume_text: str, job_type: str, company_name: str) -> str:
    """
    用 DeepSeek 分析简历，针对目标岗位给出具体的优化建议。
    """
    client = get_deepseek_client()

    prompt = f"""你是一位专业的简历优化顾问，擅长帮助应届生优化 AI 产品方向的简历。

求职者的目标：
- 目标公司：{company_name}
- 目标岗位：{job_type}

简历内容：
{resume_text}

请从以下 4 个维度给出具体优化建议：

【整体评分】
（满分 10 分，给出评分和一句总结）

【亮点保留】
（列出简历中值得保留和强化的 2～3 个亮点）

【具体优化建议】
（针对目标岗位，给出 5 条可以立即执行的修改建议，要具体到某句话怎么改）

【补充建议】
（建议求职者额外补充的项目经历、技能或证书，2～3 条）"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"简历优化失败：{str(e)}，请检查 DEEPSEEK_API_KEY 是否正确。"
