Ext.define('gar.store.instrumentManufacturer', {
			extend : 'Ext.data.Store',
			// id : 'exp_store',
			autoLoad : true,
			model : 'gar.model.instrumentManufacturer',
			pageSize : 100,
			buffered : true,
			leadingBufferZone : 300,
			proxy : {
				type : 'ajax',
				url : '/experiments/ajax/display/Instrument_manufacturer/',
				reader : {
					type : 'json',
					root : 'Instrument_manufacturers'
				}
			}
		});
