Ext.define('gar.view.ControlMenu', {
			extend : 'Ext.window.Window',
			//alias : 'widget.globalplot',
			title : 'Analysis Panel',
			layout : 'border',
			defaults : {
				collapsible : true,
				split : true,
				bodyPadding : 15
			},
			width : 670,
			height : 660,
			minimizable : true,
			autoShow : true,
			listeners : {
				"minimize" : function(window, opts) {
					window.collapse();
					window.setWidth(150);
					window.alignTo(Ext.getBody(), 'bl-bl')
				}
			},
			tools : [{
						type : 'restore',
						handler : function(evt, toolEl, owner, tool) {
							var window = owner.up('window');
							window.setWidth(700);
							window.expand('', false);
							window.center();
						}
					}],
			initComponent : function() {
				var controlPanel = Ext.create('Ext.tab.Panel', {
							xtype: 'plain-tabs',
							region : 'center', // a center region is ALWAYS required for border layout
							// deferredRender: false,
							activeTab : 0, // first tab initially active
							items : []
						})
				this.items = [controlPanel, {
							title : 'title',
							region : 'west',
							collapsible : true,
							width : 200,
							margins : '0 0 0 5',
							layout : {
								type : 'accordion'
							},
							items : [{
										// contentEl: 'west',
										title : 'Navigation',
										items : [{
													xtype : 'button',
													text : 'Distribution',
													handler : this.boxplot
												}, {
													xtype : 'button',
													text : 'PCA',
													handler : this.PCA
												}, {
													xtype : 'button',
													text : 'Stack',
													handler : this.stack
												}, {
													xtype : 'button',
													text : 'Correlation',
													handler : this.correlation
												}]
									}, {
										title : 'Plot',
										items : [{
													xtype : 'button',
													text : 'heatmap',
													handler : this.heatmap
												}, {
													xtype : 'button',
													text : 'k-heatmap',
													handler : this.k_heatmap
												}, {
													xtype : 'button',
													text : 'Volcano',
													handler : this.volcano
												},{
													xtype : 'button',
													text : 'Venn',
													handler : this.venn
												},]
									}, {
										title : 'Information'
									}]
						}];
				this.callParent(arguments);
			},
			boxplot : function() {
			},
			correlation : function() {
			},
			PCA : function() {
			},
			stack : function() {
			},
			heatmap : function() {
			},
			volcano : function() {
			},
			venn : function() {
			},
			k_heatmap:function(){
				
			}
		});
