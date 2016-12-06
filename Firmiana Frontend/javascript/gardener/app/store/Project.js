Ext.define('gar.store.Project', {
			extend : 'Ext.data.Store',
			//id : 'exp_store',
			autoLoad : true,
			model : 'gar.model.Project',
			pageSize : 100,
			buffered : true,
			leadingBufferZone : 300,
			proxy : {
				type : 'ajax',
				url : '/experiments/ajax/display/Project/',
				reader : {
						type : 'json',
						root : 'Projects'
					}

			}
		});
