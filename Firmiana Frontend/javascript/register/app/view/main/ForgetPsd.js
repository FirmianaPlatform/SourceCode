
Ext.define("register.view.main.ForgetPsd",{
    extend: "Ext.form.Panel",
    xtype: 'forgetPsd',

    requires: [
        "register.view.main.ForgetPsdController",
        "register.view.main.ForgetPsdModel"
    ],

    controller: "main-forgetpsd",
    viewModel: {
        type: "main-forgetpsd"
    },
    
    header: {
        layout: {
            align: 'stretchmax'
        },
        title: {
            text: 'Forget Password',
            margin: '0 0 0 15',
            flex: 0
        },

    },
    bodyPadding: '15 5 15 15',
//    anchor: '100% 100%',
    defaults: {
    	margin: '15 0 8 15',
        width: 620,
        labelWidth: 80
    },

    initComponent: function() {
    	var me = this
    	this.items = [{
    		xtype: 'textfield',
            fieldLabel: 'Email',
            emptyText: 'Input your email address',
            name: 'email',
            vtype: 'email',
            allowBlank: false
    	}],
    	this.dockedItems = [{
        	xtype: 'toolbar',
        	dock: 'bottom',
//        	ui: 'footer',
        	margin: '0 0 0 20',
        	items: [{
        		text: 'Reset my password',
        		handler:function(){
        			var form = me.getForm();
                    console.log(form)
                    if (form.isValid()) {
                        form.submit({
                            url: '/forgetpsd/',
                            standardSubmit: true,
                            success: function(form, action) {
                            	console.log(form)
                            	console.log(action)
                             },
                             failure: function(form, action) {
                                 switch (action.failureType) {
                                     case Ext.form.action.Action.CLIENT_INVALID:
                                         Ext.Msg.alert('Failure', 'Form fields may not be submitted with invalid values');
                                         break;
                                     case Ext.form.action.Action.CONNECT_FAILURE:
                                         Ext.Msg.alert('Failure', 'Ajax communication failed');
                                         break;
                                     case Ext.form.action.Action.SERVER_INVALID:
                                        Ext.Msg.alert('Failure', action.result.msg);
                                }
                             }
                        })
                    }
				}
        	}]
        }]
    	this.callParent(arguments);
    }
});
