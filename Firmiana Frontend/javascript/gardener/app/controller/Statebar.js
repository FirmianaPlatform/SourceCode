Ext.define('gar.controller.Statebar', {
	extend : 'Ext.app.Controller',
	views : ['State'],
	// stores : ['ProtShort'],
	// models : ['PepShort', 'ProtShort'],
	init : function() {
		var system_state = {
			run : function() {
				Ext.Ajax.request({
							url : '/gardener/system_state/',
							success : function(response) {
								var text = response.responseText;
								var state = Ext.JSON.decode(text);
								var btstate = Ext.getCmp('btstate')
								btstate.setTooltip('Remaining resources(Cpu:'
										+ state.cpu + ',Mem:' + state.mem
										+ ',Running Tasks:' + state.task)
								if (state.mem >= 25 || state.cpu >= 50) {
									btstate.setIconCls('btstate')
								}
								if (state.mem < 25 || state.cpu < 50) {
									btstate.setIconCls('btstate_mid')
								}
								if (state.mem < 5 || state.cpu < 25) {
									btstate.setIconCls('btstate_low')
								}
							}
						});
			},
			interval : 60000
		}
		Ext.TaskManager.start(system_state);

  		Ext.TaskManager.start({
    		run:function(){
    			Ext.getCmp('info').items.items[0].setText(' Today is '+ Ext.Date.format(new Date(),'Y/n/d(D) H:i:s'));
    		},
	  		//scope: this,
	  		interval: 1000
  		});
  					
  					
		this.control({
			'#changepw' : {
				click : function() {
					
					Ext.tip.QuickTipManager.init();
					csrftoken = Ext.util.Cookies.get('csrftoken');
					var submitForm = function() {
						form = passwordPanel.getForm();
						//console.log(form)
						if (form.isValid()) {
							form.submit({
										url : '/changepassword/',
                						method:'POST',
										waitMsg : 'Checking......',
										success:function(form,action) 
											{
												Ext.Msg.alert('Success',action.result.tex)
												Ext.getCmp('changePasswordWindow').close()
											},
										failure:function(form,action) 
											{Ext.Msg.alert('Error',action.result.tex)}
									})
						}
					};

					var resetForm = function() {
						form = passwordPanel.getForm()
						form.reset()
					};

					Ext.apply(Ext.form.field.VTypes, {
								password : function(val, field) {
									if (field.initialPassField) {
										var pwd = field.up('form').down('#'
												+ field.initialPassField);
										return (val == pwd.getValue());
									}
									return true;
								},

								passwordText : 'Password do not match'
							});

					var passwordPanel = Ext.create('Ext.form.Panel', {
								width : 300,
								// height:500,
								// frame: true,
								bodyStyle : {
					// padding: '20px 10px'
								},
								bodyPadding : '15 5 15 15',
								defaults : {
									width : 270,
									labelWidth : 110
								},

								items : [
										{
											xtype : 'displayfield',
											fieldLabel : 'Logged in as:',
											value : Ext.util.Cookies.get("username"),
											editable : false,
											allowBlank : false
										},
										{
											xtype : 'textfield',
											fieldLabel : 'Old Password',
											name : 'password0',
											vtype : 'password',
											itemId : 'password0',
											inputType: 'password',
											allowBlank : false
										}, {
											xtype : 'textfield',
											fieldLabel : 'New Password',
											name : 'password1',
											vtype : 'password',
											itemId : 'password1',
											inputType: 'password',
											allowBlank : false
										}, {
											xtype : 'textfield',
											fieldLabel : 'Confirm Password',
											name : 'password2',
											vtype : 'password',
											initialPassField : 'password1',
											inputType: 'password',
											allowBlank : false
										}, {
											xtype : 'hiddenfield',
											name : 'csrfmiddlewaretoken',
											value : csrftoken
										}],
								buttons : [{
											text : 'Reset',
											handler : resetForm
										}, {
											text : 'Submit',
											handler : submitForm
										}]
							});

					var win = Ext.create('Ext.Window', {
								draggable: {
            							constrain: true,
            							constrainTo: Ext.getBody()
        							},
								title : 'Change Password',
								layout : 'fit',
								height : 224,
								width : 314,
								modal: true,
								id: 'changePasswordWindow',
								items : [passwordPanel],
								animateTarget: 'changepw'
							});
					win.show()
				}
			},

			'#btmessage' : {
				click : function() {
					var panel = Ext.getCmp('job_status');
					if (panel) {
						var main = Ext.getCmp("content-panel");
						main.setActiveTab(panel);
						panel.down('grid').getStore().load()
						return;
					}
					
					var filters = {
							ftype : 'filters',
							encode : true
						};
						
					function onStoreSizeChange() {
							job_grid.down('#status').update({
										count : store.getTotalCount()
									});
					};
					var store = Ext.create('gar.store.Notice', 
							{
								listeners : { totalcountchange : onStoreSizeChange }
							}
					);
					var job_grid = Ext.create('gar.view.Notice',{
						store:store,
						forceFit: true,
						features : [filters],
						dockedItems : [{
										dock : 'top',
										xtype : 'toolbar',
										items : [{
													text : 'Clear Filter Data',
													handler : function() {
														console.log('123')
														job_grid.filters.clearFilters();
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
														var filterData = job_grid.filters.getFilterData()
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
													//icon:'/static/images/refresh.png',
													text : 'Refresh This Tab',
													tooltip : 'Update to Latest Progress',
													handler : function() 
														{ store.load() }
												}, '->', {
													xtype : 'component',
													itemId : 'status',
													tpl : 'Matching Jobs: {count}',
													style : 'margin-right:5px'
												}]
									}],
						emptyText : 'No Matching Records'
					});
//					var win = Ext.create('Ext.Window',{
//						title:'Job status',
//						width:500,
//						height:500,
//						layout:'fit',
//						animateTarget:'btmessage',
//						item :[grid]
//						
//						
//					});
//					win.show();

					tab = Ext.getCmp('content-panel')
					tab.add({
						title : 'Job Status',
						id:'job_status',
						//iconCls : 'tabs',
						closable : true,
						layout : 'fit',
						items : [job_grid]
					}).show()
								
//					var my_timer = {
//    					run:function(){store.load()},
//	  					//scope: this,
//	  					interval: 300000
//  					}
//  					Ext.TaskManager.start(my_timer)
				}

			},
			'#btcube' : {
				click : function() {

					var timestamp = 'kegg' + (new Date()).valueOf();
					var store = Ext.create('Ext.data.Store', {
								// autoLoad : true,
								pageSize : 500,
								proxy : {
									type : 'ajax',
									timeout : 300000000,
									url : '/gardener/kegg_statistic/',
									reader : {
										type : 'json',
										root : 'data',
										metaProperty : 'metaData',
										totalProperty : 'total'
									}
								},
								listeners : {
									metachange : function(store, meta) {
										var columndata = meta.columns
										Ext.getCmp(timestamp).reconfigure(
												store, columndata)
										var column = Ext.getCmp(timestamp)
												.getView().getGridColumns(); // return all the columns of grid.
										column[12].renderer = function(value) {
											if (value == 'up') {
												return '<font color="#FF0000">'
														+ value + '</font>';
											} else {
												return '<font color="#33CC00">'
														+ value + '</font>';
											}
											// return column
											// value
										}
									}
								}
							});

					var filters = {
						ftype : 'filters',
						encode : true
					}
					var createGrid = function() {
						grid = Ext.create('gar.view.KeggStatistic', {
									emptyText : 'No Matching Records',
									store : store,
									features : [filters],
									id : timestamp,
									listeners : {
										cellclick : function(dbcell, td, cell,
												record, tr, row, e) {
											a = Ext.getElementById(td.id).classList[2]
													.toString().substring(12)
											var win = new Ext.Window({
														title : 'KEGG viwer',
														layout : 'fit',
														autoScroll : true,
														height : 655,
														width : 950,
														maximizable : true,
														html : '<img src=' + record.data.img + '>'
													});
											win.show()
										}
									}
								});
					}
					var win = new Ext.Window({
						draggable: {
            							constrain: true,
            							constrainTo: Ext.getBody()
        							},
						layout : 'fit',
						title : 'Confirm',
						resizable : false,
						closable : true,
						height : 130,
						animateTarget: 'btcube',
						items : {
							xtype : 'form',
							height : 100,
							width : 300,
							bodyPadding : 10,
							border : false,
							buttonAlign : 'center',
							items : [{
										xtype : 'numberfield',
										labelAligh : 'left',
										labelWidth : 120,
										fieldLabel : 'How many rows',
										value : 2,
										width : 280,
										name : 'kegg_num'
									}],
							buttons : [{
										text : 'Reset',
										handler : function() {
											this.up('form').getForm().reset();
										}
									}, {
										text : 'Start',
										handler : function() {
											kg_num = this.up('form').getForm()
													.findField('kegg_num')
													.getSubmitValue()
											// console.log(kg_num)
											store.getProxy().extraParams = {
												kegg_num : kg_num
											}
											createGrid();
											store.load();
											tab = Ext.getCmp('content-panel')
											tab.add({
														title : 'KEGG Pathway Viewer',
														iconCls : 'tabs',
														closable : true,
														layout : 'fit',
														items : [grid]
													}).show()
											win.close()
										}
									}]
						}
					})
					win.show()
				}
			}
		})
	}
})