Ext.define('gar.view.State', {
			extend : 'Ext.Toolbar',
			initComponent : function() {
				Ext.regModel('Search_box', {
							fields : [{
										type : 'string',
										name : 'name'
									}, {
										type : 'string',
										name : 'value'
									}]
						});
				var themeName =
					[
						{"name" : "classic", "value" : "classic"}, 
						{"name" : "neptune", "value" : "neptune"}, 
						{"name" : "access",  "value" : "access"}, 
						{"name" : "gray",    "value" : "gray"}
					]
//				var store_theme = Ext.create('Ext.data.Store', {
//		    		fields: ['name'],
//		    		data : [
//		        		{"name" : "classic"},
//		        		{"name" : "neptune"},
//		        		{"name" : "access"},
//						{"name" : "gray"}
//		    		]
//				});
				var store_theme =Ext.create('Ext.data.Store', {model : 'Search_box',data : themeName})
				var uname = Ext.util.Cookies.get("username");
	  	  		//var info_message = 'Firmiana Experiment Viewer -- Today is '+ Ext.Date.format(new Date(),'n/d/Y(D) h:i:s');
	  	  		

  					
				Ext.apply(this, {
							id : "info",
							// frame:true,
							region : "south",
							height : 35,
							items : [
										{
											xtype : 'tbtext',
											id : 'info_message'
											//text : info_message
										},'->',	
										{
											xtype : 'tbtext',
											id:'login_as',
											text : 'Logged in as '+ '<font color=purple>'+uname +'</font>' + ' @' + Ext.Date.format(new Date(),'Y/n/d(D) H:i:s')
										},	
									  '->',
//									{
//										id : 'theme',
//                						xtype: 'combo',
//                						store: store_theme,
//                						width: 80,
//                						displayField : 'name',
//                						editable:false,
//                						//typeAhead: true,
//                						value:'classic',
//                						queryMode : 'local',
//                						//selectOnFocus: true,
//                						
//                						listeners: 
//                							{select: function(combo, record, index)
//                								{
//                									Ext.util.CSS.swapStyleSheet('window', '/static/ext4/resources/ext-theme-'+combo.getValue()+'/ext-theme-'+combo.getValue()+'-all.css');
//                    								//Ext.Msg.alert('Theme','Change theme to \"'+combo.getValue()+'\"');
//                								}
//                							}
//                						
//            						},
									'-',{
										text : 'User Management',
										iconCls : "usermanage",
										id : 'usermanage',
										// menuAlign : 'tl-bl',
										menu : {
											xtype : 'menu',
											items : ['-',
												{
													text : 'Lock Screen',
													iconCls : "imlogin",
													id : 'btlogin'
												},'-',{
													text : 'Change Password',
													iconCls : "changepw",
													id : 'changepw'
												},'-',{
													text : 'Logout(Homepage)',
													iconCls : "imlogoff",
													id : 'btlogoff'
												},'-']
										}
									},
//									'-',{
//										xtype : 'button',
//										text : '',
//										iconCls : "btcube",
//										id : 'btcube'
//									},
									'-',{
										xtype : 'button',
										text : 'Job Status',
										iconCls : "btmessage",
										id : 'btmessage'
									},'-',{
										xtype : 'button',
										iconCls : "btstate",
										id : 'btstate',
										tooltip : 'Connection Well.'
									},
									// {
									// 	xtype : 'button',
									// 	text : 'Reset tool window',
									// 	tooltip : 'Click when Tool Window\'s position is out of control',
									// 	handler:function(){
									// 		Ext.getCmp('toolsPanel').alignTo(Ext.getCmp('newcompare'),(0,0));
									// 	}
									// },
									{
										xtype : 'hiddenfield',
										id : 'info_experiments_selected'
									}, {
										xtype : 'hiddenfield',
										id : 'info_searches_selected',
										value : '0'
									}, {
										xtype : 'hiddenfield',
										id : 'info_protein_tab_index',
										value : 0
									}, {
										xtype : 'hiddenfield',
										id : 'info_peptide_tab_index',
										value : 0
									}, {
										xtype : 'hiddenfield',
										id : 'info_compare_tab_index',
										value : 0
									},{
										xtype : 'hiddenfield',
										id : 'info_tab_index',
										value : 0
									},{
										xtype : 'hiddenfield',
										id : 'info_compare_tool_index',
										value : ''
									}]
						});
				this.callParent(arguments);
			}
		})
