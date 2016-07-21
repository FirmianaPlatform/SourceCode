Ext.define('gar.view.tools.CenterPanel',{
    extend: 'Ext.tab.Panel',

    requires: [
    	'gar.view.tools.centerpanel.PPI',
        'gar.view.tools.centerpanel.Distribution',
        'gar.view.tools.centerpanel.MultiBoxplot',
        'gar.view.tools.centerpanel.PCA',
        'gar.view.tools.centerpanel.Correlation',
        'gar.view.tools.centerpanel.Stack',
        'gar.view.tools.centerpanel.Heatmap',
        'gar.view.tools.centerpanel.KHeatmap',
        'gar.view.tools.centerpanel.GroupExperiment',
        'gar.view.tools.centerpanel.Volcano',
        'gar.view.tools.centerpanel.Venn',
        'gar.view.tools.centerpanel.GoClassification',
        'gar.view.tools.centerpanel.GoEnrich',
        'gar.view.tools.centerpanel.test',
        'gar.view.tools.centerpanel.TF-TG',
        'gar.view.tools.centerpanel.Kinase-Substrate',
        'gar.view.tools.centerpanel.KEGG',
        'gar.view.tools.centerpanel.Motif'
    ],

    alias: 'widget.centerpanel',
    region: 'center',
    id: 'toolsCenterpanel',
    // width: 600,
    //split: true,
    border: false,
    //floatable: false,
    //autoScroll: false,
//    plugins: Ext.create('Ext.ux.TabScrollerMenu', {
//        maxText: 15,
//        pageSize: 5
//    }),

    initComponent: function() {

    	// this.items = [{
	    // 	xtype: 'statusbar',

     //        // defaults to use when the status is cleared:
     //        defaultText: 'Default status text',
     //        defaultIconCls: 'default-icon',

     //        // values to set initially:
     //        text: 'Ready',
     //        iconCls: 'ready-icon',

     //        // any standard Toolbar items:
     //        items: [{
     //            text: 'A Button'
     //        }, '-', 'Plain Text']
	    // }];
	    
    	this.callParent(arguments);
    }
});