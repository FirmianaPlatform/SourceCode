Ext.define('gar.view.tools.centerpanel.GroupExperiment',{
	/**
	 * @requires Ext.window.MessageBox
	 */
	requires: [
		'Ext.window.MessageBox'
	],
    extend: 'Ext.panel.Panel',
    alias: 'widget.groupexp',
    id: 'groupexppanel',
    // width: 600,
    autoScroll: false,
    split: true,
    floatable: false,
    closable: false,
    title: 'Group Experiment',
    layout: 'border',
    /**
     * @requires 'gar.view.Notice'
     */
    requires: [
    	
    ],

    initComponent: function() {

    	var me = this;
    	store_fin = Ext.create('Ext.data.TreeStore');
    	store_fin.setRootNode('');

    	var group_index = 1;
    	var condition_index = [];
    	var condition_flag = 0;
    	var thisNode = new Object();

    	//initialize tree
    	var root_fin = store_fin.getRootNode();
    	root_fin.appendChild({
			text: 'Group' + group_index,
			leaf: false,
			checked : false
		});
		group_index++;
		root_fin.lastChild.appendChild({
			text: 'Condition1',
			leaf: false,
			checked : false
		})
		root_fin.lastChild.expand();
		condition_index.push(2);

		var change = function(Lastdata) {
			for (var i = 0; i < Lastdata.length; i++) {
				if (Lastdata[i].columns)
					change(Lastdata[i].columns)
				if (Lastdata[i] && Lastdata[i].text) {
					if (Lastdata[i].dataIndex && Lastdata[i].dataIndex.indexOf('VS') != -1) {
						var tempString = Lastdata[i].dataIndex.split('VS')
						Lastdata[i].renderer = function(value, metaData, record, row, col, store, gridView) {
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
    	

    	this.items = [
    	{
    		xtype: 'toolbar',
    		border: '1 1 0 1',
    		region: 'north',
    		items: [
	    		{
	    			xtype: 'button',
	    			text: 'New Group',
	    			handler: function() {
	    				root_fin.appendChild({
	    					text: 'Group' + group_index,
	    					leaf: false,
	    					checked : false
	    				});
	    				group_index++;
	    				root_fin.lastChild.appendChild({
	    					text: 'Condition1',
	    					leaf: false,
	    					checked : false
	    				})
	    				root_fin.lastChild.expand();
	    				condition_index.push(2);
	    			}
	    		},
	    		{
	    			xtype: 'button',
	    			text: 'New Condition',
	    			handler: function() {
	    				if(condition_flag == 1)
	    				{
	    					thisNode.appendChild({
								text : 'Condition'+condition_index[thisNode.data.text[5]-1],
								leaf : false,
								checked : false
							});
							condition_index[thisNode.data.text[5]-1]++;
							thisNode.expand();
	    				}
	    				else
	    				{
	    					Ext.Msg.alert('Error!', 'Make sure that you have selected a <b>GROUP</b>.');
	    				}
	    			}
	    		},{
	    			xtype: 'button',
	    			text: 'Delete',
	    			handler: function() {
	    				Ext.getCmp('dustbinPanel').getRootNode().appendChild(thisNode)
	    			}
	    		},{
	    			xtype: 'button',
	    			text: 'Reset',
	    			handler: function() {
	    				store_fin.getRootNode().removeAll();
	    				group_index = 1;
    					condition_index = [];
    					condition_flag = 0;
    					Ext.getCmp('tree_init').store.load();
    					Ext.getCmp('dustbinPanel').store.load();
    				}
	    		},'-',{
	    			xtype: 'button',
	    			text: 'Dustbin',
	    			handler: function() {
	    				var cp = Ext.getCmp('dustbinPanel');
	    				cp.show();
	    				cp.expand();
	    			},
	    		},'-',{
	    			text: 'Combine',
	    			menu: [{
	    				text: 'Group',
	    				menu: [{
	    					text: 'Average',
	    					handler: function() {
	    						groupLevel = 1
		    					combineGroup('avg')
	    					}
	    				},{
	    					text: 'Median',
	    					handler: function() {
	    						groupLevel = 1
	    						combineGroup('med')
	    					}
	    				}]
	    				
	    			},{
	    				text: 'Condition',
	    				menu: [{
	    					text: 'Average',
	    					handler: function() {
	    						groupLevel = 2
	    						combineCondition('avg')
	    					}
	    				},{
	    					text: 'Median',
	    					handler: function() {
	    						groupLevel = 2
	    						combineCondition('med')
	    					}
	    				}]
	    			}]
	    		},
	    		{
	    			xtype: 'button',
	    			text: 'Group Done',
	    			handler: function() {
	    				groupLevel = 3
	    				var nodeStore = Ext.getCmp('tree_fin').getRootNode();
	    				columndata = oldcolumndata;
	    				newcolumndata = [];
	    				if (columndata[1].dataIndex == 'Sequence') {
							for (i = 0; i < 5; i++) {
								newcolumndata.push(columndata[i])
							}
						} else {
							for (i = 0; i < 7; i++) {
								newcolumndata.push(columndata[i])
							}
						}
						nodeStore.eachChild(function(n) {
							if (n.isLeaf()) {
								var x = new Object();
								pp = n.raw.text.split('_')
								x["text"] = pp[0]
								// for (i = 0; i < columndata.length; i++) {
								// 	if (columndata[i].text.indexOf(pp[0]) != -1) {
								// 		newcolumndata.push(columndata[i])

								// 		var tempIndexText = columndata[i].columns[0].columns[0].dataIndex.split('_')
								// 		x["dataIndex"] = tempIndexText[0]+'_'+tempIndexText[1]+'_'+tempIndexText[2]+'_'+tempIndexText[3]
								// 		console.log(x)
								// 	}
								// }
							} else if (n.raw.text.indexOf("Group") != -1) {
								var groupNode = new Object();
								groupNode["text"] = n.data.text
								var tempGroupIndexText = n.data.text + '|';
								var b = []
								for (i = 0; i < n.childNodes.length; i++) {
									var tempConditionIndexText = n.data.text + '_' + n.childNodes[i].data.text + '|'
									cNode = n.childNodes[i]
									if (cNode.isLeaf()) {
										alert("Experiments must under 1 condition")
										return
									}
									var cNodeColumns = new Object()
									var cNodeColumnList = []
									for (j = 0; j < cNode.childNodes.length; j++) {
										var x = new Object();
										pp = cNode.childNodes[j].raw.text.split('_')
										for (k = 0; k < columndata.length; k++) {
											if (columndata[k].text.indexOf(pp[0]) != -1) {
												x = columndata[k]
												var tempIndexText = columndata[k].columns[0].columns[0].dataIndex
												x["dataIndex"] = x.text + '|' + tempIndexText
												tempConditionIndexText += tempIndexText
												if(j != cNode.childNodes.length - 1)
													tempConditionIndexText += ';'
												tempGroupIndexText += tempIndexText
												if((i != n.childNodes.length - 1)||(j != cNode.childNodes.length - 1))
													tempGroupIndexText += ';'
											}
										}
										x["checked"] = cNode.childNodes[j].data.checked
										cNodeColumnList.push(x)
									}
									cNodeColumns['text'] = cNode.data.text
									cNodeColumns['columns'] = cNodeColumnList
									cNodeColumns['dataIndex'] = tempConditionIndexText
									// console.log(cNodeColumns)
									b.push(cNodeColumns)
								}
								groupNode['columns'] = b
								groupNode['dataIndex'] = tempGroupIndexText
								newcolumndata.push(groupNode)
							}
						})
						columndata = newcolumndata

						/*======= Something about ratio =======*/
						for (i = 0; i < columndata.length; i++) {
							if (columndata[i].text == 'Annotation') {
							} else if (columndata[i].columns) {
								groupNode = columndata[i]
								for (j = 0; j < groupNode.columns.length; j++) {
									cNode = groupNode.columns[j]
									checkNum = 0
									var temp = -1
									for (k = 0; k < cNode.columns.length; k++) {
										if (cNode.columns[k].checked) {
											temp = k
											checkNum = checkNum + 1
											controlString = cNode.columns[k].columns[0].columns[0].dataIndex
										}
									}
									if(temp == -1)
										continue
									if (checkNum > 1) {
										// console.log(checkNum)
										alert("You should choose 1 Experiment as control")
										return
									} else {
										for (k = 0; k < cNode.columns.length; k++) {
											testString = String(columndata[i].columns[j].columns[k].columns[0].columns[0].dataIndex)
											columndata[i].columns[j].columns[k].columns[0].columns[0].renderer = function(value, metaData, record, row, col, store, gridView) {
												return value.toExponential(2)
											}
											if (k != temp) {
												columndata[i].columns[j].columns[k].columns[0].columns[2].filter = {
													type : 'float',
													encode : 'true'
												}
												columndata[i].columns[j].columns[k].columns[0].columns[2].sortable = true
												columndata[i].columns[j].columns[k].columns[0].columns[2].dataIndex = columndata[i].columns[j].columns[k].columns[0].columns[0].dataIndex + 'VS' + controlString
											} else {
												columndata[i].columns[j].columns[k].columns[0].columns[2].dataIndex = columndata[i].columns[j].columns[k].columns[0].columns[0].dataIndex.split('VS')[0]
												var len = columndata[i].columns[j].columns[k].columns[0].columns[2].dataIndex.length
												columndata[i].columns[j].columns[k].columns[0].columns[2].dataIndex = columndata[i].columns[j].columns[k].columns[0].columns[2].dataIndex.substr(0, len - 4)
												columndata[i].columns[j].columns[k].columns[0].columns[2].dataIndex = columndata[i].columns[j].columns[k].columns[0].columns[2].dataIndex + 'ratio'
												columndata[i].columns[j].columns[k].columns[0].columns[2].renderer = function(value, record) {
													return 1
												}
											}
										}
									}
								}
							}
						}
						
						change(columndata)
						var temp_store = Ext.getCmp('store'+info_compare_tool_index);
						var number = groupExpHistoryStore.data.items.length + 1;
						
						groupExpHistoryStore.add({
							name: 'Record ' + number,
							time: (new Date()).toTimeString().substr(0,8),
							tree: store_fin,
							data: columndata,
							treeInit: Ext.getCmp('tree_init').store,
							treeDust: Ext.getCmp('dustbinPanel').store
						});
						groupExpHistoryStore.save();
						Ext.getCmp(info_compare_tool_index).reconfigure(undefined, columndata);
						Ext.getCmp('west_tooltype').expand();
						Ext.getCmp('groupexppanel').close();
						Ext.getCmp('treeinitpanel').close();
						Ext.example.msg('Group Done', 'Grouping finished.')
						// Group first
						hasGrouped++
	    			}
	    		}
	    	]
    	},
    	{
    		xtype: 'treepanel',
    		region: 'center',
			id: 'tree_fin',
			layout: 'fit',
			border: '0 1 1 1',
			selModel: {
                mode: 'MULTI'
            },
            lines: false,
            useArrows: true,
			scroll: true,
			rootVisible: false,
			store: store_fin,
			hideHeaders: true,
			columns : [{
                xtype : 'treecolumn',
                dataIndex : 'text',
                border: 0,
                flex : 1,
                editor : {
                    xtype : 'textfield',
                    allowBlank : false,
                    allowOnlyWhitespace : false
                }
            }],
            listeners: {
            	'select': function(me, record, index, eOpts) {
		    		thisNode = record;
		    		if(record.data.parentId == 'root')
		    			condition_flag = 1;
		    		else
		    			condition_flag = 0;
		    	},
				'checkchange': function(node, checked) {

					if(checked)
					{
						checkNode = node
						var brothersLength = node.parentNode.childNodes.length
						var thisIndex = node.data.index
						var root = Ext.getCmp('tree_fin').getRootNode();
						var checkResult

						//checkChildren function
						var checkChildren = function(depth) {
							var checkChildrenIter = function(node, depth) {
								if(node.data.depth <= depth)
								{
									for(var i = 0; i < node.childNodes.length; i++)
									{
										if(!checkResult)
											checkChildrenIter(node.childNodes[i],depth);
									}
								}
								else
								{
									if(node.data.checked == true)
									{
										checkResult = node
									}
									for(var i = 0; i < node.childNodes.length; i++)
									{
										if(!checkResult)
											checkChildrenIter(node.childNodes[i],depth)
									}
								}
							}
							checkChildrenIter(root, depth)
						}

						//checkParents functionv
						var checkParents = function(depth) {
							var checkParentsIter = function(node,depth) {
								if(node.data.depth < depth - 1)
								{
									for(var i = 0; i < node.childNodes.length; i++)
									{
										if(!checkResult)
										{
											if(node.childNodes[i].data.checked == true)
												checkResult = node.childNodes[i]
											checkParentsIter(node.childNodes[i],depth)
										}
									}
								}
							}
							checkParentsIter(root, depth)
						}

						//check brothers
						for(var i = 0; i < brothersLength; i++)
						{
							if(i != thisIndex)
							{
								if(node.parentNode.childNodes[i].data.checked)
								{
									node.parentNode.childNodes[i].set('cls','toolsControlPanel_alert')
									Ext.Msg.alert('Attention','A conflict is detected.',function() {
										node.parentNode.childNodes[i].set('cls','')
										node.set('checked',false)
									})
									break
								}
							}
						}

						//check children
						checkChildren(node.data.depth)
						if(checkResult)
						{
							checkResult.set('cls','toolsControlPanel_alert')
							Ext.Msg.alert('Attention','A conflict is detected.',function() {
								checkResult.set('cls','')
								node.set('checked',false)
								checkResult = null
							})
						}

						//check parents
						checkParents(node.data.depth)
						if(checkResult)
						{
							checkResult.set('cls','toolsControlPanel_alert')
							Ext.Msg.alert('Attention','A conflict is detected.',function() {
								checkResult.set('cls','')
								node.set('checked',false)
								checkResult = null
							})
						}
						
					}

				}		
            },
			viewConfig : {
				plugins : {
					ptype : 'treeviewdragdrop',
					containerScroll : true
				}
			},
			plugins: {
				ptype : 'cellediting',
				// clicksToEdit : 1,
				listeners : {
					beforeedit : function(editor, e) {
						if(e.record.isLeaf())
							return false
					},
					edit : function(editor, e) {
						// commit the changes right after editing finished
						e.record.commit();
					}
				}
			}
    	}
    	];

    	//combineCondition function
    	var combineCondition = function(type){
			var nodeStore = Ext.getCmp('tree_fin').getRootNode();
			columndata = oldcolumndata;
			newcolumndata = [];
			if (columndata[1].dataIndex == 'Sequence') {
				for (i = 0; i < 5; i++) {
					newcolumndata.push(columndata[i])
				}
			} else {
				for (i = 0; i < 7; i++) {
					newcolumndata.push(columndata[i])
				}
			};
			nodeStore.eachChild(function(n) {
				var ratioController = ''
				if (n.isLeaf()) {
					
				} else if (n.raw.text.indexOf("Group") != -1) {
					var groupNode = new Object();
					groupNode["text"] = n.data.text
					var b = []
					for (i = 0; i < n.childNodes.length; i++) {
						cNode = n.childNodes[i]

						if (cNode.isLeaf()) {
							alert("Experiments must under 1 condition")
							return
						}
						var cNodeColumns = new Object()
						var cNodeColumnList = []

						//dataIndex add 'area'
						var x = new Object();
						x.text = 'Area';
						x.filter = {
							type : 'float',
							encode : 'true'
						}
						x.sortable = true
						x.renderer = function(value, metaData, record, row, col, store, gridView) {
							return value.toExponential(2);
						}
						x.dataIndex = '';
						for (j = 0; j < cNode.childNodes.length; j++) {
							
							pp = cNode.childNodes[j].raw.text.split('_')
							for (k = 0; k < columndata.length; k++) {
								if (columndata[k].text.indexOf(pp[0]) != -1) {
									x.dataIndex += columndata[k].columns[0].columns[0].dataIndex;
								}
							}
							x["checked"] = cNode.childNodes[j].data.checked
							if(j != cNode.childNodes.length - 1)
								x.dataIndex+=';';
						}
						cNodeColumnList.push(x)
						//dataIndex add 'area' end

						//dataIndex add 'Psm'
						x = new Object();
						x.text = 'PSM';
						x.filter = {
							type : 'float',
							encode : 'true'
						}
						x.sortable = true
						x.dataIndex = '';
						for (j = 0; j < cNode.childNodes.length; j++) {
							
							pp = cNode.childNodes[j].raw.text.split('_')
							for (k = 0; k < columndata.length; k++) {
								if (columndata[k].text.indexOf(pp[0]) != -1) {
									x.dataIndex += columndata[k].columns[0].columns[1].dataIndex;
								}
							}
							x["checked"] = cNode.childNodes[j].data.checked
							if(j != cNode.childNodes.length - 1)
								x.dataIndex+=';';
						}
						cNodeColumnList.push(x);
						//dataIndex add 'psm' end

						//dataIndex add 'ratio'
						x = new Object();
						x.text = 'Ratio';
						x.filter = {
							type : 'float',
							encode : 'true'
						}
						x.sortable = true
						x.renderer = function(value, metaData, record, row, col, store, gridView) {
							return value.toExponential(2);
						}
						x.dataIndex = '';
						for (j = 0; j < cNode.childNodes.length; j++) {
							
							pp = cNode.childNodes[j].raw.text.split('_')
							for (k = 0; k < columndata.length; k++) {
								if (columndata[k].text.indexOf(pp[0]) != -1) {
									x.dataIndex += columndata[k].columns[0].columns[0].dataIndex;
								}
							}
							x["checked"] = cNode.childNodes[j].data.checked
							if(j != cNode.childNodes.length - 1)
								x.dataIndex+=';';
						}
						cNodeColumnList.push(x);
						//dataIndex add 'ratio' end
						if(n.childNodes[i].data.checked)
						{
							ratioController = x.dataIndex
						}

						cNodeColumns['text'] = cNode.data.text
						cNodeColumns['columns'] = cNodeColumnList
						b.push(cNodeColumns)
					}
					if(ratioController == ''){
						for(var i = 0; i < b.length; i++)
						{
							b[i].columns[2].dataIndex += 'VS'+b[i].columns[2].dataIndex
						}
					}else{
						for(var i = 0; i < b.length; i++)
						{
							b[i].columns[2].dataIndex += 'VS'+ratioController
						}
					}
					
					groupNode["columns"] = b
					newcolumndata.push(groupNode)
				}
			});

			//set dataIndex for combined group and condition
			var startNum
			if (columndata[1].dataIndex == 'Sequence') {
				startNum = 5
			} else {
				startNum = 7
			}
			for (var i = startNum; i < newcolumndata.length; i++)
			{
				var gNode = newcolumndata[i]
				var tmpDataIndex = ''
				for ( var j = 0; j < gNode.columns.length; j++)
				{
					var cNode = gNode.columns[j]
					tmpDataIndex += cNode.columns[0].dataIndex 
					if(j != gNode.columns.length - 1)
						tmpDataIndex += ';'
					cNode.dataIndex = gNode.text + '_' + cNode.text + '|' + cNode.columns[0].dataIndex
				}
				gNode.dataIndex = gNode.text + '|' + tmpDataIndex
			}

			columndata = newcolumndata;
			
			var column = []
			var columnChange = function(Lastdata) {
				var ok = false
				for (var i = 0; i < Lastdata.length; i++) {
					if (Lastdata[i].columns)
						columnChange(Lastdata[i].columns)
					else
					{
						column.push(Lastdata[i].dataIndex)
					}
				}
				return
			}
			columnChange(columndata)
			combineRatioChangeColor(columndata)
			Ext.getCmp(info_compare_tool_index).reconfigure(undefined, columndata);
			console.log(column)
			var tmpStore = Ext.getCmp(info_compare_tool_index).getStore()
			tmpStore.getProxy().extraParams['columns'] = column
			tmpStore.getProxy().extraParams['statistical'] = type
			tmpStore.load()
			Ext.getCmp('west_tooltype').expand();
			Ext.getCmp('groupexppanel').close();
			Ext.getCmp('treeinitpanel').close();
    	};


    	//combineGroup function
    	var combineGroup = function(type){
			var nodeStore = Ext.getCmp('tree_fin').getRootNode();
			var x
			var ratioController = ''
			columndata = oldcolumndata;
			newcolumndata = [];
			if (columndata[1].dataIndex == 'Sequence') {
				x = columndata[5].columns[0].columns[0].text
				for (i = 0; i < 5; i++) {
					newcolumndata.push(columndata[i])
				}
			} else {
				x = columndata[7].columns[0].columns[0].text
				for (i = 0; i < 7; i++) {
					newcolumndata.push(columndata[i])
				}
			};
			
			nodeStore.eachChild(function(n) {
				if (n.isLeaf()) {
				} else if (n.raw.text.indexOf("Group") != -1) {
					var gNodeColumns = new Object()
					var gNodeColumnList = []
					var groupNode = new Object()

					var area = new Object()
					area.text = x
					area.filter = {
						type : 'float',
						encode : 'true'
					}
					area.sortable = true
					area.dataIndex = ''
					area.renderer = function(value, metaData, record, row, col, store, gridView) {
							return value.toExponential(2);
						}
					var psm = new Object()
					psm.text = 'PSM'
					psm.filter = {
						type : 'float',
						encode : 'true'
					}
					psm.sortable = true
					psm.dataIndex = ''
					psm.renderer = function(value, metaData, record, row, col, store, gridView) {
							return value.toExponential(2);
						}
					var ratio = new Object()
					ratio.text = 'Ratio'
					ratio.filter = {
						type : 'float',
						encode : 'true'
					}
					ratio.sortable = true
					ratio.dataIndex = ''
					ratio.renderer = function(value, metaData, record, row, col, store, gridView) {
							return value.toExponential(2);
						}

					groupNode["text"] = n.data.text
					for (i = 0; i < n.childNodes.length; i++) {
						cNode = n.childNodes[i]
						if (cNode.isLeaf()) {
							alert("Experiments must under 1 condition")
							return
						}

						//dataIndex
						for (j = 0; j < cNode.childNodes.length; j++) {
							
							pp = cNode.childNodes[j].raw.text.split('_')
							for (k = 0; k < columndata.length; k++) {
								if (columndata[k].text.indexOf(pp[0]) != -1) {
									area.dataIndex += columndata[k].columns[0].columns[0].dataIndex;
									psm.dataIndex += columndata[k].columns[0].columns[1].dataIndex;
									ratio.dataIndex += columndata[k].columns[0].columns[0].dataIndex;
								}
							}
							// x["checked"] = cNode.childNodes[j].data.checked
							if(!((i == n.childNodes.length - 1)&&(j == cNode.childNodes.length - 1)))
							{
								area.dataIndex+=';';
								psm.dataIndex+=';';
								ratio.dataIndex+=';';
							}
						}
					}
					if(n.data.checked)
					{
						ratioController = ratio.dataIndex
					}
					// ratio.dataIndex += 'VS'
					// ratio.dataIndex += ratioController
					gNodeColumnList.push(area)
					gNodeColumnList.push(psm)
					gNodeColumnList.push(ratio)
					groupNode['columns'] = gNodeColumnList
					newcolumndata.push(groupNode)
				}
			});
			if (newcolumndata[1].dataIndex == 'Sequence') {
				for (i = 5; i < newcolumndata.length; i++) {
					if(ratioController == '')
					{
						newcolumndata[i].columns[2].dataIndex += 'VS'+newcolumndata[i].columns[2].dataIndex
					}else{
						newcolumndata[i].columns[2].dataIndex += 'VS'+ratioController
					}
				}
			} else {
				for (i = 7; i < newcolumndata.length; i++) {
					if(ratioController == '')
					{
						newcolumndata[i].columns[2].dataIndex += 'VS'+newcolumndata[i].columns[2].dataIndex
					}else{
						newcolumndata[i].columns[2].dataIndex += 'VS'+ratioController
					}
				}
			};

			//set dataIndex for combined group and condition
			var startNum
			if (newcolumndata[1].dataIndex == 'Sequence') {
				startNum = 5
			} else {
				startNum = 7
			}
			for (var i = startNum; i < newcolumndata.length; i++)
			{
				newcolumndata[i].dataIndex = newcolumndata[i].text + '|' + newcolumndata[i].columns[0].dataIndex
			}

			columndata = newcolumndata;

			
			var column = []
			var change = function(Lastdata) {
				var ok = false
				for (var i = 0; i < Lastdata.length; i++) {
					if (Lastdata[i].columns)
						change(Lastdata[i].columns)
					else
					{
						column.push(Lastdata[i].dataIndex)
					}
				}
				return
			}
			change(columndata)
			combineRatioChangeColor(columndata)
			Ext.getCmp(info_compare_tool_index).reconfigure(undefined, columndata);
			var tmpStore = Ext.getCmp(info_compare_tool_index).getStore()
			tmpStore.getProxy().extraParams['columns'] = column
			tmpStore.getProxy().extraParams['statistical'] = type
			tmpStore.load()
			Ext.getCmp('west_tooltype').expand();
			Ext.getCmp('groupexppanel').close();
			Ext.getCmp('treeinitpanel').close();
    	};
	    this.callParent(arguments);
    }
});