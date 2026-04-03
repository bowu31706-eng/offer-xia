# main.py
# FastAPI 后端主程序
# 定义 4 个 HTTP 接口，供微信小程序调用

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

import services

# 加载 .env 文件中的 API Key
load_dotenv()

app = FastAPI(title="职前探 API", version="1.0.0")

# 允许跨域请求（微信小程序调用后端时需要）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── 请求体数据模型（定义每个接口接收什么参数）────────────────────────────────

class SearchRequest(BaseModel):
    company_name: str           # 公司名称，例如 "字节跳动"

class JDRequest(BaseModel):
    jd_text: str                # 完整 JD 文本

class QuestionRequest(BaseModel):
    company_name: str           # 公司名称
    job_type: str = "AI产品经理"  # 岗位名称，默认 AI 产品经理

class ResumeRequest(BaseModel):
    resume_text: str            # 简历文本内容
    job_type: str = "AI产品经理"  # 目标岗位
    company_name: str = ""      # 目标公司（可选）


# ── 提供前端网页 ──────────────────────────────────────────────────────────────
@app.get("/")
def serve_frontend():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "ok", "message": "职前探 API 运行正常"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "职前探 API 运行正常"}


# ── 接口 2：搜索公司动态 ──────────────────────────────────────────────────────
@app.post("/search")
def search_company(req: SearchRequest):
    """
    搜索目标公司的近期动态。
    小程序传入公司名称，返回搜索结果摘要。
    """
    if not req.company_name.strip():
        raise HTTPException(status_code=400, detail="公司名称不能为空")

    result = services.search_company(req.company_name)
    return {"success": True, "data": result}


# ── 接口 3：解析 JD ───────────────────────────────────────────────────────────
@app.post("/analyze-jd")
def analyze_jd(req: JDRequest):
    """
    解析职位描述（JD），提取核心能力要求和关键词。
    小程序传入 JD 文本，返回结构化分析结果。
    """
    if not req.jd_text.strip():
        raise HTTPException(status_code=400, detail="JD 内容不能为空")

    result = services.analyze_jd(req.jd_text)
    return {"success": True, "data": result}


# ── 接口 4：生成面试题 ────────────────────────────────────────────────────────
@app.post("/generate-questions")
def generate_questions(req: QuestionRequest):
    """
    根据公司和岗位生成 10 道高频面试题及备考建议。
    """
    if not req.company_name.strip():
        raise HTTPException(status_code=400, detail="公司名称不能为空")

    result = services.generate_questions(req.company_name, req.job_type)
    return {"success": True, "data": result}


# ── 接口 5：优化简历 ──────────────────────────────────────────────────────────
@app.post("/optimize-resume")
def optimize_resume(req: ResumeRequest):
    """
    分析简历内容，针对目标岗位给出具体优化建议。
    """
    if not req.resume_text.strip():
        raise HTTPException(status_code=400, detail="简历内容不能为空")

    result = services.optimize_resume(req.resume_text, req.job_type, req.company_name)
    return {"success": True, "data": result}


# ── 本地运行入口 ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    # 本地测试时运行：python main.py
    # 访问 http://localhost:8000 查看接口
    # 访问 http://localhost:8000/docs 查看自动生成的接口文档
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
