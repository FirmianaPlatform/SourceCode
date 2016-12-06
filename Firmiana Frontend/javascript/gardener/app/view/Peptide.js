Ext.define('gar.view.Peptide', {
	extend : 'Ext.grid.Panel',
	alias : 'widget.peptide',
	border : false,
	// frame:true,
	autoscroll : true,
	rowLines : true,
	columnLines : true,
	// margin : "0 0 10 0",
	// height : 180,
	viewConfig : {
		// stripeRows : true,
		enableTextSelection : true
	},
	multiSelect : true,
	// forceFit:true,
	plugins : {
		ptype : 'bufferedrenderer',
		trailingBufferZone : 0,
		leadingBufferZone : 100
	},
	columns : [{
				xtype : 'rownumberer',
				width : 50
			}, {
				text : 'Exp Name',
				dataIndex : 'exp_name',
				hidden : true
			}, {
				text : 'Experiment Description',
				dataIndex : 'exp_description',
				hidden : true
			}, {
				text : "Sequence",
				align : 'left',
				dataIndex : 'sequence',
				filter : {
					type : 'string',
					encode : true
				},
				sortable : true,
				renderer : function(value) {
					return Ext.String
							.format(
									'<a href="https://db.systemsbiology.net/sbeams/cgi/PeptideAtlas/Search?search_key={0}&build_type_name=Any&action=GO"  target="_blank" title={0}>{0}</a>',
									value);
				}
			}, {
				text : "PSMs",
				dataIndex : 'num_psms',
				filter : {
					type : 'int',
					encode : true
				},
				sortable : true,
				renderer : function(value, metaData, record, rowIndex, colIndex, store) {
					cssstring = '<div class="x-grid3-cell-inner" style="text-align:center;';
					cssstring += '">' + "<a href='#'>"
					return cssstring + value + '</a>' + '</div>'

				}
			}, {
				text : "Protein Groups",
				dataIndex : 'num_protein_groups',
				filter : {
					type : 'int',
					encode : true
				},
				renderer : function(value, metaData, record, rowIndex, colIndex, store) {
					metaData.tdAttr = "title='" + value + "'";
					return value
				},
				sortable : true
			}, {
				text : "Protein Group Accessions",
				dataIndex : 'protein_group_accessions',
				filter : {
					type : 'string',
					encode : true
				},
				renderer : function(value, metaData, record, rowIndex, colIndex, store) {
					metaData.tdAttr = "title='" + value + "'";
					return value
				},
				sortable : true
			}, {
				text : "Modification",
				dataIndex : 'modification',
				filter : {
					type : 'string',
					encode : true
				},
				renderer : function(value, metaData, record, rowIndex, colIndex, store) {
					metaData.tdAttr = "title='" + value + "'";
					return value
				},
				sortable : true
			}, {
				text : "Area",
				dataIndex : 'area',
				filter : {
					type : 'float',
					encode : true
				},
				sortable : true,
				renderer : function(value, rocord, store) {
					// console.log(store.getProxy().getReader())
					big = 1e9
					ratio = value / big
					p = parseInt(255 - ratio * 255);
					if (ratio > 1) {
						p = parseInt(0);
					}
					k = ("00" + p.toString(16)).substr(p.toString(16).length)
					s = "#ff" + k + k
					return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + value.toExponential(5) + '</div>'
				}
			}, {
				text : "FOT(*10^-6)",
				// hidden : true,
				dataIndex : 'fot',
				filter : {
					type : 'float',
					encode : true
				},
				renderer : function(value) {
					return value.toExponential(5);
				},
				sortable : true
			}, {
				text : "Q Value",
				// hidden : true,
				dataIndex : 'q_value',
				filter : {
					type : 'float',
					encode : true
				},
				sortable : true
			}, {
				text : "PEP",
				// hidden : true,
				dataIndex : 'pep',
				filter : {
					type : 'float',
					encode : true
				},
				sortable : true
			}, {
				text : "Ion Score",
				dataIndex : 'ion_score',
				filter : {
					type : 'float',
					encode : true
				},
				sortable : true
			}, {
				text : "Exp Score",
				dataIndex : 'exp_value',
				filter : {
					type : 'float',
					encode : true
				},
				sortable : true,
				renderer : function(value) {
					return value.toExponential(3);
				}
			}, {
				text : "Charge",
				dataIndex : 'charge',
				filter : {
					type : 'int',
					encode : true
				},
				sortable : true
			}, {
				text : "MH+",
				dataIndex : 'mh_da',
				filter : {
					type : 'float',
					encode : true
				},
				sortable : true,
				renderer : function(value) {
					return value.toFixed(4);
				}
			}, {
				text : "Delta M",
				dataIndex : 'delta_m_ppm',
				filter : {
					type : 'float',
					encode : true
				},
				sortable : true,
				renderer : function(value) {
					return value.toFixed(4);
				}
			}, {
				text : "Retention Time(minute)",
				dataIndex : 'rt_min',
				filter : {
					type : 'float',
					encode : true
				},
				sortable : true
			}, {
				text : "Missed Cleavages Num",
				dataIndex : 'num_missed_cleavages',
				filter : {
					type : 'int',
					encode : true
				},
				sortable : true
			}, {
				text : 'From where',
				dataIndex : 'from_where',
				filter : {
					type : 'string',
					encode : true
				},
				renderer : function(value, metaData, record, rowIndex, colIndex, store) {
					metaData.tdAttr = "title='" + value + "'";
					return value
				},
				sortable : true
			}, {
				text : "FDR",
				dataIndex : 'fdr',
				filter : {
					type : 'float',
					encode : true
				},
				renderer : function(value) {
					s = "#ffffff"
					if (value >= 0.04999) {
						s = "#c8c8c8";
					}
					return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + value.toFixed(4) + '</div>'
				}
			}]

})