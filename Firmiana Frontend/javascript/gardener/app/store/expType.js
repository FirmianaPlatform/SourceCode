Ext.define('gar.store.expType', {
			extend : 'Ext.data.Store',
			//id : 'exp_store',
			autoLoad : true,
			model : 'gar.model.expType',
			pageSize : 100,
			buffered : true,
			leadingBufferZone : 300,
			proxy : {
					type : 'ajax',
					url : '/experiments/ajax/display/Experiment_type/',
					reader : {
						type : 'json',
						root : 'Experiment_types'
					}
				}
		});
