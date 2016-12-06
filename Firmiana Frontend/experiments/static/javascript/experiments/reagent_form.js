Ext.onReady(function() {
    var add_application=function(){
        var win = new Ext.Window({
            title: 'ADD Application',
            width: 400,
            items: [
                {
                    xtype:'form',
                    border: true,
                    frame: true,
                    id: 'application_form',
                    items: [{
                        xtype: 'textfield',
                        labelWidth: 120,
                        labelAligh: 'left',
                        width: 450,
                        fieldLabel: 'Application',
                        name: 'Application'
                    }]
                }
            ],
            bbar: [
                '->',
                {
                    text: 'Submit',
                    handler: function(){
                        application_form = Ext.getCmp('application_form');
                        var newV = application_form.items.items[0].value;
                        applicationStore.add({Application:newV});
                        win.close();
                    }
                }
            ]
        });
        win.show();
    };

    var add_react_pecies=function(){
        var win = new Ext.Window({
            title: 'ADD React Species',
            width: 400,
            items: [
                {
                    xtype:'form',
                    border: true,
                    frame: true,
                    id: 'species_form',
                    items: [{
                        xtype: 'textfield',
                        labelWidth: 120,
                        labelAligh: 'left',
                        width: 450,
                        fieldLabel: 'React Species',
                        name: 'React Species'
                    }]
                }
            ],
            bbar: [
                '->',
                {
                    text: 'Submit',
                    handler: function(){
                        species_form = Ext.getCmp('species_form');
                        var newV = species_form.items.items[0].value;
                        reactSpeciesStore.add({React_species:newV});
                        win.close();
                    }
                }
            ]
        });
        win.show();
    };

    //CSRF protection
    csrftoken = Ext.util.Cookies.get('csrftoken');
    
    // function: submit / canel form
    var submitForm = function() {
        formpanel = Ext.getCmp('formPanel');
        form = formpanel.getForm();
        if (form.isValid()){
            form.submit({
                url :  '/experiments/save/reagent/',
                standardSubmit: true,
            })
        }
    };

    var cancelForm = function() {
        formpanel = Ext.getCmp('formPanel');
        formpanel.getForm().reset();
    };

    //Manufactorer Store
    var reagentManufacturerStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Reagent_manufacturer/',
            reader: {
                type: 'json',
                root: 'Reagent_manufacturers'
            }
        },
        fields: [
            {name: 'Reagent_manufacturer', type: 'string'}
        ],
        autoLoad: true
    });

    // React Sepecies Store
    var reactSpeciesStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/React_species/',
            reader: {
                type: 'json',
                root: 'React_speciess'
            }
        },
        fields: [
            {name:'React_species', type: 'string'}
        ],
        autoLoad: true
    });

    var antigenClonalTypeStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Antigen_clonal_type/',
            reader: {
                type: 'json',
                root: 'Antigen_clonal_types'
            }
        },
        fields: [
            {name:'Antigen_clonal_type', type: 'string'}
        ],
        autoLoad: true
    });

    // Antigen Host Species Store
    var antigenSpeciesStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Antigen_species/',
            reader: {
                type: 'json',
                root: 'Antigen_speciess'
            }
        },
        fields: [
            {name:'Antigen_species', type: 'string'}
        ],
        autoLoad: true
    });

    var antigenModificationStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Antigen_modification/',
            reader: {
                type: 'json',
                root: 'Antigen_modifications'
            }
        },
        fields: [
            {name:'Antigen_modification', type: 'string'}
        ],
        autoLoad: true
    });

    //Purification Store
    var purificationStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Purification/',
            reader: {
                type: 'json',
                root: 'Purifications'
            }
        },
        fields: [
            {name: 'Purification', type: 'string'}
        ],
        autoLoad: true
    });

    // Conjugate Store
    var conjugateStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Conjugate/',
            reader: {
                type: 'json',
                root: 'Conjugates'
            }
        },
        fields: [
            {name: 'Conjugate', type: 'string'}
        ],
        autoLoad: true
    });

    //Affinity Store
    var affinityStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Affinity/',
            reader: {
                type: 'json',
                root: 'Affinitys'
            }
        },
        fields: [
            {name: 'Affinity', type: 'string'}
        ],
        autoLoad: true
    });

    // Application Store
    var applicationStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url: '/experiments/ajax/display/Application/',
            reader: {
                type: 'json',
                root: 'Applications'
            }
        },
        fields: [
            {name: 'Application', type: 'string'}
        ],
        autoLoad: true
    });

    //general panel information
    var general = Ext.create('Ext.panel.Panel', {
        title: 'GENERAL',
        frame: true,
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
                fieldLabel: 'Name',
                name: 'name'
            },{
                xtype: 'combobox',
                fieldLabel: 'Manufacturer',
                displayField: 'Reagent_manufacturer',
                name: 'Reagent_manufacturer',
                store: reagentManufacturerStore,
                queryModel: true,
                typeAhead: true
            },{
                xtype: 'textfield',
                fieldLabel: 'Catalog No',
                name: 'catalog_no'
            },{
                xtype: 'combobox',
                fieldLabel: 'Affinity',
                displayField: 'Affinity',
                name: 'Affinity',
                store: affinityStore,
                queryModel: 'local',
                typeAhead: true
            },{
                xtype: 'container',
                layout: {
                    type: 'hbox',
                    align: 'stretch',
                },
                items: [
                    {
                        xtype: 'combobox',
                        fieldLabel: 'Application',
                        displayField: 'Application',
                        name: 'Application',
                        store: applicationStore,
                        queryMode: 'local',
                        multiSelect: true,
                        labelWidth: 120,
                        width: 415,
                        allowBlank: false,
                    },{
                        xtype: 'button',
                        text: 'Add',
                        handler: add_application
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
                        valueField: 'React_species',
                        fieldLabel: 'Species React',
                        name: 'React_species',
                        displayField: 'React_species',
                        store: reactSpeciesStore,
                        queryMode: 'local',
                        multiSelect:true,
                        labelWidth: 120,
                        width: 415,
                        allowBlank: false
                    },{
                        xtype: 'button',
                        text: 'Add',
                        handler: add_react_pecies
                    }
                ]
            },{
                xtype: 'combobox',
                fieldLabel: 'Purification',
                displayField: 'Purification',
                name: 'Purification',
                store: purificationStore,
                queryMode: 'local',
                typeAhead: true
            },{
                xtype: 'combobox',
                fieldLabel: 'Conjugate',
                name: 'Conjugate',
                displayField: 'Conjugate',
                store: conjugateStore,
                queryMode: 'local',
                typeAhead: true
            },{
                xtype: 'radiogroup',
                fieldLabel: 'Reagent type',
                name: 'reagent_type',
                id: 'reagent_type',
                columns: 2,
                vertical: true,
                items: [
                    {boxLabel:'Antigen',name:'reagent_type', inputValue:'Antigen',},
                    {boxLabel:'DNA',name:'reagent_type', inputValue:'DNA'},
                    {boxLabel:'Protein',name:'reagent_type', inputValue:'Protein'},
                    {boxLabel:'Other',name:'reagent_type', inputValue:'other'},
                ]
            },{
                xtype: 'hiddenfield',
                name: 'csrfmiddlewaretoken',
                value: csrftoken
            }]
    });


    buttonPanel = Ext.create('Ext.panel.Panel', {
        frame: true,
        renderTo: 'button',
        border: true,
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
            frame: true,
            id: 'formPanel',
            renderTo: 'form',
            items: [general],
    });

    //antigen information
    var antigen = Ext.create( 'Ext.panel.Panel',{
        title: 'ANTIGEN INFO',
        border: true,
        frame: true,
        id: 'antigen',
        headerPosition: 'left',
        defaults: {
            labelWidth: 120,
            labelAligh: 'left',
            width: 450,
            allowBlank: true,
        },
        items: [
            {
                xtype: 'textfield',
                fieldLabel: 'GeneID',
                name: 'gene_id'
            },{
                xtype: 'combobox',
                fieldLabel: 'Host Species',
                displayField: 'Antigen_species',
                name: 'Antigen_species',
                store: antigenSpeciesStore,
                queryMode: 'local',
                typeAhead: true
            },{
                xtype: 'combobox',
                fieldLabel: 'Clonal Type',
                name: 'Antigen_clonal_type',
                displayField: 'Antigen_clonal_type',
                store: antigenClonalTypeStore,
                queryMode: 'local',
                typeAhead: true
            },{
                xtype: 'combobox',
                fieldLabel: 'Modification',
                name: 'Antigen_modification',
                displayField: 'Antigen_modification',
                store: antigenModificationStore,
                queryMode: 'local',
                typeAhead: true
            }]
    });

    //dna information
    var dna = Ext.create( 'Ext.panel.Panel',{
        title: 'DNA INFO',
        border: true,
        frame: true,
        id: 'dna',
        headerPosition: 'left',
        defaults: {
            labelWidth: 120,
            labelAligh: 'left',
            width: 450,
            allowBlank: false,
        },
        items: [
            {
                xtype: 'textareafield',
                name: 'dna_sequence',
                fieldLabel: 'DNA Sequence',
            }
        ]
    });
                

    //ubi information
    var ubi = Ext.create( 'Ext.panel.Panel',{
        title: 'UBI INFO',
        border: true,
        frame: true,
        id: 'ubi',
        headerPosition: 'left',
        defaults: {
            labelWidth: 120,
            labelAligh: 'left',
            width: 450,
            allowBlank: false,
        },
        items: [
            {
                xtype: 'textareafield',
                name: 'domain',
                fieldLabel: 'Domain',
            }
        ]
    });
                
    //Other information
    var remarks = Ext.create( 'Ext.panel.Panel',{
        title: 'REMARKS',
        border: true,
        frame: true,
        id: 'remarks',
        headerPosition: 'left',
        defaults: {
            labelWidth: 120,
            labelAligh: 'left',
            width: 450,
            allowBlank: false,
        },
        items: [
            {
                xtype: 'textareafield',
                name: 'remarks',
                fieldLabel: 'Remarks',
            }
        ]
    });

    //event listener for type radio
    typeradio = Ext.getCmp('reagent_type');
    typeradio.on('change', function(radio, newV, oldV, e){
        if (oldV.reagent_type == 'Antigen'){
            formPanel.remove(antigen, false);
        } else if (oldV.reagent_type == 'DNA'){
            formPanel.remove(dna, false);
        } else if (oldV.reagent_type == 'Protein') {
            formPanel.remove(ubi, false);
        } else if (oldV.reagent_type == 'other') {
            formPanel.remove(remarks, false);
        }

        if (newV.reagent_type == 'Antigen'){
            formPanel.add(antigen);
        } else if (newV.reagent_type == 'DNA'){
            formPanel.add(dna);
        } else if (newV.reagent_type == 'Protein') {
            formPanel.add(ubi);
        } else {
            formPanel.add(remarks);
        }
    });
});
