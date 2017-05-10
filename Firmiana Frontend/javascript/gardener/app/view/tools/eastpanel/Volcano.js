Ext.define("gar.view.tools.eastpanel.Volcano", {
    extend: 'Ext.panel.Panel',
    height: 600,
    width: 300,
    layout: 'anchor',
    //id: 'eastpanelVolcano',
    closable: false,
    alias: 'widget.eastVolcano',
    title: 'Volcano Information',
    dataTxt:"None",

    /**
     * @method initComponent
     * @inheritdoc
     * @return {void}
     */
    initComponent: function() {
		var me = this;
        //var val = this.val
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
				items: ['->',{
					text: 'Export',
					handler: function() {
						//console(me.dataTxt)
						if(me.dataTxt!="None") window.open(me.dataTxt)
						//window.open(me.down('grid').store.url) 
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
				{//locked:true,
					//text : "No.",
					xtype : 'rownumberer',
					width : 45
				},
				{
					text : 'Symbol',
					dataIndex : 'symbol',
					width : 70,
					filter : {
						type : 'string'
					}
				},{
					text : 'log2(Ratio)',
					dataIndex : 'ratio',
					filter : {
						type : 'float'
					},
					renderer : function(value) {
						return value.toFixed(2);
					}
				},{
					text : '-log10(P-value)',
					//hidden:true,
					dataIndex : 'pvalue',
					width : 85,
					filter : {
						type : 'float'
					},
					renderer : function(value) {
						return value.toFixed(4);
					}
				}]
		
		});
		//toolbar.items.items[0].disable()
        this.items = [goGrid]
    	this.callParent(arguments);
    }
})