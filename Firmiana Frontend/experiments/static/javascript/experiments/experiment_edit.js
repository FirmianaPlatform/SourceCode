Ext.onReady(function() {
    var add_digest_type=function(){
        var win = new Ext.Window({
            title: 'ADD Digest Type',
            width: 400,
            items: [
                {
                    xtype:'form',
                    border: true,
                    frame: true,
                    id: 'type_form',
                    items: [{
                        xtype: 'textfield',
                        labelWidth: 120,
                        labelAligh: 'left',
                        width: 450,
                        fieldLabel: 'Type',
                        name: 'Type'
                    }]
                }
            ],
            bbar: [
                '->',
                {
                    text: 'Submit',
                    handler: function(){
                        var type_form = Ext.getCmp('type_form');
                        var newV = type_form.items.items[0].value;
                        digestTypeStore.add({Digest_type:newV});
                        win.close();
                    }
                }
            ]
        });
        win.show();
    };

    var add_digest_enzyme = function(){
        var win = new Ext.Window({
            title: 'ADD Digest Enzyme',
            width: 400,
            items: [
                {
                    xtype:'form',
                    border: true,
                    frame: true,
                    id: 'enzyme_form',
                    items: [{
                        xtype: 'textfield',
                        labelWidth: 120,
                        labelAligh: 'left',
                        width: 450,
                        fieldLabel: 'Enzyme',
                        name: 'Enzyme'
                    }]
                }
            ],
            bbar: [
                '->',
                {
                    text: 'Submit',
                    handler: function(){
                        enzyme_form = Ext.getCmp('enzyme_form');
                        var newV = enzyme_form.items.items[0].value;
                        digestEnzymeStore.add({Digest_enzyme:newV});
                        win.close();
                    }
                }
            ]
        });
        win.show();
    };
    //CSRF protection
    csrftoken = Ext.util.Cookies.get('csrftoken');

    Ext.QuickTips.init();
    //function used to deal submit and cancel form
    var submitForm = function() {
        form = formPanel.getForm();
        if (form.isValid()){
            form.submit({
                url :  '/experiments/editsave/experiment/',
                standardSubmit: true,
            })
        }
    };

    var cancelForm = function() {
        formPanel.getForm().reset();
    };
        
    
    // Model and Store for combobox of experimenter
    var experimenterStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url :  '/experiments/ajax/experimenter/',
            reader: {
                type: 'json',
                root: 'experimenters',
            }
        },
        fields: [
            {name:'experimenter', type: 'string'}
        ],
        autoLoad: true
    });

    var reagentMethodStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url :  '/experiments/ajax/display/Reagent_method/',
            reader: {
                type: 'json',
                root: 'Reagent_methods',
            }
        },
        fields: [
            {name:'Reagent_method', type: 'string'}
        ],
        autoLoad: true
    });
    // Model and Store for combobox of project
    var reagentBufferStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url :  '/experiments/ajax/display/Reagent_buffer/',
            reader: {
                type: 'json',
                root: 'Reagent_buffers',
            }
        },
        fields: [
            {name:'Reagent_buffer', type: 'string'}
        ],
        autoLoad: true
    });
    // Model and Store for combobox of project
    var projectStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url :  '/experiments/ajax/display/Project/',
            reader: {
                type: 'json',
                root: 'Projects',
            }
        },
        fields: [
            {name: 'Project', type: 'string'}
        ],
        autoLoad: true
    });

    var digestTypeStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url :  '/experiments/ajax/display/Digest_type/',
            reader: {
                type: 'json',
                root: 'Digest_types',
            }
        },
        fields: [
            {name: 'Digest_type', type: 'string'}
        ],
        autoLoad: true
    });

    var digestEnzymeStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url :  '/experiments/ajax/display/Digest_enzyme/',
            reader: {
                type: 'json',
                root: 'Digest_enzymes',
            }
        },
        fields: [
            {name: 'Digest_enzyme', type: 'string'}
        ],
        autoLoad: true
    });

    var instrumentManufacturerStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url :  '/experiments/ajax/display/Instrument_manufacturer/',
            reader: {
                type: 'json',
                root: 'Instrument_manufacturers',
            }
        },
        fields: [
            {name: 'Instrument_manufacturer', type: 'string'}
        ],
        autoLoad: true
    });

    var instrumentAdministratorStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url :  '/experiments/ajax/display/Instrument_administrator/',
            reader: {
                type: 'json',
                root: 'Instrument_administrators',
            }
        },
        fields: [
            {name: 'Instrument_administrator', type: 'string'}
        ],
        autoLoad: true
    });

    var separationMethodStore = Ext.create('Ext.data.Store', {
        proxy: {
            type: 'ajax',
            url :  '/experiments/ajax/display/Separation_method/',
            reader: {
                type: 'json',
                root: 'Separation_methods',
            }
        },
        fields: [
            {name: 'Separation_method', type: 'string'}
        ],
        autoLoad: true
    });

    // function: add a reagent panel to the formpanel
    var addReagent = function(index,reagentnum){
        var reagent = Ext.create( 'Ext.form.Panel',{
            title: 'REAGENT '+reagentnum,
            id : 'reagent'+reagentnum,
            border: true,
            frame: true,
            bodyStyle: 'padding: 10',
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
                    fieldLabel: 'Reagent No.',
                    displayField:'Reagent_no',
                    name:'reagent_no'+reagentnum,
                    store: Ext.create('Ext.data.Store',{
                        fields:[
                            {name:'reagent_no', type:'string'}
                        ],
                        proxy: {
                            type: 'ajax',
                            url :  '/experiments/ajax/reagent_no/',
                            reader: {
                                type: 'json',
                            }
                        }
                    }),
                    typeAhead: true
                },{
                    xtype:'textfield',
                    fieldLabel: 'Amount',
                    name: 'reagent_amount'+reagentnum
                },{
                    xtype: 'combobox',
                    fieldLabel: 'Method',
                    displayField:'Reagent_method',
                    name: 'Reagent_method'+reagentnum,
                    store: reagentMethodStore, 
                },{
                    xtype: 'combobox',
                    fieldLabel: 'Wash Buffer',
                    displayField:'Reagent_buffer',
                    name: 'Reagent_buffer'+reagentnum,
                    store: reagentBufferStore,
                },{
                    xtype: 'textareafield',
                    fieldLabel: 'Ajustments',
                    name: 'reagent_ajustments'+reagentnum,
                    allowBlank: true
                }]
        });
        formPanel.insert(index,reagent);
    };

    // function: add a  sample panel to the formpanel
    var addSample = function(index,samplenum){
        sample = Ext.create( 'Ext.form.Panel',{
            title: 'SAMPLE '+samplenum,
            id: 'sample'+samplenum,
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
                    fieldLabel: 'Sample No.',
                    displayField:'sample_no',
                    name:'sample_no'+samplenum,
                    store: Ext.create('Ext.data.Store',{
                        fields:[
                            {name:'sample_no', type:'string'}
                        ],
                        proxy: {
                            type: 'ajax',
                            url :  '/experiments/ajax/sample_no/',
                            reader: {
                                type: 'json',
                            }
                        }
                    }),
                    typeAhead: true,
                    listeners:{
                        change: function(combo, record, index){
                            Ext.Ajax.request({
                                url: '/experiments/data/sample_short/',
                                params: {
                                    id: combo.up().items.items[0].value,
                                    csrfmiddlewaretoken:csrftoken
                                },
                                success: function(response){
                                    var text = response.responseText;
                                    responseJson = Ext.JSON.decode(text);
                                    combo.up().items.items[1].setValue(responseJson.experimenter);
                                    combo.up().items.items[2].setValue(responseJson.date);
                                    combo.up().items.items[3].setValue(responseJson.txid);
                                    combo.up().items.items[4].setValue(responseJson.cell_tissue);
                                }
                            });
                        }
                    }

                },{
                    xtype: 'displayfield',
                    fieldLabel: 'Experimenter',
                    id: 'experimenter'+samplenum,
                    name: 'experimenter',
                    allowBlank: false
                },{
                    xtype: 'displayfield',
                    fieldLabel: 'Date',
                    id: 'date'+samplenum,
                    name: 'date'
                },{
                    xtype: 'displayfield',
                    fieldLabel: 'Taxon',
                    name: 'txid'+samplenum,
                    id: 'txid'+samplenum
                },{
                    xtype: 'displayfield',
                    fieldLabel: 'Cell/Tissue',
                    name: 'cell_tissue'+samplenum,
                    id: 'cell_tissue'+samplenum
                },{
                    xtype: 'textfield',
                    fieldLabel: 'Amount',
                    name: 'sample_amount'+samplenum
                },{
                    xtype: 'textareafield',
                    fieldLabel: 'Ajustments',
                    name: 'sample_ajustments'+samplenum,
                    allowBlank: true
                }]
        });
        formPanel.insert(index,sample);
    };
    
    var addSeparation = function(index, method_order){
        methodPanel = Ext.create( 'Ext.container.Container',{
            id: 'method'+method_order,
            //frame: true,
            layout: {
                type: 'hbox',
                align: 'stretch',
            },
            defaults:{
                labelWidth: 50,
                width: 200,
                bodyStyle:'padding:10',
            },
            items: [
                {
                    xtype: 'combobox',
                    fieldLabel: '#'+method_order,
                    displayField: 'Separation_method',
                    name: 'Separation_method'+method_order,
                    flex: 2,
                    store: separationMethodStore,
                    typeAhead: true
                },{
                    xtype: 'numberfield',
                    name: 'separation_num'+method_order,
                    minValue: 1,
                    flex:1
                }
            ],
        });
        separationPanel.insert(index, methodPanel);
    };


    //function used to delete a ragent panel from formpanel
    var delReagent = function(reagentnum){
        for( i = reagentnum; i>0; i--){
            reagent = Ext.getCmp('reagent'+i);
            formPanel.remove(reagent);
        }
    };


    //function used to delete a sample panel from formpanel
    var delSample = function(samplenum){
        for( i = samplenum; i>0; i--){
            sample = Ext.getCmp('sample'+i);
            formPanel.remove(sample);
        }
    };

    //function used to delete a separation method panel from separationPanel
    var delSeparation = function(methodnum){
        for( i = methodnum; i>0; i--){
            method = Ext.getCmp('method'+i);
            separationPanel.remove(method);
        }
    };

    //general panel for input general experiment information
    var generalPanel = Ext.create('Ext.form.Panel', {
        title: 'GENERAL',
        frame: true,
        headerPosition: 'left',
        bodyStyle: 'padding: 10;',
        defaults: {
            labelWidth: 120,
            labelAligh: 'left',
            width: 450,
            allowBlank: false,
            msgTarget: 'qtip'
        },
        items: [
            {
                xtype: 'textfield',
                fieldLabel: 'Experiment NO.',
                name:'experiment_no',
                readOnly: true
            },{
                xtype: 'datefield',
                fieldLabel: 'Date',
                name:'date'
            },{
                xtype: 'combobox',
                fieldLabel: 'Project',
                displayField:'Project',
                name: 'Project',
                store: projectStore,
                typeAhead: true
            },{
                xtype: 'numberfield',
                fieldLabel:'Sample Number', 
                id:'sample_num',
                name: 'sample_num',
                //hideTrigger: true,
                minValue: 0,
                maxValue: 10,
                listeners:{
                    change: function(o, newV, oldV){
                        if (oldV){
                            delSample(oldV);
                        }
                        for (i=1; i <= newV; i++) {
                            addSample(i,i);
                        }
                    }
                },
            },{
                xtype: 'numberfield',
                fieldLabel: 'Reagent Number',
                id: 'reagent_num',
                name: 'reagent_num',
                minValue: 0,
                maxValue: 10,
                listeners:{
                    change: function(o, newV, oldV){
                        sample_number = Ext.getCmp('sample_num');
                        index = sample_number.value;
                        if (oldV){
                            delReagent(oldV);
                        }
                        for (i=1; i <= newV; i++) {
                            addReagent(index+i, i);
                        }
                    }
                }
            },{
                xtype: 'hiddenfield',
                name: 'csrfmiddlewaretoken',
                value: csrftoken
            }]
    });


    //separation panel for input general experiment information
    var separationPanel = Ext.create( 'Ext.panel.Panel',{
        title: 'SEPARATION',
        frame: true,
        headerPosition: 'left',
        defaults: {
            labelWidth: 120,
            labelAligh: 'left',
            allowBlank: true,
            width: 450,
        },
        items: [
            {
                xtype:'combobox',
                fieldLabel:'Experimenter',
                displayField: 'experimenter',
                name: 'separation_experimenter',
                store: experimenterStore,
                typeAhead:true
            },{
                xtype: 'numberfield',
                fieldLabel: 'Separation Method Number',
                id: 'method_num',
                name: 'method_num',
                minValue: 0,
                maxValue: 10,
                listeners: {
                    change: function(o, newV, oldV){
                        if (oldV){
                            delSeparation(oldV);
                        }
                        for (i=1; i <= newV; i++) {
                            addSeparation(i+1, i);
                        }
                    }
                }
            },{
                xtype: 'textareafield',
                name: 'separation_ajustments',
                fieldLabel: 'Ajustments'
            }]
    });

    //digest panel for input general digest information
    var digestPanel = Ext.create( 'Ext.panel.Panel',{
        title: 'DIGEST',
        border: true,
        frame: true,
        headerPosition: 'left',
        defaults: {
            labelWidth: 120,
            labelAlign: 'left',
            allowBlank: true,
            width: 450,
        },
        items: [
            {
                xtype:'combobox',
                fieldLabel:'Experimenter',
                name: 'digest_experimenter',
                displayField: 'experimenter',
                store: experimenterStore,
                typeAhead: true
            },{
                xtype: 'combobox',
                fieldLabel: 'Type',
                name: 'Digest_type',
                displayField: 'Digest_type',
                store: digestTypeStore,
                queryMode: 'local',
                typeAhead: true
            },{
                xtype: 'combobox',
                fieldLabel: 'Enzyme',
                name: 'Digest_enzyme',
                displayField: 'Digest_enzyme',
                store: digestEnzymeStore,
                queryMode: 'local',
                typeAhead: true
            }]
    });

    // instrument related information
    var instrumentPanel = Ext.create('Ext.panel.Panel', {
        title: 'INSTRUMENT',
        border: true,
        frame: true,
        headerPosition: 'left',
        defaults: {
            labelWidth: 120,
            labelAlign: 'left',
            width: 450,
            allowBlank: true
        },
        items: [
            {
                xtype: 'textfield',
                fieldLabel: 'Instrument Name',
                name: 'instrument_name'
            },{
                xtype: 'combobox',
                fieldLabel: 'Administrator',
                name: 'Instrument_administrator',
                displayField: 'Instrument_administrator',
                store: instrumentAdministratorStore,
                typeAhead: true
            },{
                xtype: 'combobox',
                fieldLabel: 'Manufacturer',
                name: 'Instrument_manufacturer',
                displayField: 'Instrument_manufacturer',
                store: instrumentManufacturerStore,
            },{
                xtype: 'textfield',
                fieldLabel: 'Type',
                name: 'instrument_type'
            }]
    });

    // comment related information
    var commentPanel = Ext.create('Ext.panel.Panel', {
        title: 'COMMENT',
        frame: true,
        headerPosition: 'left',
        defaults: {
            labelWidth: 120,
            labelAlign: 'top',
            width: 450,
            allowBlank: true,
        },
        items: [
            {
                xtype: 'textareafield',
                fieldLabel: 'Experiment Description',
                name: 'description'
            },{
                xtype: 'textareafield',
                fieldLabel: 'Experiment Comments/Conclusions',
                name: 'comments_conclusions'
            }]
    });

    // button for submit of cancel form
    var buttonPanel = Ext.create('Ext.panel.Panel', {
        frame: true,
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
        id: 'formPanel',
        renderTo:'form',
        items: [generalPanel, separationPanel, digestPanel, instrumentPanel, commentPanel, buttonPanel],
    });

    sample_num = Ext.getCmp('sample_num');
    reagent_num = Ext.getCmp('reagent_num');
    samplenum = Ext.get('samplenum');
    reagentnum = Ext.get('reagentnum');
    sample_num.setValue(samplenum.getHTML());
    reagent_num.setValue(reagentnum.getHTML());
    no = Ext.get('no');


    formPanel.getForm().load({
        url: '/experiments/load/experiment/',
        method: 'POST',
        params: {
            experiment_no : no.getHTML(),
            csrfmiddlewaretoken:csrftoken
        },
    });

});
