Ext.define('gar.model.ExperimentPlot', {
				extend : 'Ext.data.Model',
				fields : [{
							name : 'id',
							type : 'string'
						},{
							name : 'exp_id',
							type : 'int'
						}, {
							name : 'name',
							type : 'string'
						}, {
							name : 'type',
							type : 'string'
						},{
							name : 'repeat_id',
							type : 'int'
						},{
							name : 'rank',
							type : 'int'
						},{
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
							name : 'stage',
							type : 'int'
						}]
			});