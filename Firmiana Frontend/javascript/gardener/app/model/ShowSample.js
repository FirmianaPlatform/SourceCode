Ext.define('gar.model.ShowSample', {
			extend : 'Ext.data.Model',
			fields : [{
						name : 'sample_no',
						type : 'int'
					}, {
						name : 'experimenter',
						type : 'string'
					}, {
						name : 'date',
						type : 'date'
					}, {
						name : 'txid',
						type : 'string'
					}, {
						name : 'cell_tissue',
						type : 'string'
					}, {
						name : 'subcellular_organelle',
						type : 'string'
					}, {
						name : 'rx',
						type : 'string'
					}, {
						name : 'genotype',
						type : 'string'
					}, {
						name : 'methods',
						type : 'string'
					}]
		});