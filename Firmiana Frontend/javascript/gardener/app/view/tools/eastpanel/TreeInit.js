Ext.define("gar.view.tools.eastpanel.TreeInit", {
    extend: 'Ext.panel.Panel',
    height: 600,
    layout: 'border',
    id: 'treeinitpanel',
    closable: false,
    alias: 'widget.treeinit',
    title: 'Experiment List',
    

    /**
     * @method initComponent
     * @inheritdoc
     * @return {void}
     */
    initComponent: function() {

        var val = this.val;

        var tree_store = Ext.create('gar.store.CompareTree');
        tree_store.getProxy().extraParams = {
            val : val
        }
        var expListDict = [[],[]]
        tree_store.load({
            scope: this,
            callback: function() {
                var i = 0
                tree_store.getRootNode().eachChild(function(node){
                    expListDict[0][i] = node
                    expListDict[1][i] = 0
                    i++
                })
            }
        })

/*----  Dustbin Store initialized ----*/

        //Dustbin <em>Drag experiments and drop them here.</em>
        storeDustbin = Ext.create('Ext.data.TreeStore');
        storeDustbin.setRootNode('');
        var rootDustbin = storeDustbin.getRootNode();

/*----  Dustbin Store initialized finished----*/

        var findString = function() {
            var v, matches = 0
            var root = Ext.getCmp('tree_init').getRootNode()
            var tempChildren = root.childNodes

            for(var i = 0; i < tempChildren.length; i++)
            {
                for(var j = 0; j < expListDict[0].length; j++)
                {
                    if(tempChildren[i].data.text == expListDict[0][j].data.text)
                    {
                        expListDict[1][j] = 0
                        break
                    }
                }
            }
            root.removeAll()
            var tmpString = Ext.getCmp('treeInitSearch').getValue()
            tmpString=tmpString.replace('(','\\(')
            tmpString=tmpString.replace(')','\\)')
            v = new RegExp(tmpString, 'i')
            for(var i = 0; i < expListDict[0].length; i++)
            {
                if((v.test(expListDict[0][i].data.text) == true)&&(expListDict[1][i]==0))
                {
                    matches++
                    root.appendChild(expListDict[0][i])
                    expListDict[1][i] = 1
                }
            }
            Ext.getCmp('treeInitSearchMatches').setValue(matches)
        }

        this.items = [{
            region: 'center',
            xtype: 'treepanel',
            id: 'tree_init',
            layout: 'fit',
            height: 600,
            lines: false,
            hideHeaders: true,
            useArrows: true,
            rootVisible: false,
            store: tree_store,
            selModel: {
                mode: 'MULTI'
            },
            columns : [{
                xtype : 'treecolumn',
                text: 'Experiment Name',
                dataIndex : 'text',
                flex : 1,
                editor : {
                    xtype : 'textfield',
                    allowBlank : false,
                    allowOnlyWhitespace : false
                }
            }],
            // plugins: [{
            //     ptype: 'bufferedrenderer'
            // }],
            viewConfig : {
                plugins : {
                    ptype : 'treeviewdragdrop',
                    containerScroll : true
                }
            },
            dockedItems: [{
                xtype: 'toolbar',
                dock: 'top',
                items: [{
                    xtype: 'trigger',
                    fieldLabel: 'Search:',
                    triggerCls : Ext.baseCSSPrefix + 'form-search-trigger',
                    labelWidth: 50,
                    width : 150,
                    id: 'treeInitSearch',
                    allowBlank : true,
                    style : 'margin-left: 5px',
                    onTriggerClick : findString,
                    listeners : {
                        specialkey : function(field, event) {
                           if (event.getKey() == event.ENTER) {
                           // Ext.MessageBox.confirm('hahaha');
                              findString()
                           }
                        }
                    }
                },'->',{
                    xtype: 'displayfield',
                    fieldLabel: 'Matches',
                    id: 'treeInitSearchMatches',
                    labelWidth: null,
                    listeners: {
                        beforerender: function() {
                            var me = this
                            Ext.getCmp('tree_init').store.on('fillcomplete', function(store, node){
                                me.setValue(node.childNodes.length)
                            })
                        }
                    }
                }]
            }]
        },{
            region: 'south',
            xtype: 'treepanel',
            title: 'Dustbin',
            id: 'dustbinPanel',
            store: storeDustbin,
            root: {
                expanded: true,
                text: '<em>Drag <b>EXPERIMENT</b> and drop it here.</em>'
            },
            layout: 'fit',
            hideHeaders: true,
            height: 200,
            lines: false,
            useArrows: true,
            collapsible: true,
            collapsed: true,
            hidden: true,
            floatable: false,
            selModel: {
                mode: 'MULTI'
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
            viewConfig : {
                plugins : {
                    ptype : 'treeviewdragdrop',
                    containerScroll : true
                }
            }
        }
        ]

        this.callParent(arguments);
    },
})