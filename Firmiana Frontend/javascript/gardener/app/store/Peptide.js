Ext.define('gar.store.Peptide', {
			initComponent : function() {

			var max=0;		
			},
			extend : 'Ext.data.Store',
			autoLoad : true,
			model : 'gar.model.Peptide',
			pageSize : 400,
			buffered : true,
			//leadingBufferZone : 300,
			proxy : {
				timeout : 3000000,
				type : 'ajax',
				url : '/gardener/data/showpeptide/',
				reader : {
					type : 'json',
					root : 'data',
					totalProperty : 'total'
				}
			},
			getmax:function(){
				return max;
			},
			setmax:function(v){
				max=v
			}
			
});
