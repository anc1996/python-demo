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
        image_code:'',// 图形验证码
        sms_code:'',//短信验证码内容
        sms_code_tip:'获取短信验证码',//短音验证码消息

        // v-show，Boolean
        error_name:false,//用户名，false表示不显示提示内容
        error_password:false,// 密码，false表示不显示提示内容
        error_password2:false,
        error_mobile:false,// 手机号，false表示不显示提示内容
        error_allow:false,// 是否同意协议，false表示不显示提示内容
        error_image_code:false,// 图形验证码，false表示不显示提示内容
        error_sms_code:false, // 短信验证码，false表示不显示内容


        // 加锁开关
        send_flag:false, // 控制短信发送验证的频率。false表示可以点击

         //error_message
        error_name_message:'',// 用户名错误提示
        error_mobile_message:'',// 手机号错误提示
        error_image_code_message:'',// 图形验证码错误提示
        error_sms_code_message:'', // 输入短信验证码错误提示


         // 图形验证码url绑定
        image_code_url:'', // 图形验证码url
        uuid:'', // 图形验证码唯一标识
    },
    // vue生命周期，页面挂载元素都加载完后
    mounted(){
        // 生成图形验证码
        this.generate_image_code();
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
            //判断用户名是否重复注册
            if(this.error_name==false){
                let url='/usernames/'+this.username+'/count/';
                axios.get(url,{
                    responseType:'json'
                })
                    .then(response=>{
                        if(response.data.count >0 ){
                            this.error_name_message='用户名已存在';
                            this.error_name=true;
                        }else {
                            this.error_name=false;
                        }
                    })
                    .catch(error=>{
                        console.log(error.response);
                    });
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
            //判断手机是否重复注册
            if(this.error_mobile==false){
                let url='/mobiles/'+this.mobile+'/count/';
                axios.get(url,{
                    responseType:'json'
                })
                    .then(response=>{
                        if(response.data.count >0 ){
                            this.error_mobile_message='手机号已存在';
                            this.error_mobile=true;
                        }else {
                            this.error_mobile=false;
                        }
                    })
                    .catch(error=>{
                        console.log(error.response);
                    });
            }
        },
        //生成图形验证码的方法：封装思想，代码服用
        generate_image_code(){
            this.uuid=generateUUID();
            this.image_code_url='/image_codes/'+this.uuid+'/';
        },
        // 校验图形验证码
        check_image_code(){
            if(this.image_code.length!=4){
                this.error_image_code_message='输入图形验证码长度不是4位';
                this.error_image_code=true;
            }else {
                this.error_image_code=false;
            }
        },
        // 校验短信验证码
        check_sms_code(){
            if(this.sms_code.length!=4){
                this.error_sms_code_message = '请输入4位短信验证码';
                this.error_sms_code = true;
            }
            else {
                this.error_sms_code_message = '';
                this.error_sms_code = false;
            }
        },

        // 发送短信验证码
        send_sms_code(){
            // 避免恶意用户频繁的点击获取短信验证码
            // 如果send_flag=true，不能点击按钮，该按钮已上锁
            if(this.send_flag==true)
            { return }
            //没有，可以进入，同时上锁。
            this.send_flag=true;
            this.check_mobile();
            this.check_image_code();
            if (this.error_mobile==true || this.check_image_code==true)
            {
                this.send_flag=false; // 解锁
                return;
            }
            let url='/sms_codes/' + this.mobile + '/?image_code=' + this.image_code+'&uuid='+ this.uuid;
            axios.get(url,{responseType:'json'})
                .then(response=>{
                    // 后端返回RETCODE.OK=0
                    if(response.data.code=='0') {
                        //展示倒计时60秒
                        // setInterval('回调函数','时间间隔')，定时器
                        let time_count=60;
                        let t=setInterval(()=>{
                            //倒计时结束
                            if (time_count==1){
                                // 停止回调函数执行
                                clearInterval(t);
                                //还原sms_code_tip的提示文字
                                this.sms_code_tip='重新获取短信验证码'
                                // 重新生成图形验证码
                                this.generate_image_code();
                                this.send_flag=false; // 解锁
                            }
                            //正在倒计时
                            else {
                                time_count=time_count-1;
                                this.sms_code_tip=time_count+'秒';
                            }
                        },1000)
                    }
                    else {
                        // RETCODE.IMAGECODEERR=4001，输入图形验证码错误或失效
                        if(response.data.code=='4001'){
                            this.error_image_code_message=response.data.errmsg;
                            this.error_image_code=true;
                        }
                        // RETCODE.THROTTLINGERR=4002，发送短信验证码频繁
                        if(response.data.code=='4002')
                        {
                            this.error_image_code_message=response.data.errmsg;
                            this.error_image_code=true;
                        }
                        this.send_flag=false; // 解锁
                    }
                })
                .catch(error=>{
                    console.log(error.response);
                    this.send_flag=false;  // 解锁
                })
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
            this.check_sms_code();
            const errors = [
                this.error_name,
                this.error_password,
                this.error_password2,
                this.error_mobile,
                this.error_allow,
                this.error_sms_code,
            ];

          if (errors.some(error => error === true)) {
            window.event.returnValue = false;
          }
        },
    }
});