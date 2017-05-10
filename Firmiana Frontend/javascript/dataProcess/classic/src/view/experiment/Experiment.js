Ext.define('Admin.view.experiment.Experiment', {
    extend: 'Ext.container.Container',

    // xtype: 'email',

    controller: 'experiment',

    // viewModel: {
    //     type: 'email'
    // },

    // itemId: 'emailMainContainer',

    layout: {
        type: 'fit'
        // align: 'stretch'
    },

    margin: '20 0 0 20',

    items: [
        // {
        //     xtype: 'container',
        //
        //     itemId: 'navigationPanel',
        //
        //     layout: {
        //         type: 'vbox',
        //         align: 'stretch'
        //     },
        //
        //     width: '30%',
        //     minWidth: 180,
        //     maxWidth: 240,
        //
        //     defaults: {
        //         cls: 'navigation-email',
        //         margin: '0 20 20 0'
        //     },
        //
        //     items: [
        //         {
        //             xtype: 'emailmenu',
        //             listeners: {
        //                 click: 'onMenuClick'
        //             }
        //         },
        //         {
        //             xtype: 'emailfriendslist'
        //         }
        //     ]
        // },
        {
            xtype: 'container',
            // itemId: 'contentPanel',
            margin: '0 20 20 0',
            layout: {
                type : 'anchor',
                anchor : '100%'
            },
            items:[{
                xtype: 'grid',
                id: 'exp_grid',
                store: Ext.create('Admin.store.experiment.Experiment',{
                    forceFit: true
                }),
                columns: [
                        {
                            text: "Exp_Number",
                            dataIndex: "Exp_Number",
                            flex:1
                        },{
                            text: "FoundCountT",
                            dataIndex: "FoundCountT",
                            flex:1
                        },{
                            text: "ExpType",
                            dataIndex: "ExpType",
                            flex:1
                        },{
                            text: "Exp_date",
                            dataIndex: "Exp_date",
                            flex:2
                        },{
                            text: "Exp_experimenter",
                            dataIndex: "Exp_experimenter",
                            flex:1
                        },{
                            text: "Cell_Tissue",
                            dataIndex: "Cell_Tissue",
                            flex:2
                        },{
                            text: "Fraction",
                            dataIndex: "Fraction",
                            flex:1
                        },{
                            text: "Genotype",
                            dataIndex: "Genotype",
                            flex:1
                        },{
                            text: "Treatment",
                            dataIndex: "Treatment",
                            flex:1
                        },{
                            text: "AffinityRecNumber",
                            dataIndex: "AffinityRecNumber",
                            flex:1
                        }
                    ]
            }]
        }]
});
