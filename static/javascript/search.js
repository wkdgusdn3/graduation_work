function searchNews() {
	var keyword =  $("#keyword").val();

	$.ajax({
		url: "/searchNews",
		type: "post",
		dataType : "json",
		data: {keyword:keyword},
		success: function(data) {
			var innerHTML = "";

			for(var i=0; i<data.rows.length; i++) {
				var oneItem = data.rows[i];

				var sysdate = new Date(oneItem[6]); 

				innerHTML += "<li class='article show' id=<%=" + oneItem[0] + "%>";
				innerHTML += "<p class='q' onclick='searchSummaryResult(" + oneItem[0] + ")'" + "><a>Q: " + oneItem[3] + " (" + sysdate.toLocaleDateString() + ")</a></p>";
				innerHTML += "<p class='a' style='display: none;' ><div id = 'summary" + oneItem[0] + "'></div></p></li>";

			}

			search_keyword_result.innerHTML = innerHTML;
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