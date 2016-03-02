Ext.define('gar.store.Ms1_tic', {
			extend : 'Ext.data.Store',
			id : 'tic_store',
			model : 'gar.model.Ms1_tic',
			proxy : {
				type : 'ajax',
				url : '/gardener/data/showms1_tic_data/',
				reader : {
					type : 'json',
					root : 'data',
					totalProperty : 'total'
				}

			}
		});
