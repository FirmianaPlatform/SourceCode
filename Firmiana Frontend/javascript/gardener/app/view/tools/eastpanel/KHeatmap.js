Ext.define("gar.view.tools.eastpanel.KHeatmap", {
    extend: 'Ext.panel.Panel',
//     height: 600,
    width: 300,
    layout: 'anchor',
    //id: 'eastpanelGoEnrich',
    closable: false,
    alias: 'widget.eastK-meansHeatmap',
    title: 'K-mean Heatmap',
    
    initComponent: function() {
        var val = String(rec.get('csv_name'));
        var me = this
		var filters = {
			ftype : 'filters',
			//encode : true,
			local: true
		}

		var img = Ext.create('Ext.Img',{
			anchor: '100% 50%',
			border: 1,
		})

		var goGrid = Ext.create('Ext.grid.Panel', {		
			//title: 'File List Grid',
			//store : fileListStore,
			anchor: '100% 50%',
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
				},'-',{
					text: 'Export',
					menu: [{
						text: 'Table',
						handler: function() {
							window.open(me.down('grid').store.url)
						}
					},{
						text: 'Diagram',
						handler: function() {
							window.open(me.down('image').src)
						}
					}]
				},'->',{
					xtype: 'displayfield',
                    fieldLabel: 'Matches',
                    labelWidth: null,
                    listeners: {
                        // beforerender: function() {
                        //     var me = this
                        //     Ext.getCmp('tree_init').store.on('fillcomplete', function(store, node){
                        //         me.setValue(node.childNodes.length)
                        //     })
                        // }
                    }
				}]
			}],
			viewConfig : {
				//trackOver: false,
				stripeRows : true,
				enableTextSelection : true
			},
			defaults:{
				width:200
			},
			features : [filters],
			columns : [
				{//locked:true,
					//text : "No.",
					xtype : 'rownumberer',
					width : 45
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
				}]
		});

        this.items = [goGrid,img]
    	this.callParent(arguments);
    }
})