Ext.define('gar.store.ReagentMethod', {
			extend : 'Ext.data.Store',
			//id : 'exp_store',
			autoLoad : true,
			model : 'gar.model.ReagentMethod',
			pageSize : 100,
			buffered : true,
			leadingBufferZone : 300,
			proxy : {
				type : 'ajax',
				url : '/experiments/ajax/display/Reagent_method/',
				reader : {
						type : 'json',
						root : 'Reagent_methods'
					}

			}
		});
