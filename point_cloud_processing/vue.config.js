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
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        // pathRewrite: {
        //   '^/api': ''
        // }
      }

    }
  }
}