//HOMEPAGE
$(document).ready(function(){
    $(window).scroll(function () {
      var scrollVal = $(this).scrollTop();
      if(scrollVal > 100){
		  $('.home_top').attr('class','top_color');
	  }else{
		  $('.top_color').attr('class','home_top');
	  }
	});
});
//choose.html
$(document).ready(function(){
	$("#status").hide();
	var dt = new Date();
	$(document).on('click','#submit', function(){
		$("#status").show();
		var $a =$('#s_num');
		function refresh(){
			$.ajax({
			    url: "/choose/timely_stock",
			    type: 'GET',
			    dataType: 'html',
			    data:{'stock':$a.val()},
			    success: function(data) {
					$('#choo').empty();
					$('#choose_title').remove();
			    	$('.fig').remove();
			    	$('#choosepage_div').after(data);
			    	$('#choosepage_div~div').attr('class','fig');
					$("#status").hide(); 
					if (Number($('#redORgreen1 tbody tr td:eq(3)').text())>0){
			    		 $('#redORgreen1 tbody tr td:eq(3)').attr('class','red');
			    		}
			    	else if(Number($('#redORgreen1  tbody tr td:eq(3)').text())<0){
			    		$('#redORgreen1 tbody tr td:eq(3)').attr('class','green');
			    		}
			    	else if(Number($('#redORgreen1  tbody tr td:eq(3)').text())==0){
			    		$('#redORgreen1  tbody tr td:eq(3)').attr('class','white');
			    		}
			    		
			    		
			    	if (Number($('#redORgreen2 tbody tr td:eq(9)').text())>0){
			    		 $('#redORgreen2 tbody tr td:eq(9)').attr('class','red');
			    		}
			    	else if(Number($('#redORgreen2  tbody tr td:eq(9)').text())<0){
			    		$('#redORgreen2 tbody tr td:eq(9)').attr('class','green');
			    		}
			    	else if(Number($('#redORgreen2  tbody tr td:eq(9)').text())==0){
			    		$('#redORgreen2  tbody tr td:eq(9)').attr('class','white');
			    		}
			    		
			    	if ((dt.getHours()<=9 || dt.getHours()>=13) || (dt.getHours()==13 && dt.getMinutes()>=30)){
			    		return false;
			    		}
			    	else{
			    		setTimeout(refresh,1000*10);
			    		}
			    	}  	
			})
			.fail(function() {
				alert($a.val()+' 此股票代非上市股票')
				$("#status").hide();
			})
		}
		refresh();
	})
		/*$('#submit').on('click', function(){
		$.ajax({
		    url: "/choose/random",
		    type: 'GET',
		    dataType: 'html',
		})
		.done(function(data) {
		    	$('#choose_div').after(data);
		})

	});*/
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
			$('#aa').next().remove();
		    $('#aa').after(data);
		})
		.fail(function() {
			alert('網址錯誤')
			$("#status").hide();
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
			$('#aaa').nextAll().remove();
		    $('#aaa').after(data);
		})
		.fail(function() {
			alert('查無資訊')
			$("#status").hide();
		})   
	})
	/*$(document).ajaxStop(function(){
		alert("All AJAX requests completed");
	});	//所有ajax完成發出
	*/
});

