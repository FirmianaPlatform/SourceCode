/*Ext.require(['Ext.tip.QuickTipManager', 'Ext.menu.*','Ext.util.*',
		'Ext.form.field.ComboBox', 'Ext.layout.container.Table',
		'Ext.container.ButtonGroup']);
*/
Ext.Loader.setPath('Ext', '/static/ext4/');
Ext.Loader.setConfig({
			enabled : true
		});

Ext.require(['Ext.tip.QuickTipManager', 'Ext.menu.*','Ext.util.*',
		'Ext.form.field.ComboBox', 'Ext.layout.container.Table',
		'Ext.container.ButtonGroup']);
		
Ext.onReady(function() {

	Ext.QuickTips.init();
	Ext.form.Field.prototype.msgTarget = 'side';
	
	var submitter = function() 
		{	
			var form = login_form.getForm();
			
			var s = 30;
			var my_timer = {
    			run:function(){
	    			if(s<0){
	      				//alert('The server is Too Busy! Try again please.');
	      				login_form.down('#login_submit').setText('Retry')
                    	login_form.down('#login_submit').enable()
	      				return false;
	    			}else{
	      				login_form.down('#login_submit').setText('Wait: '+s+' sec');
	      				s--;
	    			}
	  			},
	  			//scope: this,
	  			interval: 1000
  			}
  			Ext.TaskManager.start(my_timer)

			login_form.down('#login_submit').disable()
            
            var useremail = form.findField('email').getValue()
            if (form.isValid()) 
            	{
                	form.submit({
                		method:'POST',
                    	success: function(form, action) {
                    				/*var onemonth = form.findField('time').getSubmitValue()
                       				if(onemonth){
                       					var d = new Date(new Date().getTime()+(1000*60*60*24*30));
                       					//var dd = new Date().getTime()
                       					Ext.util.Cookies.set('username',action.result.name,d) ;
                       					//Ext.util.Cookies.set('usercookie',useremail,d);
                       								
                       				}else{
                       				//alert('Welcome, '+useremail+' ,thanks for using Firmiana!'+d.getTime());
                       					Ext.util.Cookies.set('username',action.result.name);
                       					//console.log(action.result)
                       					//Ext.util.Cookies.set('usercookie',useremail);
                       								
                       				};		*/
                       				window.location.reload()
                       				//alert('Last login time : '+ action.result.last_login)
                      
                    	},
                    	failure: function(form, action) {
                    				//exploadMask.hide();
                        			//Ext.Msg.alert('Failed', action.result.tex);
                    				Ext.TaskManager.stop(my_timer)
                    				//alert(action.result.tex)
                    				if(s<2)
                    					{alert('Connection failed! Try again please.')}
                    				else
                    					{alert('Sorry, please check your email or password !')}
                    				login_form.down('#login_submit').setText('Retry')
                    				login_form.down('#login_submit').enable()
                    	}
                	});
            	}
        }
	var login_form = Ext.create('Ext.form.FormPanel', {
				renderTo : 'home_nav',
				//cls : 'home_nav-text',
				border:false,
				//height:36,
				//autoHeight : true,
				frame:false,  
				layout:'column',
				//defaultType: 'textfield',
				width: '100%',
				url: '/logins/',
				bodyStyle:"border-bottom:true",
				items: 
	    			[
	        			{	
	        				xtype: 'textfield',
	            			vtype: 'email',
	            			name: 'email',
	            			fieldLabel: 'Email Address ',
	        				labelAlign :'right', 
	        				labelStyle: 'font-weight:bold;padding:0',
	        				columnWidth : .3,
	            			maxLength:100,
	            			//maskRe: /[\w\.@\d_]/i,
	            			allowBlank: false
	        			},{
	        				
							xtype : 'hidden',
							name : 'redirect',
							value : window.location.href
						},{
							xtype : 'textfield',
	            			inputType : 'password', 
	            			name : 'password',
	            			fieldLabel: 'Password ',
	            			labelWidth : 75,
							labelAlign :'right',
							labelStyle: 'font-weight:bold;padding:0',
							columnWidth : .22,
	            			maxLength : 40,
	            			//minLength:5,
	            			allowBlank : false,
	            			listeners : {
											specialkey : function(field, event) {
												if (event.getKey() == event.ENTER) {
													//Ext.MessageBox.confirm('hahaha');
													//this.up('form').getForm().reset();
													submitter()
												}
											}
										}
	        			},{
	        				xtype : 'checkboxfield',
                			itemId : 'checkbox1',
                			name : 'time',
	        				margin : '0 0 0 5',
	        				columnWidth : .25,
	        				checked:true,
 							boxLabel : 'Keep login for one month.'

	        			},{		
	        				xtype : 'button',
        					itemId : 'login_submit',
        					name :'login_button',
        					margin : '0 0 0 10',
	        				columnWidth : .1,
	        				//layout : "form",
        					text : 'Login',
        					value : 'Login',
        					formBind : true, //only enabled once the form is valid
        					handler : submitter
    						
	        			},{	
	        				xtype : 'button',
        					text : 'Reset',	
	        				margin : '0 0 0 10',
	        				columnWidth : .1,
        					handler : function() {
            						this.up('form').getForm().reset();
        						}
        						
    						}
	    		]
	});

});

			