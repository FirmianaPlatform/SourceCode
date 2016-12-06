Ext.define('gar.store.Experiment', {
			extend : 'Ext.data.Store',
			id : 'exp_store',
			autoLoad : true,
			model : 'gar.model.Experiment',
			pageSize : 100,
			buffered : true,
			proxy : {
				type : 'ajax',
				url : '/gardener/data/showdatabase/',
				reader : {
					type : 'json',
					root : 'data',
					totalProperty : 'total'
				}

			}
		});
