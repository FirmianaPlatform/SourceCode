Ext.define('gar.store.digestEnzyme', {
			extend : 'Ext.data.Store',
			//id : 'exp_store',
			autoLoad : true,
			model : 'gar.model.digestEnzyme',
			pageSize : 100,
			buffered : true,
			leadingBufferZone : 300,
			proxy : {
					type : 'ajax',
					url : '/experiments/ajax/display/Digest_enzyme/',
					reader : {
						type : 'json',
						root : 'Digest_enzymes'
					}
				}
		});
