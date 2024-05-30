# 单文件组件组测

(python39) PS E:\source\python\python_Web_Development\demo\vue\FileDemo> dir


    目录: E:\source\python\python_Web_Development\demo\vue\FileDemo


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         2024/5/27     17:06                .vscode 
d-----         2024/5/28     19:08                components # 组件
d-----         2024/5/27     12:50                node_modules # 第三方包
-a----         2024/5/28     19:19            634 App.vue # 根组件
-a----         2024/5/27     18:56            902 index.html # 入口页面
-a----         2024/5/27     18:55         340912 index.js # 入口文件
-a----         2024/5/27     17:13            179 main.js # 程项目打包的入口文件
-a----         2024/5/27     12:50         354363 package-lock.json # 
-a----         2024/5/27     17:33            844 package.json # npm管理包
-a----         2024/5/27     19:56           1581 webpack.config.js # webpack配置文件

# 环境配置

单文件组件不能直接运行使用，需要依赖node项目对其进行解析打包，在使用之前需要先进行环境配置

1. 安装node版本管理工具nvm

   1. ```shell
      curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
      // 更新配置
      source .bashrc
      ```

2. 安装最新版本的node

   1. ```shell
      nvm install node
      ```

3. 更新npm的安装源

   1. ```shell
      npm config set registry https://registry.npm.taobao.org
      ```

4. 创建项目目录

   1. ```shell
      mkdir project
      ```

5. 进入项目目录，初始化项目目录

   1. ```shell
      cd project
      npm init
      ```

### 项目打包

文件编写完成后并不能直接运行index.html产生效果，需要对项目进行打包生成一个渲染后的index.js文件进行使用

```shell
npm run build
```

打包后会在当前目录下生成一个index.js 文件，在index.html中引用该文件，运行index.html文件看到效果

### 项目调试运行

每次我们需要看到组件效果需要手动生成一个index.js文件，这是我们可以借助webpack-dev-server自动运行我们的代码

```shell
// 在项目目录下，执行下面指令可以开启前端服务，自动运行前端代码
./node_modules/.bin/webpack-dev-server
```