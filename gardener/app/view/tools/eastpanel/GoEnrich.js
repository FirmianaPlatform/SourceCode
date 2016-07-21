Ext.define("gar.view.tools.eastpanel.GoEnrich", {
    extend: 'Ext.panel.Panel',
    height: 600,
    width: 300,
    layout: 'anchor',
    //id: 'eastpanelGoEnrich',
    closable: false,
    alias: 'widget.eastGOEnrich',
    title: 'GO Enrich',
    

    /**

	 * @method initComponent
	 * @inheritdoc
	 * @return {void}
	 */
    requires: [ 'Ext.selection.CellModel' ],
    initComponent: function() {
        var cellEditing = new Ext.grid.plugin.CellEditing({
            clicksToEdit: 1
        });
        //var val = this.val
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
			defaults:{
				width:200
			},
			columns : [
			{
				text : 'ID',
				dataIndex : 'ID',
				width : 100,
				renderer : function(value, metaData, record, rowIndex, colIndex, store) {
					metaData.tdAttr = "title='" + value + "'";
					return value 
				}	
			},{
				text : 'Description',
				dataIndex : 'Description',
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
				text : 'BgRatio',
				dataIndex : 'BgRatio',
				renderer : function(value, metaData, record, rowIndex, colIndex, store) {
					metaData.tdAttr = "title='" + value + "'";
					return value 
				}	
			},{
				text : 'pvalue',
				dataIndex : 'pvalue',
				renderer : function(value, metaData, record, rowIndex, colIndex, store) {
					metaData.tdAttr = "title='" + value + "'";
					return value 
				}	
			},{
				text : 'p.adjust',
				dataIndex : 'p.adjust',
				renderer : function(value, metaData, record, rowIndex, colIndex, store) {
					metaData.tdAttr = "title='" + value + "'";
					return value 
				}	
			},{
				text : 'qvalue',
				dataIndex : 'qvalue',
				renderer : function(value, metaData, record, rowIndex, colIndex, store) {
					metaData.tdAttr = "title='" + value + "'";
					return value 
				}	
			},{
				text : 'geneID',
				dataIndex : 'geneID',
				width : 175,
                editor: {
                    allowBlank: true
                }
//				renderer : function(val) {
//					//console.log("<input id='experiment_selector_" + val + "' type='checkbox' value=" + val + "/>")
//					return "<div style=\"height:13px;\"><input type='text' value=" + val + "/><div>";
//					
//				}	
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