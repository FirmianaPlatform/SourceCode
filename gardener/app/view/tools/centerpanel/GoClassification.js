Ext.define('gar.view.tools.centerpanel.GoClassification',{
    extend: 'Ext.panel.Panel',
    alias: 'widget.GOClassification',
    width: 600,
    split: true,
    floatable: false,
    closable: true,
    title: 'GO Classification',
	layout:'border',
    initComponent: function() {
		var east_temp_panel = Ext.widget( 'east' + this.title.replace(" ","") );
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
		
		var loadMask = new Ext.LoadMask(east_temp_panel.down('grid'), {  
            msg:'Loading...',    
            disabled:false
        });  
    	var tmpHtml,dataJson,totalNum,tmpPng,tmpPdf
    	var timestamp = (new Date()).valueOf()
    	var goClassificationLevel = 2
    	var ontology = 'BP'
    	var organism = 'mouse'
    	var compare_grid = Ext.getCmp(info_compare_tool_index);
		var	temp_filter = compare_grid.filters.buildQuery(compare_grid.filters.getFilterData());
    	var temp_name = this.temp_name
    	var gridType = this.gridType
		var plotOrganism = Ext.create('Ext.data.Store', {
		    fields: ['name'],
		    data : [
		        {"name": 'mouse'},
		        {"name": 'human'}
		    ]
		});
    	var plotOntology = Ext.create('Ext.data.Store', {
		    fields: ['name'],
		    data : [
		        {"name": 'BP'},
		        {"name": 'CC'},
		        {"name": 'MF'}
		    ]
		});

		var plot = function(btn) {
			if(btn!='yes'){return}
			var centerWin = Ext.getCmp('PlotFrame'+timestamp)
			var loading1 = '<div align="center"><img src="/static/images/loading/loading5.gif"/></div>';
			//var loading2 = '<div align="center" style="padding-top:50px"><img src="/static/images/loading/loading13.gif" /></div>';
    		var val = String(rec.get('csv_name'));
    		//Ext.getCmp('PlotFrame'+timestamp).removeAll();
    		centerWin.update(loading1);
    		////east_temp_panel.removeAll();
    		//east_temp_panel.update(loading2);

			temp_filter = compare_grid.filters.buildQuery(compare_grid.filters.getFilterData());
			east_temp_panel.down('grid').disable();
			if(goGridStore)
			{
				goTxt = ''
				goGridStore.data.items.forEach(function(item){
					goTxt += item.raw.name
					if(item.index != goGridStore.data.items.length - 1)
						goTxt += ';'
				})
			}
			//loadMask.show();
    		Ext.Ajax.request({
				timeout : 600000,
				url : '/gardener/newcmpprotein/',
				method : 'POST',
				params : {
					id : val,
					filter : temp_filter,
					R_type : 'GOClassification',
					organism : organism,
					ontology: ontology,
					goClassificationLevel: goClassificationLevel,
					goTxt: goTxt,
					temp_name:temp_name,
					gridType:gridType,
					normalizationLevel: normalizationLevel
				},
				success : function(response) {
					var tmpResponse = Ext.JSON.decode(response.responseText);
					tmpHtml = tmpResponse.tmpHtml
					console.log( tmpHtml )
					dataJson = tmpResponse.data 
					totalNum = tmpResponse.total 
					tmpPng = tmpResponse.png 
					tmpPdf = tmpResponse.pdf 
					//Ext.getCmp('PlotFrame'+timestamp).update(tmpHtml);
					
					var fileListStore = Ext.create('Ext.data.Store', {
						data:dataJson,
						fields : [{
									name : 'ID',
									type : 'string'
								},{
									name : 'Description',
									type : 'string'
								},{
									name : 'GeneRatio',
									type : 'string'
								},{
									name : 'geneID',
									type : 'string'
								},{
									name : 'Count',
									type : 'int'
								}],
								listeners : {},
						autoLoad : true
					});
					fileListStore.sort('Description','DESC');
					east_temp_panel.down('grid').reconfigure(fileListStore)
					east_temp_panel.down('grid').enable();
					centerWin.update(tmpHtml);
					//east_temp_panel.update('');
					//east_temp_panel.add(goGrid)
					//loadMask.hide();

					//pop success msg
					Ext.example.msg('Suceess','Plotting done.')
				},
				failure : function() {
    				//east_temp_panel.removeAll();
					east_temp_panel.down('grid').enable();
    				//loadMask.hide();
					centerWin.update("Sorry! Error happen, please contact Admin with current URL.");
				}
			});
		}

    	this.items = [{
	        xtype: 'toolbar',
	        border: 0,
	        region:'north',
	        items: [
	        	{
	        	xtype: 'combo',
	            fieldLabel: 'Species',
	            value: 'mouse',
	            editable: false,
	            width: 150,
	            labelWidth: 65,
	            store: plotOrganism,
	            displayField: 'name',
	            listeners: {
	            	change: function(item, newvalue) {
	            		organism = newvalue
	            	}
	            }
	        },{
	        	xtype: 'combo',
	            fieldLabel: 'Ontology',
	            value: 'BP',
	            editable: false,
	            width: 125,
	            labelWidth: 65,
	            store: plotOntology,
	            displayField: 'name',
	            listeners: {
	            	change: function(item, newvalue) {
	            		ontology = newvalue
	            	}
	            }
	        },{
	        	xtype: 'numberfield',
	            fieldLabel: 'Level',
	            name: 'level',
	            width: 110,
	            labelWidth: 50,
	            value: 2,
	            minValue: 1,
	            maxValue: 10,
	            listeners: {
	            	change: function(item, newvalue) {
	            		goClassificationLevel = newvalue
	            	}
	            }
	        },{
	        	xtype: 'button',
	        	text: 'Start',
	        	handler: function() {
	        		Ext.MessageBox.confirm('Confirm', Ext.String.format("Use [ organism = {0} ] [ ontology = {1} ] [ level = {2} ] ?",organism,ontology,goClassificationLevel), plot); 
	        	}
	        }
//	        ,'->',{
//	        	xtype: 'button',
//	        	text: 'Download'
//	        },
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
	        xtype: 'panel',
    		autoScroll: true,
	        border: 0,
	        id: 'PlotFrame'+timestamp,
	        region: 'center',
	        //height: 500,
	        items:[],
	        html: ''
	    }];
	    this.callParent(arguments);
    }
});