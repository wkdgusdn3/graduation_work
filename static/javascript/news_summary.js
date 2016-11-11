// menuBar active 관리
$(document).ready( function () {
    var selected = document.location.pathname;
    
    switch(selected) {
        case "/main" :
        $("li[name='menuBar'][value='0']").addClass('active');
        break;
        case "/search" :
        $("li[name='menuBar'][value='1']").addClass('active');
        break;
        case "/summary" :
        $("li[name='menuBar'][value='2']").addClass('active');
        break;
        case "/summarywithurl" :
        $("li[name='menuBar'][value='3']").addClass('active');
        break;
    }
});