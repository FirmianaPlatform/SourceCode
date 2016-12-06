Ext.define('gar.controller.Metadata', {
			extend : 'Ext.app.Controller',
			views : ['User'],
			init : function() {
				
				/*********************Refresh Show tab after editing*********************/
				//editTabIdList = ["edit_sample_tab", "edit_reagent_tab", "edit_exp_tab"]
				//showTabTitleList = ["Show Sample", "Show Reagent", "Show Experiment"]
				refreshShowTab =  function(tabTitle){
					var tab = Ext.getCmp('content-panel');
					var display = tab.items.items;
					//var editTabId = "edit_sample_tab";
					//var tabTitle = "Show Sample";
					var showTabId = "";
					for(var i=0; i<display.length; i++){
						var showTab = display[i];
						if(showTab.title==tabTitle ){
							showTabId = showTab.id;
							break;
						}
					}
					if(showTabId!=""){
						var showTabStore = Ext.getCmp(showTabId).items.items[0].store;
						showTabStore.load();
					}
				};
				
				/*********************Refresh Show tab after editing*********************/
				
				// /*********************EditReagent*********************/
				// CreateReagentForm=function(reagent_id){
				// var panel = Ext.getCmp('edit_reagent_tab');
				// if (panel) {
				// var main = Ext.getCmp("content-panel");
				// main.setActiveTab(panel);
				// return 0;
				// }
				// var timestamp = 'compare' + (new Date()).valueOf();
				// var add_application = function() {
				// var win = new Ext.Window({
				// title : 'ADD Application',
				// width : 320,
				// items : [{
				// xtype : 'form',
				// border : false,
				// // frame : true,
				// bodyPadding : 10,
				// id : 'application_form' + '',
				// items : [{
				// xtype : 'textfield',
				// labelWidth : 90,
				// labelAligh : 'left',
				// width : 250,
				// fieldLabel : 'Application',
				// name : 'Application'
				// }]
				// }],
				// bbar : ['->', {
				// text : 'Submit',
				// handler : function() {
				// application_form = Ext.getCmp('application_form' + '');
				// var newV = application_form.items.items[0].value;
				// applicationStore.add({
				// Application : newV
				// });
				// win.close();
				// }
				// }]
				// });
				// win.show();
				// };
				// var add_react_pecies = function() {
				// var win = new Ext.Window({
				// title : 'ADD React Species',
				// width : 400,
				// items : [{
				// xtype : 'form',
				// border : true,
				// // frame : true,
				// id : 'species_form' + '',
				// items : [{
				// xtype : 'textfield',
				// labelWidth : 120,
				// labelAligh : 'left',
				// width : 450,
				// fieldLabel : 'React Species',
				// name : 'React Species'
				// }]
				// }],
				// bbar : ['->', {
				// text : 'Submit',
				// handler : function() {
				// species_form = Ext.getCmp('species_form' + '');
				// var newV = species_form.items.items[0].value;
				// reactSpeciesStore.add({
				// React_species : newV
				// });
				// win.close();
				// }
				// }]
				// });
				// win.show();
				// };
				// // CSRF protection
				// csrftoken = Ext.util.Cookies.get('csrftoken');
				// // function: submit / canel form
				// var submitForm = function() {
				// formpanel = Ext.getCmp(timestamp);
				// var form = formpanel.getForm();
				// if (form.isValid()) {
				// form.submit({
				// //url : '/experiments/save/reagent/',
				// url : '/experiments/editsave/reagent/',
				// params : {
				// reagent_no : reagent_id
				// // csrfmiddlewaretoken : csrftoken
				// },
				// waitMsg : 'Saving Reagent......',
				// timeout : 300000,
				// // standardSubmit : true
				// success : function(frm, act) {
				// val = String(act.result.msg);
				// len = val.legnth
				// // console.log(len)
				// // val=val.substring(1)
				// if (val.length < 6) {
				// for (i = val.length; i < 6; i++)
				// val = '0' + val
				// }
				// Ext.Msg.alert('Success', 'Reagent add complete. Reagent No: '
				// + val);
				// },
				// failure : function(form, action) {
				// Ext.Msg.alert('Failed', 'Reagent adding failed.Contact
				// admin.');
				// }
				// })
				// }
				// };
				// var cancelForm = function() {
				// formpanel = Ext.getCmp(timestamp);
				// formpanel.getForm().reset();
				// };
				// // Manufactorer Store
				// var companyStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/all_company/',
				// reader : {
				// type : 'json',
				// root : 'all_company'
				// }
				// },
				// fields : [{
				// name : 'company',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var labStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/all_lab/',
				// reader : {
				// type : 'json',
				// root : 'all_lab'
				// }
				// },
				// fields : [{
				// name : 'lab',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var experimenterStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/all_experimenter/',
				// reader : {
				// type : 'json',
				// root : 'experimenters'
				// }
				// },
				// fields : [{
				// name : 'experimenter',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var reagentManufacturerStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Reagent_manufacturer/',
				// reader : {
				// type : 'json',
				// root : 'Reagent_manufacturers'
				// }
				// },
				// fields : [{
				// name : 'Reagent_manufacturer',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// // React Sepecies Store
				// var reactSpeciesStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/React_species/',
				// reader : {
				// type : 'json',
				// root : 'React_speciess'
				// }
				// },
				// fields : [{
				// name : 'React_species',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var antigenClonalTypeStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Antigen_clonal_type/',
				// reader : {
				// type : 'json',
				// root : 'Antigen_clonal_types'
				// }
				// },
				// fields : [{
				// name : 'Antigen_clonal_type',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// // Antigen Host Species Store
				// var antigenSpeciesStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Antigen_species/',
				// reader : {
				// type : 'json',
				// root : 'Antigen_speciess'
				// }
				// },
				// fields : [{
				// name : 'Antigen_species',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var antigenModificationStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Antigen_modification/',
				// reader : {
				// type : 'json',
				// root : 'Antigen_modifications'
				// }
				// },
				// fields : [{
				// name : 'Antigen_modification',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// // Purification Store
				// var purificationStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Purification/',
				// reader : {
				// type : 'json',
				// root : 'Purifications'
				// }
				// },
				// fields : [{
				// name : 'Purification',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// // Conjugate Store
				// var conjugateStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Conjugate/',
				// reader : {
				// type : 'json',
				// root : 'Conjugates'
				// }
				// },
				// fields : [{
				// name : 'Conjugate',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// // Affinity Store
				// var affinityStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Affinity/',
				// reader : {
				// type : 'json',
				// root : 'Affinitys'
				// }
				// },
				// fields : [{
				// name : 'Affinity',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// // Application Store
				// var applicationStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Application/',
				// reader : {
				// type : 'json',
				// root : 'Applications'
				// }
				// },
				// fields : [{
				// name : 'Application',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// // general panel information
				// var general = Ext.create('Ext.panel.Panel', {
				// title : 'General',
				// // frame : true,
				// layout : 'auto',
				// headerPosition : 'top',
				// bodyPadding : 10,
				// defaults : {
				// labelWidth : 120,
				// labelAligh : 'left',
				// width : 800,
				// allowBlank : false
				// },
				// items : [{
				// fieldLabel : 'Experimenter',
				// xtype : 'fieldcontainer',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// defaults : {
				// editable : false
				// },
				// items : [{
				// xtype : 'combobox',
				// displayField : 'company',
				// name : 'company',
				// valueField : 'company',
				// store : companyStore,
				// queryMode : 'local',
				// allowBlank : false,
				// emptyText : 'Company',
				// width : 300,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// var lab = Ext.getCmp("reagent-lab");
				// lab.clearValue();
				// lab.store.load({
				// params : {
				// id : records[0].data.company
				// }
				// })
				// }
				// }
				// }
				// }, {
				// xtype : 'combobox',
				// displayField : 'lab',
				// valueField : 'lab',
				// name : 'lab',
				// id : 'reagent-lab',
				// emptyText : 'Laboratory',
				// store : labStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 200,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// var experimenter = Ext.getCmp("reagent-experimenter");
				// experimenter.clearValue();
				// experimenter.store.load({
				// params : {
				// id : records[0].data.lab
				// }
				// })
				// }
				// }
				// }
				// }, {
				// xtype : 'combobox',
				// displayField : 'experimenter',
				// valueField : 'experimenter',
				// emptyText : 'Experimenter',
				// name : 'experimenter',
				// id : 'reagent-experimenter',
				// store : experimenterStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 180
				// }]
				// }, {
				// xtype : 'radiogroup',
				// fieldLabel : 'Reagent type',
				// name : 'reagent_type',
				// id : 'reagent_type' + '',
				// columns : 2,
				// vertical : true,
				// items : [{
				// boxLabel : 'Antibodies',
				// name : 'reagent_type',
				// inputValue : 'Antigen',
				// id:'Antigen'
				// }, {
				// boxLabel : 'Nuclear Acid',
				// name : 'reagent_type',
				// inputValue : 'DNA',
				// id:'DNA'
				// }, {
				// boxLabel : 'Proteins Motif',
				// name : 'reagent_type',
				// inputValue : 'Protein',
				// id:'Protein'
				// }, {
				// boxLabel : 'Chemial',
				// name : 'reagent_type',
				// inputValue : 'chemical',
				// id:'chemical'
				// }, {
				// boxLabel : 'Other',
				// name : 'reagent_type',
				// inputValue : 'other',
				// id:'other'
				// }]
				// }, {
				// xtype : 'textfield',
				// fieldLabel : 'Reagent Name',
				// name : 'name'
				// }, {
				// xtype : 'datefield',
				// fieldLabel : 'Date',
				// value : Ext.Date.format(new Date(), 'n/d/Y'),
				// width : 450,
				// name : 'date'
				// }, {
				// xtype : 'combobox',
				// fieldLabel : 'Manufacturer',
				// displayField : 'Reagent_manufacturer',
				// name : 'Reagent_manufacturer',
				// store : reagentManufacturerStore,
				// queryModel : true,
				// typeAhead : true
				// }, {
				// xtype : 'textfield',
				// fieldLabel : 'Catalog No',
				// name : 'catalog_no',
				// allowBlank : true
				// }, {
				// xtype : 'combobox',
				// fieldLabel : 'Conjugate Beads',
				// displayField : 'Conjugate',
				// name : 'Conjugate',
				// store : conjugateStore,
				// queryModel : 'local',
				// typeAhead : true
				// }, {
				// xtype : 'fieldcontainer',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'combobox',
				// fieldLabel : 'Application',
				// displayField : 'Application',
				// name : 'Application',
				// store : applicationStore,
				// queryMode : 'local',
				// multiSelect : true,
				// labelWidth : 120,
				// width : 415,
				// allowBlank : false
				// }, {
				// xtype : 'button',
				// text : 'Add',
				// handler : add_application
				// }]
				// }, {
				// xtype : 'fieldcontainer',
				// // fieldLabel : 'Species React',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'combobox',
				// valueField : 'React_species',
				// fieldLabel : 'Source Species',
				// name : 'React_species_source',
				// displayField : 'React_species',
				// store : reactSpeciesStore,
				// emptyText : 'Source',
				// queryMode : 'local',
				// multiSelect : true,
				// labelWidth : 120,
				// width : 415,
				// allowBlank : false
				// }, {
				// xtype : 'combobox',
				// valueField : 'React_species',
				// fieldLabel : 'Target Species',
				// // fieldLabel : 'Species
				// // React',
				// name : 'React_species_target',
				// displayField : 'React_species',
				// store : reactSpeciesStore,
				// queryMode : 'local',
				// emptyText : 'Target',
				// multiSelect : true,
				// labelWidth : 120,
				// width : 300,
				// allowBlank : false
				// }]
				// }, {
				// xtype : 'textfield',
				// name : 'Ispec_num',
				// fieldLabel : 'Ispec No',
				// labelWidth : 120,
				// allowBlank : true
				// }, {
				// xtype : 'hiddenfield',
				// name : 'csrfmiddlewaretoken',
				// value : csrftoken
				// }]
				// });
				// var buttonPanel = Ext.create('Ext.panel.Panel', {
				// // frame : true,
				// // renderTo : 'button',
				// // border : true,
				// buttonAlign : "center",
				// buttons : [{
				// text : 'Submit',
				// handler : submitForm
				// }, {
				// text : 'Cancel',
				// handler : cancelForm
				// }]
				// });
				// var formPanel = Ext.create('Ext.form.Panel', {
				// // frame : true,
				// // overflowY : 'scroll',
				// id : timestamp,
				// // renderTo : 'form',
				// items : [general]
				// }); // antigen information
				// var antigen = Ext.create('Ext.panel.Panel', {
				// title : 'ANTIGEN INFO',
				// border : true,
				// bodyPadding : 10,
				// // frame : true,
				// id : 'antigen' + '',
				// headerPosition : 'left',
				// defaults : {
				// labelWidth : 120,
				// labelAligh : 'left',
				// width : 450,
				// allowBlank : true
				// },
				// items : [{
				// xtype : 'textfield',
				// fieldLabel : 'GeneID',
				// name : 'gene_id'
				// }, {
				// xtype : 'combobox',
				// fieldLabel : 'Host Species',
				// displayField : 'Antigen_species',
				// name : 'Antigen_species',
				// store : antigenSpeciesStore,
				// queryMode : 'local',
				// typeAhead : true
				// }, {
				// xtype : 'combobox',
				// fieldLabel : 'Clonal Type',
				// name : 'Antigen_clonal_type',
				// displayField : 'Antigen_clonal_type',
				// store : antigenClonalTypeStore,
				// queryMode : 'local',
				// typeAhead : true
				// }, {
				// xtype : 'combobox',
				// fieldLabel : 'Modification',
				// name : 'Antigen_modification',
				// displayField : 'Antigen_modification',
				// store : antigenModificationStore,
				// queryMode : 'local',
				// typeAhead : true
				// }]
				// });
				// // dna information
				// var dna = Ext.create('Ext.panel.Panel', {
				// title : 'DNA INFO',
				// bodyPadding : 10,
				// border : true,
				// // frame : true,
				// id : 'dna' + '',
				// headerPosition : 'left',
				// defaults : {
				// labelWidth : 120,
				// labelAligh : 'left',
				// width : 450,
				// allowBlank : false
				// },
				// items : [{
				// xtype : 'textareafield',
				// name : 'dna_sequence',
				// fieldLabel : 'DNA Sequence'
				// }]
				// });
				// // ubi information
				// var ubi = Ext.create('Ext.panel.Panel', {
				// title : 'UBI INFO',
				// border : true,
				// bodyPadding : 10,
				// // frame : true,
				// id : 'ubi' + '',
				// headerPosition : 'left',
				// defaults : {
				// labelWidth : 120,
				// labelAligh : 'left',
				// width : 450,
				// allowBlank : false
				// },
				// items : [{
				// xtype : 'textareafield',
				// name : 'domain',
				// fieldLabel : 'Domain'
				// }]
				// });
				// var cas = Ext.create('Ext.panel.Panel', {
				// title : 'Chemical INFO',
				// bodyPadding : 10,
				// border : true,
				// // frame : true,
				// id : 'cas' + '',
				// headerPosition : 'left',
				// defaults : {
				// labelWidth : 120,
				// labelAligh : 'left',
				// width : 450,
				// allowBlank : false
				// },
				// items : [{
				// xtype : 'textareafield',
				// name : 'cas_number',
				// fieldLabel : 'CAS Number'
				// }]
				// });
				// // Other information
				// var remarks = Ext.create('Ext.panel.Panel', {
				// title : 'Description',
				// border : true,
				// bodyPadding : 10,
				// // frame : true,
				// id : 'remarks' + '',
				// headerPosition : 'left',
				// defaults : {
				// labelWidth : 120,
				// labelAligh : 'left',
				// width : 450,
				// allowBlank : false
				// },
				// items : [{
				// xtype : 'textareafield',
				// name : 'remarks',
				// fieldLabel : 'Remarks'
				// }]
				// });
				// // event listener for type radio
				// typeradio = Ext.getCmp('reagent_type' + '');
				// typeradio.on('change', function(radio, newV, oldV, e) {
				// if (oldV.reagent_type == 'Antigen') {
				// formPanel.remove(antigen, false);
				// } else if (oldV.reagent_type == 'DNA') {
				// formPanel.remove(dna, false);
				// } else if (oldV.reagent_type == 'Protein') {
				// formPanel.remove(ubi, false);
				// } else if (oldV.reagent_type == 'other') {
				// formPanel.remove(remarks, false);
				// } else if (oldV.reagent_type == 'chemical') {
				// formPanel.remove(cas, false);
				// }
				// if (newV.reagent_type == 'Antigen') {
				// formPanel.add(antigen);
				// } else if (newV.reagent_type == 'DNA') {
				// formPanel.add(dna);
				// } else if (newV.reagent_type == 'Protein') {
				// formPanel.add(ubi);
				// } else if (newV.reagent_type == 'chemical') {
				// formPanel.add(cas);
				// } else {
				// formPanel.add(remarks);
				// }
				// });
				// // formPanel.add(buttonPanel)
				// tab = Ext.getCmp('content-panel')
				// tab.add({
				// id : 'edit_reagent_tab',
				// title : 'Edit Reagent',
				// iconCls : 'addreagent',
				// closable : true,
				// layout : 'anchor',
				// items : [formPanel, buttonPanel]
				// }).show()
				// }
				//				
				// EditReagent=function(reagentID){
				// CreateReagentForm(reagentID)
				// Ext.Ajax.request({
				// url : '/experiments/load/reagent/',
				// params : {
				// reagent_no : reagentID
				// // csrfmiddlewaretoken : csrftoken
				// },
				// success : function(response) {
				// //var panel = Ext.create('gar.view.Experiment_detail')
				// var text = response.responseText;
				// responseJson = Ext.JSON.decode(text).data;
				// console.log(responseJson.reagent_type)
				// Ext.getCmp(responseJson.reagent_type).setValue(true)
				// }
				// });
				//
				// Ext.getCmp('edit_reagent_tab').items.items[0].getForm().load({
				// url : '/experiments/load/reagent/',
				// method : 'POST',
				// params : {
				// reagent_no : reagentID
				// }
				// });
				// }
				// /*********************EditReagent*********************/

				/** *******************EditReagent******************** */
				CreateReagentForm = function(reagent_id) {
					var panel = Ext.getCmp('edit_reagent_tab'  + "_metadata");
					if (panel) {
						var main = Ext.getCmp("content-panel");
						main.setActiveTab(panel);
						return 0;
					}
					var timestamp = 'compare' + (new Date()).valueOf();
					var add_application = function() {
						var win = new Ext.Window({
									title : 'ADD Application',
									width : 320,
									items : [{
												xtype : 'form',
												border : false,
												// frame : true,
												bodyPadding : 10,
												id : 'application_form' + timestamp,
												items : [{
															xtype : 'textfield',
															labelWidth : 90,
															labelAligh : 'left',
															width : 250,
															fieldLabel : 'Application',
															name : 'Application'
														}]
											}],
									bbar : ['->', {
												text : 'Submit',
												handler : function() {
													application_form = Ext.getCmp('application_form' + timestamp);
													var newV = application_form.items.items[0].value;
													applicationStore.add({
																Application : newV
															});
													win.close();
												}
											}]
								});
						win.show();
					};
					var add_react_pecies = function() {
						var win = new Ext.Window({
									title : 'ADD React Species',
									width : 400,
									items : [{
												xtype : 'form',
												border : true,
												// frame : true,
												id : 'species_form' + timestamp,
												items : [{
															xtype : 'textfield',
															labelWidth : 120,
															labelAligh : 'left',
															width : 450,
															fieldLabel : 'React Species',
															name : 'React Species'
														}]
											}],
									bbar : ['->', {
												text : 'Submit',
												handler : function() {
													species_form = Ext.getCmp('species_form' + timestamp);
													var newV = species_form.items.items[0].value;
													reactSpeciesStore.add({
																React_species : newV
															});
													win.close();
												}
											}]
								});
						win.show();
					};
					// CSRF protection
					csrftoken = Ext.util.Cookies.get('csrftoken');
					// function: submit / canel form
					var submitForm = function() {
						formpanel = Ext.getCmp(timestamp);
						var form = formpanel.getForm();
						if (form.isValid()) {
							Ext.Ajax.timeout = 180000;
							form.submit({
										// url : '/experiments/save/reagent/',
										url : '/experiments/editsave/reagent/',
										params : {
											reagent_no : reagent_id
											// csrfmiddlewaretoken : csrftoken
										},
										waitMsg : 'Saving Reagent......',
										//timeout : 300000,
										// standardSubmit : true
										success : function(frm, act) {
											val = String(act.result.msg);
											len = val.legnth
											// console.log(len)
											// val=val.substring(1)
											if (val.length < 6) {
												for (var i = val.length; i < 6; i++)
													val = '0' + val
											}
											Ext.Msg.alert('Success', 'Modify a reagent successfully. Reagent No.: ' + val);
											
											//refresh Show Reagent
											tabTitle = "Show Reagent";
											//refreshShowTab(tabTitle);
										},
										failure : function(form, action) {
											Ext.Msg.alert('Failed', 'Modify a reagent unsuccessfully. Contact admin.');
										}
									});

						}
					};
					var cancelForm = function() {
						formpanel = Ext.getCmp(timestamp);
						formpanel.getForm().reset();
					};
					// Manufactorer Store
					var companyStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/all_company/',
									reader : {
										type : 'json',
										root : 'all_company'
									}
								},
								fields : [{
											name : 'company',
											type : 'string'
										}],
								autoLoad : true
							});
					var labStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/all_lab/',
									reader : {
										type : 'json',
										root : 'all_lab'
									}
								},
								fields : [{
											name : 'lab',
											type : 'string'
										}],
								autoLoad : true
							});
					var experimenterStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/all_experimenter/',
									reader : {
										type : 'json',
										root : 'experimenters'
									}
								},
								fields : [{
											name : 'experimenter',
											type : 'string'
										}],
								autoLoad : true
							});
					var reagentManufacturerStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Reagent_manufacturer/',
									reader : {
										type : 'json',
										root : 'Reagent_manufacturers'
									}
								},
								fields : [{
											name : 'Reagent_manufacturer',
											type : 'string'
										}],
								autoLoad : true
							});
					// React Sepecies Store
					var reactSpeciesStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/React_species/',
									reader : {
										type : 'json',
										root : 'React_speciess'
									}
								},
								fields : [{
											name : 'React_species',
											type : 'string'
										}],
								autoLoad : true
							});
					var antigenClonalTypeStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Antigen_clonal_type/',
									reader : {
										type : 'json',
										root : 'Antigen_clonal_types'
									}
								},
								fields : [{
											name : 'Antigen_clonal_type',
											type : 'string'
										}],
								autoLoad : true
							});
					// Antigen Host Species Store
					var antigenSpeciesStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Antigen_species/',
									reader : {
										type : 'json',
										root : 'Antigen_speciess'
									}
								},
								fields : [{
											name : 'Antigen_species',
											type : 'string'
										}],
								autoLoad : true
							});
					var antigenModificationStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Antigen_modification/',
									reader : {
										type : 'json',
										root : 'Antigen_modifications'
									}
								},
								fields : [{
											name : 'Antigen_modification',
											type : 'string'
										}],
								autoLoad : true
							});
					// Purification Store
					var purificationStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Purification/',
									reader : {
										type : 'json',
										root : 'Purifications'
									}
								},
								fields : [{
											name : 'Purification',
											type : 'string'
										}],
								autoLoad : true
							});
					// Conjugate Store
					var conjugateStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Conjugate/',
									reader : {
										type : 'json',
										root : 'Conjugates'
									}
								},
								fields : [{
											name : 'Conjugate',
											type : 'string'
										}],
								autoLoad : true
							});
					// Affinity Store
					var affinityStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Affinity/',
									reader : {
										type : 'json',
										root : 'Affinitys'
									}
								},
								fields : [{
											name : 'Affinity',
											type : 'string'
										}],
								autoLoad : true
							});
					// Application Store
					var applicationStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Application/',
									reader : {
										type : 'json',
										root : 'Applications'
									}
								},
								fields : [{
											name : 'Application',
											type : 'string'
										}],
								autoLoad : true
							});
					// general panel information
					var general = Ext.create('Ext.panel.Panel', {
								title : 'General',
								// frame : true,
								layout : 'auto',
								headerPosition : 'top',
								bodyPadding : 10,
								defaults : {
									labelWidth : 120,
									labelAligh : 'left',
									width : 800,
									allowBlank : false
								},
								items : [{
											fieldLabel : 'Experimenter',
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											defaults : {
												editable : false
											},
											items : [{
														xtype : 'combobox',
														displayField : 'company',
														name : 'company',
														valueField : 'company',
														store : companyStore,
														queryMode : 'local',
														allowBlank : false,
														emptyText : 'Company',
														width : 300,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	var lab = Ext.getCmp("reagent-lab" + timestamp);
																	lab.clearValue();
																	lab.store.load({
																				params : {
																					id : records[0].data.company
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'lab',
														valueField : 'lab',
														name : 'lab',
														id : 'reagent-lab' + timestamp,
														emptyText : 'Laboratory',
														store : labStore,
														queryMode : 'local',
														allowBlank : false,
														width : 200,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	var experimenter = Ext.getCmp("reagent-experimenter" + timestamp);
																	experimenter.clearValue();
																	experimenter.store.load({
																				params : {
																					id : records[0].data.lab
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'experimenter',
														valueField : 'experimenter',
														emptyText : 'Experimenter',
														name : 'experimenter',
														id : 'reagent-experimenter' + timestamp,
														store : experimenterStore,
														queryMode : 'local',
														allowBlank : false,
														width : 180
													}]
										}, {
											xtype : 'radiogroup',
											fieldLabel : 'Reagent type',
											name : 'reagent_type',
											id : 'reagent_type' + timestamp,
											columns : 2,
											vertical : true,
											items : [{
														boxLabel : 'Antibodies',
														name : 'reagent_type',
														inputValue : 'Antigen',
														id : 'Antigen'
													}, {
														boxLabel : 'Nuclear Acid',
														name : 'reagent_type',
														inputValue : 'DNA',
														id : 'DNA'
													}, {
														boxLabel : 'Proteins Motif',
														name : 'reagent_type',
														inputValue : 'Protein',
														id : 'Protein',
														hidden : true
													}, {
														boxLabel : 'Chemical',
														name : 'reagent_type',
														inputValue : 'chemical',
														id : 'chemical'
													}, {
														boxLabel : 'Other',
														name : 'reagent_type',
														inputValue : 'other',
														id : 'other'
													}]
										}, {
											xtype : 'textfield',
											fieldLabel : 'Reagent Name',
											name : 'name'
										}, {
											xtype : 'datefield',
											fieldLabel : 'Date',
											value : Ext.Date.format(new Date(), 'n/d/Y'),
											width : 450,
											name : 'date'
										}, {
											xtype : 'combobox',
											fieldLabel : 'Manufacturer',
											displayField : 'Reagent_manufacturer',
											name : 'Reagent_manufacturer',
											store : reagentManufacturerStore,
											queryModel : true,
											typeAhead : true
										}, {
											xtype : 'textfield',
											fieldLabel : 'Catalog No',
											name : 'catalog_no',
											allowBlank : true
										}, {
											xtype : 'combobox',
											fieldLabel : 'Conjugate Beads',
											displayField : 'Conjugate',
											name : 'Conjugate',
											store : conjugateStore,
											queryModel : 'local',
											typeAhead : true
										}, {
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											items : [{
														xtype : 'combobox',
														fieldLabel : 'Application',
														displayField : 'Application',
														name : 'Application',
														store : applicationStore,
														queryMode : 'local',
														multiSelect : true,
														labelWidth : 120,
														width : 415,
														allowBlank : false
													}, {
														xtype : 'button',
														text : 'Add',
														handler : add_application
													}]
										}, {
											xtype : 'fieldcontainer',
											// fieldLabel : 'Species React',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											items : [{
														xtype : 'combobox',
														valueField : 'React_species',
														fieldLabel : 'Source Species',
														name : 'React_species_source',
														displayField : 'React_species',
														store : reactSpeciesStore,
														emptyText : 'Source',
														queryMode : 'local',
														multiSelect : true,
														labelWidth : 120,
														width : 415,
														allowBlank : false
													}, {
														xtype : 'combobox',
														valueField : 'React_species',
														fieldLabel : 'Target Species',
														// fieldLabel : 'Species
														// React',
														name : 'React_species_target',
														displayField : 'React_species',
														store : reactSpeciesStore,
														queryMode : 'local',
														emptyText : 'Target',
														multiSelect : true,
														labelWidth : 120,
														width : 300,
														allowBlank : false
													}]
										}, 
//										{
//											xtype : 'textfield',
//											name : 'Ispec_num',
//											fieldLabel : 'Ispec No',
//											labelWidth : 120,
//											allowBlank : true
//										}, 
										{
											xtype : 'hiddenfield',
											name : 'csrfmiddlewaretoken',
											value : csrftoken
										}]
							});
					var buttonPanel = Ext.create('Ext.panel.Panel', {
								// frame : true,
								// renderTo : 'button',
								// border : true,
								buttonAlign : "center",
								buttons : [{
											text : 'Submit',
											handler : submitForm
										}, {
											text : 'Cancel',
											handler : cancelForm
										}]
							});
					var commentsPanel = Ext.create('Ext.form.Panel', {
						title : 'Comments',
						border : true,
						// frame : true,
						bodyPadding : 10,
						headerPosition : 'top',
						defaults : {
							labelWidth : 120,
							// labelAlign : 'top',
							width : 800
							// allowBlank : false
						},
						items : [{
									xtype : 'textareafield',
									name : 'comments',
									fieldLabel : 'Extra Comments'
								},
								{
									xtype : 'textfield',
									name : 'Ispec_num',
									fieldLabel : 'Ispec No',
									labelWidth : 120,
									allowBlank : true
								}]
					});
					
					var formPanel = Ext.create('Ext.form.Panel', {
								// frame : true,
								// overflowY : 'scroll',
								id : timestamp,
								// renderTo : 'form',
								items : [general, commentsPanel]
							}); // antigen information
					var antigen = Ext.create('Ext.panel.Panel', {
								title : 'ANTIGEN INFO',
								border : true,
								bodyPadding : 10,
								// frame : true,
								id : 'antigen' + timestamp,
								headerPosition : 'left',
								defaults : {
									labelWidth : 120,
									labelAligh : 'left',
									width : 450,
									allowBlank : true
								},
								items : [{
											xtype : 'textfield',
											fieldLabel : 'GeneID',
											name : 'gene_id'
										}, {
											xtype : 'combobox',
											fieldLabel : 'Host Species',
											displayField : 'Antigen_species',
											name : 'Antigen_species',
											store : antigenSpeciesStore,
											queryMode : 'local',
											typeAhead : true
										}, {
											xtype : 'combobox',
											fieldLabel : 'Clonal Type',
											name : 'Antigen_clonal_type',
											displayField : 'Antigen_clonal_type',
											store : antigenClonalTypeStore,
											queryMode : 'local',
											typeAhead : true
										}, {
											xtype : 'combobox',
											fieldLabel : 'Modification',
											name : 'Antigen_modification',
											displayField : 'Antigen_modification',
											store : antigenModificationStore,
											queryMode : 'local',
											typeAhead : true
										}]
							});
					// dna information
					var dna = Ext.create('Ext.panel.Panel', {
								title : 'DNA INFO',
								bodyPadding : 10,
								border : true,
								// frame : true,
								id : 'dna' + timestamp,
								headerPosition : 'left',
								defaults : {
									labelWidth : 120,
									labelAligh : 'left',
									width : 450,
									allowBlank : false
								},
								items : [{
											xtype : 'textareafield',
											name : 'dna_sequence',
											fieldLabel : 'DNA Sequence'
										}]
							});
					// ubi information
					var ubi = Ext.create('Ext.panel.Panel', {
								title : 'UBI INFO',
								border : true,
								bodyPadding : 10,
								// frame : true,
								id : 'ubi' + timestamp,
								headerPosition : 'left',
								defaults : {
									labelWidth : 120,
									labelAligh : 'left',
									width : 450,
									allowBlank : false
								},
								items : [{
											xtype : 'textareafield',
											name : 'domain',
											fieldLabel : 'Domain'
										}]
							});
					var cas = Ext.create('Ext.panel.Panel', {
								title : 'Chemical INFO',
								bodyPadding : 10,
								border : true,
								// frame : true,
								id : 'cas' + timestamp,
								headerPosition : 'left',
								defaults : {
									labelWidth : 120,
									labelAligh : 'left',
									width : 450,
									allowBlank : false
								},
								items : [{
											xtype : 'textareafield',
											name : 'cas_number',
											fieldLabel : 'CAS Number'
										}]
							});
					// Other information
					var remarks = Ext.create('Ext.panel.Panel', {
								title : 'Description',
								border : true,
								bodyPadding : 10,
								// frame : true,
								id : 'remarks' + timestamp,
								headerPosition : 'left',
								defaults : {
									labelWidth : 120,
									labelAligh : 'left',
									width : 450,
									allowBlank : false
								},
								items : [{
											xtype : 'textareafield',
											name : 'remarks',
											fieldLabel : 'Remarks'
										}]
							});
					// event listener for type radio
					typeradio = Ext.getCmp('reagent_type' + timestamp);
					typeradio.on('change', function(radio, newV, oldV, e) {
								if (oldV.reagent_type == 'Antigen') {
									formPanel.remove(antigen, false);
								} else if (oldV.reagent_type == 'DNA') {
									formPanel.remove(dna, false);
								} else if (oldV.reagent_type == 'Protein') {
									formPanel.remove(ubi, false);
								} else if (oldV.reagent_type == 'other') {
									formPanel.remove(remarks, false);
								} else if (oldV.reagent_type == 'chemical') {
									formPanel.remove(cas, false);
								}
								if (newV.reagent_type == 'Antigen') {
									formPanel.insert(1,antigen);
								} else if (newV.reagent_type == 'DNA') {
									formPanel.insert(1,dna);
								} else if (newV.reagent_type == 'Protein') {
									formPanel.insert(1,ubi);
								} else if (newV.reagent_type == 'chemical') {
									formPanel.insert(1,cas);
								} else {
									formPanel.insert(1,remarks);
								}
							});
					// formPanel.add(buttonPanel)
					tab = Ext.getCmp('content-panel')
					tab.add({
								id : 'edit_reagent_tab' + "_metadata",
								title : 'Edit Reagent ' + reagent_id,
								iconCls : 'addreagent',
								closable : true,
								layout : 'anchor',
								items : [formPanel, buttonPanel],
		                        overflowY: 'scroll'
							}).show();
				}

				EditReagent = function(reagentID) {
					CreateReagentForm(reagentID)
					Ext.Ajax.request({
								url : '/experiments/load/reagent/',
								params : {
									reagent_no : reagentID
									// csrfmiddlewaretoken : csrftoken
								},
								success : function(response) {
									// var panel =
									// Ext.create('gar.view.Experiment_detail')
									var text = response.responseText;
									responseJson = Ext.JSON.decode(text).data;
									console.log(responseJson.reagent_type);
									
									Ext.getCmp(responseJson.reagent_type).setValue(true)
								}
							});

					Ext.getCmp('edit_reagent_tab' + "_metadata").items.items[0].getForm().load({
								url : '/experiments/load/reagent/',
								method : 'POST',
								params : {
									reagent_no : reagentID
								}
							});
				}
				/** *******************EditReagent******************** */

				/** *******************EditExperiment******************** */
				CreateExperimentForm = function(experiment_id, expResponseJson) {
					var panel = Ext.getCmp('edit_exp_tab'  + "_metadata");
					if (panel) {
						var main = Ext.getCmp("content-panel");
						main.setActiveTab(panel);
						return 0;
					}
					var timestamp = 'compare' + (new Date()).valueOf();
					// for setValue()
					exp_timestamp = timestamp;

					console.log("HHH");
					console.log(expResponseJson.Reagent_buffer1);

					var add_digest_type = function() {
						var win = new Ext.Window({
									title : 'ADD Digest Type',
									width : 400,
									items : [{
												xtype : 'form',
												border : true,
												// frame : true,
												id : 'type_form' + timestamp,
												items : [{
															xtype : 'textfield',
															labelWidth : 120,
															labelAligh : 'left',
															width : 450,
															fieldLabel : 'Type',
															name : 'Type'
														}]
											}],
									bbar : ['->', {
												text : 'Submit',
												handler : function() {
													var type_form = Ext.getCmp('type_form' + timestamp);
													var newV = type_form.items.items[0].value;
													digestTypeStore.add({
																Digest_type : newV
															});
													win.close();
												}
											}]
								});
						win.show();
					};
					var add_digest_enzyme = function() {
						var win = new Ext.Window({
									title : 'ADD Digest Enzyme',
									width : 400,
									items : [{
												xtype : 'form',
												border : true,
												// frame : true,
												id : 'enzyme_form' + timestamp,
												items : [{
															xtype : 'textfield',
															labelWidth : 120,
															labelAligh : 'left',
															width : 450,
															fieldLabel : 'Enzyme',
															name : 'Enzyme'
														}]
											}],
									bbar : ['->', {
												text : 'Submit',
												handler : function() {
													var enzyme_form = Ext.getCmp('enzyme_form' + timestamp);
													var newV = enzyme_form.items.items[0].value;
													digestEnzymeStore.add({
																Digest_enzyme : newV
															});
													win.close();
												}
											}]
								});
						win.show();
					};
					var add_project = function() {
						var win = new Ext.Window({
									title : 'ADD Project',
									width : 400,
									items : [{
												xtype : 'form',
												border : true,
												// frame : true,
												id : 'project_form' + timestamp,
												items : [{
															xtype : 'textfield',
															labelWidth : 120,
															labelAligh : 'left',
															width : 450,
															fieldLabel : 'Project',
															name : 'Project'
														}]
											}],
									bbar : ['->', {
												text : 'Submit',
												handler : function() {
													application_form = Ext.getCmp('project_form' + timestamp);
													var newV = application_form.items.items[0].value;
													projectStore.add({
																Project : newV
															});
													win.close();
												}
											}]
								});
						win.show();
					};
					// CSRF protection
					csrftoken = Ext.util.Cookies.get('csrftoken');
					Ext.QuickTips.init();
					// function used to deal submit and cancel
					// form
					var submitForm = function() {
						var form = formPanel.getForm();
						console.log(form)
						if (form.isValid()) {
							Ext.Ajax.timeout = 180000;
							form.submit({
								// url :
								// '/experiments/save/experiment/',
								url : '/experiments/editsave/experiment/',
								params : {
									experiment_no : experiment_id
									// csrfmiddlewaretoken : csrftoken
								},
								waitMsg : 'Saving Experiment......',
								//timeout : 300000,
								// standardSubmit :
								// true,
								success : function(frm, act) {
									Ext.Msg.alert('Success', 'Modify an experiment successfully. Experiment No.: '
													+ Ext.encode(act.result.msg));
									//Refresh Show Experiment
									tabTitle = "Show Experiment";
									//refreshShowTab(tabTitle);
								},
								failure : function(form, action) {
									Ext.Msg.alert('Failed', 'Modify an experiment unsuccessfully. Contact admin.');
								}
							});
						}
					};
					var cancelForm = function() {
						formPanel.getForm().reset();
					};
					// Model and Store for combobox of
					// experimenter
					/*
					 * var experimenterStore = Ext.create('Ext.data.Store', {
					 * proxy : { type : 'ajax', url :
					 * '/experiments/ajax/experimenter/', reader : { type :
					 * 'json', root : 'experimenters' } }, fields : [{ name :
					 * 'experimenter', type : 'string' }], autoLoad : true });
					 */
					var reagentMethodStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Reagent_method/',
									reader : {
										type : 'json',
										root : 'Reagent_methods'
									}
								},
								fields : [{
											name : 'Reagent_method',
											type : 'string'
										}],
								autoLoad : true
							});
					var instrumentStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Instrument/',
									reader : {
										type : 'json',
										root : 'Instruments'
									}
								},
								fields : [{
											name : 'Instrument',
											type : 'string'
										}],
								autoLoad : true
							});
					var MS1Store = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/instrument_ms1/',
									reader : {
										type : 'json',
										root : 'Instrument_MS1'
									}
								},
								fields : [{
											name : 'Instrument_MS1',
											type : 'string'
										}]
							});
					var MS1tolStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/instrument_ms1_tol/',
									reader : {
										type : 'json',
										root : 'Instrument_MS1_tol'
									}
								},
								fields : [{
											name : 'Instrument_MS1_tol',
											type : 'string'
										}]
							});
					var MS2Store = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/instrument_ms2/',
									reader : {
										type : 'json',
										root : 'Instrument_MS2'
									}
								},
								fields : [{
											name : 'Instrument_MS2',
											type : 'string'
										}]
							});
					var MS2tolStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/instrument_ms2_tol/',
									reader : {
										type : 'json',
										root : 'Instrument_MS2_tol'
									}
								},
								fields : [{
											name : 'Instrument_MS2_tol',
											type : 'string'
										}]
							});
					// Model and Store for combobox of project
					var reagentBufferStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Reagent_buffer/',
									reader : {
										type : 'json',
										root : 'Reagent_buffers'
									}
								},
								fields : [{
											name : 'Reagent_buffer',
											type : 'string'
										}],
								autoLoad : true
							});
					// Model and Store for combobox of project
					var projectStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Project/',
									reader : {
										type : 'json',
										root : 'Projects'
									}
								},
								fields : [{
											name : 'Project',
											type : 'string'
										}],
								autoLoad : true
							});
					var expTypeStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Experiment_type/',
									reader : {
										type : 'json',
										root : 'Experiment_types'
									}
								},
								fields : [{
											name : 'Experiment_type',
											type : 'string'
										}],
								autoLoad : true
							});
					var digestTypeStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Digest_type/',
									reader : {
										type : 'json',
										root : 'Digest_types'
									}
								},
								fields : [{
											name : 'Digest_type',
											type : 'string'
										}],
								autoLoad : true
							});
					var digestEnzymeStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Digest_enzyme/',
									reader : {
										type : 'json',
										root : 'Digest_enzymes'
									}
								},
								fields : [{
											name : 'Digest_enzyme',
											type : 'string'
										}],
								autoLoad : true
							});
					var workflowModeStore = Ext.create('Ext.data.Store', {
	                            proxy: {
	                                type: 'ajax',
	                                url: '/experiments/ajax/display/Workflow_mode/',
	                                reader: {
	                                    type: 'json',
	                                    root: 'Workflow_modes'
	                                }
	                            },
	                            fields: [{
	                                name: 'Workflow_mode',
	                                type: 'string'
	                            }],
	                            autoLoad: true
	                        });
					var searchEngineStore = Ext.create('Ext.data.Store', {
	                            proxy: {
	                                type: 'ajax',
	                                url: '/experiments/ajax/display/searchEngine/',
	                                reader: {
	                                    type: 'json',
	                                    root: 'searchEngines'
	                                }
	                            },
	                            fields: [{
	                                name: 'searchEngine',
	                                type: 'string'
	                            }],
	                            autoLoad: true
	                        });
					var searchDatabaseStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Search_database/',
									reader : {
										type : 'json',
										root : 'Search_databases'
									}
								},
								fields : [{
											name : 'Search_database',
											type : 'string'
										}],
								autoLoad : true
							});
					var instrumentManufacturerStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Instrument_manufacturer/',
									reader : {
										type : 'json',
										root : 'Instrument_manufacturers'
									}
								},
								fields : [{
											name : 'Instrument_manufacturer',
											type : 'string'
										}],
								autoLoad : true
							});
					var companyStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/all_company/',
									reader : {
										type : 'json',
										root : 'all_company'
									}
								},
								fields : [{
											name : 'company',
											type : 'string'
										}],
								autoLoad : true
							});
					var labStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/all_lab/',
									reader : {
										type : 'json',
										root : 'all_lab'
									}
								},
								fields : [{
											name : 'lab',
											type : 'string'
										}],
								autoLoad : true
							});
					var experimenterStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/all_experimenter/',
									reader : {
										type : 'json',
										root : 'experimenters'
									}
								},
								fields : [{
											name : 'experimenter',
											type : 'string'
										}],
								autoLoad : true
							});
					var separationMethodStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Separation_md/',
									reader : {
										type : 'json',
										root : 'Separation_mds'
									}
								},
								fields : [{
											name : 'Separation_md',
											type : 'string'
										}],
								autoLoad : true
							});
					var fixedModificationStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Fixed_Modification/',
									reader : {
										type : 'json',
										root : 'Fixed_Modifications'
									}
								},
								fields : [{
											name : 'Fixed_Modification',
											type : 'string'
										}],
								autoLoad : true
							});
					var dynamicModificationStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Dynamic_Modification/',
									reader : {
										type : 'json',
										root : 'Dynamic_Modifications'
									}
								},
								fields : [{
											name : 'Dynamic_Modification',
											type : 'string'
										}],
								autoLoad : true
							});
					var quantificationMethodsStore = Ext.create('Ext.data.Store', {
	                            // proxy: {
	                            //     type: 'ajax',
	                            //     url: '/experiments/ajax/display/Quantification_Method/',
	                            //     reader: {
	                            //         type: 'json',
	                            //         root: 'Quantification_Methods'
	                            //     }
	                            // },
	                            fields: [{
	                                name: 'quantificationMethod',
	                                type: 'string'
	                            }],
	                            data: [
	                            {quantificationMethod: 'Label-free'},
	                            {quantificationMethod: 'Labeled (SILAC)'},
	                            {quantificationMethod: 'Labeled (iTRAQ)'},
                            	{quantificationMethod: 'Labeled (TMT)'}
	                            ],
	                            autoLoad: true
	                        });
					// function: add a reagent panel to the
					// formpanel
					var addReagent = function(index, reagentnum) {
						var reagent = Ext.create('Ext.form.Panel', {
									title : 'Reagent ' + reagentnum,
									id : 'reagent' + reagentnum + timestamp,
									border : true,
									// frame : true,
									bodyPadding : 10,
									headerPosition : 'left',
									defaults : {
										labelWidth : 120,
										labelAligh : 'left',
										width : 450,
										allowBlank : false
									},
									items : [{
												xtype : 'combobox',
												fieldLabel : 'Reagent No.',
												displayField : 'reagent_no',
												name : 'reagent_no' + reagentnum,
												value : expResponseJson.reagentNoList[reagentnum - 1],
												editable : false,
												store : Ext.create('Ext.data.Store', {
															fields : [{
																		name : 'reagent_no',
																		type : 'string'
																	}],
															proxy : {
																type : 'ajax',
																url : '/experiments/ajax/reagent_no/',
																reader : {
																	type : 'json'
																}
															}
														}),
												typeAhead : true,
												listeners : {
													'afterrender' : function(combo, record, index) {
														Ext.Ajax.request({
																	url : '/experiments/data/reagent_short/',
																	params : {
																		id : combo.up().items.items[0].value,
																		csrfmiddlewaretoken : csrftoken
																	},
																	success : function(response) {
																		var text = response.responseText;
																		// var
																		// reagentResponseJson
																		// =
																		// Ext.JSON.decode(text);
																		reagentResponseJson = Ext.JSON.decode(text);
																		// combo.up().items.items[0].setValue(expResponseJson.reagentNoList[reagentnum-1]);
																		console.log("combo");
																		combo.up().items.items[1].setValue(reagentResponseJson.experimenter);
																		combo.up().items.items[2].setValue(reagentResponseJson.date);
																		combo.up().items.items[3].setValue(reagentResponseJson.name);
																		combo.up().items.items[4].setValue(reagentResponseJson.manufacturer);
																		combo.up().items.items[5].setValue(reagentResponseJson.catalog_no);
																		combo.up().items.items[6].setValue(reagentResponseJson.type);
																	}
																});
													},
													'select' : function(combo, record, index) {
														Ext.Ajax.request({
																	url : '/experiments/data/reagent_short/',
																	params : {
																		id : combo.up().items.items[0].value,
																		csrfmiddlewaretoken : csrftoken
																	},
																	success : function(response) {
																		var text = response.responseText;
																		var reagentResponseJson = Ext.JSON.decode(text);
																		// combo.up().items.items[0].setValue(expResponseJson.reagentNoList[reagentnum-1]);
																		console.log("combo");
																		combo.up().items.items[1].setValue(reagentResponseJson.experimenter);
																		combo.up().items.items[2].setValue(reagentResponseJson.date);
																		combo.up().items.items[3].setValue(reagentResponseJson.name);
																		combo.up().items.items[4].setValue(reagentResponseJson.manufacturer);
																		combo.up().items.items[5].setValue(reagentResponseJson.catalog_no);
																		combo.up().items.items[6].setValue(reagentResponseJson.type);
																	}
																});
													}
												}
											}, {
												xtype : 'displayfield',
												fieldLabel : 'Experimenter',
												id : 'rea-experimenter' + reagentnum + timestamp,
												allowBlank : false
											}, {
												xtype : 'displayfield',
												fieldLabel : 'Date',
												id : 'rea-date' + reagentnum + timestamp,
												name : 'date'
											}, {
												xtype : 'displayfield',
												fieldLabel : 'Name',
												id : 'rea-name' + reagentnum + timestamp,
												allowBlank : false
											}, {
												xtype : 'displayfield',
												fieldLabel : 'manufacturer',
												id : 'rea-manu' + reagentnum + timestamp
											}, {
												xtype : 'displayfield',
												fieldLabel : 'catalog_no',
												id : 'rea-cata' + reagentnum + timestamp
											}, {
												xtype : 'displayfield',
												fieldLabel : 'Type',
												id : 'rea-type' + reagentnum + timestamp
											}, {
												xtype : 'fieldcontainer',
												layout : {
													type : 'hbox',
													align : 'stretch'
												},
												items : [{
															xtype : 'textfield',
															fieldLabel : 'Amount',
															labelWidth : 120,
															name : 'reagent_amount' + reagentnum,
															value : expResponseJson.reagentAmountList[reagentnum - 1]
														}, {
															xtype : 'combobox',
															width : 80,
															name : 'reagent_unit' + reagentnum,
															displayField : 'Rx_unit_detail',
															store : Ext.create('Ext.data.Store', {
																		fields : [{
																					name : 'Rx_unit_detail',
																					type : 'string'
																				}],
																		proxy : {
																			type : 'ajax',
																			url : '/experiments/ajax/display/Rx_unit_detail/',
																			reader : {
																				type : 'json',
																				root : 'Rx_unit_details'
																			}
																		}
																	}),
															value : expResponseJson.reagentUnitList[reagentnum - 1]
														}]
											}, {
												xtype : 'combobox',
												fieldLabel : 'Method',
												displayField : 'Reagent_method',
												name : 'Reagent_method' + reagentnum,
												store : reagentMethodStore
											}, {
												xtype : 'combobox',
												fieldLabel : 'Wash Buffer',
												displayField : 'Reagent_buffer',
												name : 'Reagent_buffer' + reagentnum,
												value : expResponseJson.reagentBufferList[reagentnum - 1],
												store : reagentBufferStore
											}, {
												xtype : 'textareafield',
												fieldLabel : 'Adjustments',
												name : 'reagent_ajustments' + reagentnum,
												allowBlank : true
											}]
								});
						formPanel.insert(index, reagent);
					};
					// function: add a sample panel to the
					// formpanel
					var addSample = function(index, samplenum) {
						var sample = Ext.create('Ext.form.Panel', {
									title : 'Sample ' + samplenum,
									id : 'sample' + samplenum + timestamp,
									border : true,
									// frame : true,
									bodyPadding : 10,
									headerPosition : 'left',
									defaults : {
										labelWidth : 120,
										labelAligh : 'left',
										width : 450,
										allowBlank : false
									},
									items : [{
												xtype : 'combobox',
												fieldLabel : 'Sample No.',
												displayField : 'sample_no',
												name : 'sample_no' + samplenum,
												value : expResponseJson.sampleNoList[samplenum - 1],
												editable : false,
												store : Ext.create('Ext.data.Store', {
															fields : [{
																		name : 'sample_no',
																		type : 'string'
																	}],
															proxy : {
																type : 'ajax',
																url : '/experiments/ajax/sample_no/',
																reader : {
																	type : 'json'
																}
															}
														}),
												typeAhead : true,
												listeners : {
													'afterrender' : function(combo, record, index) {
														Ext.Ajax.request({
																	url : '/experiments/data/sample_short/',
																	params : {
																		id : combo.up().items.items[0].value,
																		csrfmiddlewaretoken : csrftoken
																	},
																	success : function(response) {
																		// console.log("samplenum="
																		// +
																		// samplenum
																		// )
																		var text = response.responseText;
																		// var
																		// sampleResponseJson
																		// =
																		// Ext.JSON.decode(text);
																		sampleResponseJson = Ext.JSON.decode(text);
																		combo.up().items.items[1].setValue(sampleResponseJson.experimenter);
																		combo.up().items.items[2].setValue(sampleResponseJson.date);
																		combo.up().items.items[3].setValue(sampleResponseJson.source_type);
																		combo.up().items.items[4].setValue(sampleResponseJson.txid);
																		combo.up().items.items[5].setValue(sampleResponseJson.source_strain);
																		combo.up().items.items[6].setValue(sampleResponseJson.source_genotype);
																		combo.up().items.items[7].setValue(sampleResponseJson.source_change);
																		combo.up().items.items[8].setValue(sampleResponseJson.rx);
																	}
																});
													},
													'select' : function(combo, record, index) {
														Ext.Ajax.request({
																	url : '/experiments/data/sample_short/',
																	params : {
																		id : combo.up().items.items[0].value,
																		csrfmiddlewaretoken : csrftoken
																	},
																	success : function(response) {
																		// console.log("samplenum="
																		// +
																		// samplenum
																		// )
																		var text = response.responseText;
																		var sampleResponseJson = Ext.JSON.decode(text);
																		combo.up().items.items[1].setValue(sampleResponseJson.experimenter);
																		combo.up().items.items[2].setValue(sampleResponseJson.date);
																		combo.up().items.items[3].setValue(sampleResponseJson.source_type);
																		combo.up().items.items[4].setValue(sampleResponseJson.txid);
																		combo.up().items.items[5].setValue(sampleResponseJson.source_strain);
																		combo.up().items.items[6].setValue(sampleResponseJson.source_genotype);
																		combo.up().items.items[7].setValue(sampleResponseJson.source_change);
																		combo.up().items.items[8].setValue(sampleResponseJson.rx);
																	}
																});
													}
												}
											}, {
												xtype : 'displayfield',
												fieldLabel : 'Experimenter',
												id : 'experimenter' + samplenum + timestamp,
												name : 'experimenter',
												allowBlank : false
											}, {
												xtype : 'displayfield',
												fieldLabel : 'Date',
												id : 'date' + samplenum + timestamp,
												name : 'date'
											}, {
												xtype : 'displayfield',
												fieldLabel : 'Type',
												name : 'txtype' + samplenum,
												id : 'txtype' + samplenum + timestamp
											}, {
												xtype : 'displayfield',
												fieldLabel : 'Taxon',
												name : 'txid' + samplenum,
												id : 'txid' + samplenum + timestamp
											}, {
												xtype : 'displayfield',
												fieldLabel : 'Strain',
												name : 'txstrain' + samplenum,
												id : 'txstrain' + samplenum + timestamp
											}, {
												xtype : 'displayfield',
												fieldLabel : 'Genotype',
												name : 'txgenotype' + samplenum,
												id : 'txgenotype' + samplenum + timestamp
											}, {
												xtype : 'displayfield',
												fieldLabel : 'Target Gene',
												name : 'txtarget' + samplenum,
												id : 'txtarget' + samplenum + timestamp
											}, {
												xtype : 'displayfield',
												fieldLabel : 'Treatment',
												name : 'txtreat' + samplenum,
												id : 'txtreat' + samplenum + timestamp
											}, {
												xtype : 'fieldcontainer',
												layout : {
													type : 'hbox',
													align : 'stretch'
												},
												items : [{
															xtype : 'textfield',
															fieldLabel : 'Amount',
															labelWidth : 120,
															name : 'sample_amount' + samplenum,
															value : expResponseJson.sampleAmountList[samplenum - 1]
														}, {
															xtype : 'combobox',
															width : 80,
															name : 'sample_unit' + samplenum,
															displayField : 'Rx_unit_detail',
															store : Ext.create('Ext.data.Store', {
																		fields : [{
																					name : 'Rx_unit_detail',
																					type : 'string'
																				}],
																		proxy : {
																			type : 'ajax',
																			url : '/experiments/ajax/display/Rx_unit_detail/',
																			reader : {
																				type : 'json',
																				root : 'Rx_unit_details'
																			}
																		}
																	}),
															value : expResponseJson.sampleUnitList[samplenum - 1]
														}]
											}, {
												xtype : 'textareafield',
												fieldLabel : 'Adjustments',
												name : 'sample_ajustments' + samplenum,
												value : expResponseJson.sampleAdjustmentsList[samplenum - 1],
												allowBlank : true
											}]
								});
						formPanel.insert(index, sample);
					};
					var addSeparation = function(index, method_order) {
						var methodPanel = Ext.create('Ext.container.Container', {
									id : 'method' + method_order + timestamp,
									// frame: true,
									layout : {
										type : 'hbox',
										align : 'stretch'
									},
									defaults : {
										labelWidth : 120,
										width : 100,
										bodyStyle : 'padding:10'
									},
									items : [{
												xtype : 'combobox',
												emptyText : 'Name',
												fieldLabel : '#' + method_order,
												displayField : 'Separation_md',
												name : 'separation_method' + method_order,
												flex : 2,
												store : separationMethodStore,
												typeAhead : true
											}, {
												xtype : 'textfield',
												name : 'separation_source' + method_order,
												emptyText : 'Source'
											}, {
												xtype : 'textfield',
												name : 'separation_Size' + method_order,
												emptyText : 'Size'
											}, {
												xtype : 'textfield',
												name : 'separation_buffer' + method_order,
												emptyText : 'Buffer'
											}, {
												xtype : 'textfield',
												name : 'separation_others' + method_order,
												emptyText : 'PH/others'
											}/*
												 * , { xtype : 'numberfield',
												 * name : 'separation_num' +
												 * method_order, minValue : 1,
												 * flex : 1 }
												 */]
								});
						separationPanel.insert(index, methodPanel);
					};
					// function used to delete a ragent panel
					// from formpanel
					var delReagent = function(reagentnum) {
						for (i = reagentnum; i > 0; i--) {
							var reagent = Ext.getCmp('reagent' + i + timestamp);
							formPanel.remove(reagent);
						}
					};
					// function used to delete a sample panel
					// from formpanel
					var delSample = function(samplenum) {
						for (i = samplenum; i > 0; i--) {
							var sample = Ext.getCmp('sample' + i + timestamp);
							formPanel.remove(sample);
						}
					};
					// function used to delete a separation
					// method panel from
					// separationPanel
					var delSeparation = function(methodnum) {
						for (i = methodnum; i > 0; i--) {
							var method = Ext.getCmp('method' + i + timestamp);
							separationPanel.remove(method);
						}
					};
					// general panel for input general
					// experiment information
					var generalPanel = Ext.create('Ext.form.Panel', {
								title : 'General',
								// frame : true,
								headerPosition : 'top',
								// autoHeight: true,
								bodyPadding : 10,
								defaults : {
									labelWidth : 120,
									labelAligh : 'left',
									width : 1000,
									allowBlank : false,
									msgTarget : 'side'
								},
								items : [{
											fieldLabel : 'Experimenter',
											// afterLabelTextTpl : required,
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											defaults : {
												allowBlank : false,
												editable : false,
												msgTarget : 'side'
											},
											items : [{
														xtype : 'combobox',
														displayField : 'company',
														name : 'company',
														valueField : 'company',
														store : companyStore,
														queryMode : 'local',
														emptyText : 'Company',
														width : 300,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	var lab = Ext.getCmp("exp-lab" + timestamp);
																	lab.clearValue();
																	lab.store.load({
																				params : {
																					id : records[0].data.company
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'lab',
														valueField : 'lab',
														name : 'lab',
														id : 'exp-lab' + timestamp,
														emptyText : 'Laboratory',
														store : labStore,
														queryMode : 'local',
														width : 200,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	var experimenter = Ext.getCmp("exp-experimenter" + timestamp);
																	experimenter.clearValue();
																	experimenter.store.load({
																				params : {
																					id : records[0].data.lab
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'experimenter',
														valueField : 'experimenter',
														emptyText : 'Experimenter',
														name : 'experimenter',
														id : 'exp-experimenter' + timestamp,
														store : experimenterStore,
														queryMode : 'local',
														width : 180
													}]
										}, {
											xtype : 'datefield',
											fieldLabel : 'Date',
											value : Ext.Date.format(new Date(), 'n/d/Y'),
											// afterLabelTextTpl : required,
											width : 450,
											name : 'date'
										}, {
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											defaults : {
												allowBlank : false,
												msgTarget : 'side',
												width : 300
											},
											items : [{
														xtype : 'textfield',
														fieldLabel : 'Funding',
														// afterLabelTextTpl :
														// required,
														name : 'Funding',
														emptyText : 'Fund',
														labelWidth : 120
													}, {
														xtype : 'textfield',
														fieldLabel : 'Project',
														name : 'Project',
														emptyText : 'Project',
														labelWidth : 60
													}, {
														xtype : 'textfield',
														name : 'PI',
														emptyText : 'PI Name',
														fieldLabel : 'PI Name',
														labelWidth : 60
													}]
										}, {
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											items : [{
														xtype : 'textfield',
														fieldLabel : 'Execution',
														name : 'SubProject',
														emptyText : 'SubProject',
														labelWidth : 120,
														width : 300
													}, {
														xtype : 'textfield',
														name : 'Subject',
														fieldLabel : 'Subject',
														emptyText : 'Subject',
														labelWidth : 60,
														width : 300
													}, {
														xtype : 'textfield',
														name : 'Manager',
														emptyText : 'Manager Name',
														fieldLabel : 'Manager',
														queryMode : 'local',
														labelWidth : 60,
														width : 300
													}]
										}, {
											xtype : 'combobox',
											fieldLabel : 'Experiment_type',
											displayField : 'Experiment_type',
											// afterLabelTextTpl : required,
											name : 'Experiment_type',
											store : expTypeStore,
											typeAhead : true,
											width : 240
										}, {
											xtype : 'numberfield',
											fieldLabel : 'Total number of Sample',
											// afterLabelTextTpl : required,
											id : 'sample_num' + timestamp,
											name : 'sample_num',
											minValue : 0,
											maxValue : 10,
											value : 0,
											listeners : {
												change : function(o, newV, oldV) {
													console.log("sample-newV:" + newV);
													console.log("sample-oldV:" + oldV);
													if (newV > 10) {
														alert('Number of sample must be smaller than 10!')
														newV = 1
														Ext.getCmp('sample_num' + timestamp).setValue(1)
													}
													if (oldV) {
														delSample(oldV);
													}
													for (i = 1; i <= newV; i++) {
														addSample(i, i);
													}
												}
											},
											width : 240
										}, {
											xtype : 'numberfield',
											fieldLabel : 'Total number of Reagent',
											// afterLabelTextTpl: required,
											id : 'reagent_num' + timestamp,
											name : 'reagent_num',
											minValue : 0,
											maxValue : 10,
											value : 0,
											allowblank : true,
											listeners : {
												change : function(o, newV, oldV) {
													if (newV > 10) {
														alert('Number of sample must be smaller than 10!')
														newV = 1
														Ext.getCmp('reagent_num' + timestamp).setValue(1)
													}
													sample_number = Ext.getCmp('sample_num' + timestamp);
													index = sample_number.value;
													if (oldV) {
														delReagent(oldV);
													}
													for (i = 1; i <= newV; i++) {
														addReagent(index + i, i);
													}
												}
											},
											width : 240
										}, {
											xtype : 'hiddenfield',
											name : 'csrfmiddlewaretoken',
											value : csrftoken
										}]
							});
					// separation panel for input general
					// experiment information
					var separationPanel = Ext.create('Ext.panel.Panel', {
								title : 'Pre-Separation',
								// frame : true,
								id : 'pre_separation' + timestamp,
								name : 'separationPanel',
								headerPosition : 'top',
								bodyPadding : 10,
								defaults : {
									labelWidth : 120,
									labelAligh : 'left',
									allowBlank : true,
									width : 1000
								},
								items : [{
											xtype : 'radiogroup',
											fieldLabel : 'Methods',
											name : 'separ_methods',
											id : 'pre_separation_methods' + timestamp,
											columns : 10,
											vertical : true,
											items : [{
														boxLabel : 'Online',
														name : 'separ_methods',
														inputValue : 'Online',
														checked : true
													}, {
														boxLabel : 'Offline',
														name : 'separ_methods',
														inputValue : 'Offline'
													}, {
														boxLabel : 'None',
														name : 'separ_methods',
														inputValue : 'None'
													}]
										}, {
											width : 240,
											xtype : 'numberfield',
											fieldLabel : 'Separation Method Number',
											id : 'method_num' + timestamp,
											name : 'method_num',
											value : 0,
											minValue : 0,
											maxValue : 10,
											listeners : {
												change : function(o, newV, oldV) {
													if (oldV) {
														delSeparation(oldV);
													}
													for (i = 1; i <= newV; i++) {
														addSeparation(i + 1, i);// it's
														// not
														// perfect
													}
												}
											}
										}, {
											xtype : 'textareafield',
											name : 'separation_ajustments',
											fieldLabel : 'Adjustments'
										}]
							});
					// digest panel for input general digest
					// information
					var digestPanel = Ext.create('Ext.panel.Panel', {
								title : 'Digest',
								border : true,
								// frame : true,
								bodyPadding : 10,
								headerPosition : 'top',
								defaults : {
									labelWidth : 120,
									// afterLabelTextTpl : required,
									labelAlign : 'left',
									allowBlank : false,
									width : 450,
									editable : false,
									msgTarget : 'side'
								},
								items : [{
											xtype : 'combobox',
											fieldLabel : 'Type',
											name : 'Digest_type',
											displayField : 'Digest_type',
											store : digestTypeStore,
											queryMode : 'local',
											typeAhead : true
										}, {
											xtype : 'combobox',
											fieldLabel : 'Enzyme',
											name : 'Digest_enzyme',
											displayField : 'Digest_enzyme',
											value : 'Trypsin',
											store : digestEnzymeStore,
											queryMode : 'local',
											typeAhead : true
										}]
							});

					// mode panel: choose workflow or import from elsewhere
                    var modePanel = Ext.create('Ext.panel.Panel', {
                        title: 'Mode',
                        border: true,
                        // frame : true,
                        bodyPadding: 10,
                        headerPosition: 'top',
                        defaults: {
                            labelWidth: 120,
                            // afterLabelTextTpl: required,
                            labelAlign: 'left',
                            // allowBlank: false,
                            // width: 450,
                            editable: false,
                            msgTarget: 'side'
                        },
                        items: [{
                            xtype: 'combobox',
                            fieldLabel: 'Mode',
                            name: 'workflowMode',
                            displayField: 'Workflow_mode',
                            value: 'FTP',
                            store: workflowModeStore,
                            // queryMode: 'local',
                            typeAhead: true,
                            listeners:{
                                change: function( item, newValue, oldValue, eOpts ){
                                    console.log(oldValue,newValue)
                                    if(oldValue){
                                        switch(oldValue){
                                            case 'FTP':{break}
                                            case 'Firmiana Cloud':{break}
                                            default:{
                                                var modePanelLength = modePanel.items.length
                                                modePanel.remove(modePanel.items.items[modePanelLength - 1])
                                            }
                                        }
                                    }
                                    if(newValue){
                                        switch(newValue){
                                            case 'FTP':{break}
                                            case 'Firmiana Cloud':{break}
                                            case 'PRIDE':{
                                                var prideDataStore = Ext.create('Ext.data.Store',{
                                                    fields:[
                                                        {name:'filename',   type:'string'},
                                                        {name:'fileurl',    type:'string'}
                                                    ]
                                                })
                                                var pridePanel = Ext.create('Ext.form.FieldSet',{
                                                    xtype: 'fieldset',
                                                    width: 1000,
                                                    title: 'PRIDE Options',
                                                    bodyPadding: 10,
                                                    defaults: {
                                                        labelWidth: 120,
                                                        labelAlign: 'left',
                                                        msgTarget: 'side',
                                                    },
                                                    items:[{
                                                        xtype: 'textfield',
                                                        name: 'pxdno',
                                                        fieldLabel: 'PXD No.',
                                                        width: 200,
                                                        allowBlank: false,
                                                        // afterLabelTextTpl: required,
                                                        flex:1,
                                                        listeners:{
                                                            blur: function(item,the) {
                                                                if(item.value){
                                                                    var newValue = item.value
                                                                    var myMask = new Ext.LoadMask({
                                                                        msg    : 'Please wait...',
                                                                        target : pridePanel
                                                                    });
                                                                    myMask.show()
                                                                    Ext.Ajax.request({
                                                                        url : '/experiments/getPrideFileList/',
                                                                        method : 'GET',
                                                                        params : {
                                                                            pxdNo: newValue
                                                                        },
                                                                        success : function(response) {
                                                                            prideDataStore.removeAll()
                                                                            var responseText = response.responseText
                                                                            var addressList = responseText.split(';')
                                                                            for(var i = 0; i < addressList.length; i++){
                                                                                var array = addressList[i].split(',')
                                                                                prideDataStore.add({'filename': array[0], 'fileurl': array[1]})
                                                                            }
                                                                            myMask.hide()
                                                                            var itemselector = Ext.create('Ext.ux.form.ItemSelector',{
                                                                                name: 'prideFileList',
                                                                                height: 400,
                                                                                fieldLabel: 'File list',
                                                                                store: prideDataStore,
                                                                                displayField: 'filename',
                                                                                valueField: 'fileurl',
                                                                                fromTitle: 'File available',
                                                                                toTitle: 'File selected'
                                                                            })
                                                                            if(pridePanel.down('itemselector')){}else{
                                                                                pridePanel.insert(1,itemselector)
                                                                            }
                                                                        },
                                                                        failure : function() {
                                                                            myMask.hide()
                                                                            Ext.Msg.alert("Error","Wrong pxd No.. Please check again.");
                                                                        }
                                                                    });
                                                                }
                                                            }
                                                        }
                                                    }]
                                                })
                                                modePanel.insert(1,pridePanel)
                                                break
                                            }
                                            case 'MassIVE':{
                                                var prideDataStore = Ext.create('Ext.data.Store',{
                                                    fields:[
                                                        {name:'filename',   type:'string'},
                                                        {name:'fileurl',    type:'string'}
                                                    ]
                                                })
                                                var pridePanel = Ext.create('Ext.form.FieldSet',{
                                                    xtype: 'fieldset',
                                                    width: 1000,
                                                    title: 'PRIDE Options',
                                                    bodyPadding: 10,
                                                    defaults: {
                                                        labelWidth: 120,
                                                        labelAlign: 'left',
                                                        msgTarget: 'side',
                                                    },
                                                    items:[{
                                                        xtype: 'textfield',
                                                        name: 'pxdno',
                                                        fieldLabel: 'PXD No.',
                                                        width: 200,
                                                        allowBlank: false,
                                                        // afterLabelTextTpl: required,
                                                        flex:1,
                                                        listeners:{
                                                            blur: function(item,the) {
                                                                if(item.value){
                                                                    var newValue = item.value
                                                                    var myMask = new Ext.LoadMask({
                                                                        msg    : 'Please wait...',
                                                                        target : pridePanel
                                                                    });
                                                                    myMask.show()
                                                                    Ext.Ajax.request({
                                                                        url : '/experiments/getPrideFileList/',
                                                                        method : 'GET',
                                                                        params : {
                                                                            pxdNo: newValue
                                                                        },
                                                                        success : function(response) {
                                                                            prideDataStore.removeAll()
                                                                            var responseText = response.responseText
                                                                            var addressList = responseText.split(';')
                                                                            for(var i = 0; i < addressList.length; i++){
                                                                                var array = addressList[i].split(',')
                                                                                prideDataStore.add({'filename': array[0], 'fileurl': array[1]})
                                                                            }
                                                                            myMask.hide()
                                                                            var itemselector = Ext.create('Ext.ux.form.ItemSelector',{
                                                                                name: 'prideFileList',
                                                                                height: 400,
                                                                                fieldLabel: 'File list',
                                                                                store: prideDataStore,
                                                                                displayField: 'filename',
                                                                                valueField: 'fileurl',
                                                                                fromTitle: 'File available',
                                                                                toTitle: 'File selected'
                                                                            })
                                                                            if(pridePanel.down('itemselector')){}else{
                                                                                pridePanel.insert(1,itemselector)
                                                                            }
                                                                        },
                                                                        failure : function() {
                                                                            Ext.Msg.alert("Error","Wrong pxd No.. Please check again.");
                                                                        }
                                                                    });
                                                                }
                                                            }
                                                        }
                                                    }]
                                                })
                                                modePanel.insert(1,pridePanel)
                                                break
                                            }
                                            default:{
                                                Ext.Msg.alert('','Coming soon...')
                                            }
                                        }
                                    }
                                }
                            }
                        }]
                    });

					// search engine panel: choose workflow
                    var searchEnginePanel = Ext.create('Ext.panel.Panel', {
                        title: 'Search engine',
                        border: true,
                        // frame : true,
                        bodyPadding: 10,
                        headerPosition: 'top',
                        defaults: {
                            labelWidth: 120,
                            // afterLabelTextTpl: required,
                            labelAlign: 'left',
                            // allowBlank: false,
                            // width: 450,
                            editable: false,
                            msgTarget: 'side'
                        },
                        items: [{
                            xtype: 'combobox',
                            fieldLabel: 'Search Engine',
                            name: 'searchEngine',
                            displayField: 'searchEngine',
                            value: 'Mascot',
                            store: searchEngineStore,
                            typeAhead: true,
                            listeners: {
                                change: function( item, newValue, oldValue, eOpts ){
                                    if(oldValue){
                                        var searchEnginePanelLength = searchEnginePanel.items.length
                                        if(searchEnginePanelLength != 1)
                                            searchEnginePanel.remove(searchEnginePanel.items.items[searchEnginePanelLength - 1])
                                    }
                                    if(newValue){
                                        switch(newValue){
                                            case 'Mascot':{
                                                var mascotPanel = Ext.create('Ext.form.FieldSet',{
                                                    xtype: 'fieldset',
                                                    width: 1000,
                                                    title: 'Mascot Options',
                                                    bodyPadding: 10,
                                                    defaults: {
                                                        labelWidth: 120,
                                                        labelAlign: 'left',
                                                        editable: false,
                                                        msgTarget: 'side',
                                                    },
                                                    
                                                    items:[{
                                                        xtype: 'fieldcontainer',
                                                        layout: {
                                                            type: 'hbox',
                                                            align: 'stretch'
                                                        },
                                                        defaults: {
                                                            labelWidth: 170,
                                                            editable: false,
                                                            msgTarget: 'side',
                                                            margin: '0 0 0 20',
                                                        },
                                                        items:[{
                                                            xtype: 'combo',
                                                            fieldLabel: 'Missed Cleavages Allowed',
                                                            name: 'missedCleavagesAllowed',
                                                            id: 'aabbcc',
                                                            store: Ext.create('Ext.data.Store', {
                                                                proxy: {
                                                                    type: 'ajax',
                                                                    url: '/experiments/ajax/display/Mascot_mode_missedCleavagesAllowed/',
                                                                    reader: {
                                                                        type: 'json',
                                                                        root: 'Mascot_mode_missedCleavagesAlloweds'
                                                                    }
                                                                },
                                                                fields: [{
                                                                    name: 'Mascot_mode_missedCleavagesAllowed',
                                                                    type: 'string'
                                                                }],
                                                                autoLoad: true
                                                            }),
                                                            displayField: 'Mascot_mode_missedCleavagesAllowed',
                                                            queryMode: 'local',
                                                            value: '2',
                                                            flex:1
                                                        },{
                                                            xtype: 'combo',
                                                            fieldLabel: 'Enzyme',
                                                            name: 'mascotEnzyme',
                                                            store: Ext.create('Ext.data.Store', {
                                                                proxy: {
                                                                    type: 'ajax',
                                                                    url: '/experiments/ajax/display/Mascot_mode_mascotEnzyme/',
                                                                    reader: {
                                                                        type: 'json',
                                                                        root: 'Mascot_mode_mascotEnzymes'
                                                                    }
                                                                },
                                                                fields: [{
                                                                    name: 'Mascot_mode_mascotEnzyme',
                                                                    type: 'string'
                                                                }],
                                                                autoLoad: true
                                                            }),
                                                            displayField: 'Mascot_mode_mascotEnzyme',
                                                            queryMode: 'local',
                                                            value: 'Trypsin',
                                                            flex:1
                                                        }]
                                                    },{
                                                        xtype: 'fieldcontainer',
                                                        layout: {
                                                            type: 'hbox',
                                                            align: 'stretch'
                                                        },
                                                        defaults: {
                                                            labelWidth: 170,
                                                            editable: false,
                                                            msgTarget: 'side',
                                                            margin: '0 0 0 20',
                                                        },
                                                        items: [{
                                                            xtype: 'combo',
                                                            fieldLabel: 'Peptide Charge',
                                                            name: 'peptideCharge',
                                                            store: Ext.create('Ext.data.Store', {
                                                                proxy: {
                                                                    type: 'ajax',
                                                                    url: '/experiments/ajax/display/Mascot_mode_peptideCharge/',
                                                                    reader: {
                                                                        type: 'json',
                                                                        root: 'Mascot_mode_peptideCharges'
                                                                    }
                                                                },
                                                                fields: [{
                                                                    name: 'Mascot_mode_peptideCharge',
                                                                    type: 'string'
                                                                }],
                                                                autoLoad: true
                                                            }),
                                                            displayField: 'Mascot_mode_peptideCharge',
                                                            queryMode: 'local',
                                                            value: '2+, 3+ and 4+',
                                                            flex: 1
                                                        }, {
                                                            xtype: 'combo',
                                                            fieldLabel: 'Precursor Search Type',
                                                            name: 'precursorSearchType',
                                                            store: Ext.create('Ext.data.Store', {
                                                                proxy: {
                                                                    type: 'ajax',
                                                                    url: '/experiments/ajax/display/Mascot_mode_precursorSearchType/',
                                                                    reader: {
                                                                        type: 'json',
                                                                        root: 'Mascot_mode_precursorSearchTypes'
                                                                    }
                                                                },
                                                                fields: [{
                                                                    name: 'Mascot_mode_precursorSearchType',
                                                                    type: 'string'
                                                                }],
                                                                autoLoad: true
                                                            }),
                                                            displayField: 'Mascot_mode_precursorSearchType',
                                                            queryMode: 'local',
                                                            value: 'Monoisotopic',
                                                            flex: 1
                                                        }]
                                                    }]
                                                })
                                                searchEnginePanel.insert(1,mascotPanel)
                                                break
                                            }
                                            case 'X!Tandem':{
                                                var xtandemPanel = Ext.create('Ext.form.FieldSet',{
                                                    xtype: 'fieldset',
                                                    width: 1000,
                                                    title: 'X!Tandem Options',
                                                    bodyPadding: 10,
                                                    defaults: {
                                                        labelWidth: 120,
                                                        labelAlign: 'left',
                                                        editable: false,
                                                        msgTarget: 'side',
                                                    },
                                                    items:[{
                                                        xtype: 'fieldcontainer',
                                                        layout: {
                                                            type: 'hbox',
                                                            align: 'stretch'
                                                        },
                                                        defaults: {
                                                            labelWidth: 170,
                                                            editable: false,
                                                            msgTarget: 'side',
                                                            margin: '0 0 0 20',
                                                        },
                                                        items:[{
                                                            xtype: 'combo',
                                                            fieldLabel: 'Fragmentation Method',
                                                            name: 'fragmentationMethod',
                                                            store: Ext.create('Ext.data.Store', {
                                                                fields: [{
                                                                    name: 'fragmentationMethod',
                                                                    type: 'string'
                                                                }],
                                                                data: [
                                                                    {'fragmentationMethod':'CID/HCD/QTOF'},
                                                                    {'fragmentationMethod':'ETD'}
                                                                ],
                                                                autoLoad: true
                                                            }),
                                                            displayField: 'fragmentationMethod',
                                                            queryMode: 'local',
                                                            value: 'CID/HCD/QTOF',
                                                            flex:1
                                                        },{
                                                            xtype: 'combo',
                                                            fieldLabel: 'Cysteine Protecting Group',
                                                            name: 'cysteineProtectingGroup',
                                                            store: Ext.create('Ext.data.Store', {
                                                                fields: [{
                                                                    name: 'cysteineProtectingGroup',
                                                                    type: 'string'
                                                                }],
                                                                data: [
                                                                    {'cysteineProtectingGroup':'Carbamidomethylation (+57)'},
                                                                    {'cysteineProtectingGroup':'Carboxymethylation (+58)'},
                                                                    {'cysteineProtectingGroup':'NIPIA/NIPCAM (+99)'},
                                                                    {'cysteineProtectingGroup':'None'}
                                                                ],
                                                                autoLoad: true
                                                            }),
                                                            displayField: 'cysteineProtectingGroup',
                                                            queryMode: 'local',
                                                            value: 'Carbamidomethylation (+57)',
                                                            flex:1
                                                        }]
                                                    },{
                                                        xtype: 'fieldcontainer',
                                                        layout: {
                                                            type: 'hbox',
                                                            align: 'stretch'
                                                        },
                                                        defaults: {
                                                            labelWidth: 170,
                                                            editable: false,
                                                            msgTarget: 'side',
                                                            margin: '0 0 0 20',
                                                        },
                                                        items: [{
                                                            xtype: 'combo',
                                                            fieldLabel: 'Protease',
                                                            name: 'protease',
                                                            store: Ext.create('Ext.data.Store', {
                                                                fields: [{
                                                                    name: 'protease',
                                                                    type: 'string'
                                                                }],
                                                                data: [
                                                                    {'protease':'Trypsin'},
                                                                    {'protease':'Chymotrypsin'},
                                                                    {'protease':'Lys-C'},
                                                                    {'protease':'Lys-N'},
                                                                    {'protease':'Arg-C'},
                                                                    {'protease':'Glu-C'},
                                                                    {'protease':'Asp-N'},
                                                                    {'protease':'None'},
                                                                ],
                                                                autoLoad: true
                                                            }),
                                                            displayField: 'protease',
                                                            queryMode: 'local',
                                                            value: 'Trypsin',
                                                            flex: 1
                                                        }, {
                                                            xtype: 'combo',
                                                            fieldLabel: 'Number of Allowed 13C',
                                                            name: 'numberOfAllowed13C',
                                                            store: Ext.create('Ext.data.Store', {
                                                                fields: [{
                                                                    name: 'numberOfAllowed13C',
                                                                    type: 'string'
                                                                }],
                                                                data: [
                                                                    {'numberOfAllowed13C': 0},
                                                                    {'numberOfAllowed13C': 1}
                                                                ],
                                                                autoLoad: true
                                                            }),
                                                            displayField: 'numberOfAllowed13C',
                                                            queryMode: 'local',
                                                            value: 1,
                                                            flex: 1
                                                        }]
                                                    }]
                                                })
                                                searchEnginePanel.insert(1,xtandemPanel)
                                                break
                                            }
                                            default:{
                                                Ext.Msg.alert('','Coming soon...')
                                            }
                                        }
                                    }
                                }
                            }
                        },{
                            xtype: 'fieldset',
                            width: 1000,
                            title: 'Mascot Options',
                            bodyPadding: 10,
                            defaults: {
                                labelWidth: 120,
                                labelAlign: 'left',
                                editable: false,
                                msgTarget: 'side',
                            },
                            
                            items:[{
                                xtype: 'fieldcontainer',
                                layout: {
                                    type: 'hbox',
                                    align: 'stretch'
                                },
                                defaults: {
                                    labelWidth: 170,
                                    editable: false,
                                    msgTarget: 'side',
                                    margin: '0 0 0 20',
                                },
                                items:[{
                                    xtype: 'combo',
                                    fieldLabel: 'Missed Cleavages Allowed',
                                    name: 'missedCleavagesAllowed',
                                    id: 'aabbcc',
                                    store: Ext.create('Ext.data.Store', {
                                        proxy: {
                                            type: 'ajax',
                                            url: '/experiments/ajax/display/Mascot_mode_missedCleavagesAllowed/',
                                            reader: {
                                                type: 'json',
                                                root: 'Mascot_mode_missedCleavagesAlloweds'
                                            }
                                        },
                                        fields: [{
                                            name: 'Mascot_mode_missedCleavagesAllowed',
                                            type: 'string'
                                        }],
                                        autoLoad: true
                                    }),
                                    displayField: 'Mascot_mode_missedCleavagesAllowed',
                                    queryMode: 'local',
                                    value: '2',
                                    flex:1
                                },{
                                    xtype: 'combo',
                                    fieldLabel: 'Enzyme',
                                    name: 'mascotEnzyme',
                                    store: Ext.create('Ext.data.Store', {
                                        proxy: {
                                            type: 'ajax',
                                            url: '/experiments/ajax/display/Mascot_mode_mascotEnzyme/',
                                            reader: {
                                                type: 'json',
                                                root: 'Mascot_mode_mascotEnzymes'
                                            }
                                        },
                                        fields: [{
                                            name: 'Mascot_mode_mascotEnzyme',
                                            type: 'string'
                                        }],
                                        autoLoad: true
                                    }),
                                    displayField: 'Mascot_mode_mascotEnzyme',
                                    queryMode: 'local',
                                    value: 'Trypsin',
                                    flex:1
                                }]
                            },{
                                xtype: 'fieldcontainer',
                                layout: {
                                    type: 'hbox',
                                    align: 'stretch'
                                },
                                defaults: {
                                    labelWidth: 170,
                                    editable: false,
                                    msgTarget: 'side',
                                    margin: '0 0 0 20',
                                },
                                items: [{
                                    xtype: 'combo',
                                    fieldLabel: 'Peptide Charge',
                                    name: 'peptideCharge',
                                    store: Ext.create('Ext.data.Store', {
                                        proxy: {
                                            type: 'ajax',
                                            url: '/experiments/ajax/display/Mascot_mode_peptideCharge/',
                                            reader: {
                                                type: 'json',
                                                root: 'Mascot_mode_peptideCharges'
                                            }
                                        },
                                        fields: [{
                                            name: 'Mascot_mode_peptideCharge',
                                            type: 'string'
                                        }],
                                        autoLoad: true
                                    }),
                                    displayField: 'Mascot_mode_peptideCharge',
                                    queryMode: 'local',
                                    value: '2+, 3+ and 4+',
                                    flex: 1
                                }, {
                                    xtype: 'combo',
                                    fieldLabel: 'Precursor Search Type',
                                    name: 'precursorSearchType',
                                    store: Ext.create('Ext.data.Store', {
                                        proxy: {
                                            type: 'ajax',
                                            url: '/experiments/ajax/display/Mascot_mode_precursorSearchType/',
                                            reader: {
                                                type: 'json',
                                                root: 'Mascot_mode_precursorSearchTypes'
                                            }
                                        },
                                        fields: [{
                                            name: 'Mascot_mode_precursorSearchType',
                                            type: 'string'
                                        }],
                                        autoLoad: true
                                    }),
                                    displayField: 'Mascot_mode_precursorSearchType',
                                    queryMode: 'local',
                                    value: 'Monoisotopic',
                                    flex: 1
                                }]
                            }]
                        }]
                    });

					// instrument related information
					var instrumentPanel = Ext.create('Ext.panel.Panel', {
								title : 'SearchDatabase-Parameter',
								border : true,
								// frame : true,
								headerPosition : 'top',
								bodyPadding : 10,
								defaults : {
									labelWidth : 120,
									labelAlign : 'left',
									width : 1000,
									allowBlank : false,
									editable : false,
									msgTarget : 'side'
									// afterLabelTextTpl : required
								},
								items : [{
			                                xtype: 'fieldcontainer',
			                                layout: {
			                                    type: 'hbox',
			                                    align: 'stretch'
			                                },
			                                defaults: {
			                                    editable: false,
			                                    allowBlank: false,
			                                    msgTarget: 'side',
			                                    // afterLabelTextTpl: required
			                                },
			                                items: [{
			                                    width: 450,
			                                    xtype: 'combobox',
			                                    id: 'searchdatabase',
			                                    fieldLabel: 'Search database',
			                                    labelWidth: 120,
			                                    name: 'Search_database',
			                                    queryMode: 'local',
			                                    displayField: 'Search_database',
			                                    store: searchDatabaseStore
			                                },{
			                                    xtype: 'button',
			                                    text: 'Other database',
			                                    margin: '0 0 0 5',
			                                    handler: function(){
			                                        var uploadWindow = Ext.create('Ext.window.Window',{
			                                            width: 400,
			                                            height: 300,
			                                            autoShow: true,
			                                            modal: true,
			                                            title: 'Upload FASTA file',
			                                            layout: 'anchor',
			                                            items:[{
			                                                xtype: 'form',
			                                                id: 'upload_form',
			                                                anchor: '100% 100%',
			                                                margin: '10 10 10 10',
			                                                border: 0,
			                                                defaults: {
			                                                    allowBlank: false,
			                                                    msgTarget: 'side',
			                                                    // afterLabelTextTpl: required,
			                                                    labelWidth: 120,
			                                                },
			                                                dockedItems: [{
			                                                    xtype: 'toolbar',
			                                                    dock: 'bottom',
			                                                    layout: {
			                                                        pack: 'center',
			                                                        align: 'middle'
			                                                    },
			                                                    items: [{
			                                                        xtype: 'button',
			                                                        text: 'Submit',
			                                                        handler: function(){
			                                                            formpanel = Ext.getCmp('upload_form');
			                                                            var form = formpanel.getForm();
			                                                            if (form.isValid()) {
			                                                                Ext.Ajax.timeout = 180000;
			                                                                form.submit({
			                                                                    url: '/experiments/save/upload/',
			                                                                    waitMsg: 'Uploading FASTA file...',
			                                                                    //timeout : 300000,
			                                                                    // standardSubmit : true
			                                                                    success: function(frm, act) {
			                                                                        // val = String(act.result.msg);
			                                                                        // len = val.legnth
			                                                                        // // console.log(len)
			                                                                        // // val=val.substring(1)
			                                                                        // if (val.length < 6) {
			                                                                        //     for (i = val.length; i < 6; i++)
			                                                                        //         val = '0' + val
			                                                                        // }
			                                                                        var text = act.response.responseText
			                                                                        var fastaLibName = Ext.JSON.decode(text).fastaLibName
			                                                                        Ext.getCmp('searchdatabase').setValue(fastaLibName)
			                                                                        Ext.Msg.alert('Success', 'Upload finished.');
			                                                                        searchDatabaseStore.load()
			                                                                        uploadWindow.close()
			                                                                    },
			                                                                    failure: function(form, action) {
			                                                                        Ext.Msg.alert('Failed', 'Upload failed. Contact admin.');
			                                                                    }
			                                                                })
			                                                            }
			                                                        }
			                                                    }, {
			                                                        xtype: 'button',
			                                                        text: 'Cancel',
			                                                        handler: function(){
			                                                            formpanel = Ext.getCmp('upload_form');
			                                                            formpanel.getForm().reset();
			                                                        }
			                                                    }]
			                                                }],
			                                                items:[{
			                                                    xtype: 'textfield',
			                                                    fieldLabel: 'Species',
			                                                    name: 'upload_species'
			                                                },{
			                                                    xtype: 'combo',
			                                                    fieldLabel: 'Data source',
			                                                    name: 'upload_datasource',
			                                                    displayField: 'name',
			                                                    editable: false,
			                                                    store: Ext.create('Ext.data.Store', {
			                                                        fields: ['name'],
			                                                        data : [
			                                                            {"name":"UniProt"},
			                                                            {"name":"RefSeq"},
			                                                            // {"name":"Arizona"}
			                                                            ],
			                                                        autoLoad: true
			                                                    })
			                                                },{
			                                                    xtype: 'datefield',
			                                                    fieldLabel: 'Version date',
			                                                    name: 'upload_date',
			                                                    width: '200',
			                                                    editable: false,
			                                                },{
			                                                    width: 350,
			                                                    xtype: 'filefield',
			                                                    name: 'upload_file',
			                                                    fieldLabel: 'FASTA file',
			                                                    buttonText: 'Browse',
			                                                    emptyText: 'File path'
			                                                },{
			                                                    xtype: 'hiddenfield',
			                                                    name: 'upload_timestamp',
			                                                    value: timestamp
			                                                }]
			                                            }]
			                                        })
			                                    }                               
			                                }]
			                            }, {
											width : 450,
											xtype : 'combobox',
											fieldLabel : 'Manufacturer',
											name : 'Instrument_manufacturer',
											displayField : 'Instrument_manufacturer',
											store : instrumentManufacturerStore
										}, {
											width : 450,
											xtype : 'combobox',
											fieldLabel : 'Instrument',
											name : 'Instrument_name',
											id : "Instrument_name" + timestamp,
											displayField : 'Instrument',
											store : instrumentStore,
											typeAhead : true,
											listeners : {
												select : {
													fn : function(combo, records, index) {
														var ms1 = Ext.getCmp("instrument_MS1" + timestamp);
														// console.log(lab)
														ms1.clearValue();
														ms1.store.load({
																	params : {
																		id : records[0].data.Instrument
																	}
																});
														
														// ms1.setValue(ms1.store.data.items[0].data.Instrument_MS1)
														var ms2 = Ext.getCmp("instrument_MS2" + timestamp);
														ms2.clearValue();
														// console.log(records[0].data)
														ms2.store.load({
																	params : {
																		id : records[0].data.Instrument
																	}
																});
														
														//intrusments = Ext.getCmp("Instrument_name" + timestamp);
														//intrusments_id = intrusments.lastValue;
														//console.log("intrusments_id:" + intrusments_id);
													}
												}
											}
										}, {
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											defaults : {
												editable : false,
												allowBlank : false,
												msgTarget : 'side'
												// afterLabelTextTpl : required
											},
											items : [{
														xtype : 'combobox',
														fieldLabel : 'Details',
														name : 'instrument_MS1',
														displayField : 'Instrument_MS1',
														emptyText : 'MS1',
														store : MS1Store,
														queryMode : 'local',
														id : 'instrument_MS1' + timestamp,
														labelWidth : 120,
														width : 300,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	var tol = Ext.getCmp("instrument_MS1_tol" + timestamp);
																	tol.clearValue();
																	tol.store.load({
																				params : {
																					id : records[0].data.Instrument_MS1
																				}
																			});
																	// tol.setValue(tol.store.data.items[0].data.Instrument_MS1_tol)
//																	if(combo.value=="Orbitrap" || combo.value=="TOF"){
//						                                                combobox_instrument_MS1_tol_unit = Ext.getCmp("instrument_MS1_tol_unit"+timestamp);
//						                                                combobox_instrument_MS1_tol_unit.setValue("ppm");
//						                                            }
//						                                            if(combo.value=="Ion Trap"){
//						                                                combobox_instrument_MS1_tol_unit = Ext.getCmp("instrument_MS1_tol_unit"+timestamp);
//						                                                combobox_instrument_MS1_tol_unit.setValue("Da");
//						                                            }
																}
															}
														}
													}, {
														xtype : 'combobox',
														name : 'instrument_MS1_tol',
														displayField : 'Instrument_MS1_tol',
														id : 'instrument_MS1_tol' + timestamp,
														store : MS1tolStore,
														queryMode : 'local',
														emptyText : 'Precursor Mass Tolerance',
														width : 195,
														editable : true
													}, 
													{
						                                xtype: 'combobox',
						                                name: 'instrument_MS1_tol_unit',
						                                displayField: 'Instrument_MS1_tol_unit',
						                                id: 'instrument_MS1_tol_unit' + timestamp,
						                                store: ["ppm", "Da"],
						                                queryMode: 'local',
						                                emptyText: 'unit',
						                                width: 70
						                            },
						                            
													{
														xtype : 'combobox',
														name : 'instrument_MS2',
														id : 'instrument_MS2' + timestamp,
														displayField : 'Instrument_MS2',
														emptyText : 'MS2',
														store : MS2Store,
														queryMode : 'local',
														width : 150,
														padding: '0, 0, 0, 20',
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	// console.log(records[0].data)
																	var lab = Ext.getCmp("instrument_MS2_tol" + timestamp);
																	lab.clearValue();
																	lab.store.load({
																				params : {
																					id : records[0].data.Instrument_MS2
																				}
																			});
//																	combobox_instrument_MS2_tol_unit = Ext.getCmp("instrument_MS2_tol_unit" + timestamp);
//						                                            combobox_instrument_MS2_tol_unit.setValue("Da");
																}
															}
														}
													}, {
														xtype : 'combobox',
														name : 'instrument_MS2_tol',
														id : 'instrument_MS2_tol' + timestamp,
														displayField : 'Instrument_MS2_tol',
														store : MS2tolStore,
														emptyText : 'Fragment Mass Tolerance',
														queryMode : 'local',
														width : 195,
														editable : true
													},
													{
						                                xtype: 'combobox',
						                                name: 'instrument_MS2_tol_unit',
						                                id: 'instrument_MS2_tol_unit' + timestamp,
						                                displayField: 'Instrument_MS2_tol_unit',
						                                store: ["ppm", "Da"],
						                                queryMode: 'local',
						                                emptyText: 'Unit',
						                                width: 70
						                            }]
										}, {
											xtype : 'combobox',
											fieldLabel : 'Fixed Modifications',
											afterLabelTextTpl : '',
											name : 'Fixed_Modification',
											displayField : 'Fixed_Modification',
											emptyText : '',
											store : fixedModificationStore,
											multiSelect : true,
											queryMode : 'local',
											labelWidth : 120,
											allowBlank : true
											// listeners : {
										// boxready : function(combo, eOpts) {
										// var tempvalue = [];
										// tempvalue.push('DeStreak (C)')
										// tempvalue.push('Acetyl (Protein
										// N-term)')
										// tempvalue.push('Oxidation (M)')
										// combo.setValue(tempvalue);
										// }
										// }
									}	, {
											xtype : 'combobox',
											name : 'Dynamic_Modification',
											fieldLabel : 'Dynamic Modifications',
											afterLabelTextTpl : '',
											multiSelect : true,
											displayField : 'Dynamic_Modification',
											store : dynamicModificationStore,
											emptyText : '',
											allowBlank : true
										}, {
			                                xtype: 'button',
			                                text: 'Add new modification',
			                                margin: '0 0 15 0',
			                                width: 180,
			                                handler: function(){
			                                    var compositionDict = new Array()
			                                    var specificityText = ""
			                                    var newModificationWindow = Ext.create('Ext.window.Window',{
			                                        width: 540,
			                                        height: 510,
			                                        autoShow: true,
			                                        modal: true,
			                                        title: 'Add new modification',
			                                        layout: 'anchor',
			                                        items:[{
			                                            xtype: 'form',
			                                            id: 'add_new_modification',
			                                            anchor: '100% 100%',
			                                            margin: '15 10 10 10',
			                                            border: 0,
			                                            defaults: {
			                                                allowBlank: false,
			                                                msgTarget: 'side',
			                                                // afterLabelTextTpl: required,
			                                                labelWidth: 120,
			                                                width: 500
			                                            },
			                                            dockedItems: [{
			                                                xtype: 'toolbar',
			                                                dock: 'bottom',
			                                                layout: {
			                                                    pack: 'center',
			                                                    align: 'middle'
			                                                },
			                                                items: [{
			                                                    xtype: 'button',
			                                                    text: 'Submit',
			                                                    handler: function(){
			                                                        formpanel = Ext.getCmp('add_new_modification')
			                                                        var form = formpanel.getForm()
			                                                        var submitDate = new Date
			                                                        formpanel.items.items[5].setValue(Ext.Date.format(submitDate, 'd/m/Y')) 
			                                                        if (formpanel.items.items[2].items.items[0].value == ''){
			                                                            Ext.Msg.alert('Warning','Composition cannot be empty.')
			                                                        }
			                                                        else if (formpanel.items.items[3].items.items[4].value == ''){
			                                                            Ext.Msg.alert('Warning','Specificity cannot be empty.')
			                                                        }
			                                                        else if (form.isValid()) {
			                                                            Ext.Ajax.timeout = 180000;
			                                                            form.submit({
			                                                                url: '/experiments/save/new_modification/',
			                                                                waitMsg: 'Adding new modification...',
			                                                                //timeout : 300000,
			                                                                // standardSubmit : true
			                                                                success: function(frm, act) {
			                                                                    // val = String(act.result.msg);
			                                                                    // len = val.legnth
			                                                                    // // console.log(len)
			                                                                    // // val=val.substring(1)
			                                                                    // if (val.length < 6) {
			                                                                    //     for (i = val.length; i < 6; i++)
			                                                                    //         val = '0' + val
			                                                                    // }
			                                                                    Ext.Msg.alert('Success', 'New modification is added.');
			                                                                    dynamicModificationStore.load()
			                                                                    fixedModificationStore.load()
			                                                                },
			                                                                failure: function(form, action) {
			                                                                    Ext.Msg.alert('Failed', 'Failed to add new modification. Contact admin.');
			                                                                }
			                                                            })
			                                                        }
			                                                    }
			                                                }, {
			                                                    xtype: 'button',
			                                                    text: 'Reset',
			                                                    handler: function(){
			                                                        var formpanel = Ext.getCmp('add_new_modification');
			                                                        formpanel.getForm().reset();
			                                                        compositionDict = new Array()
			                                                        specificityText = ''
			                                                        this.up().up().items.items[3].items.items[0].store.removeAll()
			                                                        // console.log(compositionDict)
			                                                    }
			                                                }]
			                                            }],
			                                            items:[{
			                                                xtype: 'textfield',
			                                                fieldLabel: 'Title',
			                                                name: 'new_modi_title',
			                                                width: 450
			                                            },{
			                                                xtype: 'textfield',
			                                                fieldLabel: 'Fullname',
			                                                name: 'new_modi_fullname',
			                                                width: 450
			                                            },{
			                                                xtype: 'fieldset',
			                                                width: 500,
			                                                title: 'Delta',
			                                                bodyPadding: 10,
			                                                defaults: {
			                                                    labelWidth: 120,
			                                                    labelAlign: 'left',
			                                                    editable: false,
			                                                    msgTarget: 'side',
			                                                },
			                                                items: [{
			                                                    xtype: 'displayfield',
			                                                    fieldLabel: 'Composition',
			                                                    submitValue: true,
			                                                    width: 370,
			                                                    name: 'new_modi_composition',
			                                                    value: '',
			                                                    // msgTarget: 'side',
			                                                    // afterLabelTextTpl: required,
			                                                },{
			                                                    xtype: 'fieldcontainer',
			                                                    layout: {
			                                                        type: 'hbox',
			                                                        align: 'stretch'
			                                                    },
			                                                    defaults: {
			                                                        editable: false,
			                                                    },
			                                                    items: [{
			                                                        xtype: 'combobox',
			                                                        submitValue: false,
			                                                        fieldLabel: 'Symbols',
			                                                        width: 235,
			                                                        labelWidth: 120,
			                                                        value: '13C',
			                                                        displayField: 'name',
			                                                        store: Ext.create('Ext.data.Store', {
			                                                            fields: ['name'],
			                                                            data : [
			                                                                {'name':"13C"},{'name':"15N"},{'name':"18O"},{'name':"2H"},{'name':"Ac"},{'name':"Ag"},{'name':"As"},{'name':"Au"},{'name':"B"},
			                                                                {'name':"Br"},{'name':"C"},{'name':"Ca"},{'name':"Cd"},{'name':"Cl"},{'name':"Co"},{'name':"Cr"},{'name':"Cu"},{'name':"dHex"},
			                                                                {'name':"F"},{'name':"Fe"},{'name':"H"},{'name':"Hep"},{'name':"Hex"},{'name':"HexA"},{'name':"HexNAc"},{'name':"Hg"},
			                                                                {'name':"I"},{'name':"K"},{'name':"Kdn"},{'name':"Kdo"},{'name':"Li"},{'name':"Me"},{'name':"Mg"},{'name':"Mn"},
			                                                                {'name':"Mo"},{'name':"N"},{'name':"Na"},{'name':"NeuAc"},{'name':"NeuGc"},{'name':"Ni"},{'name':"O"},{'name':"P"},
			                                                                {'name':"Pd"},{'name':"Pent"},{'name':"Phos"},{'name':"S"},{'name':"Se"},{'name':"Sulf"},{'name':"Water"},{'name':"Zn"}
			                                                                ],
			                                                            autoLoad: true
			                                                        })
			                                                    },{
			                                                        xtype: 'combobox',
			                                                        submitValue: false,
			                                                        width: 100,
			                                                        value: '1',
			                                                        margin: '0 0 0 5',
			                                                        displayField: 'name',
			                                                        store: Ext.create('Ext.data.Store', {
			                                                            fields: ['name'],
			                                                            data : [
			                                                                {'name':"-10"},{'name':"-9"},{'name':"-8"},{'name':"-7"},{'name':"-6"},{'name':"-5"},{'name':"-4"},{'name':"-3"},{'name':"-2"},{'name':"-1"},
			                                                                {'name':"1"},{'name':"2"},{'name':"3"},{'name':"4"},{'name':"5"},{'name':"6"},{'name':"7"},{'name':"8"},{'name':"9"},{'name':"10"}
			                                                                ],
			                                                            autoLoad: true
			                                                        })
			                                                    },{
			                                                        xtype: 'button',
			                                                        text: 'Add',
			                                                        margin: '0 0 0 5',
			                                                        width: 60,
			                                                        handler: function(){
			                                                            var valueSymbol1 = this.up().items.items[0].value
			                                                            var valueSymbol2 = parseInt(this.up().items.items[1].value)
			                                                            if(compositionDict[valueSymbol1]){
			                                                                compositionDict[valueSymbol1] += valueSymbol2
			                                                                if(compositionDict[valueSymbol1] == 0)
			                                                                    delete compositionDict[valueSymbol1]
			                                                            }else{
			                                                                compositionDict[valueSymbol1] = valueSymbol2
			                                                            }

			                                                            var compositionText = "";
			                                                            for (var key in compositionDict) {
			                                                                if(!isNaN(compositionDict[key])){
			                                                                    if (compositionText == "") {
			                                                                        compositionText = key + '(' + compositionDict[key] + ')';
			                                                                    }
			                                                                    else {
			                                                                        compositionText += " " + key + '(' + compositionDict[key] + ')';
			                                                                    }
			                                                                } 
			                                                            }
			                                                            console.log(compositionText)
			                                                            this.up().up().items.items[0].setValue(compositionText)
			                                                        }
			                                                    }]
			                                                }]
			                                            },{
			                                                xtype: 'fieldset',
			                                                width: 500,
			                                                title: 'Specificity',
			                                                bodyPadding: 10,
			                                                defaults: {
			                                                    allowBlank: false,
			                                                    msgTarget: 'side',
			                                                    // afterLabelTextTpl: required,
			                                                    labelWidth: 120,
			                                                    labelAlign: 'left',
			                                                    editable: false,
			                                                    msgTarget: 'side',
			                                                },
			                                                items: [{
			                                                    xtype: 'grid',
			                                                    height: 100,
			                                                    margin: '0 0 5 0',
			                                                    columns: [
			                                                        { text: 'Site',  dataIndex: 'site', flex: 2 },
			                                                        { text: 'Position', dataIndex: 'position', flex: 2 },
			                                                        { text: 'Classification', dataIndex: 'classification', flex: 3 }
			                                                    ],
			                                                    store: Ext.create('Ext.data.Store', {
			                                                        fields: ['site','position','classification'],
			                                                        data : [
			                                                        ],
			                                                        autoLoad: true
			                                                    })
			                                                },{
			                                                    xtype: 'combo',
			                                                    fieldLabel: 'Site',
			                                                    submitValue: false,
			                                                    editable: false,
			                                                    displayField: 'name',
			                                                    value: 'A',
			                                                    store: Ext.create('Ext.data.Store', {
			                                                        fields: ['name'],
			                                                        data : [
			                                                            {'name':"A"},{'name':"R"},{'name':"N"},{'name':"D"},{'name':"C"},{'name':"E"},{'name':"Q"},{'name':"G"},{'name':"H"},
			                                                            {'name':"I"},{'name':"L"},{'name':"K"},{'name':"M"},{'name':"F"},{'name':"P"},{'name':"S"},{'name':"T"},{'name':"W"},
			                                                            {'name':"Y"},{'name':"V"},{'name':"N-term"},{'name':"C-term"},{'name':"U"},{'name':"O"},{'name':"J"}
			                                                            ],
			                                                        autoLoad: true
			                                                    })
			                                                },{
			                                                    xtype: 'combo',
			                                                    fieldLabel: 'Position',
			                                                    submitValue: false,
			                                                    editable: false,
			                                                    value: 'Anywhere',
			                                                    displayField: 'name',
			                                                    store: Ext.create('Ext.data.Store', {
			                                                        fields: ['name'],
			                                                        data : [
			                                                            {'name':"Anywhere"},{'name':"Any N-term"},{'name':"Any C-term"},{'name':"Protein N-term"},{'name':"Protein C-term"}
			                                                            ],
			                                                        autoLoad: true
			                                                    })
			                                                },{
			                                                    xtype: 'combo',
			                                                    fieldLabel: 'Classification',
			                                                    submitValue: false,
			                                                    editable: false,
			                                                    displayField: 'name',
			                                                    value: 'Post-translational',
			                                                    store: Ext.create('Ext.data.Store', {
			                                                        fields: ['name'],
			                                                        data : [
			                                                            {'name':"Post-translational"},{'name':"Co-translational"},{'name':"Pre-translational"},{'name':"Chemical derivative"},{'name':"Artefact"},
			                                                            {'name':"N-linked glycosylation"},{'name':"O-linked glycosylation"},{'name':"Other glycosylation"},{'name':"Synth. pep. protect. gp."},
			                                                            {'name':"Isotopic label"},{'name':"Non-standard residue"},{'name':"Multiple"},{'name':"Other"},{'name':"AA substitution"}
			                                                            ],
			                                                        autoLoad: true
			                                                    })
			                                                },{
			                                                    xtype: 'hiddenfield',
			                                                    name: 'new_modi_specificity',
			                                                    value: '',
			                                                },{
			                                                    xtype: 'button',
			                                                    text: 'Add',
			                                                    margin: '0 0 5 0',
			                                                    width: 60,
			                                                    handler: function(){
			                                                        var valueSymbol1 = this.up().items.items[1].value
			                                                        var valueSymbol2 = this.up().items.items[2].value
			                                                        var valueSymbol3 = this.up().items.items[3].value
			                                                        this.up().items.items[0].store.add({'site':valueSymbol1,'position':valueSymbol2,'classification':valueSymbol3})
			                                                        if(specificityText != ''){
			                                                            specificityText += ';'
			                                                        }
			                                                        specificityText += valueSymbol1 + ',' + valueSymbol2 + ',' + valueSymbol3
			                                                        console.log(specificityText)
			                                                        this.up().items.items[4].setValue(specificityText)
			                                                    }
			                                                }]
			                                            },{
			                                                xtype: 'hiddenfield',
			                                                name: 'upload_timestamp',
			                                                value: timestamp
			                                            },{
			                                                xtype: 'hiddenfield',
			                                                name: 'new_modi_addtime',
			                                                value: new Date
			                                            }]
			                                        }]
			                                    })
			                                }                               
			                            }, {
											xtype : 'numberfield',
											fieldLabel : 'Repeat Number',
											name : 'repeat',
											minValue : 1,
											editable : true,
											width : 240
										}, {
											xtype : 'numberfield',
											fieldLabel : 'Fraction Number',
											name : 'fraction',
											minValue : 1,
											editable : true,
											width : 240
										},{
			                                xtype: 'combobox',
			                                name: 'quantificationMethods',
			                                fieldLabel: 'Quantification Method',
			                                afterLabelTextTpl: '',
			                                displayField: 'quantificationMethod',
			                                store: quantificationMethodsStore,
			                                emptyText: '',
			                                allowBlank: false,
			                                width: 450,
			                                // afterLabelTextTpl: required,
			                            },{
			                                xtype: 'fieldcontainer',
			                                layout: {
			                                    type: 'hbox',
			                                    align: 'stretch'
			                                },
			                                defaults: {
			                                    labelWidth: 170,
			                                    editable: false,
			                                    msgTarget: 'side',
			                                },
			                                items:[{
			                                    xtype: 'radiofield',
			                                    name: 'addexperimentFdr',
			                                    inputValue: 'Protein-Level FDR',
			                                    fieldLabel: '',
			                                    checked: true,
			                                    labelWidth: 0,
			                                    width: 155,
			                                    labelSeparator: '',
			                                    hideEmptyLabel: false,
			                                    boxLabel: 'Protein-Level FDR',
			                                    // afterLabelTextTpl: required,
			                                    listeners:{
			                                        change: function( item, newValue, oldValue, eOpts ){
			                                            if(newValue==true){
			                                                item.up().down('numberfield').show()
			                                            }else{
			                                                item.up().down('numberfield').hide()
			                                            }
			                                        }
			                                    }
			                                },{
			                                    xtype: 'numberfield',
			                                    name: 'addexperimentProteinFdrValue',
			                                    fieldLabel: '',
			                                    // hidden: true,
			                                    margin: '0 0 0 20',
			                                    editable: true,
			                                    value: 0.01,
			                                    minValue: 0.01,
			                                    step: 0.01,
			                                    maxValue: 1
			                                }]
			                            }]
							});
					var commentPanel = Ext.create('Ext.panel.Panel', {
								title : 'Comment',
								// frame : true,
								headerPosition : 'top',
								bodyPadding : 10,
								defaults : {
									labelWidth : 120,
									labelAlign : 'top',
									width : 600,
									allowBlank : true
								},
								items : [{
											xtype : 'textfield',
											fieldLabel : 'Ispec No.',
											name : 'ispecno',
											labelAlign : 'left'
										},
										// {
										// xtype : 'textareafield',
										// fieldLabel : 'Experiment
										// Description',
										// name : 'description'
										// },
										{
											xtype : 'textareafield',
											fieldLabel : 'Experiment Comments/Conclusions',
											name : 'comments_conclusions'
										}]
							});
					// button for submit of cancel form
					var buttonPanel = Ext.create('Ext.panel.Panel', {
								// frame : true,
								border : true,
								buttonAlign : "center",
								buttons : [{
											text : 'Submit',
											handler : submitForm
										}, {
											text : 'Cancel',
											handler : cancelForm
										}]
							});
					var formPanel = Ext.create('Ext.form.Panel', {
								id : timestamp,
								// border:true,
								// frame:true,
								// renderTo : 'form',
								overflowY : 'scroll',
								items : [generalPanel, separationPanel, digestPanel, modePanel, searchEnginePanel, instrumentPanel, commentPanel, buttonPanel]
							});
					/*
					 * var win_addexp = new Ext.window.Window({ layout: 'fit',
					 * id:'add_exp_tab', title: 'Add Experiment', resizable
					 * :true, closable: true, maximizable:true,
					 * collapsible:true, height: 600, width: 1100, //draggable: {
					 * constrain: true, constrainTo: Ext.getBody() },
					 * 
					 * items:[formPanel]}); win_addexp.show();
					 */
					tab = Ext.getCmp('content-panel')
					tab.add({
								id : 'edit_exp_tab' + "_metadata",
								title : 'Edit Experiment ' + experiment_id,
								iconCls : 'editexperiment',
								closable : true,
								layout : 'fit',
								items : [formPanel]
							}).show()
				}

				EditExperiment = function(experimentID) {
					// CreateExperimentForm(experimentID);
					Ext.Ajax.request({
								url : '/experiments/loadnew/experiment/',
								// url : '/experiments/load/experiment/',
								params : {
									experiment_no : experimentID
									// csrfmiddlewaretoken : csrftoken
								},
								success : function(response) {
									var text = response.responseText;
									responseJson = Ext.JSON.decode(text).data;
									CreateExperimentForm(experimentID, responseJson);
									
									//load instrusments
									
									var instrument_id = responseJson.Instrusment_name;
									var ms1 = Ext.getCmp("instrument_MS1" + exp_timestamp);
									ms1.store.load({
										params : {
											id : instrument_id
										}
									});

									var ms2 = Ext.getCmp("instrument_MS2" + exp_timestamp);
									ms2.store.load({
										params : {
											id : instrument_id
										}
									});


									var ms1_tol_id = responseJson.instrument_MS1;
									var ms1_tol = Ext.getCmp("instrument_MS1_tol" + exp_timestamp);
									ms1_tol.store.load({
										params : {
											id : ms1_tol_id
										}
									});

									var ms2_tol_id = responseJson.instrument_MS2;
									var ms2_tol = Ext.getCmp("instrument_MS2_tol" + exp_timestamp);
									ms2_tol.store.load({
										params : {
											id : ms2_tol_id
										}
									});
									
									
									Ext.getCmp('edit_exp_tab' + "_metadata").items.items[0].getForm().load({
												url : '/experiments/loadnew/experiment/',
												// url :
												// '/experiments/load/experiment/',
												method : 'POST',
												params : {
													experiment_no : experimentID
												}
											});
									var pre_separation_methods = responseJson.pre_separation_methods;
									var pre_separation_methods_cmp = Ext.getCmp("pre_separation_methods" + exp_timestamp);
									if(pre_separation_methods=="Online"){
										pre_separation_methods_cmp.items.items[0].setValue(true);
									}
									else if(pre_separation_methods=="Offline"){
										pre_separation_methods_cmp.items.items[1].setValue(true);
									}
									else{
										pre_separation_methods_cmp.items.items[2].setValue(true);
									}
									//set pre_separation_methods
									
									
									//id : 'method' + method_order + timestamp
									
									
									// var panel =
									// Ext.create('gar.view.Experiment_detail')

									// console.log(responseJson.experiment_type)
									// Ext.getCmp(responseJson.experiment_type).setValue(true)

									// Pre-Sepration,size--setValue
									/*
									 * var method_num = responseJson.method_num
									 * var id = "" var sepIndex = 1
									 * for(sepIndex; sepIndex<method_num+1;sepIndex++){
									 * id = "method" + sepIndex + exp_timestamp
									 * Ext.getCmp(id).items.items[2].setValue(responseJson.separation_size[sepIndex-1])
									 * id = "" }
									 */

								}
							});

				}

				/** *******************EditExperiment******************** */

				/** *******************EditSample******************** */
				// The code of this part has been encoded in ShowSample.js
				// CreateSampleForm=function(sample_id, response) {
				// var panel = Ext.getCmp('edit_sample_tab');
				// if (panel) {
				// var main = Ext.getCmp("content-panel");
				// main.setActiveTab(panel);
				// return 0;
				// }
				// var timestamp = 'compare' + (new Date()).valueOf()
				// // CSRF protection
				// csrftoken = Ext.util.Cookies.get('csrftoken');
				// var submitForm = function() {
				// formpanel = Ext.getCmp(timestamp);
				// var form = formpanel.getForm();
				// if (form.isValid()) {
				// form.submit({
				// url : '/experiments/editsave/sample/',
				// params : {
				// sample_no : sample_id
				// // csrfmiddlewaretoken : csrftoken
				// },
				// waitMsg : 'Saving Sample......',
				// timeout : 300000,
				// success : function(frm, act) {
				// val = String(act.result.msg);
				// len = val.legnth
				// // console.log(len)
				// // val=val.substring(1)
				// if (val.length < 6) {
				// for (i = val.length; i < 6; i++)
				// val = '0' + val
				// }
				// Ext.Msg.alert('Success', 'Request was successful. Sample No:
				// ' + val);
				// // Ext.Msg.alert('Success', 'Sample
				// // add complete. Sample No: ' +
				// // Ext.encode(act.result.msg));
				// },
				// failure : function(form, action) {
				// Ext.Msg.alert('Failed', 'Sample adding failed.Contact
				// admin.');
				// }
				// })
				// }
				// };
				// var cancelForm = function() {
				// formpanel = Ext.getCmp(timestamp);
				// formpanel.getForm().reset();
				// };
				// // experimenter Model and store
				// var companyStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/all_company/',
				// reader : {
				// type : 'json',
				// root : 'all_company'
				// }
				// },
				// fields : [{
				// name : 'company',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var labStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/all_lab/',
				// reader : {
				// type : 'json',
				// root : 'all_lab'
				// }
				// },
				// fields : [{
				// name : 'lab',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var experimenterStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/all_experimenter/',
				// reader : {
				// type : 'json',
				// root : 'experimenters'
				// }
				// },
				// fields : [{
				// name : 'experimenter',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var sourceTissueTaxonAorMStore = Ext.create('Ext.data.Store',
				// {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/Source_TissueTaxonAorM/',
				// reader : {
				// type : 'json',
				// root : 'Source_TissueTaxonAorM'
				// }
				// },
				// fields : [{
				// name : 'Source_TissueTaxonAorM',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var sourceTissueTaxonIDStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/Source_TissueTaxonID/',
				// reader : {
				// type : 'json',
				// root : 'tissueID'
				// }
				// },
				// fields : [{
				// name : 'tissueID',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var sourceTissueTaxonNameStore = Ext.create('Ext.data.Store',
				// {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/Source_TissueTaxonName/',
				// reader : {
				// type : 'json',
				// root : 'tissueName'
				// }
				// },
				// fields : [{
				// name : 'tissueName',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var geneIDStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Source_TissueTaxonID/',
				// reader : {
				// type : 'json',
				// root : 'Source_TissueTaxonIDs'
				// }
				// },
				// fields : [{
				// name : 'Source_TissueTaxonID',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var SourceTissueSystemStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/Source_TissueSystem/',
				// reader : {
				// type : 'json',
				// root : 'Source_TissueSystem'
				// }
				// },
				// fields : [{
				// name : 'Source_TissueSystem',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var SourceTissueOrganStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/Source_TissueOrgan/',
				// reader : {
				// type : 'json',
				// root : 'Source_TissueOrgan'
				// }
				// },
				// fields : [{
				// name : 'Source_TissueOrgan',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var SourceTissueStructureStore = Ext.create('Ext.data.Store',
				// {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display2/Source_TissueStructure/',
				// reader : {
				// type : 'json',
				// root : 'Source_TissueStructure'
				// }
				// },
				// fields : [{
				// name : 'Source_TissueStructure',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var SourceTissueTypeStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Source_TissueType/',
				// reader : {
				// type : 'json',
				// root : 'Source_TissueTypes'
				// }
				// },
				// fields : [{
				// name : 'Source_TissueType',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var sourceTissueTaxonStrainStore =
				// Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/Source_TissueTaxonStrain/',
				// reader : {
				// type : 'json',
				// root : 'tissueStrain'
				// }
				// },
				// fields : [{
				// name : 'tissueStrain',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var sourceTaxonStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Source_taxon/',
				// reader : {
				// type : 'json',
				// root : 'Source_taxons'
				// }
				// },
				// fields : [{
				// name : 'Source_taxon',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var allAgeUnitStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/All_AgeUnit/',
				// reader : {
				// type : 'json',
				// root : 'All_AgeUnits'
				// }
				// },
				// fields : [{
				// name : 'All_AgeUnit',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var rxUnitStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Rx_unit/',
				// reader : {
				// type : 'json',
				// root : 'Rx_units'
				// }
				// },
				// fields : [{
				// name : 'Rx_unit',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var rxUnitDetailStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/unit_detail/',
				// reader : {
				// type : 'json',
				// root : 'unit_detail'
				// }
				// },
				// fields : [{
				// name : 'unit_detail',
				// type : 'string'
				// }]
				// // autoLoad : true
				// });
				// var rxTreatmentStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Rx_treatment/',
				// reader : {
				// type : 'json',
				// root : 'Rx_treatments'
				// }
				// },
				// fields : [{
				// name : 'Rx_treatment',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var rxTreatmentDetailStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/treatment_detail/',
				// reader : {
				// type : 'json',
				// root : 'all_detail'
				// }
				// },
				// fields : [{
				// name : 'all_detail',
				// type : 'string'
				// }]
				// // autoLoad : true
				// });
				// var ubiSubcellStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Ubi_subcell/',
				// reader : {
				// type : 'json',
				// root : 'Ubi_subcells'
				// }
				// },
				// fields : [{
				// name : 'Ubi_subcell',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var ubiMethodStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Ubi_method/',
				// reader : {
				// type : 'json',
				// root : 'Ubi_methods'
				// }
				// },
				// fields : [{
				// name : 'Ubi_method',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var genotypeStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Genotype/',
				// reader : {
				// type : 'json',
				// root : 'Genotypes'
				// }
				// },
				// fields : [{
				// name : 'Genotype',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var cellTypeStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Cell_type/',
				// reader : {
				// type : 'json',
				// root : 'Cell_types'
				// }
				// },
				// fields : [{
				// name : 'Cell_type',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var cellcellTypeStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/source_CellType/',
				// reader : {
				// type : 'json',
				// root : 'source_CellTypes'
				// }
				// },
				// fields : [{
				// name : 'source_CellType',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var cellnameStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display2/Cell_Name/',
				// reader : {
				// type : 'json',
				// root : 'Cell_Name'
				// }
				// },
				// fields : [{
				// name : 'Cell_Name',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var tissueTypeStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Tissue_type/',
				// reader : {
				// type : 'json',
				// root : 'Tissue_types'
				// }
				// },
				// fields : [{
				// name : 'Tissue_type',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var tissueGenderStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Tissue_gender/',
				// reader : {
				// type : 'json',
				// root : 'Tissue_genders'
				// }
				// },
				// fields : [{
				// name : 'Tissue_gender',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var fluidNameStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Fluid_name/',
				// reader : {
				// type : 'json',
				// root : 'Fluid_names'
				// }
				// },
				// fields : [{
				// name : 'Fluid_name',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var ContainNoStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/ContainNoStore/',
				// reader : {
				// type : 'json',
				// root : 'ContainNo'
				// }
				// },
				// fields : [{
				// name : 'ContainNo',
				// type : 'string'
				// }]
				// });
				// var ContainBasketStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/ContainBasketStore/',
				// reader : {
				// type : 'json',
				// root : 'ContainBasket'
				// }
				// },
				// fields : [{
				// name : 'ContainBasket',
				// type : 'string'
				// }]
				// });
				// var ContainLayerStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/ContainLayerStore/',
				// reader : {
				// type : 'json',
				// root : 'ContainLayer'
				// }
				// },
				// fields : [{
				// name : 'ContainLayer',
				// type : 'string'
				// }]
				// });
				// // general panel
				// var generalPanel = Ext.create('Ext.form.Panel', {
				// title : 'General',
				// id : 'sample-general',
				// // frame : true,
				// storeId : 'methods',
				// layout : 'auto',
				// headerPosition : 'top',
				// bodyPadding : 10,
				// defaults : {
				// labelWidth : 120,
				// labelAligh : 'left',
				// width : 1000,
				// allowBlank : false
				// },
				// items : [{
				// fieldLabel : 'Experimenter',
				// xtype : 'fieldcontainer',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// defaults : {
				// editable : false
				// },
				// items : [{
				// xtype : 'combobox',
				// displayField : 'company',
				// name : 'company',
				// valueField : 'company',
				// store : companyStore,
				// queryMode : 'local',
				// allowBlank : false,
				// emptyText : 'Company',
				// width : 300,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// var lab = Ext.getCmp("lab");
				// lab.clearValue();
				// lab.store.load({
				// params : {
				// id : records[0].data.company
				// }
				// })
				// }
				// }
				// }
				// }, {
				// xtype : 'combobox',
				// displayField : 'lab',
				// valueField : 'lab',
				// name : 'lab',
				// id : 'lab',
				// emptyText : 'Laboratory',
				// store : labStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 200,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// var experimenter = Ext.getCmp("experimenter");
				// experimenter.clearValue();
				// experimenter.store.load({
				// params : {
				// id : records[0].data.lab
				// }
				// })
				// }
				// }
				// }
				// }, {
				// xtype : 'combobox',
				// displayField : 'experimenter',
				// valueField : 'experimenter',
				// emptyText : 'Experimenter',
				// name : 'experimenter',
				// id : 'experimenter',
				// store : experimenterStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 180
				// }]
				// }, {
				// xtype : 'datefield',
				// fieldLabel : 'Date',
				// value : Ext.Date.format(new Date(), 'n/d/Y'),
				// emptyText : 'Date',
				// name : 'date',
				// width : '200'
				// }, {
				// xtype : 'radiogroup',
				// fieldLabel : 'Sample Location',
				// name : 'location',
				// id : 'location' + timestamp,
				// columns : 3,
				// items : [{
				// boxLabel : 'Refrigerator',
				// name : 'location',
				// inputValue : 'Refrigerator'
				// }, {
				// boxLabel : 'Liquid Nitrogen',
				// name : 'location',
				// inputValue : 'Liquid Nitrogen'
				// }, {
				// boxLabel : 'Others',
				// name : 'location',
				// inputValue : 'Others'
				// }]
				// }, {
				// xtype : 'radiogroup',
				// fieldLabel : 'Source Type',
				// name : 'cell_tissue',
				// id : 'cell_tissue' + timestamp,
				// columns : 2,
				// items : [{
				// boxLabel : 'Tissue',
				// name : 'cell_tissue',
				// inputValue : 'Tissue'
				// }, {
				// boxLabel : 'Cell \& MicroOrganism',
				// name : 'cell_tissue',
				// inputValue : 'Cell'
				// }, {
				// boxLabel : 'Fluid & Excreta',
				// name : 'cell_tissue',
				// inputValue : 'Fluid'
				// }, {
				// boxLabel : 'Others',
				// name : 'cell_tissue',
				// inputValue : 'Others'
				// }]
				// }, {
				// xtype : 'numberfield',
				// fieldLabel : 'Total number of Treatment',
				// //afterLabelTextTpl : required,
				// id : 'treat_num',
				// name : 'treat_num',
				// minValue : 0,
				// maxValue : 10,
				// value : 0,
				// listeners : {
				// change : function(o, newV, oldV) {
				// if (newV > 10) {
				// alert('Number of treatment must be smaller than 10!')
				// newV = 1
				// Ext.getCmp('treat_num' + timestamp).setValue(1)
				// }
				// if (oldV) {
				// delTreatment(oldV);
				// }
				// for (i = 1; i <= newV; i++) {
				// addTreatment(i + 1, i);
				// }
				// }
				// },
				// width : 240
				// }, {
				// xtype : 'hiddenfield',
				// name : 'csrfmiddlewaretoken',
				// value : csrftoken
				// }]
				// });
				// // source tissue panel
				// var addGene = function(where, index, samplenum) {
				// var sample = {
				// fieldLabel : 'Target Gene ' + samplenum,
				// xtype : 'fieldcontainer',
				// id : 'target_Gene' + samplenum,
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'textfield',
				// emptyText : 'Gene Symbol',
				// // fieldLabel : 'Target
				// // Gene',
				// name : 'geneSymbol' + samplenum,
				// allowBlank : true
				// }, {
				// xtype : 'textfield',
				// emptyText : 'Gene ID',
				// // fieldLabel : 'Target
				// // Gene',
				// name : 'GeneID' + samplenum,
				// allowBlank : true
				// }, {
				// xtype : 'combobox',
				// displayField : 'Source_TissueTaxonID',
				// valueField : 'Source_TissueTaxonID',
				// emptyText : 'TaxonID',
				// name : 'geneTaxon' + samplenum,
				// store : geneIDStore,
				// queryMode : 'local',
				// allowBlank : true,
				// width : 150
				// }]
				// };
				// var temp = Ext.getCmp(where);
				// //console.log(temp)
				// temp.insert(index, sample);
				// }
				// var delGene = function(where, samplenum) {
				// for (i = samplenum; i > 0; i--) {
				// var sample = Ext.getCmp('target_Gene' + i);
				// var temp = Ext.getCmp(where);
				// temp.remove(sample);
				// }
				// };
				// var source_tissue = Ext.create('Ext.form.Panel', {
				// title : 'Tissue',
				// border : true,
				// // frame : true,
				// id : 'source_tissue',
				// bodyPadding : 10,
				// headerPosition : 'left',
				// defaults : {
				// labelWidth : 120,
				// labelAligh : 'left',
				// width : 800,
				// allowBlank : false
				// },
				// items : [{
				// fieldLabel : 'Taxon',
				// xtype : 'fieldcontainer',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'combobox',
				// displayField : 'Source_TissueTaxonAorM',
				// name : 'Source_TissueTaxonAorM',
				// valueField : 'Source_TissueTaxonAorM',
				// store : new Ext.data.SimpleStore({
				// fields : ["Source_TissueTaxonAorM"],
				// data : [["Animal"], ["Plant"]]
				// }),
				// queryMode : 'local',
				// allowBlank : false,
				// width : 120,
				// emptyText : 'Animal/Plant',
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// var lab = Ext.getCmp("tissueName");
				// lab.clearValue();
				// lab.store.load({
				// params : {
				// id : records[0].data.Source_TissueTaxonAorM
				// }
				// })
				// var lab = Ext.getCmp("tissue-system");
				// lab.clearValue();
				// lab.store.load({
				// params : {
				// id : records[0].data.Source_TissueTaxonAorM
				// }
				// })
				// }
				// }
				// }
				// }, {
				// xtype : 'combobox',
				// displayField : 'tissueName',
				// valueField : 'tissueName',
				// name : 'tissueName',
				// id : 'tissueName',
				// emptyText : 'Taxon Name',
				// store : sourceTissueTaxonNameStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 300,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// // console.log(records)
				// var experimenter = Ext.getCmp("tissueID");
				// experimenter.clearValue();
				// experimenter.store.load({
				// params : {
				// id : records[0].data.tissueName
				// }
				// })
				// }
				// }
				// }
				// }, {
				// xtype : 'combobox',
				// displayField : 'tissueID',
				// valueField : 'tissueID',
				// emptyText : 'Taxon ID',
				// name : 'tissueID',
				// id : 'tissueID',
				// store : sourceTissueTaxonIDStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 100,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// // console.log(records)
				// var experimenter = Ext.getCmp("Tissue_strain");
				// experimenter.clearValue();
				// experimenter.store.load({
				// params : {
				// id : records[0].data.tissueID
				// }
				// })
				// }
				// }
				// }
				// }]
				// }, {
				// xtype : 'combobox',
				// fieldLabel : 'Strain',
				// id : 'Tissue_strain',
				// emptyText : 'Strain Name',
				// valueField : 'tissueStrain',
				// displayField : 'tissueStrain',
				// name : 'tissueStrain',
				// queryMode : 'local',
				// store : sourceTissueTaxonStrainStore
				// }, {
				// xtype : 'fieldcontainer',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// fieldLabel : 'Age',
				// items : [{
				// xtype : 'textfield',
				// name : 'tissue_age'
				// }, {
				// xtype : 'combobox',
				// displayField : 'All_AgeUnit',
				// valueField : 'All_AgeUnit',
				// name : 'All_AgeUnit',
				// store : allAgeUnitStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 180
				// }]
				// }, {
				// xtype : 'combobox',
				// fieldLabel : 'Gender',
				// displayField : 'Tissue_gender',
				// name : 'Tissue_gender',
				// store : tissueGenderStore,
				// width : 300
				// }, {
				// xtype : 'combobox',
				// fieldLabel : 'Genotype',
				// displayField : 'Genotype',
				// name : 'Genotype',
				// store : genotypeStore
				// }, {
				// xtype : 'numberfield',
				// fieldLabel : 'Total number of Target Gene',
				// //afterLabelTextTpl : required,
				// // id : 'Gene_num',
				// name : 'Geme_num',
				// minValue : 0,
				// maxValue : 10,
				// value : 0,
				// listeners : {
				// change : function(o, newV, oldV) {
				// if (newV > 10) {
				// alert('Number of Gene must be smaller than 10!')
				// newV = 1
				// Ext.getCmp('Geme_num').setValue(1)
				// }
				// if (oldV) {
				// delGene('source_tissue', oldV);
				// }
				// for (i = 1; i <= newV; i++) {
				// addGene('source_tissue', i + 5, i);
				// }
				// }
				// },
				// width : 240
				// }, {
				// fieldLabel : 'Tissue',
				// xtype : 'fieldcontainer',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'combobox',
				// displayField : 'Source_TissueSystem',
				// name : 'Source_TissueSystem',
				// valueField : 'Source_TissueSystem',
				// id : 'tissue-system',
				// store : SourceTissueSystemStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 180,
				// emptyText : 'System',
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// var lab = Ext.getCmp("tissue-organ");
				// lab.clearValue();
				// lab.store.load({
				// params : {
				// id : records[0].data.Source_TissueSystem
				// }
				// })
				// }
				// }
				// }
				// }, {
				// xtype : 'combobox',
				// displayField : 'Source_TissueOrgan',
				// valueField : 'Source_TissueOrgan',
				// name : 'Source_TissueOrgan',
				// id : 'tissue-organ',
				// emptyText : 'Organ',
				// store : SourceTissueOrganStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 150,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// var lab = Ext.getCmp("tissue-structure");
				// lab.clearValue();
				// lab.store.load({
				// params : {
				// id : records[0].data.Source_TissueOrgan
				// }
				// })
				// }
				// }
				// }
				// }, {
				// xtype : 'combobox',
				// displayField : 'Source_TissueStructure',
				// valueField : 'Source_TissueStructure',
				// name : 'Source_TissueStructure',
				// id : 'tissue-structure',
				// emptyText : 'Anatomical Structure',
				// store : SourceTissueStructureStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 120
				// }, {
				// xtype : 'combobox',
				// displayField : 'Source_TissueType',
				// valueField : 'Source_TissueType',
				// emptyText : 'Status',
				// name : 'Source_TissueType',
				// store : SourceTissueTypeStore,
				// queryMode : 'local',
				// allowBlank : false
				// }]
				// },
				// // {
				// // fieldLabel : 'Target Gene',
				// // xtype : 'fieldcontainer',
				// // layout : {
				// // type : 'hbox',
				// // align : 'stretch'
				// // },
				// // items : [{
				// // xtype : 'textfield',
				// // emptyText : 'Gene Symbol',
				// // // fieldLabel : 'Target
				// // // Gene',
				// // name : 'geneSymbol',
				// // allowBlank : true
				// // }, {
				// // xtype : 'textfield',
				// // emptyText : 'Gene ID',
				// // // fieldLabel : 'Target
				// // // Gene',
				// // name : 'GeneID',
				// // allowBlank : true
				// // }, {
				// // xtype : 'combobox',
				// // displayField : 'Source_TissueTaxonID',
				// // valueField : 'Source_TissueTaxonID',
				// // emptyText : 'Gene Taxon',
				// // name : 'geneTaxon',
				// // store : geneIDStore,
				// // queryMode : 'local',
				// // allowBlank : true,
				// // width : 100
				// // }]
				// // },
				// {
				// xtype : 'timefield',
				// fieldLabel : 'CR Time',
				// format : 'G:i:s',
				// increment : 15,
				// name : 'circ_time',
				// allowBlank : true
				// }, {
				// xtype : 'textfield',
				// fieldLabel : 'Specific ID',
				// name : 'Specific_ID',
				// allowBlank : true
				// }]
				// });
				// // source cell panel
				// var source_cell = Ext.create('Ext.form.Panel', {
				// id : 'source_cell',
				// title : 'Cell and MicroOrganism',
				// border : true,
				// // frame : true,
				// bodyPadding : 10,
				// headerPosition : 'left',
				// defaults : {
				// labelWidth : 120,
				// labelAligh : 'left',
				// width : 800,
				// allowBlank : false
				// },
				// items : [{
				// fieldLabel : 'Taxon',
				// xtype : 'fieldcontainer',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'combobox',
				// displayField : 'Source_TissueTaxonAorM',
				// name : 'Source_TissueTaxonAorM',
				// emptyText : 'Cell/MicroOrganism',
				// valueField : 'Source_TissueTaxonAorM',
				// store : new Ext.data.SimpleStore({
				// fields : ["Source_TissueTaxonAorM"],
				// data : [["Animal"], ["Microorganism"]]
				// }),
				// queryMode : 'local',
				// allowBlank : false,
				// width : 120,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// var lab = Ext.getCmp("cellName");
				// lab.clearValue();
				// lab.store.load({
				// params : {
				// id : records[0].data.Source_TissueTaxonAorM
				// }
				// })
				// }
				// }
				// }
				// }, {
				// xtype : 'combobox',
				// displayField : 'tissueName',
				// valueField : 'tissueName',
				// name : 'tissueName',
				// id : 'cellName',
				// emptyText : 'Taxon Name',
				// store : sourceTissueTaxonNameStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 300,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// // console.log(records)
				// var experimenter = Ext.getCmp("cellID");
				// experimenter.clearValue();
				// experimenter.store.load({
				// params : {
				// id : records[0].data.tissueName
				// }
				// })
				// }
				// }
				// }
				// }, {
				// xtype : 'combobox',
				// displayField : 'tissueID',
				// valueField : 'tissueID',
				// emptyText : 'Taxon ID',
				// name : 'tissueID',
				// id : 'cellID',
				// store : sourceTissueTaxonIDStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 100,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// // console.log(records)
				// var experimenter = Ext.getCmp("cellstrain");
				// experimenter.clearValue();
				// experimenter.store.load({
				// params : {
				// id : records[0].data.tissueID
				// }
				// })
				// }
				// }
				// }
				// }]
				// }, {
				// xtype : 'combobox',
				// fieldLabel : 'Strain',
				// emptyText : 'Strain Name',
				// id : 'cellstrain',
				// queryMode : 'local',
				// valueField : 'tissueStrain',
				// displayField : 'tissueStrain',
				// name : 'tissueStrain',
				// store : sourceTissueTaxonStrainStore
				// }, {
				// xtype : 'combobox',
				// fieldLabel : 'Genotype',
				// displayField : 'Genotype',
				// name : 'Genotype',
				// store : genotypeStore
				// }, {
				// xtype : 'numberfield',
				// fieldLabel : 'Total number of Target Gene',
				// //afterLabelTextTpl : required,
				// // id : 'Gene_num',
				// name : 'Geme_num',
				// minValue : 0,
				// maxValue : 10,
				// value : 0,
				// listeners : {
				// change : function(o, newV, oldV) {
				// if (newV > 10) {
				// alert('Number of Gene must be smaller than 10!')
				// newV = 1
				// Ext.getCmp('Geme_num').setValue(1)
				// }
				// if (oldV) {
				// delGene('source_cell', oldV);
				// }
				// for (i = 1; i <= newV; i++) {
				// addGene('source_cell', i + 3, i);
				// }
				// }
				// },
				// width : 240
				// }, {
				// fieldLabel : 'Cell',
				// xtype : 'fieldcontainer',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'combobox',
				// displayField : 'source_CellType',
				// name : 'cellcelltype',
				// emptyText : 'Type',
				// valueField : 'source_CellType',
				// store : cellcellTypeStore,
				// queryMode : 'local',
				// width : 300,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// var lab = Ext.getCmp("cellcellname");
				// lab.clearValue();
				// lab.store.load({
				// params : {
				// id : records[0].data.source_CellType
				// }
				// })
				// }
				// }
				// }
				// }, {
				// xtype : 'combobox',
				// displayField : 'Cell_Name',
				// emptyText : 'Name',
				// valueField : 'Cell_Name',
				// name : 'Cell_Name',
				// id : 'cellcellname',
				// store : cellnameStore,
				// queryMode : 'local',
				// width : 300
				// }]
				// },
				// // {
				// // fieldLabel : 'Target Gene',
				// // xtype : 'fieldcontainer',
				// // layout : {
				// // type : 'hbox',
				// // align : 'stretch'
				// // },
				// // items : [{
				// // xtype : 'textfield',
				// // emptyText : 'Gene Symbol',
				// // // fieldLabel : 'Target
				// // // Gene',
				// // name : 'geneSymbol',
				// // allowBlank : true
				// // }, {
				// // xtype : 'textfield',
				// // emptyText : 'Gene ID',
				// // // fieldLabel : 'Target
				// // // Gene',
				// // name : 'GeneID',
				// // allowBlank : true
				// // }, {
				// // xtype : 'combobox',
				// // displayField : 'Source_TissueTaxonID',
				// // valueField : 'Source_TissueTaxonID',
				// // emptyText : 'Gene Taxon',
				// // name : 'geneTaxon',
				// // store : geneIDStore,
				// // queryMode : 'local',
				// // allowBlank : true,
				// // width : 100
				// // }]
				// // },
				// {
				// xtype : 'timefield',
				// fieldLabel : 'CR Time',
				// format : 'G:i:s',
				// increment : 15,
				// name : 'circ_time',
				// allowBlank : true
				// }, {
				// xtype : 'textfield',
				// fieldLabel : 'Specific ID',
				// name : 'Specific_ID',
				// allowBlank : true
				// }]
				// });
				// var source_fluid = Ext.create('Ext.form.Panel', {
				// id : 'source_fluid',
				// title : 'Fluid & Excreta',
				// border : true,
				// bodyPadding : 10,
				// // frame : true,
				// headerPosition : 'left',
				// defaults : {
				// labelWidth : 120,
				// labelAligh : 'left',
				// width : 800,
				// allowBlank : false
				// },
				// items : [{
				// fieldLabel : 'Taxon',
				// xtype : 'fieldcontainer',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'combobox',
				// displayField : 'Source_TissueTaxonAorM',
				// name : 'Source_TissueTaxonAorM',
				// valueField : 'Source_TissueTaxonAorM',
				// store : new Ext.data.SimpleStore({
				// fields : ["Source_TissueTaxonAorM"],
				// data : [["Animal"], ["Plant"]]
				// }),
				// queryMode : 'local',
				// allowBlank : false,
				// emptyText : 'Animal/Plant',
				// width : 120,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// var lab = Ext.getCmp("fluidName");
				// lab.clearValue();
				// lab.store.load({
				// params : {
				// id : records[0].data.Source_TissueTaxonAorM
				// }
				// })
				// }
				// }
				// }
				// }, {
				// xtype : 'combobox',
				// displayField : 'tissueName',
				// valueField : 'tissueName',
				// emptyText : 'Taxon Name',
				// name : 'tissueName',
				// id : 'fluidName',
				// store : sourceTissueTaxonNameStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 300,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// // console.log(records)
				// var experimenter = Ext.getCmp("fluidID");
				// experimenter.clearValue();
				// experimenter.store.load({
				// params : {
				// id : records[0].data.tissueName
				// }
				// })
				// }
				// }
				// }
				// }, {
				// xtype : 'combobox',
				// displayField : 'tissueID',
				// valueField : 'tissueID',
				// emptyText : 'Taxon ID',
				// name : 'tissueID',
				// id : 'fluidID',
				// store : sourceTissueTaxonIDStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 100,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// // console.log(records)
				// var experimenter = Ext.getCmp("fluidstrain");
				// experimenter.clearValue();
				// experimenter.store.load({
				// params : {
				// id : records[0].data.tissueID
				// }
				// })
				// }
				// }
				// }
				// }]
				// }, {
				// xtype : 'combobox',
				// fieldLabel : 'Strain',
				// id : 'fluidstrain',
				// valueField : 'tissueStrain',
				// emptyText : 'Strain Name',
				// displayField : 'tissueStrain',
				// name : 'tissueStrain',
				// store : sourceTissueTaxonStrainStore
				// }, {
				// fieldLabel : 'Age',
				// xtype : 'fieldcontainer',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'textfield',
				// // fieldLabel : 'Target
				// // Gene',
				// name : 'tissue_age'
				// }, {
				// xtype : 'combobox',
				// displayField : 'All_AgeUnit',
				// valueField : 'All_AgeUnit',
				// name : 'All_AgeUnit',
				// // id : 'tissueName',
				// store : allAgeUnitStore,
				// queryMode : 'local',
				// allowBlank : false,
				// width : 180
				// }]
				// }, {
				// xtype : 'combobox',
				// fieldLabel : 'Gender',
				// displayField : 'Tissue_gender',
				// name : 'Tissue_gender',
				// store : tissueGenderStore
				// }, {
				// xtype : 'combobox',
				// fieldLabel : 'Genotype',
				// displayField : 'Genotype',
				// name : 'Genotype',
				// store : genotypeStore
				// }, {
				// xtype : 'numberfield',
				// fieldLabel : 'Total number of Target Gene',
				// //afterLabelTextTpl : required,
				// // id : 'Gene_num',
				// name : 'Geme_num',
				// minValue : 0,
				// maxValue : 10,
				// value : 0,
				// listeners : {
				// change : function(o, newV, oldV) {
				// if (newV > 10) {
				// alert('Number of Gene must be smaller than 10!')
				// newV = 1
				// Ext.getCmp('Geme_num').setValue(1)
				// }
				// if (oldV) {
				// delGene('source_fluid', oldV);
				// }
				// for (i = 1; i <= newV; i++) {
				// addGene('source_fluid', i + 5, i);
				// }
				// }
				// },
				// width : 240
				// },
				// // {
				// // fieldLabel : 'Target Gene',
				// // xtype : 'fieldcontainer',
				// // layout : {
				// // type : 'hbox',
				// // align : 'stretch'
				// // },
				// // items : [{
				// // xtype : 'textfield',
				// // emptyText : 'Gene Symbol',
				// // // fieldLabel : 'Target
				// // // Gene',
				// // name : 'geneSymbol',
				// // allowBlank : true
				// // }, {
				// // xtype : 'textfield',
				// // emptyText : 'Gene ID',
				// // // fieldLabel : 'Target
				// // // Gene',
				// // name : 'GeneID',
				// // allowBlank : true
				// // }, {
				// // xtype : 'combobox',
				// // displayField : 'Source_TissueTaxonID',
				// // valueField : 'Source_TissueTaxonID',
				// // emptyText : 'Gene Taxon',
				// // name : 'geneTaxon',
				// // store : geneIDStore,
				// // queryMode : 'local',
				// // allowBlank : false,
				// // width : 100,
				// // allowBlank : true
				// // }]
				// // },
				// {
				// xtype : 'combobox',
				// store : fluidNameStore,
				// fieldLabel : 'Fluid/Excreta',
				// displayField : 'Fluid_name',
				// name : 'Fluid_name',
				// valueField : 'Fluid_name'
				// }, {
				// xtype : 'textfield',
				// fieldLabel : 'Specific ID',
				// name : 'Specific_ID',
				// allowBlank : true
				// }]
				// });
				// var source_others = Ext.create('Ext.form.Panel', {
				// title : 'Others',
				// border : true,
				// // frame : true,
				// bodyPadding : 10,
				// headerPosition : 'left',
				// defaults : {
				// labelWidth : 120,
				// labelAligh : 'left',
				// width : 450,
				// allowBlank : false
				// },
				// items : [{
				// xtype : 'textareafield',
				// fieldLabel : 'Others',
				// name : 'tissue_others'
				// }]
				// });
				// // rx panel
				// var addTreatment = function(index, treatnum) {
				// var rxPanel = Ext.create('Ext.form.Panel', {
				// title : 'Treatment' + treatnum,
				// id : 'Treatment' + treatnum,
				// border : true,
				// bodyPadding : 10,
				// layout : 'anchor',
				// headerPosition : 'top',
				// defaults : {
				// labelWidth : 120,
				// labelAligh : 'left',
				// width : 800,
				// allowBlank : false
				// },
				// items : [{
				// xtype : 'fieldcontainer',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'combobox',
				// fieldLabel : 'Treatments',
				// displayField : 'Rx_treatment',
				// name : 'Rx_treatment' + treatnum,
				// store : rxTreatmentStore,
				// queryMode : 'local',
				// labelWidth : 120,
				// width : 415,
				// allowBlank : false,
				// listeners : {
				// select : {
				// fn : function(combo, records, index) {
				// var lab = Ext.getCmp("treantment_detail" + treatnum);
				// lab.clearValue();
				// lab.store.load({
				// params : {
				// id : records[0].data.Rx_treatment
				// }
				// })
				// }
				// },
				// change : {
				// fn : function(combo, newValue, oldValue) {
				// // console.log(box)
				// var sample = {
				// fieldLabel : 'New Target Gene ',
				// xtype : 'fieldcontainer',
				// id : 'New_target_Gene' + treatnum,
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'textfield',
				// emptyText : 'Gene Symbol',
				// // fieldLabel : 'Target
				// // Gene',
				// name : 'newGeneSymbol' + treatnum,
				// value : responseJson.rx_geneSymbol[treatnum-1],
				// allowBlank : true
				// }, {
				// xtype : 'textfield',
				// emptyText : 'Gene ID',
				// // fieldLabel : 'Target
				// // Gene',
				// name : 'newGeneID' + treatnum,
				// value : responseJson.rx_geneID[treatnum-1],
				// allowBlank : true
				// }, {
				// xtype : 'combobox',
				// displayField : 'Source_TissueTaxonID',
				// valueField : 'Source_TissueTaxonID',
				// emptyText : 'Gene Taxon',
				// name : 'newGeneTaxon' + treatnum,
				// store : geneIDStore,
				// queryMode : 'local',
				// value : responseJson.rx_geneTaxon[treatnum-1],
				// allowBlank : true,
				// width : 100
				// }]
				// };
				// var sample2 = {
				// xtype : 'fieldcontainer',
				// id : 'samp-treat-unit' + treatnum,
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'textfield',
				// fieldLabel : 'Amount',
				// name : 'amount' + treatnum,
				// width : 180,
				// labelWidth : 120,
				// value : responseJson.rx_amount[treatnum-1],
				// allowBlank : true
				// }, {
				// xtype : 'combobox',
				// displayField : 'Rx_unit',
				// name : 'Rx_unit' + treatnum,
				// store : rxUnitStore,
				// queryMode : 'local',
				// emptyText : 'Param type',
				// //value : responseJson.rx_unit[treatnum-1],
				// allowBlank : true,
				// listeners : {
				// change : {
				// fn : function(box, newValue, oldValue) {
				// // console.log(box)
				// var detailPanel = Ext.create('Ext.form.ComboBox', {
				// id : 'unit_detail_' + treatnum,
				// displayField : 'unit_detail',
				// name : 'unit_detail_' + treatnum,
				// store : rxUnitDetailStore,
				// queryMode : 'local',
				// emptyText : 'Param unit',
				// editable : false,
				// //value : responseJson.rx_unit_deatil1[treatnum-1],
				// allowBlank : true
				// })
				// var detailPanel2 = {
				// xtype : 'fieldcontainer',
				// id : 'unit_detail2_' + treatnum,
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'combobox',
				// // id :
				// // 'detailPanel2-1',
				// valueField : 'rx_dur_unit',
				// displayField : 'rx_dur_unit',
				// name : 'unit_detail2_' + treatnum,
				// store : new Ext.data.SimpleStore({
				// fields : ["rx_dur_unit"],
				// data : [["L"], ["mL"], ["g"], ["kg"], ["mol"], ["mmol"]]
				// })
				// }, {
				// xtype : 'displayfield',
				// // id :
				// // 'detailPanel2-2',
				// value : ' / '
				// }, {
				// xtype : 'combobox',
				// // id :
				// // 'detailPanel22-1',
				// valueField : 'rx_dur_unit',
				// displayField : 'rx_dur_unit',
				// name : 'unit_detail22_' + treatnum,
				// store : new Ext.data.SimpleStore({
				// fields : ["rx_dur_unit"],
				// data : [["L"], ["mL"], ["uL"], ["nL"], ["Kg"], ["g"], ["mg"]]
				// })
				// }]
				// }
				// var temp = Ext.getCmp('samp-treat-unit' + treatnum);
				// if (oldValue != 'Concentration')
				// temp.remove(Ext.getCmp('unit_detail_' + treatnum), false)
				// else if (oldValue == 'Concentration') {
				// temp.remove(Ext.getCmp('unit_detail2_' + treatnum), false)
				// }
				// if (newValue != 'Concentration') {
				// detailPanel.clearValue()
				// detailPanel.store.load({
				// params : {
				// id : newValue
				// }
				// })
				// temp.insert(2, detailPanel)
				// } else if (newValue == 'Concentration') {
				// temp.insert(2, detailPanel2)
				// }
				// }
				// }
				// }
				// }]
				// }
				// var temp = Ext.getCmp('Treatment' + treatnum);
				// // console.log(temp.items.items[2].id)
				// // console.log(temp.items)
				// // if (newValue != 'Gene Engineering') {
				// // if ('New_target_Gene' + treatnum ==
				// // temp.items.items[2].id){
				// temp.remove(temp.items.items[1], false)
				// // }
				// // }
				// if (newValue == 'Gene Engineering')
				// temp.insert(1, sample)
				// else {
				// temp.insert(1, sample2)
				// }
				// }
				// }
				// }
				// }, {
				// xtype : 'combobox',
				// id : 'treantment_detail' + treatnum,
				// // fieldLabel :
				// // 'Treatments',
				// displayField : 'all_detail',
				// name : 'all_detail' + treatnum,
				// store : rxTreatmentDetailStore,
				// queryMode : 'local',
				// labelWidth : 120,
				// allowBlank : true
				// }]
				// }, {
				// xtype : 'fieldcontainer',
				// id : 'samp-treat-unit' + treatnum,
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'textfield',
				// fieldLabel : 'Amount',
				// name : 'amount' + treatnum,
				// width : 180,
				// labelWidth : 120,
				// allowBlank : true
				// }, {
				// xtype : 'combobox',
				// displayField : 'Rx_unit',
				// name : 'Rx_unit' + treatnum,
				// store : rxUnitStore,
				// queryMode : 'local',
				// emptyText : 'Param type',
				// allowBlank : true,
				// listeners : {
				// change : {
				// fn : function(box, newValue, oldValue) {
				// // console.log(box)
				// var detailPanel = Ext.create('Ext.form.ComboBox', {
				// id : 'unit_detail_' + treatnum,
				// displayField : 'unit_detail',
				// name : 'unit_detail' + treatnum,
				// store : rxUnitDetailStore,
				// queryMode : 'local',
				// emptyText : 'Param unit',
				// editable : false,
				// allowBlank : true
				// })
				// var detailPanel2 = {
				// xtype : 'fieldcontainer',
				// id : 'unit_detail2_' + treatnum,
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'combobox',
				// // id : 'detailPanel2-1',
				// valueField : 'rx_dur_unit',
				// displayField : 'rx_dur_unit',
				// name : 'unit_detail2' + treatnum,
				// store : new Ext.data.SimpleStore({
				// fields : ["rx_dur_unit"],
				// data : [["L"], ["mL"], ["g"], ["kg"], ["mol"], ["mmol"]]
				// })
				// }, {
				// xtype : 'displayfield',
				// // id : 'detailPanel2-2',
				// value : ' / '
				// }, {
				// xtype : 'combobox',
				// // id : 'detailPanel22-1',
				// valueField : 'rx_dur_unit',
				// displayField : 'rx_dur_unit',
				// name : 'unit_detail22' + treatnum,
				// store : new Ext.data.SimpleStore({
				// fields : ["rx_dur_unit"],
				// data : [["L"], ["mL"], ["uL"], ["nL"], ["Kg"], ["g"], ["mg"]]
				// })
				// }]
				// }
				// var temp = Ext.getCmp('samp-treat-unit' + treatnum);
				// if (oldValue != 'Concentration')
				// temp.remove(Ext.getCmp('unit_detail_' + treatnum), false)
				// else if (oldValue == 'Concentration') {
				// temp.remove(Ext.getCmp('unit_detail2_' + treatnum), false)
				// }
				// if (newValue != 'Concentration') {
				// detailPanel.clearValue()
				// detailPanel.store.load({
				// params : {
				// id : newValue
				// }
				// })
				// temp.insert(2, detailPanel)
				// } else if (newValue == 'Concentration') {
				// temp.insert(2, detailPanel2)
				// }
				// }
				// }
				// }
				// }]
				// }, {
				// xtype : 'fieldcontainer',
				// fieldLabel : 'Duration',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'textfield',
				// name : 'duration' + treatnum,
				// labelWidth : 120,
				// allowBlank : true
				// }, {
				// xtype : 'combobox',
				// displayField : 'rx_dur_unit',
				// name : 'rx_dur_unit' + treatnum,
				// valueField : 'rx_dur_unit',
				// store : new Ext.data.SimpleStore({
				// fields : ["rx_dur_unit"],
				// data : [["Week"], ["Day"], ["Hour"], ["Minute"], ["Second"]]
				// }),
				// queryMode : 'local',
				// width : 200
				// }]
				// }]
				// });
				// formPanel.insert(index, rxPanel);
				// };
				// var delTreatment = function(samplenum) {
				// for (i = samplenum; i > 0; i--) {
				// var sample = Ext.getCmp('Treatment' + i);
				// formPanel.remove(sample);
				// }
				// };
				// // var rxPanel = Ext.create('Ext.form.Panel', {
				// // title : 'Treatment',
				// // border : true,
				// // bodyPadding : 10,
				// // // frame : true,
				// // // bodyStyle : 'padding: 5 5 0',
				// // layout : 'anchor',
				// // headerPosition : 'top',
				// // defaults : {
				// // labelWidth : 120,
				// // labelAligh : 'left',
				// // width : 800,
				// // allowBlank : false
				// // },
				// // items : [{
				// // xtype : 'fieldcontainer',
				// // layout : {
				// // type : 'hbox',
				// // align : 'stretch'
				// // },
				// // items : [{
				// // xtype : 'combobox',
				// // fieldLabel : 'Treatments',
				// // displayField : 'Rx_treatment',
				// // name : 'Rx_treatment',
				// // store : rxTreatmentStore,
				// // queryMode : 'local',
				// // labelWidth : 120,
				// // width : 415,
				// // allowBlank : false,
				// // listeners : {
				// // select : {
				// // fn : function(combo, records, index) {
				// // var lab = Ext.getCmp("treantment_detail");
				// // lab.clearValue();
				// // lab.store.load({
				// // params : {
				// // id : records[0].data.Rx_treatment
				// // }
				// // })
				// // }
				// // }
				// // }
				// // }, {
				// // xtype : 'combobox',
				// // id : 'treantment_detail',
				// // // fieldLabel :
				// // // 'Treatments',
				// // displayField : 'all_detail',
				// // name : 'all_detail',
				// // store : rxTreatmentDetailStore,
				// // queryMode : 'local',
				// // labelWidth : 120,
				// // allowBlank : true
				// // }]
				// // }, {
				// // xtype : 'fieldcontainer',
				// // id : 'samp-treat-unit',
				// // layout : {
				// // type : 'hbox',
				// // align : 'stretch'
				// // },
				// // items : [{
				// // xtype : 'textfield',
				// // fieldLabel : 'Amount',
				// // name : 'amount',
				// // width : 180,
				// // labelWidth : 120,
				// // allowBlank : true
				// // }, {
				// // xtype : 'combobox',
				// // displayField : 'Rx_unit',
				// // name : 'Rx_unit',
				// // store : rxUnitStore,
				// // queryMode : 'local',
				// // emptyText : 'Param type',
				// // allowBlank : true,
				// // listeners : {
				// // change : {
				// // fn : function(box, newValue, oldValue) {
				// // // console.log(box)
				// // var temp = Ext.getCmp('samp-treat-unit');
				// // if (oldValue != 'Concentration')
				// // temp.remove(detailPanel, false)
				// // else if (oldValue == 'Concentration') {
				// // temp.remove(Ext.getCmp('unit_detail2'), false)
				// // }
				// // if (newValue != 'Concentration') {
				// // detailPanel.clearValue()
				// // detailPanel.store.load({
				// // params : {
				// // id : newValue
				// // }
				// // })
				// // temp.insert(2, detailPanel)
				// // } else if (newValue == 'Concentration') {
				// // temp.insert(2, detailPanel2)
				// // }
				// // }
				// // }
				// // }
				// // }]
				// // }, {
				// // xtype : 'fieldcontainer',
				// // layout : {
				// // type : 'hbox',
				// // align : 'stretch'
				// // },
				// // items : [{
				// // xtype : 'textfield',
				// // name : 'duration',
				// // fieldLabel : 'Duration',
				// // labelWidth : 120,
				// // allowBlank : true
				// // }, {
				// // xtype : 'combobox',
				// // displayField : 'rx_dur_unit',
				// // name : 'rx_dur_unit',
				// // valueField : 'rx_dur_unit',
				// // store : new Ext.data.SimpleStore({
				// // fields : ["rx_dur_unit"],
				// // data : [["Week"], ["Day"], ["Hour"], ["Minute"],
				// ["Second"]]
				// // }),
				// // queryMode : 'local',
				// // width : 200
				// // }]
				// // }]
				// // });
				// var ubiPanel = Ext.create('Ext.form.Panel', {
				// title : 'Information',
				// border : true,
				// // frame : true,
				// bodyPadding : 10,
				// headerPosition : 'top',
				// defaults : {
				// labelWidth : 120,
				// labelAligh : 'left',
				// width : 800,
				// allowBlank : false
				// },
				// items : [{
				// xtype : 'fieldcontainer',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'combobox',
				// fieldLabel : 'Subcelluar Organelle',
				// name : 'Ubi_subcell',
				// displayField : 'Ubi_subcell',
				// store : ubiSubcellStore,
				// queryMode : 'local',
				// multiSelect : true,
				// editable : true,
				// labelWidth : 120,
				// width : 415,
				// allowBlank : false
				// }]
				// }, {
				// xtype : 'fieldcontainer',
				// layout : {
				// type : 'hbox',
				// align : 'stretch'
				// },
				// items : [{
				// xtype : 'combobox',
				// valueField : 'Ubi_method',
				// fieldLabel : 'Protocol',
				// displayField : 'Ubi_method',
				// name : 'Ubi_method',
				// store : ubiMethodStore,
				// // queryMode : 'local',
				// multiSelect : true,
				// labelWidth : 120,
				// width : 800,
				// allowBlank : false
				// }]
				// }, /*
				// * { xtype : 'combobox', name : 'Ubi_detergent', displayField
				// :
				// * 'Ubi_detergent', fieldLabel : 'Detergent', store :
				// ubiDetergentStore },
				// */{
				// xtype : 'textfield',
				// name : 'Ubi_salt',
				// // displayField : 'Ubi_salt',
				// fieldLabel : 'Salt'
				// // store : ubiSaltStore
				// }]
				// });
				// var commentsPanel = Ext.create('Ext.form.Panel', {
				// title : 'Comments',
				// border : true,
				// // frame : true,
				// bodyPadding : 10,
				// headerPosition : 'top',
				// defaults : {
				// labelWidth : 120,
				// // labelAlign : 'top',
				// width : 800
				// // allowBlank : false
				// },
				// items : [{
				// xtype : 'textareafield',
				// name : 'comments',
				// fieldLabel : 'Extract Comments'
				// }, {
				// xtype : 'textfield',
				// // fieldLabel : 'Target
				// // Gene',
				// name : 'Ispec_num',
				// fieldLabel : 'Ispec No',
				// width : 400
				// }]
				// });
				// var buttonPanel = Ext.create('Ext.panel.Panel', {
				// // frame : true,
				// // renderTo: 'button',
				// buttonAlign : "center",
				// buttons : [{
				// text : 'Submit',
				// handler : submitForm
				// }, {
				// text : 'Cancel',
				// handler : cancelForm
				// }]
				// });
				// var formPanel = Ext.create('Ext.form.Panel', {
				// id : timestamp,
				// // renderTo : 'form',
				// overflowY : 'scroll',
				// items : [generalPanel, ubiPanel, commentsPanel, buttonPanel]
				// });
				// // console.log(timestamp)
				// // event listener for type radio
				// typeradio = Ext.getCmp('cell_tissue' + timestamp);
				// typeradio.on('change', function(radio, newV, oldV, e) {
				// if (oldV.cell_tissue == 'Tissue') {
				// formPanel.remove(source_tissue, false);
				// } else if (oldV.cell_tissue == 'Cell') {
				// formPanel.remove(source_cell, false);
				// } else if (oldV.cell_tissue == 'Fluid') {
				// formPanel.remove(source_fluid, false);
				// } else if (oldV.cell_tissue == 'Others') {
				// formPanel.remove(source_others, false);
				// }
				// if (newV.cell_tissue == 'Tissue') {
				// formPanel.insert(1, source_tissue);
				// } else if (newV.cell_tissue == 'Cell') {
				// formPanel.insert(1, source_cell);
				// } else if (newV.cell_tissue == 'Fluid') {
				// formPanel.insert(1, source_fluid);
				// } else if (newV.cell_tissue == 'Others') {
				// formPanel.insert(1, source_others);
				// }
				// });
				// // For Container
				// var RefrigeratorNoStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Refrigerator_No/',
				// reader : {
				// type : 'json',
				// root : 'Refrigerator_Nos'
				// }
				// },
				// fields : [{
				// name : 'Refrigerator_No',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var RefrigeratorTemperStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Refrigerator_Temperature/',
				// reader : {
				// type : 'json',
				// root : 'Refrigerator_Temperatures'
				// }
				// },
				// fields : [{
				// name : 'Refrigerator_Temperature',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var RefrigeratorLayerStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Refrigerator_Layer/',
				// reader : {
				// type : 'json',
				// root : 'Refrigerator_Layers'
				// }
				// },
				// fields : [{
				// name : 'Refrigerator_Layer',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var RefrigeratorPanel = Ext.create('Ext.container.Container',
				// {
				// // id : 'Location-Refrigerator',
				// layout : {
				// type : 'hbox'
				// },
				// defaults : {
				// labelWidth : 120,
				// width : 800
				// },
				// items : [{
				// xtype : 'combobox',
				// emptyText : 'Refrigerator No.',
				// fieldLabel : '#Refrigerator',
				// displayField : 'Refrigerator_No',
				// name : 'RefrigeratorNo',
				// store : RefrigeratorNoStore,
				// typeAhead : true,
				// width : 300
				// }, {
				// xtype : 'combobox',
				// emptyText : 'Temperature',
				// displayField : 'Refrigerator_Temperature',
				// name : 'RefrigeratorTemper',
				// store : RefrigeratorTemperStore,
				// typeAhead : true,
				// width : 300
				// }, {
				// xtype : 'combobox',
				// emptyText : 'Refrigerator Layer',
				// displayField : 'Refrigerator_Layer',
				// name : 'RefrigeratorLayer',
				// store : RefrigeratorLayerStore,
				// typeAhead : true,
				// width : 300
				// }]
				// })
				// // nitrogen-panel
				// var NitrogenContStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Nitrogen_Container/',
				// reader : {
				// type : 'json',
				// root : 'Nitrogen_Containers'
				// }
				// },
				// fields : [{
				// name : 'Nitrogen_Container',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var NitrogenBasketStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Nitrogen_Basket/',
				// reader : {
				// type : 'json',
				// root : 'Nitrogen_Baskets'
				// }
				// },
				// fields : [{
				// name : 'Nitrogen_Basket',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var NitrogenLayerStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Nitrogen_Layer/',
				// reader : {
				// type : 'json',
				// root : 'Nitrogen_Layers'
				// }
				// },
				// fields : [{
				// name : 'Nitrogen_Layer',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var NitrogenPanel = Ext.create('Ext.container.Container', {
				// // id : 'Location-Refrigerator',
				// layout : {
				// type : 'hbox'
				// },
				// defaults : {
				// labelWidth : 120,
				// width : 800
				// },
				// items : [{
				// xtype : 'combobox',
				// emptyText : 'Container No.',
				// fieldLabel : '#Liquid Nitrogen',
				// displayField : 'Nitrogen_Container',
				// name : 'Nitrogen_Container',
				// store : NitrogenContStore,
				// typeAhead : true,
				// width : 300
				// }, {
				// xtype : 'combobox',
				// emptyText : 'Nitrogen Basket',
				// displayField : 'Nitrogen_Basket',
				// name : 'Nitrogen_Basket',
				// store : NitrogenBasketStore,
				// typeAhead : true,
				// width : 300
				// }, {
				// xtype : 'combobox',
				// emptyText : 'Nitrogen Layer',
				// displayField : 'Nitrogen_Layer',
				// name : 'Nitrogen_Layer',
				// store : NitrogenLayerStore,
				// typeAhead : true,
				// width : 300
				// }]
				// })
				// // others
				// var OtherTemperStore = Ext.create('Ext.data.Store', {
				// proxy : {
				// type : 'ajax',
				// url : '/experiments/ajax/display/Others_Temperature/',
				// reader : {
				// type : 'json',
				// root : 'Others_Temperatures'
				// }
				// },
				// fields : [{
				// name : 'Others_Temperature',
				// type : 'string'
				// }],
				// autoLoad : true
				// });
				// var OtherTemperPanel = Ext.create('Ext.container.Container',
				// {
				// // id : 'Location-Refrigerator',
				// layout : {
				// type : 'hbox'
				// },
				// defaults : {
				// labelWidth : 120,
				// width : 800
				// },
				// items : [{
				// xtype : 'combobox',
				// emptyText : 'Temperature',
				// fieldLabel : '#Others',
				// displayField : 'Others_Temperature',
				// name : 'Others_Temperature',
				// store : OtherTemperStore,
				// typeAhead : true,
				// width : 300
				// }, {
				// xtype : 'textfield',
				// emptyText : 'Location',
				// name : 'Others_location',
				// width : 300
				// }]
				// })
				// typeradio = Ext.getCmp('location' + timestamp);
				// typeradio.on('change', function(radio, newV, oldV, e) {
				// // console.log(oldV)
				// // console.log(newV)
				// if (oldV.location == 'Refrigerator') {
				// generalPanel.remove(RefrigeratorPanel, false)
				// } else if (oldV.location == 'Liquid Nitrogen') {
				// generalPanel.remove(NitrogenPanel, false)
				// } else if (oldV.location == 'Others') {
				// generalPanel.remove(OtherTemperPanel, false)
				// }
				// if (newV.location == 'Refrigerator') {
				// generalPanel.insert(3, RefrigeratorPanel);
				// } else if (newV.location == 'Liquid Nitrogen') {
				// generalPanel.insert(3, NitrogenPanel);
				// } else if (newV.location == 'Others') {
				// generalPanel.insert(3, OtherTemperPanel);
				// }
				// });
				// tab = Ext.getCmp('content-panel')
				// tab.add({
				// id : 'edit_sample_tab',
				// title : 'Edit Sample',
				// iconCls : 'addsample',
				// closable : true,
				// layout : 'fit',
				// items : [formPanel]
				// }).show()
				// };
				//				
				// EditSample=function(sampleID){
				//				    
				// Ext.Ajax.request({
				// url : '/experiments/load/sample/',
				// params : {
				// sample_no : sampleID
				// // csrfmiddlewaretoken : csrftoken
				// },
				// success : function(response) {
				//							
				// CreateSampleForm(sampleID, response);
				//							
				// //var panel = Ext.create('gar.view.Experiment_detail')
				// Ext.getCmp('edit_sample_tab').items.items[0].getForm().load({
				// url : '/experiments/load/sample/',
				// method : 'POST',
				// params : {
				// sample_no : sampleID
				// }
				// });
				// console.log("sampleID:" + sampleID);
				// var text = response.responseText;
				// responseJson = Ext.JSON.decode(text).data;
				//							
				// //Sample Location
				// var sampleLocation =
				// Ext.getCmp('sample-general').getForm().findField('location');
				// if(responseJson.RefrigeratorLayer){
				// sampleLocation.items.items[0].setValue(true);
				// }else if(responseJson.Nitrogen_Layer){
				// sampleLocation.items.items[1].setValue(true);
				// }else{
				// sampleLocation.items.items[2].setValue(true);
				// }
				//							
				// //Source Type
				// var sampleSourceType =
				// Ext.getCmp('sample-general').getForm().findField('cell_tissue');
				//							
				// var geneListLength = 0;
				// var geneSymbolVar = "geneSymbol";
				// var GeneIDVar = "GeneID";
				// var geneTaxonVar = "geneTaxon";
				// var geneSmallList;
				// var Cmp_source_cell
				// var geneListVar
				//					       
				// //deal Source Type
				// if(responseJson.cell_tissue == "Tissue"){
				// sampleSourceType.items.items[0].setValue(true);
				// //sampleSourceType.items.items[1].setValue(false);
				// //sampleSourceType.items.items[2].setValue(false);
				// //sampleSourceType.items.items[3].setValue(false);
				//							    
				// if(responseJson.geneList[0] != ""){
				// console.log("responseJson.geneList[0] != ''");
				// Cmp_source_tissue = Ext.getCmp('source_tissue').getForm();
				// //Get form of "Tissue"
				// geneListVar = responseJson.geneList; //Get geneList :
				// ["g1|g1-001|10036", "g2|g2-002|10090"]
				// Ext.getCmp("source_tissue").items.items[5].setValue(geneListVar.length);
				// //Set Total number of Target Gene
				//								
				// if(geneListVar.length>0){
				// for(var
				// listIndex=0;listIndex<geneListVar.length;listIndex++){
				// geneSmallList = geneListVar[listIndex].split("|"); //Get
				// geneList[index].split("|") : ["g1", "g1-001", "10036"]
				//								
				// geneSymbolVar = "geneSymbol" + (listIndex+1); //Set name
				// "geneSymbol1"
				// Cmp_source_tissue.findField(geneSymbolVar).setValue(geneSmallList[0]);
				// //Set "geneSymbol" Value
				// GeneIDVar = "GeneID" + (listIndex+1);
				// Cmp_source_tissue.findField(GeneIDVar).setValue(geneSmallList[1]);
				// geneTaxonVar = "geneTaxon" + (listIndex+1);
				// Cmp_source_tissue.findField(geneTaxonVar).setValue(geneSmallList[2]);
				// }
				// }
				//							    
				// }
				// else{
				// Ext.getCmp("source_tissue").items.items[5].setValue(0);
				// }
				//						    
				// }else if(responseJson.cell_tissue == "Cell"){
				// //sampleSourceType.items.items[0].setValue(false);
				// sampleSourceType.items.items[1].setValue(true);
				// //sampleSourceType.items.items[2].setValue(false);
				// //sampleSourceType.items.items[3].setValue(false);
				//								
				// if(responseJson.geneList[0] != ""){
				// Cmp_source_cell = Ext.getCmp('source_cell').getForm();
				// geneListVar = responseJson.geneList;
				// Ext.getCmp("source_cell").items.items[3].setValue(geneListVar.length);
				//								
				// if(geneListVar.length>0){
				// for(var
				// listIndex=0;listIndex<geneListVar.length;listIndex++){
				// geneSmallList = geneListVar[listIndex].split("|");
				// console.log(geneSmallList);
				//									
				// geneSymbolVar = "geneSymbol" + (listIndex+1);
				// //console.log(geneSymbolVar + "---" + geneSmallList[0])
				// Cmp_source_cell.findField(geneSymbolVar).setValue(geneSmallList[0]);
				// GeneIDVar = "GeneID" + (listIndex+1);
				// //console.log(GeneIDVar + "---" + geneSmallList[1])
				// Cmp_source_cell.findField(GeneIDVar).setValue(geneSmallList[1]);
				// geneTaxonVar = "geneTaxon" + (listIndex+1);
				// //console.log(geneTaxonVar + "---" + geneSmallList[2])
				// Cmp_source_cell.findField(geneTaxonVar).setValue(geneSmallList[2]);
				// }
				// }
				// }
				// else{
				// Ext.getCmp("source_cell").items.items[3].setValue(0);
				// }
				//								
				//								
				//								
				// }else if(responseJson.cell_tissue == "Fluid"){
				// //sampleSourceType.items.items[0].setValue(false);
				// //sampleSourceType.items.items[1].setValue(false);
				// sampleSourceType.items.items[2].setValue(true);
				// //sampleSourceType.items.items[3].setValue(false);
				//								
				// if(responseJson.geneList[0] != ""){
				// Cmp_source_fluid = Ext.getCmp('source_fluid').getForm();
				// //Get form of "Fluid & Excreta"
				// geneListVar = responseJson.geneList; //Get geneList :
				// ["g1|g1-001|10036", "g2|g2-002|10090"]
				// Ext.getCmp("source_fluid").items.items[5].setValue(geneListVar.length);
				// //Set Total number of Target Gene
				//								
				// if(geneListVar.length>0){
				// for(var
				// listIndex=0;listIndex<geneListVar.length;listIndex++){
				// geneSmallList = geneListVar[listIndex].split("|"); //Get
				// geneList[index].split("|") : ["g1", "g1-001", "10036"]
				//								
				// geneSymbolVar = "geneSymbol" + (listIndex+1); //Set name
				// "geneSymbol1"
				// Cmp_source_fluid.findField(geneSymbolVar).setValue(geneSmallList[0]);
				// //Set "geneSymbol" Value
				// GeneIDVar = "GeneID" + (listIndex+1);
				// Cmp_source_fluid.findField(GeneIDVar).setValue(geneSmallList[1]);
				// geneTaxonVar = "geneTaxon" + (listIndex+1);
				// Cmp_source_fluid.findField(geneTaxonVar).setValue(geneSmallList[2]);
				// }
				// }
				// }
				// else{
				// Ext.getCmp("source_fluid").items.items[3].setValue(0);
				// }
				//								
				// }else{
				// //sampleSourceType.items.items[0].setValue(false);
				// //sampleSourceType.items.items[1].setValue(false);
				// //sampleSourceType.items.items[2].setValue(false);
				// sampleSourceType.items.items[3].setValue(true);
				// }
				//							
				// //Total number of Treatment
				// var totalNumberOfTreatment =
				// Ext.getCmp('sample-general').getForm().findField('treat_num');
				// totalNumberOfTreatment.setValue(responseJson.treatmentsCount);
				//							
				// var treatIndex;
				// //deal Treatment + No.
				// if(responseJson.treatmentsCount>0){
				// for(treatIndex=1;
				// treatIndex<=responseJson.treatmentsCount;treatIndex++){
				// console.log("pre--Rx_treatment");
				// Ext.getCmp('Treatment'+treatIndex).getForm().findField('Rx_treatment'+treatIndex).setValue(responseJson.rx_treatments[treatIndex-1]);
				// }
				// }
				//							
				// //deal Treatment + No.
				// if(responseJson.treatmentsCount>0){
				// for(treatIndex=1;
				// treatIndex<=responseJson.treatmentsCount;treatIndex++){
				// console.log("pre--Rx_treatment");
				// Ext.getCmp("treantment_detail"+treatIndex).setValue(responseJson.rx_treatments_detail[treatIndex-1]);
				//						            
				// console.log("pre--rx_duration")
				// Ext.getCmp("Treatment"+treatIndex).items.items[2].items.items[0].setValue(responseJson.rx_duration[treatIndex-1]);
				// Ext.getCmp("Treatment"+treatIndex).items.items[2].items.items[1].setValue(responseJson.rx_duration_time[treatIndex-1]);
				// }
				// }
				//							
				//							
				// //deal "Concentration"
				// var unitConcentration;
				// if(responseJson.treatmentsCount>0){
				// for(treatIndex=1;
				// treatIndex<=responseJson.treatmentsCount;treatIndex++){
				// if(responseJson.rx_treatments[treatIndex-1]!= "Gene
				// Engineering" && responseJson.rx_unit[treatIndex-1] !=
				// "Concentration"){
				// Ext.getCmp("samp-treat-unit"+treatIndex).items.items[1].setValue(responseJson.rx_unit[treatIndex-1]);
				// Ext.getCmp("samp-treat-unit"+treatIndex).items.items[2].setValue(responseJson.rx_unit_deatil1[treatIndex-1]);
				// }
				// if(responseJson.rx_treatments[treatIndex-1]!= "Gene
				// Engineering" && responseJson.rx_unit[treatIndex-1] ==
				// "Concentration"){
				// Ext.getCmp("samp-treat-unit"+treatIndex).items.items[1].setValue(responseJson.rx_unit[treatIndex-1]);
				// unitConcentration =
				// responseJson.rx_unit_deatil2[treatIndex-1].split("/");
				// Ext.getCmp("unit_detail2_" +
				// treatIndex).items.items[0].setValue(unitConcentration[0]);
				// Ext.getCmp("unit_detail2_" +
				// treatIndex).items.items[2].setValue(unitConcentration[1]);
				// }
				// }
				//							    
				// }
				//
				// }
				// });
				//					
				//					
				//					
				// }
				//				
				//				
				//				
				//				
				// /*********************EditSample*********************/

				/** *******************EditSample******************** */
				// The code of this part has been encoded in ShowSample.js
				CreateSampleForm = function(sample_id, response) {
					var panel = Ext.getCmp('edit_sample_tab'  + "_metadata");
					if (panel) {
						var main = Ext.getCmp("content-panel");
						main.setActiveTab(panel);
						return 0;
					}
					var timestamp = 'compare' + (new Date()).valueOf()
					// CSRF protection
					csrftoken = Ext.util.Cookies.get('csrftoken');
					var submitForm = function() {
						formpanel = Ext.getCmp(timestamp);
						var form = formpanel.getForm();
						if (form.isValid()) {
							Ext.Ajax.timeout = 180000;
							form.submit({
										url : '/experiments/editsave/sample/',
										params : {
											sample_no : sample_id
											// csrfmiddlewaretoken : csrftoken
										},
										waitMsg : 'Saving Sample......',
										//timeout : 300000,
										success : function(frm, act) {
											val = String(act.result.msg);
											len = val.legnth
											// console.log(len)
											// val=val.substring(1)
											if (val.length < 6) {
												for (i = val.length; i < 6; i++)
													val = '0' + val
											}
											Ext.Msg.alert('Success', 'Modify a sample successfully. Sample No: ' + val);
											// Ext.Msg.alert('Success', 'Sample
											// add complete. Sample No: ' +
											// Ext.encode(act.result.msg));
											
											//refresh Show Sample
											tabTitle = "Show Sample";
											//refreshShowTab(tabTitle);
											
										},
										failure : function(form, action) {
											Ext.Msg.alert('Failed', 'Modify a sample unsuccessfully. Contact admin.');
										}
									});
						}
					};
					var cancelForm = function() {
						formpanel = Ext.getCmp(timestamp);
						formpanel.getForm().reset();
					};
					// experimenter Model and store
					var companyStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/all_company/',
									reader : {
										type : 'json',
										root : 'all_company'
									}
								},
								fields : [{
											name : 'company',
											type : 'string'
										}],
								autoLoad : true
							});
					var labStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/all_lab/',
									reader : {
										type : 'json',
										root : 'all_lab'
									}
								},
								fields : [{
											name : 'lab',
											type : 'string'
										}],
								autoLoad : true
							});
					var experimenterStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/all_experimenter/',
									reader : {
										type : 'json',
										root : 'experimenters'
									}
								},
								fields : [{
											name : 'experimenter',
											type : 'string'
										}],
								autoLoad : true
							});
					var sourceTissueTaxonAorMStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/Source_TissueTaxonAorM/',
									reader : {
										type : 'json',
										root : 'Source_TissueTaxonAorM'
									}
								},
								fields : [{
											name : 'Source_TissueTaxonAorM',
											type : 'string'
										}],
								autoLoad : true
							});
					var sourceTissueTaxonIDStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/Source_TissueTaxonID/',
									reader : {
										type : 'json',
										root : 'tissueID'
									}
								},
								fields : [{
											name : 'tissueID',
											type : 'string'
										}],
								autoLoad : true
							});
					var sourceTissueTaxonNameStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/Source_TissueTaxonName/',
									reader : {
										type : 'json',
										root : 'tissueName'
									}
								},
								fields : [{
											name : 'tissueName',
											type : 'string'
										}],
								autoLoad : true
							});
					var geneIDStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Source_TissueTaxonID/',
									reader : {
										type : 'json',
										root : 'Source_TissueTaxonIDs'
									}
								},
								fields : [{
											name : 'Source_TissueTaxonID',
											type : 'string'
										}],
								autoLoad : true
							});
					var SourceTissueSystemStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/Source_TissueSystem/',
									reader : {
										type : 'json',
										root : 'Source_TissueSystem'
									}
								},
								fields : [{
											name : 'Source_TissueSystem',
											type : 'string'
										}],
								autoLoad : true
							});
					var SourceTissueOrganStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/Source_TissueOrgan/',
									reader : {
										type : 'json',
										root : 'Source_TissueOrgan'
									}
								},
								fields : [{
											name : 'Source_TissueOrgan',
											type : 'string'
										}],
								autoLoad : true
							});
					var SourceTissueStructureStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display2/Source_TissueStructure/',
									reader : {
										type : 'json',
										root : 'Source_TissueStructure'
									}
								},
								fields : [{
											name : 'Source_TissueStructure',
											type : 'string'
										}],
								autoLoad : true
							});
					var SourceTissueTypeStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Source_TissueType/',
									reader : {
										type : 'json',
										root : 'Source_TissueTypes'
									}
								},
								fields : [{
											name : 'Source_TissueType',
											type : 'string'
										}],
								autoLoad : true
							});
					var sourceTissueTaxonStrainStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/Source_TissueTaxonStrain/',
									reader : {
										type : 'json',
										root : 'tissueStrain'
									}
								},
								fields : [{
											name : 'tissueStrain',
											type : 'string'
										}],
								autoLoad : true
							});
					var sourceTaxonStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Source_taxon/',
									reader : {
										type : 'json',
										root : 'Source_taxons'
									}
								},
								fields : [{
											name : 'Source_taxon',
											type : 'string'
										}],
								autoLoad : true
							});
					var allAgeUnitStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/All_AgeUnit/',
									reader : {
										type : 'json',
										root : 'All_AgeUnits'
									}
								},
								fields : [{
											name : 'All_AgeUnit',
											type : 'string'
										}],
								autoLoad : true
							});
					var rxUnitStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Rx_unit/',
									reader : {
										type : 'json',
										root : 'Rx_units'
									}
								},
								fields : [{
											name : 'Rx_unit',
											type : 'string'
										}],
								autoLoad : true
							});
					var rxUnitDetailStore = Ext.create('Ext.data.Store', {
						proxy : {
							type : 'ajax',
							url : '/experiments/ajax/unit_detail/',
							reader : {
								type : 'json',
								root : 'unit_detail'
							}
						},
						fields : [{
									name : 'unit_detail',
									type : 'string'
								}]
							// autoLoad : true
						});
					var rxTreatmentStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Rx_treatment/',
									reader : {
										type : 'json',
										root : 'Rx_treatments'
									}
								},
								fields : [{
											name : 'Rx_treatment',
											type : 'string'
										}],
								autoLoad : true
							});
					var rxTreatmentDetailStore = Ext.create('Ext.data.Store', {
						proxy : {
							type : 'ajax',
							url : '/experiments/ajax/treatment_detail/',
							reader : {
								type : 'json',
								root : 'all_detail'
							}
						},
						fields : [{
									name : 'all_detail',
									type : 'string'
								}]
							// autoLoad : true
						});
					var ubiSubcellStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Ubi_subcell/',
									reader : {
										type : 'json',
										root : 'Ubi_subcells'
									}
								},
								fields : [{
											name : 'Ubi_subcell',
											type : 'string'
										}],
								autoLoad : true
							});
					var ubiMethodStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Ubi_method/',
									reader : {
										type : 'json',
										root : 'Ubi_methods'
									}
								},
								fields : [{
											name : 'Ubi_method',
											type : 'string'
										}],
								autoLoad : true
							});
					var genotypeStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Genotype/',
									reader : {
										type : 'json',
										root : 'Genotypes'
									}
								},
								fields : [{
											name : 'Genotype',
											type : 'string'
										}],
								autoLoad : true
							});
					var cellTypeStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Cell_type/',
									reader : {
										type : 'json',
										root : 'Cell_types'
									}
								},
								fields : [{
											name : 'Cell_type',
											type : 'string'
										}],
								autoLoad : true
							});
					var cellcellTypeStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/source_CellType/',
									reader : {
										type : 'json',
										root : 'source_CellTypes'
									}
								},
								fields : [{
											name : 'source_CellType',
											type : 'string'
										}],
								autoLoad : true
							});
					var cellnameStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display2/Cell_Name/',
									reader : {
										type : 'json',
										root : 'Cell_Name'
									}
								},
								fields : [{
											name : 'Cell_Name',
											type : 'string'
										}],
								autoLoad : true
							});
					var tissueTypeStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Tissue_type/',
									reader : {
										type : 'json',
										root : 'Tissue_types'
									}
								},
								fields : [{
											name : 'Tissue_type',
											type : 'string'
										}],
								autoLoad : true
							});
					var tissueGenderStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Tissue_gender/',
									reader : {
										type : 'json',
										root : 'Tissue_genders'
									}
								},
								fields : [{
											name : 'Tissue_gender',
											type : 'string'
										}],
								autoLoad : true
							});
					var fluidNameStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Fluid_name/',
									reader : {
										type : 'json',
										root : 'Fluid_names'
									}
								},
								fields : [{
											name : 'Fluid_name',
											type : 'string'
										}],
								autoLoad : true
							});
					var ContainNoStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/ContainNoStore/',
									reader : {
										type : 'json',
										root : 'ContainNo'
									}
								},
								fields : [{
											name : 'ContainNo',
											type : 'string'
										}]
							});
					var ContainBasketStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/ContainBasketStore/',
									reader : {
										type : 'json',
										root : 'ContainBasket'
									}
								},
								fields : [{
											name : 'ContainBasket',
											type : 'string'
										}]
							});
					var ContainLayerStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/ContainLayerStore/',
									reader : {
										type : 'json',
										root : 'ContainLayer'
									}
								},
								fields : [{
											name : 'ContainLayer',
											type : 'string'
										}]
							});
					// general panel
					var generalPanel = Ext.create('Ext.form.Panel', {
								title : 'General',
								id : 'sample-general' + '-edit',
								// frame : true,
								storeId : 'methods',
								layout : 'auto',
								headerPosition : 'top',
								bodyPadding : 10,
								defaults : {
									labelWidth : 120,
									labelAligh : 'left',
									width : 1000,
									allowBlank : false
								},
								items : [{
											fieldLabel : 'Experimenter',
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											defaults : {
												editable : false
											},
											items : [{
														xtype : 'combobox',
														displayField : 'company',
														name : 'company',
														valueField : 'company',
														store : companyStore,
														queryMode : 'local',
														allowBlank : false,
														emptyText : 'Company',
														width : 300,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	var lab = Ext.getCmp("lab" + '-edit');
																	lab.clearValue();
																	lab.store.load({
																				params : {
																					id : records[0].data.company
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'lab',
														valueField : 'lab',
														name : 'lab',
														id : 'lab' + '-edit',
														emptyText : 'Laboratory',
														store : labStore,
														queryMode : 'local',
														allowBlank : false,
														width : 200,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	var experimenter = Ext.getCmp("experimenter" + '-edit');
																	experimenter.clearValue();
																	experimenter.store.load({
																				params : {
																					id : records[0].data.lab
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'experimenter',
														valueField : 'experimenter',
														emptyText : 'Experimenter',
														name : 'experimenter',
														id : 'experimenter' + '-edit',
														store : experimenterStore,
														queryMode : 'local',
														allowBlank : false,
														width : 180
													}]
										}, {
											xtype : 'datefield',
											fieldLabel : 'Date',
											value : Ext.Date.format(new Date(), 'n/d/Y'),
											emptyText : 'Date',
											name : 'date',
											width : '200'
										}, {
											xtype : 'radiogroup',
											fieldLabel : 'Sample Location',
											name : 'location',
											id : 'location' + '-edit',
											columns : 3,
											items : [{
														boxLabel : 'Refrigerator',
														name : 'location',
														inputValue : 'Refrigerator'
													}, {
														boxLabel : 'Liquid Nitrogen',
														name : 'location',
														inputValue : 'Liquid Nitrogen'
													}, {
														boxLabel : 'Others',
														name : 'location',
														inputValue : 'Others'
													}]
										}, {
											xtype : 'radiogroup',
											fieldLabel : 'Source Type',
											name : 'cell_tissue',
											id : 'cell_tissue' + '-edit',
											columns : 2,
											items : [{
														boxLabel : 'Tissue',
														name : 'cell_tissue',
														inputValue : 'Tissue'
													}, {
														boxLabel : 'Cell \& MicroOrganism',
														name : 'cell_tissue',
														inputValue : 'Cell'
													}, {
														boxLabel : 'Fluid & Excreta',
														name : 'cell_tissue',
														inputValue : 'Fluid'
													}, {
														boxLabel : 'Others',
														name : 'cell_tissue',
														inputValue : 'Others'
													}]
										}, {
											xtype : 'numberfield',
											fieldLabel : 'Total number of Treatment',
											// afterLabelTextTpl : required,
											id : 'treat_num' + '-edit',
											name : 'treat_num',
											minValue : 0,
											maxValue : 10,
											value : 0,
											listeners : {
												change : function(o, newV, oldV) {
													if (newV > 10) {
														alert('Number of treatment must be smaller than 10!')
														newV = 1
														Ext.getCmp('treat_num' + '-edit').setValue(1)
													}
													if (oldV) {
														delTreatment(oldV);
													}
													for (i = 1; i <= newV; i++) {
														addTreatment(i + 1, i);
													}
												}
											},
											width : 240
										}, {
											xtype : 'hiddenfield',
											name : 'csrfmiddlewaretoken',
											value : csrftoken
										}]
							});
					// source tissue panel
					var addGene = function(where, index, samplenum) {
						var sample = {
							fieldLabel : 'Target Gene ' + samplenum,
							xtype : 'fieldcontainer',
							id : 'target_Gene' + samplenum + '-edit',
							layout : {
								type : 'hbox',
								align : 'stretch'
							},
							items : [{
										xtype : 'textfield',
										emptyText : 'Gene Symbol',
										// fieldLabel : 'Target
										// Gene',
										name : 'geneSymbol' + samplenum,
										allowBlank : true
									}, {
										xtype : 'textfield',
										emptyText : 'Gene ID',
										// fieldLabel : 'Target
										// Gene',
										name : 'GeneID' + samplenum,
										allowBlank : true
									}, {
										xtype : 'combobox',
										displayField : 'Source_TissueTaxonID',
										valueField : 'Source_TissueTaxonID',
										emptyText : 'TaxonID',
										name : 'geneTaxon' + samplenum,
										store : geneIDStore,
										queryMode : 'local',
										allowBlank : true,
										width : 150
									}]
						};
						var temp = Ext.getCmp(where);
						// console.log(temp)
						temp.insert(index, sample);
					}
					var delGene = function(where, samplenum) {
						for (i = samplenum; i > 0; i--) {
							var sample = Ext.getCmp('target_Gene' + i + '-edit');
							var temp = Ext.getCmp(where);
							temp.remove(sample);
						}
					};
					var source_tissue = Ext.create('Ext.form.Panel', {
								title : 'Tissue',
								border : true,
								// frame : true,
								id : 'source_tissue' + '-edit',
								bodyPadding : 10,
								headerPosition : 'left',
								defaults : {
									labelWidth : 120,
									labelAligh : 'left',
									width : 800,
									allowBlank : false
								},
								items : [{
											fieldLabel : 'Taxon',
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											items : [{
														xtype : 'combobox',
														displayField : 'Source_TissueTaxonAorM',
														name : 'Source_TissueTaxonAorM',
														valueField : 'Source_TissueTaxonAorM',
														store : new Ext.data.SimpleStore({
																	fields : ["Source_TissueTaxonAorM"],
																	data : [["Animal"], ["Plant"]]
																}),
														queryMode : 'local',
														allowBlank : false,
														width : 120,
														emptyText : 'Animal/Plant',
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	var lab = Ext.getCmp("tissueName" + '-edit');
																	lab.clearValue();
																	lab.store.load({
																				params : {
																					id : records[0].data.Source_TissueTaxonAorM
																				}
																			})
																	var lab = Ext.getCmp("tissue-system" + '-edit');
																	lab.clearValue();
																	lab.store.load({
																				params : {
																					id : records[0].data.Source_TissueTaxonAorM
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'tissueName',
														valueField : 'tissueName',
														name : 'tissueName',
														id : 'tissueName' + '-edit',
														emptyText : 'Taxon Name',
														store : sourceTissueTaxonNameStore,
														queryMode : 'local',
														allowBlank : false,
														width : 300,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	// console.log(records)
																	var experimenter = Ext.getCmp("tissueID" + '-edit');
																	experimenter.clearValue();
																	experimenter.store.load({
																				params : {
																					id : records[0].data.tissueName
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'tissueID',
														valueField : 'tissueID',
														emptyText : 'Taxon ID',
														name : 'tissueID',
														id : 'tissueID' + '-edit',
														store : sourceTissueTaxonIDStore,
														queryMode : 'local',
														allowBlank : false,
														width : 100,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	// console.log(records)
																	var experimenter = Ext.getCmp("Tissue_strain" + '-edit');
																	experimenter.clearValue();
																	experimenter.store.load({
																				params : {
																					id : records[0].data.tissueID
																				}
																			})
																}
															}
														}
													}]
										}, {
											xtype : 'combobox',
											fieldLabel : 'Strain',
											id : 'Tissue_strain' + '-edit',
											emptyText : 'Strain Name',
											valueField : 'tissueStrain',
											displayField : 'tissueStrain',
											name : 'tissueStrain',
											queryMode : 'local',
											store : sourceTissueTaxonStrainStore
										}, {
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											fieldLabel : 'Age',
											items : [{
														xtype : 'textfield',
														name : 'tissue_age'
													}, {
														xtype : 'combobox',
														displayField : 'All_AgeUnit',
														valueField : 'All_AgeUnit',
														name : 'All_AgeUnit',
														store : allAgeUnitStore,
														queryMode : 'local',
														allowBlank : false,
														width : 180
													}]
										}, {
											xtype : 'combobox',
											fieldLabel : 'Gender',
											displayField : 'Tissue_gender',
											name : 'Tissue_gender',
											store : tissueGenderStore,
											width : 300
										}, {
											xtype : 'combobox',
											fieldLabel : 'Genotype',
											displayField : 'Genotype',
											name : 'Genotype',
											store : genotypeStore
										}, {
											xtype : 'numberfield',
											fieldLabel : 'Total number of Target Gene',
											// afterLabelTextTpl : required,
											id : 'Gene_num_tissue',
											name : 'Gene_num',
											minValue : 0,
											maxValue : 10,
											value : 0,
											listeners : {
												change : function(o, newV, oldV) {
													if (newV > 10) {
														alert('Number of Gene must be smaller than 10!')
														newV = 1
														Ext.getCmp('Gene_num_tissue').setValue(1)
													}
													if (oldV) {
														delGene('source_tissue-edit', oldV);
													}
													for (i = 1; i <= newV; i++) {
														addGene('source_tissue-edit', i + 5, i);
													}
												}
											},
											width : 240
										}, {
											fieldLabel : 'Tissue',
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											items : [{
														xtype : 'combobox',
														displayField : 'Source_TissueSystem',
														name : 'Source_TissueSystem',
														valueField : 'Source_TissueSystem',
														id : 'tissue-system' + '-edit',
														store : SourceTissueSystemStore,
														queryMode : 'local',
														allowBlank : false,
														width : 180,
														emptyText : 'System',
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	var lab = Ext.getCmp("tissue-organ" + '-edit');
																	lab.clearValue();
																	lab.store.load({
																				params : {
																					id : records[0].data.Source_TissueSystem
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'Source_TissueOrgan',
														valueField : 'Source_TissueOrgan',
														name : 'Source_TissueOrgan',
														id : 'tissue-organ' + '-edit',
														emptyText : 'Organ',
														store : SourceTissueOrganStore,
														queryMode : 'local',
														allowBlank : false,
														width : 150,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	var lab = Ext.getCmp("tissue-structure" + '-edit');
																	lab.clearValue();
																	lab.store.load({
																				params : {
																					id : records[0].data.Source_TissueOrgan
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'Source_TissueStructure',
														valueField : 'Source_TissueStructure',
														name : 'Source_TissueStructure',
														id : 'tissue-structure' + '-edit',
														emptyText : 'Anatomical Structure',
														store : SourceTissueStructureStore,
														queryMode : 'local',
														allowBlank : false,
														width : 120
													}, {
														xtype : 'combobox',
														displayField : 'Source_TissueType',
														valueField : 'Source_TissueType',
														emptyText : 'Status',
														name : 'Source_TissueType',
														store : SourceTissueTypeStore,
														queryMode : 'local',
														allowBlank : false
													}]
										},
										// {
										// fieldLabel : 'Target Gene',
										// xtype : 'fieldcontainer',
										// layout : {
										// type : 'hbox',
										// align : 'stretch'
										// },
										// items : [{
										// xtype : 'textfield',
										// emptyText : 'Gene Symbol',
										// // fieldLabel : 'Target
										// // Gene',
										// name : 'geneSymbol',
										// allowBlank : true
										// }, {
										// xtype : 'textfield',
										// emptyText : 'Gene ID',
										// // fieldLabel : 'Target
										// // Gene',
										// name : 'GeneID',
										// allowBlank : true
										// }, {
										// xtype : 'combobox',
										// displayField :
										// 'Source_TissueTaxonID',
										// valueField : 'Source_TissueTaxonID',
										// emptyText : 'Gene Taxon',
										// name : 'geneTaxon',
										// store : geneIDStore,
										// queryMode : 'local',
										// allowBlank : true,
										// width : 100
										// }]
										// },
										{
											xtype : 'timefield',
											fieldLabel : 'CR Time',
											format : 'G:i:s',
											increment : 15,
											name : 'circ_time',
											allowBlank : true
										}, {
											xtype : 'textfield',
											fieldLabel : 'Specific ID',
											name : 'Specific_ID',
											allowBlank : true
										}]
							});
					// source cell panel
					var source_cell = Ext.create('Ext.form.Panel', {
								id : 'source_cell' + '-edit',
								title : 'Cell and MicroOrganism',
								border : true,
								// frame : true,
								bodyPadding : 10,
								headerPosition : 'left',
								defaults : {
									labelWidth : 120,
									labelAligh : 'left',
									width : 800,
									allowBlank : false
								},
								items : [{
											fieldLabel : 'Taxon',
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											items : [{
														xtype : 'combobox',
														displayField : 'Source_TissueTaxonAorM',
														name : 'Source_TissueTaxonAorM',
														emptyText : 'Cell/MicroOrganism',
														valueField : 'Source_TissueTaxonAorM',
														store : new Ext.data.SimpleStore({
																	fields : ["Source_TissueTaxonAorM"],
																	data : [["Animal"], ["Microorganism"]]
																}),
														queryMode : 'local',
														allowBlank : false,
														width : 120,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	var lab = Ext.getCmp("cellName" + '-edit');
																	lab.clearValue();
																	lab.store.load({
																				params : {
																					id : records[0].data.Source_TissueTaxonAorM
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'tissueName',
														valueField : 'tissueName',
														name : 'tissueName',
														id : 'cellName' + '-edit',
														emptyText : 'Taxon Name',
														store : sourceTissueTaxonNameStore,
														queryMode : 'local',
														allowBlank : false,
														width : 300,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	// console.log(records)
																	var experimenter = Ext.getCmp("cellID" + '-edit');
																	experimenter.clearValue();
																	experimenter.store.load({
																				params : {
																					id : records[0].data.tissueName
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'tissueID',
														valueField : 'tissueID',
														emptyText : 'Taxon ID',
														name : 'tissueID',
														id : 'cellID' + '-edit',
														store : sourceTissueTaxonIDStore,
														queryMode : 'local',
														allowBlank : false,
														width : 100,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	// console.log(records)
																	var experimenter = Ext.getCmp("cellstrain" + '-edit');
																	experimenter.clearValue();
																	experimenter.store.load({
																				params : {
																					id : records[0].data.tissueID
																				}
																			})
																}
															}
														}
													}]
										}, {
											xtype : 'combobox',
											fieldLabel : 'Strain',
											emptyText : 'Strain Name',
											id : 'cellstrain' + '-edit',
											queryMode : 'local',
											valueField : 'tissueStrain',
											displayField : 'tissueStrain',
											name : 'tissueStrain',
											store : sourceTissueTaxonStrainStore
										}, {
											xtype : 'combobox',
											fieldLabel : 'Genotype',
											displayField : 'Genotype',
											name : 'Genotype',
											store : genotypeStore
										}, {
											xtype : 'numberfield',
											fieldLabel : 'Total number of Target Gene',
											// afterLabelTextTpl : required,
											id : 'Gene_num_cell',
											name : 'Gene_num',
											minValue : 0,
											maxValue : 10,
											value : 0,
											listeners : {
												change : function(o, newV, oldV) {
													if (newV > 10) {
														alert('Number of Gene must be smaller than 10!')
														newV = 1
														Ext.getCmp('Gene_num_cell').setValue(1)
													}
													if (oldV) {
														delGene('source_cell-edit', oldV);
													}
													for (i = 1; i <= newV; i++) {
														addGene('source_cell-edit', i + 3, i);
													}
												}
											},
											width : 240
										}, {
											fieldLabel : 'Cell',
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											items : [{
														xtype : 'combobox',
														displayField : 'source_CellType',
														name : 'cellcelltype',
														emptyText : 'Type',
														valueField : 'source_CellType',
														store : cellcellTypeStore,
														queryMode : 'local',
														width : 300,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	var lab = Ext.getCmp("cellcellname" + '-edit');
																	lab.clearValue();
																	lab.store.load({
																				params : {
																					id : records[0].data.source_CellType
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'Cell_Name',
														emptyText : 'Name',
														valueField : 'Cell_Name',
														name : 'Cell_Name',
														id : 'cellcellname' + '-edit',
														store : cellnameStore,
														queryMode : 'local',
														width : 300
													}]
										},
										// {
										// fieldLabel : 'Target Gene',
										// xtype : 'fieldcontainer',
										// layout : {
										// type : 'hbox',
										// align : 'stretch'
										// },
										// items : [{
										// xtype : 'textfield',
										// emptyText : 'Gene Symbol',
										// // fieldLabel : 'Target
										// // Gene',
										// name : 'geneSymbol',
										// allowBlank : true
										// }, {
										// xtype : 'textfield',
										// emptyText : 'Gene ID',
										// // fieldLabel : 'Target
										// // Gene',
										// name : 'GeneID',
										// allowBlank : true
										// }, {
										// xtype : 'combobox',
										// displayField :
										// 'Source_TissueTaxonID',
										// valueField : 'Source_TissueTaxonID',
										// emptyText : 'Gene Taxon',
										// name : 'geneTaxon',
										// store : geneIDStore,
										// queryMode : 'local',
										// allowBlank : true,
										// width : 100
										// }]
										// },
										{
											xtype : 'timefield',
											fieldLabel : 'CR Time',
											format : 'G:i:s',
											increment : 15,
											name : 'circ_time',
											allowBlank : true
										}, {
											xtype : 'textfield',
											fieldLabel : 'Specific ID',
											name : 'Specific_ID',
											allowBlank : true
										}]
							});
					var source_fluid = Ext.create('Ext.form.Panel', {
								id : 'source_fluid' + '-edit',
								title : 'Fluid & Excreta',
								border : true,
								bodyPadding : 10,
								// frame : true,
								headerPosition : 'left',
								defaults : {
									labelWidth : 120,
									labelAligh : 'left',
									width : 800,
									allowBlank : false
								},
								items : [{
											fieldLabel : 'Taxon',
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											items : [{
														xtype : 'combobox',
														displayField : 'Source_TissueTaxonAorM',
														name : 'Source_TissueTaxonAorM',
														valueField : 'Source_TissueTaxonAorM',
														store : new Ext.data.SimpleStore({
																	fields : ["Source_TissueTaxonAorM"],
																	data : [["Animal"], ["Plant"]]
																}),
														queryMode : 'local',
														allowBlank : false,
														emptyText : 'Animal/Plant',
														width : 120,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	var lab = Ext.getCmp("fluidName" + '-edit');
																	lab.clearValue();
																	lab.store.load({
																				params : {
																					id : records[0].data.Source_TissueTaxonAorM
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'tissueName',
														valueField : 'tissueName',
														emptyText : 'Taxon Name',
														name : 'tissueName',
														id : 'fluidName' + '-edit',
														store : sourceTissueTaxonNameStore,
														queryMode : 'local',
														allowBlank : false,
														width : 300,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	// console.log(records)
																	var experimenter = Ext.getCmp("fluidID" + '-edit');
																	experimenter.clearValue();
																	experimenter.store.load({
																				params : {
																					id : records[0].data.tissueName
																				}
																			})
																}
															}
														}
													}, {
														xtype : 'combobox',
														displayField : 'tissueID',
														valueField : 'tissueID',
														emptyText : 'Taxon ID',
														name : 'tissueID',
														id : 'fluidID' + '-edit',
														store : sourceTissueTaxonIDStore,
														queryMode : 'local',
														allowBlank : false,
														width : 100,
														listeners : {
															select : {
																fn : function(combo, records, index) {
																	// console.log(records)
																	var experimenter = Ext.getCmp("fluidstrain" + '-edit');
																	experimenter.clearValue();
																	experimenter.store.load({
																				params : {
																					id : records[0].data.tissueID
																				}
																			})
																}
															}
														}
													}]
										}, {
											xtype : 'combobox',
											fieldLabel : 'Strain',
											id : 'fluidstrain' + '-edit',
											valueField : 'tissueStrain',
											emptyText : 'Strain Name',
											displayField : 'tissueStrain',
											name : 'tissueStrain',
											store : sourceTissueTaxonStrainStore
										}, {
											fieldLabel : 'Age',
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											items : [{
														xtype : 'textfield',
														// fieldLabel : 'Target
														// Gene',
														name : 'tissue_age'
													}, {
														xtype : 'combobox',
														displayField : 'All_AgeUnit',
														valueField : 'All_AgeUnit',
														name : 'All_AgeUnit',
														// id : 'tissueName',
														store : allAgeUnitStore,
														queryMode : 'local',
														allowBlank : false,
														width : 180
													}]
										}, {
											xtype : 'combobox',
											fieldLabel : 'Gender',
											displayField : 'Tissue_gender',
											name : 'Tissue_gender',
											store : tissueGenderStore
										}, {
											xtype : 'combobox',
											fieldLabel : 'Genotype',
											displayField : 'Genotype',
											name : 'Genotype',
											store : genotypeStore
										}, {
											xtype : 'numberfield',
											fieldLabel : 'Total number of Target Gene',
											// afterLabelTextTpl : required,
											id : 'Gene_num_fluid',
											name : 'Gene_num',
											minValue : 0,
											maxValue : 10,
											value : 0,
											listeners : {
												change : function(o, newV, oldV) {
													if (newV > 10) {
														alert('Number of Gene must be smaller than 10!')
														newV = 1
														Ext.getCmp('Geme_num').setValue(1)
													}
													if (oldV) {
														delGene('source_fluid-edit', oldV);
													}
													for (i = 1; i <= newV; i++) {
														addGene('source_fluid-edit', i + 5, i);
													}
												}
											},
											width : 240
										},
										// {
										// fieldLabel : 'Target Gene',
										// xtype : 'fieldcontainer',
										// layout : {
										// type : 'hbox',
										// align : 'stretch'
										// },
										// items : [{
										// xtype : 'textfield',
										// emptyText : 'Gene Symbol',
										// // fieldLabel : 'Target
										// // Gene',
										// name : 'geneSymbol',
										// allowBlank : true
										// }, {
										// xtype : 'textfield',
										// emptyText : 'Gene ID',
										// // fieldLabel : 'Target
										// // Gene',
										// name : 'GeneID',
										// allowBlank : true
										// }, {
										// xtype : 'combobox',
										// displayField :
										// 'Source_TissueTaxonID',
										// valueField : 'Source_TissueTaxonID',
										// emptyText : 'Gene Taxon',
										// name : 'geneTaxon',
										// store : geneIDStore,
										// queryMode : 'local',
										// allowBlank : false,
										// width : 100,
										// allowBlank : true
										// }]
										// },
										{
											xtype : 'combobox',
											store : fluidNameStore,
											fieldLabel : 'Fluid/Excreta',
											displayField : 'Fluid_name',
											name : 'Fluid_name',
											valueField : 'Fluid_name'
										}, {
											xtype : 'textfield',
											fieldLabel : 'Specific ID',
											name : 'Specific_ID',
											allowBlank : true
										}]
							});
					var source_others = Ext.create('Ext.form.Panel', {
								title : 'Others',
								border : true,
								// frame : true,
								bodyPadding : 10,
								headerPosition : 'left',
								defaults : {
									labelWidth : 120,
									labelAligh : 'left',
									width : 450,
									allowBlank : false
								},
								items : [{
											xtype : 'textareafield',
											fieldLabel : 'Others',
											name : 'tissue_others'
										}]
							});
					// rx panel
					var addTreatment = function(index, treatnum) {
						var rxPanel = Ext.create('Ext.form.Panel', {
									title : 'Treatment' + treatnum,
									id : 'Treatment' + treatnum + '-edit',
									border : true,
									bodyPadding : 10,
									layout : 'anchor',
									headerPosition : 'top',
									defaults : {
										labelWidth : 120,
										labelAligh : 'left',
										width : 800,
										allowBlank : false
									},
									items : [{
										xtype : 'fieldcontainer',
										layout : {
											type : 'hbox',
											align : 'stretch'
										},
										items : [{
											xtype : 'combobox',
											fieldLabel : 'Treatments',
											displayField : 'Rx_treatment',
											name : 'Rx_treatment' + treatnum,
											store : rxTreatmentStore,
											queryMode : 'local',
											labelWidth : 120,
											width : 415,
											allowBlank : false,
											listeners : {
												select : {
													fn : function(combo, records, index) {
														var lab = Ext.getCmp("treantment_detail" + treatnum + '-edit');
														lab.clearValue();
														lab.store.load({
																	params : {
																		id : records[0].data.Rx_treatment
																	}
																})
													}
												},
												change : {
													fn : function(combo, newValue, oldValue) {
														// console.log(box)
														var sample = {
															fieldLabel : 'New Target Gene ',
															xtype : 'fieldcontainer',
															id : 'New_target_Gene' + treatnum + '-edit',
															layout : {
																type : 'hbox',
																align : 'stretch'
															},
															items : [{
																		xtype : 'textfield',
																		emptyText : 'Gene Symbol',
																		// fieldLabel
																		// :
																		// 'Target
																		// Gene',
																		name : 'newGeneSymbol' + treatnum,
																		value : responseJson.rx_geneSymbol[treatnum - 1],
																		allowBlank : true
																	}, {
																		xtype : 'textfield',
																		emptyText : 'Gene ID',
																		// fieldLabel
																		// :
																		// 'Target
																		// Gene',
																		name : 'newGeneID' + treatnum,
																		value : responseJson.rx_geneID[treatnum - 1],
																		allowBlank : true
																	}, {
																		xtype : 'combobox',
																		displayField : 'Source_TissueTaxonID',
																		valueField : 'Source_TissueTaxonID',
																		emptyText : 'Gene Taxon',
																		name : 'newGeneTaxon' + treatnum,
																		store : geneIDStore,
																		queryMode : 'local',
																		value : responseJson.rx_geneTaxon[treatnum - 1],
																		allowBlank : true,
																		width : 100
																	}]
														};
														var sample2 = {
															xtype : 'fieldcontainer',
															id : 'samp-treat-unit' + treatnum + '-edit',
															layout : {
																type : 'hbox',
																align : 'stretch'
															},
															items : [{
																		xtype : 'textfield',
																		fieldLabel : 'Amount',
																		name : 'amount' + treatnum,
																		width : 180,
																		labelWidth : 120,
																		value : responseJson.rx_amount[treatnum - 1],
																		allowBlank : true
																	}, {
																		xtype : 'combobox',
																		displayField : 'Rx_unit',
																		name : 'Rx_unit' + treatnum,
																		store : rxUnitStore,
																		queryMode : 'local',
																		emptyText : 'Param type',
																		// value
																		// :
																		// responseJson.rx_unit[treatnum-1],
																		allowBlank : true,
																		listeners : {
																			change : {
																				fn : function(box, newValue, oldValue) {
																					// console.log(box)
																					var detailPanel = Ext.create('Ext.form.ComboBox', {
																								id : 'unit_detail_' + treatnum + '-edit',
																								displayField : 'unit_detail',
																								name : 'unit_detail_' + treatnum,
																								store : rxUnitDetailStore,
																								queryMode : 'local',
																								emptyText : 'Param unit',
																								editable : false,
																								// value
																								// :
																								// responseJson.rx_unit_deatil1[treatnum-1],
																								allowBlank : true
																							})
																					var detailPanel2 = {
																						xtype : 'fieldcontainer',
																						id : 'unit_detail2_' + treatnum + '-edit',
																						layout : {
																							type : 'hbox',
																							align : 'stretch'
																						},
																						items : [{
																							xtype : 'combobox',
																							// id :
																							// 'detailPanel2-1',
																							valueField : 'rx_dur_unit',
																							displayField : 'rx_dur_unit',
																							name : 'unit_detail2_' + treatnum,
																							store : new Ext.data.SimpleStore({
																										fields : ["rx_dur_unit"],
																										data : [["L"], ["mL"], ["ng"], ["g"], ["kg"],
																												["mol"], ["mmol"]]
																									})
																						}, {
																							xtype : 'displayfield',
																							// id :
																							// 'detailPanel2-2',
																							value : ' / '
																						}, {
																							xtype : 'combobox',
																							// id :
																							// 'detailPanel22-1',
																							valueField : 'rx_dur_unit',
																							displayField : 'rx_dur_unit',
																							name : 'unit_detail22_' + treatnum,
																							store : new Ext.data.SimpleStore({
																										fields : ["rx_dur_unit"],
																										data : [["L"], ["mL"], ["uL"], ["nL"],
																												["Kg"], ["g"], ["mg"]]
																									})
																						}]
																					}
																					var temp = Ext.getCmp('samp-treat-unit' + treatnum + '-edit');
																					if (oldValue != 'Concentration')
																						temp.remove(Ext.getCmp('unit_detail_' + treatnum + '-edit'),
																								false)
																					else if (oldValue == 'Concentration') {
																						temp.remove(Ext.getCmp('unit_detail2_' + treatnum + '-edit'),
																								false)
																					}
																					if (newValue != 'Concentration') {
																						detailPanel.clearValue()
																						detailPanel.store.load({
																									params : {
																										id : newValue
																									}
																								})
																						temp.insert(2, detailPanel)
																					} else if (newValue == 'Concentration') {
																						temp.insert(2, detailPanel2)
																					}
																				}
																			}
																		}
																	}]
														}
														var temp = Ext.getCmp('Treatment' + treatnum + '-edit');
														// console.log(temp.items.items[2].id)
														// console.log(temp.items)
														// if (newValue != 'Gene
														// Engineering') {
														// if ('New_target_Gene'
														// + treatnum ==
														// temp.items.items[2].id){
														temp.remove(temp.items.items[1], false)
														// }
														// }
														if (newValue == 'Gene Engineering')
															temp.insert(1, sample)
														else {
															temp.insert(1, sample2)
														}
													}
												}
											}
										}, {
											xtype : 'combobox',
											id : 'treantment_detail' + treatnum + '-edit',
											// fieldLabel :
											// 'Treatments',
											displayField : 'all_detail',
											name : 'all_detail' + treatnum,
											store : rxTreatmentDetailStore,
											queryMode : 'local',
											labelWidth : 120,
											allowBlank : true
										}]
									}, {
										xtype : 'fieldcontainer',
										id : 'samp-treat-unit' + treatnum + '-edit',
										layout : {
											type : 'hbox',
											align : 'stretch'
										},
										items : [{
													xtype : 'textfield',
													fieldLabel : 'Amount',
													name : 'amount' + treatnum,
													width : 180,
													labelWidth : 120,
													allowBlank : true
												}, {
													xtype : 'combobox',
													displayField : 'Rx_unit',
													name : 'Rx_unit' + treatnum,
													store : rxUnitStore,
													queryMode : 'local',
													emptyText : 'Param type',
													allowBlank : true,
													listeners : {
														change : {
															fn : function(box, newValue, oldValue) {
																// console.log(box)
																var detailPanel = Ext.create('Ext.form.ComboBox', {
																			id : 'unit_detail_' + treatnum + '-edit',
																			displayField : 'unit_detail',
																			name : 'unit_detail' + treatnum,
																			store : rxUnitDetailStore,
																			queryMode : 'local',
																			emptyText : 'Param unit',
																			editable : false,
																			allowBlank : true
																		})
																var detailPanel2 = {
																	xtype : 'fieldcontainer',
																	id : 'unit_detail2_' + treatnum + '-edit',
																	layout : {
																		type : 'hbox',
																		align : 'stretch'
																	},
																	items : [{
																				xtype : 'combobox',
																				// id :
																				// 'detailPanel2-1',
																				valueField : 'rx_dur_unit',
																				displayField : 'rx_dur_unit',
																				name : 'unit_detail2' + treatnum,
																				store : new Ext.data.SimpleStore({
																							fields : ["rx_dur_unit"],
																							data : [["L"], ["mL"], ["ng"], ["g"], ["kg"], ["mol"], ["mmol"]]
																						})
																			}, {
																				xtype : 'displayfield',
																				// id :
																				// 'detailPanel2-2',
																				value : ' / '
																			}, {
																				xtype : 'combobox',
																				// id :
																				// 'detailPanel22-1',
																				valueField : 'rx_dur_unit',
																				displayField : 'rx_dur_unit',
																				name : 'unit_detail22' + treatnum,
																				store : new Ext.data.SimpleStore({
																							fields : ["rx_dur_unit"],
																							data : [["L"], ["mL"], ["uL"], ["nL"], ["Kg"], ["g"],
																									["mg"]]
																						})
																			}]
																}
																var temp = Ext.getCmp('samp-treat-unit' + treatnum + '-edit');
																if (oldValue != 'Concentration')
																	temp.remove(Ext.getCmp('unit_detail_' + treatnum + '-edit'), false)
																else if (oldValue == 'Concentration') {
																	temp.remove(Ext.getCmp('unit_detail2_' + treatnum + '-edit'), false)
																}
																if (newValue != 'Concentration') {
																	detailPanel.clearValue()
																	detailPanel.store.load({
																				params : {
																					id : newValue
																				}
																			})
																	temp.insert(2, detailPanel)
																} else if (newValue == 'Concentration') {
																	temp.insert(2, detailPanel2)
																}
															}
														}
													}
												}]
									}, {
										xtype : 'fieldcontainer',
										fieldLabel : 'Duration',
										layout : {
											type : 'hbox',
											align : 'stretch'
										},
										items : [{
													xtype : 'textfield',
													name : 'duration' + treatnum,
													labelWidth : 120,
													allowBlank : true
												}, {
													xtype : 'combobox',
													displayField : 'rx_dur_unit',
													name : 'rx_dur_unit' + treatnum,
													valueField : 'rx_dur_unit',
													store : new Ext.data.SimpleStore({
																fields : ["rx_dur_unit"],
																data : [["Week"], ["Day"], ["Hour"], ["Minute"], ["Second"]]
															}),
													queryMode : 'local',
													width : 200
												}]
									}]
								});
						formPanel.insert(index, rxPanel);
					};
					var delTreatment = function(samplenum) {
						for (i = samplenum; i > 0; i--) {
							var sample = Ext.getCmp('Treatment' + i + '-edit');
							formPanel.remove(sample);
						}
					};
					// var rxPanel = Ext.create('Ext.form.Panel', {
					// title : 'Treatment',
					// border : true,
					// bodyPadding : 10,
					// // frame : true,
					// // bodyStyle : 'padding: 5 5 0',
					// layout : 'anchor',
					// headerPosition : 'top',
					// defaults : {
					// labelWidth : 120,
					// labelAligh : 'left',
					// width : 800,
					// allowBlank : false
					// },
					// items : [{
					// xtype : 'fieldcontainer',
					// layout : {
					// type : 'hbox',
					// align : 'stretch'
					// },
					// items : [{
					// xtype : 'combobox',
					// fieldLabel : 'Treatments',
					// displayField : 'Rx_treatment',
					// name : 'Rx_treatment',
					// store : rxTreatmentStore,
					// queryMode : 'local',
					// labelWidth : 120,
					// width : 415,
					// allowBlank : false,
					// listeners : {
					// select : {
					// fn : function(combo, records, index) {
					// var lab = Ext.getCmp("treantment_detail");
					// lab.clearValue();
					// lab.store.load({
					// params : {
					// id : records[0].data.Rx_treatment
					// }
					// })
					// }
					// }
					// }
					// }, {
					// xtype : 'combobox',
					// id : 'treantment_detail',
					// // fieldLabel :
					// // 'Treatments',
					// displayField : 'all_detail',
					// name : 'all_detail',
					// store : rxTreatmentDetailStore,
					// queryMode : 'local',
					// labelWidth : 120,
					// allowBlank : true
					// }]
					// }, {
					// xtype : 'fieldcontainer',
					// id : 'samp-treat-unit',
					// layout : {
					// type : 'hbox',
					// align : 'stretch'
					// },
					// items : [{
					// xtype : 'textfield',
					// fieldLabel : 'Amount',
					// name : 'amount',
					// width : 180,
					// labelWidth : 120,
					// allowBlank : true
					// }, {
					// xtype : 'combobox',
					// displayField : 'Rx_unit',
					// name : 'Rx_unit',
					// store : rxUnitStore,
					// queryMode : 'local',
					// emptyText : 'Param type',
					// allowBlank : true,
					// listeners : {
					// change : {
					// fn : function(box, newValue, oldValue) {
					// // console.log(box)
					// var temp = Ext.getCmp('samp-treat-unit');
					// if (oldValue != 'Concentration')
					// temp.remove(detailPanel, false)
					// else if (oldValue == 'Concentration') {
					// temp.remove(Ext.getCmp('unit_detail2'), false)
					// }
					// if (newValue != 'Concentration') {
					// detailPanel.clearValue()
					// detailPanel.store.load({
					// params : {
					// id : newValue
					// }
					// })
					// temp.insert(2, detailPanel)
					// } else if (newValue == 'Concentration') {
					// temp.insert(2, detailPanel2)
					// }
					// }
					// }
					// }
					// }]
					// }, {
					// xtype : 'fieldcontainer',
					// layout : {
					// type : 'hbox',
					// align : 'stretch'
					// },
					// items : [{
					// xtype : 'textfield',
					// name : 'duration',
					// fieldLabel : 'Duration',
					// labelWidth : 120,
					// allowBlank : true
					// }, {
					// xtype : 'combobox',
					// displayField : 'rx_dur_unit',
					// name : 'rx_dur_unit',
					// valueField : 'rx_dur_unit',
					// store : new Ext.data.SimpleStore({
					// fields : ["rx_dur_unit"],
					// data : [["Week"], ["Day"], ["Hour"], ["Minute"],
					// ["Second"]]
					// }),
					// queryMode : 'local',
					// width : 200
					// }]
					// }]
					// });
					var ubiPanel = Ext.create('Ext.form.Panel', {
								title : 'Information',
								border : true,
								// frame : true,
								bodyPadding : 10,
								headerPosition : 'top',
								defaults : {
									labelWidth : 120,
									labelAligh : 'left',
									width : 800,
									allowBlank : false
								},
								items : [{
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											items : [{
														xtype : 'combobox',
														fieldLabel : 'Subcelluar Organelle',
														name : 'Ubi_subcell',
														displayField : 'Ubi_subcell',
														store : ubiSubcellStore,
														queryMode : 'local',
														multiSelect : true,
														editable : true,
														labelWidth : 120,
														width : 415,
														allowBlank : false
													}]
										}, {
											xtype : 'fieldcontainer',
											layout : {
												type : 'hbox',
												align : 'stretch'
											},
											items : [{
														xtype : 'combobox',
														valueField : 'Ubi_method',
														fieldLabel : 'Protocol',
														displayField : 'Ubi_method',
														name : 'Ubi_method',
														store : ubiMethodStore,
														// queryMode : 'local',
														multiSelect : true,
														labelWidth : 120,
														width : 800,
														allowBlank : false
													}]
										}, /*
											 * { xtype : 'combobox', name :
											 * 'Ubi_detergent', displayField :
											 * 'Ubi_detergent', fieldLabel :
											 * 'Detergent', store :
											 * ubiDetergentStore },
											 */{
											xtype : 'textfield',
											name : 'Ubi_salt',
											// displayField : 'Ubi_salt',
											fieldLabel : 'Salt'
											// store : ubiSaltStore
									}]
							});
					var commentsPanel = Ext.create('Ext.form.Panel', {
								title : 'Comments',
								border : true,
								// frame : true,
								bodyPadding : 10,
								headerPosition : 'top',
								defaults : {
									labelWidth : 120,
									// labelAlign : 'top',
									width : 800
									// allowBlank : false
								},
								items : [{
											xtype : 'textareafield',
											name : 'comments',
											fieldLabel : 'Extra Comments'
										}, 
//										{
//											xtype : 'textfield',
//											// fieldLabel : 'Target
//											// Gene',
//											name : 'Ispec_num',
//											fieldLabel : 'Ispec No',
//											width : 400
//										},
										{
											xtype : 'textfield',
											name : 'Ispec_num',
											fieldLabel : 'Ispec No',
											labelWidth : 120,
											allowBlank : true
										}]
							});
					var buttonPanel = Ext.create('Ext.panel.Panel', {
								// frame : true,
								// renderTo: 'button',
								buttonAlign : "center",
								buttons : [{
											text : 'Submit',
											handler : submitForm
										}, {
											text : 'Cancel',
											handler : cancelForm
										}]
							});
					var formPanel = Ext.create('Ext.form.Panel', {
								id : timestamp,
								// renderTo : 'form',
								overflowY : 'scroll',
								items : [generalPanel, ubiPanel, commentsPanel, buttonPanel]
							});
					// console.log(timestamp)
					// event listener for type radio
					typeradio = Ext.getCmp('cell_tissue' + '-edit');
					typeradio.on('change', function(radio, newV, oldV, e) {
								if (oldV.cell_tissue == 'Tissue') {
									formPanel.remove(source_tissue, false);
								} else if (oldV.cell_tissue == 'Cell') {
									formPanel.remove(source_cell, false);
								} else if (oldV.cell_tissue == 'Fluid') {
									formPanel.remove(source_fluid, false);
								} else if (oldV.cell_tissue == 'Others') {
									formPanel.remove(source_others, false);
								}
								if (newV.cell_tissue == 'Tissue') {
									formPanel.insert(1, source_tissue);
								} else if (newV.cell_tissue == 'Cell') {
									formPanel.insert(1, source_cell);
								} else if (newV.cell_tissue == 'Fluid') {
									formPanel.insert(1, source_fluid);
								} else if (newV.cell_tissue == 'Others') {
									formPanel.insert(1, source_others);
								}
							});
					// For Container
					var RefrigeratorNoStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Refrigerator_No/',
									reader : {
										type : 'json',
										root : 'Refrigerator_Nos'
									}
								},
								fields : [{
											name : 'Refrigerator_No',
											type : 'string'
										}],
								autoLoad : true
							});
					var RefrigeratorTemperStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Refrigerator_Temperature/',
									reader : {
										type : 'json',
										root : 'Refrigerator_Temperatures'
									}
								},
								fields : [{
											name : 'Refrigerator_Temperature',
											type : 'string'
										}],
								autoLoad : true
							});
					var RefrigeratorLayerStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Refrigerator_Layer/',
									reader : {
										type : 'json',
										root : 'Refrigerator_Layers'
									}
								},
								fields : [{
											name : 'Refrigerator_Layer',
											type : 'string'
										}],
								autoLoad : true
							});
					var RefrigeratorPanel = Ext.create('Ext.container.Container', {
								// id : 'Location-Refrigerator',
								layout : {
									type : 'hbox'
								},
								defaults : {
									labelWidth : 120,
									width : 800
								},
								items : [{
											xtype : 'combobox',
											emptyText : 'Refrigerator No.',
											fieldLabel : '#Refrigerator',
											displayField : 'Refrigerator_No',
											name : 'RefrigeratorNo',
											store : RefrigeratorNoStore,
											typeAhead : true,
											width : 300
										}, {
											xtype : 'combobox',
											emptyText : 'Temperature',
											displayField : 'Refrigerator_Temperature',
											name : 'RefrigeratorTemper',
											store : RefrigeratorTemperStore,
											typeAhead : true,
											width : 300
										}, {
											xtype : 'combobox',
											emptyText : 'Refrigerator Layer',
											displayField : 'Refrigerator_Layer',
											name : 'RefrigeratorLayer',
											store : RefrigeratorLayerStore,
											typeAhead : true,
											width : 300
										}]
							})
					// nitrogen-panel
					var NitrogenContStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Nitrogen_Container/',
									reader : {
										type : 'json',
										root : 'Nitrogen_Containers'
									}
								},
								fields : [{
											name : 'Nitrogen_Container',
											type : 'string'
										}],
								autoLoad : true
							});
					var NitrogenBasketStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Nitrogen_Basket/',
									reader : {
										type : 'json',
										root : 'Nitrogen_Baskets'
									}
								},
								fields : [{
											name : 'Nitrogen_Basket',
											type : 'string'
										}],
								autoLoad : true
							});
					var NitrogenLayerStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Nitrogen_Layer/',
									reader : {
										type : 'json',
										root : 'Nitrogen_Layers'
									}
								},
								fields : [{
											name : 'Nitrogen_Layer',
											type : 'string'
										}],
								autoLoad : true
							});
					var NitrogenPanel = Ext.create('Ext.container.Container', {
								// id : 'Location-Refrigerator',
								layout : {
									type : 'hbox'
								},
								defaults : {
									labelWidth : 120,
									width : 800
								},
								items : [{
											xtype : 'combobox',
											emptyText : 'Container No.',
											fieldLabel : '#Liquid Nitrogen',
											displayField : 'Nitrogen_Container',
											name : 'Nitrogen_Container',
											store : NitrogenContStore,
											typeAhead : true,
											width : 300
										}, {
											xtype : 'combobox',
											emptyText : 'Nitrogen Basket',
											displayField : 'Nitrogen_Basket',
											name : 'Nitrogen_Basket',
											store : NitrogenBasketStore,
											typeAhead : true,
											width : 300
										}, {
											xtype : 'combobox',
											emptyText : 'Nitrogen Layer',
											displayField : 'Nitrogen_Layer',
											name : 'Nitrogen_Layer',
											store : NitrogenLayerStore,
											typeAhead : true,
											width : 300
										}]
							})
					// others
					var OtherTemperStore = Ext.create('Ext.data.Store', {
								proxy : {
									type : 'ajax',
									url : '/experiments/ajax/display/Others_Temperature/',
									reader : {
										type : 'json',
										root : 'Others_Temperatures'
									}
								},
								fields : [{
											name : 'Others_Temperature',
											type : 'string'
										}],
								autoLoad : true
							});
					var OtherTemperPanel = Ext.create('Ext.container.Container', {
								// id : 'Location-Refrigerator',
								layout : {
									type : 'hbox'
								},
								defaults : {
									labelWidth : 120,
									width : 800
								},
								items : [{
											xtype : 'combobox',
											emptyText : 'Temperature',
											fieldLabel : '#Others',
											displayField : 'Others_Temperature',
											name : 'Others_Temperature',
											store : OtherTemperStore,
											typeAhead : true,
											width : 300
										}, {
											xtype : 'textfield',
											emptyText : 'Location',
											name : 'Others_location',
											width : 300
										}]
							})
					typeradio = Ext.getCmp('location' + '-edit');
					typeradio.on('change', function(radio, newV, oldV, e) {
								// console.log(oldV)
								// console.log(newV)
								if (oldV.location == 'Refrigerator') {
									generalPanel.remove(RefrigeratorPanel, false)
								} else if (oldV.location == 'Liquid Nitrogen') {
									generalPanel.remove(NitrogenPanel, false)
								} else if (oldV.location == 'Others') {
									generalPanel.remove(OtherTemperPanel, false)
								}
								if (newV.location == 'Refrigerator') {
									generalPanel.insert(3, RefrigeratorPanel);
								} else if (newV.location == 'Liquid Nitrogen') {
									generalPanel.insert(3, NitrogenPanel);
								} else if (newV.location == 'Others') {
									generalPanel.insert(3, OtherTemperPanel);
								}
							});
					tab = Ext.getCmp('content-panel')
					tab.add({
								id : 'edit_sample_tab' + "_metadata",
								title : 'Edit Sample ' + sample_id,
								iconCls : 'addsample',
								closable : true,
								layout : 'fit',
								items : [formPanel]
							}).show()
				};

				EditSample = function(sampleID) {

					Ext.Ajax.request({
								url : '/experiments/load/sample/',
								params : {
									sample_no : sampleID
									// csrfmiddlewaretoken : csrftoken
								},
								success : function(response) {

									CreateSampleForm(sampleID, response);

									// var panel =
									// Ext.create('gar.view.Experiment_detail')
									Ext.getCmp('edit_sample_tab'  + "_metadata").items.items[0].getForm().load({
												url : '/experiments/load/sample/',
												method : 'POST',
												params : {
													sample_no : sampleID
												}
											});
									console.log("sampleID:" + sampleID);
									var text = response.responseText;
									responseJson = Ext.JSON.decode(text).data;

									// Sample Location
									var sampleLocation = Ext.getCmp('sample-general' + '-edit').getForm().findField('location');
									if (responseJson.RefrigeratorLayer) {
										sampleLocation.items.items[0].setValue(true);
									} else if (responseJson.Nitrogen_Layer) {
										sampleLocation.items.items[1].setValue(true);
									} else {
										sampleLocation.items.items[2].setValue(true);
									}

									// Source Type
									var sampleSourceType = Ext.getCmp('sample-general' + '-edit').getForm().findField('cell_tissue');

									var geneListLength = 0;
									var geneSymbolVar = "geneSymbol";
									var GeneIDVar = "GeneID";
									var geneTaxonVar = "geneTaxon";
									var geneSmallList;
									var Cmp_source_cell
									var geneListVar

									// deal Source Type
									if (responseJson.cell_tissue == "Tissue") {
										sampleSourceType.items.items[0].setValue(true);
										// sampleSourceType.items.items[1].setValue(false);
										// sampleSourceType.items.items[2].setValue(false);
										// sampleSourceType.items.items[3].setValue(false);

										if (responseJson.geneList[0] != "") {
											console.log("responseJson.geneList[0] != ''");
											Cmp_source_tissue = Ext.getCmp('source_tissue' + '-edit').getForm(); // Get
																													// form
																													// of
																													// "Tissue"
											geneListVar = responseJson.geneList; // Get
																					// geneList
																					// :
																					// ["g1|g1-001|10036",
																					// "g2|g2-002|10090"]
											Ext.getCmp("source_tissue" + '-edit').items.items[5].setValue(geneListVar.length); // Set
																																// Total
																																// number
																																// of
																																// Target
																																// Gene

											if (geneListVar.length > 0) {
												for (var listIndex = 0; listIndex < geneListVar.length; listIndex++) {
													geneSmallList = geneListVar[listIndex].split("|"); // Get
																										// geneList[index].split("|")
																										// :
																										// ["g1",
																										// "g1-001",
																										// "10036"]

													geneSymbolVar = "geneSymbol" + (listIndex + 1); // Set
																									// name
																									// "geneSymbol1"
													Cmp_source_tissue.findField(geneSymbolVar).setValue(geneSmallList[0]); // Set
																															// "geneSymbol"
																															// Value
													GeneIDVar = "GeneID" + (listIndex + 1);
													Cmp_source_tissue.findField(GeneIDVar).setValue(geneSmallList[1]);
													geneTaxonVar = "geneTaxon" + (listIndex + 1);
													Cmp_source_tissue.findField(geneTaxonVar).setValue(geneSmallList[2]);
												}
											}

										} else {
											Ext.getCmp("source_tissue" + '-edit').items.items[5].setValue(0);
										}

									} else if (responseJson.cell_tissue == "Cell") {
										// sampleSourceType.items.items[0].setValue(false);
										sampleSourceType.items.items[1].setValue(true);
										// sampleSourceType.items.items[2].setValue(false);
										// sampleSourceType.items.items[3].setValue(false);

										if (responseJson.geneList[0] != "") {
											Cmp_source_cell = Ext.getCmp('source_cell' + '-edit').getForm();
											geneListVar = responseJson.geneList;
											Ext.getCmp("source_cell" + '-edit').items.items[3].setValue(geneListVar.length);

											if (geneListVar.length > 0) {
												for (var listIndex = 0; listIndex < geneListVar.length; listIndex++) {
													geneSmallList = geneListVar[listIndex].split("|");
													console.log(geneSmallList);

													geneSymbolVar = "geneSymbol" + (listIndex + 1);
													// console.log(geneSymbolVar
													// + "---" +
													// geneSmallList[0])
													Cmp_source_cell.findField(geneSymbolVar).setValue(geneSmallList[0]);
													GeneIDVar = "GeneID" + (listIndex + 1);
													// console.log(GeneIDVar +
													// "---" + geneSmallList[1])
													Cmp_source_cell.findField(GeneIDVar).setValue(geneSmallList[1]);
													geneTaxonVar = "geneTaxon" + (listIndex + 1);
													// console.log(geneTaxonVar
													// + "---" +
													// geneSmallList[2])
													Cmp_source_cell.findField(geneTaxonVar).setValue(geneSmallList[2]);
												}
											}
										} else {
											Ext.getCmp("source_cell" + '-edit').items.items[3].setValue(0);
										}

									} else if (responseJson.cell_tissue == "Fluid") {
										// sampleSourceType.items.items[0].setValue(false);
										// sampleSourceType.items.items[1].setValue(false);
										sampleSourceType.items.items[2].setValue(true);
										// sampleSourceType.items.items[3].setValue(false);

										if (responseJson.geneList[0] != "") {
											Cmp_source_fluid = Ext.getCmp('source_fluid' + '-edit').getForm(); // Get
																												// form
																												// of
																												// "Fluid
																												// &
																												// Excreta"
											geneListVar = responseJson.geneList; // Get
																					// geneList
																					// :
																					// ["g1|g1-001|10036",
																					// "g2|g2-002|10090"]
											Ext.getCmp("source_fluid" + '-edit').items.items[5].setValue(geneListVar.length); // Set
																																// Total
																																// number
																																// of
																																// Target
																																// Gene

											if (geneListVar.length > 0) {
												for (var listIndex = 0; listIndex < geneListVar.length; listIndex++) {
													geneSmallList = geneListVar[listIndex].split("|"); // Get
																										// geneList[index].split("|")
																										// :
																										// ["g1",
																										// "g1-001",
																										// "10036"]

													geneSymbolVar = "geneSymbol" + (listIndex + 1); // Set
																									// name
																									// "geneSymbol1"
													Cmp_source_fluid.findField(geneSymbolVar).setValue(geneSmallList[0]); // Set
																															// "geneSymbol"
																															// Value
													GeneIDVar = "GeneID" + (listIndex + 1);
													Cmp_source_fluid.findField(GeneIDVar).setValue(geneSmallList[1]);
													geneTaxonVar = "geneTaxon" + (listIndex + 1);
													Cmp_source_fluid.findField(geneTaxonVar).setValue(geneSmallList[2]);
												}
											}
										} else {
											Ext.getCmp("source_fluid" + '-edit').items.items[3].setValue(0);
										}

									} else {
										// sampleSourceType.items.items[0].setValue(false);
										// sampleSourceType.items.items[1].setValue(false);
										// sampleSourceType.items.items[2].setValue(false);
										sampleSourceType.items.items[3].setValue(true);
									}

									// Total number of Treatment
									var totalNumberOfTreatment = Ext.getCmp('sample-general' + '-edit').getForm().findField('treat_num');
									totalNumberOfTreatment.setValue(responseJson.treatmentsCount);

									var treatIndex;
									// deal Treatment + No.
									if (responseJson.treatmentsCount > 0) {
										for (treatIndex = 1; treatIndex <= responseJson.treatmentsCount; treatIndex++) {
											console.log("pre--Rx_treatment");
											Ext.getCmp('Treatment' + treatIndex + '-edit').getForm().findField('Rx_treatment' + treatIndex)
													.setValue(responseJson.rx_treatments[treatIndex - 1]);
										}
									}

									// deal Treatment + No.
									if (responseJson.treatmentsCount > 0) {
										for (treatIndex = 1; treatIndex <= responseJson.treatmentsCount; treatIndex++) {
											console.log("pre--Rx_treatment");
											Ext.getCmp("treantment_detail" + treatIndex + '-edit')
													.setValue(responseJson.rx_treatments_detail[treatIndex - 1]);

											console.log("pre--rx_duration")
											Ext.getCmp("Treatment" + treatIndex + '-edit').items.items[2].items.items[0]
													.setValue(responseJson.rx_duration[treatIndex - 1]);
											Ext.getCmp("Treatment" + treatIndex + '-edit').items.items[2].items.items[1]
													.setValue(responseJson.rx_duration_time[treatIndex - 1]);
										}
									}

									// deal "Concentration"
									var unitConcentration;
									if (responseJson.treatmentsCount > 0) {
										for (treatIndex = 1; treatIndex <= responseJson.treatmentsCount; treatIndex++) {
											if (responseJson.rx_treatments[treatIndex - 1] != "Gene Engineering"
													&& responseJson.rx_unit[treatIndex - 1] != "Concentration") {
												Ext.getCmp("samp-treat-unit" + treatIndex + '-edit').items.items[1]
														.setValue(responseJson.rx_unit[treatIndex - 1]);
												Ext.getCmp("samp-treat-unit" + treatIndex + '-edit').items.items[2]
														.setValue(responseJson.rx_unit_deatil1[treatIndex - 1]);
											}
											if (responseJson.rx_treatments[treatIndex - 1] != "Gene Engineering"
													&& responseJson.rx_unit[treatIndex - 1] == "Concentration") {
												Ext.getCmp("samp-treat-unit" + treatIndex + '-edit').items.items[1]
														.setValue(responseJson.rx_unit[treatIndex - 1]);
												unitConcentration = responseJson.rx_unit_deatil2[treatIndex - 1].split("/");
												Ext.getCmp("unit_detail2_" + treatIndex + '-edit').items.items[0].setValue(unitConcentration[0]);
												Ext.getCmp("unit_detail2_" + treatIndex + '-edit').items.items[2].setValue(unitConcentration[1]);
											}
										}

									}

								}
							});

				}

				/** *******************EditSample******************** */

				Reagent_detail = function(text) {
					var win = Ext.create('Ext.Window', {
								layout : {
									type : 'hbox',
									align : 'left'
								},
								autoScroll : true,
								resizable : true,
								title : 'Detailed Information of ' + text,
								width : 700,
								height : 450,
								items : []
							})
					win.show()
					expList = text.split(';')
					for (expL = 0; expL < expList.length; expL++) {
						Ext.Ajax.request({
									url : '/experiments/load/reagent/',
									params : {
										reagent_no : expList[expL].split('Rea')[1]
										// csrfmiddlewaretoken : csrftoken
									},
									success : function(response) {
										var panel = Ext.create('gar.view.Reagent_detail')
										var text = response.responseText;
										responseJson = Ext.JSON.decode(text).data;
										Reagent_name = String(responseJson.Reagent_name)
										// console.log(Reagent_name)
										while (Reagent_name.length < 6) {
											Reagent_name = '0' + Reagent_name
										}
										Reagent_name = 'Rea' + Reagent_name
										panel.items.items[0].setValue(Reagent_name)
										panel.items.items[1].setValue(responseJson.company + '/ ' + responseJson.lab + '/ '
												+ responseJson.experimenter)
										panel.items.items[2].setValue(responseJson.date)
										panel.items.items[3].setValue(responseJson.reagent_type)
										panel.items.items[4].setValue(responseJson.Reagent_manufacturer)
										panel.items.items[5].setValue(responseJson.catalog_no)
										panel.items.items[5].setValue(responseJson.Conjugate)
										panel.items.items[7].setValue(responseJson.Application)
										panel.items.items[8].setValue(responseJson.React_species_source)
										panel.items.items[9].setValue(responseJson.React_species_target)
										// panel.items.items[9].setValue(responseJson.React_species_target)
										win.insert(0, panel)
									}
								});
						// console.log(win)
					}

				}
				Sample_detail = function(text) {
					var win = Ext.create('Ext.Window', {
								layout : {
									type : 'hbox',
									align : 'left'
								},
								autoScroll : true,
								resizable : true,
								title : 'Detailed Information of ' + text,
								width : 700,
								height : 450,
								items : []
							})
					win.show()
					expList = text.split(';')
					for (expL = 0; expL < expList.length; expL++) {
						Ext.Ajax.request({
									url : '/experiments/load/sample/',
									params : {
										sample_no : expList[expL].split('Sam')[1]
										// csrfmiddlewaretoken : csrftoken
									},
									success : function(response) {
										var panel = Ext.create('gar.view.Sample_detail')
										var text = response.responseText;
										responseJson = Ext.JSON.decode(text).data;
										Sample_name = String(responseJson.Sample_name)
										// console.log(Reagent_name)
										while (Sample_name.length < 6) {
											Sample_name = '0' + Sample_name
										}
										Sample_name = 'Sam' + Sample_name
										panel.items.items[0].setValue(Sample_name)
										panel.items.items[1].setValue(responseJson.company + '/ ' + responseJson.lab + '/ '
												+ responseJson.experimenter)
										panel.items.items[2].setValue(responseJson.date)
										panel.items.items[3].setValue(responseJson.detail_location)
										panel.items.items[7].setValue(responseJson.Specific_ID)
										panel.items.items[8].setValue(responseJson.Ubi_subcell)
										panel.items.items[9].setValue(responseJson.Ubi_method)
										panel.items.items[10].setValue(responseJson.comments)
										panel.items.items[11].setValue(responseJson.Ispec_num)
										win.insert(0, panel)
									}
								});
						// console.log(win)
					}

				}

			}
		})
