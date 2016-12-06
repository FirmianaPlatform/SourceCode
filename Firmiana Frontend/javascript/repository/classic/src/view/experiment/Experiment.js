Ext.define('dataViewer.view.experiment.Experiment', {
    extend: 'Ext.container.Container',

    xtype: 'projectlist',

    controller: 'experiment',

    requires: [
        'dataViewer.view.experiment.Menu'
    ],

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
                    {
                        cls: 'delete-focus-bg',
                        iconCls:'x-fa fa-plus',
                        tooltip: 'New submission',
                        handler: function(){
                            // var metadata_window = Ext.create('Ext.window.Window',{
                            //     height: 600,
                            //     width: 800,
                            //     autoShow: true,
                            //     modal: true
                            // })
                            var metadata_window = Ext.create('dataViewer.view.metadata.Metadata')
                        }
                    },{
                        cls: 'delete-focus-bg',
                        iconCls:'x-fa fa-pencil',
                        id: 'reposEditButton',
                        disabled: true,
                        tooltip: 'Edit',
                        handler: function(){
                            // var metadata_window = Ext.create('Ext.window.Window',{
                            //     height: 600,
                            //     width: 800,
                            //     autoShow: true,
                            //     modal: true
                            // })
                            var metadata_window = Ext.create('dataViewer.view.metadata.ShowMetadata',{
                                project_pxdNo: project_pxdNo
                            })
                        }
                    },{
                        // xtype: 'combo',
                        cls: 'delete-focus-bg',
                        iconCls:'x-fa fa-share-alt',
                        id: 'reposShareButton',
                        menu: Ext.create('dataViewer.view.experiment.Menu'),
                        disabled: true,
                        tooltip: 'Share',
                        handler: function(){
                            // var share_window = Ext.create('Ext.window.Window',{
                            //     height: 600,
                            //     width: 800,
                            //     autoShow: true,
                            //     modal: true
                            // })
                            // var metadata_window = Ext.create('dataViewer.view.metadata.ShowMetadata',{
                            //     project_pxdNo: project_pxdNo
                            // })
                        }
                    }
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
                id: 'exp_grid',
                store: Ext.create('dataViewer.store.experiment.Experiment',{
                    forceFit: true
                }),
                columns: [
                        {
                            text: "PXD No.",
                            dataIndex: "pxdNo",
                            flex:1,
                        },{
                            text: "Project Name",
                            dataIndex: "projectName",
                            flex:2
                        // },{
                        //     text: "Description",
                        //     dataIndex: "description",
                        //     flex:2.5
                        },{
                            text: "Species",
                            dataIndex: "species",
                            flex:1
                        },{
                            xtype: 'widgetcolumn',
                            widget: {
                                xtype: 'combo',
                                border: 0,
                                height: 20,
                                store: [
                                    'Private',
                                    'Underreview',
                                    'Publicated'
                                ],
                                listeners:[{
                                    select: function(cb, e){
                                        var rec = cb.getWidgetRecord()
                                        // Ext.Msg.confirm("Confirmation", "Are you sure you want to change " + rec.getData().projectName + "'s status to " + e.getData().field1 + "?", function(btn){
                                        //     if(btn === 'yes'){
                                        //         console.log('yes')
                                        //     } else if (btn === 'no'){
                                        //         this.close()
                                        //     }
                                        // });
                                        Ext.Ajax.request({
                                            url: '/repos/changeProjectStatus/',
                                            method: 'GET',
                                            params: {
                                                pxdNo: rec.getData().pxdNo,
                                                status: e.getData().field1
                                            },
                                            success: function(response) {
                                                Ext.Msg.alert('Success', Ext.JSON.decode(response.responseText).msg);
                                            },
                                            failure: function(response) {
                                                Ext.Msg.alert('Failed', Ext.JSON.decode(response.responseText).msg);
                                            }
                                        })
                                        console.log(cb)
                                    }
                                }]
                            },
                            text: "Status",
                            dataIndex: "status",
                            flex:1
                        }
                    ],
                    listeners: [{
                        select: function (grid, record){
                            Ext.getCmp('reposEditButton').enable()
                            Ext.getCmp('reposShareButton').enable()
                            
                            project_pxdNo = record.getData().pxdNo
                            // console.log(record)
                        }
                    },{
                        deselect: function (grid, record){
                            Ext.getCmp('reposEditButton').disable()
                            Ext.getCmp('reposShareButton').disable()
                        }
                    }]
            }]
        }]
});
