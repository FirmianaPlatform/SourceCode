Ext.define('gar.view.tools.centerpanel.Venn',{
    extend: 'Ext.panel.Panel',
    alias: 'widget.Venn',
    width: 600,
    split: true,
    floatable: false,
    closable: true,
    title: 'Venn',
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

		var store_combo = Ext.create('Ext.data.Store', {
			data:[{'name':'A'},{'name':'B'},{'name':'C'}],
			fields : [{
						name : 'name',
						type : 'string'
					}],
			autoLoad : true
			});
			
		var temp_name = this.temp_name
    	var gridType = this.gridType
    	var timestamp = (new Date()).valueOf();
    	var statis = 'Average';
    	var vennExp = []
    	var vennExpNum = 0
    	var vennExpArrayOperator = Ext.Array
    	var vennList = []
		var tmpHtml=''
    	//initializing vennExp menu
        var vennOptionsMenu = Ext.create('Ext.menu.Menu')

        //different condition for different plot level
        var vennOptionsMenuChange = function(level) {
        	if(level == 'Experiment')
	        {
	        	vennOptionsMenu.removeAll()
	        	vennExp = []
	        	vennExpNum = 0
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
	        					vennOptionsMenu.add({
						            text: tempText,
						            value: tempValue,
						            checked: false,
						            listeners: {
						            	beforecheckchange: function(item, checked) {
						            		if((vennExpNum == 5) && checked)
						            		{
						            			Ext.Msg.alert('Attention','You can only check up to <b>5</b> experiments.')
						            			return false
						            		}
						            	},
						            	checkchange: function(item, checked) {
						            		if(checked){
					            				vennExp.push(item.value)
						            			Ext.example.msg('Venn Experiment', 'A new Venn Experiment has been added: <b>{0}</b>.', item.text);
						            			vennExpNum++
						            		}else{
						            			vennExpArrayOperator.remove(vennExp, item.value)
						            			vennExpNum--
						            		}
						            	}
						            }
						        })
	        				}
	        		}
	        	}
	        }
	        else if(level == 'Condition')
	        {
	        	vennOptionsMenu.removeAll()
	        	vennExp = []
	        	vennExpNum = 0
	        	for(var i = 1; i < columndata.length; i++)
	        	{
	        		if(columndata[i].dataIndex.indexOf('repeat') != -1)
	        		{
	        			var tempVennConditionMenu = Ext.create('Ext.menu.Menu')

				        vennOptionsMenu.add({
				            text: columndata[i].text,
				            menu: tempVennConditionMenu
				        })

				        for(var j = 0; j < columndata[i].columns.length; j++)
				        {
				        	tempVennConditionMenu.add({
					            text: columndata[i].columns[j].text,
					            value: columndata[i].columns[j].dataIndex,
					            checked: false,
					            listeners: {
					            	beforecheckchange: function(item, checked) {
					            		if((vennExpNum == 5) && checked)
					            		{
					            			Ext.Msg.alert('Attention','You can only check up to <b>4</b> experiments.')
					            			return false
					            		}
					            	},
					            	checkchange: function(item, checked) {
					            		if(checked){
				            				vennExp.push(item.value)
					            			Ext.example.msg('Venn Experiment', 'A new Venn Experiment has been added: <b>{0}</b>.', item.text);
					            			vennExpNum++
					            		}else{
					            			vennExpArrayOperator.remove(vennExp, item.value)
					            			vennExpNum--
					            		}
					            	}
					            }
					        })
				        }
	        		}
	        	}
	        }
	        else if (level == 'Group')
	        {
	        	vennOptionsMenu.removeAll()
	        	vennExp = []
	        	vennExpNum = 0
	        	for(var i = 1; i < columndata.length; i++)
	        	{
	        		if(columndata[i].dataIndex.indexOf('repeat') != -1)
	        		{
	        			vennOptionsMenu.add({
				            text: columndata[i].text,
				            value: columndata[i].dataIndex,
						    checked: false,
				            listeners: {
				            	beforecheckchange: function(item, checked) {
				            		if((vennExpNum == 5) && checked)
				            		{
				            			Ext.Msg.alert('Attention','You can only check up to <b>4</b> experiments.')
				            			return false
				            		}
				            	},
				            	checkchange: function(item, checked) {
				            		if(checked){
			            				vennExp.push(item.value)
				            			Ext.example.msg('Venn Experiment', 'A new Venn Experiment has been added: <b>{0}</b>.', item.text);
				            			vennExpNum++
				            		}else{
				            			vennExpArrayOperator.remove(vennExp, item.value)
				            			vennExpNum--
				            		}
				            	}
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
			var centerWin = Ext.getCmp('PlotFrame'+timestamp)
			var level = Ext.getCmp('plotlevel'+timestamp).getRawValue();
			if(vennExpNum < 2){
				Ext.Msg.alert('Warning','Need two or more ' + level + 's.');
				return
			}

			var loading = '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>';
    		
    		var val = String(rec.get('csv_name'));
    		centerWin.update(loading);
    		get(columndata, level);
  			console.log(vennExp)
  			
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
					vennExp: vennExp,
					temp_name:temp_name,
					gridType:gridType,
					normalizationLevel: normalizationLevel
				},
				success : function(response) {
					//console.log(response.responseText);
					
					var jsonObject = Ext.JSON.decode(response.responseText)
					tmpHtml = jsonObject.tmpHtml
					vennList = jsonObject.vennList
					regionList = jsonObject.regionList
					
//            		var newStore_combo = Ext.create('Ext.data.Store', {
//						data:regionList,
//						proxy :'memory',
//						fields : [{
//									name : 'name',
//									type : 'string'
//								}]
//						//autoLoad : true
//						});
					store_combo.removeAll()// = regionList
					Ext.Array.forEach(regionList,function(x){
						store_combo.add(x)
					})
					//store_combo.add(newStore_combo.getRange())
					//store_combo.load()
					
					dataJson = vennList['A']
					var fileListStore = Ext.create('Ext.data.Store', {
						data:dataJson,
						fields : [{
									name : 'no',
									type : 'int'
								},{
									name : 'name',
									type : 'string'
								},{
									name : 'region',
									type : 'string'
								}],
								listeners : {},
						autoLoad : true
					});
					
					//fileListStore.filter('region','A');
					
					east_temp_panel.down('grid').reconfigure(fileListStore)
					east_temp_panel.down('grid').enable();
					

					
					centerWin.update(tmpHtml);
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
		vennOptionsMenuChange(plot_level.last().data.name)

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
	            		vennOptionsMenuChange(newValue)
	            	}
	            }
	        },{
				text: 'Statistical',
	        	menu: statisMenu
        	},{
	        	text: 'Dimension',
	        	menu: vennOptionsMenu
	        },{
	        	xtype: 'button',
	        	text: 'GO',
	        	handler: function() {
	        		plot('venn')
	        	}
	        },'->',{
					fieldLabel: 'Region :',
					xtype : 'combo',
					value : 'A',
					displayField : 'name',
		            width: 115,
		            labelWidth: 55,
					store : store_combo,
					queryMode : 'local',
					editable:false,
		            listeners : {
		            	change: function(me, newValue, oldValue, eOpts)
		            	{
		            		//alert(newValue)
		            		//console.log(this.up().up().up().down('grid'))
		            		var vennStore = Ext.create('Ext.data.Store', {
								data:vennList[newValue],
								fields : [{
											name : 'no',
											type : 'int'
										},{
											name : 'name',
											type : 'string'
										},{
											name : 'region',
											type : 'string'
										}],
										listeners : {},
								autoLoad : true
							});
		            		var g = east_temp_panel.down('grid')
		            		g.reconfigure(vennStore)
		            		//sss.load()

		            	}
		            }
					//selectOnFocus: true,
					//typeAhead: true,
					//id : 'anywhere-combo'
			},{
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