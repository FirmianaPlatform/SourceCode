Ext.define('gar.model.PeptidePlot', {
				extend : 'Ext.data.Model',
				fields : [{
							name : 'id',
							type : 'int'
						},{
							name : 'rt',
							type : 'float'
						},{
							name : 'ms1_rt',
							type : 'float'
						}, {
							name : 'pre_mz',
							type : 'float'
						}, {
							name : 'ms2_scan',
							type : 'int'
						},{
							name : 'search_id',
							type : 'int'
						},{
							name : 'ms1_scan',
							type : 'int'
						},{
							name : 'intensity',
							type : 'float'
						}, {
							name : 'area',
							type : 'float'
						}, {
							name : 'sequence',
							type : 'string'
						}, {
							name : 'modification',
							type : 'string'
						}, {
							name : 'rank',
							type : 'int'
						}, {
							name : 'repeat_id',
							type : 'int'
						}, {
							name : 'fraction_id',
							type : 'int'
						},{
							name : 'xplot',
							type : 'float'
						}, {
							name : 'yplot',
							type : 'float'
						}, {
							name : 'charge',
							type : 'int'
						}, {
							name : 'filename',
							type : 'string'
						}]
			});