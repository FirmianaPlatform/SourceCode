Ext.define('gar.view.CompareTree', {
			extend : 'Ext.tree.Panel',
			xtype : 'tree-reorder',
			useArrows : true,
			rootVisible : false,
			initComponent : function() {
				nodei = 1;
				Ext.apply(this, {
							// store : new Ext.data.TreeStore({}),
							viewConfig : {
								plugins : {
									ptype : 'treeviewdragdrop',
									containerScroll : true
								}
							},
							plugins : {
								ptype : 'cellediting',
								clicksToEdit : 1,
								listeners : {
									edit : function(editor, e) {
										// commit the changes right after editing finished
										e.record.commit();
									}
								}
							},
							columns : [{
										xtype : 'treecolumn',
										dataIndex : 'text',
										flex : 1,
										editor : {
											xtype : 'textfield',
											allowBlank : false,
											allowOnlyWhitespace : false
										}
									}],
							tbar : [{
										text : 'New Group',
										scope : this,
										handler : this.onNewGroupClick
									}, {
										text : 'New Condition',
										scope : this,
										handler : this.onNewConditionClick
									}, {
										text : 'Dustbin',
										scope : this,
										handler : this.onDustBinClick
									}, {
										text : 'Group Done',
										scope : this,
										handler : this.onGroupDone
									}]
						});
				this.callParent();
			},
			onNewGroupClick : function() {
				nodei = nodei + 1
				// var me = this
				var treeNode = this.getRootNode();
				treeNode.appendChild({
							text : 'Group' + nodei,
							leaf : false
						});
				//console.log(treeNode)
				treeNode.childNodes[treeNode.childNodes.length - 1].appendChild({
							text : 'Condition' + 1,
							leaf : false
						});
				//console.log(treeNode)
			},
			onNewConditionClick : function() {
				// var me = this
				var treeNode = this.getRootNode();
				treeNode.appendChild({
							text : 'Condition1',
							leaf : false
						});
			},
			onDustBinClick : function() {
				// var me = this
				var treeNode = this.getRootNode();
				treeNode.appendChild({
							text : 'Dustbin',
							leaf : false
						});
			},
			onGroupDone : function() {
			}
		})