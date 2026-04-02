// utils/api.js
// 封装所有后端 API 请求
// 所有页面通过 import api from '../../utils/api' 调用，不用重复写请求代码

const app = getApp();

/**
 * 基础请求函数：封装 wx.request，返回 Promise
 * @param {string} path   接口路径，例如 '/search'
 * @param {object} data   请求体数据
 */
function request(path, data) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: app.globalData.baseUrl + path,
      method: 'POST',
      data: data,
      header: { 'Content-Type': 'application/json' },
      success(res) {
        if (res.statusCode === 200 && res.data.success) {
          resolve(res.data.data);
        } else {
          // 后端返回了错误信息
          const msg = res.data?.detail || res.data?.message || '请求失败，请稍后重试';
          reject(new Error(msg));
        }
      },
      fail(err) {
        // 网络层错误（断网、域名不通等）
        reject(new Error('网络连接失败，请检查网络后重试'));
      },
    });
  });
}

// ── 导出 4 个业务接口 ──────────────────────────────────────────────────────

/** 搜索公司动态 */
function searchCompany(companyName) {
  return request('/search', { company_name: companyName });
}

/** 解析 JD */
function analyzeJD(jdText) {
  return request('/analyze-jd', { jd_text: jdText });
}

/** 生成面试题 */
function generateQuestions(companyName, jobType = 'AI产品经理') {
  return request('/generate-questions', {
    company_name: companyName,
    job_type: jobType,
  });
}

/** 优化简历 */
function optimizeResume(resumeText, jobType = 'AI产品经理', companyName = '') {
  return request('/optimize-resume', {
    resume_text: resumeText,
    job_type: jobType,
    company_name: companyName,
  });
}

module.exports = {
  searchCompany,
  analyzeJD,
  generateQuestions,
  optimizeResume,
};
