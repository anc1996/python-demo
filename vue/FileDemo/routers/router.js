import Vue from 'vue'
import Router from 'vue-router'
import Child1 from '../components/Child1.vue'
import Child2 from '../components/Child2.vue'

// 1. 定义（路由）组件。
Vue.use(Router)
// 2. 定义路由规则
export default new Router({
    routes: [
        {
            path: '/child1',
            component: Child1
        },
        {
            path: '/child2',
            component: Child2
        }
    ]
})