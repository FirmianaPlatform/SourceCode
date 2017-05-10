    var userName;  
    var passWord;  
    var xmlHttpRequest;  
      
      
    //XmlHttpRequest对象  
    function createXmlHttpRequest(){  
        if(window.ActiveXObject){ //如果是IE浏览器  
            return new ActiveXObject("Microsoft.XMLHTTP");  
        }else if(window.XMLHttpRequest){ //非IE浏览器  
            return new XMLHttpRequest();  
        }  
    }  
      
    function onLogin(){  
        userName = document.f1.username.value;  
        passWord = document.f1.password.value;    
          
        var url = "LoginServlet?username="+userName+"&password="+passWord+"";     
              
        //1.创建XMLHttpRequest组建  
        xmlHttpRequest = createXmlHttpRequest();  
          
        //2.设置回调函数  
        xmlHttpRequest.onreadystatechange = zswFun;  
          
        //3.初始化XMLHttpRequest组建  
        xmlHttpRequest.open("POST",url,true);  
          
        //4.发送请求  
        xmlHttpRequest.send(null);    
    }     
      
      
    //回调函数  
    function zswFun(){  
        if(xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200){  
            var b = xmlHttpRequest.responseText;  
            if(b == "true"){  
                alert("登录成功！");  
            }else{  
                alert("登录失败！");  
            }         
        }  
    }
	
						//XmlHttpRequest对象  
					function createXmlHttpRequest(){  
						if(window.ActiveXObject){ //如果是IE浏览器  
							return new ActiveXObject("Microsoft.XMLHTTP");  
						}else if(window.XMLHttpRequest){ //非IE浏览器  
							return new XMLHttpRequest();  
						}
					}
					function onLogin(email, password){  
						userName = email;
						passWord = password;   
          
						var url = "http://61.50.134.132/logins/?email="+userName+"&password="+passWord+"";     
              
						//1.创建XMLHttpRequest组建  
						xmlHttpRequest = createXmlHttpRequest();  
          
						//2.设置回调函数  
						xmlHttpRequest.onreadystatechange = zswFun;  
          
						//3.初始化XMLHttpRequest组建  
						xmlHttpRequest.open("POST",url,true);  
          
						//4.发送请求  
						xmlHttpRequest.send(null);    
					}      
					
					//回调函数  
					function zswFun(){  
						if(xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200){  
							var b = xmlHttpRequest.responseText;  
							if(b == "true"){  
								alert("登录成功！");  
							}else{  
								alert("登录失败！");  
							}         
						}  
					}