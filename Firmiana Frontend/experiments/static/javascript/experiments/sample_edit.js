Ext.onReady(function() {
    var add_rx_treament=function(){
        var win = new Ext.Window({
            title: 'ADD Treatment',
            width: 400,
            items: [
                {
                    xtype:'form',
                    border: true,
                    frame: true,
                    id: 'treatment_form',
                    items: [{
                        xtype: 'textfield',
                        labelWidth: 120,
                        labelAligh: 'left',
                        width: 450,
                        fieldLabel: 'Treatment',
                        name: 'Treatment'
                    }]
                }
            ],
            bbar: [
                '->',
                {
                    text: 'Submit',
                    handler: function(){
                        treatment_form = Ext.getCmp('treatment_form');
                        var newV = treatment_form.items.items[0].value;
                        rxTreatmentStore.add({Rx_treatment:newV});
                        win.close();
                    }
                }
            ]
        });
        win.show();
    };

    var add_ubi_subcell=function(){
        var win = new Ext.Window({
            title: 'ADD Subcelluar Organelle',
            width: 400,
            items: [
                {
                    xtype:'form',
                    border: true,
                    frame: true,
                    id: 'subcell_form',
                    items: [{
                        xtype: 'textfield',
                        labelWidth: 120,
                        labelAligh: 'left',
                        width: 450,
                        fieldLabel: 'Subcelluar Organelle',
                        name: 'Subcelluar Orangelle'
                    }]
                }
            ],
            bbar: [
                '->',
                {
                    text: 'Submit',
                    handler: function(){
                        var subcell_form = Ext.getCmp('subcell_form');
                        var newV = subcell_form.items.items[0].value;
                        ubiSubcellStore.add({Ubi_subcell:newV});
                        win.close();
                    }
                }
            ]
        });
        win.show();
    };

    var add_ubi_method = function(){
        var win = new Ext.Window({
            title: 'ADD Method',
            width: 400,
            items: [
                {
                    xtype:'form',
                    border: true,
                    frame: true,
                    id: 'method_form',
                    items: [{
                        xtype: 'textfield',
                        labelWidth: 120,
                        labelAligh: 'left',
                        width: 450,
                        fieldLabel: 'Method',
                        name: 'Method'
                    }]
                }
            ],
            bbar: [
                '->',
                {
                    text: 'Submit',
                    handler: function(){
                        method_form = Ext.getCmp('method_form');
                        var newV = method_form.items.items[0].value;
                        ubiMethodStore.add({Ubi_method:newV});
                        win.close();
                    }
                }
            ]
        });
        win.show();
    };
    //CSRF protection
    csrftoken = Ext.util.Cookies.get('csrftoken');

    var submitForm = function() {
        formpanel = Ext.getCmp('formPanel');
        form = formpanel.getForm();
        if (form.isValid()){
            form.submit({
                url :  '/experiments/editsave/sample/',
                standardSubmit: true,
            })
        }
    };
        
    var cancelForm = function() {
        formpanel = Ext.getCmp('formPanel');
        formpanel.getForm().reset();
    };

    //experimenter Model and store
    
    var experimenterStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/experimenter/',
            reader: {
                type: 'json',
                root: 'experimenters',
            }
        },
        fields: [
            {name: 'experimenter', type: 'string'}
        ],
        autoLoad: true
    });

    var sourceTaxonStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Source_taxon/',
            reader: {
                type: 'json',
                root: 'Source_taxons',
            }
        },
        fields: [
            {name: 'Source_taxon', type: 'string'}
        ],
        autoLoad: true
    });
    
    var rxTreatmentStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Rx_treatment/',
            reader: {
                type: 'json',
                root: 'Rx_treatments',
            }
        },
        fields: [
            {name: 'Rx_treatment', type: 'string'}
        ],
        autoLoad: true
    });
    
    var ubiSubcellStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Ubi_subcell/',
            reader: {
                type: 'json',
                root: 'Ubi_subcells',
            }
        },
        fields: [
            {name: 'Ubi_subcell', type: 'string'}
        ],
        autoLoad: true
    });
    
    var ubiMethodStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Ubi_method/',
            reader: {
                type: 'json',
                root: 'Ubi_methods',
            }
        },
        fields: [
            {name: 'Ubi_method', type: 'string'}
        ],
        autoLoad: true
    });
    
    var ubiDetergentStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Ubi_detergent/',
            reader: {
                type: 'json',
                root: 'Ubi_detergents',
            }
        },
        fields: [
            {name: 'Ubi_detergent', type: 'string'}
        ],
        autoLoad: true
    });
    
    var ubiSaltStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Ubi_salt/',
            reader: {
                type: 'json',
                root: 'Ubi_salts',
            }
        },
        fields: [
            {name: 'Ubi_salt', type: 'string'}
        ],
        autoLoad: true
    });
    
    var genotypeStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Genotype/',
            reader: {
                type: 'json',
                root: 'Genotypes',
            }
        },
        fields: [
            {name: 'Genotype', type: 'string'}
        ],
        autoLoad: true
    });
    
    var cellTypeStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Cell_type/',
            reader: {
                type: 'json',
                root: 'Cell_types',
            }
        },
        fields: [
            {name: 'Cell_type', type: 'string'}
        ],
        autoLoad: true
    });
    
    var tissueTypeStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Tissue_type/',
            reader: {
                type: 'json',
                root: 'Tissue_types',
            }
        },
        fields: [
            {name: 'Tissue_type', type: 'string'}
        ],
        autoLoad: true
    });
    
    var tissueStrainStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Tissue_strain/',
            reader: {
                type: 'json',
                root: 'Tissue_strains',
            }
        },
        fields: [
            {name: 'Tissue_strain', type: 'string'}
        ],
        autoLoad: true
    });
    
    var tissueGenderStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Tissue_gender/',
            reader: {
                type: 'json',
                root: 'Tissue_genders',
            }
        },
        fields: [
            {name: 'Tissue_gender', type: 'string'}
        ],
        autoLoad: true
    });
    
    
    //general panel
    var generalPanel = Ext.create('Ext.form.Panel', {
        title: 'GENERAL',
        frame: true,
        storeId: 'methods',
        layout: 'auto',
        headerPosition: 'left',
        bodyStyle: 'padding: 10;',
        defaults: {
            labelWidth: 120,
            labelAligh: 'left',
            width: 450,
            allowBlank: false,
        },
        items: [
            {
                xtype: 'textfield',
                fieldLabel: 'Sample NO.',
                name:'sample_no',
                readOnly: true
            },{
                xtype: 'combobox',
                fieldLabel: 'Experimenter',
                displayField: 'experimenter',
                name: 'experimenter',
                store: experimenterStore,
            },{
                xtype: 'datefield',
                fieldLabel: 'Date',
                name: 'date'
            },{
                xtype: 'textfield',
                fieldLabel: 'Location',
                name: 'location'
            },{
                xtype: 'radiogroup',
                fieldLabel: 'Source Type',
                name: 'cell_tissue',
                id: 'cell_tissue',
                columns: 2,
                items: [
                    {boxLabel: 'Tissue', name: 'cell_tissue',inputValue:'Tissue'},   
                    {boxLabel: 'Cell', name: 'cell_tissue',inputValue:'Cell'},   
                ],
            },{
                xtype: 'hiddenfield',
                name: 'csrfmiddlewaretoken',
                value: csrftoken
            }]
    });

    //source  tissue  panel
    var source_tissue = Ext.create( 'Ext.form.Panel',{
        title: 'TISSUE',
        border: true,
        frame: true,
        headerPosition: 'left',
        defaults: {
            labelWidth: 120,
            labelAligh: 'left',
            width: 450,
            allowBlank: false,
        },
        items: [{
                xtype: 'combobox',
                fieldLabel: 'Taxon',
                displayField: 'Source_taxon',
                name: 'Source_taxon',
                store: sourceTaxonStore,
            },{
                xtype: 'combobox',
                fieldLabel: 'Tissue',
                displayField: 'Tissue_type',
                name: 'Tissue_type',
                store: tissueTypeStore,
            },{
                xtype: 'combobox',
                fieldLabel: 'Gender',
                displayField: 'Tissue_gender',
                name: 'Tissue_gender',
                store: tissueGenderStore,
            },{
                xtype: 'combobox',
                fieldLabel: 'Strain',
                displayField: 'Tissue_strain',
                name: 'Tissue_strain',
                store: tissueStrainStore,
            },{
                xtype: 'combobox',
                fieldLabel: 'Genotype',
                displayField: 'Genotype',
                name: 'Genotype',
                store: genotypeStore,
            },{
                xtype: 'textfield',
                fieldLabel: 'Changes',
                name: 'changes'
            },{
                xtype: 'textfield',
                fieldLabel: 'Age',
                name: 'age'
            },{
                xtype: 'timefield',
                fieldLabel: 'Circ Time',
                format: 'G:i:s',
                increment: 15,
                name: 'circ_time'
            }]
    });

    // source  cell  panel
    var source_cell = Ext.create( 'Ext.form.Panel',{
        title: 'CELL',
        border: true,
        frame: true,
        headerPosition: 'left',
        defaults: {
            labelWidth: 120,
            labelAligh: 'left',
            width: 450,
            allowBlank: false,
        },
        items: [
            {
                xtype: 'combobox',
                fieldLabel: 'Taxon',
                displayField: 'Source_taxon',
                name: 'Source_taxon',
                store: sourceTaxonStore,
            },{
                xtype: 'combobox',
                fieldLabel: 'Cell',
                displayField: 'Cell_type',
                name: 'Cell_type',
                store: cellTypeStore,
            },{
                xtype: 'textfield',
                fieldLabel: 'Age',
                name: 'age'
            },{
                xtype: 'combobox',
                fieldLabel: 'Genotype',
                displayField: 'Genotype',
                name: 'Genotype',
                store: genotypeStore
            },{
                xtype: 'textfield',
                fieldLabel: 'Changes',
                name: 'changes'
            },{
                xtype: 'timefield',
                fieldLabel: 'Circ Time',
                format: 'G:i:s',
                increment: 15,
                name: 'circ_time'
            }]
    });

    //rx panel
    var rxPanel = Ext.create( 'Ext.form.Panel',{
        title: 'RX',
        border: true,
        frame: true,
        bodyStyle: 'padding: 5 5 0',
        layout:'anchor',
        headerPosition: 'left',
        defaults: {
            labelWidth: 120,
            labelAligh: 'left',
            width: 450,
            allowBlank: false,
        },
        items: [
            {
                xtype: 'container',
                layout: {
                    type: 'hbox',
                    align: 'stretch',
                },
                items: [
                    {
                        xtype: 'combobox',
                        fieldLabel: 'Treatments',
                        displayField: 'Rx_treatment',
                        name: 'Rx_treatment',
                        store: rxTreatmentStore,
                        queryMode: 'local',
                        multiSelect: true,
                        editable: false,
                        labelWidth: 120,
                        width: 415,
                        allowBlank: false,
                    },{
                        xtype: 'button',
                        text: 'Add',
                        handler: add_rx_treament
                    }
                ]
            },{
                xtype:'textfield',
                name: 'amount',
                fieldLabel: 'Amount'
            },{
                xtype:'textfield',
                name:'duration',
                fieldLabel: 'Duration'
            }]
    });
                
    //
    var ubiPanel = Ext.create( 'Ext.form.Panel',{
        title: 'UBI INFO',
        border: true,
        frame: true,
        headerPosition: 'left',
        defaults: {
            labelWidth: 120,
            labelAligh: 'left',
            width: 450,
            allowBlank: false,
        },
        items: [
            {
                xtype: 'container',
                layout: {
                    type: 'hbox',
                    align: 'stretch',
                },
                items: [
                    {
                        xtype: 'combobox',
                        fieldLabel: 'Subcelluar Organelle',
                        name: 'Ubi_subcell',
                        displayField: 'Ubi_subcell',
                        store: ubiSubcellStore,
                        queryMode: 'local',
                        multiSelect: true,
                        editable: false,
                        labelWidth: 120,
                        width: 415,
                        allowBlank: false,
                    },{
                        xtype: 'button',
                        text: 'Add',
                        handler: add_ubi_subcell
                    }
                ]
            },{
                xtype: 'container',
                layout: {
                    type: 'hbox',
                    align: 'stretch',
                },
                items: [
                    {
                        xtype: 'combobox',
                        valueField: 'Ubi_method',
                        fieldLabel: 'Methods',
                        displayField: 'Ubi_method',
                        name: 'Ubi_method',
                        store: ubiMethodStore,
                        queryMode: 'local',
                        multiSelect: true,
                        editable: false,
                        labelWidth: 120,
                        width: 415,
                        allowBlank: false,
                    },{
                        xtype: 'button',
                        text: 'Add',
                        handler: add_ubi_method
                    }
                ]
            },{
                xtype:'combobox',
                name: 'Ubi_detergent',
                displayField: 'Ubi_detergent',
                fieldLabel: 'Ubi_detergent',
                store: ubiDetergentStore
            },{
                xtype: 'combobox',
                name: 'Ubi_salt',
                displayField: 'Ubi_salt',
                fieldLabel: 'Ubi_salt',
                store: ubiSaltStore
            }
        ]
    });

    var commentsPanel = Ext.create( 'Ext.form.Panel',{
        title: 'COMMENTS',
        border: true,
        frame: true,
        headerPosition: 'left',
        defaults: {
            labelWidth: 120,
            labelAlign: 'top',
            width: 450,
            allowBlank: false,
        },
        items: [
            {
                xtype: 'textareafield',
                name: 'comments',
                fieldLabel: 'Extract Comments',
            }
        ]
    });

    var buttonPanel = Ext.create('Ext.panel.Panel', {
        frame: true,
        //renderTo: 'button',
        buttons: [
            {
                text: 'Submit',
                handler: submitForm
            },{
                text: 'Cancel',
                handler: cancelForm
            }]
    });
        

    formPanel = Ext.create('Ext.form.Panel', {
        id: 'formPanel',
        renderTo: 'form',
        items: [ generalPanel, rxPanel, ubiPanel, commentsPanel, buttonPanel],
    });


    //event listener for type radio
    typeradio = Ext.getCmp('cell_tissue');
    typeradio.on('change', function(radio, newV, oldV, e){
        if (oldV.cell_tissue== 'Tissue'){
            formPanel.remove(source_tissue, false);
        } else if (oldV.cell_tissue == 'Cell'){
            formPanel.remove(source_cell, false);
        }

        if (newV.cell_tissue == 'Tissue'){
            formPanel.insert(1, source_tissue);
        } else if (newV.cell_tissue == 'Cell'){
            formPanel.insert(1, source_cell);
        }
    });

    cell_tissue_value = Ext.get('cell_tissue_value')
    typeradio.setValue({'cell_tissue':cell_tissue_value.getHTML()});
    console.log(cell_tissue_value.getHTML());
    no = Ext.get('no');
    formPanel.getForm().load({
        url: '/experiments/load/sample/',
        method: 'POST',
        params: {
            sample_no : no.getHTML(),
            csrfmiddlewaretoken:csrftoken
        },
    });
});
