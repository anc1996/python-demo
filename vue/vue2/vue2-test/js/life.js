var app = new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue!'
    },
    // 声明周期钩子,beforeCreate在Observe Data之前开始监控Data对象数据变化
    // 执行顺序：beforeCreate -> created -> beforeMount -> mounted
    beforeCreate:function () {
        console.log('beforeCreate')
    },
    // created在Observe Data之后开始监控Data对象数据变化。
    created:function () {
        console.log('created')
    },
    // beforeMount在挂载之前开始
    beforeMount:function () {
        console.log('beforeMount')
    },
    // mounted在挂载之后开始
    mounted:function () {
        console.log('mounted')
    },
    // 实时监控数据变化，随时更新dom
    // beforeUpdate在更新之前开始
    beforeUpdate:function () {
      console.log('beforeUpdate')
    },
    // updated在更新之后开始
    updated:function (){
      console.log('updated')
    },
    // 销毁前执行，可以做一些清理工作
    // beforeDestroy在销毁之前开始
    beforeDestroy:function () {
        console.log('beforeDestroy')
    },
    // destroyed在销毁之后开始
    destroyed:function () {
        console.log('destroyed')
    }
})