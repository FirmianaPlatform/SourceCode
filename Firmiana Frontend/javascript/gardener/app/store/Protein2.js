Ext.define('gar.store.Protein2', {
			extend : 'Ext.data.Store',
			autoLoad : true,
			model : 'gar.model.Protein',
			pageSize : 400,
			buffered : true,
			proxy : {
				type : 'ajax',
				url : '/gardener/data/silacprotein/',
				timeout:600000,
				reader : {
					type : 'json',
					root : 'data',
					totalProperty : 'total'
				}
			}
		});
