Ext.define("gar.view.tools.eastpanel.Kinase-Substrate", {
    extend: 'Ext.panel.Panel',
    height: 600,
    width: 300,
    layout: 'anchor',
    //id: 'eastpanelGoClassification',
    closable: false,
    alias: 'widget.eastKinase/Substrate',
    title: 'Kinase/Substrate',
    

    /**
     * @method initComponent
     * @inheritdoc
     * @return {void}
     */
    initComponent: function() {

        //var val = this.val
        this.items = []
    	this.callParent(arguments);
    }
})