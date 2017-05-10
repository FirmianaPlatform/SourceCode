Ext.define('gar.view.Search', {
			extend : 'Ext.grid.Panel',
			alias : 'widget.search',
			rowLines : true,
			columnLines : true,
			loadMask : true,
			//frame:true,
			columns : [ {
						xtype : 'rownumberer',
						width : 50
					}, 
//						{
//						text:"+",
//						align : 'center',
//						xtype : 'checkcolumn',
//						width : 40,
//						dataIndex : 'active1',
//						sortable : false
//					}, 
						{
						text : 'Repeat ID',
						dataIndex : 'repeat_id'
					}, {
						text : 'Rank ID',
						dataIndex : 'rank'
					}, {
						text : 'File Name',
						dataIndex : 'name'
					}, {
						text : 'Spectrum Num',
						dataIndex : 'num_spectrum'
					}, {
						text : 'Peptide Num',
						dataIndex : 'num_peptide',
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							cssstring = '<div class="x-grid3-cell-inner" style="text-align:center;';
							cssstring += '">' + "<a href='#'>"
							return cssstring + value + '</a>' + '</div>'

						}
					}, {
						text : 'Isoform Num',
						dataIndex : 'num_isoform',
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							cssstring = '<div class="x-grid3-cell-inner" style="text-align:center;';
							cssstring += '">' + "<a href='#'>"
							return cssstring + value + '</a>' + '</div>'

						}
					}, {
						text : 'Gene Num',
						dataIndex : 'num_gene',
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							cssstring = '<div class="x-grid3-cell-inner" style="text-align:center;';
							cssstring += '">' + "<a href='#'>"
							return cssstring + value + '</a>' + '</div>'

						}
					}, {
						text : 'Information',
						dataIndex : 'log',
						flex : 1
					}, {
						text : 'Update Time',
						dataIndex : 'date',
						width:180
					}, {
						text : 'User',
						dataIndex : 'user'
					}, {
						text : 'Progress',
						dataIndex : 'stage'
					}],
			viewConfig : {
				stripeRows : true,
				enableTextSelection : true
			}

		})