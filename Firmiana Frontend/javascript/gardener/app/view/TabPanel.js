Ext.define('gar.view.TabPanel', {
	extend : 'Ext.tab.Panel',
	initComponent : function() {
		var store = Ext.create('gar.store.Experiment', {
					// allow the grid to interact with the paging
					// scroller by
					// buffering
					listeners : {
						totalcountchange : onStoreSizeChange
					}
				});
		var downloadType = ''
		exploadMask = new Ext.LoadMask(this, {
					msg : 'Loading.....'
				});
		function onStoreSizeChange() {
			grid.down('#status').update({
						count : store.getTotalCount()
					});
		}
		var filters = {
			ftype : 'filters',
			encode : true
		}

		// var downloadMenu = Ext.create(Ext.menu.Menu,{
		// 	defaults: {
  //       		checked: false,
  //       		group: 'batchdownload'
  //       	},
		// 	items:[{
		// 		text: 'Peptide',
		// 		value: 'Peptide',
		// 		listeners: {
		// 			checkchange: function(item, checked) {
	 //            		if(checked){
  //           				downloadType = item.value
	 //            		}
	 //            	}
		// 		}
		// 	}, {
		// 		text: 'Protein',
		// 		value: 'Protein',
		// 		listeners: {
		// 			checkchange: function(item, checked) {
	 //            		if(checked){
  //           				downloadType = item.value
	 //            		}
	 //            	}
		// 		}
		// 	}, {
		// 		text: 'Gene',
		// 		value: 'Gene',
		// 		listeners: {
		// 			checkchange: function(item, checked) {
	 //            		if(checked){
  //           				downloadType = item.value
	 //            		}
	 //            	}
		// 		}
		// 	},'-',{
		// 		text: 'Start download',
		// 		handler: function() {
		// 			var s = ''
		// 			for(var i = 0; i < checkBoxList.length; i++){
		// 				s += checkBoxList[i]
		// 				if(i != checkBoxList.length - 1){
		// 					s += ','
		// 				}
		// 			}
		// 			console.log(s)
					
		// 			window.open('/api/batch_download/download/?' + 'dataType=' + downloadType + '&' + 'expList=' + s)
		// 		}
		// 	}]
		// })

		var grid = Ext.create('gar.view.Experiment', {
					id : 'grid_experiment',
					store : store,
					features : [filters],
					dockedItems : [{
								dock : 'top',
								xtype : 'toolbar',
								items : [
//										{
//											text : 'Check all',
//											handler : function() {}
//										},
										{
											text : 'Uncheck all',
											hidden:true,
											handler : function() {
												//this.up('tabpanel').getActiveTab().down('grid').selModel.selectAll();
												//var store = this.up().store
												//console.log(store.length)
												//globalStore = store
												if(store.getCount()==0) return
												
												for(var i = 0; i < store.getCount(); i++)
												{
													var exp_id = store.getAt(i).data.id
													if(document.getElementById('experiment_selector_' + exp_id))
													{document.getElementById('experiment_selector_' + exp_id).checked = false}
														
												}
												Ext.getCmp('info_experiments_selected').setValue("[]")
												checkBoxList = []
												
											}
										},
										{
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
										}, {
											iconCls:'refresh',
											//icon : '/static/images/refresh.png',
											text : 'Refresh This Tab',
											tooltip : 'Update to Latest Progress',
											handler : function() {
												store.load()
											}
										}, {
											text: 'Download',
											menu: [{
												text: 'Peptide',
												value: 'peptide',
												handler: function(item, checked) {
								            		var s = ''
													for(var i = 0; i < checkBoxList.length; i++){
														s += checkBoxList[i]
														if(i != checkBoxList.length - 1){
															s += ','
														}
													}
													window.open('/api/batch_download/download/?' + 'dataType=' + item.value + '&' + 'expList=' + s)
													console.log(item.value)
								            	}
											}, {
												text: 'Protein',
												value: 'protein',
												handler: function(item, checked) {
								            		var s = ''
													for(var i = 0; i < checkBoxList.length; i++){
														s += checkBoxList[i]
														if(i != checkBoxList.length - 1){
															s += ','
														}
													}
													window.open('/api/batch_download/download/?' + 'dataType=' + item.value + '&' + 'expList=' + s)
													console.log(item.value)
								            	}
											}, {
												text: 'Gene',
												value: 'gene',
												handler: function(item, checked) {
								            		var s = ''
													for(var i = 0; i < checkBoxList.length; i++){
														s += checkBoxList[i]
														if(i != checkBoxList.length - 1){
															s += ','
														}
													}
													window.open('/api/batch_download/download/?' + 'dataType=' + item.value + '&' + 'expList=' + s)
													console.log(item.value)
								            	}
											}]
										}, 
										// {
										// 	text: 'PPI',
										// 	menu: [{
										// 		text: 'PPI Launch',
										// 		handler: function() {
										// 			Ext.Ajax.request({
										//                 method: "GET",
										//                 timeout: 100000,
										//                 url: '/gardener/firmiana_ppi/',
										//                 params: {
										//                 	expIDList: checkBoxIDList.toString(),
										//                 	cutoff: 5,
										//                 	percent: 0.35
										//                 },
										//                 success: function(response) {
										//                     console.log('PPI Ajax Request succeed.')
										//                     var responseText = response.responseText
										//                     jsonObject = Ext.JSON.decode(responseText)
										//                 }
										//             })
										// 		}
										// 	},{
										// 		text: 'PPI Analysis',
										// 		handler: function() {
										// 			Ext.Ajax.request({
										//                 method: "GET",
										//                 timeout: 100000,
										//                 url: '/gardener/firmiana_ppi_analysis/',
										//                 params: {
										//                 	expIDList: checkBoxIDList.toString(),
										//                 	cutoff: 5,
										//                 	percent: 0.35
										//                 },
										//                 success: function(response) {
										//                     console.log('PPI Ajax Request succeed.')
										//                     var responseText = response.responseText
										//                 }
										//             })
										// 		}
										// 	}]
										// },
										  '->', {
											xtype : 'component',
											itemId : 'status',
											tpl : 'Matching Experiments: {count}',
											style : 'margin-right:5px'
										}]
							}],
					emptyText : 'No Matching Records',
					plugins : [{
						ptype : 'rowexpander',
						selectRowOnExpand : true,
						expandOnDblClick : true,
						rowBodyTpl : ['<div id="Reasearch-{id}" ></div>'],
						toggleRow : function(rowIdx) {
							var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row).down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view.getRecord(rowNode), grid = this.getCmp(), id = record
									.get('id'), targetId = 'Reasearch-' + id;
							if (row.hasCls(this.rowCollapsedCls)) {
								row.removeCls(this.rowCollapsedCls);
								this.recordsExpanded[record.internalId] = true;
								this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
								if (rowNode.grid) {
									nextBd.removeCls(hiddenCls);
									rowNode.grid.doComponentLayout();
								} else {
									Ext.create('Ext.data.Store', {
												model : 'gar.model.Search',
												pageSize : 100,
												autoLoad : true,
												proxy : {
													timeout : 300000,
													type : 'ajax',
													url : '/gardener/data/showsearch/',
													extraParams : {
														id : id
													},
													reader : {
														type : 'json',
														root : 'data',
														totalProperty : 'total'
													}
												},
												autoLoad : {
													callback : function() {
														nextBd.removeCls(hiddenCls);
														Ext.create('gar.view.Search', {
																	renderTo : targetId,
																	store : this,
																	row : row
																});
														rowNode.grid = grid;
														grid.suspendEvents();
													}
												},
												listeners : {
													beforeload : function() {
														exploadMask.show();
													},
													load : function() {
														exploadMask.hide();
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
					}],
					listeners : {
						//"scroll":function(){console.log("qw")},
						render : function(s) {
							
							var restoreCheck = function(){
								firstNum = s.store.lastRequestStart
										for(var i = 0; i < checkBoxList.length; i++){
											for(var j = firstNum; j < firstNum + 100; j++){
												if(s.store.getAt(j).data.name==checkBoxList[i]){
													var exp_id = s.store.getAt(j).data.id
													document.getElementById('experiment_selector_' + exp_id).checked = true
												}
											}
										}
							}
							Ext.get(s.id).dom.addEventListener('mousewheel', function(e) {
										restoreCheck()
										s.fireEvent('mousewheel', s, e);	
									}, false); // Webkit browsers and
							// IE9+
							Ext.get(s.id).dom.addEventListener('scroll', function(e) {
										restoreCheck()
										s.fireEvent('mousewheel', s, e);
									}, false);
							Ext.get(s.id).dom.addEventListener('DOMMouseScroll', function(e) {
										restoreCheck()
										s.fireEvent('mousewheel', s, e);
									}, false); // Firefox
						}
					}
				});
		// var column= grid.getView().getGridColumns(); // return all
		// the columns of grid.
		// column[2].renderer = function(value){
		// return 'qiuqiuqiuqiuqiuq' ; // return column value
		// }
		Ext.apply(this, {
			//xtype: 'plain-tabs',
			id : 'content-panel',
			region : 'center',
			defaults : {
				//autoScroll : true,
				bodyPadding : 0
			},
			activeTab : 0,
			//border : true,
			loadMask : true,
			viewConfig : {
				loadingText : 'Loading Experiment Relation Data...'
			},
			plugins : Ext.create('Ext.ux.TabCloseMenu', {
				extraItemsTail : ['-', {
					text : 'Detailed Information',
					handler : function(item) {
						// this.tabPanel.remove(this.item)
						//console.log(currentItem)
						title = currentItem.title
						names = title.split(' ')
						exp_name = String(names[names.length - 1])
						if (exp_name.indexOf('Exp') == -1) {
							Ext.Msg.alert('Detailed Information', title);
						} else {
							var win = Ext.create('Ext.Window', {
										// draggable : {
										// constrain : true,
										// constrainTo : Ext.getBody()
										// },
								layout: {
								    type: 'hbox',
								    align: 'left'
								},
										autoScroll : true,
										resizable : true,
										title : 'Detailed Information of ' + title,
										width : 700,
										height : 450,
										// y : 50,
										items : []
									})
							win.show()
							expList = exp_name.split('*')
							for (expL = 0; expL < expList.length; expL++) {
								Ext.Ajax.request({
									url : '/experiments/load/experiment/',
									params : {
										experiment_no : expList[expL].split('Exp')[1]
										// csrfmiddlewaretoken : csrftoken
									},
									success : function(response) {
										var panel = Ext.create('gar.view.Experiment_detail')
										var text = response.responseText;
										responseJson = Ext.JSON.decode(text).data;
										console.log(panel)
										panel.items.items[0].setValue(responseJson.expname);
										panel.items.items[1].setValue(responseJson.company + '/ ' + responseJson.lab + '/ ' + responseJson.experimenter);
										panel.items.items[2].setValue(responseJson.date);
										panel.items.items[3].setValue(responseJson.Funding + '/ ' + responseJson.Project + '/ ' + responseJson.PI);
										panel.items.items[4].setValue(responseJson.SubProject + '/ ' + responseJson.Subject + '/ ' + responseJson.Manager);
										panel.items.items[5].setValue(responseJson.Experiment_type);
										panel.items.items[6].setValue(responseJson.description);
										panel.items.items[7].setValue(responseJson.sample_num);
										panel.items.items[8].setValue(responseJson.reagent_num);
										panel.items.items[9].setValue(responseJson.method_num);
										panel.items.items[10].setValue(responseJson.Digest_type + '/ ' + responseJson.Digest_enzyme);
										panel.items.items[11]
												.setValue(responseJson.search_database + '/ ' + responseJson.instrument_name + '/ ms1:' + responseJson.ms1 + '-' + responseJson.ms1_details + '/ ms2:' + responseJson.ms2 + '-' + responseJson.ms2_details);
										panel.items.items[12].setValue(responseJson.ispec);
										panel.items.items[13].setValue(responseJson.comments_conclusions);
										// console.log(responseJson)
										win.insert(0, panel)
									}
								});
								// console.log(win)
							}
						}
					}
				}
				// {
				// text: 'Enabled',
				// checked: true,
				// hideOnClick: true,
				// handler: function(item) {
				// currentItem.tab.setDisabled(!item.checked);
				// }
				// }
				],
				listeners : {
					beforemenu : function(menu, item) {
						currentItem = item
					}
				}
			}),
			// plain: true,
			items : [{
						id : 'HomePage',
						title : 'Experiment Viewer',
						iconCls : 'displayexperiment',
						layout : 'fit',
						items : grid,
						closable : false
					}
			// ,{id : 'testHomePage',
			// title : 'HomePage',
			// iconCls : 'home',
			// layout : 'fit',
			// html : '<iframe scrolling="auto" frameborder="0" width="100%" height="100%" src="/gardener/help/">
			// </iframe>',
			// closable : true}
			]
		});
		this.callParent(arguments);
	}
})