function post_signup() {
    const id = $("#post-signup-id").val();
    const pw = $("#post-signup-pw").val();

    $.ajax({
        type: "POST",
        url: "/memo",
        data: {url_give: url, comment_give: comment},
        success: function (response) { // 성공하면
            if (response["result"] == "success") {
                alert("포스팅 성공했어");
                window.location.reload(); //성공했을떄 페이지 리로드
            }else{
                alert("서버오류!!!!!!!")
            }
        }
    })
}