Ext.define("gar.view.tools.eastpanel.Correlation", {
    extend: 'Ext.panel.Panel',
    height: 600,
    width: 300,
    layout: 'anchor',
    //id: 'eastpanelGoEnrich',
    closable: false,
    alias: 'widget.eastCorrelation',
    title: 'Correlation',
    
    initComponent: function() {
        //var val = this.val
		var panel = Ext.create('Ext.panel.Panel', {		
			border: 0,
			anchor: '100% 100%',
			autoScroll: true
		});
        this.items = [panel]
    	this.callParent(arguments);
    }
})