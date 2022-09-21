
// 회원가입 버튼 함수
function post_signup() {
    const id = $("#post-signup-id").val();
    const pass = $("#post-signup-pw1").val();
    const pass2 = $("#post-signup-pw2").val();
    const name = $("#post-signup-name").val();

    if(id == ''){
        alert("아이디를 입력하여 주세요.");
        return
    }else if(pass == ''){
        alert("비밀번호를 입력하여 주세요.")
        return
    }else if(pass2 == ''){
        alert("비밀번호를 입력하여 주세요.")
        return
    }else if(name == ''){
        alert("이름을 입력하여 주세요.")
        return
    }


    $.ajax({
        type: "POST",
        url: "/signup",
        data: {url_id: id, url_pw: pass, url_pw2: pass2, url_name: name},
        success: function (response) { 
            if (response["result"] == "success") {                
                alert('회원가입이 완료 되었습니다.')
                
                location.href = '/'
            }else if(response["result"] == "fail"){
                alert(response['msg'])
            }else{
                alert(response['msg2'])
            }
            
        }
    })

}

function cen(){
    location.href = '/'
}


//아이디 실시간 중복체크
function checkId() {
    const id = $("#post-signup-id").val();

    $.ajax({
        type: "POST",
        url: "/id_check",
        data: {url_id: id},
        success: function (response) { // 성공하면
            if (response["result"] == "success") {
                $('#checkid').html("사용불가능한 아이디 입니다.")
                $('#checkid').css('color', 'red')
                
            }else if(response["result"] == "bb"){
                
                $('#checkid').html("사용가능한 아이디 입니다.")
                $('#checkid').css('color', 'blue')
                
            }else{
                alert("서버오류!")
            }
        }
    })

}


//실시간 비밀번호 중복 체크
function passwordCheckFunction(){
    var password1 = $("#post-signup-pw1").val();
    var password2 = $("#post-signup-pw2").val();
    if(password1 != password2){
        $("#checkMessage").html("비밀번호가 일치하지 않습니다.");
    } else {
        $("#checkMessage").html("");
    }
}
