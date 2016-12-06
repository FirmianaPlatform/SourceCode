Ext.onReady( function(){
    Ext.define('Extract', {
        extend: 'Ext.data.Model',
        fields: [
            {name: 'sample_no', type: 'int'},
            {name: 'experimenter', type: 'string'},
            {name: 'date', type: 'date'},
            {name: 'txid', type: 'string'},
            {name: 'cell_tissue', type: 'string'},
            {name: 'subcellular_organelle', type: 'string'},
            {name: 'rx', type: 'string'},
            {name: 'genotype', type: 'string'},
            {name: 'methods', type: 'string'},
        ],
    });
    
    var store = Ext.create('Ext.data.Store', {
        pageSize: 50,
        model: 'Extract',
        remoteSort: true,
        proxy: {
            type: 'ajax',
            url: '/experiments/data/sample/',
            reader: {
                type: 'json',
                root: 'samples',
                totalProperty: 'total'
            },
            simpleSortMode: true
        },
        sorters: [
            {
                property: 'sample_no',
                direction: 'ASC'
            }
        ]
    });


    Ext.create('Ext.grid.Panel', {
        title: 'Sample Information',
        renderTo: 'grid',
        columnLines: true,
        rowLines: true,
        scroll: 'both',
        minHeight: 650,
        store: store,
        columns: [{
            text: 'Sample No',
            flex: 1,
            dataIndex: 'sample_no'
        },{
            text:'Experimenter',
            flex: 1,
            dataIndex: 'experimenter',
        },{
            xtype: 'datecolumn',
            text:'Date',
            flex: 1,
            dataIndex: 'date',
            format: 'Y-m-d'
        },{
            text:'txID',
            flex: 1,
            dataIndex:'txid'
        },{
            text:'Cell/Tissue',
            flex: 1,
            dataIndex:'cell_tissue'
        },{
            text:'Subcellular organelle',
            flex: 1,
            dataIndex:'subcellular_organelle'
        },{
            text:'Rx(s)',
            flex: 1,
            dataIndex:'rx'
        },{
            text:'Genotype(s)',
            flex: 1,
            dataIndex:'genotype'
        },{
            text:'Methods',
            flex: 1,
            dataIndex:'methods',
        },{
            xtype: 'actioncolumn',
            flex: 1,
            items:[{
                icon: '/static/images/edit.jpg',
                tooltip: 'Edit',
                handler: function(grid, rowIndex, colIndex){
                    var rec  =  grid.getStore().getAt(rowIndex);
                    document.location.href = '/experiments/edit/sample/?no='+rec.get('sample_no');
                }
            },{
                icon: '/static/images/delete-item.jpg',
                tooltip: 'Delete',
                handler: function(grid, rowIndex, colIndex){
                    var rec  =  grid.getStore().getAt(rowIndex);
                    Ext.MessageBox.confirm('Confirm delete','Are you sure to delete?',function(btn){
                        if (btn == 'yes'){
                            Ext.Ajax.request({
                                url: '/experiments/delete/sample/?no='+rec.get('sample_no'),
                                success: function(response){
                                    responseArray = Ext.JSON.decode(response.responseText);
                                    if(responseArray.success=='True'){
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
    store.loadPage(1);
});


