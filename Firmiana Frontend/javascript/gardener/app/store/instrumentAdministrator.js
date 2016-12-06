Ext.define('gar.store.instrumentAdministrator', {
			extend : 'Ext.data.Store',
			//id : 'exp_store',
			autoLoad : true,
			model : 'gar.model.instrumentAdministrator',
			pageSize : 100,
			buffered : true,
			leadingBufferZone : 300,
			proxy : {
					type : 'ajax',
					url : '/experiments/ajax/display/Instrument_administrator/',
					reader : {
						type : 'json',
						root : 'Instrument_administrators'
					}
				}
		});
