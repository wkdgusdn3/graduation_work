function summaryNewsWithUrl(url) {
    $.ajax({
        url: "/summaryNewsWithUrl",
        type: "post",
        dataType : "json",
        data: {url:url},
        success: function(data) {
            content.innerHTML = data.content;
            summaryContent.innerHTML = data.summaryContent;
        },
        beforeSend: function(){
            $('.wrap-loading').removeClass('display-none');
        },
        complete: function(){
            $('.wrap-loading').addClass('display-none');
        },
        error: function(data) {
            alert("error")
        }
    });
}