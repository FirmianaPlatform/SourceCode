Ext.define('gar.view.ShowReagent', {
	extend : 'Ext.grid.Panel',
	border : false,
	columnLines : true,
	loadMask : true,
	columns : [{
            text: 'Reagent No',
            flex: 1,
            dataIndex: 'reagent_no'
        },{
            text:'Reagent Type',
            flex: 1,
            dataIndex: 'reagent_type'
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
            text:'Applications',
            flex: 1,
            dataIndex:'applications'
        },{
            text:'React Species',
            flex: 1,
            dataIndex:'react_speciess'
        },{
            text:'Catalog',
            flex: 1,
            dataIndex:'catalog_no'
        },{
            xtype: 'actioncolumn',
            flex: 1,
            items:[{
                icon: '/static/images/edit.png',
                tooltip: 'Edit',
                handler: function(grid, rowIndex, colIndex){
                    var rec  =  grid.getStore().getAt(rowIndex);
                    EditReagent(rec.get('reagent_no'))
                    //document.location.href = '/experiments/edit/reagent/?no='+rec.get('reagent_no');
                }
            },{},{
                icon: '/static/images/delete-item.png',
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
                                        grid.getStore().load();
                                    }else{
                                        Ext.Msg.alert('Fail', responseArray.error);
                                    }
                                }
                            });
                        }
                    });
                }
            }]
        }]
})
