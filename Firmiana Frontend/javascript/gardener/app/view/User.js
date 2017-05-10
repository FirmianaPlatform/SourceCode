Ext.define('gar.view.User',{ 
    extend: 'Ext.window.Window', 
    alias : 'widget.user',
    autoShow: true,
    initComponent : function(){ 
      Ext.apply(this,{ 
	    layout: 'fit',
	    id:'login',
	    title: 'User Form',
	    resizable :false,
	    closable: false,
	    items: {  
	    xtype:'form',
	    url: '/logins/',
	    height: 130,
	    width: 280,
	    bodyPadding: 10,
	    defaultType: 'textfield',
	    items: [
	        {
	            fieldLabel: 'Email Address',
	            name: 'email',
	            maxLength:40,
	            minLength:5,
	            maskRe: /[\w\.@\d_]/i,
	            allowBlank: false
	        },{
			xtype : 'hidden',
			name : 'redirect',
			value : window.location.href
		},
	        {
	            fieldLabel: 'Password',
	            inputType: 'password', 
	            name: 'password',
	            maxLength:50,
	            minLength:5,
	            xtype: 'textfield',
	            allowBlank: false
	        },
	        {
	            xtype: 'checkboxfield',
 				boxLabel  : 'Auto login in one month.',
                name      : 'time',
                id        : 'checkbox1'

	        }
	    ],
	        buttons: [{
        text: 'Reset',
        handler: function() {
            this.up('form').getForm().reset();
        }
    }, {
        text: 'Submit',
        name:'login_button',
        id:'login_submit',
        value:'Login',
        formBind: true, //only enabled once the form is valid
        handler: function() {
            var form = this.up('form').getForm();
            if (form.isValid()) {
                form.submit({
                	waitMsg : 'Checking......',
                	method:'POST',
                    success: function(form, action) {
                    	//console.log(action.result)
                    	var if_month=form.findField('time').getSubmitValue()
                    	//console.log(if_month)
                       if(if_month){
                       	Ext.util.Cookies.set('usercookie',action.result.name,new Date(new Date().getTime()+(1000*60*60*24*30))) ;                      	
                       }else{
                       	Ext.util.Cookies.set('usercookie',action.result.name);
                       };
                       	var uname = Ext.util.Cookies.get("username");
	  	  				Ext.getElementById('login_as').innerHTML = 'Logged in as ' + uname;
                      	Ext.getCmp('login').close();
                      	Ext.getCmp('desk').enable();
                      
                    },
                    failure: function(form, action) {
                        Ext.Msg.alert('Failed', action.result.tex);
                    }
                });
            }
        }
    }]
	    }
        }); 
        this.callParent(arguments); 
    } 
})

