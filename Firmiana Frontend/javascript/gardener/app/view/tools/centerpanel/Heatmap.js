Ext.define('gar.view.tools.centerpanel.Heatmap',{
    extend: 'Ext.panel.Panel',
    alias: 'widget.Heatmap',
    width: 600,
    split: true,
    floatable: false,
    closable: true,
    title: 'Heatmap',
	layout:'border',
    
    /**
     * @requires 'gar.view.Notice'
     */
    requires: [
    	'gar.view.Notice'
    ],

    initComponent: function() {
    	var temp_name = this.temp_name
    	var gridType = this.gridType
		var east_temp_panel = Ext.widget( 'east' + this.title.replace(" ","") );
	    this.objEastPanel.add(east_temp_panel);
	    this.objEastPanel.setActiveTab(east_temp_panel);
	    
	    this.on('activate', function() { 
			this.objEastPanel.setActiveTab(east_temp_panel)
		}) 		
		
	    this.on('close', function() { 
			east_temp_panel.close()
		}) 	
    	var timestamp = (new Date()).valueOf();
    	var statis = 'Average';

    	var minValue = '3366FF';
    	var maxValue = 'FF0000';
    	var cutoff = 0.01
    	var fontsize = 8
    	var zscore = 'Yes'
    	var log = 'Yes'
    	var clusterType = 'Bilateral'

    	switch(groupLevel)
    	{
    		case 1: {
    			var plot_level = Ext.create('Ext.data.Store', {
		    		fields: ['name'],
		    		data : [
		        		{"name": 'Group'}
					]
				})
				break
    		}
    		case 2: {
    			var plot_level = Ext.create('Ext.data.Store', {
		    		fields: ['name'],
		    		data : [
		        		{"name": 'Group'},
		        		{"name": 'Condition'}
					]
				})
				break
    		}
    		case 3: {
    			var plot_level = Ext.create('Ext.data.Store', {
		    		fields: ['name'],
		    		data : [
		        		{"name": 'Group'},
		        		{"name": 'Condition'},
		        		{"name": 'Experiment'}
					]
				})
				break
    		}
    		default: break
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
            if (level == 'Group') 
            {
                for (var i = startNum; i < columndata.length; i++) {
                    out.push(columndata[i].dataIndex);
                }
            } 
            else if (level == 'Condition') 
            {
                for (var i = startNum; i < columndata.length; i++) {
                    var gNode = columndata[i]
                    for (var j = 0; j < gNode.columns.length; j++) {
                        out.push(gNode.columns[j].dataIndex)
                    }
                }
            } 
			else if (level == 'Experiment')
			{
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
			return [out, temp_filter];
		};

		var get = function(columndata, level) {
			temp = getColumn(columndata, level);
			out = temp[0];
			temp_filter = temp[1];

		};

		var plot = function(type){
			var level = Ext.getCmp('plotlevel'+timestamp).getRawValue();
			get(columndata, level);
			if(out.length < 2){
				Ext.Msg.alert('Warning','Need two or more '+level+'s.');
				return
			}
			
			var loading = '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>';
    		
    		
    		var val = String(rec.get('csv_name'));
    		//var type = 'boxplot';
    		Ext.getCmp('PlotFrame'+timestamp).update(loading);
    		
    		Ext.Ajax.request({
				timeout : 600000,
				url : '/gardener/newcmpprotein/',
				method : 'GET',
				params : {
					id : val,
					levels : out,
					filter : temp_filter,
					R_type : type,
					minValue: minValue,
					maxValue: maxValue,
					statistical : statis,
					temp_name:temp_name,
					gridType:gridType,
					normalizationLevel: normalizationLevel,
					zscore: zscore,
					cutoff: cutoff,
					log: log,
					clusterType: clusterType,
					fontsize : fontsize
				},
				success : function(response) {
					console.log(response.responseText);
					Ext.getCmp('PlotFrame'+timestamp).update(response.responseText);

					//pop success msg
					Ext.example.msg('Suceess','Plotting done.')
				},
				failure : function() {
					Ext.getCmp('PlotFrame'+timestamp).update("Sorry! Error happen, please contact Admin with current URL.");
				}
			});
		}

		var colorPickerFrom = Ext.create('Ext.menu.ColorPicker', {
		    value: '3366FF',
		    listeners: {
	        select: function(picker, selColor) {
	            minValue = selColor;
		        }
		    }
		});

		var colorPickerTo = Ext.create('Ext.menu.ColorPicker', {
		    value: 'FF0000',
		    listeners: {
	        select: function(picker, selColor) {
	            maxValue = selColor;
		        }
		    }
		});

		var zscoreMenu = Ext.create('Ext.menu.Menu',{
        	defaults: {
        		checked: false,
        		group: 'zscoremenu'+timestamp
        	},
        	items: [{
        		text: 'Yes',
        		checked: true,
        		handler: function() {
        			zscore = 'Yes'
        		}
        	},{
        		text: 'No',
        		handler: function() {
        			zscore = 'No'
        		}
        	}]
        })

        var logMenu = Ext.create('Ext.menu.Menu',{
        	defaults: {
        		checked: false,
        		group: 'logmenu'+timestamp
        	},
        	items: [{
        		text: 'Yes',
        		checked: true,
        		handler: function() {
        			log = 'Yes'
        		}
        	},{
        		text: 'No',
        		handler: function() {
        			log = 'No'
        		}
        	}]
        })

        var clusterTypeMenu = Ext.create('Ext.menu.Menu',{
        	defaults: {
        		checked: false,
        		group: 'clusterType' + timestamp
        	},
        	items: [{
        		text: 'Unilateral Clustering',
        		handler: function() {
        			clusterType = 'Unilateral'
        		}
        	},{
        		text: 'Bilateral Clustering',
        		checked: true,
        		handler: function() {
        			clusterType = 'Bilateral'
        		}
        	}]
        })

        var statisMenu = Ext.create('Ext.menu.Menu',{
        	defaults: {
        		checked: false,
        		group: 'statismunu'+timestamp
        	},
        	items: [{
        		text: 'Average',
        		checked: true,
        		handler: function() {
        			statis = 'Average'
        		}
        	},{
        		text: 'Median',
        		handler: function() {
        			statis = 'Median'
        		}
        	}]
        })

    	this.items = [{
	        region:'north',
	        xtype: 'toolbar',
	        border: 0,
	        items: [{
	            xtype: 'combo',
	            id: 'plotlevel'+timestamp,
	            fieldLabel: 'Plot Level:',
				editable : false,
	            value: plot_level.last().data.name,
	            width: 155,
	            labelWidth: 40,
	            store: plot_level,
	            displayField: 'name'
	        },{
	        	xtype: 'numberfield',
	            fieldLabel: 'Cutoff',
	            name: 'cutoff',
	            width: 120,
	            labelWidth: 45,
	            value: 0.01,
	            minValue: 0.01,
	            maxValue: 1e9,
	            step: 0.01,
	            listeners: {
	            	change: function(item, newvalue) {
	            		cutoff = newvalue
	            	}
	            }
	        },{
	        	xtype: 'numberfield',
	            fieldLabel: 'Font Size',
	            name: 'fontsize',
	            width: 100,
	            labelWidth: 45,
	            value: 8,
	            minValue: 1,
	            maxValue: 20,
	            step: 1,
	            listeners: {
	            	change: function(item, newvalue) {
	            		fontsize = newvalue
	            	}
	            }
	        },{
	        	text: 'Param',
	        	menu: [{
	        		text: 'Zscore',
	        		menu: zscoreMenu
	        	},{
	        		text: 'Log',
	        		menu: logMenu
	        	},{
	        		text: 'Cluster Type',
	        		menu: clusterTypeMenu
	        	}]
	        },{
	        	text: 'Options',
	        	menu: [{
					text: 'Statistical',
		        	menu: statisMenu
	        	},{
	        		text: 'Color Selector',
		        	menu: [{
		        		text: 'From',
		        		menu: colorPickerFrom
		        	},{
		        		text: 'To',
		        		menu: colorPickerTo
		        	}]
	        	}]
	        },{
	        	xtype: 'button',
	        	text: 'GO',
	        	handler: function() {
	        		plot('heatmap')
	        	}
	        },'->',
	        {
	        	xtype: 'button',
	        	text: 'Download'
	        }
	        // {
	        //     xtype: 'textfield',
	        //     width: 170,
	        //     labelWidth: 45,
	        //     name: 'protein search',
	        //     fieldLabel: 'Search',
	        //     emptyText: 'Protein Search',
	        //     labelAlign: 'right'
	        // }
	        ]
	    },{
	        region:'center',
	        xtype: 'panel',
	        border: 0,
	        id: 'PlotFrame'+timestamp,
	        autoScroll:true,
	        //layout: 'fit',
	        //height: 600,
	        html: ''
	    }
	    ];
	    this.callParent(arguments);
    }
});