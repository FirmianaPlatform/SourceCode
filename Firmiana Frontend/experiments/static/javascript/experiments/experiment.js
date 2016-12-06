Ext.onReady( function(){
    Ext.define('Experiment', {
        extend: 'Ext.data.Model',
        fields: [
            {name: 'experiment_no', type: 'string'},
            {name: 'experimenter', type: 'string'},
            {name: 'date', type: 'date'},
            {name: 'instrument', type: 'string'},
            {name: 'digest_enzyme', type: 'string'},
            {name: 'digest_type', type: 'string'},
            {name: 'samples', type:'string'},
            {name: 'reagents', type: 'string'},
            {name: 'separations', type: 'string'}
        ]
    });
    
    var store = Ext.create('Ext.data.Store', {
        pageSize: 50,
        model: 'Experiment',
        remoteSort: true,
        proxy: {
            type: 'ajax',
            url: '/experiments/data/experiment/',
            reader: {
                type: 'json',
                root: 'experiments',
                totalProperty: 'total'
            },
            simpleSortMode: true
        },
        sorters: [
            {
                property: 'experiment_no',
                direction: 'ASC'
            }
        ]
    });

    Ext.create('Ext.grid.Panel', {
        title: 'Experiment Information',
        renderTo:'grid',
        columnLines: true,
        rowLines: true,
        forceFit: true,
        scroll: 'both',
        minHeight: 650,
        store: store,
        columns: [{
            text: 'Experiment ID',
            flex: 1,
            dataIndex: 'experiment_no'
        },{
            text:'Experimenter',
            flex: 1,
            dataIndex: 'experimenter'
        },{
            xtype: 'datecolumn',
            text:'Date',
            dataIndex:'date',
            flex: 1,
            format: 'Y-m-d'
        },{
            text:'Instrument',
            flex: 1,
            dataIndex:'instrument'
        },{
            text:'Digest type',
            flex: 1,
            dataIndex:'digest_type'
        },{
            text:'Digest enzyme',
            flex: 1,
            dataIndex:'digest_enzyme'
        },{
            text:'Samples',
            flex: 1,
            dataIndex:'samples'
        },{
            text:'Reagents',
            flex: 1,
            dataIndex:'reagents'
        },{
            text:'Separation',
            flex: 1,
            dataIndex:'separations'
        },{
            xtype: 'actioncolumn',
            flex: 1,
            items:[{
                icon: '/static/images/edit.jpg',
                tooltip: 'Edit',
                handler: function(grid, rowIndex, colIndex){
                    var rec  =  grid.getStore().getAt(rowIndex);
                    document.location.href = '/experiments/edit/experiment/?no='+rec.get('experiment_no');
                }
            },{
                icon: '/static/images/delete-item.jpg',
                tooltip: 'Delete',
                handler: function(grid, rowIndex, colIndex){
                    var rec  =  grid.getStore().getAt(rowIndex);
                    Ext.MessageBox.confirm('Confirm delete','Are you sure to delete?',function(btn){
                        if (btn == 'yes'){
                            Ext.Ajax.request({
                                url: '/experiments/delete/experiment/?no='+rec.get('experiment_no'),
                                success: function(response){
                                    responseArray = Ext.JSON.decode(response.responseText);
                                    if(responseArray.success=='true'){
                                        store.reload();
                                    }else{
                                        Ext.Msg.alert('Fail', responseArray.error);
                                    }
                                }
                            });
                        }
                    });
                }
            }]
        }],
        bbar: Ext.create('Ext.PagingToolbar',{
            store: store,
            displayInfo: true,
            displayMsg: 'Displaying  {0} - {1} of {2}',
            emptyMsg: 'No records to display'
        })
    });
    store.loadPage(1)
    
});


