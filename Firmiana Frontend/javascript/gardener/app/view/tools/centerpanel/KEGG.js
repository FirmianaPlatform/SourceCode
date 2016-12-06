Ext.define('gar.view.tools.centerpanel.KEGG',{
    extend: 'Ext.panel.Panel',
    alias: 'widget.KEGG',
    width: 600,
    split: true,
    floatable: false,
    closable: true,
    title: 'KEGG',
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
	    	    
	    var goGridStore = this.goGridStore
	    var goTxt = 'None'
	    
	    this.on('activate', function() { 
			this.objEastPanel.setActiveTab(east_temp_panel)
		}) 		
		
	    this.on('close', function() { 
			east_temp_panel.close()
		}) 
    	var timestamp = (new Date()).valueOf()
    	var species = 'mouse'
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

			//loading pic
			var width = Ext.getCmp('PlotFrame' + timestamp).getWidth()
			var height = Ext.getCmp('PlotFrame' + timestamp).getHeight()
    		mainImg.setWidth(400)
    		mainImg.setHeight(300)
    		mainImg.setSrc('/static/images/loading/loading5.gif')

			var level = Ext.getCmp('plotlevel'+timestamp).getRawValue();
    		var val = String(rec.get('csv_name'));
    		get(columndata, level);
    		
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
					species: species,
					temp_name:temp_name,
					gridType:gridType,
					normalizationLevel: normalizationLevel,
					goTxt:goTxt
				},
				success : function(response) {

					//set main heatmap img
					mainImg.setSrc('')
					mainImg.setWidth(width*0.95)
    				mainImg.setHeight(height*0.95)
    				// mainImg.setHeight(height)
    				// mainImg.setLocalX(140)

					imgList = response.responseText
					imgList = imgList.split(';')
					for(var i = 0; i < imgList.length; i++)
						imgList[i] = imgList[i].split(':')

					dataViewStore.removeAll()
					imgList.forEach(function(item) {
							var keggname = item[0]
							dataViewStore.add({'name': keggname, 'url': item[1]})
						}
					)
					//pop success msg
					Ext.example.msg('Suceess','Plotting done.')
				},
				failure : function() {
					Ext.getCmp('PlotFrame'+timestamp).update("Sorry! Error happen, please contact Admin with current URL.");
				}
			});
		}

		//main img initialize
		var mainImg = Ext.create('Ext.Img',{
        	xtype: 'image',
        	id: 'toolsKeggMainImg' + timestamp
        })

        //dataview store
        var dataViewStore = Ext.create('Ext.data.Store', {
            fields: ['name', 'url']
        });

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
	            displayField: 'name'
	        },{
	        	text: 'Species',
	        	menu: [{
	        		text: 'human',
	        		checked: false,
	        		group: 'keggSpecies',
	        		handler: function() {
	        			species = 'human'
	        		}
	        	},{
	        		text: 'mouse',
	        		checked: true,
	        		group: 'keggSpecies',
	        		handler: function() {
	        			species = 'mouse'
	        		}
	        	},{
	        		text: 'xenopus',
	        		checked: true,
	        		group: 'keggSpecies',
	        		handler: function() {
	        			species = 'xenopus'
	        		}
	        	}]
	        },{
	        	xtype: 'button',
	        	text: 'GO',
	        	handler: function() {
	        		plot('kegg')
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
	                	id: 'toolsKeggDataView' + timestamp,
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
                                mainImg.setSrc(record.data.url)
                            }
                        }
	                }]
		        }]
	    }
	    ];
	    this.callParent(arguments);
    }
});