

// 检查邮箱格式
function checkEmailFormat(inputId, errorSpanId) {
   let email = $(inputId).val();
   let errorSpan = $(inputId).next(errorSpanId);
   if (!/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}/.test(email)) {
       errorSpan.css({'color': 'red', 'font-size': '10px'});
       errorSpan.text('邮箱格式不正确');
       return false;
   } else {
       errorSpan.text('');
       return true;
   }
}



// 检查输入是否为空
function checkEmptyInput(inputId, errorSpanId, errorMessage) {
    let value = $(inputId).val();
    let errorSpan = $(inputId).next(errorSpanId);
    if (!value) {
        errorSpan.css({ 'color': 'red', 'font-size': '10px' });
        errorSpan.text(errorMessage);
        return false;
    } else {
        errorSpan.text('');
        return true;
    }
}

// 检查手机号格式
function checkPhoneFormat(inputId, errorSpanId) {
    let phone = $(inputId).val();
    let errorSpan = $(inputId).next(errorSpanId);
    if (!/^1[3456789]\d{9}$/.test(phone)) {
        errorSpan.css({ 'color': 'red', 'font-size': '10px' });
        errorSpan.text('手机号码格式不正确');
        return false;
    } else {
        errorSpan.text('');
        return true;
    }
}

//  检查验证码格式
function checkCodeFormat(inputId, errorSpanId) {
    let code = $(inputId).val();
    let errorSpan = $(this).next(errorSpanId);
    if (!/^\d{6}$/.test(code)) {
        errorSpan.addClass('error');
        errorSpan.text('验证码格式不正确');
        return false;
    } else {
        errorSpan.removeClass('error');
        errorSpan.text('');
        return true;
    }
}
// 检查年龄格式
function checkAgeFormat(inputId, errorSpanId) {
    let age = $(inputId).val();
    let errorSpan = $(inputId).next(errorSpanId);
    if (!/^\d{1,3}$/.test(age)) {
        errorSpan.addClass('error');
        errorSpan.text('年龄格式不正确');
        return false;
    } else {
        errorSpan.removeClass('error');
        errorSpan.text('');
        return true;
    }
}



// 倒计时函数
function startCountdown() {
    let countdown = 60;
    $('#send-code-btn').prop('disabled', true);
    $('#send-code-btn').text(countdown + '秒后重试');

    let timer = setInterval(function() {
        countdown--;
        $('#send-code-btn').text(countdown + '秒后重试');

        if (countdown <= 0) {
            clearInterval(timer);
            $('#send-code-btn').prop('disabled', false);
            $('#send-code-btn').text('发送验证码');
        }
    }, 1000);
}

