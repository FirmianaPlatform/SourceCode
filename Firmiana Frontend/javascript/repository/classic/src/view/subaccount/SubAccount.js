Ext.define('dataViewer.view.subaccount.SubAccount', {
    extend: 'Ext.container.Container',

    xtype: 'subaccount',

    // controller: 'experiment',

    // viewModel: {
    //     type: 'email'
    // },

    // itemId: 'emailMainContainer',

    layout: {
        type: 'fit'
        // align: 'stretch'
    },

    margin: '10 0 0 10',

    items: [{
            xtype: 'container',
            margin: '0 10 10 0',
            layout: {
                type : 'anchor',
                anchor : '100%'
            },
            items:[{
                xtype: 'toolbar',
                cls: 'sencha-dash-dash-headerbar toolbar-btn-shadow',
                height: 64,
                itemId: 'headerBar',
                items: [{
                        xtype: 'tbspacer',
                        flex: 1
                    },
                    // {
                    //     cls: 'delete-focus-bg',
                    //     iconCls:'x-fa fa-search',
                    //     href: '#search',
                    //     hrefTarget: '_self',
                    //     tooltip: 'See latest search'
                    // },
                    // {
                    //     cls: 'delete-focus-bg',
                    //     iconCls:'x-fa fa-plus',
                    //     tooltip: 'New submission',
                    //     handler: function(){
                    //         // var metadata_window = Ext.create('Ext.window.Window',{
                    //         //     height: 600,
                    //         //     width: 800,
                    //         //     autoShow: true,
                    //         //     modal: true
                    //         // })
                    //         var metadata_window = Ext.create('dataViewer.view.metadata.Metadata')
                    //     }
                    // },
                    {
                        cls: 'delete-focus-bg',
                        iconCls:'x-fa fa-pencil',
                        id: 'subaccount-edit',
                        disabled: true,
                        tooltip: 'Edit',
                        handler: function(){
                            // var metadata_window = Ext.create('Ext.window.Window',{
                            //     height: 600,
                            //     width: 800,
                            //     autoShow: true,
                            //     modal: true
                            // })
                            // var metadata_window = Ext.create('dataViewer.view.metadata.ShowMetadata',{
                            //     project_pxdNo: project_pxdNo
                            // })
                        }
                    },
                    // {
                    //     cls: 'delete-focus-bg',
                    //     iconCls:'x-fa fa-bell'
                    // },
                    // {
                    //     cls: 'delete-focus-bg',
                    //     iconCls:'x-fa fa-th-large',
                    //     href: '#profile',
                    //     hrefTarget: '_self',
                    //     tooltip: 'See your profile'
                    // },
                    // {
                    //     xtype: 'tbtext',
                    //     text: 'CrickDing',
                    //     cls: 'top-user-name'
                    // },
                    // {
                    //     xtype: 'image',
                    //     cls: 'header-right-profile-image',
                    //     height: 35,
                    //     width: 35,
                    //     alt:'current user image',
                    //     src: 'resources/images/user-profile/ding.jpeg'
                    // }
                ]
            },{
                xtype: 'grid',
                id: 'subaccount-grid',
                store: Ext.create('dataViewer.store.subaccount.SubAccount',{
                    forceFit: true
                }),
                columns: [
                        {
                            text: "Account",
                            dataIndex: "username",
                            flex:1,
                        },{
                            text: "Annotation",
                            dataIndex: "annotation",
                            flex:1
                        },{
                            text: "Shared Projects",
                            dataIndex: "sharedProjectList",
                            flex:3
                        },{
                            xtype: 'checkcolumn',   
                            text: "Active",
                            dataIndex: "isActive",
                            flex:1
                        }
                    ],
                    listeners: [{
                        select: function (grid, record){
                            Ext.getCmp('subaccount-edit').enable()
                            project_username = record.getData().username
                            console.log(project_username)
                        }
                    },{
                        deselect: function (grid, record){
                            Ext.getCmp('subaccount-edit').disable()
                        }
                    }]
            }]
        }]
});
