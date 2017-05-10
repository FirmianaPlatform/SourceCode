Ext.define('gar.controller.NewCompare', {
	extend : 'Ext.app.Controller',
	views : ['Menu'],
	init : function() {
		this.control({
			'#newcompare' : {
				click : function() {
					var data = (Ext.getCmp('info_experiments_selected').getValue()) ? Ext.decode(Ext.getCmp('info_experiments_selected').getValue()) : 0;
					console.log(data)
					//Ext.getCmp('info_experiments_selected').setValue(0)
					var len = (data != 0) ? data.length : 0
					var explist = ''
					var fraction_num = -1
					var columndata
					var notComplete=''
					for (i = 0; i < len; i++) {
						explist = explist + String(data[i].id) + ','
						if (data[i].stage!='5')
							notComplete=notComplete+data[i].name+';'
						if (fraction_num == -1)
							fraction_num = data[i].num_fraction
						else if (data[i].num_fraction != fraction_num)
							fraction_num = -2
					}
					if (len == 0) {
						Ext.Msg.show({
									title : 'Empty Experiment List',
									msg : 'Please Choose at least One Experiment',
									buttons : Ext.Msg.OK
								})
						return 0
					}
					notComplete=notComplete.substr(0,notComplete.length-1)
					if (notComplete!=''){
						Ext.Msg.show({
							title : 'Experiments Wrong',
							msg : notComplete+'are still running',
							buttons : Ext.Msg.OK
						})
				return 0
					}
					var submitForm = function() {
						var form = panel.getForm();
						// console.log(form)
						form.submit({
									url : '/gardener/newcompare/',
									params : {
										explist : explist
									},
									success : function(frm, act) {
										win.close();
										Ext.getCmp('btmessage').fireEvent('click');
										val = String(act.result.msg);
										Ext.Ajax.request({
											url : '/gardener/newcmpprotein/',
											params : {
												id : val,
												type : 1
											},
											method : 'POST'
												// , success : function(response)
												// {Ext.Msg.alert('Status',response.responseText)}
											});
										return
									},
									failure : function(response) {
										alert('Something wrong, please contact admin!');
									}
								})
					};
					var panel = new Ext.form.FormPanel({
								// frame : true,
								bodyPadding : '10 0 10 20',
								border : false,
								items : [{
											xtype : 'radiogroup',
											fieldLabel : 'Views',
											name : 'Views',
											columns : 3,
											vertical : true,
											items : [ {
												boxLabel : 'Peptide',
												name : 'Views',
												inputValue : 'Peptide'
											},{
														boxLabel : 'Protein',
														name : 'Views',
														inputValue : 'Protein',
														// width : 200,
														checked : true
													}, {
														boxLabel : 'Gene',
														name : 'Views',
														inputValue : 'Gene'
													}]
										}, {
											xtype : 'radiogroup',
											fieldLabel : 'Cross search',
											name : 'cross_search',
											columns : 2,
											vertical : true,
											items : [{
												boxLabel : 'Yes',
												name : 'cross_search',
												inputValue : 'Yes'
													// width : 200
												}, {
												boxLabel : 'No',
												name : 'cross_search',
												inputValue : 'No',
												checked : true
											}]
										}, {
											xtype : 'radiogroup',
											fieldLabel : 'Unified QC',
											name : 'QC',
											columns : 2,
											vertical : true,
											items : [{
												boxLabel : 'Yes',
												name : 'QC',
												inputValue : 'Yes'
													// width : 200
												}, {
												boxLabel : 'No',
												name : 'QC',
												inputValue : 'No',
												checked : true
											}]
										}, {
											xtype : 'numberfield',
											labelAligh : 'left',
											fieldLabel : 'dMz (ppm)',
											value : 10,
											name : 'dMz'
										}, {
											xtype : 'numberfield',
											labelAligh : 'left',
											fieldLabel : 'dRT (s)',
											name : 'dRT',
											value : 60
										}, {
											xtype : 'numberfield',
											labelAligh : 'left',
											fieldLabel : 'Ionscore',
											name : 'ionscore',
											value : 15
										}, {
											xtype : 'textarea',
											labelAligh : 'left',
											fieldLabel : 'Description',
											name : 'description'
										}]
							})
					var cmp_button = Ext.create('Ext.panel.Panel', {
								// frame : true,
								// renderTo : 'button',
								border : false,
								buttonAlign : "center",
								buttons : [{
											text : 'Start',
											handler : submitForm
										}]
							});
					if (fraction_num == -2) {
						// console.log(panel.items.items[1])
						panel.items.items[1].disable()// = true
						// panel.items.items[2].disable()// = true
					}
					var win = new Ext.Window({
						draggable : {
							constrain : true,
							constrainTo : Ext.getBody()
						},
						title : 'Comparison Search',
						width : 500,
						resizable : false,
						animateTarget : 'newcompare',
						items : [panel, cmp_button]
							/*
							 * , bbar : ['->', { text : 'Yes', handler : submitForm }, { text : 'No', handler :
							 * function() { win.close() } }]
							 */
						})
					win.show()
				}
			},
			'notice' : {
				cellclick : function(grid, td, cellIndex, record, tr, rowIndex, e, eOpts) {
					// console.log(grid.headerCt.grid.columns[cellIndex+2].text)
					// console.log(cellIndex)
					//console.log(grid.headerCt.grid.columns)
					text = grid.headerCt.grid.columns[cellIndex + 3].text
					if (text == 'Experiments Compared') {
						exp_name = record.data.exp_name
						console.log(exp_name)
						var rec = grid.getStore().getAt(rowIndex);
						// console.log(rec.data)
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
									title : 'Comparison Info of ' + exp_name,
									width : 700,
									height : 450,
									// y : 50,
									items : []
								})
						win.show()
						expList = exp_name.split('*')
						for (expL = 0; expL <expList.length; expL++) {
							Ext.Ajax.request({
										url : '/experiments/load/experiment/',
										params : {
											experiment_no : expList[expL].split('Exp')[1]
											// csrfmiddlewaretoken : csrftoken
										},
										success : function(response) {
											var panel = Ext.create('gar.view.Experiment_detail')
											var text = response.responseText;
											exp_Info_responseJson = Ext.JSON.decode(text).data;
											panel.items.items[0].setValue(exp_Info_responseJson.expname);
											panel.items.items[1].setValue(exp_Info_responseJson.company + '/ ' + exp_Info_responseJson.lab + '/ ' + exp_Info_responseJson.experimenter);
											panel.items.items[2].setValue(exp_Info_responseJson.date);
											panel.items.items[3].setValue(exp_Info_responseJson.Funding + '/ ' + exp_Info_responseJson.Project + '/ ' + exp_Info_responseJson.PI);
											panel.items.items[4].setValue(exp_Info_responseJson.SubProject + '/ ' + exp_Info_responseJson.Subject + '/ ' + exp_Info_responseJson.Manager);
											panel.items.items[5].setValue(exp_Info_responseJson.Experiment_type);
											panel.items.items[6].setValue(exp_Info_responseJson.description);
											panel.items.items[7].setValue(exp_Info_responseJson.sample_id);
											panel.items.items[8].setValue(exp_Info_responseJson.reagent_id);
											panel.items.items[9].setValue(exp_Info_responseJson.method_num);
											panel.items.items[10].setValue(exp_Info_responseJson.Digest_type + '/ ' + exp_Info_responseJson.Digest_enzyme);
											panel.items.items[11]
													.setValue(exp_Info_responseJson.search_database + '/ ' + exp_Info_responseJson.instrument_name + '/ ms1:' + exp_Info_responseJson.ms1 + '-' 
													+ exp_Info_responseJson.ms1_details + '/ ms2:' + exp_Info_responseJson.ms2 + '-' + exp_Info_responseJson.ms2_details);
											panel.items.items[12].setValue(exp_Info_responseJson.ispec);
											panel.items.items[13].setValue(exp_Info_responseJson.comments_conclusions);
											//console.log(responseJson)
											win.insert(0, panel)
										}
									});
							//console.log(win)
						}
					}
				}
			}
		})
	}
})