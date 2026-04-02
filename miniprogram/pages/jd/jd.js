// jd.js - JD 备考分析页逻辑
const api = require('../../utils/api');

Page({
  data: {
    companyName: '',   // 用户输入的公司名
    jdText: '',        // 用户输入的 JD 文本
    jobType: 'AI产品经理', // 岗位类型（固定）

    // 三个步骤各自的加载状态和结果
    step1Loading: false,
    step2Loading: false,
    step3Loading: false,

    companyInfo: '',   // 公司动态搜索结果
    jdAnalysis: '',    // JD 解析结果
    questions: '',     // 面试题生成结果

    // 控制结果区域是否显示
    showResult: false,

    // 当前正在执行的步骤描述（显示在加载动画旁边）
    loadingText: '',
  },

  // 公司名输入事件
  onCompanyInput(e) {
    this.setData({ companyName: e.detail.value });
  },

  // JD 文本输入事件
  onJDInput(e) {
    this.setData({ jdText: e.detail.value });
  },

  // 点击"开始分析"按钮
  async onStartAnalysis() {
    const { companyName, jdText } = this.data;

    // 表单校验
    if (!companyName.trim()) {
      wx.showToast({ title: '请输入公司名称', icon: 'none' });
      return;
    }
    if (!jdText.trim()) {
      wx.showToast({ title: '请粘贴 JD 内容', icon: 'none' });
      return;
    }

    // 清空上次结果，展示结果区域
    this.setData({
      showResult: true,
      companyInfo: '',
      jdAnalysis: '',
      questions: '',
    });

    // 滚动到结果区域
    wx.pageScrollTo({ selector: '#result-section', duration: 300 });

    // ── 步骤一：搜索公司动态 ──────────────────────────────────────────────
    this.setData({ step1Loading: true, loadingText: '正在搜索公司动态...' });
    try {
      const companyInfo = await api.searchCompany(companyName);
      this.setData({ companyInfo, step1Loading: false });
    } catch (err) {
      this.setData({
        companyInfo: `搜索失败：${err.message}`,
        step1Loading: false,
      });
    }

    // ── 步骤二：解析 JD ───────────────────────────────────────────────────
    this.setData({ step2Loading: true, loadingText: '正在解析 JD...' });
    try {
      const jdAnalysis = await api.analyzeJD(jdText);
      this.setData({ jdAnalysis, step2Loading: false });
    } catch (err) {
      this.setData({
        jdAnalysis: `解析失败：${err.message}`,
        step2Loading: false,
      });
    }

    // ── 步骤三：生成面试题 ────────────────────────────────────────────────
    this.setData({ step3Loading: true, loadingText: '正在生成面试题...' });
    try {
      const questions = await api.generateQuestions(companyName, this.data.jobType);
      this.setData({ questions, step3Loading: false, loadingText: '' });
    } catch (err) {
      this.setData({
        questions: `生成失败：${err.message}`,
        step3Loading: false,
        loadingText: '',
      });
    }

    wx.showToast({ title: '分析完成！', icon: 'success' });
  },

  // 复制全部结果到剪贴板
  onCopyAll() {
    const { companyName, companyInfo, jdAnalysis, questions } = this.data;
    const fullText = `【${companyName} 备考报告】\n\n【公司动态】\n${companyInfo}\n\n${jdAnalysis}\n\n${questions}`;
    wx.setClipboardData({
      data: fullText,
      success: () => wx.showToast({ title: '已复制到剪贴板', icon: 'success' }),
    });
  },

  // 清空重来
  onReset() {
    this.setData({
      companyName: '',
      jdText: '',
      companyInfo: '',
      jdAnalysis: '',
      questions: '',
      showResult: false,
    });
    wx.pageScrollTo({ scrollTop: 0, duration: 300 });
  },
});
