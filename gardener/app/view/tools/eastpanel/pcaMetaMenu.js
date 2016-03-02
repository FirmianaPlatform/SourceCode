Ext.define("gar.view.tools.eastpanel.pcaMetaMenu", {
    extend: 'Ext.panel.Panel',
    height: 600,
    width: 300,
    layout: 'anchor',
    //id: 'eastpanelPCA',
    closable: false,
    alias: 'widget.pcaMetaMenu',
    //title: 'PCA Information',
    

    /**
     * @method initComponent
     * @inheritdoc
     * @return {void}
     */
    initComponent: function() {
        this.items = [
        {
            xtype: 'panel',
            anchor: '100% 100%',
            items: [{
                xtype: 'fieldset',
                margin: '10 15 0 15',
                title: 'Experiment Info',
                defaultType: 'checkbox', // each item will be a checkbox
                layout: 'anchor',
                defaults: {
                    anchor: '100%',
                    hideEmptyLabel: false,
                    labelWidth: 0,
                    checked:false
                },
                items: [{
                    boxLabel: 'Species',
                    name: 'species',
                    inputValue: 'species'
                }, {
                    boxLabel: 'Date of experiment',
                    name: 'dateOfExperiment',
                    inputValue: 'dateOfExperiment',
                    checked:true
                }, {
                    boxLabel: 'Date of operation',
                    name: 'dateOfOperation',
                    inputValue: 'dateOfOperation'
                }, {
                    boxLabel: 'Instrument',
                    name: 'instrument',
                    inputValue: 'instrument'
                }, {
                    boxLabel: 'Method',
                    name: 'method',
                    inputValue: 'method'
                }, {
                    boxLabel: 'Separation',
                    name: 'separation',
                    inputValue: 'separation'
                }, {
                    boxLabel: 'Sex',
                    name: 'sex',
                    inputValue: 'sex'
                }, {
                    boxLabel: 'Age',
                    name: 'age',
                    inputValue: 'age'
                }, {
                    boxLabel: 'Reagent',
                    name: 'reagent',
                    inputValue: 'reagent'
                }, {
                    boxLabel: 'Sample',
                    name: 'sample',
                    inputValue: 'sample',
                    checked:true
                }, {
                    boxLabel: 'Tissue/Cell Type',
                    name: 'tissueType',
                    inputValue: 'tissueType'
                }, {
                    boxLabel: 'Strain',
                    name: 'strain',
                    inputValue: 'strain'
                }, {
                    boxLabel: 'CR Time',
                    name: 'circ_time',
                    inputValue: 'circ_time'
                }
                ]
            }]
        }]
    	this.callParent(arguments);
    }
})