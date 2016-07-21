Ext.define('gar.view.Tools',{
    extend: 'Ext.window.Window',

    /**
     * @requires gar.view.Tools.ToolType
     */
    requires: [
        'gar.view.tools.ToolTypeProtein',
        'gar.view.tools.ToolTypePeptide',
        'Ext.tip.QuickTipManager',
        'gar.view.tools.CenterPanel',
        'gar.view.tools.EastPanel',
        'gar.view.tools.toolsStatusBar'
    ],
    alias: 'widget.tools',
    layout: 'border',
    padding: 0,
    // id: 'PPIplot',
    title: 'Tools Control Panel',
    header: {
        titlePosition: 2,
        titleAlign: 'center'
    },
    maximizable: true,
    minimizable: true,
     
    width:1200,
    height: 660,
    autoShow: true,
    closable: true,
    closeAction: 'destroy',
    listeners : {
		"minimize" : function(window, opts) {
			window.collapse();
			window.setWidth(150);
			window.alignTo(Ext.getBody(), 'bl-bl')
		}
	},
	tools : [{
		type : 'restore',
		handler : function(evt, toolEl, owner, tool) {
			var window = owner.up('window');
			window.setWidth(1200);
			window.expand('', false);
			window.center();
		}
	}],

    initComponent: function() {
    	var temp_name = this.temp_name
    	var val = this.val
    	var gridType = this.gridType
    	normalizationLevel = 'none_none'
    	if(this.proGene == 'gene')
    		var proGene = 'protein'
    	else
    		var proGene = this.proGene
    	this.animateTarget = 'tools' + val

    	this.id = 'toolsPanel';
    	
    	var ifclose = false;
    	this.on('beforeclose', function() {  	
    		if(ifclose){ return true;}
    	  	Ext.MessageBox.show({
				title : 'Warning',
				msg : "Do you really want to quit?",
				buttons : Ext.Msg.YESNO,
				icon : Ext.Msg.WARNIN,
				fn : function(btn) {
					if (btn == 'yes') {
						ifclose = true;
						Ext.getCmp('toolsPanel').close();
    				}
				}
				})
				return false;
    		});
    		
    	Ext.Ajax.request({
			url : '/gardener/com_getheaders/',
			params : {
				id : val,
				gridType: gridType
			},
			method : 'GET',
			success : function(response) {
				var json = Ext.JSON.decode(response.responseText);
				oldcolumndata = json.columns
				columndata = oldcolumndata


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
						//columndata[i].dataIndex = 'modification'
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
			}
		});

    	
    	Ext.tip.QuickTipManager.init();

    	var helpEl, tmpRootNodeFin, tmpRootNodeInit, tmpRootNodeDust;

    	tooltypetree = Ext.widget('tooltype' + proGene);

    	mainpanel = Ext.widget('centerpanel');

    	eastpanel = Ext.widget('eastpanel');

    	groupExpHistoryStore = Ext.create('Ext.data.Store', {
    		fields: ['name', 'time', 'tree', 'data', 'treeInit', 'treeDust']
    	});

    	groupexp = Ext.widget('groupexp');
    	mainpanel.add(groupexp);
    	mainpanel.setActiveTab(groupexp);


    	treeinit = Ext.widget('treeinit',{val: val});
    	eastpanel.add(treeinit);
    	eastpanel.setActiveTab(treeinit);

    	tooltypetree.getSelectionModel().on('select', function(selModel, record) {
	        if (record.get('leaf')) {
//	        	if(!hasGrouped){
//	        		Ext.example.msg('Warning', 'Group experiments before analysis.')
//	        		//Ext.Msg.alert('Warning','Group experiments first.');
//	        		return;
//	        	}
	        	var toolTitle = record.data.text
	        	console.log(toolTitle);
	        	if(!helpEl)
	        	{
	        		var helpBody = Ext.getCmp('tools-help').body;
		        	helpBody.update('').setStyle('background','#fff');
		        	helpEl = helpBody.createChild()
		        	helpEl.setStyle('padding','6px')
	        	}
				helpEl.hide().update(helpTips[record.data.text]).slideIn('l');
	        	//var mp = Ext.getCmp('mainpanel');
	    		var temp_panel = Ext.widget( toolTitle.replace(" ", ""), {val: val, objEastPanel:eastpanel,gridType:gridType,temp_name:temp_name} ); 
    		
	    		mainpanel.add(temp_panel).show();
	    		mainpanel.setActiveTab(temp_panel);

	        }
	    });

	    //change view function
	    var change = function(columndata, type) {

			for (var i = 0; i < columndata.length; i++) {
				if (columndata[i].columns)
				{
					change(columndata[i].columns, type)
				}
				if (columndata[i] && columndata[i].dataIndex) {
					// console.log(columndata[i].dataIndex)
					if (columndata[i].dataIndex.indexOf('area') != -1)
					{
						columndata[i].dataIndex = columndata[i].dataIndex.replace(/area/g, type.toLowerCase())
						if(columndata[i].text == 'Area')
							columndata[i].text = type
					}
					else if (columndata[i].dataIndex.indexOf('ibaq') != -1)
					{
						columndata[i].dataIndex = columndata[i].dataIndex.replace(/ibaq/g, type.toLowerCase())
						if(columndata[i].text == 'Ibaq')
							columndata[i].text = type
					}
					else if (columndata[i].dataIndex.indexOf('fot') != -1)
					{
						columndata[i].dataIndex = columndata[i].dataIndex.replace(/fot/g, type.toLowerCase())
						if(columndata[i].text == 'Fot')
							columndata[i].text = type
					}
				}
			}
			return
		}

		var combineRatioChangeColor = function(Lastdata) {
			for (var i = 0; i < Lastdata.length; i++)
			{
				if (Lastdata[i].columns)
					combineRatioChangeColor(Lastdata[i].columns)
				if (Lastdata[i] && Lastdata[i].dataIndex && Lastdata[i].dataIndex.indexOf('VS') != -1) {
					Lastdata[i].renderer = function(value, metaData, record, row, col, store, gridView) {
						// var examstring = tempString[0];
						// var controlstring = tempString[1];
						if (value != 1e9) {
							
							if (value > 1) {
								p = parseInt(1 / value * 255);
								k = ("00" + p.toString(16)).substr(p.toString(16).length)
								s = "#ff" + k + k
								return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + value.toFixed(2) + '</div>'
							} else {
								p = parseInt(value * 255);
								k = ("00" + p.toString(16)).substr(p.toString(16).length)
								s = "#" + k + "ff" + k
								return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + value.toFixed(2) + '</div>'
							}
						} else {
							p = parseInt(1 / value * 255);
							k = ("00" + p.toString(16)).substr(p.toString(16).length)
							s = "#ff" + k + k
							return '<div class="x-grid3-cell-inner" style="background-color:' + s + ';">' + "Infinity" + '</div>'
						}
					}
				}
			}
		}

	    var changeView = function(type) {
	    	change(columndata, type)
	    	var column = []
			var setColumn = function(Lastdata) {
				var ok = false
				for (var i = 0; i < Lastdata.length; i++) {
					if (Lastdata[i].columns)
						setColumn(Lastdata[i].columns)
					else
					{
						column.push(Lastdata[i].dataIndex)
					}
				}
				return
			}
			setColumn(columndata)
	    	combineRatioChangeColor(columndata)
	    	Ext.getCmp(info_compare_tool_index).reconfigure(undefined, columndata)
	    	var tmpStore = Ext.getCmp(info_compare_tool_index).getStore()
	    	tmpStore.getProxy().extraParams['columns'] = column
	    	tmpStore.load()
	    	Ext.example.msg('Change Viewer', 'You has changed the view to <b>{0}</b>.', type);
	    }

		//hide columns function
		var hideColumn = function(columnName){
			var tmpGrid = Ext.getCmp(info_compare_tool_index)
			var columnManager = tmpGrid.columnManager
			var column = columnManager.columns[0]
			var findAndHide = function(columnName, column){
				if(column.text.toLowerCase() == columnName)
				{
					column.hide()
				}
				if(column.child() != null)
					findAndHide(columnName, column.child())
				if(column.next() != null)
					findAndHide(columnName, column.next())
			}
			findAndHide(columnName, column)
		}

	    //help tips
	    var helpTips = {
	    	'Density': 			'Density tips:<br\>Density plotting time could be long.',
	    	'Distribution': 	'Distribution tips:<br\>',
	    	'Correlation': 		'Correlation tips:<br\>Color can be set before plotting.<br\>Plotting time could be long.',
	    	'PCA': 				'PCA tips:<br\>',
	    	'MultiBoxplot': 	'MultiBoxplot tips:<br\>',
	    	'Heatmap': 			'Heatmap tips:<br\>',
	    	'K-means Heatmap': 	'K-means Heatmap tips:<br\>',
	    	'Volcano': 			'Volcano tips:<br\>Choose control and case then GO.',
	    	'Venn': 			'Venn tips:<br\>2 - 5 experiments should be chosen before plotting.',
	    	'PPI': 				'PPI tips:<br\>This tool is still testing.',
	    	'GO Classification':'GO Classification tips:<br\>',
	    	'GO Enrich': 		'GO Enrich tips:<br\>',
	    	'KEGG': 			'KEGG tips:<br\>',
	    	'TF-TG': 			'TF-TG tips:<br\>',
	    	'Kinase/Substrate': 'Kinase/Substrate tips:<br\>'
	    	
	    }

	    //update info

    	this.items = [
		    {
		        region: 'west',
		        xtype: 'panel',
		        title: 'Navigation',
		        flex: 2,
		        layout: 'border',
		        split: true,
		        collapsible: true,
		        floatable: false,
		        items: [
		        {
		            region: 'center',
		            xtype: 'panel',
		            layout: 'accordion',
					flex: 3,
		            header: false,
		            split: true,
		            floatable: false,
		            items: [
		            {
		                title: 'Group Experiment',
		                id: 'west_groupexp',
		                split: true,
		                collapsible: true,
		                floatable: false,
		                collapsed: false,
		                layout: 'border',
		                items: [{
		                	region: 'center',
		                	xtype: 'grid',
		                	id: 'groupExpGrid',
		                	forceFit: true,
		                	border: 0,
		                	columns: [
		                		{ text: 'Record', dataIndex: 'name', sortable: false, menuDisabled: true, flex: 1},
		                		{ text: 'Time', dataIndex: 'time',  menuDisabled: true, flex: 1}
		                	],
		                	store: groupExpHistoryStore
		            	},{
		            		region: 'south',
		            		xtype: 'toolbar',
		            		border: 0,
		            		items: [
		            		{
		            			xtype: 'button',
		            			text: 'Restore',
		            			flex: 1,
		            			handler: function() {
		            				if(!Ext.getCmp('tree_record'))
		            				{
		            					Ext.Msg.alert('Caution','<b>One history record</b> must be chosen before restore.')
		            				}
		            				else
		            				{
		            					if(!(Ext.getCmp('groupexppanel')||(Ext.getCmp('treeinitpanel'))))
			            				{
			            					if(Ext.getCmp('tree_record'))
				            				{
				            					tmpRootNodeFin = Ext.getCmp('tree_record').store.getRootNode().copy(undefined, true);
				            					tmpRootNodeInit = Ext.getCmp('treeRecordInit').store.getRootNode().copy(undefined, true);
				            					tmpRootNodeDust = Ext.getCmp('treeRecordDust').store.getRootNode().copy(undefined, true);
				            				}
				            				if(Ext.getCmp('grouprecordpanel'))
				            					eastpanel.remove(grouprecord);
				            				groupexp = Ext.widget('groupexp');
									    	mainpanel.add(groupexp);
									    	mainpanel.setActiveTab(groupexp);
									    	Ext.getCmp('tree_fin').store.setRootNode(tmpRootNodeFin);

									    	treeinit = Ext.widget('treeinit',{val: val});
									    	eastpanel.add(treeinit);
									    	eastpanel.setActiveTab(treeinit);
									    	Ext.getCmp('tree_init').store.setRootNode(tmpRootNodeInit)
									    	Ext.getCmp('dustbinPanel').store.setRootNode(tmpRootNodeDust)
				            			}
		            				}
		            			}
		            		},{
		            			xtype: 'button',
		            			text: 'Regroup',
		            			flex: 1,
		            			handler: function() {
		            				if(!(Ext.getCmp('groupexppanel')||(Ext.getCmp('treeinitpanel'))))
		            				{
		            					if(Ext.getCmp('grouprecordpanel'))
			            					eastpanel.remove(grouprecord);
			            				groupexp = Ext.widget('groupexp');
								    	mainpanel.add(groupexp);
								    	mainpanel.setActiveTab(groupexp);
	
								    	treeinit = Ext.widget('treeinit',{val: val});
								    	eastpanel.add(treeinit);
								    	eastpanel.setActiveTab(treeinit);
								    }
		            			}
		            		}]
		            	}]
		            },{
		                title: 'Tool Type',
		                id: 'west_tooltype',
		                split: true,
		                bodyStyle : {
		                	overflowX: 'auto',
		                	overflowY: 'auto'
		                },
		                collapsible: true,
		                floatable: false,
		                collapsed: true,
		                items: [tooltypetree]
		            },{
		                title: 'Core Function',
		                xtype: 'panel',
		                border: 0,
		                split: true,
		                collapsible: true,
		                floatable: false,
		                collapsed: true,
		                dockedItems: [{
						    xtype: 'toolbar',
						    dock: 'left',
						    border: 0,
						    items: [{
			                	text: 'Change Viewer',
			                	menu: [{
			                		text: 'Area',
			                		handler: function() {
			                			changeView('Area')
			                		}
			                	},{
			                		text: 'iBaq',
			                		handler: function() {
			                			changeView('Ibaq')
			                		}
			                	},{
			                		text: 'Fot',
			                		handler: function() {
			                			changeView('Fot')
			                		}
		                		}]		                
			                },{
			                	text: 'Hide column',
			                	menu: [{
			                		text: 'Gene ID',
			                		checked: false,
			                		handler: function() {
			                			hideColumn('geneId')
			                		}
			                	},{
			                		text: 'Symbol',
			                		handler: function() {
			                			hideColumn('symbol')
			                		}
			                	},{
			                		text: 'Description',
			                		handler: function() {
			                			hideColumn('description')
			                		}
		                		},{
			                		text: 'Annotation',
			                		handler: function() {
			                			hideColumn('annotation')
			                		}
		                		},{
			                		text: 'Modification',
			                		handler: function() {
			                			hideColumn('modification')
			                		}
		                		},{
			                		text: 'User Defined',
			                		handler: function() {
			                			hideColumn('userDefined')
			                		}
		                		},{
			                		text: 'Area/Ibaq/Fot',
			                		handler: function() {
			                			hideColumn('area')
			                		}
		                		},{
			                		text: 'PSM',
			                		handler: function() {
			                			hideColumn('psm')
			                		}
		                		},{
			                		text: 'Ratio',
			                		handler: function() {
			                			hideColumn('ratio')
			                		}
		                		}]		                
			                },{
			                	xtype: 'button',
			                	text: 'Reset All',
			                	id: 'resetAllButton'+val,
			                	handler: function() {
			                		Ext.Msg.show({
			                			title: 'Attention',
			                			msg: 'This will reset all your work in the tools control panel! Input "RESET" to confirm.', 
			                			prompt: true,
			                			animateTarget: 'resetAllButton'+val,
			                			fn: function(btn, text){
										    if ((btn == 'ok')&&(text == 'RESET')){
										        // start reset all function
										        Ext.getCmp('toolsStatusBar').setStatus({
												    text: 'Starting <b>RESET ALL</b> operation.',
												    clear: {
												        wait: 1500,
												        anim: true,
												        useDefaults: true
												    }
												});
										    }
										    else{
										    	Ext.getCmp('toolsStatusBar').setStatus({
												    text: '<b>RESET ALL</b> operation has been canceled.',
												    clear: {
												        wait: 1500,
												        anim: true,
												        useDefaults: true
												    }
												});
										    }
										}
									});
			                	}
			                },{
								xtype : 'button',
								text : 'Download Data',
								handler : function() {
									data = Ext.getCmp(info_compare_tool_index).filters.getFilterData()
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
									var column = ''
									var setColumnString = function(Lastdata) {
										var ok = false
										for (var i = 0; i < Lastdata.length; i++) {
											if (Lastdata[i].columns)
												setColumnString(Lastdata[i].columns)
											else
											{
												column += (Lastdata[i].dataIndex)
												column += '^'
											}
										}
										column.substring(0,column.length - 1)
										return
									}
									setColumnString(columndata)
									column = encodeURIComponent(column)
									url = '/gardener/newcmpprotein/?download=yes&gridType='+gridType+'&id=' + val + s + '&columns=' + column + '&statistical=' + Ext.getCmp(info_compare_tool_index).getStore().proxy.extraParams.statistical + '&normalizationLevel=' + normalizationLevel
									window.open(url);
								}
			                },{
                                xtype: 'button',
                                text: 'Update Info',
                                handler: function() {
                                    var updateInfoWindow = Ext.create(Ext.window.Window, {
                                        title: 'Update Information',
                                        autoShow: true,
                                        layout: 'anchor',
                                        animateTarget: this,
                                        items: [{
                                                xtype: 'form',
                                                border: 0,
                                                anchor: '100%',
                                                fieldDefaults: {
                                                    labelAlign: 'top',
                                                    msgTarget: 'side'
                                                },
                                                items: [{
                                                        xtype: 'container',
                                                        anchor: '100%',
                                                        layout: 'hbox',
                                                        items: [{
                                                                xtype: 'htmleditor',
                                                                anchor: '100%'
                                                            }]
                                                    }]
                                            }],
                                        dockedItems: [{
                                                xtype: 'toolbar',
                                                dock: 'bottom',
                                                border: 1,
                                                style: {
                                                    borderColor: 'rgb(56,146,211)',
                                                    borderStyle: 'solid'
                                                },
                                                ui: 'footer',
                                                items: ['->', {
                                                        text: 'Save',
                                                        width: 70,
                                                        handler: function() {
                                                        	console.log(updateInfoWindow.down('form').down().down().value)
                                                        	updateInfoWindow.close()
                                                       		Ext.example.msg('UpdateInfo','Update Information is updated.')
                                                        }
                                                    }, {
                                                        text: 'Cancel',
                                                        width: 70,
                                                        handler: function() {
                                                        	updateInfoWindow.close()
                                                        }
                                                    }]
                                            }]
                                    })
                                }
                            }]
			            }]
		            }]
		        },
		        {
		            region: 'south',
		            xtype: 'panel',
		            title: 'Help',
		            id: 'tools-help',
		            layout: 'fit',
					flex: 1,
		            split: true,
		            floatable: false
		        }
		        ]
		    },
		    {
		    	region: 'center',
		    	layout: 'border',
		    	border: 0,
		    	flex: 6,
		    	items: [mainpanel]
		    },
		    {
		        region: 'east',
		        title: 'Data Panel',
		        flex: 3,
		        split: true,
		        collapsible: true,
		        floatable: false,
		        layout: 'fit',
		        border: 0,
		        items: [eastpanel]
		    }
		];

    	this.callParent(arguments);
    },
    /**
     * @method afterRender
     * @inheritdoc
     * @return {void}
     */
    afterRender: function() {

    	this.maximize()
    	//return;
    	var val = this.val 
//    	var update150513 = 	'<p class="p1" style="font-family: helvetica, arial, verdana, sans-serif;"><b><font size="2" style="background-color: rgb(204, 255, 255);">2015/5/13</font></b></p>' +
//    						'<p class="p1" style="background-color: rgb(255, 255, 255);"><font face="verdana" size="2">1.濞ｏ拷锟斤拷绛�锟斤拷濞达拷锟斤拷锟�eptide锟斤拷��ワ拷锟�ools锟斤拷锝�锟斤拷濞肩��锟斤拷��ｏ拷濡����锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟姐��锟介��锟姐�ワ拷��锟斤拷濞�锟介��������bug</font></p>' +
//							'<p class="p1" style="background-color: rgb(255, 255, 255);"><font face="verdana" size="2">2.锟斤拷锟斤拷锟斤拷tack锟斤拷���锟斤拷锟斤拷锟�锟斤拷瀹ワ拷���锟�Density</font></p>' +
//							'<p class="p1" style="background-color: rgb(255, 255, 255);"><font face="verdana" size="2">3.濞ｏ拷锟斤拷绛�锟斤拷濞达拷锟斤拷锟藉��锟�combine濞�锟界�ｏ拷锟斤拷锟斤拷锟姐�ワ拷锟斤拷锟斤拷缂�锟斤拷锟斤拷缁�锟斤拷锟斤拷锟斤拷宕����婵�锟介��锟斤拷锟藉��锟姐�ｏ拷���锟斤拷锟斤拷��ワ拷锟�ug锟斤拷锟藉��锟介��锟斤拷锟斤拷锟斤拷锟�ombine濞�锟界�ｏ拷锟斤拷锟斤拷锟斤拷锟斤拷锟�onditon锟斤拷锟斤拷锟斤拷濞间即锟斤拷��癸拷roup锟斤拷锟斤拷锟斤拷濞间即锟斤拷锟斤拷锟芥��锟藉ù锝�锟斤拷濞达拷濞达拷锟斤拷锟介��锟�</font></p>'

    	var statusBarInitial = Ext.widget('toolsStatusBar',{val: val})

	    //Ext.getCmp('toolsStatusBarPanel').add(statusBarInitial)

	    var recordGroupTree;

    	// /*----- Help tips initialization -----*/
    	// var helpEl
    	// var helpBody = Ext.getCmp('tools-help').body;
    	// helpBody.update('').setStyle('background','#fff');
    	// helpEl = helpBody.createChild();
    	// helpEl.update('You shold <b><i>GROUP/COMBINE</i></b> the experiments before plotting.')

    	Ext.getCmp('groupExpGrid').getSelectionModel().on('select', function(selModel, record) {
    		if(!Ext.getCmp('grouprecordpanel'))
    		{
	    		recordGroupTree = record; 
	    		grouprecord = Ext.widget('grouprecord',{recordGroupTree: recordGroupTree});
		    	eastpanel.add(grouprecord);
		    	eastpanel.setActiveTab(grouprecord);
		    }
		    else
		    {
		    	recordGroupTree = record;
		    	var tmpRootNode = record.data.tree.getRootNode().copy(undefined, true);
		    	Ext.getCmp('tree_record').store.setRootNode(tmpRootNode);
		    	var tmpRootNodeInit = record.data.treeInit.getRootNode().copy(undefined, true);
		    	Ext.getCmp('treeRecordInit').store.setRootNode(tmpRootNodeInit);
		    	var tmpRootNodeDust = record.data.treeDust.getRootNode().copy(undefined, true);
		    	Ext.getCmp('treeRecordDust').store.setRootNode(tmpRootNodeDust);
		    }

    	});

    	//show update info
//    	var task = new Ext.util.DelayedTask(function(){
//    		var showUpdateInfo = Ext.create(Ext.window.Window,{
//    			title: 'Update Info',
//    			width: 400,
//    			height: 300,
//    			layout: 'fit',
//    			autoShow: true,
//    			items:[{
//    				xtype: 'panel',
//    				layout: 'fit',
//    				autoScroll: true,
//    				header: false,
//    			}]
//    		})
//    		var updateInfoBody = showUpdateInfo.down('panel').body.createChild()
//    		updateInfoBody.setStyle('padding','6px')
//    		var updateInfoHistory = ''
//    		updateInfoHistory = update150513 + updateInfoHistory
//    		updateInfoBody.update(updateInfoHistory)
//		});
//		task.delay(2000)

    	this.callParent(arguments);
    }
});