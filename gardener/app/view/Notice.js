Ext.define('gar.view.Notice', {
	extend : 'Ext.grid.Panel',
	alias : 'widget.notice',
	border : false,
	autoscroll : true,
	rowLines : true,
	columnLines : true,
	viewConfig : {
		stripeRows : true,
		enableTextSelection : true
	},
	multiSelect : true,
	//forceFit : true,
	requires: [ 'Ext.selection.CellModel' ],
	plugins : {
		ptype : 'bufferedrenderer',
		trailingBufferZone : 0,
		leadingBufferZone : 100
	},
	
 	initComponent: function() {
        this.cellEditing = new Ext.grid.plugin.CellEditing({
            clicksToEdit: 1
        });
        Ext.apply(this, {
        	plugins: [this.cellEditing],
			columns : [{
						xtype : 'rownumberer',
						width : 50
					}, {
						text : "ID",
						hidden : true,
						dataIndex : 'csv_name',
						width : 50
					}, {
						hidden : true,
						dataIndex : 'explist'
					}, {
						width : 50,
						align : 'center',
						text : "Rerun",
						xtype : 'actioncolumn',
						hidden:true,
						items:[
								{
								iconCls:'redo',
								tooltip:'Rerun',
								handler:function(grid, rowIndex, colIndex, self) {
										//console.log(record)
				        				var rerun = function(btn){
				        					if(btn!='yes'){return}
											rec.set('status','running')
											Ext.Ajax.request({
														timeout : 600000,
														url : '/gardener/newcmpprotein/',
														method : 'GET',
														params : {
															id : val,
															type:1,
															rerun:1
														},
														success : function(response) {},
														failure : function(response) {}
													})
				
												
											}
											//Ext.getCmp('btmessage').fireEvent('click');
										
				        				var rec = grid.getStore().getAt(rowIndex);
				        				//haha = rec
				        				var val = String(rec.get('csv_name'));
				        				//grid.getStore().load()
										if(rec.get('status')=='running'){
											Ext.Msg.alert('Warning','This job is still Running.');
											return;
										};
				        				Ext.MessageBox.confirm('Confirm','Wait a long time ?.', rerun); 	
								}
							}
						]
						
					}, {
						width : 70,
						align : 'center',
						text : "Status",
						xtype : 'actioncolumn',
						dataIndex : 'status',
						filter : {
							type : 'string',
							encode : true
						},
						items : [
						{				
							getClass : function(v, meta, rec) {
								var status = rec.get('status');
								if (status == 'done') {
									return 'see_result'
								} else if (status == 'error') {
									return 'btstate_low'
								} else {
									return 'waitsearch'
								}
							},
							getTip : function(v, meta, rec) {
								var status = rec.get('status');
								if (status == 'done') {
									return 'Click to view result'
								} else if (status == 'error') {
									return 'Error'
								} else {
									return 'Running'
								}
							},
							handler : function(grid, rowIndex, colIndex, record) {
								rec = grid.getStore().getAt(rowIndex);
								toolWinType = rec.get('ProGene')
								hasGrouped = 0
								var val = String(rec.get('csv_name'));
								var type = rec.get('ProGene')
								var desc = ''
								if (rec.get('description') != '-')
									desc = 'Comparison Search of ' + rec.get('description')
								else
									desc = 'Comparison Search of Comparison' + rec.get('csv_name')
								var timestamp = 'compare' + (new Date()).valueOf();
								
		
								
								CreateGrid = function(val, type, desc, temp_name,tstamp) {
									console.log(tstamp)
									var timestamp=tstamp
									var explist = String(rec.get('explist')) + ',';
									var firstExp = rec.get('exp_name').split('*')[0]
									function onStoreSizeChange() {
										grid.down('#status').update({
													count : store.getTotalCount()
												});
									};
									Ext.define('dynamicModel', {
												extend : 'Ext.data.Model',
												fields : []
											});
									var store = Ext.create('Ext.data.Store', {
												autoLoad : true,
												buffered : true,
												pageSize : 500,
												model : 'dynamicModel',
												leadingBufferZone : 1500,
												proxy : {
													type : 'ajax',
													method : 'POST',
													timeout : 3000000,
													url : '/gardener/newcmpprotein/',
													reader : {
														type : 'json',
														root : 'data',
														metaProperty : 'metaData',
														totalProperty : 'total'
													},
													extraParams : {
														id : val,
														temp_name : temp_name,
														gridType:type
													}
												},
												listeners : {
													totalcountchange : onStoreSizeChange,
													metachange : function(store, meta) {
													}
												}
											});
									var filters = {
										ftype : 'filtersAdvanced',
										encode : true
									}
									info_compare_tool_index = timestamp;
									
		//							var rerun = function(val){
		//									Ext.Ajax.request({
		//												timeout : 600000,
		//												url : '/gardener/newcmpprotein/',
		//												method : 'GET',
		//												params : {
		//													id : val,
		//													type:1,
		//													rerun:1
		//												},
		//												success : function(response) {}
		//											})
		//									var panel = Ext.getCmp('job_status');
		//									if (panel) {
		//										var main = Ext.getCmp("content-panel");
		//										main.setActiveTab(panel);
		//										panel.down('grid').getStore().load()
		//										return;
		//									}
		//									else{Ext.getCmp('btmessage').fireEvent('click');}
		//							
		//							};
									var createGrid = function(val) {
										// console.log(val)
										if (type != 'peptide') {
											grid = Ext.create('gar.view.MBRun', {
												store : store,
												forceFit : false,
												features : [filters],
												dockedItems : [{
															dock : 'top',
															xtype : 'toolbar',
															items : [{
																		text : 'Refreh this tab',
																		handler : function() {
																			store.load()
																		}
																	}, {
																		text : 'Clear Filter Data',
																		handler : function() {
																			grid.filters.clearFilters();
																		}
																	}, {
																		text : 'All Filter Data',
																		tooltip : 'Get Filter Data for Grid',
																		handler : function() {
																			var annoList = {
																				'co_1': 'Coreg',
																				'ki_1': 'Kinase', 
																				'li_1': 'Ligand', 
																				're_1': 'Receptor', 
																				'pmm_1':'Plasma Membrane(Mouse)', 
																				'pmh_1':'Plasma Membrane(Human)',
																				'tf_1': 'Transcription Factor'
																			}
																			var modiList = {
																				'Acetyl_1': 'N-terminal Acetyltrasferases',
																				'Methyl_1': 'Methylation',
																				'GlyGly_1': 'Ubiquitination',
																				'Biotin_1': 'Biotin',
																				'PhosphoST_1': 'Phosphorylation-ST',
																				'PhosphoY_1': 'Phosphorylation-Y'
																			}
																			var filterData = grid.filters.getFilterData()
																			var filtersStore = Ext.create('Ext.data.Store', {
																			    fields:['field', 'type', 'value'],
																			    data:[]
																			});
		
																			for( var i = 0; i < filterData.length; i++)
																			{
																				var field, type, value
																				field = filterData[i].field
																				switch(filterData[i].data.type)
																				{
																					case 'string':
																						type = 'has string'
																						value = filterData[i].data.value
																						filtersStore.add({ 'field': field, "type": type, "value": value })
																						break
																					case 'list':
																						type = 'has type'
																						for( var j = 0; j < filterData[i].data.value.length; j++)
																						{
																							value = filterData[i].data.value[j]
																							if(field == 'annotation')
																								filtersStore.add({ 'field': field, "type": type, "value": annoList[value] })
																							else if (field == 'modification')
																								filtersStore.add({ 'field': field, "type": type, "value": modiList[value] })
																						}
																						break
																					case 'numeric':
																						switch(filterData[i].data.comparison.slice(0,2))
																						{
																							case 'gt':
																								type = 'is bigger than'
																								break
																							case 'lt':
																								type = 'is little than'
																								break
																							case 'eq':
																								type = 'equals to'
																								break
																							default:
																								type = 'null'
																						}
																						value = filterData[i].data.value
																						filtersStore.add({ 'field': field, "type": type, "value": value })
																						break
																					default: 
																						type = 'null'
																				}
																			}
		
																			var filterWindow = Ext.create(Ext.window.Window,{
																				title: 'All filter data',
																				height: 300,
																				width: 500,
																				modal: true,
																				animateTarget: this,
																				layout: 'fit',
																				autoShow: true,
																				items: [{
																					xtype: 'grid',
																					hideHeaders: true,
																					columns: [
																				        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
																				        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
																				        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
																				    ],
																				    store: filtersStore
																				}]
																			})
																		}
																	}, 
//																	{
//																		xtype : 'button',
//																		tooltip : 'Significant Test',
//																		text : '',
//																		iconCls : 'mcttest',
//																		handler : function() {
//																			var column = []
//																			var change = function(Lostdata) {
//																				var ok = false
//																				for (var i = 0; i < Lostdata.length; i++) {
//																					if (Lostdata[i].columns)
//																						change(Lostdata[i].columns)
//																					if (Lostdata[i] && Lostdata[i].text) {
//																						var checkstring
//																						if (Lostdata[i].dataIndex && Lostdata[i].dataIndex.indexOf('VS') != -1) {
//																							ok = true
//																							column.push(Lostdata[i].dataIndex)
//																							checkstring = Lostdata[i].dataIndex
//																						}
//																						if (Lostdata[i].dataIndex && Lostdata[i].dataIndex.indexOf('_vs_') != -1) {
//																							Lostdata.splice(i, 1)
//																							i = i - 1
//																						}
//																					}
//																				}
//																				if (ok) {
//																					var z = new Object();
//																					z["dataIndex"] = checkstring.replace('VS', '_vs_')
//																					column.push(checkstring.replace('VS', '_vs_'))
//																					z["text"] = "P-value"
//																					z["sortable"] = true
//																					z["filter"] = {
//																						'type' : 'float',
//																						'encode' : true
//																					}
//																					z['renderer'] = function(value, metaData, record, row, col, store, gridView) {
//																						return value.toFixed(2)
//																					}
//																					Lostdata.push(z)
//																				}
//																				return
//																			}
//																			var changeit = function() {
//																				change(columndata)
//																				// console.log(columndata)
//																				// console.log(column)
//																				Ext.getCmp(timestamp).reconfigure(store, columndata)
//																				store.getProxy().extraParams['columns'] = column
//																				store.load()
//																				win.close()
//																			}
//																			var cmp_button = Ext.create('Ext.panel.Panel', {
//																						border : false,
//																						buttonAlign : "center",
//																						buttons : [{
//																									text : 'Start',
//																									handler : changeit
//																								}]
//																					});
//																			var win = new Ext.Window({
//																						title : 'Change Viewer',
//																						width : 320,
//																						resizable : false,
//																						items : [cmp_button]
//																					})
//																			win.show()
//																		}
//																	}, 
																	// {
																	// 	xtype : 'button',
																	// 	tooltip : 'Download Data',
																	// 	text : '',
																	// 	iconCls : 'imfileup',
																	// 	handler : function() {
																	// 		data = Ext.getCmp(timestamp).filters.getFilterData()
																	// 		var s = '&filter=[';
																	// 		for (i = 0; i < data.length; i++) {
																	// 			s += '{'
																	// 			temp = String(Ext.encode(data[i].data))
																	// 			s += temp.substr(1, temp.length - 2)
																	// 			s += ',"field":"'
																	// 			s += String(data[i].field)
																	// 			s += '"}'
																	// 			if (i != data.length - 1)
																	// 				s += ','
																	// 		}
																	// 		s += ']'
																	// 		var column = ''
																	// 		var setColumnString = function(Lastdata) {
																	// 			var ok = false
																	// 			for (var i = 0; i < Lastdata.length; i++) {
																	// 				if (Lastdata[i].columns)
																	// 					setColumnString(Lastdata[i].columns)
																	// 				else
																	// 				{
																	// 					column += (Lastdata[i].dataIndex)
																	// 					column += '^'
																	// 				}
																	// 			}
																	// 			column.substring(0,column.length - 1)
																	// 			return
																	// 		}
																	// 		setColumnString(columndata)
																	// 		column = encodeURIComponent(column)
																	// 		url = '/gardener/newcmpprotein/?download=yes&gridType='+type+'&id=' + val + s + '&columns=' + column + '&statistical=' + Ext.getCmp(timestamp).getStore().proxy.extraParams.statistical
																	// 		window.open(url);
																	// 	}
																	// }, 
																	{
																		xtype : 'button',
																		text : 'Tools',
																		id : 'tools' + val,
																		listeners : {
																			click : function() {
																				if (!Ext.getCmp('toolsPanel')) {
																					view = Ext.widget('tools', {
																								val : val,
																								temp_name:temp_name,
																								gridType:type,
																								proGene : type//rec.get('ProGene')
																							});
																					info_compare_tool_index = timestamp;
																				} else {
																					alert('Only one tools-panel can be open at once.')
																				}
																			}
																		}
																	}, '->', {
																		xtype : 'component',
																		itemId : 'status',
																		tpl : 'Matching Proteins: {count}'
																	}]
														}],
												id : timestamp,
												plugins : [
												Ext.create('Ext.grid.plugin.CellEditing', {
													clicksToEdit : 1,
													listeners : {
														edit : function(editor, e) {
															// commit the changes right after editing finished
															// console.log(e)
															symbol = grid.getStore().getAt(e.rowIdx).get('Symbol')
															Ext.Ajax.request({
																timeout : 600000,
																url : '/gardener/userAnnotation/',
																method : 'POST',
																params : {
																	type : 'Protein',
																	items : symbol,
																	annotation : e.value,
																	exp: firstExp
																}
															});
														}
													}
												}),{
													ptype : 'rowexpander',
													selectRowOnExpand : true,
													expandOnDblClick : true,
													// rowBodyTpl : ['<div id="compare-Peptide-{id}"></div>'],
													rowBodyTpl : ['<div id="compare-Peptide-{id}-' + timestamp + '"></div>'],
													toggleRow : function(rowIdx, record) {
														var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row).down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view.getRecord(rowNode), grid = this
																.getCmp(), id = record.get('id'), targetId = 'compare-Peptide-' + id + '-' + timestamp, peptide = record.get('peptide');
														// console.log(rowNode)
														// console.log(Ext.getCmp(timestamp).columnManager)
														if (row.hasCls(this.rowCollapsedCls)) {
															row.removeCls(this.rowCollapsedCls);
															this.recordsExpanded[record.internalId] = true;
															this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
															if (rowNode.grid) {
																nextBd.removeCls(hiddenCls);
																rowNode.grid.doComponentLayout();
															} else {
																// var timestamp = 'compare_peptide' + (new
																// Date()).valueOf();
																// console.log(timestamp)
																columns = ''
																ddidx = ''
																tempcol = Ext.getCmp(timestamp).columnManager.columns
																// console.log(tempcol)
																for (i = 0; i < tempcol.length; i++) {
																	columns = columns + tempcol[i].text + ';'
																	ddidx = ddidx + tempcol[i].dataIndex + ';'
																}
																// console.log(columns)
																// console.log(ddidx)
																// console.log()
																Ext.create('Ext.data.Store', {
																			pageSize : 1000,
																			autoLoad : true,
																			proxy : {
																				type : 'ajax',
																				url : '/gardener/newcmp_peptide/',
																				extraParams : {
																					Xid : val,
																					peptide : peptide,
																					columndata : columns,
																					dataidx : ddidx
																				},
																				reader : {
																					type : 'json',
																					root : 'data',
																					metaProperty : 'metaData',
																					totalProperty : 'total'
																				}
																			},
																			listeners : {
																				metachange : function(store, meta) {
																					nextBd.removeCls(hiddenCls);
																					// console.log(targetId)
																					// console.log(row)
																					var rowgrid = Ext.create('gar.view.MBRunPeptide', {
																								height : 200,
																								renderTo : targetId,
																								store : this,
																								row : row
																							});
																					rowNode.grid = grid;
																					var columndata = meta.columns;
																					var tooltips = [];
																					for (i = 0; i < columndata.length; i++) {
																						if (String(columndata[i].text).indexOf("Area") != -1) {
																							columndata[i].renderer = function(value, metaData, record, row, col, store, gridView) {
																								var column = gridView.getHeaderAtIndex(col);
																								var examstring = column.dataIndex;
																								var kk = examstring.split('_')
																								kk[kk.length - 1] = 'mz'
																								var mz = kk.join('_')
																								kk[kk.length - 1] = 'rt'
																								var rt = kk.join('_')
																								metaData.tdAttr = "data-qtip='Mz: " + record.data[mz] + '<br\>RT: ' + record.data[rt] + "'";
																								return value.toExponential(2);
																							}
																						}
																						if (String(columndata[i].text).indexOf("Ratio") != -1) {
																							columndata[i].renderer = function(value, metaData, record, row, col, store, gridView) {
																								// console.log(value)
																								if (value > 1) {
																									p = parseInt(1 / ans * 255);
																									k = ("00" + p.toString(16)).substr(p.toString(16).length)
																									s = "#ff" + k + k
																									return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + value.toFixed(2) + '</div>'
																								} else if (value < 1) {
																									p = parseInt(ans * 255);
																									k = ("00" + p.toString(16)).substr(p.toString(16).length)
																									s = "#" + k + "ff" + k
																									return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + value.toFixed(2) + '</div>'
																								} else
																									return 1
																							}
																						}
																					}
																					rowgrid.reconfigure(store, columndata)
																					// grid.suspendEvents();
																				}
																			}
																		});
															}
														} else {
															row.addCls(this.rowCollapsedCls);
															nextBd.addCls(this.rowBodyHiddenCls);
															this.recordsExpanded[record.internalId] = false;
															this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
														}
													}
												}]
											});
										}
										/* ---- peptide grid start from here---- */
										else {
											var peptide_sum_plot = function(dbcell, td, cell, record, tr, row, e) {
												gridHeader = dbcell.getGridColumns()
												console.log(record)
												var clickTitle = gridHeader[cell]
												console.log(clickTitle)
												if (clickTitle.text == 'PSM') {
													var waitWin = new Ext.Window({
																draggable : {
																	constrain : true,
																	constrainTo : Ext.getBody()
																},
																title : 'Waiting for a while',
																height : 100,
																width : 250
															})
													waitWin.show()
													cellrecord = record
													var peptide_plot_store = Ext.create('gar.store.PeptidePlot');
													peptide_plot_store.load({
																params : {
																	exp_id : clickTitle.dataIndex.replace('_psms', ''),
																	pep_sequence : record.data.Sequence,
																	modification : record.data.Modification
																}
															});
													// Ext.Msg.alert('Experiment
													// Info:'+xlabel.length,
													// ylabel.length);
													// Ext.Msg.alert('Experiment
													// Info:'+xlabel,
													// ylabel);
													var rank_store = Ext.create('gar.store.TicRank');
													rank_store.load({
																params : {
																	exp_id : clickTitle.dataIndex.replace('_psms', '')
																}
															});
													var pieChart = Ext.create('Ext.chart.Chart', {
																width : 200,
																height : 100,
																xtype : 'chart',
																style : 'background:#fff',
																animate : true,
																store : peptide_plot_store,
																shadow : true,
																theme : 'Category1',
																legend : {
																	position : 'right'
																},
																axes : [{
																			type : 'Numeric',
																			minimum : 0,
																			position : 'left',
																			fields : ['fraction_id'],
																			minorTickSteps : 1,
																			grid : {
																				odd : {
																					opacity : 1,
																					fill : '#ddd',
																					stroke : '#bbb',
																					'stroke-width' : 0.5
																				}
																			}
																		}],
																series : [{
																			type : 'line',
																			highlight : {
																				size : 7,
																				radius : 7
																			},
																			axis : 'left',
																			xField : 'fraction_id',
																			yField : 'repeat_id',
																			markerConfig : {
																				type : 'cross',
																				size : 4,
																				radius : 4,
																				'stroke-width' : 0
																			}
																		}]
															});
													var grid = Ext.create('Ext.grid.Panel', {
																store : peptide_plot_store,
																height : 130,
																width : 280,
																columns : [{
																			text : 'xplot',
																			dataIndex : 'xplot'
																		}, {
																			text : 'yplot',
																			dataIndex : 'yplot'
																		}]
															});
													var Renderers = {};
													(function() {
														var ColorManager = {
															rgbToHsv : function(rgb) {
																var r = rgb[0] / 255, g = rgb[1] / 255, b = rgb[2] / 255, rd = Math.round, minVal = Math.min(r, g, b), maxVal = Math.max(r, g, b), delta = maxVal - minVal, h = 0, s = 0, v = 0, deltaRgb;
																v = maxVal;
																if (delta == 0) {
																	return [0, 0, v];
																} else {
																	s = delta / maxVal;
																	deltaRgb = {
																		r : (((maxVal - r) / 6) + (delta / 2)) / delta,
																		g : (((maxVal - g) / 6) + (delta / 2)) / delta,
																		b : (((maxVal - b) / 6) + (delta / 2)) / delta
																	};
																	if (r == maxVal) {
																		h = deltaRgb.b - deltaRgb.g;
																	} else if (g == maxVal) {
																		h = (1 / 3) + deltaRgb.r - deltaRgb.b;
																	} else if (b == maxVal) {
																		h = (2 / 3) + deltaRgb.g - deltaRgb.r;
																	}
																	// handle
																	// edge
																	// cases
																	// for
																	// hue
																	if (h < 0) {
																		h += 1;
																	}
																	if (h > 1) {
																		h -= 1;
																	}
																}
																h = rd(h * 360);
																s = rd(s * 100);
																v = rd(v * 100);
																return [h, s, v];
															},
															hsvToRgb : function(hsv) {
																var h = hsv[0] / 360, s = hsv[1] / 100, v = hsv[2] / 100, r, g, b, rd = Math.round;
																if (s == 0) {
																	v *= 255;
																	return [v, v, v];
																} else {
																	var vh = h * 6, vi = vh >> 0, v1 = v * (1 - s), v2 = v * (1 - s * (vh - vi)), v3 = v * (1 - s * (1 - (vh - vi)));
																	switch (vi) {
																		case 0 :
																			r = v;
																			g = v3;
																			b = v1;
																			break;
																		case 1 :
																			r = v2;
																			g = v;
																			b = v1;
																			break;
																		case 2 :
																			r = v1;
																			g = v;
																			b = v3;
																			break;
																		case 3 :
																			r = v1;
																			g = v2;
																			b = v;
																			break;
																		case 4 :
																			r = v3;
																			g = v1;
																			b = v;
																			break;
																		default :
																			r = v;
																			g = v1;
																			b = v2;
																	}
																	return [rd(r * 255), rd(g * 255), rd(b * 255)];
																}
															}
														};
														// Generic
														// number
														// interpolator
														var delta = function(x, y, a, b, theta) {
															return a + (b - a) * (y - theta) / (y - x);
														};
														// Add
														// renderer
														// methods.
														Ext.apply(Renderers, {
																	color : function(fieldName, minColor, maxColor, minValue, maxValue) {
																		var re = /rgb\s*\(\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*\)\s*/, minColorMatch = minColor.match(re), maxColorMatch = maxColor.match(re), interpolate = function(theta) {
																			return [delta(minValue, maxValue, minColor[0], maxColor[0], theta), delta(minValue, maxValue, minColor[1], maxColor[1], theta),
																					delta(minValue, maxValue, minColor[2], maxColor[2], theta)];
																		};
																		minColor = ColorManager.rgbToHsv([+minColorMatch[1], +minColorMatch[2], +minColorMatch[3]]);
																		maxColor = ColorManager.rgbToHsv([+maxColorMatch[1], +maxColorMatch[2], +maxColorMatch[3]]);
																		// Return
																		// the
																		// renderer
																		return function(sprite, record, attr, index, store) {
																			var value = +record.get(fieldName), rgb = ColorManager.hsvToRgb(interpolate(value)), rgbString = 'rgb(' + rgb[0] + ', ' + rgb[1] + ', ' + rgb[2] + ')';
																			return Ext.apply(attr, {
																						fill : rgbString
																					});
																		};
																	},
																	grayscale : function(fieldName, minColor, maxColor, minValue, maxValue) {
																		var re = /rgb\s*\(\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*\)\s*/, minColorMatch = minColor.match(re), maxColorMatch = maxColor.match(re), interpolate = function(theta) {
																			var ans = delta(minValue, maxValue, +minColorMatch[1], +maxColorMatch[1], theta) >> 0;
																			return [ans, ans, ans];
																		};
																		// Return
																		// the
																		// renderer
																		return function(sprite, record, attr, index, store) {
																			var value = +record.get(fieldName), rgb = interpolate(value), rgbString = 'rgb(' + rgb[0] + ', ' + rgb[1] + ', ' + rgb[2] + ')';
																			return Ext.apply(attr, {
																						fill : rgbString,
																						strokeFill : 'rgb(0, 0, 0)'
																					});
																		};
																	},
																	radius : function(fieldName, minRadius, maxRadius, minValue, maxValue) {
																		var interpolate = function(theta) {
																			return delta(minValue, maxValue, minRadius, maxRadius, theta);
																		};
																		// Return
																		// the
																		// renderer
																		return function(sprite, record, attr, index, store) {
																			var value = +record.get(fieldName), radius = interpolate(value);
																			return Ext.apply(attr, {
																						radius : radius,
																						size : radius
																					});
																		};
																	}
																});
													})();
													// current
													// renderer
													// configuration
													var rendererConfiguration = {
														xField : 'xplot',
														yField : 'yplot',
														color : false,
														colorFrom : 'rgb(250, 20, 20)',
														colorTo : 'rgb(127, 0, 240)',
														scale : false,
														scaleFrom : 'rgb(20, 20, 20)',
														scaleTo : 'rgb(220, 220, 220)',
														radius : false,
														radiusSize : 50
													};
													// update
													// the
													// visualization
													// with
													// the
													// new
													// renderer
													// configuration
													function refresh() {
														var chart = Ext.getCmp('chartCmp'), series = chart.series.items, len = series.length, rc = rendererConfiguration, color, grayscale, radius, s;
														for (var i = 0; i < len; i++) {
															s = series[i];
															s.xField = rc.xField;
															s.yField = rc.yField;
															color = rc.color ? Renderers.color(rc.color, rc.colorFrom, rc.colorTo, 0, 1) : function(a, b, attr) {
																return attr;
															};
															grayscale = rc.grayscale ? Renderers.grayscale(rc.grayscale, rc.scaleFrom, rc.scaleTo, 0, 1) : function(a, b, attr) {
																return attr;
															};
															radius = rc.radius ? Renderers.radius(rc.radius, 10, rc.radiusSize, 0, 1) : function(a, b, attr) {
																return attr;
															};
															s.renderer = function(sprite, record, attr, index, store) {
																return radius(sprite, record, grayscale(sprite, record, color(sprite, record, attr, index, store), index, store), index, store);
															};
														}
														chart.redraw();
													}
													// form
													// selection
													// callbacks/handlers.
													var xAxisHandler = function(elem) {
														var xField = elem.text;
														rendererConfiguration.xField = xField;
														refresh();
													};
													var yAxisHandler = function(elem) {
														var yField = elem.text;
														rendererConfiguration.yField = yField;
														refresh();
													};
													var colorVariableHandler = function(elem) {
														var color = elem.text;
														rendererConfiguration.color = color;
														rendererConfiguration.grayscale = false;
														refresh();
													};
													var grayscaleVariableHandler = function(elem) {
														var color = elem.text;
														rendererConfiguration.grayscale = color;
														rendererConfiguration.color = false;
														refresh();
													};
													var scaleFromHandler = function(elem) {
														var from = elem.text;
														rendererConfiguration.scaleFrom = from;
														refresh();
													};
													var scaleToHandler = function(elem) {
														var to = elem.text;
														rendererConfiguration.scaleTo = to;
														refresh();
													};
													var colorFromHandler = function(elem) {
														var from = elem.text;
														rendererConfiguration.colorFrom = from;
														refresh();
													};
													var colorToHandler = function(elem) {
														var to = elem.text;
														rendererConfiguration.colorTo = to;
														refresh();
													};
													var radiusHandler = function(elem) {
														var radius = elem.text;
														rendererConfiguration.radius = radius;
														refresh();
													};
													var radiusSizeHandler = function(elem) {
														var radius = elem.text;
														rendererConfiguration.radiusSize = parseInt(radius, 10);
														refresh();
													};
													var xAxisMenu = Ext.create('Ext.menu.Menu', {
																id : 'xAxisMenu',
																items : [{
																			text : 'xplot',
																			handler : xAxisHandler,
																			checked : true,
																			group : 'x'
																		}, {
																			text : 'yplot',
																			handler : xAxisHandler,
																			checked : false,
																			group : 'x'
																		}, {
																			text : 'area',
																			handler : xAxisHandler,
																			checked : false,
																			group : 'x'
																		}]
															});
													var yAxisMenu = Ext.create('Ext.menu.Menu', {
																id : 'yAxisMenu',
																items : [{
																			text : 'xplot',
																			handler : yAxisHandler,
																			checked : false,
																			group : 'y'
																		}, {
																			text : 'yplot',
																			handler : yAxisHandler,
																			checked : true,
																			group : 'y'
																		}, {
																			text : 'area',
																			handler : yAxisHandler,
																			checked : false,
																			group : 'y'
																		}]
															});
													var colorMenu = Ext.create('Ext.menu.Menu', {
																id : 'colorMenu',
																items : [{
																			text : 'xplot',
																			handler : colorVariableHandler,
																			checked : true,
																			group : 'color'
																		}, {
																			text : 'yplot',
																			handler : colorVariableHandler,
																			checked : false,
																			group : 'color'
																		}, {
																			text : 'area',
																			handler : colorVariableHandler,
																			checked : false,
																			group : 'color'
																		}, {
																			text : 'Color From',
																			menu : {
																				items : [{
																							text : 'rgb(250, 20, 20)',
																							handler : colorToHandler,
																							checked : true,
																							group : 'colorrange'
																						}, {
																							text : 'rgb(20, 250, 20)',
																							handler : colorToHandler,
																							checked : false,
																							group : 'colorrange'
																						}, {
																							text : 'rgb(20, 20, 250)',
																							handler : colorToHandler,
																							checked : false,
																							group : 'colorrange'
																						}, {
																							text : 'rgb(127, 0, 240)',
																							handler : colorFromHandler,
																							checked : false,
																							group : 'colorrange'
																						}, {
																							text : 'rgb(213, 70, 121)',
																							handler : colorToHandler,
																							checked : false,
																							group : 'colorrange'
																						}, {
																							text : 'rgb(44, 153, 201)',
																							handler : colorFromHandler,
																							checked : false,
																							group : 'colorrange'
																						}, {
																							text : 'rgb(146, 6, 157)',
																							handler : colorFromHandler,
																							checked : false,
																							group : 'colorrange'
																						}, {
																							text : 'rgb(49, 149, 0)',
																							handler : colorFromHandler,
																							checked : false,
																							group : 'colorrange'
																						}, {
																							text : 'rgb(249, 153, 0)',
																							handler : colorFromHandler,
																							checked : false,
																							group : 'colorrange'
																						}]
																			}
																		}, {
																			text : 'Color To',
																			menu : {
																				items : [{
																							text : 'rgb(250, 20, 20)',
																							handler : colorToHandler,
																							checked : false,
																							group : 'tocolorrange'
																						}, {
																							text : 'rgb(20, 250, 20)',
																							handler : colorToHandler,
																							checked : false,
																							group : 'tocolorrange'
																						}, {
																							text : 'rgb(20, 20, 250)',
																							handler : colorToHandler,
																							checked : false,
																							group : 'tocolorrange'
																						}, {
																							text : 'rgb(127, 0, 220)',
																							handler : colorFromHandler,
																							checked : true,
																							group : 'tocolorrange'
																						}, {
																							text : 'rgb(213, 70, 121)',
																							handler : colorToHandler,
																							checked : false,
																							group : 'tocolorrange'
																						}, {
																							text : 'rgb(44, 153, 201)',
																							handler : colorToHandler,
																							checked : false,
																							group : 'tocolorrange'
																						}, {
																							text : 'rgb(146, 6, 157)',
																							handler : colorToHandler,
																							checked : false,
																							group : 'tocolorrange'
																						}, {
																							text : 'rgb(49, 149, 0)',
																							handler : colorToHandler,
																							checked : false,
																							group : 'tocolorrange'
																						}, {
																							text : 'rgb(249, 153, 0)',
																							handler : colorToHandler,
																							checked : false,
																							group : 'tocolorrange'
																						}]
																			}
																		}]
															});
													var grayscaleMenu = Ext.create('Ext.menu.Menu', {
																id : 'grayscaleMenu',
																items : [{
																			text : 'xplot',
																			handler : grayscaleVariableHandler,
																			checked : false,
																			group : 'gs'
																		}, {
																			text : 'yplot',
																			handler : grayscaleVariableHandler,
																			checked : false,
																			group : 'gs'
																		}, {
																			text : 'area',
																			handler : grayscaleVariableHandler,
																			checked : false,
																			group : 'gs'
																		}, {
																			text : 'Scale From',
																			menu : {
																				items : [{
																							text : 'rgb(20, 20, 20)',
																							handler : scaleFromHandler,
																							checked : true,
																							group : 'gsrange'
																						}, {
																							text : 'rgb(80, 80, 80)',
																							handler : scaleFromHandler,
																							checked : false,
																							group : 'gsrange'
																						}, {
																							text : 'rgb(120, 120, 120)',
																							handler : scaleFromHandler,
																							checked : false,
																							group : 'gsrange'
																						}, {
																							text : 'rgb(180, 180, 180)',
																							handler : scaleFromHandler,
																							checked : false,
																							group : 'gsrange'
																						}, {
																							text : 'rgb(220, 220, 220)',
																							handler : scaleFromHandler,
																							checked : false,
																							group : 'gsrange'
																						}, {
																							text : 'rgb(250, 250, 250)',
																							handler : scaleFromHandler,
																							checked : false,
																							group : 'gsrange'
																						}]
																			}
																		}, {
																			text : 'Scale To',
																			menu : {
																				items : [{
																							text : 'rgb(20, 20, 20)',
																							handler : scaleToHandler,
																							checked : false,
																							group : 'togsrange'
																						}, {
																							text : 'rgb(80, 80, 80)',
																							handler : scaleToHandler,
																							checked : false,
																							group : 'togsrange'
																						}, {
																							text : 'rgb(120, 120, 120)',
																							handler : scaleToHandler,
																							checked : false,
																							group : 'togsrange'
																						}, {
																							text : 'rgb(180, 180, 180)',
																							handler : scaleToHandler,
																							checked : false,
																							group : 'togsrange'
																						}, {
																							text : 'rgb(220, 220, 220)',
																							handler : scaleToHandler,
																							checked : true,
																							group : 'togsrange'
																						}, {
																							text : 'rgb(250, 250, 250)',
																							handler : scaleToHandler,
																							checked : false,
																							group : 'togsrange'
																						}]
																			}
																		}]
															});
													var radiusMenu = Ext.create('Ext.menu.Menu', {
																id : 'radiusMenu',
																style : {
																	overflow : 'visible' // For
																	// the
																	// Combo
																	// popup
																},
																items : [{
																			text : 'xplot',
																			handler : radiusHandler,
																			checked : true,
																			group : 'radius'
																		}, {
																			text : 'yplot',
																			handler : radiusHandler,
																			checked : false,
																			group : 'radius'
																		}, {
																			text : 'area',
																			handler : radiusHandler,
																			checked : false,
																			group : 'radius'
																		}, {
																			text : 'Max Radius',
																			menu : {
																				items : [{
																							text : '20',
																							handler : radiusSizeHandler,
																							checked : false,
																							group : 'sradius'
																						}, {
																							text : '30',
																							handler : radiusSizeHandler,
																							checked : false,
																							group : 'sradius'
																						}, {
																							text : '40',
																							handler : radiusSizeHandler,
																							checked : false,
																							group : 'sradius'
																						}, {
																							text : '50',
																							handler : radiusSizeHandler,
																							checked : true,
																							group : 'sradius'
																						}, {
																							text : '60',
																							handler : radiusSizeHandler,
																							checked : false,
																							group : 'sradius'
																						}]
																			}
																		}]
															});
													peptide_plot_store.on('load', function() {
														var xlabel = peptide_plot_store.getxlabel();
														var ylabel = peptide_plot_store.getylabel();
														lxlabel = (xlabel.length === 1) ? 0 : xlabel.length
														lylabel = (ylabel.length === 1) ? 0 : ylabel.length
														var chart = Ext.create('Ext.chart.Chart', {
															id : 'chartCmp',
															xtype : 'chart',
															style : 'background:#fff',
															animate : true,
															store : peptide_plot_store,
															insetPadding : 50,
															shadow : true,
															axes : [{
																		type : 'Numeric',
																		minimum : 0,
																		position : 'left',
																		fields : ['yplot'],
																		label : {
																			renderer : function(v) {
																				if (v == 0) {
																					return ''
																				} else {
																					return 'Fraction:' + ylabel[parseInt(v - 1)]
																				}
																			}
																		},
																		title : 'MS1 intensity',
																		minorTickSteps : 0.1,
																		majorTickSteps : lylabel,
																		grid : {
																			odd : {
																				opacity : 0.15,
																				fill : '#d93a49',
																				stroke : '#ef5b9c',
																				'stroke-width' : 0
																			}
																		}
																	}, {
																		type : 'Numeric',
																		position : 'bottom',
																		fields : ['xplot'],
																		label : {
																			renderer : function(v) {
																				if (v == 0) {
																					return ''
																				} else {
																					return 'Repeat:' + xlabel[parseInt(v - 1)]
																				}
																			}
																		},
																		title : 'Retention Time',
																		type : 'Numeric',
																		minorTickSteps : 0.1,
																		majorTickSteps : lxlabel,
																		grid : {
																			odd : {
																				opacity : 0.15,
																				fill : '#444693',
																				stroke : '#6a6da9',
																				'stroke-width' : 0
																			}
																		}
																	}],
															series : [{
																type : 'scatter',
																axis : false,
																xField : 'xplot',
																yField : 'yplot',
																color : '#bed742',
																markerConfig : {
																	type : 'circle',
																	radius : 8,
																	size : 5
																},
																tips : {
																	trackMouse : true,
																	width : 580,
																	height : 170,
																	layout : 'fit',
																	items : {
																		xtype : 'container',
																		layout : 'hbox',
																		items : [pieChart, grid]
																	},
																	renderer : function(klass, item) {
																		var storeItem = item.storeItem;
																		this
																				.setTitle('Repeat' + storeItem.get('repeat_id') + '_Fraction_' + storeItem.get('fraction_id') + '( RT:' + storeItem.get('rt') + ', Intensity:' + storeItem.get('intensity') + ', Area:' + storeItem
																						.get('area') + ")");
																		grid.setSize(480, 130);
																	}
																},
																listeners : {
																	itemmousedown : function(obj) {
																		var win = Ext.create('Ext.Window', {
																			width : 1200,
																			// height
																			// :
																			// 735,
																			height : 600,
																			minHeight : 400,
																			minWidth : 550,
																			hidden : true,
																			maximizable : true,
																			title : 'MS Viewer',
																			// renderTo
																			// :
																			// Ext.getBody(),
																			layout : 'fit',
																			html : '<iframe name="spview" id="spview" width="100%" height="100%" frameborder=0 src=/gardener/peptide_viwer?sequence=' + obj.storeItem.data['sequence'] + '&charge=' + obj.storeItem.data['charge'] + '&pre_mz=' + obj.storeItem.data['pre_mz'] + '&search_id=' + obj.storeItem.data['search_id'] + '&ms1_scan=' + obj.storeItem.data['ms1_scan'] + '&ms2_scan=' + obj.storeItem.data['ms2_scan'] + '&rt=' + obj.storeItem.data['rt'] + '&ms1_rt=' + obj.storeItem.data['ms1_rt'] + '&filename=' + obj.storeItem.data['filename'] + '&id=' + obj.storeItem.data['id'] + '></iframe>'
																		});
																		// win.getEl().setStyle('z-index',
																		// '80000');
																		win.show();
																		// alert(obj.storeItem.data['ms2_scan']
																		// + '
																		// &' +
																		// obj.storeItem.data['ms1_scan']);
																	}
																}
															}]
														});
														var win = Ext.create('Ext.Window', {
																	draggable : {
																		constrain : true,
																		constrainTo : Ext.getBody()
																	},
																	width : 900,
																	height : 500,
																	minHeight : 100,
																	minWidth : 100,
																	hidden : true,
																	maximizable : true,
																	title : 'Peptide Quantification Plot',
																	// renderTo
																	// :
																	// Ext.getBody(),
																	layout : 'fit',
																	tbar : [{
																				text : 'Save Chart',
																				handler : function() {
																					Ext.MessageBox.confirm('Confirm Download', 'Would you like to download the chart as an image?', function(choice) {
																								if (choice == 'yes') {
																									chart.save({
																												type : 'image/png'
																											});
																								}
																							});
																				}
																			}, {
																				text : 'Select Color',
																				menu : colorMenu
																			}, {
																				text : 'Select Grayscale',
																				menu : grayscaleMenu
																			}],
																	items : chart
																});
														// win.getEl().setStyle('z-index',
														// '80000');
														win.show();
														waitWin.close()
														// Ext.Msg.alert('Experiment
														// Info:'+xlabel,
														// ylabel);
														refresh();
													});
												}
											}
											grid = Ext.create('gar.view.MBRun', {
														store : store,
														features : [filters],
														listeners : {
															cellclick : peptide_sum_plot
														},
														dockedItems : [{
																	dock : 'top',
																	xtype : 'toolbar',
																	items : [{
																				text : 'Refreh this tab',
																				handler : function() {
																					store.load()
																				}
																			}, {
																				text : 'Clear Filter Data',
																				handler : function() {
																					grid.filters.clearFilters();
																				}
																			}, {
																				text : 'All Filter Data',
																				tooltip : 'Get Filter Data for Grid',
																				handler : function() {
																					var filterData = grid.filters.getFilterData()
																					var filtersStore = Ext.create('Ext.data.Store', {
																					    fields:['field', 'type', 'value'],
																					    data:[]
																					});
				
																					for( var i = 0; i < filterData.length; i++)
																					{
																						var field, type, value
																						field = filterData[i].field
																						switch(filterData[i].data.type)
																						{
																							case 'string':
																								type = 'has string'
																								value = filterData[i].data.value
																								filtersStore.add({ 'field': field, "type": type, "value": value })
																								break
																							case 'numeric':
																								switch(filterData[i].data.comparison.slice(0,2))
																								{
																									case 'gt':
																										type = 'is bigger than'
																										break
																									case 'lt':
																										type = 'is little than'
																										break
																									case 'eq':
																										type = 'equals to'
																										break
																									default:
																										type = 'null'
																								}
																								value = filterData[i].data.value
																								filtersStore.add({ 'field': field, "type": type, "value": value })
																								break
																							default: 
																								type = 'null'
																						}
																					}
				
																					var filterWindow = Ext.create(Ext.window.Window,{
																						title: 'All filter data',
																						height: 300,
																						width: 500,
																						modal: true,
																						animateTarget: this,
																						layout: 'fit',
																						autoShow: true,
																						items: [{
																							xtype: 'grid',
																							hideHeaders: true,
																							columns: [
																						        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
																						        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
																						        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
																						    ],
																						    store: filtersStore
																						}]
																					})
																				}
																			}, {
																				text : 'Peptide To Protein',
																				// tooltip : 'Get Filter Data for Grid',
																				handler : function() {
																					var loadMask = new Ext.LoadMask(grid, {
																						msg : 'Loading.....'
																					});
																					var targetGridType = 'protein';
																					//var data = Ext.encode(grid.filters.getFilterData());
																					//Ext.Msg.alert('All Filter Data', data);
																					temp_filter = grid.filters.buildQuery(grid.filters.getFilterData());
																					loadMask.show();
																					Ext.Ajax.request({
																								timeout : 600000,
																								url : '/gardener/newcmpprotein/',
																								method : 'GET',
																								params : {
																									id : val,
																									// levels : out,
																									filter : temp_filter,
																									R_type : 'P2P',
																									gridType:'peptide',
																									targetGridType:targetGridType
																									// statistical : statis,
																									// tryNomalize : tryNomalize
																								},
																								success : function(response) {
																									loadMask.hide();
																									var json = Ext.JSON.decode(response.responseText);
																									var timestamp = 'compare' + (new Date()).valueOf();
																									//console.log(json)
																									temp_name = json.temp_name
																									CreateGrid(val, targetGridType, desc + '*', temp_name,timestamp)
																								},
																								failure : function() {
																									loadMask.hide();
																								}
																							});
																				}
																			 }, 
																			 // {
																				// 	xtype : 'button',
																				// 	tooltip : 'Download Data',
																				// 	text : '',
																				// 	iconCls : 'imfileup',
																				// 	handler : function() {
																				// 		data = Ext.getCmp(timestamp).filters.getFilterData()
																				// 		var s = '&filter=[';
																				// 		for (i = 0; i < data.length; i++) {
																				// 			s += '{'
																				// 			temp = String(Ext.encode(data[i].data))
																				// 			s += temp.substr(1, temp.length - 2)
																				// 			s += ',"field":"'
																				// 			s += String(data[i].field)
																				// 			s += '"}'
																				// 			if (i != data.length - 1)
																				// 				s += ','
																				// 		}
																				// 		s += ']'
																				// 		var column = ''
																				// 		var setColumnString = function(Lastdata) {
																				// 			var ok = false
																				// 			for (var i = 0; i < Lastdata.length; i++) {
																				// 				if (Lastdata[i].columns)
																				// 					setColumnString(Lastdata[i].columns)
																				// 				else
																				// 				{
																				// 					column += (Lastdata[i].dataIndex)
																				// 					column += '^'
																				// 				}
																				// 			}
																				// 			column.substring(0,column.length - 1)
																				// 			return
																				// 		}
																				// 		setColumnString(columndata)
																				// 		column = encodeURIComponent(column)
																				// 		url = '/gardener/newcmpprotein/?download=yes&gridType='+type+'&id=' + val + s + '&columns=' + column + '&statistical=' + Ext.getCmp(timestamp).getStore().proxy.extraParams.statistical
																				// 		window.open(url);
																				// 	}
																				// },
																				{
																				xtype : 'button',
																				text : 'Tools',
																				id : 'tools' + val,
																				listeners : {
																					click : function() {
																						if (!Ext.getCmp('toolsPanel')) {
																							view = Ext.widget('tools', {
																								val : val,
																								temp_name:temp_name,
																								gridType:type,
																								proGene : type//rec.get('ProGene')
																									});
																							info_compare_tool_index = timestamp;
																						} else {
																							alert('Only one tools-panel can be open at once.')
																						}
																					}
																				}
																			}, '->', {
																				xtype : 'component',
																				itemId : 'status',
																				tpl : 'Matching Peptides: {count}'
																			}]
																}],
														id : timestamp
													});
										}
										/* ---- peptide grid end here ---- */
									}
									Ext.Ajax.request({
												url : '/gardener/com_getheaders/',
												params : {
													id : val,
													//explist : explist,
													gridType:type
												},
												timeout:600000,
												method : 'GET',
												success : function(response) {
													var json = Ext.JSON.decode(response.responseText);
													var oldcolumndata = json.columns
													var columndata = oldcolumndata
													for (i = 0; i < columndata.length; i++) {
														if (columndata[i].text == 'Symbol') {
															columndata[i].renderer = function(value) {
																return Ext.String.format('<a href="http://www.ncbi.nlm.nih.gov/gene/?term={0}"  target="_blank">{0}</a>', value);
															}
														}
														if (columndata[i].text == 'Annotation') {
															var anno_list = [['co_1', 'Coreg'], ['ki_1', 'Kinase'], ['li_1', 'Ligand'], ['re_1', 'Receptor'], ['pmm_1', 'Plasma Membrane(Mouse)'], ['pmh_1', 'Plasma Membrane(Human)'],
																	['tf_1', 'Transcription Factor']]
															var optionsStore = new Ext.data.Store({
																		fields : ['id', 'text'],
																		proxy : {
																			data : anno_list,
																			type : 'memory',
																			reader : {
																				type : 'array'
																			}
																		}
																	})
															// columndata[i].xtype = 'actioncolumn';
															columndata[i].dataIndex = 'annotation'
															columndata[i].filter = {
																type : 'list',
																store : optionsStore
															}
															columndata[i].renderer = function(value, metaData, record, rowIndex, colIndex, store) {
																// console.log(record.data)
																value = '      ';
																bkimg = "";
																bksz = "";
																bkpst = "";
																bkrp = "";
																pst = 0;
																{
																	if (record.data.co > 0) {
																		bkimg += ("url(/static/images/bkg_pink.png),")
																	} else {
																		bkimg += ("url(/static/images/bkg_gray.png),")
																	}
																	bksz += ("12% 100%,")
																	bkpst += (pst.toString());
																	pst += 15
																	bkpst += ("% 0%,")
																	bkrp += "no-repeat,"
																}
																{
																	if (record.data.ki > 0) {
																		bkimg += ("url(/static/images/bkg_red.png),")
																	} else {
																		bkimg += ("url(/static/images/bkg_gray.png),")
																	}
																	bksz += ("12% 100%,")
																	bkpst += (pst.toString());
																	pst += 15
																	bkpst += ("% 0%,")
																	bkrp += "no-repeat,"
																}
																{
																	if (record.data.li > 0) {
																		bkimg += ("url(/static/images/bkg_yellow.png),")
																	} else {
																		bkimg += ("url(/static/images/bkg_gray.png),")
																	}
																	bksz += ("12% 100%,")
																	bkpst += (pst.toString());
																	pst += 15
																	bkpst += ("% 0%,")
																	bkrp += "no-repeat,"
																}
																{
																	if (record.data.re > 0) {
																		bkimg += ("url(/static/images/bkg_green.png),")
																	} else {
																		bkimg += ("url(/static/images/bkg_gray.png),")
																	}
																	bksz += ("12% 100%,")
																	bkpst += (pst.toString());
																	pst += 15
																	bkpst += ("% 0%,")
																	bkrp += "no-repeat,"
																}
																{
																	if (record.data.pmm > 0) {
																		bkimg += ("url(/static/images/bkg_blue.png),")
																	} else {
																		bkimg += ("url(/static/images/bkg_gray.png),")
																	}
																	bksz += ("12% 100%,")
																	bkpst += (pst.toString());
																	pst += 15
																	bkpst += ("% 0%,")
																	bkrp += "no-repeat,"
																}
																{
																	if (record.data.pmh > 0) {
																		bkimg += ("url(/static/images/bkg_violet.png),")
																	} else {
																		bkimg += ("url(/static/images/bkg_gray.png),")
																	}
																	bksz += ("12% 100%,")
																	bkpst += (pst.toString());
																	pst += 15
																	bkpst += ("% 0%,")
																	bkrp += "no-repeat,"
																}
																{
																	if (record.data.tf > 0) {
																		bkimg += ("url(/static/images/bkg_brown.png),")
																	} else {
																		bkimg += ("url(/static/images/bkg_gray.png),")
																	}
																	bksz += ("12% 100%,")
																	bkpst += (pst.toString());
																	pst += 15
																	bkpst += ("% 0%,")
																	bkrp += "no-repeat,"
																}
																cssstring = '<div class="x-grid3-cell-inner" style="white-space: pre;';
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
																return cssstring + value + '</div>'
															}
															columndata[i].items = []
															// console.log(columndata[i])
														}
														if (columndata[i].text == 'Modification' && columndata[1].dataIndex != 'Sequence') {
															//var modi_list = [['pho_1', 'Phospho']]
															var modi_list= 	[['Acetyl_1', 'N-terminal Acetyltrasferases'], ['Methyl_1', 'Methylation'], ['GlyGly_1', 'Ubiquitination'], ['Biotin_1', 'Biotin'], ['PhosphoST_1', 'Phosphorylation-ST'], ['PhosphoY_1', 'Phosphorylation-Y']]
															var optionsStore1 = new Ext.data.Store({
																		fields : ['id', 'text'],
																		proxy : {
																			data : modi_list,
																			type : 'memory',
																			reader : {
																				type : 'array'
																			}
																		}
																	})
															// columndata[i].xtype = 'actioncolumn';
															//columndata[i].dataIndex = ''
															columndata[i].filter = {
																type : 'list',
																store : optionsStore1
															}
															columndata[i].items = []
															columndata[i].renderer = function(value, metaData, record, rowIndex, colIndex, store) {
																value = '      ';
																bkimg = "";
																bksz = "";
																bkpst = "";
																bkrp = "";
																pst = 0;
																{
																	if (record.data.Acetyl > 0) {
																		bkimg += ("url(/static/images/bkg_pink.png),")
																	} else {
																		bkimg += ("url(/static/images/bkg_gray.png),")
																	}
																	bksz += ("12% 100%,")
																	bkpst += (pst.toString());
																	pst += 15
																	bkpst += ("% 0%,")
																	bkrp += "no-repeat,"
																}
																{
																	if (record.data.Methyl > 0) {
																		bkimg += ("url(/static/images/bkg_red.png),")
																	} else {
																		bkimg += ("url(/static/images/bkg_gray.png),")
																	}
																	bksz += ("12% 100%,")
																	bkpst += (pst.toString());
																	pst += 15
																	bkpst += ("% 0%,")
																	bkrp += "no-repeat,"
																}
																{
																	if (record.data.GlyGly > 0) {
																		bkimg += ("url(/static/images/bkg_yellow.png),")
																	} else {
																		bkimg += ("url(/static/images/bkg_gray.png),")
																	}
																	bksz += ("12% 100%,")
																	bkpst += (pst.toString());
																	pst += 15
																	bkpst += ("% 0%,")
																	bkrp += "no-repeat,"
																}
																{
																	if (record.data.Biotin > 0) {
																		bkimg += ("url(/static/images/bkg_green.png),")
																	} else {
																		bkimg += ("url(/static/images/bkg_gray.png),")
																	}
																	bksz += ("12% 100%,")
																	bkpst += (pst.toString());
																	pst += 15
																	bkpst += ("% 0%,")
																	bkrp += "no-repeat,"
																}
																{
																	if (record.data.PhosphoST > 0) {
																		bkimg += ("url(/static/images/bkg_blue.png),")
																	} else {
																		bkimg += ("url(/static/images/bkg_gray.png),")
																	}
																	bksz += ("12% 100%,")
																	bkpst += (pst.toString());
																	pst += 15
																	bkpst += ("% 0%,")
																	bkrp += "no-repeat,"
																}
																{
																	if (record.data.PhosphoY > 0) {
																		bkimg += ("url(/static/images/bkg_violet.png),")
																	} else {
																		bkimg += ("url(/static/images/bkg_gray.png),")
																	}
																	bksz += ("12% 100%,")
																	bkpst += (pst.toString());
																	pst += 15
																	bkpst += ("% 0%,")
																	bkrp += "no-repeat,"
																}
																{}
																cssstring = '<div class="x-grid3-cell-inner" style="white-space: pre;';
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
																return cssstring + value + '</div>'
															}
															// console.log(columndata[i])
														}
														if (String(columndata[i].text).indexOf("Exp") != -1) {
															// console.log(columndata[i])
															columndata[i].columns[0].columns[0].renderer = function(value, metaData, record, row, col, store, gridView) {
																return value.toExponential(2);
															}
															if (type=='peptide')
															columndata[i].columns[0].columns[1].renderer = function(value, metaData, record, row, col, store, gridView) {
																cssstring = '<div class="x-grid3-cell-inner" style="text-align:center;';
																cssstring += '">' + "<a href='#'>"
																return cssstring + value + '</a>' + '</div>'
															}
														}
														
														if (String(columndata[i].text).indexOf("Median") != -1 || String(columndata[i].text).indexOf("Var") != -1 || String(columndata[i].text).indexOf("Average") != -1) {
															columndata[i].renderer = function(value, metaData, record, row, col, store, gridView) {
																return value.toExponential(2);
															}
														}
													}
													Ext.getCmp(timestamp).reconfigure(store, columndata);
												}
											});
									console.log('before createGrid' + val);
									createGrid(val);
									tab = Ext.getCmp('content-panel');
									// console.log(rec)
									tab.add({
												title : desc,
												iconCls : 'tabs',
												closable : true,
												layout : 'fit',
												items : [grid]
											}).show()
								}	
								if (rec.get('status') == 'done') {
									CreateGrid(val, type, desc, '',timestamp)
								};// if end
							}// handler end
						}]
						// item end
					}, {
						text : 'Job Description',
						dataIndex : 'description',
						width : 150,
						filter : {
							type : 'string',
							encode : true
						},
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							metaData.tdAttr = "data-qtip='" + value + "'";
							return value
						},
						sortable : true
					}, {
						text : 'Experiments Compared',
						dataIndex : 'exp_name',
						width : 180,
						filter : {
							type : 'string',
							encode : true
						},
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							cssstring = '<div class="x-grid3-cell-inner" style="text-align:left;';
							cssstring += '">' + "<a href='#'>"
							metaData.tdAttr = "data-qtip='" + value + "'";
							//console.log(cssstring + value + '</a>' + '</div>');
							return cssstring + value + '</a>' + '</div>'
						},
						// renderer : function(value, metaData, record, rowIndex, colIndex, store) {
						//					
						// return value
						// },
						sortable : true
					}, {
						text : "Exp count",
						dataIndex : 'explist_length'
					}, {
						text : 'Delta M/Z',
						dataIndex : 'dmz',
						filter : {
							type : 'float',
							encode : true
						},
						sortable : true
					}, {
						text : 'Delta RT',
						dataIndex : 'drt',
						filter : {
							type : 'float',
							encode : true
						},
						sortable : true
					}, {
						text : 'Ionscore',
						dataIndex : 'ionscore',
						filter : {
							type : 'float',
							encode : true
						},
						sortable : true
					}, {
						text : 'Compare?',
						dataIndex : 'compare',
						filter : {
							type : 'string',
							encode : true
						},
						sortable : true
					}, {
						text : 'QC?',
						dataIndex : 'qc',
						filter : {
							type : 'string',
							encode : true
						},
						sortable : true
					}, {
						text : 'View',
						dataIndex : 'ProGene',
						filter : {
							type : 'string',
							encode : true
						},
						sortable : true,
		                editor: new Ext.form.field.ComboBox({
		                    typeAhead: true,
		                    triggerAction: 'all',
		                    editable:false,
		                    store: [
		                        ['peptide','peptide'],
		                        ['protein','protein'],
		                        ['gene','gene']
		                    ]
		                })
					}, {
						text : 'Update time',
						dataIndex : 'update_time',
						filter : {
							type : 'string',
							encode : true
						},
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							metaData.tdAttr = "data-qtip='" + value + "'";
							return value
						},
						sortable : true
					}, {
						text : 'Commit time',
						dataIndex : 'create_time',
						filter : {
							type : 'string',
							encode : true
						},
						renderer : function(value, metaData, record, rowIndex, colIndex, store) {
							metaData.tdAttr = "data-qtip='" + value + "'";
							return value
						},
						sortable : true
					}, {
						text : "User",
						dataIndex : 'user',
						filter : {
							type : 'string',
							encode : true
						}
					}]
			});
		this.callParent();
	}
			 
})