Ext.define('gar.store.TicRank', {
			extend : 'Ext.data.Store',
			model : 'gar.model.TicRank',
			proxy : {
				type : 'ajax',
				url : '/gardener/data/get_rank/',
				reader : {
					type : 'json',
					root : 'data',
					totalProperty : 'total'
				}

			}
		});
