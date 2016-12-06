Ext.define('gar.store.Experimenter', {
			extend : 'Ext.data.Store',
			//id : 'exp_store',
			autoLoad : true,
			model : 'gar.model.Experimenter',
			pageSize : 100,
			buffered : true,
			leadingBufferZone : 300,
			proxy : {
				type : 'ajax',
				url : '/experiments/ajax/experimenter/',
				reader : {
						type : 'json',
						root : 'experimenters'
					}

			}
		});
