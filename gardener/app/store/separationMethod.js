Ext.define('gar.store.separationMethod', {
			extend : 'Ext.data.Store',
			// id : 'exp_store',
			autoLoad : true,
			model : 'gar.model.separationMethod',
			pageSize : 100,
			buffered : true,
			leadingBufferZone : 300,
			proxy : {
				type : 'ajax',
				url : '/experiments/ajax/display/Separation_method/',
				reader : {
					type : 'json',
					root : 'Separation_methods'
				}
			}
		});
