function comment_cr(){
    const comment = $("#post-comment").val();
    console.log(comment);

    $.ajax({
        type: "POST",
        url: "/api/comment",
        data: {comment: comment},
        success: function (response) { 
            if (response["result"] == "success") { 
                console.log('작성완료')
            }else{
                alert(response['msg2'])
            }
            
        }
    })

}