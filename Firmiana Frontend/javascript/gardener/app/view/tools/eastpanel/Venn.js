Ext.define("gar.view.tools.eastpanel.Venn", {
    extend: 'Ext.panel.Panel',
    height: 600,
    width: 300,
    layout: 'anchor',
    //id: 'eastpanelGoClassification',
    closable: false,
    alias: 'widget.eastVenn',
    title: 'Interaction List',
    
    initComponent: function() {
    	var val = String(rec.get('csv_name'));
        var me = this;
		var filters = {
			ftype : 'filters',
			//encode : true,
			local: true
		}
		var goGrid = Ext.create('Ext.grid.Panel', {		
			//title: 'File List Grid',
			//store : fileListStore,
			anchor: '100% 100%',
			forceFit: true,
			dockedItems: [{
				xtype: 'toolbar',
				dock: 'top',
				border: 0,
				items: [{
					text: 'Further Analysis',
					menu: [{
						text: 'GO Classification',
						handler: function(record) {
							if(goGrid.store.data.length==0) {alert('No data');return;}
							var toolTitle = record.text 
							var temp_panel = Ext.widget(toolTitle.replace(" ", ""), {val: val, objEastPanel:eastpanel, goGridStore: goGrid.store} ); 
			    			mainpanel.add(temp_panel).show();
			    			mainpanel.setActiveTab(temp_panel);
			    			Ext.example.msg('Success','Data has been sent to ' + toolTitle + ' for further analysis.')
						}
					},{
						text: 'GO Enrich',
						handler: function(record) {
							if(goGrid.store.data.length==0) {alert('No data');return;}
							var toolTitle = record.text 
							var temp_panel = Ext.widget(toolTitle.replace(" ", ""), {val: val, objEastPanel:eastpanel, goGridStore: goGrid.store} ); 
			    			mainpanel.add(temp_panel).show();
			    			mainpanel.setActiveTab(temp_panel);
			    			Ext.example.msg('Success','Data has been sent to ' + toolTitle + ' for further analysis.')
						}
					},{
						text: 'KEGG',
						handler: function(record) {
							if(goGrid.store.data.length==0) {alert('No data');return;}
							var toolTitle = record.text 
							var temp_panel = Ext.widget(toolTitle.replace(" ", ""), {val: val, objEastPanel:eastpanel, goGridStore: goGrid.store} ); 
			    			mainpanel.add(temp_panel).show();
			    			mainpanel.setActiveTab(temp_panel);
			    			Ext.example.msg('Success','Data has been sent to ' + toolTitle + ' for further analysis.')
						}
					},{
						text: 'TF-TG',
						handler: function(record) {
							if(goGrid.store.data.length==0) {alert('No data');return;}
							var toolTitle = record.text 
							var temp_panel = Ext.widget(toolTitle.replace(" ", ""), {val: val, objEastPanel:eastpanel, goGridStore: goGrid.store} ); 
			    			mainpanel.add(temp_panel).show();
			    			mainpanel.setActiveTab(temp_panel);
			    			Ext.example.msg('Success','Data has been sent to ' + toolTitle + ' for further analysis.')
						}
					},{
						text: 'Kinase/Substrate',
						handler: function(record) {
							if(goGrid.store.data.length==0) {alert('No data');return;}
							var toolTitle = record.text 
							var temp_panel = Ext.widget(toolTitle.replace(" ", ""), {val: val, objEastPanel:eastpanel, goGridStore: goGrid.store} ); 
			    			mainpanel.add(temp_panel).show();
			    			mainpanel.setActiveTab(temp_panel);
			    			Ext.example.msg('Success','Data has been sent to ' + toolTitle + ' for further analysis.')
						}
					}]
				},'->',{
					text: 'Export',
					handler: function() {
						if(goGrid.store.data.length==0) {alert('No data');return;}
						
						var goTxt = ""
						goGrid.store.data.items.forEach(function(item){
							goTxt += item.raw.name
							if(item.index != goGrid.store.data.items.length - 1)
								goTxt += '\n'
						})
						var win = Ext.create('Ext.Window', {
							width : 200,
							// height
							// :
							// 735,
							height : 400,
							minHeight : 100,
							minWidth : 50,
							//hidden : true,
							maximizable : true,
							title : 'Data clipboard',
							items:[{xtype:"textarea",value:goTxt}],
							layout : 'fit'
						});
						
						win.show();
					}			
				}]
			}],
			viewConfig : {
				//trackOver: false,
				stripeRows : true,
				enableTextSelection : true
			},
			defaults:{
				width:100
			},
			features : [filters],
			columns : [
//				{//locked:true,
//					//text : "No.",
//					xtype : 'rownumberer',
//					width : 45
//				},
				{
					text : 'No.',
					dataIndex : 'no',
					width : 45,
					filter : {
						type : 'int'
					}
				},{
					text : 'Symbol',
					dataIndex : 'name',
					filter : {
						type : 'string'
					},
					renderer : function(value, metaData, record, rowIndex, colIndex, store) {
						metaData.tdAttr = "title='" + value + "'";
						return value 
					}	
				},{
					text : 'Region',
					//hidden:true,
					dataIndex : 'region',
					width : 85,
					filter : {
						type : 'string'
					},
					renderer : function(value, metaData, record, rowIndex, colIndex, store) {
						metaData.tdAttr = "title='" + value + "'";
						return value 
					}	
				}]
		
		});

		//toolbar.items.items[0].disable()
        this.items = [goGrid]
    	this.callParent(arguments);
    }
})