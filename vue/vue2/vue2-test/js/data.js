

var vue=new Vue({
    //接管元素
    el:'#app',
    //data为双向绑定数据
    data: {
        message: '百度',
        counter:1,
        total:0,
        hello: 'hello,Good Boy!',
        url: 'http://www.baidu.com',
        showmessage: '当前时间是：' + new Date().toDateString(),
        isLogin: true, /*为true显示内容*/
        level: 0,
        isButtonDisabled:true,
        seen: false,
        items: ['python', 'mysql', 'linux', 'redis', 'javascript', 'css'],
        todos: [
            {text: '学习 JavaScript'},
            {text: '学习 Vue'},
            {text: '整个牛X项目'}
        ],
        object: {
            title: 'How to do lists in Vue',
            author: 'Jane Doe',
            publishedAt: '2016-04-10'
        },
        listdict: [
            {
                title: 'Vue',
                author: 'Jane Doe',
                publishedAt: '2016-04-10'
            },
            {
                title: 'python',
                author: 'Ricky',
                publishedAt: '2019-04-10'
            },
            {
                title: 'itcast',
                author: 'itcast',
                publishedAt: '2006-05-08'
            }
        ],
        message1:'hello',
        username:'',
        password1:'',
        password2:'',
        sex:'',
        like:[], //checkbox建议选用列表
        city:'',
        desc:'',
        classevent: ['学习html','学习python','mysql'],
        newitem:'',
    },
    // methods方法
    methods:{
        login:function(){
            alert('我被点击了')
        },
        register:function () {
            alert('注册按钮')
        },
        addnum:function (counter) {
            //this表示当前的vue，我们通过this.total来获取data中的变量
            this.total+=counter;
            alert(this.total);
        },
        register1:function () {
            if(this.password1==this.password2){
                console.log('注册成功')
            }
            console.log(this.username+','+this.password1+','
                +this.sex+','+this.like+','+this.city+','+this.desc)
        },
        checkusername:function () {
            console.log('用户名：'+this.username)
        },
        add:function () {
            this.classevent.push(this.newitem);
            this.newitem='';
        },
        // 删除列表元素
        deleteclassevent:function (index) {
            this.classevent.splice(index,1)
        },
        // 列表元素上移动
        up:function (index) {
            // 1.获取当前的元素
            current=this.classevent[index]
            // 2.先把当前的元素删除
            this.classevent.splice(index,1)
            // 3.再添加,添加的时候让它的索引-1
            this.classevent.splice(index-1,0,current)
        },
        // 列表元素下移
        down:function (index) {
            // 1.获取当前的元素
            current=this.classevent[index]
            // 2.先把当前的元素删除
            this.classevent.splice(index,1)
            // 3.再添加,添加的时候让它的索引+1
            this.classevent.splice(index+1,0,current)
        }
    },
})