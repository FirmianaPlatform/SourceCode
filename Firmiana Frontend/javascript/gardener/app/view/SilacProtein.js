var anno_click = function(anno_id) {
	// var annos = ['Coreg','Kinase','Ligand','Receptor','PlasmaMembrane-mouse','PlasmaMembrane-human','TF']
	var grid = Ext.getCmp('content-panel').activeTab.items.items[0]
	var record = grid.selModel.selected.items[0]
	var anno_selected = record.data.annotation
	Ext.Msg.alert('Annotation', 'Annotation = ' + anno_selected + ', you select No.' + (1 + anno_id))
	var anno_store = Ext.getCmp('content-panel').getActiveTab().down('grid').getStore()
	// anno_store.filter("annotation",/0;0;0;0;0;0;0/)
	// anno_store.filter({"field":{type:"string",name:"annotation"},"value":anno_selected})
	// anno_store.getProxy().extraParams.type = 'string';
}
Ext.define('gar.view.SilacProtein', {
			extend : 'Ext.grid.Panel',
			alias : 'widget.silacprotein',
			viewConfig : {
				stripeRows : true,
				enableTextSelection : true
			},
			columnLines : true,
			border : false,
			// frame:true,
			// loadMask : true,
			// selType: 'checkboxmodel',
			// forceFit:true,
			// collapsible: true,
			multiSelect : true,
			plugins : {
				ptype : 'bufferedrenderer',
				trailingBufferZone : 0,
				leadingBufferZone : 200
			},
			initComponent : function() {
				var anno_list = [['co_1', 'Coreg'], ['ki_1', 'Kinase'], ['li_1', 'Ligand'], ['re_1', 'Receptor'], ['pmm_1', 'Plasma Membrane(Mouse)'], ['pmh_1', 'Plasma Membrane(Human)'], ['tf_1', 'Transcription Factor']]
				var modi_list = [['Acetyl_1', 'N-terminal Acetyltrasferases'], ['Methyl_1', 'Methylation'], ['GlyGly_1', 'Ubiquitination'], ['Biotin_1', 'Biotin'], ['PhosphoST_1', 'Phosphorylation-ST'], ['PhosphoY_1', 'Phosphorylation-Y']]
				var click_filter = function(grid, rowIndex, colIndex, i) {
					var record = grid.getStore().getAt(rowIndex);
					// console.log(record)
					var anno = record.get('annotation');
					var anno_arr = anno.split(';');
					if (0) {
						// Ext.Msg.alert('Annotation',anno +' (' + anno_list[i] + ' is clicked).');
						// var store = Ext.getCmp('content-panel').getActiveTab().down('grid').getStore();
						var store = grid.getStore()
						// store.reload()
						var win = Ext.getCmp('anno_filter_win')
						if (win) {
							win.close()
						}
						var win = Ext.create('gar.view.Annotation', {});
						// var rec = grid.selModel.selected.items[0]
						// win.anchorTo(rec,'l',[2,2],true)
						/*
						 * if (1) { var store = Ext.create('gar.store.Protein', { listeners : { totalcountchange :
						 * onStoreSizeChange } }); var filters = { ftype : 'filters', encode : true }
						 * store.getProxy().extraParams = { sid:176, stype : 'anno', anno : anno }; var grid =
						 * Ext.create('gar.view.Protein', { store : store, features : [filters], dockedItems : [{ dock :
						 * 'top', xtype : 'toolbar', items : [{ text : 'Clear Filter Data', handler : function() {
						 * grid.filters.clearFilters(); } }, { text : 'All Filter Data', tooltip : 'Get Filter Data for
						 * Grid', handler : function() { var data = Ext.encode(grid.filters.getFilterData());
						 * Ext.Msg.alert('All Filter Data', data); } }, '->', { xtype : 'component', itemId : 'status',
						 * tpl : 'Matching Proteins: {count}', style : 'margin-right:5px' }] }], emptyText : 'No
						 * Matching Records', }) } function onStoreSizeChange() { grid.down('#status').update({ count :
						 * store.getTotalCount() }); } c = Ext.getCmp('content-panel')
						 * Ext.getCmp('info_tab_index').value += 1 c.add({ title : 'protein' + ' of ' + anno, //iconCls :
						 * 'tabs', closable : true, // id : 'tab_'+ Ext.getCmp('info_tab_index').value, layout : 'fit',
						 * items : [grid] }).show()
						 */
					}
				};
				var my_getClass = function(rec, i) {
					var annos = rec.get('annotation');
					var anno_arr = annos.split(',');
					return 'anno_' + anno_arr[i]
				};
				var my_getTip = function(rec, i) {
					var annos = rec.get('annotation');
					var anno_arr = annos.split(',');
					if (anno_arr[i].substring(anno_arr[i].length - 1) == '1') {
						return anno_list[i][1];
					} else {
						return '';
					}
				}
				var getModificationClass = function(rec, i) {
					var modi = rec.get('modification');
					var mod = modi.split(',')[i]
					var flag = mod.substring(mod.length - 1);
					if (flag == '0') {
						return 'mod_none'
					} else {
						var cla = 'mod_' + mod;
						return cla.substring(0, cla.length - 2);
					}
				};
				var getModificationTip = function(rec, i) {
					var modi = rec.get('modification');
					var mod = modi.split(',')[i]
					var flag = mod.substring(mod.length - 1);
					if (flag == '0') {
						return ''
					} else {
						return modi_list[i][1]
					}
				}
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
				var optionsStore2 = new Ext.data.Store({
							fields : ['id', 'text'],
							proxy : {
								data : modi_list,
								type : 'memory',
								reader : {
									type : 'array'
								}
							}
						})
				Ext.apply(this, {
							columns : [{
										xtype : 'rownumberer',
										width : 60
									}, {
										text : 'Exp Name',
										dataIndex : 'exp_name',
										hidden : true
									}, {
										text : 'Experiment Description',
										dataIndex : 'exp_description',filter : {
											type : 'string',
											encode : true
										},
										hidden : true
									}, {
										text : "Accession",
										align : 'left',
										dataIndex : 'accession',
										width : 95,
										filter : {
											type : 'string',
											encode : true
										},
										sortable : true,
										renderer : function(value, metaData, record, rowIndex, colIndex, store) {
											cssstring = '<div class="x-grid3-cell-inner" style="text-align:left;';
											cssstring += '">' + "<a href='#'>"
											return cssstring + value + '</a>' + '</div>'
										}
									}, {
										text : "Symbol",
										align : 'left',
										dataIndex : 'symbol',
										width : 85,
										filter : {
											type : 'string',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											return Ext.String.format('<a href="http://www.ncbi.nlm.nih.gov/gene/?term={0}"  target="_blank">{0}</a>', value);
										}
									}, {
										width : 81,
										text : "Annotation",
										xtype : 'actioncolumn',
										dataIndex : 'annotation',
										filter : {
											type : 'list',
											store : optionsStore
										},
										// flex : 0.5,
										items : [{
													getClass : function(v, meta, rec) {
														return my_getClass(rec, 0)
													},
													getTip : function(v, meta, rec) {
														return my_getTip(rec, 0)
													},
													handler : function(grid, rowIndex, colIndex) {
														click_filter(grid, rowIndex, colIndex, 0)
													}
												}, {
													getClass : function(v, meta, rec) {
														return my_getClass(rec, 1)
													},
													getTip : function(v, meta, rec) {
														return my_getTip(rec, 1)
													},
													handler : function(grid, rowIndex, colIndex) {
														click_filter(grid, rowIndex, colIndex, 1)
													}
												}, {
													getClass : function(v, meta, rec) {
														return my_getClass(rec, 2)
													},
													getTip : function(v, meta, rec) {
														return my_getTip(rec, 2)
													},
													handler : function(grid, rowIndex, colIndex) {
														click_filter(grid, rowIndex, colIndex, 2)
													}
												}, {
													getClass : function(v, meta, rec) {
														return my_getClass(rec, 3)
													},
													getTip : function(v, meta, rec) {
														return my_getTip(rec, 3)
													},
													handler : function(grid, rowIndex, colIndex) {
														click_filter(grid, rowIndex, colIndex, 3)
													}
												}, {
													getClass : function(v, meta, rec) {
														return my_getClass(rec, 4)
													},
													getTip : function(v, meta, rec) {
														return my_getTip(rec, 4)
													},
													handler : function(grid, rowIndex, colIndex) {
														click_filter(grid, rowIndex, colIndex, 4)
													}
												}, {
													getClass : function(v, meta, rec) {
														return my_getClass(rec, 5)
													},
													getTip : function(v, meta, rec) {
														return my_getTip(rec, 5)
													},
													handler : function(grid, rowIndex, colIndex) {
														click_filter(grid, rowIndex, colIndex, 5)
													}
												}, {
													getClass : function(v, meta, rec) {
														return my_getClass(rec, 6)
													},
													getTip : function(v, meta, rec) {
														return my_getTip(rec, 6)
													},
													handler : function(grid, rowIndex, colIndex) {
														click_filter(grid, rowIndex, colIndex, 6)
													}
												}]
									}, {
										width : 90,
										text : "Modification",
										xtype : 'actioncolumn',
										dataIndex : 'modification',
										filter : {
											type : 'list',
											store : optionsStore2
										},
										// flex : 0.5,
										items : [{
													getClass : function(v, meta, rec) {
														return getModificationClass(rec, 0)
													},
													getTip : function(v, meta, rec) {
														return getModificationTip(rec, 0)
													},
													handler : function(grid, rowIndex, colIndex) {
														click_filter(grid, rowIndex, colIndex, 0)
													}
												}, {
													getClass : function(v, meta, rec) {
														return getModificationClass(rec, 1)
													},
													getTip : function(v, meta, rec) {
														return getModificationTip(rec, 1)
													},
													handler : function(grid, rowIndex, colIndex) {
														click_filter(grid, rowIndex, colIndex, 1)
													}
												}, {
													getClass : function(v, meta, rec) {
														return getModificationClass(rec, 2)
													},
													getTip : function(v, meta, rec) {
														return getModificationTip(rec, 2)
													},
													handler : function(grid, rowIndex, colIndex) {
														click_filter(grid, rowIndex, colIndex, 2)
													}
												}, {
													getClass : function(v, meta, rec) {
														return getModificationClass(rec, 3)
													},
													getTip : function(v, meta, rec) {
														return getModificationTip(rec, 3)
													},
													handler : function(grid, rowIndex, colIndex) {
														click_filter(grid, rowIndex, colIndex, 3)
													}
												}, {
													getClass : function(v, meta, rec) {
														return getModificationClass(rec, 4)
													},
													getTip : function(v, meta, rec) {
														return getModificationTip(rec, 4)
													},
													handler : function(grid, rowIndex, colIndex) {
														click_filter(grid, rowIndex, colIndex, 4)
													}
												}, {
													getClass : function(v, meta, rec) {
														return getModificationClass(rec, 5)
													},
													getTip : function(v, meta, rec) {
														return getModificationTip(rec, 5)
													},
													handler : function(grid, rowIndex, colIndex) {
														click_filter(grid, rowIndex, colIndex, 5)
													}
												}]
									}, /*
										 * { text : "Relation", width : 60, dataIndex : 'annotation', sortable : true,
										 * renderer : function(value, metaData, record, rowIndex, colIndex, store) { var
										 * bkimg = " "; //var anno_string = value; //console.log(value); { if
										 * (value=='') {var anno = [0,0,0,0,0,0,0]} else {var anno = value.split(';')} }
										 * //var anno =
										 * [record.data.test1_1,record.data.test1_2,record.data.test1_3,record.data.test1_4,record.data.test1_5,record.data.test1_6,record.data.test1_7]
										 * var annos = ['Coreg','Kinase','Ligand','Receptor','Mouse-Plasma
										 * Membrane','Human-Plasma Membrane','Transcription Factor'] var color =
										 * ['bkg_pink.png','bkg_red.png','bkg_yellow.png','bkg_green.png','bkg_blue.png','bkg_violet.png','bkg_brown.png']
										 * for (i=0;i<3;i++) { if (0)//anno[i]=='1') { { bkimg += ' <input type="image"
										 * src="/static/images/' + color[i] + '"
										 * style="margin-top:2px;margin-left:1px;cursor:pointer;height:13px;width:9px;"
										 * class="x-action-col-icon annotation_' //bkimg += i + '" data-qtip="' +
										 * annos[i] + '">' bkimg += i + '" data-qtip="' + annos[i] + '"
										 * onclick="anno_click(' + i + ');">' } else { bkimg += ' <input type="image"
										 * src="/static/images/bkg_gray.png"
										 * style="margin-top:2px;margin-left:1px;cursor:default;height:13px;width:9px;"
										 * class="x-action-col-icon">' } } cssstring = '' //cssstring = '<div
										 * class="x-grid3-cell-inner">'; cssstring += bkimg //cssstring += '</div> '
										 * //console.log(cssstring) return cssstring } }{ text : "Symbol", hidden :
										 * true,// I'll be back. dataIndex : 'symbol', filter : { type : 'string',
										 * encode : true }, sortable : true },
										 */
									{
										text : 'Other members',
										dataIndex : 'other_members',
										filter : {
											type : 'string',
											encode : true
										},
										renderer : function(value, metaData, record, rowIndex, colIndex, store) {
											metaData.tdAttr = "title='" + value + "'";
											return value
										},
										sortable : true,
										width : 115
									}, {
										width : 240,
										text : "User Annotation",
										dataIndex : 'user_specified',
										filter : {
											type : 'string',
											encode : true
										},
										editor : {
											//xtype : 'textfield',
											allowBlank : true
										},
										renderer:function(value){
											return value?value:''
										},
										hidden: true
										//sortable : true
									}, {
										text : "Description",
										width : 250,
										flex : 1,
										dataIndex : 'description',
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
										width : 70,
										text : "Score",
										dataIndex : 'score',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											return value.toFixed(2);
										}
									}, {
										width : 80,
										text : "Coverage",
										dataIndex : 'coverage',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											bkimg = "";
											bksz = "";
											bkpst = "";
											bkrp = "";
											pst = 0;
											{
												bkimg += ("url(/static/images/bkg_green.png),")
												pst = value * 100;
												bksz += (pst.toString());
												bksz += ("% 100%,")
												bkpst += ("0% 0%,")
												bkrp += "no-repeat,"
											}
											cssstring = '<div class="x-grid3-cell-inner" style="text-align:center;';
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
											return cssstring + value.toFixed(4) + '</div>'
										}
									}, {
										text : "Area(light)",
										dataIndex : 'larea',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											return value.toExponential(5);
										}
									}, {
										text : "Area(heavy)",
										dataIndex : 'harea',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											return value.toExponential(5);
										}
									}, {
										text : "Area(ratio)",
										dataIndex : 'area_ratio',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											if (value == 1e9){
												var s = "#ff0000"
												return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + '1e9' + '</div>'
											}else if (value > 1) {
												var p = parseInt(1 / value * 255);
												var k = ("00" + p.toString(16)).substr(p.toString(16).length)
												var s = "#ff" + k + k
												return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + value.toFixed(2) + '</div>'
											} else if (value < 1) {
												var p = parseInt(value * 255);
												var k = ("00" + p.toString(16)).substr(p.toString(16).length)
												var s = "#" + k + "ff" + k
												return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + value.toFixed(2) + '</div>'
											} else
												return 1
											// return value.toExponential(5);
										}
									}, {
										text : "iFOT(light) (*10^-6)",
										dataIndex : 'lfot',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											return value.toFixed(5);
										}
									}, {
										text : "iFOT(heavy) (*10^-6)",
										dataIndex : 'hfot',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											return value.toFixed(5);
										}
									}, {
										text : "iFOT(ratio)",
										dataIndex : 'fot_ratio',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											if (value == 1e9){
												var s = "#ff0000"
												return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + value.toFixed(2) + '</div>'
											}else if (value > 1) {
												var p = parseInt(1 / value * 255);
												var k = ("00" + p.toString(16)).substr(p.toString(16).length)
												var s = "#ff" + k + k
												return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + value.toFixed(2) + '</div>'
											} else if (value < 1) {
												var p = parseInt(value * 255);
												var k = ("00" + p.toString(16)).substr(p.toString(16).length)
												var s = "#" + k + "ff" + k
												return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + value.toFixed(2) + '</div>'
											} else
												return 1
										}
									}, {
										text : "iBAQ(light)",
										dataIndex : 'libaq',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											return value.toExponential(5);
										}
									}, {
										text : "iBAQ(heavy)",
										dataIndex : 'hibaq',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											return value.toExponential(5);
										}
									}, {
										text : "iBAQ(ratio)",
										dataIndex : 'ibaq_ratio',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											if (value == 1e9){
												var s = "#ff0000"
												return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + value.toFixed(2) + '</div>'
											}else if (value > 1) {
												var p = parseInt(1 / value * 255);
												var k = ("00" + p.toString(16)).substr(p.toString(16).length)
												var s = "#ff" + k + k
												return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + value.toFixed(2) + '</div>'
											} else if (value < 1) {
												var p = parseInt(value * 255);
												var k = ("00" + p.toString(16)).substr(p.toString(16).length)
												var s = "#" + k + "ff" + k
												return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + value.toFixed(2) + '</div>'
											} else
												return 1
										}
									}, {
										text : "Protein Num",
										dataIndex : 'num_proteins',
										filter : {
											type : 'int',
											encode : true
										},
										sortable : true
									}, {
										text : "Unique Peptide Num",
										dataIndex : 'num_uni_peptides',
										filter : {
											type : 'int',
											encode : true
										},
										sortable : true
									}, {
										text : "Peptide Num",
										dataIndex : 'num_peptides',
										filter : {
											type : 'int',
											encode : true
										},
										sortable : true
									}, {
										text : "PSM Num",
										dataIndex : 'num_psms',
										filter : {
											type : 'int',
											encode : true
										},
										sortable : true
									}, {
										width : 60,
										text : "Length",
										dataIndex : 'length',
										filter : {
											type : 'int',
											encode : true
										},
										sortable : true
									}, {
										width : 90,
										text : "Molecular Weight",
										dataIndex : 'mw',
										filter : {
											type : 'float',
											encode : true
										},
										renderer : function(value) {
											return value.toFixed(2);
										},
										sortable : true
									}, 
//									{
//										text : "calc. pI",
//										// text : "Theoretically Calculated Isoelectric Point",
//										dataIndex : 'calc_pi',
//										filter : {
//											type : 'float',
//											encode : true
//										},
//										sortable : true,
//										renderer : function(value) {
//											return value.toFixed(4);
//										},
//										hidden : true
//									}, 
									{
										width : 60,
										text : "FDR",
										dataIndex : 'fdr',
										filter : {
											type : 'float',
											encode : true
										},
										renderer : function(value) {
											// s = "#ffffff"
											// if (value >= 0.04999) {
											// s = "#c8c8c8";
											// }
											// return '<div class="x-grid3-cell-inner" style="background-color:' + s +
											// ';">' + value.toFixed(4) + '</div>'
											return value.toFixed(3);
										},
										hidden : true
									}]
						});
				this.callParent(arguments);
			}
		})