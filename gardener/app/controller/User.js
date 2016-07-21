Ext.define('gar.controller.User',{ 
    extend: 'Ext.app.Controller', 
    views: [ 'User' ],    
    init : function(){ 

        this.control({
            "#btlogin": {
            	afterrender:this.checkUser,
                click: this.showLogin
            },
            "#btchangepass": {
                click: this.showChangepass
            },
            "#btlogoff": {
                click: this.logoff
            },
            '#login':{
            	destroy: this.showDesk
            },
            
            '#menu-panel':{
				afterrender: this.expandmenu
            }
        });
    	
    }, 
// show login window 
    showLogin: function() {
    	var login = Ext.widget('user'); 	  	
 	  	Ext.getCmp('desk').disable();
 	  	var cookievalue=  Ext.util.Cookies.clear("username");
		var cookievalue=  Ext.util.Cookies.clear("galaxysession");
		var cookievalue=  Ext.util.Cookies.clear("csrftoken");
		Ext.Ajax.request({
					url : '/logout/',
					success : function(response)
						{ 	
							
							//window.location.href='/login';
						},
					failure : function(response) 
						{ 
							//Ext.Msg.alert('Error','Logout failed, check your network.');
							//Ext.getCmp('desk').enable();
						}
		});
 	  	login.show();
	    },

	    
	 showChangepass: function() {
    	var changepass = Ext.widget('changepass');
 	  	changepass.show();
	    },
//show desk	    
	    showDesk:function(){
	    	Ext.getCmp('desk').enable();
	    },
	    
//check user state need add server test for key string.
	    
	    checkUser:function(){
		  var cookievalue = Ext.util.Cookies.get("username"); 
	    	if(cookievalue==null){        
	    		window.location.href='/login'
				//this.showLogin()   	
	  	  	}
	  	  	else if(cookievalue!=null && cookievalue.length<1){  
	  	  		window.location.href='/login'
				//this.showLogin()   	
	  	  	}

	  	  	//visitor count 
			/*Ext.Ajax.request({
					//url : '/visicount/',
					success : function(response)
						{ 	
							var text = response.responseText;
							//var count = Ext.JSON.decode(text);
							//var visit = count.v
							//var online = count.o
							Ext.getElementById('info_message').childNodes[0].nodeValue='Fimiana Experiment View.(Total visitors: '+text+')'
						},
					failure : function(response) 
						{}
					});*/
				
	    },
		   

//logoff
	    logoff:function(){
	    	Ext.getCmp('desk').disable();
	    	//Ext.Msg.alert('Logout','Waiting for logout...If failed, try again.');
	    	var cookievalue=  Ext.util.Cookies.clear("username");
		  	var cookievalue=  Ext.util.Cookies.clear("galaxysession");
		  	var cookievalue=  Ext.util.Cookies.clear("csrftoken");
			Ext.Ajax.request({
					url : '/logout/',
					success : function(response)
						{ 	
							
							//window.location.href='/login';
						},
					failure : function(response) 
						{ 
							//Ext.Msg.alert('Error','Logout failed, check your network.');
							//Ext.getCmp('desk').enable();
						}
			});
			window.location.href='/login';
		  //this.showLogin()
		  //window.location.reload();
	    },

//menu appear
	    expandmenu:function(){
		  var cookievalue=  Ext.util.Cookies.get("usercookie");
	    	if(cookievalue == null){
	    	Ext.getCmp('menu-panel').collapse();
	  	  }
	    else{
	    	Ext.getCmp('menu-panel').expand();
	    }
	    }
}) 