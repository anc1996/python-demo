import Vue from "vue";
import App from './App.vue';
import router from './routers/router.js';
// 引入ElementUI
import ElementUI from 'element-ui';
// 引入css
import 'element-ui/lib/theme-chalk/index.css';
// 使用ElementUI
Vue.use(ElementUI)

new Vue({
    el:'#app',
    // 注册路由
    router,
   // 渲染App组件中的内容，返回给index.html文件使用，挂载到#app上
    render:function(create){
        return create(App)
    }
})