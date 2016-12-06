Ext.define('gar.view.tools.centerpanel.Motif',{
    extend: 'Ext.panel.Panel',
    alias: 'widget.PTMMotif',
    width: 600,
    split: true,
    floatable: false,
    closable: true,
    title: 'PTM Motif',
    layout: 'border',

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
		var tmpHtml='',tmpPng='',tmpPdf=''
		var timestamp = (new Date()).valueOf();

		var searchDatabaseStore = Ext.create('Ext.data.Store', {
		    proxy : {
		        type : 'ajax',
		        url : '/experiments/ajax/display/Search_database/',
		        reader : {
		            type : 'json',
		            root : 'Search_databases'
		        }
		    },
		    fields : [{
		        name : 'Search_database',
		        type : 'string'
		    }],
		    autoLoad : true
		});

		var plot = function(type){
			var centerWin = Ext.getCmp('PlotFrame'+timestamp)
			var loading = '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>';
    		
    		var val = String(rec.get('csv_name'));
    		var compare_grid = Ext.getCmp(info_compare_tool_index);
			var temp_filter = compare_grid.filters.buildQuery(compare_grid.filters.getFilterData());
    		centerWin.update(loading);
    		console.log(Ext.getCmp('toolsMotif' + timestamp).getValue())
    		Ext.Ajax.request({
				timeout : 600000,
				url : '/gardener/newcmpprotein/',
				method : 'GET',
				params : {
					id : val,
					filter : temp_filter,
					R_type : type,
					normalizationLevel: normalizationLevel,
					dataBase: Ext.getCmp('toolsMotif' + timestamp).getValue()
				},
				success : function(response) {
					// console.log(response.responseText);
					var jsonObject = Ext.JSON.decode(response.responseText)
					tmpHtml = jsonObject.tmpHtml
					centerWin.update(tmpHtml);

					//pop success msg
					Ext.example.msg('Suceess','Plotting done.')
				},
				failure : function() {
					centerWin.update("Sorry! Error happen, please contact Admin with current URL.");
				}
			});
		}


    	this.items = [{
    		region: 'north',
	        xtype: 'toolbar',
	        border: 0,
	        items: [{
				xtype : 'combobox',
				id: 'toolsMotif' + timestamp,
				width : 250,
				labelWidth: 60,
				editable: false,
				fieldLabel : 'Database',
				value: '',
				name : 'Search_database',
				displayField : 'Search_database',
				valueField: 'Search_database',
				store : searchDatabaseStore
			},{
	        	xtype: 'button',
	        	text: 'GO',
	        	handler: function() {
	        		if(Ext.getCmp('toolsMotif' + timestamp).getValue() == '')
	        			Ext.getCmp('toolsMotif' + timestamp).setActiveError('')
	        		else
	        			plot('motif')
	        	}
	        },'->',
	        {
	        	xtype: 'button',
	        	text: 'Download'
	        },
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
	        //layout: 'fit',
	        autoScroll:true,
	        //height: 580,
	        html: tmpHtml
	    }
	    ];
	    this.callParent(arguments);
    }
});


