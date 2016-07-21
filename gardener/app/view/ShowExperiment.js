Ext.define('gar.view.ShowExperiment', {
	extend : 'Ext.grid.Panel',
	border : false,
	columnLines : true,
	loadMask : true,
	columns : [{
				text : 'EID',
				flex : 1,
				dataIndex : 'experiment_no'
			},{
				text : 'Exp Name',
				flex : 1,
				dataIndex : 'experiment_name'
			}, {
				text : 'Experimenter',
				flex : 1,
				dataIndex : 'experimenter'
			}, {
				xtype : 'datecolumn',
				text : 'Date',
				dataIndex : 'date',
				flex : 1,
				format : 'Y-m-d'
			}, {
				text : 'Instrument',
				flex : 1,
				dataIndex : 'instrument'
			}, {
				text : 'Digest type',
				flex : 1,
				dataIndex : 'digest_type'
			}, {
				text : 'Digest enzyme',
				flex : 1,
				dataIndex : 'digest_enzyme'
			}, {
				text : 'Samples',
				flex : 1,
				dataIndex : 'samples'
			}, {
				text : 'Reagents',
				flex : 1,
				dataIndex : 'reagents'
			}, {
				text : 'Separation',
				flex : 1,
				dataIndex : 'separations'
			}, {
				xtype : 'actioncolumn',
				flex : 1,
				items : [{
					icon : '/static/images/edit.png',
					tooltip : 'Edit',
					handler : function(grid, rowIndex, colIndex) {
						//Ext.Msg.alert('Building', 'This function is not ready.')
						//var rec = grid.getStore().getAt(rowIndex);
						//document.location.href = '/experiments/edit/experiment/?no='
						//		+ rec.get('experiment_no');
						
						var rec  =  grid.getStore().getAt(rowIndex);
						console.log(rec.get('experiment_no'));
                        EditExperiment(rec.get('experiment_no'));
						
					}
				}, {},{
					icon : '/static/images/delete-item.png',
					tooltip : 'Delete',
					handler : function(grid, rowIndex, colIndex) {
						console.log(grid)
						var rec = grid.getStore().getAt(rowIndex);
						Ext.MessageBox.confirm('Confirm delete',
								'Are you sure to delete?', function(btn) {
									if (btn == 'yes') {
										Ext.Ajax.request({
											url : '/experiments/delete/experiment/?no='
													+ rec.get('experiment_no'),
											success : function(response, store) {

												responseArray = Ext.JSON.decode(response.responseText);
												if (responseArray.success == 'True') {
													grid.store.load()
													//grid.refresh()
												} else {
													Ext.Msg.alert('Fail',responseArray.error);
												}

											}
										});
									//	grid.store.reload()
									//	Ext.getCmp(grid.id).refresh()
									}
								});
					}
				}]
			}]
})
