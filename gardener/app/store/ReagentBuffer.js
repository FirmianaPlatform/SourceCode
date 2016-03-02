Ext.define('gar.store.ReagentBuffer', {
			extend : 'Ext.data.Store',
			//id : 'exp_store',
			autoLoad : true,
			model : 'gar.model.ReagentBuffer',
			pageSize : 100,
			buffered : true,
			leadingBufferZone : 300,
			proxy : {
				type : 'ajax',
				url : '/experiments/ajax/display/Reagent_buffer/',
				reader : {
						type : 'json',
						root : 'Reagent_buffers'
					}

			}
		});
