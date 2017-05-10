Ext.define('register.view.main.Register', {
    extend: 'Ext.form.Panel',
    xtype: 'register',
    id: 'registerPanel',

    requires: [
        "register.view.main.RegisterController",
    ],

    controller: "main-register",

    header: {
        layout: {
            align: 'stretchmax'
        },
        title: {
            text: 'Register',
            margin: '0 0 0 15',
            flex: 0
        },

    },
    bodyPadding: '15 5 15 15',
//    anchor: '100% 100%',
    defaults: {
    	margin: '15 0 8 15',
        width: 620,
        labelWidth: 140
    },

    initComponent: function() {
    	
    	me = this
        Ext.tip.QuickTipManager.init();
        csrftoken = Ext.util.Cookies.get('csrftoken');

        var submitForm = function() {
            var form = me.getForm();
            console.log(form)
            if (form.isValid()) {
                form.submit({
                    url: '/regist/',
                    standardSubmit: true
                })
            }
        };

        var resetForm = function() {

            form = me.getForm()
            form.reset()
        };

        var companyStore = Ext.create('Ext.data.Store', {
            proxy: {
                type: 'ajax',
                url: '/experiments/ajax/all_company/',
                reader: {
                    type: 'json',
                    rootProperty: 'all_company'
                }
            },
            fields: [{
                name: 'company',
                type: 'string'
            }],
            autoLoad: true
        });

        var labStore = Ext.create('Ext.data.Store', {
            proxy: {
                type: 'ajax',
                url: '/experiments/ajax/all_lab/',
                reader: {
                    type: 'json',
                    rootProperty: 'all_lab'
                }
            },
            fields: [{
                name: 'lab',
                type: 'string'
            }],
            autoLoad: true
        });

        Ext.apply(Ext.form.field.VTypes, {
            password: function(val, field) {
                if (field.initialPassField) {
                    var pwd = field.up('form').down('#' + field.initialPassField);
                    return (val == pwd.getValue());
                }
                return true;
            },
            passwordText: 'Password do not match'
        });

        //hander
        timestamp = (new Date()).valueOf();

        this.items = [{
                xtype: 'fieldcontainer',
                layout: {
                    type: 'hbox',
                    align: 'stretch'
                },
                items: [{
                    xtype: 'combobox',
                    fieldLabel: 'Company',
                    displayField: 'company',
                    valueField: 'company',
                    name: 'company',
                    id: 'com',
                    store: companyStore,
                    editable: false,
                    queryMode: 'local',
                    labelWidth: 140,
                    width: 520,
                    allowBlank: false,
                    emptyText: 'Your company',
                    listeners: {
                        select: {
                            fn: function(combo, records, index) {
                            	console.log(records)
                                var lab = Ext.getCmp("com-lab");
                                lab.clearValue();
                                lab.store.load({
                                    params: {
                                        id: records.data.company
                                    }
                                })
                            }
                        }
                    }
                }, {
                    xtype: 'button',
                    text: 'Ohters',
                    flex: 1,
                    margin: '0 0 0 20',
                    handler : function(){
                        Ext.Msg.prompt('Add new company','Please enter your company name:',function(btn,text){
                            if(btn == 'ok'){
                            	var myMask = new Ext.LoadMask({
                            	    msg    : 'Please wait...',
                            	    target : Ext.getCmp('registerPanel')
                            	});
                            	myMask.show();
                            	Ext.Ajax.request({
                                    timeout: 600000,
                                    url: '/gardener/addACompany/',
                                    method: 'GET',
                                    params: {
                                        companyName: text
                                    },
                                    success:function(response){
                                    	var responseJson = Ext.JSON.decode(response.responseText)
                                    	if(responseJson.success){
                                    		Ext.Msg.alert('Success','New company: "' + text + '" is added successfully.')
                                    		Ext.getCmp('com').setValue(text)
                                    		myMask.hide();
                                    	}else{
                                    		Ext.Msg.alert('Failed','Company: "'+ text + '" has existed.')
                                    		myMask.hide()
                                    	}
                                    },
                                    failure:function(){
                                        console.log('failed')
                                    }
                                })
                            }
                        })
                    }
                }]
            }, {
                xtype: 'fieldcontainer',
                layout: {
                    type: 'hbox',
                    align: 'stretch'
                },
                items: [{
                    xtype: 'combobox',
                    fieldLabel: 'Laboratory',
                    displayField: 'lab',
                    valueField: 'lab',
                    name: 'lab',
                    id: 'com-lab',
                    store: labStore,
                    editable: false,
                    queryMode: 'local',
                    labelWidth: 140,
                    width: 520,
                    allowBlank: false,
                    emptyText: 'Company needed'
                }, {
                    xtype: 'button',
                    text: 'Ohters',
                    flex: 1,
                    margin: '0 0 0 20',
                    handler : function(){
                    	var companyText = Ext.getCmp('com').value
                        Ext.Msg.prompt('Add new laboratory','Please enter your laboratory name:',function(btn,text){
                            if(btn == 'ok'){
                            	console.log(companyText)
                            	var myMask = new Ext.LoadMask({
                            	    msg    : 'Please wait...',
                            	    target : Ext.getCmp('registerPanel')
                            	});
                            	myMask.show();
                            	Ext.Ajax.request({
                                    timeout: 600000,
                                    url: '/gardener/addALaboratory/',
                                    method: 'GET',
                                    params: {
                                        companyName: companyText,
                                        laboratoryName: text
                                    },
                                    success:function(response){
                                    	var responseJson = Ext.JSON.decode(response.responseText)
                                    	if(responseJson.success){
                                    		Ext.Msg.alert('Success','New laboratory: "' + text + '" is added successfully.')
                                    		Ext.getCmp('com-lab').setValue(text)
                                    		myMask.hide();
                                    	}else{
                                    		Ext.Msg.alert('Failed','Laboratory: "' + text + '" has existed.')
                                    		myMask.hide()
                                    	}
                                    },
                                    failure:function(){
                                        console.log('failed')
                                    }
                                })
                            }
                        })
                    }
                }]
            },

            //////////////////
            {
                xtype: 'textfield',
                fieldLabel: 'PI Name',
                name: 'username',
                emptyText: 'This will be your user name.',
                regex:/^\w+$/,
                regexText:'Only alphanumeric characters and the underscore is allowed.',
                allowBlank: false
            }, {
                xtype: 'textfield',
                fieldLabel: 'Stuff Name',
                name: 'stuffName',
                allowBlank: false
            }, {
                xtype: 'textfield',
                fieldLabel: 'Email',
                name: 'email',
                vtype: 'email',
                allowBlank: false
            }, {
                xtype: 'textfield',
                fieldLabel: 'Password',
                name: 'password1',
                inputType: 'password',
                itemId: 'password1',
                allowBlank: false
            }, {
                xtype: 'textfield',
                fieldLabel: 'Confirm Password',
                name: 'password2',
                inputType: 'password',
                vtype: 'password',
                initialPassField: 'password1',
                allowBlank: false,
                flex: 1
            }, {
                xtype: 'hiddenfield',
                name: 'csrfmiddlewaretoken',
                value: csrftoken
            }
        ],
        this.dockedItems = [{
        	xtype: 'toolbar',
        	dock: 'bottom',
//        	ui: 'footer',
        	margin: '0 0 0 20',
        	items: [
//        	    { xtype: 'tbspacer', width: 50 },
				{text: 'Reset', handler: resetForm},
				{
					text: 'Submit', 
					handler: submitForm,
					id: 'registerSubmit',
					disabled: true
				}
        	]
        }]
        this.callParent(arguments);
    },

    listeners:{
    	validitychange:function(item, valid, eOpts ){
    		var submitButton = Ext.getCmp('registerSubmit')
    		if(valid==true){
    			submitButton.enable()
    		}else{
    			submitButton.disable()
    		}
    	}
    }
});
