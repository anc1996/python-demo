# webpacktest

> webpacktest使用基本方式

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# run unit tests
npm run unit

# run e2e tests
npm run e2e

# run all tests
npm test
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).

这是创建webpack前端代码编写项目的方式
```bash
Vue-cli的使用
我们的项目文件都是手动创建出来，在实际开发中我们可以借助vue-cli创建出我们的所有项目文件

全局安装vue-cli

npm install --global vue-cli
项目创建

vue init webpack 项目名
运行调试项目

// 进入项目目录下，执行下面指令
npm run dev
项目打包

npm run build
```


### 项目结构
- **文件夹1(src)**，主开发目录，要开发的单文件组件全部在这个目录下
- **文件夹2(static)**，静态资源目录，所有的css，js文件放在这个文件夹
- **文件夹3(components)**，组件目录，vue格式的单文件组件都存在这个目录中
- **文件夹4(router)**，路由目录，在此文件夹中配置组件路由
- **还有node_modules目录是node的包目录**，config是配置目录，build是项目打包时依赖的目录。
