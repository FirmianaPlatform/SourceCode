Ext.define("gar.view.tools.eastpanel.TF-TG", {
    extend: 'Ext.panel.Panel',
    height: 600,
    width: 300,
    layout: 'anchor',
    //id: 'eastpanelGoClassification',
    closable: false,
    alias: 'widget.eastTF-TG',
    title: 'TF-TG',
    

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