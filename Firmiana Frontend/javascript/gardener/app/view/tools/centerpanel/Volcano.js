Ext.define('gar.view.tools.centerpanel.Volcano',{
    extend: 'Ext.panel.Panel',
    alias: 'widget.Volcano',
    width: 600,
    split: true,
    floatable: false,
    closable: true,
    title: 'Volcano',
    layout:'border',
    /**
     * @requires 'gar.view.Notice'
     */
    requires: [
    	'gar.view.Notice'
    ],

    initComponent: function() {
		var east_temp_panel = Ext.widget( 'east' + this.title );
	    this.objEastPanel.add(east_temp_panel);
	    this.objEastPanel.setActiveTab(east_temp_panel);
	    
	    this.on('activate', function() { 
			this.objEastPanel.setActiveTab(east_temp_panel)
		}) 		
		
	    this.on('close', function() { 
			east_temp_panel.close()
		}) 
		
    	var val = this.val
    	var timestamp = (new Date()).valueOf();
    	var statis = 'Average';
    	var caseExp, controlExp
    	var tmpHtml=''
    	var temp_name = this.temp_name
    	var gridType = this.gridType
    	//initializing caseExp and controlExp menu
        var controlExpMenu = Ext.create('Ext.menu.Menu',{
        	defaults: {
        		checked:false,
        		group: 'controlExpMenu' + timestamp
        	}
        })
        var caseExpMenu = Ext.create('Ext.menu.Menu',{
        	defaults: {
        		checked:false,
        		group: 'caseExpMenu' + timestamp
        	}
        })
        var statisMenu = Ext.create('Ext.menu.Menu',{
        	defaults: {
        		checked: false,
        		group: 'statismunu' + timestamp
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
        
        var xlim = ylim = 5;
		var xlimOpt = Ext.create('Ext.data.Store', {
			fields : ['name'],
			data : [{ "name" : 3 }, 
					{ "name" : 4 }, 
					{ "name" : 5 },
					{ "name" : 6 },
					{ "name" : 7 },
					{ "name" : 8 },
					{ "name" : 9 },
					{ "name" : 10 }]
		});
		
		var ylimOpt = Ext.create('Ext.data.Store', {
			fields : ['name'],
			data : [{ "name" : 3 }, 
					{ "name" : 4 }, 
					{ "name" : 5 },
					{ "name" : 6 }]
		});
		
    	// //initializing expStore
    	// var expStore = Ext.create('gar.store.CompareTree');
     //    expStore.getProxy().extraParams = {
     //        val : val
     //    }

        //different condition for different plot level
        var controlCaseMenuChange = function(level) {
        	if(level == 'Experiment')
	        {
	        	controlExpMenu.removeAll()
	        	caseExpMenu.removeAll()


	        	for(var i = 1; i < columndata.length; i++)
	        	{
	        		if(columndata[i].dataIndex.indexOf('repeat') != -1)
	        		{
	        			for(var j = 0; j < columndata[i].columns.length; j++)
	        				for(var k = 0; k < columndata[i].columns[j].columns.length; k++)
	        				{
	        					var tempTextSplit  = columndata[i].columns[j].columns[k].text.split('<br\>');
	        					var tempText = tempTextSplit[0]+'_'+tempTextSplit[1]+'_'+tempTextSplit[2]
	        					var tempValue = columndata[i].columns[j].columns[k].dataIndex
	        					controlExpMenu.add({
						            text: tempText,
						            value: tempValue,
						            handler: function(item) {
						            	controlExp = item.value
						            	Ext.example.msg('Control Experiment', 'Control experiment has been set to <b>{0}</b>.', item.text);
						            }
						        })
						        
						        caseExpMenu.add({
						            text: tempText,
						            value: tempValue,
						            handler: function(item) {
						            	caseExp = item.value
						            	Ext.example.msg('Case Experiment', 'Case experiment has been set to <b>{0}</b>.', item.text);
						            }
						        })
	        				}
	        		}
	        	}
	        }
	        else if(level == 'Condition')
	        {
	        	controlExpMenu.removeAll()
	        	caseExpMenu.removeAll()
	        	
	        	for(var i = 1; i < columndata.length; i++)
	        	{
	        		if(columndata[i].dataIndex.indexOf('repeat') != -1)
	        		{
	        			var tempControlConditionMenu = Ext.create('Ext.menu.Menu',{
				        	defaults: {
				        		checked:false,
				        		group: 'controlExpMenu'
				        	}
				        })
				        var tempCaseConditionMenu = Ext.create('Ext.menu.Menu',{
				        	defaults: {
				        		checked:false,
				        		group: 'caseExpMenu'
				        	}
				        })

				        controlExpMenu.add({
				            text: columndata[i].text,
				            menu: tempControlConditionMenu
				        })
				        
				        caseExpMenu.add({
				            text: columndata[i].text,
				            menu: tempCaseConditionMenu
				        })

				        for(var j = 0; j < columndata[i].columns.length; j++)
				        {
				        	tempControlConditionMenu.add({
					            text: columndata[i].columns[j].text,
					            value: columndata[i].columns[j].dataIndex,
					            handler: function(item) {
					            	controlExp = item.value
					            	Ext.example.msg('Control Experiment', 'Control experiment has been set to <b>{0}</b>.', item.text);
					            }
					        })
					        tempCaseConditionMenu.add({
					            text: columndata[i].columns[j].text,
					            value: columndata[i].columns[j].dataIndex,
					            handler: function(item) {
					            	caseExp = item.value
					            	Ext.example.msg('Case Experiment', 'Case experiment has been set to <b>{0}</b>.', item.text);
					            }
					        })
				        }
	        		}
	        	}
	        }
	        else if (level == 'Group')
	        {
	        	controlExpMenu.removeAll()
	        	caseExpMenu.removeAll()

	        	for(var i = 1; i < columndata.length; i++)
	        	{
	        		if(columndata[i].dataIndex.indexOf('repeat') != -1)
	        		{
	        			controlExpMenu.add({
				            text: columndata[i].text,
				            value: columndata[i].dataIndex,
				            handler: function(item) {
				            	controlExp = item.value
				            	Ext.example.msg('Control Experiment', 'Control experiment has been set to <b>{0}</b>.', item.text);
				            }
				        })
				        
				        caseExpMenu.add({
				            text: columndata[i].text,
				            value: columndata[i].dataIndex,
				            handler: function(item) {
				            	caseExp = item.value
				            	Ext.example.msg('Case Experiment', 'Case experiment has been set to <b>{0}</b>.', item.text);
				            }
				        })
	        		}
	        	}
	        }
        }
        

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
			if(!controlExp || !caseExp){
				Ext.Msg.alert('Warning','None control or case was selected.');
				return
			}
			if(controlExp == caseExp){
				Ext.Msg.alert('Warning','Control is same to case.');
				return
			}
			var centerWin = Ext.getCmp('PlotFrame'+timestamp)
			var loading = '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>';
    		var level = Ext.getCmp('plotlevel'+timestamp).getRawValue();
    		var val = String(rec.get('csv_name'));
    		centerWin.update(loading);
    		get(columndata, level);
    		console.log(controlExp,caseExp)
    		
    		east_temp_panel.down('grid').disable();
    		Ext.Ajax.request({
				timeout : 600000,
				url : '/gardener/newcmpprotein/',
				method : 'GET',
				params : {
					id : val,
					levels : out,
					filter : temp_filter,
					R_type : type,
					statistical : statis,
					controlExp: controlExp,
					caseExp: caseExp,
					temp_name:temp_name,
					gridType:gridType,
					normalizationLevel: normalizationLevel,
					xlim:xlim,
					ylim:ylim
				},
				success : function(response) {
					//console.log(response.responseText);
					var jsonObject = Ext.JSON.decode(response.responseText)
					tmpHtml = jsonObject.tmpHtml
					east_temp_panel.dataTxt = jsonObject.dataTxt
					centerWin.update(tmpHtml);
					
					dataJson = jsonObject.ratioPvalueList
					var fileListStore = Ext.create('Ext.data.Store', {
						data:dataJson,
						fields : [{
									name : 'symbol',
									type : 'string'
								},{
									name : 'ratio',
									type : 'float'
								},{
									name : 'pvalue',
									type : 'float'
								}],
								listeners : {},
						autoLoad : true
					});
					//fileListStore.sort('Description','DESC');
					east_temp_panel.down('grid').reconfigure(fileListStore)
					east_temp_panel.down('grid').enable();
					
					//pop success msg
					Ext.example.msg('Suceess','Plotting done.')
				},
				failure : function() {
					centerWin.update("Sorry! Error happen, please contact Admin with current URL.");
					east_temp_panel.down('grid').enable();
				}
			});
		}

		//initializing menu
		controlCaseMenuChange(plot_level.last().data.name)

    	this.items = [{
    		region:'north',
	        xtype: 'toolbar',
	        border: 0,
	        items: [{
	            xtype: 'combo',
	            id: 'plotlevel'+timestamp,
	            fieldLabel: 'Plot level:',
				editable : false,
	            value: plot_level.last().data.name,
	            width: 175,
	            labelWidth: 65,
	            store: plot_level,
	            displayField: 'name',
	            listeners : {
	            	change: function(me, newValue, oldValue, eOpts)
	            	{
	            		controlCaseMenuChange(newValue)
	            	}
	            }
	        },{
	        	text: 'Controll',
	        	menu: controlExpMenu
	        },{
	        	text: 'Case',
	        	menu: caseExpMenu
	        },{
				text: 'Statistical',
	        	menu: statisMenu
        	},{
				xtype : 'combo',
				//id : 'toolsPcaPc1' + timestamp,
				editable : false,
				fieldLabel : 'X:',
				value : 5,
				width : 72,
				labelWidth : 18,
				store : xlimOpt,
				displayField : 'name',
	            listeners: {
	            	change: function(item, newvalue) {
	            		xlim = newvalue
	            	}
	            }
			},{
				xtype : 'combo',
				//id : 'toolsPcaPc2' + timestamp,
				editable : false,
				fieldLabel : 'Y:',
				value : 5,
				width : 68,
				labelWidth : 18,
				store : ylimOpt,
				displayField : 'name',
	            listeners: {
	            	change: function(item, newvalue) {
	            		ylim = newvalue
	            	}
	            }
			},{
	        	xtype: 'button',
	        	text: 'GO',
	        	handler: function() {
	        		plot('volcano')
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
	        //maximizable : true,
	        //layout: 'fit',
	        //height: 500,
	        autoScroll:true,
	        html: ''
	    }
	    ];
	    this.callParent(arguments);
    }
});
