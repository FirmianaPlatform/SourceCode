Ext.define('gar.view.tools.EastPanel',{
    extend: 'Ext.tab.Panel',

    requires: [
    	'gar.view.tools.eastpanel.GoEnrich',
    	'gar.view.tools.eastpanel.GoClassification',
    	'gar.view.tools.eastpanel.PPI',
        'gar.view.tools.eastpanel.TreeInit',
        'gar.view.tools.eastpanel.GroupRecord',
        'gar.view.tools.eastpanel.Stack',
        'gar.view.tools.eastpanel.PCA',
        'gar.view.tools.eastpanel.pcaMetaMenu',
        'gar.view.tools.eastpanel.Volcano',
        'gar.view.tools.eastpanel.Venn',
        'gar.view.tools.eastpanel.TF-TG',
        'gar.view.tools.eastpanel.Kinase-Substrate',
        'gar.view.tools.eastpanel.KEGG',
        'gar.view.tools.eastpanel.KHeatmap',
        'gar.view.tools.eastpanel.MultiBoxplot',
        'gar.view.tools.eastpanel.Correlation',
        'gar.view.tools.eastpanel.Distribution',
        'gar.view.tools.eastpanel.Heatmap',
        'gar.view.tools.eastpanel.Motif',
        'gar.view.tools.eastpanel.Distribution'
    ],

    alias: 'widget.eastpanel',
    width: 300,
    split: true,
    collapsible: false,
    floatable: false,
//    plugins: Ext.create('Ext.ux.TabScrollerMenu', {
//        maxText: 15,
//        pageSize: 5
//    }),
    defaults : {
		//autoScroll : true,
		bodyPadding : 0
	},
	border : true,
	loadMask : true,
	viewConfig : {
		loadingText : 'Loading Experiment Relation Data...'
	},
    initComponent: function() {
    	// this.items = [{
	    	
	    // }];
	    
    	this.callParent(arguments);
    }
});