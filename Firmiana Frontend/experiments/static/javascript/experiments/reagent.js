Ext.onReady( function(){
    Ext.define('Reagent', {
        extend: 'Ext.data.Model',
        fields: [
            {name: 'reagent_no', type: 'string'},
            {name: 'reagent_type', type: 'string'},
            {name: 'name', type: 'string'},
            {name: 'manufacturer', type: 'string'},
            {name: 'catalog_no', type: 'string'},
            {name: 'affinity_type', type: 'string'},
            {name: 'applications', type: 'string'},
            {name: 'react_speciess', type: 'string'},
            {name: 'purification', type: 'string'},
            {name: 'conjugate', type: 'string'},
        ]
    });
    

    var store = Ext.create('Ext.data.Store', {
        pageSize: 50,
        model: 'Reagent',
        remoteSort: true,
        proxy: {
            type: 'ajax',
            url: '/experiments/data/reagent/',
            reader: {
                type: 'json',
                root: 'reagents',
                totalProperty:'total'
            },
            simpleSortMode: true
        },
        sorters: [
            {
                property: 'reagent_no',
                direction: 'ASC'
            }
        ]
    });

    Ext.create('Ext.grid.Panel', {
        renderTo: 'grid',
        columnLines: true,
        rowLines: true,
        forceFit: true,
        scroll: 'both',
        minHeight: 650,
        title: 'Reagent Information',
        store: store,
        columns: [{
            text: 'Reagent No',
            flex: 1,
            dataIndex: 'reagent_no'
        },{
            text:'Reagent Type',
            flex: 1,
            dataIndex: 'reagent_type',
        },{
            text:'Name',
            flex: 1,
            dataIndex:'name'
        },{
            text:'Manufacturer',
            flex: 1,
            dataIndex:'manufacturer'
        },{
            text:'Conjugate',
            flex: 1,
            dataIndex:'conjugate'
        },{
            text:'Affinity Type',
            flex: 1,
            dataIndex:'affinity_type'
        },{
            text:'Applications',
            flex: 1,
            dataIndex:'applications'
        },{
            text:'React Species',
            flex: 1,
            dataIndex:'react_speciess'
        },{
            text:'Purification',
            flex: 1,
            dataIndex:'purification'
        },{
            text:'Catalog',
            flex: 1,
            dataIndex:'catalog_no'
        },{
            xtype: 'actioncolumn',
            flex: 1,
            items:[{
                icon: '/static/images/edit.jpg',
                tooltip: 'Edit',
                handler: function(grid, rowIndex, colIndex){
                    var rec  =  grid.getStore().getAt(rowIndex);
                    document.location.href = '/experiments/edit/reagent/?no='+rec.get('reagent_no');
                }
            },{
                icon: '/static/images/delete-item.jpg',
                tooltip: 'Delete',
                handler: function(grid, rowIndex, colIndex){
                    var rec  =  grid.getStore().getAt(rowIndex);
                    Ext.MessageBox.confirm('Confirm delete','Are you sure to delete?',function(btn){
                        if (btn == 'yes'){
                            Ext.Ajax.request({
                                url: '/experiments/delete/reagent/?no='+rec.get('reagent_no'),
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

