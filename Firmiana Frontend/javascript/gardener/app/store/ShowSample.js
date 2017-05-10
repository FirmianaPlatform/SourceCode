Ext.define('gar.store.ShowSample', {
	extend : 'Ext.data.Store',
	id : 'show_sam_store',
	autoLoad : true,
	remoteSort : true,
	model : 'gar.model.ShowSample',
	pageSize : 200,
	buffered : true,
	leadingBufferZone : 300,
	proxy : {
		type : 'ajax',
		url : '/experiments/data/sample/',
		reader : {
			type : 'json',
			root : 'samples',
			totalProperty : 'total'
		},
		simpleSortMode : true
	},
	sorters : [{
		property : 'sample_no',
		direction : 'DESC'
	}]
});
