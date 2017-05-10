Ext.define('gar.model.Search', {
			extend : 'Ext.data.Model',
			fields : [{
						name : 'id',
						type : 'int'
					}, {
						name : 'search_id',
						type : 'int'
					}, {
						name : 'num_fraction',
						type : 'int'
					}, {
						name : 'repeat_id',
						type : 'string'
					}, {
						name : 'exp_id',
						type : 'string'
					}, {
						name : 'fraction_id',
						type : 'string'
					}, {
						name : 'name',
						type : 'string'
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
						name : 'log',
						type : 'string'
					}, {
						name : 'date',
						type : 'date'
					}, {
						name : 'user',
						type : 'string'
					}, {
						name : 'stage',
						type : 'int'
					}, {
						name : 'rank',
						type : 'int'
					}]
		})