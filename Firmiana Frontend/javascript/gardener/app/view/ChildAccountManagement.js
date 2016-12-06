Ext.define('gar.view.ChildAccountManagement',{ 
    extend: 'Ext.window.Window', 
    alias : 'widget.childAM',
    autoShow: true,
    height: 600,
    width: 800,
    modal: true,
    title: 'Sub-accounts Management',
    layout: 'fit',
    initComponent : function(){ 
        var childAMgridColumn = [
            { text: 'Account',  dataIndex: 'childs_username', flex: 2 },
            { text: 'Annotation', dataIndex: 'childs_annotation',flex:2 },
            { 
                text: 'Available Experiment', 
                dataIndex: 'childs_sharedExpList',
                editable: true,
                flex:4 
            },{ 
                text: 'Activation', 
                xtype: 'checkcolumn', 
                dataIndex: 'childs_isActive', 
                flex: 1, 
                listeners:{
                    checkchange: function(button, rowIndex, checked){
                        var rec = Ext.getCmp('childAMgrid').getStore().getAt(rowIndex)
                        var action = checked?'activate':'freeze'
                        Ext.Ajax.request({
                            url: '/experiments/manageChildAccount/',
                            method: 'GET',
                            params: {
                                action: action,
                                childName: rec.get('childs_username')
                            },
                            success: function(response) {
                                Ext.Msg.alert('Success', Ext.JSON.decode(response.responseText).text,function(){
                                    Ext.getCmp('childAMgrid').getStore().reload()
                                });
                            },
                            failure: function(response) {
                                Ext.Msg.alert('Failed', Ext.JSON.decode(response.responseText).text);
                            }
                        })
                    } 
                }
            },{   
                xtype: 'actioncolumn',
                width: 30,
                sortable: false,
                menuDisabled: true,
                flex: 1.2,
                items: [' ',{
                    iconCls: 'edit',
                    tooltip: 'Edit this account',
                    scope: this,
                    handler: function(grid, rowIndex, colIndex){
                        var rec = grid.getStore().getAt(rowIndex);
                        Ext.create('Ext.window.Window',{
                            id: 'editchild',
                            title: 'Edit sub-account: ' + rec.get('childs_username'),
                            width: 400,
                            height: 350,
                            autoShow: true,
                            modal: true,
                            layout: 'fit',
                            items: Ext.create('Ext.form.Panel',{
                                padding: '5 5 5 5',
                                border: 0,
                                url: '/experiments/manageChildAccount/',
                                method: 'GET',
                                layout: 'anchor',
                                defaults: {
                                    anchor: '100%'
                                },
                                items: [{
                                    xtype: 'hiddenfield',
                                    name: 'action',
                                    value: 'update'
                                },{
                                    xtype: 'textfield',
                                    fieldLabel: 'Sub-account Name',
                                    name: 'childName',
                                    value: rec.get('childs_username'),
                                    readOnly: true,
                                    allowBlank: false
                                },{
                                    xtype: 'textfield',
                                    fieldLabel: 'Shared Experiments',
                                    name: 'sharedExp',
                                    value: rec.get('childs_sharedExpList'),
                                    allowBlank: false,
                                    emptyText: "ex: 'Exp001234,Exp001235'"
                                }],
                                buttons: [{
                                    text: 'Reset',
                                    handler: function() {
                                        this.up('form').getForm().reset();
                                    }
                                }, {
                                    text: 'Submit',
                                    formBind: true, //only enabled once the form is valid
                                    disabled: true,
                                    handler: function() {
                                        var form = this.up('form').getForm();
                                        if (form.isValid()) {
                                            form.submit({
                                                success: function(form, action) {
                                                    Ext.Msg.alert('Success', Ext.JSON.decode(action.response.responseText).text,function(){
                                                        Ext.getCmp('editchild').close()
                                                        Ext.getCmp('childAMgrid').getStore().reload()
                                                    });
                                                },
                                                failure: function(form, action) {
                                                    Ext.Msg.alert('Failed', Ext.JSON.decode(action.response.responseText).text);
                                                }
                                            });
                                        }
                                    }
                                }]
                            })
                        })
                    }
                },' ',{
                    iconCls: 'delete',
                    tooltip: 'Delete this account',
                    scope: this,
                    handler: function(grid, rowIndex, colIndex){
                        var rec = grid.getStore().getAt(rowIndex);
                        Ext.Msg.show({
                            title:'Delete',
                            msg: 'Delete ' + rec.get('childs_username') + '?',
                            buttons: Ext.Msg.YESNOCANCEL,
                            icon: Ext.Msg.QUESTION,
                            fn: function(btn) {
                                if (btn === 'yes') {
                                    Ext.Ajax.request({
                                        url: '/experiments/manageChildAccount/',
                                        method: 'GET',
                                        params: {
                                            action: 'delete',
                                            childName: rec.get('childs_username')
                                        },
                                        success: function(response) {
                                            Ext.Msg.alert('Success', Ext.JSON.decode(response.responseText).text,function(){
                                                Ext.getCmp('childAMgrid').getStore().reload()
                                            });
                                        },
                                        failure: function(response) {
                                            Ext.Msg.alert('Failed', Ext.JSON.decode(response.responseText).text);
                                        }
                                    })
                                } else if (btn === 'no') {
                                    this.close()
                                } else {
                                    this.close()
                                } 
                            }
                        })
                    }
                },' ']
            }
        ]
        var childAMgridStore = Ext.create('Ext.data.Store', {
            fields:[
            {name: 'childs_username', type: 'string'},
            {name: 'childs_isActive', type: 'boolean'},
            {name: 'childs_annotation', type: 'string'},
            {name: 'childs_sharedExpList', type: 'string'}
            ],
            proxy: {
                type: 'ajax',
                url: '/experiments/getAllChildAccountInfo/',
                reader: {
                    type: 'json',
                    root: 'data'
                }
            },
            autoLoad: true
        })
        var childAMgrid = Ext.create(Ext.grid.Panel,{
            id: 'childAMgrid',
            region: 'center',
            plugins: [Ext.create('Ext.grid.plugin.CellEditing', {
                clicksToEdit : 1,
                listeners : {
                    edit : function(editor, e) {
                        console.log(grid3)
                        var sym = grid3.getStore().getAt(e.rowIdx).get('symbol')
                        if (!sym || sym == '-') {
                            Ext.Msg.alert('Error', 'Symbol error')
                            return
                        }
                        Ext.Ajax.request({
                                    timeout : 600000,
                                    url : '/gardener/userAnnotation/',
                                    method : 'POST',
                                    params : {
                                        exp : Ext.getCmp('content-panel').activeTab.title.split('of ')[1],
                                        symbol : sym,
                                        annotation : e.value
                                    }
                                });
                    }
                }
            })],
            columns: childAMgridColumn,
            store: childAMgridStore,
            tbar:[{
                text: 'Add',
                iconCls: 'add',
                handler: function(){
                    Ext.create('Ext.window.Window',{
                        id: 'addnewchild',
                        title: 'Add new sub-account',
                        width: 400,
                        height: 350,
                        autoShow: true,
                        modal: true,
                        layout: 'fit',
                        items: Ext.create('Ext.form.Panel',{
                            padding: '5 5 5 5',
                            border: 0,
                            url: '/experiments/manageChildAccount/',
                            method: 'GET',
                            layout: 'anchor',
                            defaults: {
                                anchor: '100%'
                            },
                            items: [{
                                xtype: 'hiddenfield',
                                name: 'action',
                                value: 'add'
                            },{
                                xtype: 'textfield',
                                fieldLabel: 'Sub-account Name',
                                name: 'childName',
                                allowBlank: false
                            },{
                                xtype: 'textfield',
                                fieldLabel: 'Password',
                                name: 'childPassword',
                                allowBlank: false,
                                inputType: 'password'
                            },{
                                xtype: 'textfield',
                                fieldLabel: 'Verify password',
                                name: 'childVerifyPassword',
                                // submitValue: false,
                                allowBlank: false,
                                inputType: 'password',
                            },{
                                xtype: 'textfield',
                                fieldLabel: 'Annotation',
                                name: 'annotation',
                                allowBlank: false
                            },{
                                xtype: 'textfield',
                                fieldLabel: 'Shared Experiments',
                                name: 'sharedExp',
                                allowBlank: false,
                                emptyText: "ex: 'Exp001234,Exp001235'"
                            }],
                            buttons: [{
                                text: 'Reset',
                                handler: function() {
                                    this.up('form').getForm().reset();
                                }
                            }, {
                                text: 'Submit',
                                formBind: true, //only enabled once the form is valid
                                disabled: true,
                                handler: function() {
                                    var form = this.up('form').getForm();
                                    if(form.getValues().childPassword != form.getValues().childVerifyPassword){
                                        Ext.Msg.alert('Failed',"Passwords don't match.")
                                    }
                                    else{
                                        if (form.isValid()) {
                                            form.submit({
                                                success: function(form, action) {
                                                    Ext.Msg.alert('Success', Ext.JSON.decode(action.response.responseText).text,function(){
                                                        Ext.getCmp('addnewchild').close()
                                                        Ext.getCmp('childAMgrid').getStore().reload()
                                                    });
                                                },
                                                failure: function(form, action) {
                                                    Ext.Msg.alert('Failed', Ext.JSON.decode(action.response.responseText).text);
                                                }
                                            });
                                        }
                                    }   
                                }
                            }]
                        })
                    })
                }
            }],
            
        })
        this.items = [{
            xtype: 'panel',
            layout: 'border',
            items: [childAMgrid]
        }]
        this.callParent(arguments); 
    },
    
})
