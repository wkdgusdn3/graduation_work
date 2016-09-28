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
        error: function(data) {
        }
    });
}