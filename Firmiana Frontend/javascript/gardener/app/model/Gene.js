Ext.define('gar.model.Gene', {
			extend : 'Ext.data.Model',
			fields : [{
						name : 'id',
						type : 'int'
					}, {
						name : 'exp_description',
						type : 'string'
					}, {
						name : 'search_id',
						type : 'int'
					}, {
						name : 'gene_id',
						type : 'int'
					}, {
						name : 'symbol',
						type : 'string'
					}, {
						name : 'protein_gi',
						type : 'string'
					}, {
						name : 'num_proteins',
						type : 'int'
					}, {
						name : 'num_identified_proteins',
						type : 'int'
					}, {
						name : 'num_uni_proteins',
						type : 'int'
					}, {
						name : 'num_peptides',
						type : 'int'
					}, {
						name : 'num_uni_peptides',
						type : 'int'
					}, {
						name : 'area',
						type : 'float'
					}, {
						name : 'fot',
						type : 'float'
					}, {
						name : 'ibaq',
						type : 'float'
					}, {
						name : 'fdr',
						type : 'float'
					}, {
						name : 'description',
						type : 'string'
					}, {
						name : 'annotation',
						type : 'string'
					}, {
						name : 'modification',
						type : 'string'
					}, {
						name : 'relation',
						type : 'string'
					}, {
						name : 'exp_name',
						type : 'string'
					}, {
						name : 'user_specified',
						type : 'string'
					}, {
						name : 'fdr',
						type : 'float'
					}]
		});