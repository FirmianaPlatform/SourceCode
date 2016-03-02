Ext.define('gar.view.tools.centerpanel.MultiBoxplot', {
	extend : 'Ext.panel.Panel',
	alias : 'widget.MultiBoxplot',
	width : 600,
	split : true,
	floatable : false,
	closable : true,
	title : 'Multi-Boxplot',
	layout : 'border',
	/**
	 * @requires 'gar.view.Notice'
	 */
	requires : ['gar.view.Notice'],

	initComponent : function() {
		var east_temp_panel = Ext.widget('eastMultiBoxplot');
		this.objEastPanel.add(east_temp_panel);
		this.objEastPanel.setActiveTab(east_temp_panel);

		this.on('activate', function() {
					this.objEastPanel.setActiveTab(east_temp_panel)
				})

		this.on('close', function() {
					east_temp_panel.close()
				})

		var tmpHtml = '', tmpPng = '', tmpPdf = ''
		var timestamp = (new Date()).valueOf();
		var statis = 'Average';
		var temp_name = this.temp_name
		var gridType = this.gridType
		switch (groupLevel) {
			case 1 : {
				var plot_level = Ext.create('Ext.data.Store', {
							fields : ['name'],
							data : [{
										"name" : 'Group'
									}]
						})
				break
			}
			case 2 : {
				var plot_level = Ext.create('Ext.data.Store', {
							fields : ['name'],
							data : [{
										"name" : 'Group'
									}, {
										"name" : 'Condition'
									}]
						})
				break
			}
			case 3 : {
				var plot_level = Ext.create('Ext.data.Store', {
							fields : ['name'],
							data : [{
										"name" : 'Group'
									}, {
										"name" : 'Condition'
									}, {
										"name" : 'Experiment'
									}]
						})
				break
			}
			default :
				break
		}

		var getColumn = function(columndata, level) {
			out = [];
			var startNum
			if (newcolumndata[1].dataIndex == 'Sequence') {
				startNum = 5
			} else {
				startNum = 7
			}
			out = [];
			if (level == 'Group') {
				for (var i = startNum; i < columndata.length; i++) {
					out.push(columndata[i].dataIndex);
				}
			} else if (level == 'Condition') {
				for (var i = startNum; i < columndata.length; i++) {
					var gNode = columndata[i]
					for (var j = 0; j < gNode.columns.length; j++) {
						out.push(gNode.columns[j].dataIndex)
					}
				}
			} else if (level == 'Experiment') {
				for (var i = startNum; i < columndata.length; i++) {
					var gNode = columndata[i]
					for (var j = 0; j < gNode.columns.length; j++) {
						var cNode = gNode.columns[j]
						var tempStr = ''
						for (var k = 0; k < cNode.columns.length; k++) {
							out.push(cNode.columns[k].columns[0].columns[0].dataIndex + '|' + cNode.columns[k].columns[0].columns[0].dataIndex)
						}
					}
				}
			}
			compare_grid = Ext.getCmp(info_compare_tool_index);
			temp_filter = compare_grid.filters.buildQuery(compare_grid.filters.getFilterData());
			sorter = []
			var store = compare_grid.store
			if (store.sorters.length > 0) {
				var sorter = store.sorters.getAt(0), dir = sorter.direction, prop = sorter.property, fields = store.model.getFields(), i, applyProp = prop;
				for (i = 0; i < fields.length; i++) {
					if (fields[i].name == prop) {
						applyProp = fields[i].mapping || prop;
						break;
					}
				}
				console.log(applyProp)
				console.log(dir)
				sorter = [{
							"property" : applyProp,
							"direction" : dir
						}]
			}
			sorter=JSON.stringify(sorter)
			return [out, temp_filter, sorter];
		};

		var get = function(columndata, level) {
			temp = getColumn(columndata, level);
			out = temp[0];
			temp_filter = temp[1];
			sorter = temp[2]

		};

		var plot = function(type) {
			var centerWin = Ext.getCmp('PlotFrame' + timestamp)
			var loading = '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>';
			var level = Ext.getCmp('plotlevel' + timestamp).getRawValue();
			var val = String(rec.get('csv_name'));
			centerWin.update(loading);
			get(columndata, level);
			Ext.Ajax.request({
						timeout : 600000,
						url : '/gardener/newcmpprotein/',
						method : 'GET',
						params : {
							id : val,
							levels : out,
							filter : temp_filter,
							R_type : type,
							statis : statis,
							temp_name : temp_name,
							gridType : gridType,
							sort : sorter,
							normalizationLevel : normalizationLevel
						},
						success : function(response) {
							// console.log(response.responseText);
							var tmpResponse = Ext.JSON.decode(response.responseText);
							tmpHtml = tmpResponse.tmpHtml
							tmpPng = tmpResponse.png
							tmpPdf = tmpResponse.pdf
							centerWin.update(tmpHtml);

							// pop success msg
							Ext.example.msg('Suceess', 'Plotting done.')
						},
						failure : function() {
							centerWin.update("<div style='padding:20px'>Sorry! Error happen, please contact Admin with current URL.</div>");
						}
					});
		}

		var statisMenu = Ext.create('Ext.menu.Menu', {
					defaults : {
						checked : false,
						group : 'statismunu' + timestamp
					},
					items : [{
								text : 'Average',
								checked : true,
								handler : function() {
									statis = 'Average'
								}
							}, {
								text : 'Median',
								handler : function() {
									statis = 'Median'
								}
							}]
				})

		this.items = [{
					region : 'north',
					xtype : 'toolbar',
					border : 0,
					items : [{
								xtype : 'combo',
								id : 'plotlevel' + timestamp,
								fieldLabel : 'Plot level:',
								editable : false,
								value : plot_level.last().data.name,
								width : 185,
								labelWidth : 65,
								store : plot_level,
								displayField : 'name'
							}, {
								text : 'Statistical',
								menu : statisMenu
							}, {
								xtype : 'button',
								text : 'GO',
								handler : function() {
									plot('genebox')
								}
							}
					// ,'->',
					// {
					// xtype: 'button',
					// text: 'Download'
					// },
					// {
					// xtype: 'textfield',
					// width: 170,
					// labelWidth: 45,
					// name: 'protein search',
					// fieldLabel: 'Search',
					// emptyText: 'Protein Search',
					// labelAlign: 'right'
					// }
					]
				}, {
					region : 'center',
					xtype : 'panel',
					border : 0,
					id : 'PlotFrame' + timestamp,
					// layout: 'fit',
					autoScroll : true,
					// height: 580,
					html : tmpHtml
				}];
		this.callParent(arguments);
	}
});