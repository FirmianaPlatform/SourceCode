Ext.define('gar.view.Gene', {
			extend : 'Ext.grid.Panel',
			alias : 'widget.gene',
			border : false,
			// frame:true,
			rowLines : true,
			columnLines : true,
			//selType : 'checkboxmodel',
			viewConfig : {
				stripeRows : true,
				enableTextSelection : true
			},
			// forceFit:true,
			multiSelect : true,
			plugins : [{
						ptype : 'bufferedrenderer',
						trailingBufferZone : 0,
						leadingBufferZone : 100
					},],
			initComponent : function() {
				var anno_list = [['co_1', 'Coreg'], ['ki_1', 'Kinase'], ['li_1', 'Ligand'], ['re_1', 'Receptor'], ['pmm_1', 'Plasma Membrane(Mouse)'], ['pmh_1', 'Plasma Membrane(Human)'], ['tf_1', 'Transcription Factor'], ['pho_1', 'Phospho']]
				var modi_list = [['Acetyl_1', 'N-terminal Acetyltrasferases'], ['Methyl_1', 'Methylation'], ['GlyGly_1', 'Ubiquitination'], ['Biotin_1', 'Biotin'], ['PhosphoST_1', 'Phosphorylation-ST'], ['PhosphoY_1', 'Phosphorylation-Y']]
				var click_filter = function(grid, rowIndex, colIndex, i) {
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
										width : 50
									}, {
										text : 'Exp Name',
										dataIndex : 'exp_name',
										hidden : true
									}, {
										text : 'Experiment Description',
										dataIndex : 'exp_description',
										filter : {
											type : 'string',
											encode : true
										},
										hidden : true
									}, {
										text : "Gene ID",
										align : 'left',
										dataIndex : 'gene_id',
										filter : {
											type : 'int',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											if(value==-1){ return '-' }
											return value
										}
										// renderer : function(value, metaData, record, rowIndex, colIndex, store) {
									// cssstring = '<div class="x-grid3-cell-inner" style="';
									// cssstring += '">' + "<a href='#'>"
									// return cssstring + value + '</a>' + '</div>' }
								}	, {
										text : "Symbol",
										dataIndex : 'symbol',
										filter : {
											type : 'string',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											return Ext.String.format('<a data-qtip="Search {0} in NCBI" href="http://www.ncbi.nlm.nih.gov/gene/?term={0}"  target="_blank">{0}</a>', value);
										}
									}, {
										width : 90,
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
										
										sortable : true
									}, {
										width : 240,
										text : "Description",
										dataIndex : 'description',
										filter : {
											type : 'string',
											encode : true
										},
										sortable : true
									} /*
										 * , { text : "Relation", renderer : function(value, metaData, record, rowIndex,
										 * colIndex, store) { value = ' '; bkimg = ""; bksz = ""; bkpst = ""; bkrp = "";
										 * pst = 0; { if (record.data.test2_1 > 0) { bkimg +=
										 * ("url(/static/images/bkg_pink.png),") } else { bkimg +=
										 * ("url(/static/images/bkg_gray.png),") } bksz += ("12% 100%,") bkpst +=
										 * (pst.toString()); pst += 15 bkpst += ("% 0%,") bkrp += "no-repeat," } { if
										 * (record.data.test2_2 > 0) { bkimg += ("url(/static/images/bkg_red.png),") }
										 * else { bkimg += ("url(/static/images/bkg_gray.png),") } bksz += ("12% 100%,")
										 * bkpst += (pst.toString()); pst += 15 bkpst += ("% 0%,") bkrp += "no-repeat," } {
										 * if (record.data.test2_3 > 0) { bkimg +=
										 * ("url(/static/images/bkg_yellow.png),") } else { bkimg +=
										 * ("url(/static/images/bkg_gray.png),") } bksz += ("12% 100%,") bkpst +=
										 * (pst.toString()); pst += 15 bkpst += ("% 0%,") bkrp += "no-repeat," } { if
										 * (record.data.test2_4 > 0) { bkimg += ("url(/static/images/bkg_green.png),") }
										 * else { bkimg += ("url(/static/images/bkg_gray.png),") } bksz += ("12% 100%,")
										 * bkpst += (pst.toString()); pst += 15 bkpst += ("% 0%,") bkrp += "no-repeat," } {
										 * if (record.data.test2_5 > 0) { bkimg += ("url(/static/images/bkg_blue.png),") }
										 * else { bkimg += ("url(/static/images/bkg_gray.png),") } bksz += ("12% 100%,")
										 * bkpst += (pst.toString()); pst += 15 bkpst += ("% 0%,") bkrp += "no-repeat," } {
										 * if (record.data.test2_6 > 0) { bkimg +=
										 * ("url(/static/images/bkg_violet.png),") } else { bkimg +=
										 * ("url(/static/images/bkg_gray.png),") } bksz += ("12% 100%,") bkpst +=
										 * (pst.toString()); pst += 15 bkpst += ("% 0%,") bkrp += "no-repeat," } { if
										 * (record.data.test2_7 > 0) { bkimg += ("url(/static/images/bkg_brown.png),") }
										 * else { bkimg += ("url(/static/images/bkg_gray.png),") } bksz += ("12% 100%,")
										 * bkpst += (pst.toString()); pst += 15 bkpst += ("% 0%,") bkrp += "no-repeat," }
										 * cssstring = '<div class="x-grid3-cell-inner" style="white-space: pre;'; {
										 * cssstring += 'background-image:'; cssstring += bkimg.substr(0, bkimg.length -
										 * 1) + ";"; cssstring += 'background-size:'; cssstring += bksz.substr(0,
										 * bksz.length - 1) + ";"; cssstring += 'background-position:'; cssstring +=
										 * bkpst.substr(0, bkpst.length - 1) + ";"; cssstring += 'background-repeat:';
										 * cssstring += bkrp.substr(0, bkrp.length - 1) + ";"; } cssstring += '">'
										 * return cssstring + value + '</div>' } // dataIndex : 'symbol', }
										 */, {
										width : 180,
										text : "Protein GI",
										dataIndex : 'protein_gi',
										filter : {
											type : 'string',
											encode : true
										},
										sortable : true
									}, {
										text : "Protein Num",
										dataIndex : 'num_proteins',
										filter : {
											type : 'int',
											encode : true
										},
										sortable : true
									}, {
										text : "Area",
										dataIndex : 'area',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											return value.toExponential(5);
										}
									}, {
										text : "iFOT(*10^-6)",
										dataIndex : 'fot',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											return value.toExponential(5);
										}
									}, {
										text : "iBAQ",
										dataIndex : 'ibaq',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											return value.toExponential(5);
										}
									}, {
										text : "Peptide Num",
										dataIndex : 'num_peptides',
										filter : {
											type : 'int',
											encode : true
										},
										sortable : true
									}, {
										width : 140,
										text : "Unique Peptide Num",
										dataIndex : 'num_uni_peptides',
										filter : {
											type : 'int',
											encode : true
										},
										sortable : true
									}, {
										width : 140,
										text : "Identified Proteins Num",
										dataIndex : 'num_identified_proteins',
										filter : {
											type : 'int',
											encode : true
										},
										sortable : true
									}, {
										width : 140,
										text : "Unique Proteins Num",
										dataIndex : 'num_uni_proteins',
										filter : {
											type : 'int',
											encode : true
										},
										sortable : true
									}, {
										text : "FDR",
										dataIndex : 'fdr',
										filter : {
											type : 'float',
											encode : true
										},
										sortable : true,
										renderer : function(value) {
											// s = "#ffffff"
											// if (value >= 0.04999) {
											// s = "#c8c8c8";
											// }
											// return '<div class="x-grid3-cell-inner" style="background-color:' + s +
											// ';">' + value.toFixed(4) + '</div>'
											return value.toFixed(3)
										},
										hidden : true
									}]
						});
				this.callParent(arguments);
			}
		})