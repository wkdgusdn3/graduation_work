function summaryNews(content) {
    $.ajax({
        url: "/summaryUserNews",
        type: "post",
        dataType : "json",
        data: {content:content},
        success: function(data) {
            var innerHTML = data.summaryNews;

            summary_result.innerHTML = "";
            summary_result.innerHTML = innerHTML;
        },
        beforeSend: function(){
            $('.wrap-loading').removeClass('display-none');
        },
        complete: function(){
            $('.wrap-loading').addClass('display-none');
        },
        error: function(data) {
        }
    });
}