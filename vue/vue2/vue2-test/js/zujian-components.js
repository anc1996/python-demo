



// 局部组件定义c,嵌到局部组件a中
var jvbuzujian_c={
    template:'<div>局部组件定义c</div>'
}


// 局部组件定义a
var jvbuzujian_a={
    template: '<div>局部组件定义a,{{age}},局部使用全局变更量:{{pro}},' +
            '<button @click="upload">上传给信息父组件</button>' +
            '<jvbuzujian_c></jvbuzujian_c>' +
        '</div>',
    data:function () {
        return {age:18}
    },
    props:['pro'], //定义接受父组件的变量值。当前的父组件为全局组件
    // 定义传值父组件的方法
    methods:{
        upload:function () {
            // 触发当前实例上的事件。附加参数都会传给监听器回调。vm.$emit( eventName, […args] )
            this.$emit('listen',this.age)
        }
    },
    // 将局部组件注册到全局组件中
    components:{
        // 要先定义局部组件c，意思在局部组件a前。才能加载。
        jvbuzujian_c,
    }
}

// 局部组件定义b
var jvbuzujian_b={
    template:'<div>局部组件定义b</div>'
}

// 全局注册的组件可以用在其被注册之后的任何 (通过 new Vue) 新创建的 Vue 根实例，也包括其组件树中的所有子组件的模板中。
// 全局组件定义,
Vue.component(
    // 组件名定义
    'component-all', {
        // 封装代码。加载局部组件
        template:'<div>全局组件定义,{{name}}.' +
                    '<jvbuzujian_b></jvbuzujian_b>  ' +
                    '<jvbuzujian_a v-bind:pro="name" v-on:listen="isShow"></jvbuzujian_a>  ' +
                    '<button @click="add">定义父组件add方法</button> ' +
                '</div>',
        // 将局部组件注册到全局组件中
        components:{
            jvbuzujian_a,
            jvbuzujian_b,
        },
        //组件定义绑定数据
        // 一个组件的 data 选项必须是一个函数，因此每个实例可以维护一份被返回对象的独立的拷贝：
        data: function () {
            return {name: 'django'}
        },
        methods:{
            add:function (){
                alert('定义父组件add方法')
            },
            isShow:function (data){
                // data接受局部组件变量值
                alert(data)
            }
        }
    }
)
new Vue({
    el:'#app',
    data:{
        name:'python'
    },
    methods: {
        add:function (){
            alert('add')
        }
    }
})