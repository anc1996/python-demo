// 创建Vue对象
let vm=new Vue({
    el:'#app',// 通过id选择器找到绑定的HTML内容
    delimiters: ['[[', ']]'],
    data:{
        // 数据对象
        // v-model
        username:'', // 用户名
        password:'',// 密码
        password2:'',
        mobile:'',// 手机号
        allow:'',// 是否同意协议
        // image_code:'',
        // sms_code:'',//短信验证码内容

        // v-show，Boolean
        error_name:false,//用户名，false表示不显示提示内容
        error_password:false,// 密码，false表示不显示提示内容
        error_password2:false,
        error_mobile:false,// 手机号，false表示不显示提示内容
        error_allow:false,// 是否同意协议，false表示不显示提示内容

         //error_message
        error_name_message:'',// 用户名错误提示
        error_mobile_message:'',// 手机号错误提示
    },
    //定义和实现事件方法
    methods:{
        // 检查用户名
        check_username() {
            //用户名是5-20个字符，[a-zA-Z0-9_-]
            //定义正则
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)) {
                // 匹配成功，不展示错误提示信息
                this.error_name = false;
            }
            // 匹配失败，展示错误提示信息
            else {
                this.error_name_message = '请输入5-20个字符的用户名';
                this.error_name = true;
            }
        },
        // 校验密码
        check_password() {
            //密码是8-20个字符
            //定义正则
            let re=/^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                // 匹配成功，不展示错误提示信息
                this.error_password = false;
            }
            else {
                 this.error_password=true;
            }
        },
        // 校验确认密码
        check_password2(){
            if(this.password==this.password2){
                this.error_password2=false;
            }else {
                this.error_password2=true;
            }
        },
        // 校验手机号
        check_mobile() {
            let re = /^1[3-9]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_mobile = false;
            }
            else {
                this.error_mobile=true;
                this.error_mobile_message = '您输入的手机号格式不正确';
            }
        },


        // 勾选用户协议核查
        check_allow(){
            if(!this.allow){
                this.error_allow=true;
            }else {
                this.error_allow=false;
            }
        },
         // 监听表单提交事件
        on_submit(){
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_allow();

            const errors = [
                this.error_name,
                this.error_password,
                this.error_password2,
                this.error_mobile,
                this.error_allow
            ];

          if (errors.some(error => error === true)) {
            window.event.returnValue = false;
          }
        },
    }
});