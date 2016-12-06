$(function () { 
	
	$('#myModal').on('hide.bs.modal', function () { window.location.reload();})
 	
 	$('#goGardener').click(function(){window.location="/gardener";})	
	 	
	$(".login_btn").click(function(){
		console.log('login_btn...')
		$("#loginbtn").val("Loading...")
		
		var email = $("#email");
		var pwd  = $("#pswd");
		var remember  = $("#remember");
		var pre=/^[a-zA-Z]\w{5,19}/;
	
		if(email.val()=="" || pwd.val()==""){
			alert("Null user name or password");
			$("#email").focus();
			$("#loginbtn").val("LOG IN")
			return false;
		}
		//if(!pre.test(email.val())){
		//	alert("Null user name or password");
		//	//$(".msg").html("<font color='red'>Error</font>");
		//	return false;
		//}
		//return false;
		
		// $(".login_btn").button("loading");
		console.log('beforeSend...');
				
		$.ajax({
			type:"POST",
			url:"/logins/",
			timeout: 30000,
			data:{
				email:   $("#email").val(),
				password:$("#pswd").val(),
				time:    $("#remember").val()
			},
			beforeSend : function(){
				//$(".msg").html("Login...");
			},
			success : function(data){
				var resJSON = $.parseJSON(data)
				// console.log(resJSON)
				if(!resJSON.success){
					var $panel = $("#loginmodal")
				    var box_left = $panel.position().left
				    $panel.stop();
				    for(var i=1; 4>=i; i++){
				        $panel.animate({left:box_left-10},50);
				        $panel.animate({left:box_left+10},50);
				    }
				    $panel.animate({left:box_left},50);
				    $("#loginbtn").val("LOG IN")
					// alert(resJSON.tex)
					// return
				}
				else{
					window.location="/gardener";
				}
				//window.location.reload();
				//$("#login_form").html("Success");
				//$(".msg").html(data);
			},
			error : function(data){
				console.log('error...');
				alert('Network unstable...')
				$(".login_btn").button("reset");
			}
		});
	}); 
	
	// $(document).keyup(function(event){ 
	//     if(event.keyCode ==13){ 
	//       $(".login_btn").trigger("click"); 
	//     } 
	// });
});

