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
	forceFit : true,
	plugins : {
		ptype : 'bufferedrenderer',
		trailingBufferZone : 0,
		leadingBufferZone : 100
	},
	columns : [{
				xtype : 'rownumberer',
				width : 50
			}, {
				hidden : true,
				dataIndex : 'csv_name'
			}, {
				hidden : true,
				dataIndex : 'explist'
			},{
				width : 70,
				align : 'center',
				text : "Status",
				xtype : 'actioncolumn',
				dataIndex : 'status',
				filter : {
					type : 'string',
					encode : true
				},
				items : [{
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
						hasGrouped = 0
						var val = String(rec.get('csv_name'));
						var type = rec.get('ProGene')
						var desc = ''
						if (rec.get('description') != '-')
							desc = 'Comparison Search of ' + rec.get('description')
						else
							desc = 'Comparison Search of Comparison' + rec.get('csv_name')
						var CreateGrid = function(val, type, desc, temp_name) {

							var explist = String(rec.get('explist')) + ',';
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
										pageSize : 10000,
										model : 'dynamicModel',
										leadingBufferZone : 300,
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
												temp_name : temp_name
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
							var timestamp = 'compare' + (new Date()).valueOf();
							info_compare_tool_index = timestamp;
							var createGrid = function(val) {
								//console.log(val)
								if (type != 'peptide') {
									grid = Ext.create('gar.view.MBRun', {
										store : store,
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
															var data = Ext.encode(grid.filters.getFilterData());
															Ext.Msg.alert('All Filter Data', data);
														}
													}, {
														xtype : 'button',
														tooltip : 'Change Viewer',
														text : '',
														iconCls : 'mcchange',
														handler : function() {
															var change = function(Lostdata, newValue) {
																for (var i = 0; i < Lostdata.length; i++) {
																	if (Lostdata[i].columns)
																		change(Lostdata[i].columns, newValue)
																	if (Lostdata[i] && Lostdata[i].text) {
																		if (Lostdata[i].text == 'Area' || Lostdata[i].text == 'Ibaq' || Lostdata[i].text == 'Fot') {
																			Lostdata[i].dataIndex = Lostdata[i].dataIndex.replace(String(Lostdata[i].text).toLowerCase(), newValue.toLowerCase())
																			Lostdata[i].text = newValue
																		}
																		if (Lostdata[i].dataIndex && Lostdata[i].dataIndex.indexOf('VS') != -1) {
																			var tempString = Lostdata[i].dataIndex.split('VS')
																			oldvalue = tempString[0].split('_')[4]
																			tempString[0] = tempString[0].replace(oldvalue.toLowerCase(), newValue.toLowerCase())
																			tempString[1] = tempString[1].replace(oldvalue.toLowerCase(), newValue.toLowerCase())
																			Lostdata[i].dataIndex = tempString[0] + 'VS' + tempString[1]
																			Lostdata[i].renderer = function(value, metaData, record, row, col, store, gridView) {
																				var examstring = tempString[0];
																				var controlstring = tempString[1];
																				if (record.data[controlstring] != 0 && record.data[controlstring] != -1) {
																					if (record.data[examstring] != -1)
																						ans = (record.data[examstring] / record.data[controlstring])
																					else
																						ans = 0
																					if (ans > 1) {
																						p = parseInt(1 / ans * 255);
																						k = ("00" + p.toString(16)).substr(p.toString(16).length)
																						s = "#ff" + k + k
																						return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + ans.toFixed(2) + '</div>'
																					} else {
																						p = parseInt(ans * 255);
																						k = ("00" + p.toString(16)).substr(p.toString(16).length)
																						s = "#" + k + "ff" + k
																						return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + ans.toFixed(2) + '</div>'
																					}
																				} else {
																					ans = 1e9
																					p = parseInt(1 / ans * 255);
																					k = ("00" + p.toString(16)).substr(p.toString(16).length)
																					s = "#ff" + k + k
																					return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + "Infinity" + '</div>'
																				}
																			}
																		}
																	}
																}
																return
															}
															var changeit = function() {
																data = panel.getForm().findField('itms').getSubmitValue()
																change(columndata, data)
																Ext.getCmp(timestamp).reconfigure(store, columndata)
																win.close()
															}
															var cmp_button = Ext.create('Ext.panel.Panel', {
																		border : false,
																		buttonAlign : "center",
																		buttons : [{
																					text : 'Start',
																					handler : changeit
																				}]
																	});
															var panel = new Ext.form.FormPanel({
																		items : [{
																					xtype : 'combobox',
																					displayField : 'itms',
																					name : 'itms',
																					fieldLabel : 'Views',
																					valueField : 'itms',
																					store : new Ext.data.SimpleStore({
																								fields : ["itms"],
																								data : [["Area"], ["Ibaq"], ["Fot"]]
																							}),
																					queryMode : 'local'
																				}]
																	})
															var win = new Ext.Window({
																		title : 'Change Viewer',
																		width : 320,
																		resizable : false,
																		items : [panel, cmp_button]
																	})
															win.show()
														}
													}, {
														xtype : 'button',
														tooltip : 'Significant Test',
														text : '',
														iconCls : 'mcttest',
														handler : function() {
															var column = []
															var change = function(Lostdata) {
																var ok = false
																for (var i = 0; i < Lostdata.length; i++) {
																	if (Lostdata[i].columns)
																		change(Lostdata[i].columns)
																	if (Lostdata[i] && Lostdata[i].text) {
																		var checkstring
																		if (Lostdata[i].dataIndex && Lostdata[i].dataIndex.indexOf('VS') != -1) {
																			ok = true
																			column.push(Lostdata[i].dataIndex)
																			checkstring = Lostdata[i].dataIndex
																		}
																		if (Lostdata[i].dataIndex && Lostdata[i].dataIndex.indexOf('_vs_') != -1) {
																			Lostdata.splice(i, 1)
																			i = i - 1
																		}
																	}
																}
																if (ok) {
																	var z = new Object();
																	z["dataIndex"] = checkstring.replace('VS', '_vs_')
																	column.push(checkstring.replace('VS', '_vs_'))
																	z["text"] = "P-value"
																	z["sortable"] = true
																	z["filter"] = {
																		'type' : 'float',
																		'encode' : true
																	}
																	z['renderer'] = function(value, metaData, record, row, col, store, gridView) {
																		return value.toFixed(2)
																	}
																	Lostdata.push(z)
																}
																return
															}
															var changeit = function() {
																change(columndata)
																// console.log(columndata)
																// console.log(column)
																Ext.getCmp(timestamp).reconfigure(store, columndata)
																store.getProxy().extraParams['columns'] = column
																store.load()
																win.close()
															}
															var cmp_button = Ext.create('Ext.panel.Panel', {
																		border : false,
																		buttonAlign : "center",
																		buttons : [{
																					text : 'Start',
																					handler : changeit
																				}]
																	});
															var win = new Ext.Window({
																		title : 'Change Viewer',
																		width : 320,
																		resizable : false,
																		items : [cmp_button]
																	})
															win.show()
														}
													}, {
														xtype : 'button',
														tooltip : 'Download Data',
														text : '',
														iconCls : 'imfileup',
														handler : function() {
															data = Ext.getCmp(timestamp).filters.getFilterData()
															var s = '&filter=[';
															for (i = 0; i < data.length; i++) {
																s += '{'
																temp = String(Ext.encode(data[i].data))
																s += temp.substr(1, temp.length - 2)
																s += ',"field":"'
																s += String(data[i].field)
																s += '"}'
																if (i != data.length - 1)
																	s += ','
															}
															s += ']'
															url = '/gardener/newcmpprotein/?download=yes&id=' + val + s
															window.open(url);
															// var url = "page2.html?args=" +
															// args.toString();
															// store.getProxy().extraParams['download'] =
															// 'no'
															// store.load()
														}
													}, {
														xtype : 'button',
														text : 'Tools',
														id: 'tools'+val,
														listeners : {
															click: function() {
																if(!Ext.getCmp('toolsPanel'))
																{
																	view = Ext.widget('tools',{val : val, proGene: rec.get('ProGene')});
																	info_compare_tool_index = timestamp;
																}
																else
																{
																	alert('Only one tools-panel can be open at once.')
																}
															}
														}
													}, 
//														{
//														hidden: false,
//														xtype : 'button',
//														text : 'Tools',
//														handler : function() {
//															getColumn = function(columndata, newValue) {
//																out = []
//																if (newValue == 'Group')
//																	for (i = 5; i < columndata.length; i++) {
//																		var tempStr = ''
//																		var gNode = columndata[i]
//																		for (j = 0; j < gNode.columns.length; j++) {
//																			var cNode = gNode.columns[j]
//																			// console.log(cNode)
//																			for (k = 0; k < cNode.columns.length; k++) {
//																				tempStr = tempStr + cNode.columns[k].columns[0].columns[0].dataIndex + ';'
//																			}
//																		}
//																		out.push(columndata[i].text + '|' + tempStr)
//																	}
//																else if (newValue == 'Condition')
//																	for (i = 5; i < columndata.length; i++) {
//																		var gNode = columndata[i]
//																		for (j = 0; j < gNode.columns.length; j++) {
//																			var cNode = gNode.columns[j]
//																			var tempStr = ''
//																			// console.log(cNode)
//																			for (k = 0; k < cNode.columns.length; k++) {
//																				tempStr = tempStr + cNode.columns[k].columns[0].columns[0].dataIndex + ';'
//																			}
//																			out.push(gNode.text + '_' + cNode.text + '|' + tempStr)
//																		}
//																	}
//																else if (newValue == 'Experiment')
//																	for (i = 5; i < columndata.length; i++) {
//																		var gNode = columndata[i]
//																		for (j = 0; j < gNode.columns.length; j++) {
//																			var cNode = gNode.columns[j]
//																			var tempStr = ''
//																			// console.log(cNode)
//																			for (k = 0; k < cNode.columns.length; k++) {
//																				// tempStr=tempStr+cNode.columns[k].columns[0].columns[0].dataIndex+';'
//																				// console.log(cNode.columns[k])
//																				out.push(cNode.columns[k].columns[0].columns[0].dataIndex + '|' + cNode.columns[k].columns[0].columns[0].dataIndex)
//																			}
//																		}
//																	}
//																// console.log(out)
//																temp_filter = Ext.getCmp(timestamp).filters.buildQuery(grid.filters.getFilterData());
//																return [out, temp_filter]
//															}
//															plot = function(me, type) {
//																var tabpanel = me.up().up().up().down('tabpanel')
//																var get = function(columndata, newValue) {
//																	temp = getColumn(columndata, newValue)
//																	out = temp[0]
//																	temp_filter = temp[1]
//																	var panel = Ext.create('Ext.panel.Panel', {
//																				width : 520,
//																				height : 530,
//																				hidden : false,
//																				autoScroll : true,
//																				maximizable : true,
//																				title : type + ' Plot Viewer',
//																				animateTarget : 'mevennplot',
//																				layout : 'fit',
//																				html : '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>',
//																				listeners : {
//																					afterRender : function() {
//																						Ext.Ajax.request({
//																									timeout : 600000,
//																									url : '/gardener/newcmpprotein/',
//																									method : 'GET',
//																									params : {
//																										id : val,
//																										levels : out,
//																										filter : temp_filter,
//																										R_type : type
//																									},
//																									success : function(response) {
//																										panel.update(response.responseText);
//																									},
//																									failure : function() {
//																										panel.update("Sorry! Error happen, please contact Admin with current URL.");
//																									}
//																								});
//																					}
//																				}
//																			});
//																	tabpanel.add(panel)
//																}
//																var changeit = function() {
//																	data = panel.getForm().findField('itms').getSubmitValue()
//																	get(columndata, data)
//																	// Ext.getCmp(timestamp).reconfigure(store,
//																	// columndata)
//																	win.close()
//																}
//																var cmp_button = Ext.create('Ext.panel.Panel', {
//																			border : false,
//																			buttonAlign : "center",
//																			buttons : [{
//																						text : 'Start',
//																						handler : changeit
//																					}]
//																		});
//																var panel = new Ext.form.FormPanel({
//																			items : [{
//																						xtype : 'combobox',
//																						displayField : 'itms',
//																						name : 'itms',
//																						fieldLabel : 'Plot Level',
//																						valueField : 'itms',
//																						store : new Ext.data.SimpleStore({
//																									fields : ["itms"],
//																									data : [["Group"], ["Condition"], ["Experiment"]]
//																								}),
//																						queryMode : 'local'
//																					}]
//																		})
//																var win = new Ext.Window({
//																			title : type + ' Plot',
//																			width : 320,
//																			resizable : false,
//																			items : [panel, cmp_button]
//																		})
//																win.show()
//															}
//															plot2 = function(me, type) {
//																var tabpanel = me.up().up().up().down('tabpanel')
//																var get = function(columndata, newValue) {
//																	temp_filter = temp[1]
//																	var panel = Ext.create('Ext.panel.Panel', {
//																				width : 520,
//																				height : 530,
//																				hidden : false,
//																				autoScroll : true,
//																				maximizable : true,
//																				title : type + ' Plot Viewer',
//																				animateTarget : 'mevennplot',
//																				layout : 'fit',
//																				html : '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>',
//																				listeners : {
//																					beforeRender : function() {
//																					},
//																					afterRender : function() {
//																						exp1 = panel2.getForm().findField('exp1').getSubmitValue()
//																						exp2 = panel2.getForm().findField('exp2').getSubmitValue()
//																						Ext.Ajax.request({
//																									timeout : 600000,
//																									url : '/gardener/newcmpprotein/',
//																									method : 'GET',
//																									params : {
//																										id : val,
//																										levels : out,
//																										filter : temp_filter,
//																										R_type : type,
//																										exp1 : exp1,
//																										exp2 : exp2
//																									},
//																									success : function(response) {
//																										panel.update(response.responseText);
//																									},
//																									failure : function() {
//																										panel.update("Sorry! Error happen, please contact Admin with current URL.");
//																									}
//																								});
//																					}
//																				}
//																			});
//																	tabpanel.add(panel)
//																}
//																var getExp = function() {
//																	out = temp[0]
//																	out2 = temp[0]
//																	for (i = 0; i < out2.length; i++)
//																		out2[i] = [out2[i]]
//																	panel2 = new Ext.form.FormPanel({
//																				items : [{
//																							xtype : 'combobox',
//																							displayField : 'exp1',
//																							name : 'exp1',
//																							fieldLabel : 'Exp1',
//																							valueField : 'exp1',
//																							store : new Ext.data.SimpleStore({
//																										fields : ["exp1"],
//																										data : out2
//																									}),
//																							queryMode : 'local'
//																						}, {
//																							xtype : 'combobox',
//																							displayField : 'exp2',
//																							name : 'exp2',
//																							fieldLabel : 'Exp2',
//																							valueField : 'exp2',
//																							store : new Ext.data.SimpleStore({
//																										fields : ["exp2"],
//																										data : out2
//																									}),
//																							queryMode : 'local'
//																						}]
//																			})
//																	var cmpbutton2 = Ext.create('Ext.panel.Panel', {
//																				border : false,
//																				buttonAlign : "center",
//																				buttons : [{
//																							text : 'Start',
//																							handler : changeit2
//																						}]
//																			});
//																	var win2 = new Ext.Window({
//																				title : type + ' Plot',
//																				width : 320,
//																				resizable : false,
//																				items : [panel2, cmpbutton2]
//																			}).show()
//																}
//																var changeit2 = function() {
//																	// data =
//																	// panel.getForm().findField('itms').getSubmitValue()
//																	// temp = getColumn(columndata, data)
//																	// console.log(temp)
//																	get(columndata, data)
//																	// Ext.getCmp(timestamp).reconfigure(store,
//																	// columndata)
//																	win.close()
//																}
//																var changeit = function() {
//																	data = panel.getForm().findField('itms').getSubmitValue()
//																	temp = getColumn(columndata, data)
//																	// console.log(temp)
//																	getExp()
//																	// Ext.getCmp(timestamp).reconfigure(store,
//																	// columndata)
//																	win.close()
//																}
//																var cmp_button = Ext.create('Ext.panel.Panel', {
//																			border : false,
//																			buttonAlign : "center",
//																			buttons : [{
//																						text : 'Start',
//																						handler : changeit
//																					}]
//																		});
//																var panel = new Ext.form.FormPanel({
//																			items : [{
//																						xtype : 'combobox',
//																						displayField : 'itms',
//																						name : 'itms',
//																						fieldLabel : 'Plot Level',
//																						valueField : 'itms',
//																						store : new Ext.data.SimpleStore({
//																									fields : ["itms"],
//																									data : [["Group"], ["Condition"], ["Experiment"]]
//																								}),
//																						queryMode : 'local'
//																					}]
//																		})
//																var win = new Ext.Window({
//																			title : type + ' Plot',
//																			width : 320,
//																			resizable : false,
//																			items : [panel, cmp_button]
//																		})
//																win.show()
//															}
//															plot3 = function(me, type) {
//																var tabpanel = me.up().up().up().down('tabpanel')
//																var get = function(columndata, newValue) {
//																	temp_filter = temp[1]
//																	var panel = Ext.create('Ext.panel.Panel', {
//																				width : 520,
//																				height : 530,
//																				hidden : false,
//																				autoScroll : true,
//																				maximizable : true,
//																				title : type + ' Plot Viewer',
//																				animateTarget : 'mevennplot',
//																				layout : 'fit',
//																				html : '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>',
//																				listeners : {
//																					beforeRender : function() {
//																					},
//																					afterRender : function() {
//																						num = panel2.getForm().findField('Num').getSubmitValue()
//																						Ext.Ajax.request({
//																									timeout : 600000,
//																									url : '/gardener/newcmpprotein/',
//																									method : 'GET',
//																									params : {
//																										id : val,
//																										levels : out,
//																										filter : temp_filter,
//																										R_type : type,
//																										k_num : num
//																									},
//																									success : function(response) {
//																										panel.update(response.responseText);
//																									},
//																									failure : function() {
//																										panel.update("Sorry! Error happen, please contact Admin with current URL.");
//																									}
//																								});
//																					}
//																				}
//																			});
//																	tabpanel.add(panel)
//																}
//																var getExp = function() {
//																	panel2 = new Ext.form.FormPanel({
//																				items : [{
//																							xtype : 'textfield',
//																							fieldLabel : 'Num',
//																							name : 'Num',
//																							labelWidth : 120
//																						}]
//																			})
//																	var cmpbutton2 = Ext.create('Ext.panel.Panel', {
//																				border : false,
//																				buttonAlign : "center",
//																				buttons : [{
//																							text : 'Start',
//																							handler : changeit2
//																						}]
//																			});
//																	var win2 = new Ext.Window({
//																				title : type + ' Plot',
//																				width : 320,
//																				resizable : false,
//																				items : [panel2, cmpbutton2]
//																			}).show()
//																}
//																var changeit2 = function() {
//																	// data =
//																	// panel.getForm().findField('itms').getSubmitValue()
//																	// temp = getColumn(columndata, data)
//																	// console.log(temp)
//																	get(columndata, data)
//																	// Ext.getCmp(timestamp).reconfigure(store,
//																	// columndata)
//																	win.close()
//																}
//																var changeit = function() {
//																	data = panel.getForm().findField('itms').getSubmitValue()
//																	temp = getColumn(columndata, data)
//																	// console.log(temp)
//																	getExp()
//																	// Ext.getCmp(timestamp).reconfigure(store,
//																	// columndata)
//																	win.close()
//																}
//																var cmp_button = Ext.create('Ext.panel.Panel', {
//																			border : false,
//																			buttonAlign : "center",
//																			buttons : [{
//																						text : 'Start',
//																						handler : changeit
//																					}]
//																		});
//																var panel = new Ext.form.FormPanel({
//																			items : [{
//																						xtype : 'combobox',
//																						displayField : 'itms',
//																						name : 'itms',
//																						fieldLabel : 'Plot Level',
//																						valueField : 'itms',
//																						store : new Ext.data.SimpleStore({
//																									fields : ["itms"],
//																									data : [["Group"], ["Condition"], ["Experiment"]]
//																								}),
//																						queryMode : 'local'
//																					}]
//																		});
//																var win = new Ext.Window({
//																			title : type + ' Plot',
//																			width : 320,
//																			resizable : false,
//																			items : [panel, cmp_button]
//																		});
//																win.show();
//															}
//															var panel = Ext.create('gar.view.ControlMenu', {
//																		boxplot : function() {
//																			me = this
//																			plot(me, 'boxplot')
//																		},
//																		stack : function() {
//																			me = this
//																			plot(me, 'stack')
//																		},
//																		heatmap : function() {
//																			me = this
//																			plot(me, 'heatmap')
//																		},
//																		correlation : function() {
//																			me = this
//																			plot(me, 'correlation')
//																		},
//																		volcano : function() {
//																			me = this
//																			plot2(me, 'volcano')
//																		},
//																		venn : function() {
//																			me = this
//																			plot2(me, 'venn')
//																		},
//																		k_heatmap : function() {
//																			me = this
//																			plot3(me, 'k-heatmap')
//																		},
//																		PCA : function() {
//																			me = this
//																			plot(me, 'pca')
//																		}
//																	})
//														}
//													}, 
														{
														xtype : 'button',
														tooltip : 'Transfer tools',
														text : 'Transfer',
														iconCls : '',
														handler : function() {
															getColumn = function(columndata, newValue) {
																out = []
																if (newValue == 'Group')
																	for (i = 5; i < columndata.length; i++) {
																		var tempStr = ''
																		var gNode = columndata[i]
																		for (j = 0; j < gNode.columns.length; j++) {
																			var cNode = gNode.columns[j]
																			// console.log(cNode)
																			for (k = 0; k < cNode.columns.length; k++) {
																				tempStr = tempStr + cNode.columns[k].columns[0].columns[0].dataIndex + ';'
																			}
																		}
																		out.push(columndata[i].text + '|' + tempStr)
																	}
																else if (newValue == 'Condition')
																	for (i = 5; i < columndata.length; i++) {
																		var gNode = columndata[i]
																		for (j = 0; j < gNode.columns.length; j++) {
																			var cNode = gNode.columns[j]
																			var tempStr = ''
																			console.log(cNode)
																			for (k = 0; k < cNode.columns.length; k++) {
																				tempStr = tempStr + cNode.columns[k].columns[0].columns[0].dataIndex + ';'
																			}
																			out.push(gNode.text + '_' + cNode.text + '|' + tempStr)
																		}
																	}
																else if (newValue == 'Experiment')
																	for (i = 5; i < columndata.length; i++) {
																		var gNode = columndata[i]
																		for (j = 0; j < gNode.columns.length; j++) {
																			var cNode = gNode.columns[j]
																			var tempStr = ''
																			// console.log(cNode)
																			for (k = 0; k < cNode.columns.length; k++) {
																				// tempStr=tempStr+cNode.columns[k].columns[0].columns[0].dataIndex+';'
																				// console.log(cNode.columns[k])
																				out.push(cNode.columns[k].columns[0].columns[0].dataIndex + '|' + cNode.columns[k].columns[0].columns[0].dataIndex)
																			}
																		}
																	}
																// console.log(out)
																temp_filter = Ext.getCmp(timestamp).filters.buildQuery(grid.filters.getFilterData());
																return [out, temp_filter]
															}
															var changeit = function() {
																data = panel.getForm().findField('itms').getSubmitValue()
																temp = getColumn(columndata, data)
																out = temp[0]
																filter_data = temp[1]
																var tree_store = Ext.create('gar.store.CompareTree');
																tree_store.getProxy().extraParams = {
																	out : out
																}
																var tree = Ext.create('gar.view.CompareTree', {
																			store : tree_store,
																			onGroupDone : function(parentNode, childNode) {
																				Ext.Ajax.request({
																							url : '/gardener/newcmpprotein/',
																							params : {
																								id : val,
																								filter : temp_filter,
																								R_type : 'transfer',
																								levels : out,
																								//explist : explist
																							},
																							method : 'GET',
																							success : function(response) {
																								var json = Ext.JSON.decode(response.responseText);
																								console.log(json)
																								temp_name = json.temp_name
																								CreateGrid(val, type, desc + '*', temp_name)
																							}
																						});
																			}
																		})
																var win = Ext.create('Ext.Window', {
																			width : 400,
																			height : 400,
																			minHeight : 200,
																			minWidth : 50,
																			hidden : false,
																			maximizable : true,
																			title : 'Group the Experiment',
																			renderTo : Ext.getBody(),
																			layout : 'fit',
																			items : tree
																		});
															}
															var cmp_button = Ext.create('Ext.panel.Panel', {
																		border : false,
																		buttonAlign : "center",
																		buttons : [{
																					text : 'Start',
																					handler : changeit
																				}]
																	});
															var panel = new Ext.form.FormPanel({
																		items : [{
																					xtype : 'combobox',
																					displayField : 'itms',
																					name : 'itms',
																					fieldLabel : 'Statistical Level',
																					valueField : 'itms',
																					store : new Ext.data.SimpleStore({
																								fields : ["itms"],
																								data : [["Group"], ["Condition"], ["Experiment"]]
																							}),
																					queryMode : 'local'
																				}]
																	})
															var win = new Ext.Window({
																		title : 'Statistical Level',
																		width : 320,
																		resizable : false,
																		items : [panel, cmp_button]
																	})
															win.show()
														}
													}, '->', {
														xtype : 'component',
														itemId : 'status',
														tpl : 'Matching Proteins: {count}'
													}]
										}],
										id : timestamp,
										plugins : [{
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
																						metaData.tdAttr = "data-qtip='Mz: " + record.data[mz] + '<br>RT: ' + record.data[rt] + "'";
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

/* ---- peptide grid start from here----*/
								else {
									grid = Ext.create('gar.view.MBRun', {
										store : store,
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
													var data = Ext.encode(grid.filters.getFilterData());
													Ext.Msg.alert('All Filter Data', data);
												}
											}, {
												xtype : 'button',
												text : 'Tools',
												id: 'tools'+val,
												listeners : {
													click: function() {
														if(!Ext.getCmp('toolsPanel'))
														{
															view = Ext.widget('tools',{val : val, proGene: rec.get('ProGene')});
															info_compare_tool_index = timestamp;
														}
														else
														{
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
										id : timestamp
									});
								}
/* ---- peptide grid end here       ----*/

							}
							Ext.Ajax.request({
										url : '/gardener/com_getheaders/',
										params : {
											id : val,
											explist : explist
										},
										method : 'POST',
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
												if (columndata[i].text == 'Modification' && columndata[0].dataIndex != 'Sequence') {
													var modi_list = [['pho_1', 'Phospho']]
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
													columndata[i].dataIndex = 'modification'
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
															if (record.data.pho > 0) {
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
															if (record.data.test1_2 > 0) {
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
															if (record.data.test1_3 > 0) {
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
															if (record.data.test1_4 > 0) {
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
															if (record.data.test1_5 > 0) {
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
															if (record.data.test1_6 > 0) {
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
															if (record.data.test1_7 > 0) {
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
													// console.log(columndata[i])
												}
												if (String(columndata[i].text).indexOf("Exp") != -1) {
													// console.log(columndata[i])
													columndata[i].columns[0].columns[0].renderer = function(value, metaData, record, row, col, store, gridView) {
														return value.toExponential(2);
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
							console.log('before createGrid'+val);
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
							CreateGrid(val, type, desc, '')
						};// if end
					}// handler end
				}]
				// item end
			}, {
				text : 'Job Description',
				dataIndex : 'description',
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
				filter : {
					type : 'string',
					encode : true
				},
				renderer : function(value, metaData, record, rowIndex, colIndex, store) {
					cssstring = '<div class="x-grid3-cell-inner" style="text-align:center;';
					cssstring += '">' + "<a href='#'>"
					metaData.tdAttr = "data-qtip='" + value + "'";
					return cssstring + value + '</a>' + '</div>'
				},
				// renderer : function(value, metaData, record, rowIndex, colIndex, store) {
				//					
				// return value
				// },
				sortable : true
			}, {
				text : "Exp amount",
				dataIndex:'explist_length'
			}, {
				text : '△M/Z',
				dataIndex : 'dmz',
				filter : {
					type : 'float',
					encode : true
				},
				sortable : true
			}, {
				text : '△RT',
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
				sortable : true
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
})