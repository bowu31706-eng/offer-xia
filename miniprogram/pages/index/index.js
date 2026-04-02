// index.js - 首页逻辑
Page({
  // 跳转到 JD 备考页
  goToJD() {
    wx.switchTab({ url: '/pages/jd/jd' });
  },

  // 跳转到简历优化页
  goToResume() {
    wx.switchTab({ url: '/pages/resume/resume' });
  },
});
