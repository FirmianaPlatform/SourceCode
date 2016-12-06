Ext.define("gar.view.tools.eastpanel.GoClassification", {
    extend: 'Ext.panel.Panel',
    height: 600,
    width: 300,
    layout: 'anchor',
    //id: 'eastpanelGoClassification',
    closable: false,
    alias: 'widget.eastGOClassification',
    title: 'GO Classification',
    

    /**
     * @method initComponent
     * @inheritdoc
     * @return {void}
    */
    requires: [ 'Ext.selection.CellModel' ],
    initComponent: function() {
        var val = this.val
        var cellEditing = new Ext.grid.plugin.CellEditing({
            clicksToEdit: 1
        });
		var goGrid = Ext.create('Ext.grid.Panel', {
			//title: 'File List Grid',
			//store : fileListStore,
			plugins: [cellEditing],
			anchor: '100% 100%',
			//forceFit:true,
			viewConfig : {
			//trackOver: false,
				stripeRows : true,
				enableTextSelection : true
			},
			defaults : {
				width : 100
			},
			columns : [
						{
							text : 'ID',
							dataIndex : 'ID',
							renderer : function(value, metaData, record, rowIndex, colIndex, store) {
								metaData.tdAttr = "title='" + value + "'";
								return value 
							}	
						},{
							text : 'Description',
							dataIndex : 'Description',
							width : 150,
							renderer : function(value, metaData, record, rowIndex, colIndex, store) {
								metaData.tdAttr = "title='" + value + "'";
								return value 
							}		
						},{
							text : 'GeneRatio',
							dataIndex : 'GeneRatio',
							renderer : function(value, metaData, record, rowIndex, colIndex, store) {
								metaData.tdAttr = "title='" + value + "'";
								return value 
							}	
						},{
							text : 'geneID',
							dataIndex : 'geneID',
							width : 175,
			                //flex: 1,
			                editor: {
			                    allowBlank: true
			                }
//							renderer : function(val) {
//								//console.log("<input id='experiment_selector_" + val + "' type='checkbox' value=" + val + "/>")
//								return "<div style=\"height:13px;\"><input type='text' value=" + val + "/><div>";
//								
//							}
						},{
							text : 'Count',
							dataIndex : 'Count',
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