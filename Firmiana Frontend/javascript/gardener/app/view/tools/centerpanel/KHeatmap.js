Ext.define('gar.view.tools.centerpanel.KHeatmap',{
    extend: 'Ext.panel.Panel',
    alias: 'widget.K-meansHeatmap',
    width: 600,
    split: true,
    floatable: false,
    closable: true,
    title: 'K-means Heatmap',
    layout:'border',
    /**
     * @requires 'gar.view.Notice'
     */
    requires: [
    	'gar.view.Notice',
    	'gar.view.tools.centerpanel.itemSelector',
    	'Ext.ux.DataView.DragSelector',
	    'Ext.ux.DataView.LabelEditor'
    ],

    initComponent: function() {
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
    	var val = String(rec.get('csv_name'));
    	var level 
    	var knumber = 10
		var kmeanList = {}
		var kmeanImgList
    	var minValue = '3366FF';
    	var maxValue = 'FF0000';
    	var cutoff = 0.01
    	var zscore = 'Yes'
    	var log = 'Yes'
    	var temp_name = this.temp_name
    	var gridType = this.gridType
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
    		var level = Ext.getCmp('plotlevel'+timestamp).getRawValue()
    		knumber = Ext.getCmp('plotKheatmapKNumber'+timestamp).getRawValue()
    		if( knumber<1){
    			Ext.Msg.alert('Warning','K number is too small.')
    			return
    		}
    		// var val = String(rec.get('csv_name'));

    		get(columndata, level);
    		
    		if(out.length < 2){
				Ext.Msg.alert('Warning','Need two or more '+level+'s.');
				return
			}
					
    		console.log(columndata,out,knumber,val)
    		// var loading = '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>';
    		// Ext.getCmp('PlotFrame'+timestamp).update(loading);

    		//loading pic
    		mainImg.setWidth(400)
    		mainImg.setHeight(300)
    		mainImg.setLocalX(140)
    		mainImg.setSrc('/static/images/loading/loading5.gif')
    		    		
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
					k_num : knumber,
					statistical : statis,
					temp_name:temp_name,
					gridType:gridType,
					normalizationLevel: normalizationLevel,
					zscore: zscore,
					cutoff: cutoff,
					log: log 
				},
				success : function(response) {
					// console.log(response.responseText);
					var jsonObject = Ext.JSON.decode(response.responseText)


					//calculate height
					var height 
					if (knumber <= 20)
						height = 350
					else if (knumber > 20)
						height = 350 + (knumber-20)*5

					//set main heatmap img
					//mainImg.setWidth(350)
					mainImg.setSrc('')
    				mainImg.setHeight(height)
    				mainImg.setLocalX(140)
					mainImgUrl = jsonObject.heatmap
					mainImg.setSrc(mainImgUrl)

					//set kmean img
					kmeanImgList = jsonObject.kmean
					dataViewStore.removeAll()
					kmeanImgList.forEach(
						function(item) {
							var kname = item.name
							kmeanList[kname] = item.list
							dataViewStore.add({'name': kname, 'url': item.url})
						}
					)

					//pop success msg
					Ext.example.msg('Suceess','Plotting done.')

				},
				failure : function() {
					Ext.Msg.alert('Error',"Sorry! Error happen, please contact Admin");
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

		get(columndata, level);

		//main img initialize
		var mainImg = Ext.create('Ext.Img',{
        	xtype: 'image',
        	id: 'toolsKHeatmapMainImg' + timestamp
        })

        //dataview store
        var dataViewStore = Ext.create('Ext.data.Store', {
            fields: ['name', 'url', 'txt']
        });
		
        var showSymbolList = function(kmeanID, kmeanUrl){
        	var n = kmeanID.split('-')[1]
    		var fileListStore = Ext.create('Ext.data.Store', {
					data:kmeanList[kmeanID],
					url: kmeanImgList[n - 1].txt,
					fields : [{
								name : 'name',
								type : 'string'
							}],
					autoLoad : true
			});
			//fileListStore.sort('Description','DESC');
			east_temp_panel.down('grid').reconfigure(fileListStore)
			east_temp_panel.down('image').setSrc(kmeanUrl)
			east_temp_panel.down('displayfield').setValue(kmeanList[kmeanID].length)
			//east_temp_panel.down('grid').enable();
        };

        var zscoreMenu = Ext.create('Ext.menu.Menu',{
        	defaults: {
        		checked: false,
        		group: 'kheatzscoremenu' + timestamp
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
	            fieldLabel: 'Plot Level:',
				editable : false,
	            value: plot_level.last().data.name,
	            width: 155,
	            labelWidth: 40,
	            store: plot_level,
	            displayField: 'name'
	        },{
	        	xtype: 'numberfield',
	        	id: 'plotKheatmapKNumber'+timestamp,
	        	fieldLabel: 'K number:',
	        	value: knumber,
	        	width: 120,
	        	minValue: 1,
	        	maxValue: 100,
	        	labelWidth: 60,
	        	listeners: {
	            	change: function(item, newvalue) {
	            		knumber = newvalue
	            	}
	            }
	        },{
	        	xtype: 'numberfield',
	            fieldLabel: 'Cutoff',
	            name: 'cutoff',
	            width: 120,
	            labelWidth: 45,
	            value: cutoff,
	            minValue: 0.01,
	            maxValue: 1e9,
	            step: 0.01,
	            listeners: {
	            	change: function(item, newvalue) {
	            		cutoff = newvalue
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
	        	},
	        	{
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
	        	text: 'Advanced',
	        	handler: function() {
	        		var itemSelector = Ext.widget('itemSelector',{
	        			plotlevel: Ext.getCmp('plotlevel'+timestamp).getRawValue(),
	        			val : val,
						out : out,
						temp_filter : temp_filter,
						Rtype : 'k-heatmap',
						minValue: minValue,
						maxValue: maxValue,
						knumber: knumber,
						statis: statis,
						timestamp: timestamp,
						temp_name:temp_name,
						gridType:gridType,
						zscore: zscore,
						cutoff: cutoff,
						log: log,
						beforedestroy: function() {
							var tmpKmeanList = Ext.JSON.decode(sessionStorage.getItem('kmeanListText'))
							if(tmpKmeanList){kmeanList = tmpKmeanList}
						}
	        		})
	        	}
	        },{
	        	xtype: 'button',
	        	text: 'GO',
	        	handler: function() {
	        		plot('k-heatmap')
	        	}
	        },'->',
	        {
	        	xtype: 'button',
	        	text: 'Download'
	        }
	        ]
	    },{
	    	region:'center',
	    	border: 0,
	    	layout: 'anchor',
	    	autoScroll: true,
	    	items: [{
		    		xtype: 'panel',
		    		border: 0,
		    		autoScroll: true,
		    		anchor: '100%, 70%',
			        id: 'PlotFrame' + timestamp,
			        layout: 'absolute',
			        items: [mainImg]
		        },{
		        	xtype: 'panel',
		        	cls: 'tools-test-dataviewpanel',
		        	border: 0,
		        	autoScroll: true,
		        	anchor: '100%, 30%',
		        	id: 'PlotFrameSouth' + timestamp,
		        	items: [{
	                	xtype: 'dataview',
	                	id: 'toolsKHeatmapDataView' + timestamp,
	                	store: dataViewStore,
	                	tpl: [
			                '<tpl for=".">',
			                    '<div class="thumb-wrap" id="{name:stripTags}">',
			                        '<div class="thumb"><img src="{url}" title="{name:htmlEncode}" ></div>',
			                        '<span class="x-editable">{shortName:htmlEncode}</span>',
			                    '</div>',
			                '</tpl>',
			                '<br\>',
			                '<br\>',
			                '<div class="x-clear"></div>'
			            ],
			            multiSelect: true,
			            height: 310,
			            itemSelector: 'div.thumb-wrap',
			            trackOver: true,
			            emptyText: 'No images to display',
			            overItemCls: 'x-item-over',
			            plugins: [
			                Ext.create('Ext.ux.DataView.DragSelector', {})
			                // Ext.create('Ext.ux.DataView.LabelEditor', {dataIndex: 'name'})
			            ],
			            prepareData: function(data) {
			                Ext.apply(data, {
			                    shortName: Ext.util.Format.ellipsis(data.name, 15),
			                    sizeString: Ext.util.Format.fileSize(data.size)
			                    // dateString: Ext.util.Format.date(data.lastmod, "m/d/Y g:i a")
			                });
			                return data;
			            },
			            listeners: {
			                itemclick: function(me, record, item ){
			                	showSymbolList(record.data.name,record.data.url)
			                }
			            }
	                }]
		        }]
	    }
	    ];
	    this.callParent(arguments);
    }
});