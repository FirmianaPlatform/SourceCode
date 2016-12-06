Ext.define('gar.model.ShowExperiment', {
			extend : 'Ext.data.Model',
			fields : [{
						name : 'experiment_no',
						type : 'string'
					},{
						name : 'experiment_name',
						type : 'string'
					}, {
						name : 'experimenter',
						type : 'string'
					}, {
						name : 'date',
						type : 'date'
					}, {
						name : 'instrument',
						type : 'string'
					}, {
						name : 'digest_enzyme',
						type : 'string'
					}, {
						name : 'digest_type',
						type : 'string'
					}, {
						name : 'samples',
						type : 'string'
					}, {
						name : 'reagents',
						type : 'string'
					}, {
						name : 'separations',
						type : 'string'
					}]
		});