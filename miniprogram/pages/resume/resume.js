// resume.js - 简历优化页逻辑
const api = require('../../utils/api');

Page({
  data: {
    resumeText: '',       // 简历文本
    companyName: '',      // 目标公司（可选）
    jobType: 'AI产品经理', // 目标岗位

    isLoading: false,     // 是否正在请求中
    result: '',           // AI 返回的优化建议
    showResult: false,    // 是否展示结果区域
  },

  onResumeInput(e) {
    this.setData({ resumeText: e.detail.value });
  },

  onCompanyInput(e) {
    this.setData({ companyName: e.detail.value });
  },

  // 点击"开始优化"
  async onStartOptimize() {
    const { resumeText, companyName, jobType } = this.data;

    if (!resumeText.trim()) {
      wx.showToast({ title: '请粘贴简历内容', icon: 'none' });
      return;
    }

    this.setData({ isLoading: true, showResult: true, result: '' });
    wx.pageScrollTo({ selector: '#resume-result', duration: 300 });

    try {
      const result = await api.optimizeResume(resumeText, jobType, companyName);
      this.setData({ result, isLoading: false });
      wx.showToast({ title: '优化完成！', icon: 'success' });
    } catch (err) {
      this.setData({
        result: `优化失败：${err.message}\n\n请检查网络连接或联系开发者。`,
        isLoading: false,
      });
    }
  },

  // 复制优化建议
  onCopyResult() {
    wx.setClipboardData({
      data: this.data.result,
      success: () => wx.showToast({ title: '已复制', icon: 'success' }),
    });
  },

  // 清空重来
  onReset() {
    this.setData({
      resumeText: '',
      companyName: '',
      result: '',
      showResult: false,
    });
    wx.pageScrollTo({ scrollTop: 0, duration: 300 });
  },
});
