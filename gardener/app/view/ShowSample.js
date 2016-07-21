Ext.define('gar.view.ShowSample', {
	extend : 'Ext.grid.Panel',
	border : false,
	columnLines : true,
	loadMask : true,
	columns : [{
				text : 'Sample No',
				flex : 1,
				dataIndex : 'sample_no',
				filter : {
					type : 'int',
					encode : true
				},
				sortable : true
			}, {
				text : 'Experimenter',
				flex : 1,
				dataIndex : 'experimenter',
				filter : {
					type : 'string',
					encode : true
				},
				sortable : true
			}, {
				xtype : 'datecolumn',
				text : 'Date',
				flex : 1,
				dataIndex : 'date',
				format : 'Y-m-d',
				filter : {
					type : 'date',
					encode : true
				},
				sortable : true
			}, {
				text : 'txID',
				flex : 1,
				dataIndex : 'txid',
				filter : {
					type : 'string',
					encode : true
				},
				sortable : true
			}, {
				text : 'Cell/Tissue',
				flex : 1,
				dataIndex : 'cell_tissue',
				filter : {
					type : 'string',
					encode : true
				},
				sortable : true
			}, {
				text : 'Subcellular organelle',
				flex : 1,
				dataIndex : 'subcellular_organelle',
				filter : {
					type : 'string',
					encode : true
				},
				sortable : true
			}, {
				text : 'Rx(s)',
				flex : 1,
				dataIndex : 'rx',
				filter : {
					type : 'string',
					encode : true
				},
				sortable : true
			}, {
				text : 'Genotype(s)',
				flex : 1,
				dataIndex : 'genotype',
				filter : {
					type : 'string',
					encode : true
				},
				sortable : true
			}, {
				text : 'Methods',
				flex : 1,
				dataIndex : 'methods',
				filter : {
					type : 'string',
					encode : true
				},
				sortable : true
			}, {
				xtype : 'actioncolumn',
				flex : 1,
				items : [ 
					{},{
					icon : '/static/images/edit.png',
					tooltip : 'Edit',
					handler : function(grid, rowIndex, colIndex) {
						var rec  =  grid.getStore().getAt(rowIndex);
                        EditSample(rec.get('sample_no'));
						
					}
					}, {},{
					icon : '/static/images/delete-item.png',
					tooltip : 'Delete',
					handler : function(grid, rowIndex, colIndex) {
						var rec = grid.getStore().getAt(rowIndex);
						Ext.MessageBox.confirm('Confirm delete',
								'Are you sure to delete?', function(btn) {
									if (btn == 'yes') {
										Ext.Ajax.request({
											url : '/experiments/delete/sample/?no='
													+ rec.get('sample_no'),
											success : function(response) {
												responseArray = Ext.JSON
														.decode(response.responseText);
												if (responseArray.success == 'True') {
													grid.getStore().load();
												} else {
													Ext.Msg.alert('Fail', responseArray.error);
												}
											}
										});
									}
								});
					}
				}]
			}]
});
