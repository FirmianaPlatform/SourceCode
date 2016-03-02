Ext.define('gar.model.MBRun', {
			extend : 'Ext.data.Model',
			fields : [{
						name : 'id',
						type : 'int'
					}, {
						name : 'name',
						type : 'string'
					}, {
						name : 'num_fraction',
						type : 'int'
					}, {
						name : 'num_repeat',
						type : 'int'
					}]
		});