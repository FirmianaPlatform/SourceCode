Ext.define("gar.view.tools.eastpanel.Distribution", {
    extend: 'Ext.panel.Panel',
    height: 600,
    width: 300,
    layout: 'anchor',
    //id: 'eastpanelGoEnrich',
    closable: false,
    alias: 'widget.eastDistribution',
    title: 'Distribution',
    
    initComponent: function() {
        //var val = this.val
		var goGrid = Ext.create('Ext.grid.Panel', {		
			//title: 'File List Grid',
			//store : fileListStore,
			anchor: '100% 100%',
			forceFit:true,
			viewConfig : {
				//trackOver: false,
				stripeRows : true,
				enableTextSelection : true
			},
			defaults:{
				width:200
			},
			columns : [
				{//locked:true,
					//text : "No.",
					xtype : 'rownumberer',
					width : 45
				},{
					text : 'Symbol',
					dataIndex : 'name',
					renderer : function(value, metaData, record, rowIndex, colIndex, store) {
						metaData.tdAttr = "title='" + value + "'";
						return value 
					}	
				}]
		
		});
        this.items = [goGrid]
    	this.callParent(arguments);
    }
})