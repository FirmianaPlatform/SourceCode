Ext.define('gar.store.Gene', {
			extend : 'Ext.data.Store',
			autoLoad : true,
			model : 'gar.model.Gene',
			pageSize : 400,
			buffered : true,
			//leadingBufferZone : 300,
			proxy : {
				type : 'ajax',
				url : '/gardener/data/showgene/',
				reader : {
					type : 'json',
					root : 'data',
					totalProperty : 'total'
				}
			}
		});
