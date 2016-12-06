Ext.define('gar.store.ShowExperiment', {
			extend : 'Ext.data.Store',
			id : 'show_exp_store',
			autoLoad : true,
			remoteSort : true,
			model : 'gar.model.ShowExperiment',
			pageSize : 100,
			buffered : true,
			leadingBufferZone : 300,
			proxy : {
				type : 'ajax',
				url : '/experiments/data/experiment/',
				reader : {
					type : 'json',
					root : 'experiments',
					totalProperty : 'total'
				},
				simpleSortMode : true
			},
			sorters : [{
						property : 'experiment_no',
						direction : 'DESC'
					}]
		});
