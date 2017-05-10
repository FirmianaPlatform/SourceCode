Ext.define('gar.store.SilacProtein', {
			extend : 'Ext.data.Store',
			autoLoad : true,
			model : 'gar.model.SilacProtein',
			pageSize : 400,
			buffered : true,
			proxy : {
				type : 'ajax',
				url : '/gardener/data/silacprotein_compare/',
				timeout:600000,
				reader : {
					type : 'json',
					root : 'data',
					totalProperty : 'total'
				}
			}
		});
 