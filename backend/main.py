# main.py
# FastAPI 后端主程序 — 职前探 全部 15 个功能接口

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

import services

load_dotenv()

app = FastAPI(title="职前探 API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── 请求体数据模型 ────────────────────────────────────────────────────────────

# 原有
class SearchRequest(BaseModel):
    company_name: str

class JDRequest(BaseModel):
    jd_text: str

class QuestionRequest(BaseModel):
    company_name: str
    job_type: str = "AI产品经理"

class ResumeRequest(BaseModel):
    resume_text: str
    job_type: str = "AI产品经理"
    company_name: str = ""

# 求职前期
class IntroRequest(BaseModel):
    job_type: str
    background_text: str

class CoverLetterRequest(BaseModel):
    company_name: str
    job_type: str
    background_text: str

class MatchRequest(BaseModel):
    jd_text: str
    resume_text: str

class SalaryRequest(BaseModel):
    company_name: str
    job_type: str
    city: str = ""

# 面试准备
class StarRequest(BaseModel):
    question: str
    experience: str = ""

class AskBackRequest(BaseModel):
    company_name: str
    job_type: str

class TechRequest(BaseModel):
    question_text: str

# 面试复盘
class ReviewRequest(BaseModel):
    question: str
    answer: str

class OfferRequest(BaseModel):
    offer_a: str
    offer_b: str

# 行业市场
class IndustryRequest(BaseModel):
    industry_name: str

class CompeteRequest(BaseModel):
    company_a: str
    company_b: str
    company_c: str = ""


# ── 前端托管 ──────────────────────────────────────────────────────────────────

@app.get("/")
def serve_frontend():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "ok", "message": "职前探 API 运行正常"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "职前探 API 运行正常", "version": "2.0.0"}


# ── 原有四个接口 ──────────────────────────────────────────────────────────────

@app.post("/search")
def search_company(req: SearchRequest):
    if not req.company_name.strip():
        raise HTTPException(status_code=400, detail="公司名称不能为空")
    return {"success": True, "data": services.search_company(req.company_name)}


@app.post("/analyze-jd")
def analyze_jd(req: JDRequest):
    if not req.jd_text.strip():
        raise HTTPException(status_code=400, detail="JD 内容不能为空")
    return {"success": True, "data": services.analyze_jd(req.jd_text)}


@app.post("/generate-questions")
def generate_questions(req: QuestionRequest):
    if not req.company_name.strip():
        raise HTTPException(status_code=400, detail="公司名称不能为空")
    return {"success": True, "data": services.generate_questions(req.company_name, req.job_type)}


@app.post("/optimize-resume")
def optimize_resume(req: ResumeRequest):
    if not req.resume_text.strip():
        raise HTTPException(status_code=400, detail="简历内容不能为空")
    return {"success": True, "data": services.optimize_resume(req.resume_text, req.job_type, req.company_name)}


# ── 求职前期 ──────────────────────────────────────────────────────────────────

@app.post("/intro")
def generate_intro(req: IntroRequest):
    if not req.job_type.strip():
        raise HTTPException(status_code=400, detail="目标岗位不能为空")
    if not req.background_text.strip():
        raise HTTPException(status_code=400, detail="请填写个人背景")
    return {"success": True, "data": services.generate_intro(req.job_type, req.background_text)}


@app.post("/cover-letter")
def generate_cover_letter(req: CoverLetterRequest):
    if not req.company_name.strip() or not req.job_type.strip():
        raise HTTPException(status_code=400, detail="公司名称和目标岗位不能为空")
    if not req.background_text.strip():
        raise HTTPException(status_code=400, detail="请填写个人背景")
    return {"success": True, "data": services.generate_cover_letter(req.company_name, req.job_type, req.background_text)}


@app.post("/match")
def evaluate_match(req: MatchRequest):
    if not req.jd_text.strip():
        raise HTTPException(status_code=400, detail="JD 内容不能为空")
    if not req.resume_text.strip():
        raise HTTPException(status_code=400, detail="简历内容不能为空")
    return {"success": True, "data": services.evaluate_match(req.jd_text, req.resume_text)}


@app.post("/salary")
def search_salary(req: SalaryRequest):
    if not req.company_name.strip() or not req.job_type.strip():
        raise HTTPException(status_code=400, detail="公司名称和目标岗位不能为空")
    return {"success": True, "data": services.search_salary(req.company_name, req.job_type, req.city)}


# ── 面试准备 ──────────────────────────────────────────────────────────────────

@app.post("/star")
def generate_star(req: StarRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="请输入面试题目")
    return {"success": True, "data": services.generate_star_answer(req.question, req.experience)}


@app.post("/askback")
def generate_askback(req: AskBackRequest):
    if not req.company_name.strip() or not req.job_type.strip():
        raise HTTPException(status_code=400, detail="公司名称和目标岗位不能为空")
    return {"success": True, "data": services.generate_askback_questions(req.company_name, req.job_type)}


@app.post("/tech")
def explain_tech(req: TechRequest):
    if not req.question_text.strip():
        raise HTTPException(status_code=400, detail="请输入题目内容")
    return {"success": True, "data": services.explain_tech_question(req.question_text)}


# ── 面试复盘 ──────────────────────────────────────────────────────────────────

@app.post("/review")
def review_interview(req: ReviewRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="请输入面试题目")
    if not req.answer.strip():
        raise HTTPException(status_code=400, detail="请输入你的回答")
    return {"success": True, "data": services.review_interview(req.question, req.answer)}


@app.post("/offer")
def compare_offers(req: OfferRequest):
    if not req.offer_a.strip() or not req.offer_b.strip():
        raise HTTPException(status_code=400, detail="请填写至少两个 offer 信息")
    return {"success": True, "data": services.compare_offers(req.offer_a, req.offer_b)}


# ── 行业市场 ──────────────────────────────────────────────────────────────────

@app.post("/industry")
def search_industry(req: IndustryRequest):
    if not req.industry_name.strip():
        raise HTTPException(status_code=400, detail="行业名称不能为空")
    return {"success": True, "data": services.search_industry(req.industry_name)}


@app.post("/compete")
def compare_companies(req: CompeteRequest):
    if not req.company_a.strip() or not req.company_b.strip():
        raise HTTPException(status_code=400, detail="请至少填写两家公司")
    return {"success": True, "data": services.compare_companies(req.company_a, req.company_b, req.company_c)}


# ── 本地运行入口 ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
