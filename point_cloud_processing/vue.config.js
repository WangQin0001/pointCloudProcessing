/* eslint-disable */
module.exports = {
  lintOnSave: false, // 全局关闭 eslint
  transpileDependencies: ['@vue/composable'],
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.glsl$/,
          use: 'raw-loader',
        },
      ],
    },
  },
  devServer: {
    port: 8080,//当前vue项目运行在8080端口
    historyApiFallback: true,//确保devserver能处理history模式的路由
    proxy: {
      '/api': { // 假设你的所有后端请求都是以 '/api' 开头的   //必须加！不然会导致网页刷新时报404
        target: 'http://127.0.0.1:8081',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        }
      }
    }
  }
}