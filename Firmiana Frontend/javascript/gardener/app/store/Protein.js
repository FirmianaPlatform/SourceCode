Ext.define('gar.store.Protein', {
			extend : 'Ext.data.Store',
			autoLoad : true,
			model : 'gar.model.Protein',
			pageSize : 400,
			buffered : true,
			proxy : {
				type : 'ajax',
				url : '/gardener/data/showprotein/',
				timeout:600000,
				reader : {
					type : 'json',
					root : 'data',
					totalProperty : 'total'
				}
			}
		});
