# services.py
# 封装所有对外 API 的调用：DeepSeek 大模型 + Tavily 搜索
# main.py 里的接口直接调用这里的函数，保持逻辑分离

import os
from openai import OpenAI
from tavily import TavilyClient


def get_deepseek_client() -> OpenAI:
    return OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )


def get_tavily_client() -> TavilyClient:
    return TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def _deepseek(prompt: str, max_tokens: int = 1500) -> str:
    """统一的 DeepSeek 调用封装，异常时返回错误文本。"""
    client = get_deepseek_client()
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 分析失败：{str(e)}"


def _tavily(query: str, max_results: int = 3) -> list:
    """统一的 Tavily 搜索封装，返回 results 列表。"""
    client = get_tavily_client()
    try:
        results = client.search(query=query, max_results=max_results)
        return results.get("results", [])
    except Exception as e:
        return []


def _format_tavily(items: list, company: str = "") -> str:
    """将 Tavily 搜索结果格式化为可读文本。"""
    if not items:
        return f"未能搜索到{'「' + company + '」' if company else ''}相关信息，建议手动查阅。"
    lines = []
    for i, item in enumerate(items, 1):
        title = item.get("title", "无标题")
        content = item.get("content", "")[:200]
        lines.append(f"{i}. {title}\n   {content}...")
    return "\n\n".join(lines)


# ══════════════════════════════════════════════════════════════════
# 原有四个功能
# ══════════════════════════════════════════════════════════════════

def search_company(company_name: str) -> str:
    """搜索目标公司近期动态（Tavily）。"""
    query = f"{company_name} 最新动态 产品 战略 2024 2025"
    items = _tavily(query, max_results=4)
    return _format_tavily(items, company_name)


def analyze_jd(jd_text: str) -> str:
    """解析 JD，提取核心能力要求和关键词（DeepSeek）。"""
    prompt = f"""你是一位资深 HR 和职业规划顾问。请分析以下职位描述（JD），提取关键信息并结构化输出。

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
    return _deepseek(prompt)


def generate_questions(company_name: str, job_type: str) -> str:
    """根据公司和岗位生成高频面试题（DeepSeek）。"""
    prompt = f"""你是一位有丰富面试经验的面试官。请为以下岗位生成 10 个高频面试题，覆盖不同题型。

目标公司：{company_name}
目标岗位：{job_type}

要求：
1. 每道题后标注题型：【行为题】【产品题】【技术认知题】【情景题】之一
2. 题目贴合该公司业务特点
3. 难度适中，偏向校招/社招初级水平

输出格式：

【高频面试题】
1. （题目内容）【题型】
...
10. （题目内容）【题型】

【备考建议】
（针对以上题目，给出 3～5 条具体备考建议）"""
    return _deepseek(prompt)


def optimize_resume(resume_text: str, job_type: str, company_name: str) -> str:
    """针对目标岗位优化简历（DeepSeek）。"""
    company_str = f"目标公司：{company_name}\n" if company_name else ""
    prompt = f"""你是一位专业的简历优化顾问。

求职目标：
{company_str}目标岗位：{job_type}

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
    return _deepseek(prompt)


# ══════════════════════════════════════════════════════════════════
# 新增功能 —— 求职前期
# ══════════════════════════════════════════════════════════════════

def generate_intro(job_type: str, background_text: str) -> str:
    """生成60秒结构化自我介绍（DeepSeek）。"""
    prompt = f"""你是一位专业的面试培训师。请根据以下信息，帮求职者写一段面试自我介绍。

目标岗位：{job_type}
个人背景/简历：
{background_text}

要求：
1. 时长控制在 60 秒左右（约 200～250 字）
2. 结构清晰：简短背景 → 核心经历/技能 → 与岗位的契合点 → 求职意愿
3. 语言自然流畅，不要像在背稿
4. 突出与【{job_type}】最相关的亮点

请直接输出自我介绍正文，然后附上：

【结构拆解】
（标注每部分对应哪个环节，方便求职者理解和记忆）

【提示】
（2～3 条现场注意事项）"""
    return _deepseek(prompt)


def generate_cover_letter(company_name: str, job_type: str, background_text: str) -> str:
    """针对特定公司和岗位生成求职信（DeepSeek）。"""
    prompt = f"""你是一位资深职业顾问，擅长撰写有说服力的求职信。

目标公司：{company_name}
目标岗位：{job_type}
求职者背景：
{background_text}

请写一封结构完整、有针对性的求职信，要求：
1. 开头点明应聘岗位并表明兴趣，提到 {company_name} 的具体吸引点
2. 中间结合背景，重点说明 2～3 个与岗位最匹配的经历/能力
3. 结尾表达期待沟通的意愿
4. 字数 300～400 字，语气专业而不失真诚
5. 不要用模板化套话

请直接输出求职信正文。"""
    return _deepseek(prompt)


def evaluate_match(jd_text: str, resume_text: str) -> str:
    """评估简历与JD的匹配度并打分（DeepSeek）。"""
    prompt = f"""你是一位专业的简历筛选专家。请对以下简历与岗位描述（JD）进行匹配度评估。

【JD 内容】
{jd_text}

【简历内容】
{resume_text}

请输出以下内容：

【匹配度评分】
（满分 100 分，给出分数和一句总体评价）

【匹配亮点】（3～5条）
- 列出简历中与 JD 高度吻合的能力/经历

【主要差距】（3～5条）
- 列出 JD 要求但简历中明显欠缺的部分

【提升建议】
（针对差距，给出 3～5 条投递前可以补充或调整的具体建议）

【综合建议】
（一句话：是否值得投递，以及核心策略）"""
    return _deepseek(prompt)


def search_salary(company_name: str, job_type: str, city: str = "") -> str:
    """搜索岗位薪资范围并给出谈薪建议（Tavily + DeepSeek）。"""
    city_str = city if city else "北京/上海"
    query = f"{company_name} {job_type} 薪资 薪酬 salary 待遇 {city_str} 2024 2025"
    items = _tavily(query, max_results=4)
    search_summary = _format_tavily(items, company_name)

    prompt = f"""你是一位薪资谈判顾问。以下是关于「{company_name}」「{job_type}」薪资的搜索结果：

{search_summary}

请基于以上信息，输出：

【薪资参考范围】
（给出月薪/年薪的参考区间，注明数据来源可信度）

【薪资构成说明】
（说明该岗位薪资通常由哪些部分组成：base、奖金、股票/期权等）

【谈薪建议】
（3～4 条具体的谈薪策略和话术建议）

【注意事项】
（2 条特别提醒）"""
    return _deepseek(prompt)


# ══════════════════════════════════════════════════════════════════
# 新增功能 —— 面试准备
# ══════════════════════════════════════════════════════════════════

def generate_star_answer(question: str, experience: str = "") -> str:
    """用 STAR 结构生成面试题回答（DeepSeek）。"""
    exp_str = f"\n求职者相关经历（供参考）：\n{experience}" if experience.strip() else ""
    prompt = f"""你是一位面试培训专家，擅长用 STAR 法则帮求职者组织面试答案。

面试题目：{question}{exp_str}

请用 STAR 结构生成一段完整的面试回答：

【STAR 结构回答】

**S（Situation - 情境）**
（描述事件背景和当时的处境，2～3句）

**T（Task - 任务）**
（说明你当时面临的具体任务或挑战，1～2句）

**A（Action - 行动）**
（重点：你具体采取了哪些行动，3～5个关键步骤）

**R（Result - 结果）**
（量化结果或影响，1～2句）

【完整回答版本】
（将以上内容整合为自然流畅的面试回答，约150～200字）

【注意事项】
（2条这道题的回答技巧）"""
    return _deepseek(prompt)


def generate_askback_questions(company_name: str, job_type: str) -> str:
    """生成反问面试官的智慧问题（DeepSeek）。"""
    prompt = f"""你是一位面试培训师。请为以下岗位生成 6 个有质量的「反问面试官」问题。

目标公司：{company_name}
目标岗位：{job_type}

要求：
1. 问题要体现求职者的思考深度和对岗位的认真态度
2. 涵盖不同维度：团队/项目/成长/公司文化/岗位期望等
3. 避免问薪资、假期等敏感问题
4. 每个问题附上「为什么问这个」的简要说明

【6 个反问问题】

1. （问题内容）
   → 为什么问：（说明意图）

2. ...

【使用建议】
（2～3 条在面试结尾提问时的注意事项）"""
    return _deepseek(prompt)


def explain_tech_question(question_text: str) -> str:
    """对技术/专业面试题进行解析和答案讲解（DeepSeek）。"""
    prompt = f"""你是一位技术面试专家。请对以下面试题进行详细解析。

题目：
{question_text}

请输出：

【题目考察点】
（这道题考察候选人哪些能力/知识点）

【解题思路】
（分步骤说明如何分析和回答这道题）

【参考答案】
（给出完整的参考回答，语言清晰易懂）

【加分点】
（回答时可以额外提到哪些内容会让面试官印象深刻）

【常见误区】
（回答时要避免的 2～3 个常见错误）"""
    return _deepseek(prompt, max_tokens=2000)


# ══════════════════════════════════════════════════════════════════
# 新增功能 —— 面试复盘
# ══════════════════════════════════════════════════════════════════

def review_interview(question: str, answer: str) -> str:
    """对面试回答进行复盘分析和改进（DeepSeek）。"""
    prompt = f"""你是一位面试教练，擅长帮候选人复盘面试表现。

面试题目：{question}

候选人的回答：
{answer}

请从以下维度进行复盘分析：

【回答评分】
（满分 10 分，给出评分和一句总评）

【亮点分析】
（这段回答中做得好的 2～3 个地方）

【不足之处】
（明确指出 2～3 个可以改进的地方）

【改进版回答】
（基于候选人的原回答，给出优化后的版本，保留原有内容框架，重点改进薄弱环节）

【下次注意】
（2 条可以立即改进的具体建议）"""
    return _deepseek(prompt)


def compare_offers(offer_a: str, offer_b: str) -> str:
    """对比分析多个 offer，给出综合建议（DeepSeek）。"""
    prompt = f"""你是一位职业规划顾问，擅长帮求职者理性分析 offer。

Offer A 信息：
{offer_a}

Offer B 信息：
{offer_b}

请从多个维度进行对比分析：

【对比总览】
（用表格或列表形式，对比两个 offer 的核心指标：薪资/公司规模/发展前景/地点/行业等）

【Offer A 优势与风险】
- 优势：（2～3条）
- 风险/劣势：（1～2条）

【Offer B 优势与风险】
- 优势：（2～3条）
- 风险/劣势：（1～2条）

【综合建议】
（基于以上分析，给出倾向性建议，并说明理由）

【决策参考问题】
（列出 3 个求职者可以问自己的问题，帮助最终做决定）"""
    return _deepseek(prompt)


# ══════════════════════════════════════════════════════════════════
# 新增功能 —— 行业市场
# ══════════════════════════════════════════════════════════════════

def search_industry(industry_name: str) -> str:
    """搜索行业近期动态并生成摘要（Tavily + DeepSeek）。"""
    query = f"{industry_name} 行业动态 趋势 发展 政策 2024 2025"
    items = _tavily(query, max_results=5)
    search_summary = _format_tavily(items, industry_name)

    prompt = f"""你是一位行业研究员。以下是关于「{industry_name}」行业的搜索结果：

{search_summary}

请整理并输出：

【行业近期动态摘要】
（3～5 条重要动态，每条注明意义）

【行业趋势判断】
（2～3 个值得关注的中长期趋势）

【对求职者的启示】
（2～3 条：在面试中如何利用这些行业动态展示你的行业认知）"""
    return _deepseek(prompt)


def compare_companies(company_a: str, company_b: str, company_c: str = "") -> str:
    """搜索并横向对比多家公司（Tavily + DeepSeek）。"""
    companies = [c for c in [company_a, company_b, company_c] if c.strip()]
    company_list = "、".join(companies)

    # 搜索每家公司
    all_info = []
    for company in companies:
        query = f"{company} 公司规模 业务 文化 发展 待遇 2024 2025"
        items = _tavily(query, max_results=2)
        summary = _format_tavily(items, company)
        all_info.append(f"=== {company} ===\n{summary}")

    search_content = "\n\n".join(all_info)

    prompt = f"""你是一位职业规划顾问。以下是关于 {company_list} 的搜索信息：

{search_content}

请对这些公司进行横向对比分析：

【公司对比总览】
（从业务方向、规模、发展阶段、行业地位几个维度对比）

【各公司特点】
（每家公司各 2～3 句核心特点描述）

【求职视角分析】
（从求职者角度，分析各公司的机会与挑战）

【面试备考建议】
（针对每家公司，各给 1～2 条面试备考的差异化建议）"""
    return _deepseek(prompt)
