Ext.define('gar.view.tools.centerpanel.itemSelector',{
    extend: 'Ext.window.Window',
	requires: [
    	'Ext.ux.form.ItemSelector',
    	'Ext.ux.form.MultiSelect',
    	'Ext.tip.QuickTipManager',
	    'Ext.ux.ajax.JsonSimlet',
	    'Ext.ux.ajax.SimManager'
    ],
    alias: 'widget.itemSelector',
    maximizable: false,
    minimizable: false,
    width:800,
    autoShow: true,
    closable: true,
    modal: true,
    closeAction: 'destroy',
    title: 'Experiment Selector',

	/**
	 * @method initComponent
	 * @inheritdoc
	 * @return {void}
	 */
	initComponent: function() {

		var val = this.val
		var out = this.out
		var temp_filter = this.temp_filter
		var type = this.Rtype
		var minValue = this.minValue
		var maxValue = this.maxValue
		var timestamp = this.timestamp
		var plotlevel = Ext.getCmp('plotlevel'+timestamp).getRawValue()
    	var	knumber = Ext.getCmp('plotKheatmapKNumber'+timestamp).getRawValue()
		var statis = this.statis
		var	temp_name = this.temp_name
		var	gridType = this.gridType
		var	zscore = this.zscore
		var	cutoff = this.cutoff
		var	log = this.log
		var currentWindow = this
		var kmeanList = {}

		var mainImg = Ext.getCmp('toolsKHeatmapMainImg' + timestamp)
		var dataViewStore = Ext.getCmp('toolsKHeatmapDataView' + timestamp).getStore()

		Ext.Loader.setConfig({enabled: true});
		Ext.Loader.setPath('Ext.ux', '../ux');


		var showSymbolList = function(kmeanID){
    		var fileListStore = Ext.create('Ext.data.Store', {
					data:kmeanList[kmeanID],
					fields : [{
								name : 'name',
								type : 'string'
							}],
					autoLoad : true
			});
			//fileListStore.sort('Description','DESC');
			east_temp_panel.down('grid').reconfigure(fileListStore)
			//east_temp_panel.down('grid').enable();
        };

		//different condition for different plot level
        var MenuChange = function(level) {
        	if(level == 'Experiment')
	        {
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
	        					dataStore.add({'text':tempText, 'value':tempValue})
	        				}
	        		}
	        	}
	        }
	        else if(level == 'Condition')
	        {
	        	for(var i = 1; i < columndata.length; i++)
	        	{
	        		if(columndata[i].dataIndex.indexOf('repeat') != -1)
	        		{
	        			var groupText = columndata[i].text

				        for(var j = 0; j < columndata[i].columns.length; j++)
				        {
				        	var tempText  = groupText + ' - ' + columndata[i].columns[j].text
				        	var tempValue = columndata[i].columns[j].dataIndex
				        	dataStore.add({'text':tempText, 'value':tempValue})
				        }
	        		}
	        	}
	        }
	        else if (level == 'Group')
	        {
	        	for(var i = 1; i < columndata.length; i++)
	        	{
	        		if(columndata[i].dataIndex.indexOf('repeat') != -1)
	        		{
	        			var tempText = columndata[i].text
	        			var tempValue = columndata[i].dataIndex
	        			dataStore.add({'text':tempText, 'value':tempValue})
	        		}
	        	}
	        }
        }

		var dataStore = Ext.create('Ext.data.ArrayStore', {
	        fields: ['text','value'],
	        // autoLoad: true,
	    });

	    MenuChange(plotlevel)

		this.items = [{
			xtype: 'form',
			layout: 'fit',
			height: 300,
			bodyPadding: 5,
			border: 0,
			items: [{
				xtype: 'itemselector',
	            // name: 'itemselector',
	            id: 'itemselector-field',
	            // fieldLabel: 'ItemSelector',
	            // imagePath: '../ux/css/images/',
	            store: dataStore,
	            displayField: 'text',
	            valueField: 'value',
	            allowBlank: false,
	            msgTarget: 'side',
	            fromTitle: 'Experiments available',
	            toTitle: 'Experiments selected'
			}]
		},
		{
			xtype: 'toolbar',
			ui: 'footer',
			items: ['->', 
			// {
			// 	text: 'clear',
			// 	handler: function() {
			// 		Ext.Msg.alert('clear')
			// 	}
			// },
			{
                text: 'Go',
                handler: function(){
                    var expList = Ext.getCmp('itemselector-field').getValue()

					if(expList.length<2){
						Ext.Msg.alert('Warning','Need two or more ' + plotlevel + 's.');
						return
					}
					// var loading = '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>';
     //                Ext.getCmp('PlotFrame'+timestamp).update(loading);

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
							expList: expList,
							temp_name:temp_name,
							gridType:gridType,
							normalizationLevel: normalizationLevel,
							zscore: zscore,
							cutoff: cutoff,
							log: log 
						},
						success : function(response) {
							// console.log(response.responseText);
							jsonObject = Ext.JSON.decode(response.responseText)


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

							//push kmeanlist to sessionstorage
							var kmeanListText = Ext.JSON.encode(kmeanList)
							sessionStorage.setItem('kmeanListText', kmeanListText)

							//pop success msg
							Ext.example.msg('Suceess','Plotting done.')
						},
						failure : function() {
							Ext.getCmp('PlotFrame'+timestamp).update("Sorry! Error happen, please contact Admin with current URL.");
						}
					});
					currentWindow.destroy()
                }
            }]
		}]
		this.callParent(arguments);
	}
});