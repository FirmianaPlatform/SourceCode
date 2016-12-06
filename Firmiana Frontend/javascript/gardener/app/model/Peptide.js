Ext.define('gar.model.Peptide', {
			extend : 'Ext.data.Model',
			fields : [{
						name : 'id',
						type : 'int'
					}, {
						name : 'search_id',
						type : 'int'
					}, {
						name : 'exp_description',
						type : 'string'
					},{
						name : 'quality',
						type : 'string'
					}, {
						name : 'sequence',
						type : 'string'
					}, {
						name : 'num_psms',
						type : 'int'
					}, {
						name : 'num_proteins',
						type : 'int'
					}, {
						name : 'num_protein_groups',
						type : 'int'
					}, {
						name : 'protein_group_accessions',
						type : 'string'
					}, {
						name : 'modification',
						type : 'string'
					}, {
						name : 'delta_cn',
						type : 'float'
					}, {
						name : 'area',
						type : 'float'
					},{
						name : 'fot',
						type : 'float'
					}, {
						name : 'q_value',
						type : 'float'
					}, {
						name : 'pep',
						type : 'float'
					}, {
						name : 'ion_score',
						type : 'float'
					}, {
						name : 'exp_value',
						type : 'float'
					}, {
						name : 'charge',
						type : 'int'
					}, {
						name : 'mh_da',
						type : 'float'
					}, {
						name : 'delta_m_ppm',
						type : 'float'
					}, {
						name : 'rt_min',
						type : 'float'
					}, {
						name : 'num_missed_cleavages',
						type : 'int'
					}, {
						name : 'exp_name',
						type : 'string'
					}, {
						name : 'fdr',
						type : 'float'
					}, {
						name : 'maxx',
						type : 'float'
					}, {
						name : 'from_where',
						type : 'string'
					}]
		})