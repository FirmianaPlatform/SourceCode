

Ext.onReady(function(){
    Ext.tip.QuickTipManager.init();
    csrftoken = Ext.util.Cookies.get('csrftoken');
  
    /*
    var win1 = Ext.create('Ext.window.Window', {
    	title : 'hello',
    	width : 200,
    	height : 200
    	
    });
    win1.show();
    */
    var submitForm = function(){    	
        form = registerPanel.getForm();
        console.log(form)
        if (form.isValid()){
            form.submit({
                url: '/register/',
                standardSubmit: true
            })
        }
    };

    var resetForm = function(){
    	
        form = registerPanel.getForm()
        form.reset()
    };

	var companyStore = Ext.create('Ext.data.Store', {
						proxy : {
							type : 'ajax',
							url : '/experiments/ajax/all_company/',
							reader : {
								type : 'json',
								root : 'all_company'
							}
						},
						fields : [{
									name : 'company',
									type : 'string'
								}],
						autoLoad : true
					});
					
	var labStore = Ext.create('Ext.data.Store', {
						proxy : {
							type : 'ajax',
							url : '/experiments/ajax/all_lab/',
							reader : {
								type : 'json',
								root : 'all_lab'
							}
						},
						fields : [{
									name : 'lab',
									type : 'string'
								}],
						autoLoad : true
					});
							
    Ext.apply(Ext.form.field.VTypes, {
        password: function(val, field){
            if(field.initialPassField){
                var pwd = field.up('form').down('#'+field.initialPassField);
                return (val==pwd.getValue());
            }
            return true;
        },

        passwordText: 'Passwrod do not match'
    });
    
        //hander
    timestamp = (new Date()).valueOf();
    var add_company = function(){
    	Ext.Msg.prompt('Name', 'Please enter your name:', function(btn, text){
    		if (btn == 'ok'){
        		// process text value and close...
    		}
		});
//    	var win = Ext.create('Ext.window.Window', {
//    		title : 'Add Company',
//    		width : 520,
//    		floating : true,
//    		//renderTo: 'register',
//    		//height: 500,
//    		items :{
//    			xtype : 'form',
//				border : false,
//				bodyPadding : 10,
//				id : 'company_form' + timestamp,
//				items : [{
//							xtype : 'textfield',
//							labelWidth : 90,
//							labelAligh : 'left',
//							width : 250,
//							fieldLabel : 'Company',
//							name : 'Company'
//						}]
//    		},
//    		bbar : ['->', {
//				text : 'Submit',
//				handler : function() {
//					company_form = Ext.getCmp('company_form' + timestamp);
//					var newCompany = company_form.items.items[0].value;
//					companyStore.add({
//								company : newCompany
//							});
//					win.close();
//				}
//			}]
//
//    	});
//    	win.show();

    };
    
   
    
    var view = Ext.create('Ext.container.Viewport',{
    	layout: 'fit',
    	items:[registerPanel],
    	renderTo:'register'
    })
    var registerPanel = Ext.create('Ext.form.Panel',{
//        renderTo: 'register',
        title: 'Register Form',
        bodyPadding:'15 5 15 15',
        defaults: {
            width: 440,
            labelWidth: 110
        },
        
        items:[
		{
			xtype : 'fieldcontainer',
			layout : {
				type : 'hbox',
				align : 'stretch'
			},
			items : [{
						xtype : 'combobox',
						fieldLabel : 'Company',
						displayField : 'company',
						valueField : 'company',
						name : 'company',
						store : companyStore,
						editable:false,
						queryMode : 'local',
						labelWidth : 110,
						width : 400,
						allowBlank : false,
						emptyText : 'Your company',
						listeners : {
							select : {
								fn : function(combo, records, index) {
									var lab = Ext.getCmp("com-lab");
									lab.clearValue();
									lab.store.load({
										params : {
											id : records[0].data.company
										}
									})
								}
							}
						}
					}, {
						xtype : 'button',
						text : 'Add',
						handler : add_company
					}]
		},{
			xtype : 'fieldcontainer',
			layout : {
				type : 'hbox',
				align : 'stretch'
			},
			items : [{
						xtype : 'combobox',
						fieldLabel : 'Laboratory',
						displayField : 'lab',
						valueField : 'lab',
						name : 'lab',
						id : 'com-lab',
						store : labStore,
						editable:false,
						queryMode : 'local',
						labelWidth : 110,
						width : 400,
						allowBlank : false,
						emptyText : 'Company needed'
					}, {
						xtype : 'button',
						text : 'Add',
						handler : add_laboratory
					}]
		},
		
		//////////////////
		{
            xtype: 'textfield',
            fieldLabel: 'PI Name',
            name: 'username',
            allowBlank : false
        },{
            xtype: 'textfield',
            fieldLabel: 'Stuff Name',
            name: 'stuffName',
            allowBlank : false
        },{
            xtype: 'textfield',
            fieldLabel: 'Email',
            name: 'email',
            vtype: 'email',
            allowBlank : false
        },{
            xtype: 'textfield',
            fieldLabel: 'Password',
            name: 'password1',
            inputType: 'password',
            itemId: 'password1',
            allowBlank : false
        },{
            xtype: 'textfield',
            fieldLabel: 'Confirm Password',
            name: 'password2',
            inputType: 'password',
            vtype: 'password',
            initialPassField: 'password1',
            allowBlank : false,
            flex: 1
        },{
            xtype: 'hiddenfield',
            name: 'csrfmiddlewaretoken',
            value: csrftoken
        }],
        dockedItems: [{
        	xtype: 'toolbar',
        	dock: 'bottom',
        	ui: 'footer',
        	items: [
				{text: 'Reset', handler: resetForm},
				{text: 'Submit', handler: submitForm}
        	]
        }]
    });
});
 var add_laboratory = function(){
    	var win = new Ext.Window({
			title : 'ADD Laboratory',
			width : 320,
			autoShow : true,
			modal : true,
			items : [{
						xtype : 'form',
						border : false,
						// frame : true,
						bodyPadding : 10,
						id : 'laboratory_form' + timestamp,
						items : [{
									xtype : 'textfield',
									labelWidth : 90,
									width : 250,
									fieldLabel : 'Laboratory',
									name : 'Laboratory'
								}]
					}],
			bbar : ['->', {
						text : 'Submit',
						handler : function() {
							laboratory_form = Ext.getCmp('laboratory_form' + timestamp);
							var newLaboratory = laboratory_form.items.items[0].value;
							labStore.add({
										lab : newLaboratory
									});
							win.close();
						}
					}]
		});
		
    };
