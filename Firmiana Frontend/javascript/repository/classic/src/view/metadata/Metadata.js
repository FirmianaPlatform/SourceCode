Ext.define('dataViewer.view.metadata.Metadata', {
    extend: 'Ext.window.Window',

    title: '  New submisson - Metadata',
    width: 800,
    height: 650,
    autoShow: true,
    modal: true,

    controller: 'metadata',

    layout: {
        type: 'fit'
    },
    /**
     * @method initComponent
     * @inheritdoc
     * @return {void}
     */
    initComponent: function() {
        var required = '<span style="color:red;font-weight:bold" data-qtip="Required">*</span>';
        this.items = [{
            xtype: 'container',
            margin: '10 10 10 10',
            layout: 'fit',
            items:[{
                xtype: 'form',
                id: 'meta_form',
                url:'/repos/addAProjectRecord/',
                method: 'GET',
                layout: 'accordion',
                defaults: {
                    border: false,
                    bodyPadding: 5,
                    defaultType: 'textfield',
                    defaults: {
                        anchor: '100%'
                    }
                },
                items: [{
                    title: 'Basic Information',
                    layout: 'anchor',
                    scrollable: true,
                    defaults: {
                        anchor: '100%',
                        padding: '0 0 0 5'
                    },
                    items: [{
                        fieldLabel: 'Project title',
                        afterLabelTextTpl: required,
                        name: 'projectname',
                        allowBlank: false
                    },{
                        fieldLabel: 'Key words',
                        afterLabelTextTpl: required,
                        name: 'keywords',
                        allowBlank: false
                    },{
                        xtype: 'textareafield',
                        fieldLabel: 'Project description',
                        afterLabelTextTpl: required,
                        labelAlign: 'top',
                        name: 'projectdescription',
                        emptyText: 'An overall description of your study',
                        allowBlank: false
                    },{
                        xtype: 'textareafield',
                        fieldLabel: 'Sample processing protocol',
                        afterLabelTextTpl: required,
                        labelAlign: 'top',
                        name: 'sampleprotocol',
                        emptyText: 'Sample preparation steps, separation, enrichment strategies, mass spectrometry protocols...',
                        allowBlank: false
                    },{
                        xtype: 'textareafield',
                        fieldLabel: 'Data processing protocol',
                        afterLabelTextTpl: required,
                        labelAlign: 'top',
                        name: 'dataprotocol',
                        emptyText: 'Search parameters, quantitative analysis, software tools ...',
                        allowBlank: false
                    },{
                        xtype: 'tagfield',
                        fieldLabel: 'Experiment type',
                        afterLabelTextTpl: required,
                        name: 'ExperimentType',
                        store: Ext.create('dataViewer.store.metadata.ExperimentType'),
                        displayField: 'Miape_ExpType',
                        valueField: 'Miape_ExpType',
                        filterPickList: true,
                        queryMode: 'Miape_ExpType',
                        publishes: 'Miape_ExpType',
                        allowBlank: false
                    }]
                },{
                    title: 'Additional Information',
                    layout: 'anchor',
                    scrollable: true,
                    defaults: {
                        anchor: '100%',
                        padding: '0 0 0 5'
                    },
                    items: [{
                        xtype: 'tagfield',
                        fieldLabel: 'Species',
                        afterLabelTextTpl: required,
                        name: 'Species',
                        store: Ext.create('dataViewer.store.metadata.Species'),
                        displayField: 'Miape_Species',
                        valueField: 'Miape_Species',
                        filterPickList: true,
                        queryMode: 'Miape_Species',
                        publishes: 'Miape_Species',
                        allowBlank: false
                    },{
                        xtype: 'tagfield',
                        fieldLabel: 'Tissue',
                        afterLabelTextTpl: required,
                        name: 'Tissue',
                        store: Ext.create('dataViewer.store.metadata.Tissue'),
                        displayField: 'Miape_Tissue',
                        valueField: 'Miape_Tissue',
                        filterPickList: true,
                        queryMode: 'Miape_Tissue',
                        publishes: 'Miape_Tissue',
                        allowBlank: false
                    },{
                        xtype: 'tagfield',
                        fieldLabel: 'Modification',
                        afterLabelTextTpl: required,
                        name: 'Modification',
                        store: Ext.create('dataViewer.store.metadata.Modification'),
                        displayField: 'Miape_Modification',
                        valueField: 'Miape_Modification',
                        filterPickList: true,
                        queryMode: 'Miape_Modification',
                        publishes: 'Miape_Modification',
                        allowBlank: false
                    },{
                        xtype: 'tagfield',
                        fieldLabel: 'Instrument',
                        afterLabelTextTpl: required,
                        name: 'Instrument',
                        store: Ext.create('dataViewer.store.metadata.Instrument'),
                        displayField: 'Miape_Instrument',
                        valueField: 'Miape_Instrument',
                        filterPickList: true,
                        queryMode: 'Miape_Instrument',
                        publishes: 'Miape_Instrument',
                        allowBlank: false
                    },{
                        xtype: 'tagfield',
                        fieldLabel: 'Cell Type',
                        afterLabelTextTpl: required,
                        name: 'CellType',
                        store: Ext.create('dataViewer.store.metadata.CellType'),
                        displayField: 'Miape_CellType',
                        valueField: 'Miape_CellType',
                        filterPickList: true,
                        queryMode: 'Miape_CellType',
                        publishes: 'Miape_CellType',
                        allowBlank: false
                    },{
                        xtype: 'tagfield',
                        fieldLabel: 'Disease',
                        afterLabelTextTpl: required,
                        name: 'Disease',
                        store: Ext.create('dataViewer.store.metadata.Disease'),
                        displayField: 'Miape_Disease',
                        valueField: 'Miape_Disease',
                        filterPickList: true,
                        queryMode: 'Miape_Disease',
                        publishes: 'Miape_Disease',
                        allowBlank: false
                    },{
                        xtype: 'tagfield',
                        fieldLabel: 'Quantification Method',
                        afterLabelTextTpl: required,
                        name: 'QuantMethods',
                        store: Ext.create('dataViewer.store.metadata.QuantMethod'),
                        displayField: 'Miape_QuantMethod',
                        valueField: 'Miape_QuantMethod',
                        filterPickList: true,
                        queryMode: 'Miape_QuantMethod',
                        publishes: 'Miape_QuantMethod',
                        allowBlank: false
                    }]
                },{
                    title: 'Lab Head',
                    layout: 'anchor',
                    scrollable: true,
                    defaults: {
                        anchor: '100%',
                        padding: '0 0 0 5'
                    },
                    items: [{
                        fieldLabel: 'Name',
                        afterLabelTextTpl: required,
                        name: 'name',
                        allowBlank: false
                    },{
                        fieldLabel: 'Email',
                        afterLabelTextTpl: required,
                        name: 'email',
                        vtype: 'email',
                        allowBlank: false
                    },{
                        xtype: 'textareafield',
                        fieldLabel: 'Affiliation',
                        labelAlign: 'top',
                        afterLabelTextTpl: required,
                        name: 'affiliation',
                        allowBlank: false
                    }]
                },{
                    title: 'Additional Dataset Details (Optional)',
                    layout: 'anchor',
                    scrollable: true,
                    defaults: {
                        anchor: '100%',
                        padding: '0 0 0 5'
                    },
                    items: [{
                        fieldLabel: 'PubMed ID(s)',
                        // afterLabelTextTpl: required,
                        name: 'pubmedID',
                        allowBlank: false
                    },{
                        fieldLabel: 'Reanalysis ProteomeXChange accession(s)',
                        labelAlign: 'top',
                        // afterLabelTextTpl: required,
                        name: 'rePXaccession',
                        allowBlank: false
                    },{
                        fieldLabel: "Links to other 'Omics' datasets",
                        labelAlign: 'top',
                        // afterLabelTextTpl: required,
                        name: 'linkToOther',
                        allowBlank: false
                    }]
                }],
                

                // Reset and Submit buttons
                buttons: [{
                    text: 'Reset',
                    handler: function() {
                        this.up('form').getForm().reset();
                    }
                }, {
                    text: 'Submit',
                    formBind: true, //only enabled once the form is valid
                    disabled: true,
                    handler: function() {
                        var form = this.up('form').getForm();
                        if (form.isValid()) {
                            form.submit({
                                waitMsg: 'Submitting form...',
                                success: function(form, action) {
                                    Ext.Msg.alert('Success', action.result.msg);
                                },
                                failure: function(form, action) {
                                    Ext.Msg.alert('Failed', action.result.msg);
                                }
                            });
                        }
                    }
                }]
            }]
        }]
        this.callParent(arguments);
    }
});
