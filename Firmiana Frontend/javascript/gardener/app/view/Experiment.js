Ext.define('gar.view.Experiment', {
			extend : 'Ext.grid.Panel',
			alias : 'widget.experiment',
			border : false,
			//frame:true,
			//autoscroll : true,
			viewConfig : {
				//trackOver: false,
				//stripeRows : true
				//enableTextSelection : true
			},
			//forceFit:true,
			multiSelect: true,
			//selType: 'checkboxmodel',
			plugins : [
				{ptype:'bufferedrenderer',trailingBufferZone:0,leadingBufferZone:100}
				],
			columnLines : true,
			
			columns : [
					{//locked:true,
						text : "",
						xtype : 'rownumberer',
						width : 45
					}, {	//locked:true,
							text:"+",
							align : 'center',
							width : 40,
							dataIndex : 'id',
							sortable : false,
							renderer : function(val) {
								//console.log("<input id='experiment_selector_" + val + "' type='checkbox' value=" + val + "/>")
								return "<div style=\"height:12px;\"><input id='experiment_selector_" + val + "' type='checkbox' value=" + val + "/><div>";
								
							}
					}, {//locked:true,
						text : "Name",
						align : 'left',
						dataIndex : 'name',
						width : 90,
						filter : {
							type : 'string',
							encode : true
						},
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							cssstring = '<div title="Click to view Experiment Detail" class="x-grid3-cell-inner" style="text-align:center;';
							cssstring += '">' + "<a href='#'>"
							return cssstring + value + '</a>' + '</div>'

						},
						sortable : true
					}, {
						text : "Type",
						width : 70,
						dataIndex : 'type',
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
						text : "Bait",
						width : 70,
						dataIndex : 'bait',
						filter : {
							type : 'string',
							encode : true
						},
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							metaData.tdAttr = "title='" + value + "'";
							return value 
						},
						sortable : true
					},{
						width : 250,
						text : "Description",
						dataIndex : 'description',
						filter : {
							type : 'string',
							encode : true
						},
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							metaData.tdAttr = "title='" + value + "'";
							return value 
						},
						sortable : true,
						flex : 1
					}, {
						text : "Species",
						hidden:true,
						dataIndex : 'species',
						width : 100,
						filter : {
							type : 'string',
							encode : true
						},
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							metaData.tdAttr = "title='" + value + "'";
							return value 
						},
						sortable : true
					},{
						text : "CTOF",
						hidden:true,
						//dataIndex : '',
						width : 200,
						filter : {
							type : 'string',
							encode : true
						},
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							
							value='';
							
							if (record.get('cell_type')!='-')
								value=value+'C: '+record.get('cell_type')+'; '
							if (record.get('organ')!='-')
								value=value+'O: '+record.get('organ')+'; '
							if (record.get('fluid')!='-')
								value=value+'F: '+record.get('fluid')+'; '
							metaData.tdAttr = "title='" + value + "'";
							return value
						},
						sortable : true
					}, {
						text : "Cell type",
						dataIndex : 'cell_type',
						hidden:true,
						width : 100,
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
						text : "Tissue",
						dataIndex : 'tissue',
						width : 100,
						hidden:true,
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
						text : "Organ",
						dataIndex : 'organ',
						width : 100,
						hidden:true,
						filter : {
							type : 'string',
							encode : true
						},
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							metaData.tdAttr = "title='" + value + "'";
							return value 
						},
						sortable : true
					},{
						text : "Fluid",
						dataIndex : 'fluid',
						width : 100,
						hidden:true,
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
						text : "Fraction",
						dataIndex : 'num_fraction',
						width : 80,
						filter : {
							type : 'int',
							encode : true
						},
						sortable : true
					}, {
						text : "Repeat",
						dataIndex : 'num_repeat',
						width : 80,
						filter : {
							type : 'int',
							encode : true
						},
						sortable : true
					}, {
						text : "Spectrum Num",
						dataIndex : 'num_spectrum',
						width : 110,
						filter : {
							type : 'int',
							encode : true
						},
						sortable : true,
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							cssstring = '<span title="Click to view TIC Plot" class="x-grid3-cell-inner" style="text-align:center;';
							cssstring += '">' + "<a href='#'>"
							return cssstring + value + '</a>' + '</span>'

						}
					}, {
						text : "Peptide Num",
						dataIndex : 'num_peptide',
						width : 100,
						filter : {
							type : 'int',
							encode : true
						},
						sortable : true,
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							cssstring = '<span title="Click to view Peptide List" class="x-grid3-cell-inner" style="text-align:center;';
							cssstring += '">' + "<a href='#'>"
							return cssstring + value + '</a>' + '</span>'

						}
					}, {
						text : "Isoform Num",
						dataIndex : 'num_isoform',
						width : 100,
						filter : {
							type : 'int',
							encode : true
						},
						sortable : true,
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							cssstring = '<div title="Click to view Protein List" class="x-grid3-cell-inner" style="text-align:center;';
							cssstring += '">' + "<a href='#'>"
							return cssstring + value + '</a>' + '</div>'

						}
					}, {
						text : "Gene Num",
						dataIndex : 'num_gene',
						width : 100,
						filter : {
							type : 'int',
							encode : true
						},
						sortable : true,
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							cssstring = '<div title="Click to view Gene List" class="x-grid3-cell-inner" style="text-align:center;';
							cssstring += '">' + "<a href='#'>"
							return cssstring + value + '</a>' + '</div>'

						}
					}, {
						text : "Instrument",
						hidden : false,
						dataIndex : 'instrument',
						width : 100,
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
						text : "Protocol",
						hidden : true,
						dataIndex : 'protocol',
						width : 100,
						filter : {
							type : 'string',
							encode : true
						},
						sortable : true
					}, {
						text : "Lab",
						hidden : true,
						dataIndex : 'lab',
						width : 100,
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
						text : "Operator",
						hidden : true,
						dataIndex : 'operator',
						width : 100,
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
						text : "Experiment Date",
						hidden : true,
						dataIndex : 'experiment_date',
						width : 100,
						filter : {
							type : 'date',
							encode : true
						},
						sortable : true
					}, {
						text : "Index Date",
						hidden : true,
						dataIndex : 'index_date',
						width : 100,
						filter : {
							type : 'date',
							encode : true
						},
						renderer : Ext.util.Format.dateRenderer('m/d/Y'),
						sortable : true
					}, {
						text : "Update date",
						hidden : true,
						dataIndex : 'update_date',
						width : 50,
						filter : {
							type : 'date',
							encode : true
						},
						renderer : Ext.util.Format.dateRenderer('m/d/Y'),
						sortable : true
					}, {
						text : "State",
						hidden : true,
						dataIndex : 'state',
						filter : {
							type : 'string',
							encode : true
						},
						sortable : true
					}, {
						text : "Progress",
						align : 'center',
						dataIndex : 'stage',
						width : 80,
						filter : {
							type : 'int',
							encode : true
						},
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							var value_display = value
							var tip = '';
							var state = record.get('state');
							cssstring = '<div style="';
							switch (value) {
								case -1:
									tip = "Metadata added"
									break;
								case 0 :
									tip = "Files copied to workflow server"
									break;
								case 1 :
									tip = "Workflow started"
									break;
								case 2 :
									tip = "Complete conversion of raw files"
									break;
								case 3 :
									tip = "Complete conversion of mzXML to mgf"
									break;
								case 4 :
									tip = "Complete Mascot search"
									break;
								case 5 :
									tip = "Complete parsing Mascot result"
									break;
							}
							
							bkimg = "";
							bksz = "";
							bkpst = "";
							bkrp = "";
							pst = 0;
							{								
								if(value==5)
									{
										bkimg += ("url(/static/images/bkg_green.png),")
										metaData.tdAttr = "title='" + tip + "'";
										pst = value * 100 / 5;
										value_display = 'Done'
										cssstring += 'color:white;';
									}
								
								else if(value>0)
									{
										pst = value * 100 / 5;
										if(state=='error'){
											bkimg += ("url(/static/images/bkg_red.png),")
											tip = 'Error happend'
										}
										else{
											bkimg += ("url(/static/images/bkg_yellow.png),")
										}
										metaData.tdAttr = "title='" + tip + "'";
									}
									
								else if(value==0)
									{	
										bkimg += ("url(/static/images/bkg_blue.png),")
										metaData.tdAttr = "title='" + tip + "'";
										pst = 100;
										value_display = 'Queued'
										cssstring += 'color:white;';
									}
								else
									{	
										bkimg += ("url(/static/images/bkg_gray.png),")
										metaData.tdAttr = "title='" + tip + "'";
										pst = 100;
										value_display = 'No file'
										cssstring += 'color:white;';
									}
								bksz += (pst.toString());
								bksz += ("% 100%,")
								bkpst += ("0% 0%,")
								bkrp += "no-repeat,"
							}
							
							{
								cssstring += 'background-image:';
								cssstring += bkimg.substr(0, bkimg.length - 1) + ";";
								cssstring += 'background-size:';
								cssstring += bksz.substr(0, bksz.length - 1) + ";";
								cssstring += 'background-position:';
								cssstring += bkpst.substr(0, bkpst.length - 1) + ";";
								cssstring += 'background-repeat:';
								cssstring += bkrp.substr(0, bkrp.length - 1) + ";";

							}
							cssstring += '">'
							
							
							return cssstring + value_display + '</div>'

						},
						sortable : true
					},{
						text : "Ispec No",
						hidden : true,
						dataIndex : 'ispec',
						filter : {
							type : 'string',
							encode : true
						},
						sortable : true
					},{
						text : "Specific ID",
						hidden : true,
						dataIndex : 'specific',
						filter : {
							type : 'string',
						encode : true
						},
						sortable : true
					},{
				width : 50,
				align : 'center',
				text : "Rerun",
				xtype : 'actioncolumn',
				//hidden:true,
				items:[
						{
						iconCls:'redo',
						tooltip:'Truncate',
						handler:function(grid, rowIndex, colIndex, self) {
								//console.log(record)
		        				var rerun = function(btn){
		        					if(btn!='yes'){return}
		        					var tmpStage = rec.get('stage') 
									rec.set('stage',0) 
									Ext.Ajax.request({
												timeout : 600000,
												url : '/truncateExp/',
												method : 'GET',
												params : {
													expName:expName
												},
												success : function(response) {
													var text = response.responseText;
													if(text=='OK'){ 
														//rec.set('stage',0) 
														
													}
													else{ 
														rec.set('stage',tmpStage) 
														Ext.Msg.alert('Error','Contact Admin.') 
													}
												},
												failure : function(response) {
													rec.set('stage',tmpStage) 
													Ext.Msg.alert('Error','Network error')
												}
											})
		
										
									}
									//Ext.getCmp('btmessage').fireEvent('click');
								
		        				var rec = grid.getStore().getAt(rowIndex);
		        				var expName = rec.get('name')
								if(rec.get('stage')<0){
									Ext.Msg.alert('Warning','This exp has no file.')
									return
								}
								if(rec.get('stage')==0){
									Ext.Msg.alert('Warning','This exp is queued.')
									return
								}
		        				Ext.MessageBox.confirm('Confirm','Restart '+ expName + ' ?', rerun); 	
						}
					}
				]
				
			}]
		})
