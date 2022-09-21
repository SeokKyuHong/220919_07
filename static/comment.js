// window.onload = funtion(){
//     const abcd = $("#board_no").text();
//     if(abcd == ){

//     }
// }

function comment_cr(nnn){
    const comment = $("#post-comment").val();
    
    

    $.ajax({
        type: "POST",
        url: "/api/comment",
        data: {comment: comment, ojid: nnn},
        success: function (response) { 
            if (response["result"] == "success") { 
                alert("댓글 등록 완료")
                document.location.reload(true);
                
            }else{
                alert('오류')
            }
            
        }
    })

}


