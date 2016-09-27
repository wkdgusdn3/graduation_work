// menuBar active 관리
$(document).ready( function () {
    var selected = document.location.pathname;
    
    switch(selected) {
        case "/main" :
        $("li[name='menuBar'][value='0']").addClass('active');
        break;
        case "/news_search" :
        $("li[name='menuBar'][value='1']").addClass('active');
        break;
        case "/news_summary" :
        $("li[name='menuBar'][value='2']").addClass('active');
        break;
    }
});

function summaryNews(content) {
    $.ajax({
        url: "/summaryUserNews",
        type: "post",
        dataType : "json",
        data: {content:content},
        success: function(data) {
            var innerHTML = data.summaryNews;
            alert(innerHTML);
        },
        error: function(data) {
        }
    });
}