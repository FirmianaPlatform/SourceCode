Ext.define('gar.store.CompareTree', {
			extend : 'Ext.data.TreeStore',
			// id : 'exp_store',
			proxy : {
				type : 'ajax',
				timeout : 3600000,
				url : '/gardener/newcmptree/'
			}
		});
