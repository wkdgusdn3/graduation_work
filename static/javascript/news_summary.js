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