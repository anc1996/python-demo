'use strict'
// Template version: 1.3.1
// see http://vuejs-templates.github.io/webpack for documentation.

const path = require('path')

module.exports = {
  dev: {
    // Paths
    assetsSubDirectory: 'static', // assets的子目录
    assetsPublicPath: '/', // assets的公共路径
    proxyTable: {
    },
    // Various Dev Server settings
    host: '192.168.20.2', // can be overwritten by process.env.HOST
    port: 8080, // 可以被 process.env.PORT 覆盖，如果端口正在使用中，将确定一个空闲的
    autoOpenBrowser: false, // 是否自动打开浏览器
    errorOverlay: true,  // 是否显示错误
    notifyOnErrors: true, // 是否显示错误
    poll: false, // https://webpack.js.org/configuration/dev-server/#devserver-watchoptions-
    /**
     * Source Maps
     */

    // https://webpack.js.org/configuration/devtool/#development
    devtool: 'cheap-module-eval-source-map', // devtool的配置

    // If you have problems debugging vue-files in devtools,
    // set this to false - it *may* help
    // https://vue-loader.vuejs.org/en/options.html#cachebusting
    cacheBusting: true, // 是否缓存

    cssSourceMap: true // 是否开启cssSourceMap
  },

  build: {
    // Template for index.html
    index: path.resolve(__dirname, '../dist/index.html'), // index的路径

    // Paths
    assetsRoot: path.resolve(__dirname, '../dist'), // assets的根路径
    assetsSubDirectory: 'static', // assets的子目录
    assetsPublicPath: '/', // assets的公共路径

    /**
     * Source Maps
     */

    productionSourceMap: true, // 是否开启生产环境的sourceMap
    // https://webpack.js.org/configuration/devtool/#production
    devtool: '#source-map', // devtool的配置

    // Gzip off by default as many popular static hosts such as
    // Surge or Netlify already gzip all static assets for you.
    // Before setting to `true`, make sure to:
    // npm install --save-dev compression-webpack-plugin
    productionGzip: false, // 是否开启生产环境的gzip
    productionGzipExtensions: ['js', 'css'], // gzip的文件类型

    // Run the build command with an extra argument to
    // View the bundle analyzer report after build finishes:
    // `npm run build --report`
    // Set to `true` or `false` to always turn it on or off
    bundleAnalyzerReport: process.env.npm_config_report // 是否开启bundleAnalyzerReport
  }
}
