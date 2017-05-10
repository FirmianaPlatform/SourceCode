Ext.define('gar.model.SilacProtein', {
			extend : 'Ext.data.Model',
			fields : [{
						name : 'id',
						type : 'int'
					}, {
						name : 'search_id',
						type : 'int'
					}, {
						name : 'other_members',
						type : 'string'
					}, {
						name : 'exp_description',
						type : 'string'
					},{
						name : 'accession',
						type : 'string'
					}, {
						name : 'symbol',
						type : 'string'
					}, {
						name : 'description',
						type : 'string'
					}, {
						name : 'score',
						type : 'float'
					}, {
						name : 'coverage',
						type : 'float'
					}, {
						name : 'num_proteins',
						type : 'int'
					}, {
						name : 'num_uni_peptides',
						type : 'int'
					}, {
						name : 'num_peptides',
						type : 'int'
					}, {
						name : 'num_psms',
						type : 'int'
					}, {
						name : 'larea',
						type : 'float'
					}, {
						name : 'harea',
						type : 'float'
					}, {
						name : 'area_ratio',
						type : 'float'
					}, {
						name : 'lfot',
						type : 'float'
					}, {
						name : 'hfot',
						type : 'float'
					}, {
						name : 'fot_ratio',
						type : 'float'
					}, {
						name : 'libaq',
						type : 'float'
					}, {
						name : 'hibaq',
						type : 'float'
					}, {
						name : 'ibaq_ratio',
						type : 'float'
					}, {
						name : 'length',
						type : 'int'
					}, {
						name : 'mw',
						type : 'float'
					}, {
						name : 'calc_pi',
						type : 'float'
					}, {
						name : 'annotation',
						type : 'string'
					},{
						name : 'modification',
						type : 'string'
					}, {
						name : 'relation',
						type : 'string'
					}, {
						name : 'exp_name',
						type : 'string'
					},  {
						name : 'user_specified',
						type : 'string'
					}, {
						name : 'fdr',
						type : 'float'
					}]
		});