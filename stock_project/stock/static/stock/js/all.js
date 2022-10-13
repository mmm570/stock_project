//choose.html
$(document).ready(function(){
	$("#status").hide();
	var dt = new Date();
	$('#submit').on('click', function(){
		$("#status").show();
		var $a =$('#s_num');
		function refresh(){
			$.ajax({
			    url: "/choose/timely_stock",
			    type: 'GET',
			    dataType: 'html',
			    data:{'stock':$a.val()},
			    success: function(data) {
					$('#choose_div2').remove();
			    	$('.fig').remove();
			    	$('#choose_div').after(data);
			    	$('#choose_div~div').attr('class','fig');
					$("#status").hide(); 
			    	if (Number($('tbody tr td:eq(9)').text())>0){
			    		 $('tbody tr td:eq(9)').attr('id','red');
			    		}
			    	else if(Number($('tbody tr td:eq(9)').text())<0){
			    		$('tbody tr td:eq(9)').attr('id','green');
			    		}
			    	else{
			    		$('tbody tr td:eq(9)').attr('id','white');
			    		}
			    	if ((dt.getHours()<=9 && dt.getHours()>=13) || (dt.getHours()==13 && dt.getMinutes()>=30)){
			    		setTimeout(refresh,1000*10);
			    		}
			    	else{
			    		setTimeout(refresh,1000*10);
			    		}
			    	}  	
			})
			.fail(function() {
				alert($a.val()+' 此股票代非上市股票')
			})
		}
		refresh();
	})
});

//trend.html
$(document).ready(function(){
	//+新增
	$(document).on('click','#addsubmit', function(){
		$.ajax({
		    url: "/trend/addtrend",
		    type: 'GET',
		    dataType: 'html', 	
		})
		.done(function(data) {
		    	$('#add_div').before(data);
		})
    })
    //送出
	$(document).on('click','#submit_add', function(e){
		var $a = $(e.target).prev().val();
		$.ajax({
		    url: "/trend/trend2",
		    type: 'GET',
		    dataType: 'html',
		    data:{'ts': $a},
		})
		.done(function(data) {
		    $(e.target).parent().nextAll().remove();
		    $(e.target).parent().after(data);
		})
		.fail(function() {
			alert('查無資訊')
		})   
	})
});

//predict.html
$(document).ready(function(){
	$("#status").hide();
	$(document).on('click','#submit_news', function(e){
		$("#status").show();
		var $a = $('#newsUrl').val();
		$.ajax({
		    url: "/predict/newUrl",
		    type: 'GET',
		    dataType: 'html',
		    data:{'url': $a},
		})
		.done(function(data) {
			$("#status").hide();
			$(e.target).next().remove();
		    $(e.target).after(data);
		})
		.fail(function() {
			alert('查無資訊')
		})   
	})
	
	$(document).on('click','#submit_newsimg', function(e){
		$("#status").show();
		var $a = $('#newsImg').val();
		$.ajax({
		    url: "/predict/newImg",
		    type: 'GET',
		    dataType: 'html',
		    data:{'code': $a},
		})
		.done(function(data) {
			$("#status").hide(); 
			$(e.target).nextAll().remove();
		    $(e.target).after(data);
		})
		.fail(function() {
			alert('查無資訊')
		})   
	})
	/*$(document).ajaxStop(function(){
		alert("All AJAX requests completed");
	});	//所有ajax完成發出
	*/
});

