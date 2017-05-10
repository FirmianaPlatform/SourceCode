Ext.define('gar.model.Experiment', {
			extend : 'Ext.data.Model',
			fields : [{
						name : 'id',
						type : 'int'

					}, {
						name : 'name',
						type : 'string'
					}, {
						name : 'type',
						type : 'string'
					}, {
						name : 'description',
						type : 'string'
					}, {
						name : 'species',
						type : 'string'
					}, {
						name : 'cell_type',
						type : 'string'
					}, {
						name : 'tissue',
						type : 'string'
					}, {
						name : 'organ',
						type : 'string'
					}, {
						name : 'fluid',
						type : 'string'
					}, {
						name : 'num_fraction',
						type : 'int'
					}, {
						name : 'num_repeat',
						type : 'int'
					}, {
						name : 'num_spectrum',
						type : 'int'
					}, {
						name : 'num_peptide',
						type : 'int'
					}, {
						name : 'num_isoform',
						type : 'int'
					}, {
						name : 'num_gene',
						type : 'int'
					}, {
						name : 'instrument',
						type : 'string'
					}, {
						name : 'protocol',
						type : 'string'
					}, {
						name : 'lab',
						type : 'string'
					}, {
						name : 'operator',
						type : 'string'
					}, {
						name : 'experiment_date',
						type : 'date'
					}, {
						name : 'index_date',
						type : 'date'
					}, {
						name : 'update_date',
						type : 'date'
					}, {
						name : 'stage',
						type : 'int'
					}, {
						name : 'state',
						type : 'string'
					}, {
						name : 'ispec_no',
						type : 'string'
					}, {
						name : 'bait',
						type : 'string'
					}, {
						name : 'ispec',
						type : 'string'
					}, {
						name : 'specific',
						type : 'string'
					}]
		});