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
				var oneItem = data.rows[i];

				innerHTML += "<li class='article show' id=<%=" + oneItem[0] + "%>";
				innerHTML += "<p class='q' onclick='searchSummaryResult(" + oneItem[0] + ")'" + "><a>Q: " + oneItem[3] + "</a></p>";
				innerHTML += "<p class='a' style='display: none;' ><div id = 'summary" + oneItem[0] + "'></div></p></li>";

			}

			search_keyword_result.innerHTML = innerHTML;
		},
		error: function(data) {
		}
	});
}

function searchSummaryResult(seq) {
		$.ajax({
		url: "/searchSummaryResult",
		type: "post",
		dataType : "json",
		data: {seq:seq},
		success: function(data) {

			var innerHTML = "";
			var summary = window['summary'+seq];

			for(var i=0; i<data.rows.length; i++) {
				var oneItem = data.rows[i];

				innerHTML += "<p> "+oneItem[2]+" </p>";

			}
			summary.innerHTML = innerHTML;
		},
		error: function(data) {
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

