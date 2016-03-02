Ext.define('gar.view.Menu', {
			extend : 'Ext.Toolbar',
			/**
			 * @requires gar.view.ppi
			 */
			requires: [
				'gar.view.ppi'
			],
			frame:true,
			initComponent : function() {
				Ext.regModel('Search_box', {
							fields : [{
										type : 'string',
										name : 'name'
									}, {
										type : 'string',
										name : 'value'
									}]
						});
				anywhere = function() {
					type = Ext.getCmp('anywhere-combo').getRawValue()

					symbol = Ext.getCmp('anywhere').getRawValue()
					if (symbol == '')
						return
					if (type == 'Protein') {
						var store = Ext.create('gar.store.Protein', {
									listeners : {
										totalcountchange : onStoreSizeChange
									}

								});
						var filters = {
							ftype : 'filters',
							encode : true
						}
						store.getProxy().extraParams = {
							stype : 'anywhere',
							symbol : symbol
						};
						var grid = Ext.create('gar.view.Protein', {
									store : store,
									features : [filters],
									dockedItems : [{
												dock : 'top',
												xtype : 'toolbar',
												items : [{
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
															xtype: 'button',
															text: 'Plot Distribution',
															handler:function() {
																var view = Ext.widget('globalplot');
															}
															//id: 'meplotdistribution'
														}, {
															xtype: 'button',
															itemId: 'ppi',
															text: 'PPI Analysis',
															disabled: true,
															handler: function() {
																var tmpGrid = grid
																var sm = tmpGrid.getSelectionModel()
																var proteinIdControl = sm.getSelection()[0].data.accession
																var proteinIdCaseList = []
																for(var i = 1; i < sm.getSelection().length; i++){
																	proteinIdCaseList.push(sm.getSelection()[i].data.accession)
																}
																Ext.widget('ppi',{
																	proteinIdControl : proteinIdControl,
																	proteinIdCaseList : proteinIdCaseList
																})
															}
														},  '->', {
															xtype : 'component',
															itemId : 'status',
															tpl : 'Matching Proteins: {count}',
															style : 'margin-right:5px'
														}]
											}],
									emptyText : 'No Matching Records',
									listeners : {
										render : function() {
											grid.columns[1].hidden = false
											grid.columns[2].hidden = false
										},
										'selectionchange': function(view, records){
											grid.down('#ppi').setDisabled(!records.length)
										}
									}
								})
					} else if (type == 'Peptide') {
						var store = Ext.create('gar.store.Peptide', {
									listeners : {
										totalcountchange : onStoreSizeChange
									}

								});
						var filters = {
							ftype : 'filters',
							encode : true
						}
						store.getProxy().extraParams = {
							stype : 'anywhere',
							symbol : symbol
						};
						var grid = Ext.create('gar.view.Peptide', {
									store : store,
									features : [filters],
									dockedItems : [{
												dock : 'top',
												xtype : 'toolbar',
												items : [{
															text : 'Clear Filter Data',
															handler : function() {
																grid.filters.clearFilters();
															}
														}, {
															text : 'All Filter Data',
															tooltip : 'Get Filter Data for Grid',
															handler : function() {
																{
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
															}
														}, '->', {
															xtype : 'component',
															itemId : 'status',
															tpl : 'Matching Peptides: {count}',
															style : 'margin-right:5px'
														}]
											}],
									emptyText : 'No Matching Records',
									listeners : {
										render : function() {
											grid.columns[1].hidden = false
											grid.columns[2].hidden = false
										},
										cellclick : peptide_sum_plot
									}
								})

					} else if (type == 'Gene') {

						var store = Ext.create('gar.store.Gene', {
									listeners : {
										totalcountchange : onStoreSizeChange
									}

								});
						var filters = {
							ftype : 'filters',
							encode : true
						}
						store.getProxy().extraParams = {
							stype : 'anywhere',
							symbol : symbol
						};
						var grid = Ext.create('gar.view.Gene', {
									store : store,
									features : [filters],
									dockedItems : [{
												dock : 'top',
												xtype : 'toolbar',
												items : [{
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
														}, '->', {
															xtype : 'component',
															itemId : 'status',
															tpl : 'Matching Genes: {count}',
															style : 'margin-right:5px'
														}]
											}],
									emptyText : 'No Matching Records',
									listeners : {
										render : function() {
											grid.columns[1].hidden = false
											grid.columns[2].hidden = false
										}
									}
								})

					}
					function onStoreSizeChange() {
						grid.down('#status').update({
									count : store.getTotalCount()
								});
					}
					c = Ext.getCmp('content-panel')
					Ext.getCmp('info_tab_index').value += 1
					c.add({
								title : 'All ' + type + ' of ' + symbol,
								iconCls : 'tabs',
								closable : true,
								// id : 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid]
							}).show()

				}
				var search_data = [{
							"name" : "Protein",
							"value" : "protein"
						}, {
							"name" : "Gene",
							"value" : "gene"
						}, {
							"name" : "Peptide",
							"value" : "peptide"
						}]

				var store_combo = Ext.create('Ext.data.Store', {
							model : 'Search_box',
							data : search_data
						});

				Ext.apply(this, {
							id : "menu",
							// frame:true,
							region : "north",
							border : false,
							height : 40,
							items : [
								' Tools : ',
								/* {
										xtype : 'button',
										tooltip : 'Quantification by Comparison Search',
										text : '',
										iconCls : "mecompare",
										id : 'mecompare'
									},*/{
										xtype : 'button',
										tooltip : 'New Comparison Search',
										iconCls : "newcompare",
										id : 'newcompare'
									}, 
//										{
//										xtype : 'button',
//										text : '',
//										tooltip : 'Scatter Plot For peptide',
//										iconCls : "mescatter",
//										id : 'mescatter'
//									}, 
										{
										xtype : 'button',
										text : '',
										tooltip : 'TIC plot',
										iconCls : "metic",
										id : 'metic'
									}, {
										xtype : 'button',
										text : '',
										iconCls : 'mebarplot',
										tooltip : 'Bar Plot',
										id : 'mebarplot'
									},{
										xtype : 'button',
										//text : 'Venn plot',
										tooltip : 'Venn plot',
										iconCls : 'mevennplot',
										id : 'mevennplot'
									}, {
										xtype : 'button',
										text : '',
										tooltip : 'Data Export',
										iconCls : "imfileup",
										id : 'btdataexport'
									}, {
										xtype : 'button',
										text : '',
										tooltip : 'Filemaker Export',
										iconCls : "btfilemaker",
										id : 'btfilemaker'
									},  {
										xtype : 'button',
										text : 'Share',
										tooltip : 'Share to another lab',
										iconCls : "",
										id : 'btpublic'
									},
//									{
//										text : 'Statistics figure',
//										iconCls : "meplot",
//										id : 'mefigure',
//										menuAlign : 'tl-bl',
//										menu : {
//											xtype : 'menu',
//											items : [{
//														text : 'Venn plot',
//														iconCls : 'mevennplot',
//														id : 'mevennplot'
//													}, {
//														text : 'Radar plot',
//														iconCls : 'meradarplot',
//														id : 'meradarplot'
//													}, {
//														text : 'PCA Analysis',
//														iconCls : 'mepca',
//														id : 'mepca'
//													}, {
//														text : 'Clustering',
//														iconCls : 'mecluster',
//														id : 'mecluster'
//													}]
//										}
//									}, 
//										{
//										text : 'Analysis tools',
//										iconCls : "metools",
//										id : 'metools',
//										menuAlign : 'tl-bl',
//										menu : {
//											xtype : 'menu',
//											items : [{
//														text : 'Statistics Analysis',
//														iconCls : 'medatacon',
//														menu : {
//															items : [{
//																		text : 'Database Selection',
//																		iconCls : 'medata',
//																		id : 'mescriptitraqfc',
//																		name : 'mescript'
//
//																	}]
//														}
//													}, {
//														text : 'Hydrophobicity',
//														iconCls : 'medroptools',
//														id : 'medroptools'
//													}, {
//														text : 'Modification',
//														iconCls : 'memodi',
//														id : 'memodi'
//													}, {
//														text : 'Pathway mapping',
//														iconCls : 'mekeggtools',
//														id : 'mekeggtools'
//													}, {
//														text : 'Fraction Analysis',
//														iconCls : 'mefraction',
//														id : 'mefraction'
//													}]
//										}
//									}, 
										{
										text : 'Experiment Management',
										iconCls : "expmanage",
										id : 'expmanage',
										// menuAlign : 'tl-bl',
										menu : {
											xtype : 'menu',
											items : [{
														text : 'Display Experiment',
														iconCls : 'displayexperiment',
														id : 'displayexperiment'
													}, {
														text : 'Display Sample',
														iconCls : 'displaysample',
														id : 'displaysample'
													}, {
														text : 'Display Reagent',
														iconCls : 'displayreagent',
														id : 'displayreagent'
													}, '-',{
														text : 'Add Experiment',
														iconCls : 'addexperiment',
														id : 'addexperiment'
													}, {
														text : 'Add Sample',
														iconCls : 'addsample',
														id : 'addsample'
													}, {
														text : 'Add Reagent',
														iconCls : 'addreagent',
														id : 'addreagent'
													}]
										}
									},'-', ' Search : ',{
										xtype : 'combo',
										value : 'Protein',
										displayField : 'name',
										width : 80,
										store : store_combo,
										queryMode : 'local',
										editable:false,
										//selectOnFocus: true,
										//typeAhead: true,
										id : 'anywhere-combo'
									}, {
										xtype : 'trigger',
										triggerCls : Ext.baseCSSPrefix + 'form-search-trigger',
										width : 100,
										name : 'artikel',
										allowBlank : true,
										style : 'margin-left: 5px',
										id : 'anywhere',
										onTriggerClick : anywhere,
										listeners : {
											specialkey : function(field, event) {
												if (event.getKey() == event.ENTER) {
													// Ext.MessageBox.confirm('hahaha');
													anywhere()
												}
											}
										}
									}, '->',{
										xtype : 'button',
										text : '',
										tooltip : 'Help',
										iconCls : "help",
										id : 'help'
									},{
										xtype : 'button',
										text : '',
										tooltip : 'NCBI',
										iconCls : "ncbi",
										id : 'entrez'
									},{
										text : 'Upload',
										tooltip : 'Upload your files',
										//iconCls : "ncbi",
										// id : 'upload_jsp',
										menu: [{
											text: 'China Node',
											handler: function() {
												window.location.href = 'http://jar-for-china-node.oss-cn-beijing.aliyuncs.com/firmiana-upload-china-node.jnlp'
											}
										},{
											text: 'USA Node',
											handler: function() {
												window.location.href = 'http://jar-for-usa-node.oss-us-west-1.aliyuncs.com/firmiana-upload-usa-node.jnlp'
											}
										}]
									}
									//'-',{
									//	xtype : 'button',
									//	text : 'WeiLai',
										//iconCls : "ncbi",
									//	id : 'WeiLai_kegg'
									//}
									]
						});
				this.callParent(arguments);
			}
		})
