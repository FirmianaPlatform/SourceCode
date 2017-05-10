Ext.define('gar.store.ProtShort', {
			extend : 'Ext.data.Store',
			autoLoad : true,
			model : 'gar.model.ProtShort',
			pageSize : 100,
			buffered : true,
			leadingBufferZone : 300,
			proxy : {
				type : 'ajax',
				url : '/gardener/data/shortprotein/',
				reader : {
					type : 'json',
					root : 'data',
					totalProperty : 'total'
				}
			}
		});
