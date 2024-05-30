import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/', // 路由路径
      name: 'HelloWorld',// 路由名称
      component: HelloWorld // 路由组件
    }
  ]
})
