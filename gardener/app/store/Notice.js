Ext.define('gar.store.Notice', {
			initComponent : function() {

			},
			extend : 'Ext.data.Store',
			autoLoad : true,
			model : 'gar.model.Notice',
			pageSize : 400,
			buffered : true,
			//leadingBufferZone : 300,
			proxy : {
				timeout : 3000000,
				type : 'ajax',
				url : '/gardener/data/showjob/',
				reader : {
					type : 'json',
					root : 'data',
					totalProperty : 'total'
				}
			}
			
});
