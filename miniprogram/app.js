// app.js
// 小程序全局入口文件
// 在这里存放全局变量，比如后端接口地址

App({
  // 全局数据：所有页面都可以通过 getApp().globalData 访问
  globalData: {
    // 后端接口地址
    // 本地测试时用 localhost，部署后换成真实域名
    baseUrl: 'https://offer-xia-production.up.railway.app',
  },

  onLaunch() {
    console.log('offer侠启动');
  },
});
