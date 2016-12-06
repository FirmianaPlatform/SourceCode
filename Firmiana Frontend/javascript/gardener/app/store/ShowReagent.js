Ext.define('gar.store.ShowReagent', {
			extend : 'Ext.data.Store',
			id : 'show_rea_store',
			autoLoad : true,
			remoteSort : true,
			model : 'gar.model.ShowReagent',
			pageSize : 100,
			buffered : true,
			leadingBufferZone : 300,
			proxy : {
				type : 'ajax',
				url : '/experiments/data/reagent/',
				reader : {
					type : 'json',
					root : 'reagents',
					totalProperty : 'total'
				},
				simpleSortMode : true
			},
			sorters : [{
						property : 'reagent_no',
						direction : 'DESC'
					}]
		});
