Ext.define('gar.model.Notice', {
			extend : 'Ext.data.Model',
			fields : [{
						name : 'id',
						type : 'int'
					}, {
						name : 'csv_name',
						type : 'int'
					}, {
						name : 'explist',
						type : 'string'
					}, {
						name : 'dmz',
						type : 'float'
					}, {
						name : 'drt',
						type : 'float'
					}, {
						name : 'ionscore',
						type : 'float'
					}, {
						name : 'searchs',
						type : 'string'
					}, {
						name : 'compare',
						type : 'string'
					}, {
						name : 'qc',
						type : 'string'
					}, {
						name : 'done',
						type : 'string'
					}, {
						name : 'ProGene',
						type : 'string'
					}, {
						name : 'create_time',
						type : 'string'
					}, {
						name : 'update_time',
						type : 'string'
					}, {
						name : 'user',
						type : 'string'
					}, {
						name : 'status',
						type : 'string'
					}, {
						name : 'exp_name',
						type : 'string'
					}, {
						name : 'explist_length',
						type : 'int'
					},  {
						name : 'description',
						type : 'string'
					}]
		})