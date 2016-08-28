function searchKeyword() {
	var keyword =  $("#keyword").val();

	$.ajax({
		url: "/search",
		type: "post",
		dataType : "json",
		data: {keyword:keyword},
		success: function(data) {
			var innerHTML = "";

			for(var i=0; i<data.rows.length; i++) {
				innerHTML += "<a>";				
				innerHTML += data.rows[i][3];
				innerHTML += "</a> <br>";
			}

			search_result.innerHTML = innerHTML;
		},
		error: function(data) {
			alert("키워드 등록에 실패하였습니다.")
		}
	});
}

function registerKeyword1() {
	var seq = $("#seq").val();
	var keyword = $("#keyword").val();
	var company = $("#company").val();

	$.ajax({
		url: "/register_keyword/insert",
		type: "post",
		dataType : "json",
		data: {seq:seq, keyword:keyword, company:company},
		success: function(data) {
			alert("키워드를 등록하였습니다.");
			$("#keyword").val("");
		},
		error: function(data) {
			alert("키워드 등록에 실패하였습니다.")
		}
	});
}

