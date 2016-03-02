Ext.define('gar.store.MBRun', {
	extend : 'Ext.data.Store',
	autoLoad : true,
	model : 'gar.model.MBRun',
	proxy : {
		type : 'ajax',
		timeout : 3000000,
		url : '/gardener/mecompare/',
		reader : {
			type : 'json',
			root : 'data',
			totalProperty : 'total'
		}
	},
	save : function() {
		var rowsData = [];
		var count = this.getCount();
		var record;
		for (var i = 0; i < count; i++) {
			record = this.getAt(i);
			rowsData.push(record.data);
		}
		Ext.getCmp('info_experiments_selected').setValue(Ext.encode(rowsData));
		//				

	}
		// This particular service cannot sort on more than one
		// field, so if grouped, disable sorting

	});
