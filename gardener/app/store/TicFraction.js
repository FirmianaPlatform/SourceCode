Ext.define('gar.store.TicFraction', {
			extend : 'Ext.data.Store',
			model : 'gar.model.TicFraction',
			proxy : {
				type : 'ajax',
				url : '/gardener/data/show_tic_fraction/',
				reader : {
					type : 'json',
					root : 'data',
					totalProperty : 'total'
				}

			}
		});
