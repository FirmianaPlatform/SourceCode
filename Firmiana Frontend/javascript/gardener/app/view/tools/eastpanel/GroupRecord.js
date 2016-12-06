Ext.define("gar.view.tools.eastpanel.GroupRecord", {
    extend: 'Ext.panel.Panel',
    height: 600,
    layout: 'accordion',
    id: 'grouprecordpanel',
    closable: true,
    alias: 'widget.grouprecord',
    title: 'Group Record',
    

    /**
     * @method initComponent
     * @inheritdoc
     * @return {void}
     */
    initComponent: function() {

        var recordGroupTree = this.recordGroupTree

        var storeGroupRecord = Ext.create('Ext.data.TreeStore');
        var tmpRootNode = recordGroupTree.data.tree.getRootNode().copy(undefined, true);
        storeGroupRecord.setRootNode(tmpRootNode);

        var storeGroupRecordInit = Ext.create('Ext.data.TreeStore');
        var tmpRootNodeInit = recordGroupTree.data.treeInit.getRootNode().copy(undefined, true);
        storeGroupRecordInit.setRootNode(tmpRootNodeInit);

        var storeGroupRecordDust = Ext.create('Ext.data.TreeStore');
        var tmpRootNodeDust = recordGroupTree.data.treeDust.getRootNode().copy(undefined, true);
        storeGroupRecordDust.setRootNode(tmpRootNodeDust);

        this.items = [{
            title: 'Group-done tree',
            xtype: 'treepanel',
            id: 'tree_record',
            layout: 'fit',
            collapsible: true,
            floatable: false,
            collapsed: false,
            rootVisible: false,
            store: storeGroupRecord,
            hideHeaders: true,
            columns : [{
                xtype : 'treecolumn',
                dataIndex : 'text',
                flex : 1,
                editor : {
                    xtype : 'textfield',
                    allowBlank : false,
                    allowOnlyWhitespace : false
                }
            }]
        },{
            title: 'Tree Initial',
            xtype: 'treepanel',
            id: 'treeRecordInit',
            layout: 'fit',
            collapsible: true,
            floatable: false,
            collapsed: true,
            rootVisible: false,
            store: storeGroupRecordInit,
            hideHeaders: true,
            columns : [{
                xtype : 'treecolumn',
                dataIndex : 'text',
                flex : 1,
                editor : {
                    xtype : 'textfield',
                    allowBlank : false,
                    allowOnlyWhitespace : false
                }
            }]
        },{
            title: 'Dustbin',
            xtype: 'treepanel',
            id: 'treeRecordDust',
            layout: 'fit',
            collapsible: true,
            floatable: false,
            collapsed: true,
            rootVisible: false,
            store: storeGroupRecordDust,
            hideHeaders: true,
            columns : [{
                xtype : 'treecolumn',
                dataIndex : 'text',
                flex : 1,
                editor : {
                    xtype : 'textfield',
                    allowBlank : false,
                    allowOnlyWhitespace : false
                }
            }]
        }]

    	this.callParent(arguments);
    },
})