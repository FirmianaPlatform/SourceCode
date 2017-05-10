Ext.define('gar.view.tools.centerpanel.Kinase-Substrate',{
    extend: 'Ext.panel.Panel',
  	alias: 'widget.Kinase/Substrate',
    width: 600,
    split: true,
    floatable: false,
    closable: true,
    title: 'Kinase/Substrate', 
	layout:'border',
    initComponent: function() {
		var east_temp_panel = Ext.widget( 'east' + this.title );
	    this.objEastPanel.add(east_temp_panel);
	    this.objEastPanel.setActiveTab(east_temp_panel);
	    
	    var goGridStore = this.goGridStore
	    var goTxt = 'None'
	    
	    this.on('activate', function() { 
			this.objEastPanel.setActiveTab(east_temp_panel)
		}) 		
		
	    this.on('close', function() { 
			east_temp_panel.close()
		}) 			
    	var val = this.val
    	var timestamp = (new Date()).valueOf()
    	var statis = 'Average';
    	var caseExp, controlExp
    	var temp_name = this.temp_name
    	var gridType = this.gridType
    	var tmpHtml=''
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
	        					var tempTextSplit  = columndata[i].columns[j].columns[k].text.split('<br>');
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
			var loading = '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>';
    		var level = Ext.getCmp('plotlevel'+timestamp).getRawValue();
    		var val = String(rec.get('csv_name'));
    		Ext.getCmp('PlotFrame'+timestamp).update(loading);
    		get(columndata, level);
    		console.log(controlExp,caseExp)
    		
			if(goGridStore)
			{
				goTxt = ''
				goGridStore.data.items.forEach(function(item){
					goTxt += item.raw.name
					if(item.index != goGridStore.data.items.length - 1)
						goTxt += ';'
				})
			}
			
    		Ext.Ajax.request({
				timeout : 600000,
				url : '/gardener/newcmpprotein/',
				method : 'POST',
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
					goTxt:goTxt
				},
				success : function(response) {
					//console.log(response.responseText);
					var jsonObject = Ext.JSON.decode(response.responseText)
					tmpHtml = jsonObject.tmpHtml
					Ext.getCmp('PlotFrame'+timestamp).update(tmpHtml);
					//pop success msg
					Ext.example.msg('Suceess','Plotting done.')
				},
				failure : function() {
					Ext.getCmp('PlotFrame'+timestamp).update("Sorry! Error happen, please contact Admin with current URL.");
				}
			});
		}

		//initializing menu
		controlCaseMenuChange(plot_level.last().data.name)

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
	            width: 185,
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
	        	text: 'Controll Exp',
	        	menu: controlExpMenu
	        },{
	        	text: 'Case Exp',
	        	menu: caseExpMenu
	        },{
				text: 'Statistical',
	        	menu: statisMenu
        	},{
	        	xtype: 'button',
	        	text: 'GO',
	        	handler: function() {
	        		plot('kinaseSubstrate')
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