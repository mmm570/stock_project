//trend.html
$(document).ready(function(){
	//+新增
	$(document).on('click','#addsubmit', function(){
		$.ajax({
		    url: "/trend/addtrend",
		    type: 'GET',
		    dataType: 'html',
		    success: function(data) {
		    	$('#addsubmit').before(data);
		    	}    	
		})
    })
    //送出
	$(document).on('click','#submit_add', function(e){
		var $a = $(e.target).prev();
		$.ajax({
		    url: "/trend/trend2",
		    type: 'GET',
		    dataType: 'html',
		    data:{'ts':$a.val()},
		    success: function(data) {
				$(e.target).nextAll().remove();
		    	$(e.target).after(data);
		    	}
		    })
		})		
});