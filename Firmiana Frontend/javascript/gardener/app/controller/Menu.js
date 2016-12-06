Ext.define('gar.controller.Menu', {
    extend: 'Ext.app.Controller',
    views: ['Menu', 'GlobalPlot', 'ReactomeTool'],
    init: function() {
        var required = '<span style="color:red;font-weight:bold" data-qtip="Required">*</span>';
        cloneActiveStore = function() {
            var grid = Ext.getCmp('content-panel').getActiveTab().down('grid')
            var store = Ext.getCmp('content-panel').getActiveTab().down('grid').getStore();
            var qpara = grid.filters.buildQuery(grid.filters.getFilterData());
            var cloneStore = new Ext.data.Store({
                // autoLoad :true,
                proxy: store.proxy,
                model: store.model,
                reader: store.reader,
                remoteFilter: true,
                pageSize: -1,
                listeners: {
                    beforeload: function(store, options) {
                        options.params = options.params || {};
                        Ext.apply(options.params, qpara);
                    }
                },
                getSym: function() {
                    var syms = [];
                    var count = this.getCount();
                    var record;
                    for (var i = 0; i < count; i++) {
                        record = this.getAt(i);
                        if (record.data.symbol) {
                            syms.push(record.data.symbol);
                        }
                    }
                    return syms
                }
            });
            return cloneStore
        }
        this.control({
            '#btdataexport': {
                click: function() {
                    //prompt dialog box
                    //Are you sure to down load this file?
                    //select a format, text or json
                    act = Ext.getCmp('content-panel').activeTab.items
                    // console.log(act.items[0].id)
                    if (String(act.items[0].id).indexOf('experiment') >= 0) {
                        data = Ext.getCmp(String(act.items[0].id)).filters.getFilterData()
                        var s = '?filter=[';
                        for (i = 0; i < data.length; i++) {
                            s += '{'
                            temp = String(Ext.encode(data[i].data))
                            s += temp.substr(1, temp.length - 2)
                            s += ',"field":"'
                            s += String(data[i].field)
                            s += '"}'
                            if (i != data.length - 1)
                                s += ','
                        }
                        s += ']'
                        window.open('/gardener/data/downdatabase/' + s);
                    } else if (String(act.items[0].id).indexOf('protein') >= 0) {
                        data = Ext.getCmp(String(act.items[0].id)).filters.getFilterData()
                        var s = '?filter=[';
                        for (i = 0; i < data.length; i++) {
                            s += '{'
                            temp = String(Ext.encode(data[i].data))
                            s += temp.substr(1, temp.length - 2)
                            s += ',"field":"'
                            s += String(data[i].field)
                            s += '"}'
                            if (i != data.length - 1)
                                s += ','
                        }
                        s += ']'
                        s += '&sid='
                        s += String(Ext.getCmp(String(act.items[0].id)).store.proxy.extraParams.sid)
                        s += '&stype='
                        s += String(Ext.getCmp(String(act.items[0].id)).store.proxy.extraParams.stype)
                        if (act.items[0].store.proxy.extraParams.stype == 'anywhere') {
                            s += '&symbol='
                            s += String(Ext.getCmp(String(act.items[0].id)).store.proxy.extraParams.symbol)
                        }
                        window.open('/gardener/data/downprotein/' + s);
                    } else if (String(act.items[0].id).indexOf('peptide') >= 0) {
                        data = Ext.getCmp(String(act.items[0].id)).filters.getFilterData()
                        var s = '?filter=[';
                        for (i = 0; i < data.length; i++) {
                            s += '{'
                            temp = String(Ext.encode(data[i].data))
                            s += temp.substr(1, temp.length - 2)
                            s += ',"field":"'
                            s += String(data[i].field)
                            s += '"}'
                            if (i != data.length - 1)
                                s += ','
                        }
                        s += ']'
                        s += '&sid='
                        s += String(Ext.getCmp(String(act.items[0].id)).store.proxy.extraParams.sid)
                        s += '&stype='
                        s += String(Ext.getCmp(String(act.items[0].id)).store.proxy.extraParams.stype)
                        window.open('/gardener/data/downpeptide/' + s);
                    } else if (String(act.items[0].id).indexOf('gene') >= 0) {
                        data = Ext.getCmp(String(act.items[0].id)).filters.getFilterData()
                        var s = '?filter=[';
                        for (i = 0; i < data.length; i++) {
                            s += '{'
                            temp = String(Ext.encode(data[i].data))
                            s += temp.substr(1, temp.length - 2)
                            s += ',"field":"'
                            s += String(data[i].field)
                            s += '"}'
                            if (i != data.length - 1)
                                s += ','
                        }
                        s += ']'
                        s += '&sid='
                        s += String(Ext.getCmp(String(act.items[0].id)).store.proxy.extraParams.sid)
                        s += '&stype='
                        s += String(Ext.getCmp(String(act.items[0].id)).store.proxy.extraParams.stype)
                        window.open('/gardener/data/downgene/' + s);
                    }
                }
            },
            '#addexperiment': {
                click: function() {
                	//(Ext.util.Cookies.get("username") != 'ChenDing') ||qiunq
                	var username = Ext.util.Cookies.get("username");
                    if(username == '') //ChenDing
                    {
                        Ext.Msg.alert("Sorry...","This tool is under maintenance until Monday.")
                    }
                    
                    else{

                        var choose_template_flag = false;
                        var panel = Ext.getCmp('add_exp_tab');
                        if (panel) {
                            var main = Ext.getCmp("content-panel");
                            main.setActiveTab(panel);
                            return 0;
                        }
                        var timestamp = 'compare' + (new Date()).valueOf();
                        var add_digest_type = function() {
                            var win = new Ext.Window({
                                title: 'ADD Digest Type',
                                width: 400,
                                items: [{
                                    xtype: 'form',
                                    border: true,
                                    // frame : true,
                                    id: 'type_form' + timestamp,
                                    items: [{
                                        xtype: 'textfield',
                                        labelWidth: 120,
                                        labelAligh: 'left',
                                        width: 450,
                                        fieldLabel: 'Type',
                                        name: 'Type'
                                    }]
                                }],
                                bbar: ['->', {
                                    text: 'Submit',
                                    handler: function() {
                                        var type_form = Ext.getCmp('type_form' + timestamp);
                                        var newV = type_form.items.items[0].value;
                                        digestTypeStore.add({
                                            Digest_type: newV
                                        });
                                        win.close();
                                    }
                                }]
                            });
                            win.show();
                        }
                        ;
                        var add_digest_enzyme = function() {
                            var win = new Ext.Window({
                                title: 'ADD Digest Enzyme',
                                width: 400,
                                items: [{
                                    xtype: 'form',
                                    border: true,
                                    // frame : true,
                                    id: 'enzyme_form' + timestamp,
                                    items: [{
                                        xtype: 'textfield',
                                        labelWidth: 120,
                                        labelAligh: 'left',
                                        width: 450,
                                        fieldLabel: 'Enzyme',
                                        name: 'Enzyme'
                                    }]
                                }],
                                bbar: ['->', {
                                    text: 'Submit',
                                    handler: function() {
                                        var enzyme_form = Ext.getCmp('enzyme_form' + timestamp);
                                        var newV = enzyme_form.items.items[0].value;
                                        digestEnzymeStore.add({
                                            Digest_enzyme: newV
                                        });
                                        win.close();
                                    }
                                }]
                            });
                            win.show();
                        }
                        ;
                        var add_project = function() {
                            var win = new Ext.Window({
                                title: 'ADD Project',
                                width: 400,
                                items: [{
                                    xtype: 'form',
                                    border: true,
                                    // frame : true,
                                    id: 'project_form' + timestamp,
                                    items: [{
                                        xtype: 'textfield',
                                        labelWidth: 120,
                                        labelAligh: 'left',
                                        width: 450,
                                        fieldLabel: 'Project',
                                        name: 'Project'
                                    }]
                                }],
                                bbar: ['->', {
                                    text: 'Submit',
                                    handler: function() {
                                        application_form = Ext.getCmp('project_form' + timestamp);
                                        var newV = application_form.items.items[0].value;
                                        projectStore.add({
                                            Project: newV
                                        });
                                        win.close();
                                    }
                                }]
                            });
                            win.show();
                        }
                        ;
                        // CSRF protection
                        csrftoken = Ext.util.Cookies.get('csrftoken');
                        Ext.QuickTips.init();
                        // function used to deal submit and cancel
                        // form
                        var submitForm = function() {
                            var form = formPanel.getForm();
                            console.log(form);
                            //var currentTime = Ext.Date.format(new Date(), 'n/d/Y');
                            //Ext.getCmp("gar.app.control.Menu.addexperimentId").items.items[2].setValue(currentTime);
                            if (form.isValid()) {
                                Ext.Ajax.timeout = 180000;
                                form.submit({
                                    url: '/experiments/save/experiment/',
                                    waitMsg: 'Adding Experiment......',
                                    //timeout : 300000,
                                    // standardSubmit :
                                    // true,
                                    success: function(frm, act) {
                                        Ext.Msg.alert('Success', 'Add an experiment successfully. Result is: ' + Ext.encode(act.result.msg));
                                    },
                                    failure: function(form, action) {
                                        Ext.Msg.alert('Failed', 'Add an experiment unsuccessfully. Contact admin.');
                                    }
                                })
                            }
                        }
                        ;
                        var cancelForm = function() {
                            formPanel.getForm().reset();
                        }
                        ;
                        // Model and Store for combobox of
                        // experimenter
                        /*
                         * var experimenterStore = Ext.create('Ext.data.Store', { proxy : { type : 'ajax', url :
                         * '/experiments/ajax/experimenter/', reader : { type : 'json', root : 'experimenters' } }, fields : [{
                         * name : 'experimenter', type : 'string' }], autoLoad : true });
                         */
                        var reagentMethodStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/display/Reagent_method/',
                                reader: {
                                    type: 'json',
                                    root: 'Reagent_methods'
                                }
                            },
                            fields: [{
                                name: 'Reagent_method',
                                type: 'string'
                            }],
                            autoLoad: true
                        });

                        var instrumentStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/display/Instrument/',
                                reader: {
                                    type: 'json',
                                    root: 'Instruments'
                                }
                            },
                            fields: [{
                                name: 'Instrument',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var MS1Store = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/instrument_ms1/',
                                reader: {
                                    type: 'json',
                                    root: 'Instrument_MS1'
                                }
                            },
                            fields: [{
                                name: 'Instrument_MS1',
                                type: 'string'
                            }]
                        });
                        var MS1tolStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/instrument_ms1_tol/',
                                reader: {
                                    type: 'json',
                                    root: 'Instrument_MS1_tol'
                                }
                            },
                            fields: [{
                                name: 'Instrument_MS1_tol',
                                type: 'string'
                            }]
                        });
                        var MS2Store = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/instrument_ms2/',
                                reader: {
                                    type: 'json',
                                    root: 'Instrument_MS2'
                                }
                            },
                            fields: [{
                                name: 'Instrument_MS2',
                                type: 'string'
                            }]
                        });
                        var MS2tolStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/instrument_ms2_tol/',
                                reader: {
                                    type: 'json',
                                    root: 'Instrument_MS2_tol'
                                }
                            },
                            fields: [{
                                name: 'Instrument_MS2_tol',
                                type: 'string'
                            }]
                        });
                        // Model and Store for combobox of project
                        var reagentBufferStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/display/Reagent_buffer/',
                                reader: {
                                    type: 'json',
                                    root: 'Reagent_buffers'
                                }
                            },
                            fields: [{
                                name: 'Reagent_buffer',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        // Model and Store for combobox of project
                        var projectStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/display/Project/',
                                reader: {
                                    type: 'json',
                                    root: 'Projects'
                                }
                            },
                            fields: [{
                                name: 'Project',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var expTypeStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/display/Experiment_type/',
                                reader: {
                                    type: 'json',
                                    root: 'Experiment_types'
                                }
                            },
                            fields: [{
                                name: 'Experiment_type',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var digestTypeStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/display/Digest_type/',
                                reader: {
                                    type: 'json',
                                    root: 'Digest_types'
                                }
                            },
                            fields: [{
                                name: 'Digest_type',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var digestEnzymeStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/display/Digest_enzyme/',
                                reader: {
                                    type: 'json',
                                    root: 'Digest_enzymes'
                                }
                            },
                            fields: [{
                                name: 'Digest_enzyme',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var workflowModeStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/display/Workflow_mode/',
                                reader: {
                                    type: 'json',
                                    root: 'Workflow_modes'
                                }
                            },
                            fields: [{
                                name: 'Workflow_mode',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var searchEngineStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/display/searchEngine/',
                                reader: {
                                    type: 'json',
                                    root: 'searchEngines'
                                }
                            },
                            fields: [{
                                name: 'searchEngine',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var searchDatabaseStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/display/Search_database/',
                                reader: {
                                    type: 'json',
                                    root: 'Search_databases'
                                }
                            },
                            fields: [{
                                name: 'Search_database',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var instrumentManufacturerStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/display/Instrument_manufacturer/',
                                reader: {
                                    type: 'json',
                                    root: 'Instrument_manufacturers'
                                }
                            },
                            fields: [{
                                name: 'Instrument_manufacturer',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var companyStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/all_company/',
                                reader: {
                                    type: 'json',
                                    root: 'all_company'
                                }
                            },
                            fields: [{
                                name: 'company',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var labStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/all_lab/',
                                reader: {
                                    type: 'json',
                                    root: 'all_lab'
                                }
                            },
                            fields: [{
                                name: 'lab',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var experimenterStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/all_experimenter/',
                                reader: {
                                    type: 'json',
                                    root: 'experimenters'
                                }
                            },
                            fields: [{
                                name: 'experimenter',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var separationMethodStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/display/Separation_md/',
                                reader: {
                                    type: 'json',
                                    root: 'Separation_mds'
                                }
                            },
                            fields: [{
                                name: 'Separation_md',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var fixedModificationStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/display/Fixed_Modification/',
                                reader: {
                                    type: 'json',
                                    root: 'Fixed_Modifications'
                                }
                            },
                            fields: [{
                                name: 'Fixed_Modification',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var dynamicModificationStore = Ext.create('Ext.data.Store', {
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/display/Dynamic_Modification/',
                                reader: {
                                    type: 'json',
                                    root: 'Dynamic_Modifications'
                                }
                            },
                            fields: [{
                                name: 'Dynamic_Modification',
                                type: 'string'
                            }],
                            autoLoad: true
                        });
                        var quantificationMethodsStore = Ext.create('Ext.data.Store', {
                            // proxy: {
                            //     type: 'ajax',
                            //     url: '/experiments/ajax/display/Quantification_Method/',
                            //     reader: {
                            //         type: 'json',
                            //         root: 'Quantification_Methods'
                            //     }
                            // },
                            fields: [{
                                name: 'quantificationMethod',
                                type: 'string'
                            }],
                            data: [
                            {quantificationMethod: 'Label-free'},
                            {quantificationMethod: 'Labeled (SILAC)'},
                            {quantificationMethod: 'Labeled (iTRAQ)'},
                            {quantificationMethod: 'Labeled (TMT)'}
                            ],
                            autoLoad: true
                        });
                        // function: add a reagent panel to the
                        // formpanel
                        var addReagent = function(index, reagentnum) {
                            var reagent = Ext.create('Ext.form.Panel', {
                                title: 'Reagent ' + reagentnum,
                                //id : 'reagent' + reagentnum + timestamp,
                                id: 'addexperiment_reagent_no' + reagentnum,
                                border: true,
                                // frame : true,
                                bodyPadding: 10,
                                headerPosition: 'left',
                                defaults: {
                                    labelWidth: 120,
                                    labelAligh: 'left',
                                    width: 450,
                                    allowBlank: false
                                },
                                items: [{
                                    xtype: 'combobox',
                                    fieldLabel: 'Reagent No.',
                                    displayField: 'reagent_no',
                                    name: 'reagent_no' + reagentnum,
                                    id: 'addexperiment_combobox_reagent_no' + reagentnum,
                                    editable: false,
                                    store: Ext.create('Ext.data.Store', {
                                        fields: [{
                                            name: 'reagent_no',
                                            type: 'string'
                                        }],
                                        proxy: {
                                            type: 'ajax',
                                            url: '/experiments/ajax/reagent_no/',
                                            reader: {
                                                type: 'json'
                                            }
                                        }
                                    }),
                                    typeAhead: true,
                                    listeners: {
                                        select: function(combo, record, index) {
                                            Ext.Ajax.request({
                                                url: '/experiments/data/reagent_short/',
                                                params: {
                                                    id: combo.up().items.items[0].value,
                                                    csrfmiddlewaretoken: csrftoken
                                                },
                                                success: function(response) {
                                                    var text = response.responseText;
                                                    responseJson = Ext.JSON.decode(text);
                                                    combo.up().items.items[1].setValue(responseJson.experimenter);
                                                    combo.up().items.items[2].setValue(responseJson.date);
                                                    combo.up().items.items[3].setValue(responseJson.name);
                                                    combo.up().items.items[4].setValue(responseJson.manufacturer);
                                                    combo.up().items.items[5].setValue(responseJson.catalog_no);
                                                    combo.up().items.items[6].setValue(responseJson.type);
                                                }
                                            });
                                        },
                                        beforeselect: function(combo, record, index) {
                                            console.log("fire before select");
                                            if (choose_template_flag) {
                                                console.log("choose");
                                            } 
                                            else {
                                                console.log("don't choose");
                                            }
                                        
                                        }
                                    }
                                }, {
                                    xtype: 'displayfield',
                                    fieldLabel: 'Experimenter',
                                    id: 'rea-experimenter' + reagentnum + timestamp,
                                    allowBlank: false
                                }, {
                                    xtype: 'displayfield',
                                    fieldLabel: 'Date',
                                    id: 'rea-date' + reagentnum + timestamp,
                                    name: 'date'
                                }, {
                                    xtype: 'displayfield',
                                    fieldLabel: 'Name',
                                    id: 'rea-name' + reagentnum + timestamp,
                                    allowBlank: false
                                }, {
                                    xtype: 'displayfield',
                                    fieldLabel: 'manufacturer',
                                    id: 'rea-manu' + reagentnum + timestamp
                                }, {
                                    xtype: 'displayfield',
                                    fieldLabel: 'catalog_no',
                                    id: 'rea-cata' + reagentnum + timestamp
                                }, {
                                    xtype: 'displayfield',
                                    fieldLabel: 'Type',
                                    id: 'rea-type' + reagentnum + timestamp
                                }, {
                                    xtype: 'fieldcontainer',
                                    layout: {
                                        type: 'hbox',
                                        align: 'stretch'
                                    },
                                    items: [{
                                        xtype: 'textfield',
                                        fieldLabel: 'Amount',
                                        labelWidth: 120,
                                        name: 'reagent_amount' + reagentnum
                                    }, {
                                        xtype: 'combobox',
                                        width: 80,
                                        name: 'reagent_unit' + reagentnum,
                                        displayField: 'Rx_unit_detail',
                                        store: Ext.create('Ext.data.Store', {
                                            fields: [{
                                                name: 'Rx_unit_detail',
                                                type: 'string'
                                            }],
                                            proxy: {
                                                type: 'ajax',
                                                url: '/experiments/ajax/display/Rx_unit_detail/',
                                                reader: {
                                                    type: 'json',
                                                    root: 'Rx_unit_details'
                                                }
                                            }
                                        })
                                    }]
                                }, {
                                    xtype: 'combobox',
                                    fieldLabel: 'Method',
                                    displayField: 'Reagent_method',
                                    name: 'Reagent_method' + reagentnum,
                                    store: reagentMethodStore
                                }, {
                                    xtype: 'combobox',
                                    fieldLabel: 'Wash Buffer',
                                    displayField: 'Reagent_buffer',
                                    name: 'Reagent_buffer' + reagentnum,
                                    store: reagentBufferStore
                                }, {
                                    xtype: 'textareafield',
                                    fieldLabel: 'Adjustments',
                                    name: 'reagent_ajustments' + reagentnum,
                                    allowBlank: true
                                }]
                            });
                            formPanel.insert(index, reagent);
                        }
                        ;
                        // function: add a sample panel to the
                        // formpanel
                        var addSample = function(index, samplenum) {
                            var sample = Ext.create('Ext.form.Panel', {
                                title: 'Sample ' + samplenum,
                                //id : 'sample' + samplenum + timestamp,
                                id: 'addexperiment_sample_no' + samplenum,
                                border: true,
                                // frame : true,
                                bodyPadding: 10,
                                headerPosition: 'left',
                                defaults: {
                                    labelWidth: 120,
                                    labelAligh: 'left',
                                    width: 450,
                                    allowBlank: false
                                },
                                items: [{
                                    xtype: 'combobox',
                                    fieldLabel: 'Sample No.',
                                    displayField: 'sample_no',
                                    name: 'sample_no' + samplenum,
                                    id: 'addexperiment_combobox_sample_no' + samplenum,
                                    editable: false,
                                    store: Ext.create('Ext.data.Store', {
                                        fields: [{
                                            name: 'sample_no',
                                            type: 'string'
                                        }],
                                        proxy: {
                                            type: 'ajax',
                                            url: '/experiments/ajax/sample_no/',
                                            reader: {
                                                type: 'json'
                                            }
                                        }
                                    }),
                                    typeAhead: true,
                                    listeners: {
                                        select: function(combo, record, index) {
                                            Ext.Ajax.request({
                                                url: '/experiments/data/sample_short/',
                                                params: {
                                                    id: combo.up().items.items[0].value,
                                                    csrfmiddlewaretoken: csrftoken
                                                },
                                                success: function(response) {
                                                    var text = response.responseText;
                                                    responseJson = Ext.JSON.decode(text);
                                                    combo.up().items.items[1].setValue(responseJson.experimenter);
                                                    combo.up().items.items[2].setValue(responseJson.date);
                                                    combo.up().items.items[3].setValue(responseJson.source_type);
                                                    combo.up().items.items[4].setValue(responseJson.txid);
                                                    combo.up().items.items[5].setValue(responseJson.source_strain);
                                                    combo.up().items.items[6].setValue(responseJson.source_genotype);
                                                    combo.up().items.items[7].setValue(responseJson.source_change);
                                                    combo.up().items.items[8].setValue(responseJson.rx);
                                                }
                                            });
                                        }
                                    }
                                }, {
                                    xtype: 'displayfield',
                                    fieldLabel: 'Experimenter',
                                    id: 'experimenter' + samplenum + timestamp,
                                    name: 'experimenter',
                                    allowBlank: false
                                }, {
                                    xtype: 'displayfield',
                                    fieldLabel: 'Date',
                                    id: 'date' + samplenum + timestamp,
                                    name: 'date'
                                }, {
                                    xtype: 'displayfield',
                                    fieldLabel: 'Type',
                                    name: 'txtype' + samplenum,
                                    id: 'txtype' + samplenum + timestamp
                                }, {
                                    xtype: 'displayfield',
                                    fieldLabel: 'Taxon',
                                    name: 'txid' + samplenum,
                                    id: 'txid' + samplenum + timestamp
                                }, {
                                    xtype: 'displayfield',
                                    fieldLabel: 'Strain',
                                    name: 'txstrain' + samplenum,
                                    id: 'txstrain' + samplenum + timestamp
                                }, {
                                    xtype: 'displayfield',
                                    fieldLabel: 'Genotype',
                                    name: 'txgenotype' + samplenum,
                                    id: 'txgenotype' + samplenum + timestamp
                                }, {
                                    xtype: 'displayfield',
                                    fieldLabel: 'Target Gene',
                                    name: 'txtarget' + samplenum,
                                    id: 'txtarget' + samplenum + timestamp
                                }, {
                                    xtype: 'displayfield',
                                    fieldLabel: 'Treatment',
                                    name: 'txtreat' + samplenum,
                                    id: 'txtreat' + samplenum + timestamp
                                }, {
                                    xtype: 'fieldcontainer',
                                    layout: {
                                        type: 'hbox',
                                        align: 'stretch'
                                    },
                                    items: [{
                                        xtype: 'textfield',
                                        fieldLabel: 'Amount',
                                        labelWidth: 120,
                                        name: 'sample_amount' + samplenum
                                    }, {
                                        xtype: 'combobox',
                                        width: 80,
                                        name: 'sample_unit' + samplenum,
                                        displayField: 'Rx_unit_detail',
                                        store: Ext.create('Ext.data.Store', {
                                            fields: [{
                                                name: 'Rx_unit_detail',
                                                type: 'string'
                                            }],
                                            proxy: {
                                                type: 'ajax',
                                                url: '/experiments/ajax/display/Rx_unit_detail/',
                                                reader: {
                                                    type: 'json',
                                                    root: 'Rx_unit_details'
                                                }
                                            }
                                        })
                                    }]
                                }, {
                                    xtype: 'textareafield',
                                    fieldLabel: 'Adjustments',
                                    name: 'sample_ajustments' + samplenum,
                                    allowBlank: true
                                }]
                            });
                            formPanel.insert(index, sample);
                        }
                        ;
                        var addSeparation = function(index, method_order) {
                            var methodPanel = Ext.create('Ext.container.Container', {
                                id: 'method' + method_order + timestamp,
                                // frame: true,
                                layout: {
                                    type: 'hbox',
                                    align: 'stretch'
                                },
                                defaults: {
                                    labelWidth: 120,
                                    width: 100,
                                    bodyStyle: 'padding:10'
                                },
                                items: [{
                                    xtype: 'combobox',
                                    emptyText: 'Name',
                                    fieldLabel: '#' + method_order,
                                    displayField: 'Separation_md',
                                    name: 'separation_method' + method_order,
                                    flex: 2,
                                    store: separationMethodStore,
                                    typeAhead: true
                                }, {
                                    xtype: 'textfield',
                                    name: 'separation_source' + method_order,
                                    emptyText: 'Source'
                                }, {
                                    xtype: 'textfield',
                                    name: 'separation_size' + method_order,
                                    emptyText: 'Size'
                                }, {
                                    xtype: 'textfield',
                                    name: 'separation_buffer' + method_order,
                                    emptyText: 'Buffer'
                                }, {
                                    xtype: 'textfield',
                                    name: 'separation_others' + method_order,
                                    emptyText: 'PH/others'
                                }/*
                                                     * , { xtype : 'numberfield', name : 'separation_num' + method_order,
                                                     * minValue : 1, flex : 1 }
                                                     */]
                            });
                            separationPanel.insert(index, methodPanel);
                        }
                        ;
                        // function used to delete a ragent panel
                        // from formpanel
                        var delReagent = function(reagentnum) {
                            for (i = reagentnum; i > 0; i--) {
                                //var reagent = Ext.getCmp('reagent' + i + timestamp);
                                var reagent = Ext.getCmp('addexperiment_reagent_no' + i);
                                formPanel.remove(reagent);
                            }
                        }
                        ;
                        // function used to delete a sample panel
                        // from formpanel
                        var delSample = function(samplenum) {
                            for (i = samplenum; i > 0; i--) {
                                //var sample = Ext.getCmp('sample' + i + timestamp);
                                var sample = Ext.getCmp('addexperiment_sample_no' + i);
                                formPanel.remove(sample);
                            }
                        }
                        ;
                        // function used to delete a separation
                        // method panel from
                        // separationPanel
                        var delSeparation = function(methodnum) {
                            for (i = methodnum; i > 0; i--) {
                                var method = Ext.getCmp('method' + i + timestamp);
                                separationPanel.remove(method);
                            }
                        }
                        ;
                        // general panel for input general
                        // experiment information
                        
                        var experimentTemplateStore = Ext.create('Ext.data.Store', {
                            fields: [{
                                name: 'experiment_no',
                                type: 'string'
                            }],
                            proxy: {
                                type: 'ajax',
                                url: '/experiments/ajax/experiment_no/',
                                reader: {
                                    type: 'json',
                                    root: 'experiment_no'
                                }
                            },
                            autoLoad: true
                        });
                        
                        //function: combobox_reloadReagentInfo
                        var combobox_reloadReagentInfo = function(combo, value) {
                            combo.items.items[0].setValue(value);
                            Ext.Ajax.request({
                                url: '/experiments/data/reagent_short/',
                                params: {
                                    id: combo.items.items[0].value,
                                    csrfmiddlewaretoken: csrftoken
                                },
                                success: function(response) {
                                    var text = response.responseText;
                                    var reagent_responseJson = Ext.JSON.decode(text);
                                    combo.items.items[1].setValue(reagent_responseJson.experimenter);
                                    combo.items.items[2].setValue(reagent_responseJson.date);
                                    combo.items.items[3].setValue(reagent_responseJson.name);
                                    combo.items.items[4].setValue(reagent_responseJson.manufacturer);
                                    combo.items.items[5].setValue(reagent_responseJson.catalog_no);
                                    combo.items.items[6].setValue(reagent_responseJson.type);
                                }
                            });
                        }
                        
                        //function: combobox_reloadReagentInfo
                        var combobox_reloadSampleInfo = function(combo, value) {
                            combo.items.items[0].setValue(value);
                            Ext.Ajax.request({
                                url: '/experiments/data/sample_short/',
                                params: {
                                    id: combo.items.items[0].value,
                                    csrfmiddlewaretoken: csrftoken
                                },
                                success: function(response) {
                                    var text = response.responseText;
                                    var sample_responseJson = Ext.JSON.decode(text);
                                    combo.items.items[1].setValue(sample_responseJson.experimenter);
                                    combo.items.items[2].setValue(sample_responseJson.date);
                                    combo.items.items[3].setValue(sample_responseJson.source_type);
                                    combo.items.items[4].setValue(sample_responseJson.txid);
                                    combo.items.items[5].setValue(sample_responseJson.source_strain);
                                    combo.items.items[6].setValue(sample_responseJson.source_genotype);
                                    combo.items.items[7].setValue(sample_responseJson.source_change);
                                    combo.items.items[8].setValue(sample_responseJson.rx);
                                }
                            });
                        }
                        
                        
                        
                        var generalPanel = Ext.create('Ext.form.Panel', {
                            title: 'General',
                            // frame : true,
                            id: "gar.app.control.Menu.addexperimentId",
                            headerPosition: 'top',
                            // autoHeight: true,
                            bodyPadding: 10,
                            defaults: {
                                labelWidth: 120,
                                labelAligh: 'left',
                                width: 1000,
                                allowBlank: false,
                                msgTarget: 'side'
                            },
                            items: [{
                                xtype: 'combobox',
                                fieldLabel: 'Choose template',
                                displayField: 'experiment_no',
                                name: 'experiment-template',
                                store: experimentTemplateStore,
                                // queryModel : true,
                                //typeAhead : true,
                                queryMode: 'local',
                                editable: true,
                                width: 805,
                                allowBlank: true,
                                listeners: {
                                    select: function() {
                                        var cmpLocation = Ext.getCmp("gar.app.control.Menu.addexperimentId");
                                        var templateNo = cmpLocation.items.items[0].value;
                                        console.log(templateNo);
                                        choose_template_flag = true;
                                        Ext.Ajax.request({
                                            url: '/experiments/loadnew/experiment/',
                                            //url : '/experiments/load/experiment/',
                                            params: {
                                                experiment_no: templateNo
                                                // csrfmiddlewaretoken : csrftoken
                                            },
                                            success: function(response) {
                                                var text = response.responseText;
                                                responseJson = Ext.JSON.decode(text).data;
                                                
                                                Ext.getCmp('add_exp_tab').items.items[0].getForm().load({
                                                    url: '/experiments/loadnew/experiment/',
                                                    //url : '/experiments/load/experiment/',
                                                    method: 'POST',
                                                    params: {
                                                        experiment_no: templateNo
                                                    }
                                                });
                                                
                                                /////////////////////////
                                                //sample
                                                if (responseJson.sample_num > 0) {
                                                    
                                                    var length = responseJson.sample_num;
                                                    var index = 0;
                                                    var id_name = "addexperiment_sample_no";
                                                    
                                                    for (var i = 1; i <= length; i++) {
                                                        addSample(index + i, i);
                                                        console.log("add_exp_add-sample" + i);
                                                    }
                                                    
                                                    for (index; index < length; index++) {
                                                        var temp = index + 1;
                                                        id_name = id_name + temp;
                                                        var combo = Ext.getCmp(id_name);
                                                        var value = responseJson.sampleNoList[index];
                                                        if (combo) {
                                                            console.log("sample combobox exist");
                                                            combobox_reloadSampleInfo(combo, value);
                                                        } 
                                                        else {
                                                            console.log("sample combobox don't exist");
                                                        }
                                                        //Ext.getCmp(id_name).items.items[0].setValue(responseJson.reagentNoList[index]);
                                                        
                                                        id_name = "addexperiment_sample_no";
                                                    }
                                                }
                                                
                                                
                                                //reagent
                                                if (responseJson.reagent_num > 0) {
                                                    
                                                    var length = responseJson.reagent_num;
                                                    var index = 0;
                                                    var id_name = "addexperiment_reagent_no";
                                                    
                                                    sample_number = Ext.getCmp('sample_num' + timestamp);
                                                    index = sample_number.value;
                                                    for (var i = 1; i <= length; i++) {
                                                        addReagent(index + i, i);
                                                        console.log("add_exp_add-reagent" + i);
                                                    }
                                                    
                                                    for (index; index < length; index++) {
                                                        var temp = index + 1;
                                                        id_name = id_name + temp;
                                                        var combo = Ext.getCmp(id_name);
                                                        var value = responseJson.reagentNoList[index];
                                                        if (combo) {
                                                            console.log("reagent combobox exist");
                                                            combobox_reloadReagentInfo(combo, value);
                                                        } 
                                                        else {
                                                            console.log("reagent combobox don't exist");
                                                        }
                                                        //Ext.getCmp(id_name).items.items[0].setValue(responseJson.reagentNoList[index]);
                                                        
                                                        id_name = "addexperiment_reagent_no";
                                                    }
                                                }
                                                
                                                //seperation
                                                var pre_separation_methods = responseJson.pre_separation_methods;
                                                var pre_separation_methods_cmp = Ext.getCmp("pre_separation_methods");
                                                if (pre_separation_methods == "Online") {
                                                    pre_separation_methods_cmp.items.items[0].setValue(true);
                                                } 
                                                else if (pre_separation_methods == "Offline") {
                                                    pre_separation_methods_cmp.items.items[1].setValue(true);
                                                } 
                                                else {
                                                    pre_separation_methods_cmp.items.items[2].setValue(true);
                                                }
                                                
                                                /////////////////////////
                                            }
                                        });
                                        //ajax
                                    
                                    
                                    
                                    
                                    
                                    }
                                }
                            }, {
                                fieldLabel: 'Experimenter',
                                afterLabelTextTpl: required,
                                xtype: 'fieldcontainer',
                                layout: {
                                    type: 'hbox',
                                    align: 'stretch'
                                },
                                defaults: {
                                    allowBlank: false,
                                    editable: false,
                                    msgTarget: 'side'
                                },
                                items: [{
                                    xtype: 'combobox',
                                    displayField: 'company',
                                    name: 'company',
                                    valueField: 'company',
                                    store: companyStore,
                                    queryMode: 'local',
                                    emptyText: 'Company',
                                    width: 300,
                                    listeners: {
                                        select: {
                                            fn: function(combo, records, index) {
                                                var lab = Ext.getCmp("exp-lab");
                                                lab.clearValue();
                                                lab.store.load({
                                                    params: {
                                                        id: records[0].data.company
                                                    }
                                                })
                                            }
                                        }
                                    }
                                }, {
                                    xtype: 'combobox',
                                    displayField: 'lab',
                                    valueField: 'lab',
                                    name: 'lab',
                                    id: 'exp-lab',
                                    emptyText: 'Laboratory',
                                    store: labStore,
                                    queryMode: 'local',
                                    width: 200,
                                    listeners: {
                                        select: {
                                            fn: function(combo, records, index) {
                                                var experimenter = Ext.getCmp("exp-experimenter");
                                                experimenter.clearValue();
                                                experimenter.store.load({
                                                    params: {
                                                        id: records[0].data.lab
                                                    }
                                                })
                                            }
                                        }
                                    }
                                }, {
                                    xtype: 'combobox',
                                    displayField: 'experimenter',
                                    valueField: 'experimenter',
                                    emptyText: 'Experimenter',
                                    name: 'experimenter',
                                    id: 'exp-experimenter',
                                    store: experimenterStore,
                                    queryMode: 'local',
                                    width: 180
                                }]
                            }, {
                                xtype: 'datefield',
                                fieldLabel: 'Date',
                                value: Ext.Date.format(new Date(), 'n/d/Y'),
                                afterLabelTextTpl: required,
                                width: 450,
                                name: 'date',
                                listeners: {
                                    "select": function(field, value) {
                                        var cmpLocation = Ext.getCmp("gar.app.control.Menu.addexperimentId");
                                        cmpLocation.items.items[2].setValue(value);
                                    }
                                }
                            }, {
                                xtype: 'fieldcontainer',
                                layout: {
                                    type: 'hbox',
                                    align: 'stretch'
                                },
                                defaults: {
                                    allowBlank: false,
                                    msgTarget: 'side',
                                    width: 300
                                },
                                items: [{
                                    xtype: 'textfield',
                                    fieldLabel: 'Funding',
                                    afterLabelTextTpl: required,
                                    name: 'Funding',
                                    emptyText: 'Fund',
                                    labelWidth: 120
                                }, {
                                    xtype: 'textfield',
                                    fieldLabel: 'Project',
                                    name: 'Project',
                                    emptyText: 'Project',
                                    labelWidth: 60
                                }, {
                                    xtype: 'textfield',
                                    name: 'PI',
                                    emptyText: 'PI Name',
                                    fieldLabel: 'PI Name',
                                    labelWidth: 60
                                }]
                            }, {
                                xtype: 'fieldcontainer',
                                layout: {
                                    type: 'hbox',
                                    align: 'stretch'
                                },
                                items: [{
                                    xtype: 'textfield',
                                    fieldLabel: 'Execution',
                                    name: 'SubProject',
                                    emptyText: 'SubProject',
                                    labelWidth: 120,
                                    width: 300
                                }, {
                                    xtype: 'textfield',
                                    name: 'Subject',
                                    fieldLabel: 'Subject',
                                    emptyText: 'Subject',
                                    labelWidth: 60,
                                    width: 300
                                }, {
                                    xtype: 'textfield',
                                    name: 'Manager',
                                    emptyText: 'Manager Name',
                                    fieldLabel: 'Manager',
                                    queryMode: 'local',
                                    labelWidth: 60,
                                    width: 300
                                }]
                            }, {
                                xtype: 'combobox',
                                fieldLabel: 'Experiment_type',
                                displayField: 'Experiment_type',
                                afterLabelTextTpl: required,
                                name: 'Experiment_type',
                                store: expTypeStore,
                                typeAhead: true,
                                width: 240
                            }, {
                                xtype: 'numberfield',
                                fieldLabel: 'Total number of Sample',
                                afterLabelTextTpl: required,
                                id: 'sample_num' + timestamp,
                                name: 'sample_num',
                                minValue: 0,
                                maxValue: 10,
                                value: 0,
                                listeners: {
                                    change: function(o, newV, oldV) {
                                        if (newV > 10) {
                                            alert('Number of sample must be smaller than 10!')
                                            newV = 1
                                            Ext.getCmp('sample_num' + timestamp).setValue(1)
                                        }
                                        if (oldV) {
                                            delSample(oldV);
                                        }
                                        for (i = 1; i <= newV; i++) {
                                            //alert("just a test")
                                            addSample(i, i);
                                        }
                                    }
                                },
                                width: 240
                            }, {
                                xtype: 'numberfield',
                                fieldLabel: 'Total number of Reagent',
                                // afterLabelTextTpl: required,
                                id: 'reagent_num' + timestamp,
                                name: 'reagent_num',
                                minValue: 0,
                                maxValue: 10,
                                value: 0,
                                allowblank: true,
                                listeners: {
                                    change: function(o, newV, oldV) {
                                        if (newV > 10) {
                                            alert('Number of sample must be smaller than 10!')
                                            newV = 1
                                            Ext.getCmp('reagent_num' + timestamp).setValue(1)
                                        }
                                        sample_number = Ext.getCmp('sample_num' + timestamp);
                                        index = sample_number.value;
                                        console.log("index:" + index);
                                        if (oldV) {
                                            delReagent(oldV);
                                        }
                                        for (i = 1; i <= newV; i++) {
                                            addReagent(index + i, i);
                                            console.log("add_exp_add-reagent" + i);
                                        }
                                    }
                                },
                                width: 240
                            }, {
                                xtype: 'hiddenfield',
                                name: 'csrfmiddlewaretoken',
                                value: csrftoken
                            }, {
                                xtype: 'hiddenfield',
                                name: 'timestamp',
                                value: timestamp
                            }]
                        });
                        // separation panel for input general
                        // experiment information
                        var separationPanel = Ext.create('Ext.panel.Panel', {
                            title: 'Pre-Separation',
                            // frame : true,
                            name: "separationPanel",
                            headerPosition: 'top',
                            bodyPadding: 10,
                            defaults: {
                                labelWidth: 120,
                                labelAligh: 'left',
                                allowBlank: true,
                                width: 1000
                            },
                            items: [{
                                xtype: 'radiogroup',
                                fieldLabel: 'Methods',
                                name: 'separ_methods',
                                id: 'pre_separation_methods',
                                columns: 10,
                                vertical: true,
                                items: [{
                                    boxLabel: 'Online',
                                    name: 'separ_methods',
                                    inputValue: 'Online',
                                    checked: true
                                }, {
                                    boxLabel: 'Offline',
                                    name: 'separ_methods',
                                    inputValue: 'Offline'
                                }, {
                                    boxLabel: 'None',
                                    name: 'separ_methods',
                                    inputValue: 'None'
                                }]
                            }, {
                                width: 240,
                                xtype: 'numberfield',
                                fieldLabel: 'Separation Method Number',
                                id: 'method_num' + timestamp,
                                name: 'method_num',
                                value: 0,
                                minValue: 0,
                                maxValue: 10,
                                listeners: {
                                    change: function(o, newV, oldV) {
                                        if (oldV) {
                                            delSeparation(oldV);
                                        }
                                        for (i = 1; i <= newV; i++) {
                                            addSeparation(i + 1, i);
                                            // it's
                                            // not
                                            // perfect
                                        }
                                    }
                                }
                            }, {
                                xtype: 'textareafield',
                                name: 'separation_ajustments',
                                fieldLabel: 'Adjustments'
                            }]
                        });
                        // digest panel for input general digest
                        // information
                        var digestPanel = Ext.create('Ext.panel.Panel', {
                            title: 'Digest',
                            border: true,
                            // frame : true,
                            bodyPadding: 10,
                            headerPosition: 'top',
                            defaults: {
                                labelWidth: 120,
                                afterLabelTextTpl: required,
                                labelAlign: 'left',
                                allowBlank: false,
                                width: 450,
                                editable: false,
                                msgTarget: 'side'
                            },
                            items: [{
                                xtype: 'combobox',
                                fieldLabel: 'Type',
                                name: 'Digest_type',
                                displayField: 'Digest_type',
                                store: digestTypeStore,
                                queryMode: 'local',
                                typeAhead: true
                            }, {
                                xtype: 'combobox',
                                fieldLabel: 'Enzyme',
                                name: 'Digest_enzyme',
                                displayField: 'Digest_enzyme',
                                value: 'Trypsin',
                                store: digestEnzymeStore,
                                queryMode: 'local',
                                typeAhead: true
                            }]
                        });

                        // mode panel: choose workflow or import from elsewhere
                        var modePanel = Ext.create('Ext.panel.Panel', {
                            title: 'Mode',
                            border: true,
                            // frame : true,
                            bodyPadding: 10,
                            headerPosition: 'top',
                            defaults: {
                                labelWidth: 120,
                                // afterLabelTextTpl: required,
                                labelAlign: 'left',
                                // allowBlank: false,
                                // width: 450,
                                editable: false,
                                msgTarget: 'side'
                            },
                            items: [{
                                xtype: 'combobox',
                                fieldLabel: 'Mode',
                                name: 'workflowMode',
                                displayField: 'Workflow_mode',
                                value: 'FTP',
                                store: workflowModeStore,
                                // queryMode: 'local',
                                typeAhead: true,
                                listeners:{
                                    change: function( item, newValue, oldValue, eOpts ){
                                        console.log(oldValue,newValue)
                                        if(oldValue){
                                            switch(oldValue){
                                                case 'FTP':{break}
                                                case 'Firmiana Cloud':{break}
                                                default:{
                                                    var modePanelLength = modePanel.items.length
                                                    modePanel.remove(modePanel.items.items[modePanelLength - 1])
                                                }
                                            }
                                        }
                                        if(newValue){
                                            switch(newValue){
                                                case 'FTP':{break}
                                                case 'Firmiana Cloud':{break}
                                                case 'PRIDE':{
                                                    var prideDataStore = Ext.create('Ext.data.Store',{
                                                        fields:[
                                                            {name:'filename',   type:'string'},
                                                            {name:'fileurl',    type:'string'}
                                                        ]
                                                    })
                                                    var pridePanel = Ext.create('Ext.form.FieldSet',{
                                                        xtype: 'fieldset',
                                                        width: 1000,
                                                        title: 'PRIDE Options',
                                                        bodyPadding: 10,
                                                        defaults: {
                                                            labelWidth: 120,
                                                            labelAlign: 'left',
                                                            msgTarget: 'side',
                                                        },
                                                        items:[{
                                                            xtype: 'textfield',
                                                            name: 'pxdno',
                                                            fieldLabel: 'PXD No.',
                                                            width: 200,
                                                            allowBlank: false,
                                                            afterLabelTextTpl: required,
                                                            flex:1,
                                                            listeners:{
                                                                blur: function(item,the) {
                                                                    if(item.value){
                                                                        var newValue = item.value
                                                                        var myMask = new Ext.LoadMask({
                                                                            msg    : 'Please wait...',
                                                                            target : pridePanel
                                                                        });
                                                                        myMask.show()
                                                                        Ext.Ajax.request({
                                                                            url : '/experiments/getPrideFileList/',
                                                                            method : 'GET',
                                                                            params : {
                                                                                pxdNo: newValue
                                                                            },
                                                                            success : function(response) {
                                                                                prideDataStore.removeAll()
                                                                                var responseText = response.responseText
                                                                                var addressList = responseText.split(';')
                                                                                for(var i = 0; i < addressList.length; i++){
                                                                                    var array = addressList[i].split(',')
                                                                                    prideDataStore.add({'filename': array[0], 'fileurl': array[1]})
                                                                                }
                                                                                myMask.hide()
                                                                                var itemselector = Ext.create('Ext.ux.form.ItemSelector',{
                                                                                    name: 'prideFileList',
                                                                                    height: 400,
                                                                                    fieldLabel: 'File list',
                                                                                    store: prideDataStore,
                                                                                    displayField: 'filename',
                                                                                    valueField: 'fileurl',
                                                                                    fromTitle: 'File available',
                                                                                    toTitle: 'File selected'
                                                                                })
                                                                                if(pridePanel.down('itemselector')){}else{
                                                                                    pridePanel.insert(1,itemselector)
                                                                                }
                                                                            },
                                                                            failure : function() {
                                                                                myMask.hide()
                                                                                Ext.Msg.alert("Error","Wrong pxd No.. Please check again.");
                                                                            }
                                                                        });
                                                                    }
                                                                }
                                                            }
                                                        }]
                                                    })
                                                    modePanel.insert(1,pridePanel)
                                                    break
                                                }
                                                case 'MassIVE':{
                                                    var prideDataStore = Ext.create('Ext.data.Store',{
                                                        fields:[
                                                            {name:'filename',   type:'string'},
                                                            {name:'fileurl',    type:'string'}
                                                        ]
                                                    })
                                                    var pridePanel = Ext.create('Ext.form.FieldSet',{
                                                        xtype: 'fieldset',
                                                        width: 1000,
                                                        title: 'PRIDE Options',
                                                        bodyPadding: 10,
                                                        defaults: {
                                                            labelWidth: 120,
                                                            labelAlign: 'left',
                                                            msgTarget: 'side',
                                                        },
                                                        items:[{
                                                            xtype: 'textfield',
                                                            name: 'pxdno',
                                                            fieldLabel: 'PXD No.',
                                                            width: 200,
                                                            allowBlank: false,
                                                            afterLabelTextTpl: required,
                                                            flex:1,
                                                            listeners:{
                                                                blur: function(item,the) {
                                                                    if(item.value){
                                                                        var newValue = item.value
                                                                        var myMask = new Ext.LoadMask({
                                                                            msg    : 'Please wait...',
                                                                            target : pridePanel
                                                                        });
                                                                        myMask.show()
                                                                        Ext.Ajax.request({
                                                                            url : '/experiments/getPrideFileList/',
                                                                            method : 'GET',
                                                                            params : {
                                                                                pxdNo: newValue
                                                                            },
                                                                            success : function(response) {
                                                                                prideDataStore.removeAll()
                                                                                var responseText = response.responseText
                                                                                var addressList = responseText.split(';')
                                                                                for(var i = 0; i < addressList.length; i++){
                                                                                    var array = addressList[i].split(',')
                                                                                    prideDataStore.add({'filename': array[0], 'fileurl': array[1]})
                                                                                }
                                                                                myMask.hide()
                                                                                var itemselector = Ext.create('Ext.ux.form.ItemSelector',{
                                                                                    name: 'prideFileList',
                                                                                    height: 400,
                                                                                    fieldLabel: 'File list',
                                                                                    store: prideDataStore,
                                                                                    displayField: 'filename',
                                                                                    valueField: 'fileurl',
                                                                                    fromTitle: 'File available',
                                                                                    toTitle: 'File selected'
                                                                                })
                                                                                if(pridePanel.down('itemselector')){}else{
                                                                                    pridePanel.insert(1,itemselector)
                                                                                }
                                                                            },
                                                                            failure : function() {
                                                                                Ext.Msg.alert("Error","Wrong pxd No.. Please check again.");
                                                                            }
                                                                        });
                                                                    }
                                                                }
                                                            }
                                                        }]
                                                    })
                                                    modePanel.insert(1,pridePanel)
                                                    break
                                                }
                                                default:{
                                                    Ext.Msg.alert('','Coming soon...')
                                                }
                                            }
                                        }
                                    }
                                }
                            }]
                        });

                        // search engine panel: choose workflow
                        var searchEnginePanel = Ext.create('Ext.panel.Panel', {
                            title: 'Search engine',
                            border: true,
                            // frame : true,
                            bodyPadding: 10,
                            headerPosition: 'top',
                            defaults: {
                                labelWidth: 120,
                                // afterLabelTextTpl: required,
                                labelAlign: 'left',
                                // allowBlank: false,
                                // width: 450,
                                editable: false,
                                msgTarget: 'side'
                            },
                            items: [{
                                xtype: 'combobox',
                                fieldLabel: 'Search Engine',
                                name: 'searchEngine',
                                displayField: 'searchEngine',
                                value: 'Mascot',
                                store: searchEngineStore,
                                typeAhead: true,
                                listeners: {
                                    change: function( item, newValue, oldValue, eOpts ){
                                        if(oldValue){
                                            var searchEnginePanelLength = searchEnginePanel.items.length
                                            if(searchEnginePanelLength != 1)
                                                searchEnginePanel.remove(searchEnginePanel.items.items[searchEnginePanelLength - 1])
                                        }
                                        if(newValue){
                                            switch(newValue){
                                                case 'Mascot':{
                                                    var mascotPanel = Ext.create('Ext.form.FieldSet',{
                                                        xtype: 'fieldset',
                                                        width: 1000,
                                                        title: 'Mascot Options',
                                                        bodyPadding: 10,
                                                        defaults: {
                                                            labelWidth: 120,
                                                            labelAlign: 'left',
                                                            editable: false,
                                                            msgTarget: 'side',
                                                        },
                                                        
                                                        items:[{
                                                            xtype: 'fieldcontainer',
                                                            layout: {
                                                                type: 'hbox',
                                                                align: 'stretch'
                                                            },
                                                            defaults: {
                                                                labelWidth: 170,
                                                                editable: false,
                                                                msgTarget: 'side',
                                                                margin: '0 0 0 20',
                                                            },
                                                            items:[{
                                                                xtype: 'combo',
                                                                fieldLabel: 'Missed Cleavages Allowed',
                                                                name: 'missedCleavagesAllowed',
                                                                id: 'aabbcc',
                                                                store: Ext.create('Ext.data.Store', {
                                                                    proxy: {
                                                                        type: 'ajax',
                                                                        url: '/experiments/ajax/display/Mascot_mode_missedCleavagesAllowed/',
                                                                        reader: {
                                                                            type: 'json',
                                                                            root: 'Mascot_mode_missedCleavagesAlloweds'
                                                                        }
                                                                    },
                                                                    fields: [{
                                                                        name: 'Mascot_mode_missedCleavagesAllowed',
                                                                        type: 'string'
                                                                    }],
                                                                    autoLoad: true
                                                                }),
                                                                displayField: 'Mascot_mode_missedCleavagesAllowed',
                                                                queryMode: 'local',
                                                                value: '2',
                                                                flex:1
                                                            },{
                                                                xtype: 'combo',
                                                                fieldLabel: 'Enzyme',
                                                                name: 'mascotEnzyme',
                                                                store: Ext.create('Ext.data.Store', {
                                                                    proxy: {
                                                                        type: 'ajax',
                                                                        url: '/experiments/ajax/display/Mascot_mode_mascotEnzyme/',
                                                                        reader: {
                                                                            type: 'json',
                                                                            root: 'Mascot_mode_mascotEnzymes'
                                                                        }
                                                                    },
                                                                    fields: [{
                                                                        name: 'Mascot_mode_mascotEnzyme',
                                                                        type: 'string'
                                                                    }],
                                                                    autoLoad: true
                                                                }),
                                                                displayField: 'Mascot_mode_mascotEnzyme',
                                                                queryMode: 'local',
                                                                value: 'Trypsin',
                                                                flex:1
                                                            }]
                                                        },{
                                                            xtype: 'fieldcontainer',
                                                            layout: {
                                                                type: 'hbox',
                                                                align: 'stretch'
                                                            },
                                                            defaults: {
                                                                labelWidth: 170,
                                                                editable: false,
                                                                msgTarget: 'side',
                                                                margin: '0 0 0 20',
                                                            },
                                                            items: [{
                                                                xtype: 'combo',
                                                                fieldLabel: 'Peptide Charge',
                                                                name: 'peptideCharge',
                                                                store: Ext.create('Ext.data.Store', {
                                                                    proxy: {
                                                                        type: 'ajax',
                                                                        url: '/experiments/ajax/display/Mascot_mode_peptideCharge/',
                                                                        reader: {
                                                                            type: 'json',
                                                                            root: 'Mascot_mode_peptideCharges'
                                                                        }
                                                                    },
                                                                    fields: [{
                                                                        name: 'Mascot_mode_peptideCharge',
                                                                        type: 'string'
                                                                    }],
                                                                    autoLoad: true
                                                                }),
                                                                displayField: 'Mascot_mode_peptideCharge',
                                                                queryMode: 'local',
                                                                value: '2+, 3+ and 4+',
                                                                flex: 1
                                                            }, {
                                                                xtype: 'combo',
                                                                fieldLabel: 'Precursor Search Type',
                                                                name: 'precursorSearchType',
                                                                store: Ext.create('Ext.data.Store', {
                                                                    proxy: {
                                                                        type: 'ajax',
                                                                        url: '/experiments/ajax/display/Mascot_mode_precursorSearchType/',
                                                                        reader: {
                                                                            type: 'json',
                                                                            root: 'Mascot_mode_precursorSearchTypes'
                                                                        }
                                                                    },
                                                                    fields: [{
                                                                        name: 'Mascot_mode_precursorSearchType',
                                                                        type: 'string'
                                                                    }],
                                                                    autoLoad: true
                                                                }),
                                                                displayField: 'Mascot_mode_precursorSearchType',
                                                                queryMode: 'local',
                                                                value: 'Monoisotopic',
                                                                flex: 1
                                                            }]
                                                        }]
                                                    })
                                                    searchEnginePanel.insert(1,mascotPanel)
                                                    break
                                                }
                                                case 'X!Tandem':{
                                                    var xtandemPanel = Ext.create('Ext.form.FieldSet',{
                                                        xtype: 'fieldset',
                                                        width: 1000,
                                                        title: 'X!Tandem Options',
                                                        bodyPadding: 10,
                                                        defaults: {
                                                            labelWidth: 120,
                                                            labelAlign: 'left',
                                                            editable: false,
                                                            msgTarget: 'side',
                                                        },
                                                        items:[{
                                                            xtype: 'fieldcontainer',
                                                            layout: {
                                                                type: 'hbox',
                                                                align: 'stretch'
                                                            },
                                                            defaults: {
                                                                labelWidth: 170,
                                                                editable: false,
                                                                msgTarget: 'side',
                                                                margin: '0 0 0 20',
                                                            },
                                                            items:[{
                                                                xtype: 'combo',
                                                                fieldLabel: 'Fragmentation Method',
                                                                name: 'fragmentationMethod',
                                                                store: Ext.create('Ext.data.Store', {
                                                                    fields: [{
                                                                        name: 'fragmentationMethod',
                                                                        type: 'string'
                                                                    }],
                                                                    data: [
                                                                        {'fragmentationMethod':'CID/HCD/QTOF'},
                                                                        {'fragmentationMethod':'ETD'}
                                                                    ],
                                                                    autoLoad: true
                                                                }),
                                                                displayField: 'fragmentationMethod',
                                                                queryMode: 'local',
                                                                value: 'CID/HCD/QTOF',
                                                                flex:1
                                                            },{
                                                                xtype: 'combo',
                                                                fieldLabel: 'Cysteine Protecting Group',
                                                                name: 'cysteineProtectingGroup',
                                                                store: Ext.create('Ext.data.Store', {
                                                                    fields: [{
                                                                        name: 'cysteineProtectingGroup',
                                                                        type: 'string'
                                                                    }],
                                                                    data: [
                                                                        {'cysteineProtectingGroup':'Carbamidomethylation (+57)'},
                                                                        {'cysteineProtectingGroup':'Carboxymethylation (+58)'},
                                                                        {'cysteineProtectingGroup':'NIPIA/NIPCAM (+99)'},
                                                                        {'cysteineProtectingGroup':'None'}
                                                                    ],
                                                                    autoLoad: true
                                                                }),
                                                                displayField: 'cysteineProtectingGroup',
                                                                queryMode: 'local',
                                                                value: 'Carbamidomethylation (+57)',
                                                                flex:1
                                                            }]
                                                        },{
                                                            xtype: 'fieldcontainer',
                                                            layout: {
                                                                type: 'hbox',
                                                                align: 'stretch'
                                                            },
                                                            defaults: {
                                                                labelWidth: 170,
                                                                editable: false,
                                                                msgTarget: 'side',
                                                                margin: '0 0 0 20',
                                                            },
                                                            items: [{
                                                                xtype: 'combo',
                                                                fieldLabel: 'Protease',
                                                                name: 'protease',
                                                                store: Ext.create('Ext.data.Store', {
                                                                    fields: [{
                                                                        name: 'protease',
                                                                        type: 'string'
                                                                    }],
                                                                    data: [
                                                                        {'protease':'Trypsin'},
                                                                        {'protease':'Chymotrypsin'},
                                                                        {'protease':'Lys-C'},
                                                                        {'protease':'Lys-N'},
                                                                        {'protease':'Arg-C'},
                                                                        {'protease':'Glu-C'},
                                                                        {'protease':'Asp-N'},
                                                                        {'protease':'None'},
                                                                    ],
                                                                    autoLoad: true
                                                                }),
                                                                displayField: 'protease',
                                                                queryMode: 'local',
                                                                value: 'Trypsin',
                                                                flex: 1
                                                            }, {
                                                                xtype: 'combo',
                                                                fieldLabel: 'Number of Allowed 13C',
                                                                name: 'numberOfAllowed13C',
                                                                store: Ext.create('Ext.data.Store', {
                                                                    fields: [{
                                                                        name: 'numberOfAllowed13C',
                                                                        type: 'string'
                                                                    }],
                                                                    data: [
                                                                        {'numberOfAllowed13C': 0},
                                                                        {'numberOfAllowed13C': 1}
                                                                    ],
                                                                    autoLoad: true
                                                                }),
                                                                displayField: 'numberOfAllowed13C',
                                                                queryMode: 'local',
                                                                value: 1,
                                                                flex: 1
                                                            }]
                                                        }]
                                                    })
                                                    searchEnginePanel.insert(1,xtandemPanel)
                                                    break
                                                }
                                                default:{
                                                    Ext.Msg.alert('','Coming soon...')
                                                }
                                            }
                                        }
                                    }
                                }
                            },{
                                xtype: 'fieldset',
                                width: 1000,
                                title: 'Mascot Options',
                                bodyPadding: 10,
                                defaults: {
                                    labelWidth: 120,
                                    labelAlign: 'left',
                                    editable: false,
                                    msgTarget: 'side',
                                },
                                
                                items:[{
                                    xtype: 'fieldcontainer',
                                    layout: {
                                        type: 'hbox',
                                        align: 'stretch'
                                    },
                                    defaults: {
                                        labelWidth: 170,
                                        editable: false,
                                        msgTarget: 'side',
                                        margin: '0 0 0 20',
                                    },
                                    items:[{
                                        xtype: 'combo',
                                        fieldLabel: 'Missed Cleavages Allowed',
                                        name: 'missedCleavagesAllowed',
                                        id: 'aabbcc',
                                        store: Ext.create('Ext.data.Store', {
                                            proxy: {
                                                type: 'ajax',
                                                url: '/experiments/ajax/display/Mascot_mode_missedCleavagesAllowed/',
                                                reader: {
                                                    type: 'json',
                                                    root: 'Mascot_mode_missedCleavagesAlloweds'
                                                }
                                            },
                                            fields: [{
                                                name: 'Mascot_mode_missedCleavagesAllowed',
                                                type: 'string'
                                            }],
                                            autoLoad: true
                                        }),
                                        displayField: 'Mascot_mode_missedCleavagesAllowed',
                                        queryMode: 'local',
                                        value: '2',
                                        flex:1
                                    },{
                                        xtype: 'combo',
                                        fieldLabel: 'Enzyme',
                                        name: 'mascotEnzyme',
                                        store: Ext.create('Ext.data.Store', {
                                            proxy: {
                                                type: 'ajax',
                                                url: '/experiments/ajax/display/Mascot_mode_mascotEnzyme/',
                                                reader: {
                                                    type: 'json',
                                                    root: 'Mascot_mode_mascotEnzymes'
                                                }
                                            },
                                            fields: [{
                                                name: 'Mascot_mode_mascotEnzyme',
                                                type: 'string'
                                            }],
                                            autoLoad: true
                                        }),
                                        displayField: 'Mascot_mode_mascotEnzyme',
                                        queryMode: 'local',
                                        value: 'Trypsin',
                                        flex:1
                                    }]
                                },{
                                    xtype: 'fieldcontainer',
                                    layout: {
                                        type: 'hbox',
                                        align: 'stretch'
                                    },
                                    defaults: {
                                        labelWidth: 170,
                                        editable: false,
                                        msgTarget: 'side',
                                        margin: '0 0 0 20',
                                    },
                                    items: [{
                                        xtype: 'combo',
                                        fieldLabel: 'Peptide Charge',
                                        name: 'peptideCharge',
                                        store: Ext.create('Ext.data.Store', {
                                            proxy: {
                                                type: 'ajax',
                                                url: '/experiments/ajax/display/Mascot_mode_peptideCharge/',
                                                reader: {
                                                    type: 'json',
                                                    root: 'Mascot_mode_peptideCharges'
                                                }
                                            },
                                            fields: [{
                                                name: 'Mascot_mode_peptideCharge',
                                                type: 'string'
                                            }],
                                            autoLoad: true
                                        }),
                                        displayField: 'Mascot_mode_peptideCharge',
                                        queryMode: 'local',
                                        value: '2+, 3+ and 4+',
                                        flex: 1
                                    }, {
                                        xtype: 'combo',
                                        fieldLabel: 'Precursor Search Type',
                                        name: 'precursorSearchType',
                                        store: Ext.create('Ext.data.Store', {
                                            proxy: {
                                                type: 'ajax',
                                                url: '/experiments/ajax/display/Mascot_mode_precursorSearchType/',
                                                reader: {
                                                    type: 'json',
                                                    root: 'Mascot_mode_precursorSearchTypes'
                                                }
                                            },
                                            fields: [{
                                                name: 'Mascot_mode_precursorSearchType',
                                                type: 'string'
                                            }],
                                            autoLoad: true
                                        }),
                                        displayField: 'Mascot_mode_precursorSearchType',
                                        queryMode: 'local',
                                        value: 'Monoisotopic',
                                        flex: 1
                                    }]
                                }]
                            }]
                        });

                        // instrument related information
                        var instrumentPanel = Ext.create('Ext.panel.Panel', {
                            title: 'SearchDatabase-Parameter',
                            border: true,
                            // frame : true,
                            headerPosition: 'top',
                            bodyPadding: 10,
                            defaults: {
                                labelWidth: 120,
                                labelAlign: 'left',
                                width: 1000,
                                allowBlank: false,
                                editable: false,
                                msgTarget: 'side',
                                afterLabelTextTpl: required
                            },
                            items: [/*
                                                 * { xtype : 'container', layout : { type : 'hbox', align : 'stretch' },
                                                 * items : [{ xtype : 'textfield', fieldLabel : 'Location', name : 'Room',
                                                 * emptyText : 'Room', labelWidth : 120, width : 300, allowBlank : false }, {
                                                 * xtype : 'textfield', name : 'No', emptyText : 'No.', labelWidth : 120,
                                                 * width : 300, allowBlank : false }, { xtype : 'textfield', name :
                                                 * 'Temperature', emptyText : 'Temperature', labelWidth : 120, width : 300,
                                                 * allowBlank : false }] },
                                                 */
                            {
                                xtype: 'fieldcontainer',
                                layout: {
                                    type: 'hbox',
                                    align: 'stretch'
                                },
                                defaults: {
                                    editable: false,
                                    allowBlank: false,
                                    msgTarget: 'side',
                                    afterLabelTextTpl: required
                                },
                                items: [{
                                    width: 450,
                                    xtype: 'combobox',
                                    id: 'searchdatabase',
                                    fieldLabel: 'Search database',
                                    labelWidth: 120,
                                    name: 'Search_database',
                                    queryMode: 'local',
                                    displayField: 'Search_database',
                                    store: searchDatabaseStore
                                },{
                                    xtype: 'button',
                                    text: 'Other database',
                                    margin: '0 0 0 5',
                                    handler: function(){
                                        var uploadWindow = Ext.create('Ext.window.Window',{
                                            width: 400,
                                            height: 300,
                                            autoShow: true,
                                            modal: true,
                                            title: 'Upload FASTA file',
                                            layout: 'anchor',
                                            items:[{
                                                xtype: 'form',
                                                id: 'upload_form',
                                                anchor: '100% 100%',
                                                margin: '10 10 10 10',
                                                border: 0,
                                                defaults: {
                                                    allowBlank: false,
                                                    msgTarget: 'side',
                                                    afterLabelTextTpl: required,
                                                    labelWidth: 120,
                                                },
                                                dockedItems: [{
                                                    xtype: 'toolbar',
                                                    dock: 'bottom',
                                                    layout: {
                                                        pack: 'center',
                                                        align: 'middle'
                                                    },
                                                    items: [{
                                                        xtype: 'button',
                                                        text: 'Submit',
                                                        handler: function(){
                                                            formpanel = Ext.getCmp('upload_form');
                                                            var form = formpanel.getForm();
                                                            if (form.isValid()) {
                                                                Ext.Ajax.timeout = 180000;
                                                                form.submit({
                                                                    url: '/experiments/save/upload/',
                                                                    waitMsg: 'Uploading FASTA file...',
                                                                    //timeout : 300000,
                                                                    // standardSubmit : true
                                                                    success: function(frm, act) {
                                                                        // val = String(act.result.msg);
                                                                        // len = val.legnth
                                                                        // // console.log(len)
                                                                        // // val=val.substring(1)
                                                                        // if (val.length < 6) {
                                                                        //     for (i = val.length; i < 6; i++)
                                                                        //         val = '0' + val
                                                                        // }
                                                                        var text = act.response.responseText
                                                                        var fastaLibName = Ext.JSON.decode(text).fastaLibName
                                                                        Ext.getCmp('searchdatabase').setValue(fastaLibName)
                                                                        Ext.Msg.alert('Success', 'Upload finished.');
                                                                        searchDatabaseStore.load()
                                                                        uploadWindow.close()
                                                                    },
                                                                    failure: function(form, action) {
                                                                        Ext.Msg.alert('Failed', 'Upload failed. Contact admin.');
                                                                    }
                                                                })
                                                            }
                                                        }
                                                    }, {
                                                        xtype: 'button',
                                                        text: 'Cancel',
                                                        handler: function(){
                                                            formpanel = Ext.getCmp('upload_form');
                                                            formpanel.getForm().reset();
                                                        }
                                                    }]
                                                }],
                                                items:[{
                                                    xtype: 'textfield',
                                                    fieldLabel: 'Species',
                                                    name: 'upload_species'
                                                },{
                                                    xtype: 'combo',
                                                    fieldLabel: 'Data source',
                                                    name: 'upload_datasource',
                                                    displayField: 'name',
                                                    editable: false,
                                                    store: Ext.create('Ext.data.Store', {
                                                        fields: ['name'],
                                                        data : [
                                                            {"name":"UniProt"},
                                                            {"name":"RefSeq"},
                                                            // {"name":"Arizona"}
                                                            ],
                                                        autoLoad: true
                                                    })
                                                },{
                                                    xtype: 'datefield',
                                                    fieldLabel: 'Version date',
                                                    name: 'upload_date',
                                                    width: '200',
                                                    editable: false,
                                                },{
                                                    width: 350,
                                                    xtype: 'filefield',
                                                    name: 'upload_file',
                                                    fieldLabel: 'FASTA file',
                                                    buttonText: 'Browse',
                                                    emptyText: 'File path'
                                                },{
                                                    xtype: 'hiddenfield',
                                                    name: 'upload_timestamp',
                                                    value: timestamp
                                                }]
                                            }]
                                        })
                                    }                               
                                }]
                            }, {
                                width: 450,
                                xtype: 'combobox',
                                fieldLabel: 'Manufacturer',
                                name: 'Instrument_manufacturer',
                                displayField: 'Instrument_manufacturer',
                                store: instrumentManufacturerStore
                            }, {
                                width: 450,
                                xtype: 'combobox',
                                fieldLabel: 'Instrument',
                                name: 'Instrument_name',
                                displayField: 'Instrument',
                                store: instrumentStore,
                                typeAhead: true,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            var ms1 = Ext.getCmp("instrument_MS1");
                                            // console.log(lab)
                                            ms1.clearValue();
                                            ms1.store.load({
                                                params: {
                                                    id: records[0].data.Instrument
                                                }
                                            })
                                            // ms1.setValue(ms1.store.data.items[0].data.Instrument_MS1)
                                            var ms2 = Ext.getCmp("instrument_MS2");
                                            ms2.clearValue();
                                            // console.log(records[0].data)
                                            ms2.store.load({
                                                params: {
                                                    id: records[0].data.Instrument
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'fieldcontainer',
                                layout: {
                                    type: 'hbox',
                                    align: 'stretch'
                                },
                                defaults: {
                                    editable: false,
                                    allowBlank: false,
                                    msgTarget: 'side',
                                    afterLabelTextTpl: required
                                },
                                items: [{
                                    xtype: 'combobox',
                                    fieldLabel: 'Details',
                                    name: 'instrument_MS1',
                                    displayField: 'Instrument_MS1',
                                    emptyText: 'MS1',
                                    store: MS1Store,
                                    queryMode: 'local',
                                    id: 'instrument_MS1',
                                    labelWidth: 120,
                                    width: 300,
                                    listeners: {
                                        select: {
                                            fn: function(combo, records, index) {
                                                var tol = Ext.getCmp("instrument_MS1_tol");
                                                tol.clearValue();
                                                tol.store.load({
                                                    params: {
                                                        id: records[0].data.Instrument_MS1
                                                    }
                                                });
                                                // tol.setValue(tol.store.data.items[0].data.Instrument_MS1_tol)
//                                                if(combo.value=="Orbitrap" || combo.value=="TOF"){
//                                                    combobox_instrument_MS1_tol_unit = Ext.getCmp("instrument_MS1_tol_unit");
//                                                    combobox_instrument_MS1_tol_unit.setValue("ppm");
//                                                }
//                                                if(combo.value=="Ion Trap"){
//                                                    combobox_instrument_MS1_tol_unit = Ext.getCmp("instrument_MS1_tol_unit");
//                                                    combobox_instrument_MS1_tol_unit.setValue("Da");
//                                                }
                                            }
                                        }
                                    }
                                }, 
                                {
                                    xtype: 'combobox',
                                    name: 'instrument_MS1_tol',
                                    displayField: 'Instrument_MS1_tol',
                                    id: 'instrument_MS1_tol',
                                    store: MS1tolStore,
                                    queryMode: 'local',
                                    emptyText: 'Precursor Mass Tolerance',
                                    width: 195,
                                    editable : true
                                }, 
                                {
                                    xtype: 'combobox',
                                    name: 'instrument_MS1_tol_unit',
                                    displayField: 'Instrument_MS1_tol_unit',
                                    id: 'instrument_MS1_tol_unit',
                                    store: ["ppm", "Da"],
                                    queryMode: 'local',
                                    emptyText: 'unit',
                                    width: 70
                                },
                                
                                
                                {
                                    xtype: 'combobox',
                                    name: 'instrument_MS2',
                                    id: 'instrument_MS2',
                                    displayField: 'Instrument_MS2',
                                    emptyText: 'MS2',
                                    store: MS2Store,
                                    queryMode: 'local',
                                    width: 150,
                                    padding: '0, 0, 0, 20',
                                    listeners: {
                                        select: {
                                            fn: function(combo, records, index) {
                                                // console.log(records[0].data)
                                                var lab = Ext.getCmp("instrument_MS2_tol");
                                                lab.clearValue();
                                                lab.store.load({
                                                    params: {
                                                        id: records[0].data.Instrument_MS2
                                                    }
                                                });
                                                //combobox_instrument_MS2_tol_unit = Ext.getCmp("instrument_MS2_tol_unit");
                                                //combobox_instrument_MS2_tol_unit.setValue("Da");
//                                                if(combo.value=="Orbitrap" || combo.value=="TOF"){
//                                                    combobox_instrument_MS2_tol_unit = Ext.getCmp("instrument_MS2_tol_unit");
//                                                    combobox_instrument_MS2_tol_unit.setValue("ppm");
//                                                }
//                                                if(combo.value=="Ion Trap"){
//                                                    combobox_instrument_MS2_tol_unit = Ext.getCmp("instrument_MS2_tol_unit");
//                                                    combobox_instrument_MS2_tol_unit.setValue("Da");
//                                                }
                                            }
                                        }
                                    }
                                }, {
                                    xtype: 'combobox',
                                    name: 'instrument_MS2_tol',
                                    id: 'instrument_MS2_tol',
                                    displayField: 'Instrument_MS2_tol',
                                    store: MS2tolStore,
                                    emptyText: 'Fragment Mass Tolerance',
                                    queryMode: 'local',
                                    width: 195,
                                    editable : true
                                },
                                {
                                    xtype: 'combobox',
                                    name: 'instrument_MS2_tol_unit',
                                    id: 'instrument_MS2_tol_unit',
                                    displayField: 'Instrument_MS2_tol_unit',
                                    store: ["ppm", "Da"],
                                    queryMode: 'local',
                                    emptyText: 'Unit',
                                    width: 70
                                }
                                ]
                            },
                            
                            /*******************backup******************************/
                            /*
                            {
                                xtype: 'fieldcontainer',
                                layout: {
                                    type: 'hbox',
                                    align: 'stretch'
                                },
                                defaults: {
                                    editable: false,
                                    allowBlank: false,
                                    msgTarget: 'side',
                                    afterLabelTextTpl: required
                                },
                                items: [{
                                    xtype: 'combobox',
                                    fieldLabel: 'Details',
                                    name: 'instrument_MS1',
                                    displayField: 'Instrument_MS1',
                                    emptyText: 'MS1',
                                    store: MS1Store,
                                    queryMode: 'local',
                                    id: 'instrument_MS1',
                                    labelWidth: 120,
                                    width: 300,
                                    listeners: {
                                        select: {
                                            fn: function(combo, records, index) {
                                                var tol = Ext.getCmp("instrument_MS1_tol");
                                                tol.clearValue();
                                                tol.store.load({
                                                    params: {
                                                        id: records[0].data.Instrument_MS1
                                                    }
                                                });
                                                // tol.setValue(tol.store.data.items[0].data.Instrument_MS1_tol)
                                            }
                                        }
                                    }
                                }, {
                                    xtype: 'combobox',
                                    name: 'instrument_MS1_tol',
                                    displayField: 'Instrument_MS1_tol',
                                    id: 'instrument_MS1_tol',
                                    store: MS1tolStore,
                                    queryMode: 'local',
                                    emptyText: 'Precursor Mass Tolerance',
                                    width: 170
                                }, {
                                    xtype: 'combobox',
                                    name: 'instrument_MS2',
                                    id: 'instrument_MS2',
                                    displayField: 'Instrument_MS2',
                                    emptyText: 'MS2',
                                    store: MS2Store,
                                    queryMode: 'local',
                                    width: 150,
                                    listeners: {
                                        select: {
                                            fn: function(combo, records, index) {
                                                // console.log(records[0].data)
                                                var lab = Ext.getCmp("instrument_MS2_tol");
                                                lab.clearValue();
                                                lab.store.load({
                                                    params: {
                                                        id: records[0].data.Instrument_MS2
                                                    }
                                                })
                                            }
                                        }
                                    }
                                }, {
                                    xtype: 'combobox',
                                    name: 'instrument_MS2_tol',
                                    id: 'instrument_MS2_tol',
                                    displayField: 'Instrument_MS2_tol',
                                    store: MS2tolStore,
                                    emptyText: 'Fragment Mass Tolerance',
                                    queryMode: 'local',
                                    width: 170
                                }]
                            },
                            */
                            /*************************************************/
                            
                            
                            {
                                xtype: 'combobox',
                                fieldLabel: 'Fixed Modifications',
                                afterLabelTextTpl: '',
                                name: 'Fixed_Modification',
                                displayField: 'Fixed_Modification',
                                emptyText: '',
                                store: fixedModificationStore,
                                multiSelect: true,
                                // queryMode: 'local',
                                labelWidth: 120,
                                allowBlank: true
                                // listeners : {
                                // boxready : function(combo, eOpts) {
                                // var tempvalue = [];
                                // tempvalue.push('DeStreak (C)')
                                // tempvalue.push('Acetyl (Protein N-term)')
                                // tempvalue.push('Oxidation (M)')
                                // combo.setValue(tempvalue);
                                // }
                                // }
                            }, {
                                xtype: 'combobox',
                                name: 'Dynamic_Modification',
                                fieldLabel: 'Dynamic Modifications',
                                afterLabelTextTpl: '',
                                multiSelect: true,
                                displayField: 'Dynamic_Modification',
                                store: dynamicModificationStore,
                                emptyText: '',
                                allowBlank: true
                            }, {
                                xtype: 'button',
                                text: 'Add new modification',
                                margin: '0 0 15 0',
                                width: 180,
                                handler: function(){
                                    var compositionDict = new Array()
                                    var specificityText = ""
                                    var newModificationWindow = Ext.create('Ext.window.Window',{
                                        width: 540,
                                        height: 510,
                                        autoShow: true,
                                        modal: true,
                                        title: 'Add new modification',
                                        layout: 'anchor',
                                        items:[{
                                            xtype: 'form',
                                            id: 'add_new_modification',
                                            anchor: '100% 100%',
                                            margin: '15 10 10 10',
                                            border: 0,
                                            defaults: {
                                                allowBlank: false,
                                                msgTarget: 'side',
                                                afterLabelTextTpl: required,
                                                labelWidth: 120,
                                                width: 500
                                            },
                                            dockedItems: [{
                                                xtype: 'toolbar',
                                                dock: 'bottom',
                                                layout: {
                                                    pack: 'center',
                                                    align: 'middle'
                                                },
                                                items: [{
                                                    xtype: 'button',
                                                    text: 'Submit',
                                                    handler: function(){
                                                        formpanel = Ext.getCmp('add_new_modification')
                                                        var form = formpanel.getForm()
                                                        var submitDate = new Date
                                                        formpanel.items.items[5].setValue(Ext.Date.format(submitDate, 'd/m/Y')) 
                                                        if (formpanel.items.items[2].items.items[0].value == ''){
                                                            Ext.Msg.alert('Warning','Composition cannot be empty.')
                                                        }
                                                        else if (formpanel.items.items[3].items.items[4].value == ''){
                                                            Ext.Msg.alert('Warning','Specificity cannot be empty.')
                                                        }
                                                        else if (form.isValid()) {
                                                            Ext.Ajax.timeout = 180000;
                                                            form.submit({
                                                                url: '/experiments/save/new_modification/',
                                                                waitMsg: 'Adding new modification...',
                                                                //timeout : 300000,
                                                                // standardSubmit : true
                                                                success: function(frm, act) {
                                                                    // val = String(act.result.msg);
                                                                    // len = val.legnth
                                                                    // // console.log(len)
                                                                    // // val=val.substring(1)
                                                                    // if (val.length < 6) {
                                                                    //     for (i = val.length; i < 6; i++)
                                                                    //         val = '0' + val
                                                                    // }
                                                                    Ext.Msg.alert('Success', 'New modification is added.');
                                                                    dynamicModificationStore.load()
                                                                    fixedModificationStore.load()
                                                                },
                                                                failure: function(form, action) {
                                                                    Ext.Msg.alert('Failed', 'Failed to add new modification. Contact admin.');
                                                                }
                                                            })
                                                        }
                                                    }
                                                }, {
                                                    xtype: 'button',
                                                    text: 'Reset',
                                                    handler: function(){
                                                        var formpanel = Ext.getCmp('add_new_modification');
                                                        formpanel.getForm().reset();
                                                        compositionDict = new Array()
                                                        specificityText = ''
                                                        this.up().up().items.items[3].items.items[0].store.removeAll()
                                                        // console.log(compositionDict)
                                                    }
                                                }]
                                            }],
                                            items:[{
                                                xtype: 'textfield',
                                                fieldLabel: 'Title',
                                                name: 'new_modi_title',
                                                width: 450
                                            },{
                                                xtype: 'textfield',
                                                fieldLabel: 'Fullname',
                                                name: 'new_modi_fullname',
                                                width: 450
                                            },{
                                                xtype: 'fieldset',
                                                width: 500,
                                                title: 'Delta',
                                                bodyPadding: 10,
                                                defaults: {
                                                    labelWidth: 120,
                                                    labelAlign: 'left',
                                                    editable: false,
                                                    msgTarget: 'side',
                                                },
                                                items: [{
                                                    xtype: 'displayfield',
                                                    fieldLabel: 'Composition',
                                                    submitValue: true,
                                                    width: 370,
                                                    name: 'new_modi_composition',
                                                    value: '',
                                                    // msgTarget: 'side',
                                                    // afterLabelTextTpl: required,
                                                },{
                                                    xtype: 'fieldcontainer',
                                                    layout: {
                                                        type: 'hbox',
                                                        align: 'stretch'
                                                    },
                                                    defaults: {
                                                        editable: false,
                                                    },
                                                    items: [{
                                                        xtype: 'combobox',
                                                        submitValue: false,
                                                        fieldLabel: 'Symbols',
                                                        width: 235,
                                                        labelWidth: 120,
                                                        value: '13C',
                                                        displayField: 'name',
                                                        store: Ext.create('Ext.data.Store', {
                                                            fields: ['name'],
                                                            data : [
                                                                {'name':"13C"},{'name':"15N"},{'name':"18O"},{'name':"2H"},{'name':"Ac"},{'name':"Ag"},{'name':"As"},{'name':"Au"},{'name':"B"},
                                                                {'name':"Br"},{'name':"C"},{'name':"Ca"},{'name':"Cd"},{'name':"Cl"},{'name':"Co"},{'name':"Cr"},{'name':"Cu"},{'name':"dHex"},
                                                                {'name':"F"},{'name':"Fe"},{'name':"H"},{'name':"Hep"},{'name':"Hex"},{'name':"HexA"},{'name':"HexNAc"},{'name':"Hg"},
                                                                {'name':"I"},{'name':"K"},{'name':"Kdn"},{'name':"Kdo"},{'name':"Li"},{'name':"Me"},{'name':"Mg"},{'name':"Mn"},
                                                                {'name':"Mo"},{'name':"N"},{'name':"Na"},{'name':"NeuAc"},{'name':"NeuGc"},{'name':"Ni"},{'name':"O"},{'name':"P"},
                                                                {'name':"Pd"},{'name':"Pent"},{'name':"Phos"},{'name':"S"},{'name':"Se"},{'name':"Sulf"},{'name':"Water"},{'name':"Zn"}
                                                                ],
                                                            autoLoad: true
                                                        })
                                                    },{
                                                        xtype: 'combobox',
                                                        submitValue: false,
                                                        width: 100,
                                                        value: '1',
                                                        margin: '0 0 0 5',
                                                        displayField: 'name',
                                                        store: Ext.create('Ext.data.Store', {
                                                            fields: ['name'],
                                                            data : [
                                                                {'name':"-10"},{'name':"-9"},{'name':"-8"},{'name':"-7"},{'name':"-6"},{'name':"-5"},{'name':"-4"},{'name':"-3"},{'name':"-2"},{'name':"-1"},
                                                                {'name':"1"},{'name':"2"},{'name':"3"},{'name':"4"},{'name':"5"},{'name':"6"},{'name':"7"},{'name':"8"},{'name':"9"},{'name':"10"}
                                                                ],
                                                            autoLoad: true
                                                        })
                                                    },{
                                                        xtype: 'button',
                                                        text: 'Add',
                                                        margin: '0 0 0 5',
                                                        width: 60,
                                                        handler: function(){
                                                            var valueSymbol1 = this.up().items.items[0].value
                                                            var valueSymbol2 = parseInt(this.up().items.items[1].value)
                                                            if(compositionDict[valueSymbol1]){
                                                                compositionDict[valueSymbol1] += valueSymbol2
                                                                if(compositionDict[valueSymbol1] == 0)
                                                                    delete compositionDict[valueSymbol1]
                                                            }else{
                                                                compositionDict[valueSymbol1] = valueSymbol2
                                                            }

                                                            var compositionText = "";
                                                            for (var key in compositionDict) {
                                                                if(!isNaN(compositionDict[key])){
                                                                    if (compositionText == "") {
                                                                        compositionText = key + '(' + compositionDict[key] + ')';
                                                                    }
                                                                    else {
                                                                        compositionText += " " + key + '(' + compositionDict[key] + ')';
                                                                    }
                                                                } 
                                                            }
                                                            console.log(compositionText)
                                                            this.up().up().items.items[0].setValue(compositionText)
                                                        }
                                                    }]
                                                }]
                                            },{
                                                xtype: 'fieldset',
                                                width: 500,
                                                title: 'Specificity',
                                                bodyPadding: 10,
                                                defaults: {
                                                    allowBlank: false,
                                                    msgTarget: 'side',
                                                    afterLabelTextTpl: required,
                                                    labelWidth: 120,
                                                    labelAlign: 'left',
                                                    editable: false,
                                                    msgTarget: 'side',
                                                },
                                                items: [{
                                                    xtype: 'grid',
                                                    height: 100,
                                                    margin: '0 0 5 0',
                                                    columns: [
                                                        { text: 'Site',  dataIndex: 'site', flex: 2 },
                                                        { text: 'Position', dataIndex: 'position', flex: 2 },
                                                        { text: 'Classification', dataIndex: 'classification', flex: 3 }
                                                    ],
                                                    store: Ext.create('Ext.data.Store', {
                                                        fields: ['site','position','classification'],
                                                        data : [
                                                        ],
                                                        autoLoad: true
                                                    })
                                                },{
                                                    xtype: 'combo',
                                                    fieldLabel: 'Site',
                                                    submitValue: false,
                                                    editable: false,
                                                    displayField: 'name',
                                                    value: 'A',
                                                    store: Ext.create('Ext.data.Store', {
                                                        fields: ['name'],
                                                        data : [
                                                            {'name':"A"},{'name':"R"},{'name':"N"},{'name':"D"},{'name':"C"},{'name':"E"},{'name':"Q"},{'name':"G"},{'name':"H"},
                                                            {'name':"I"},{'name':"L"},{'name':"K"},{'name':"M"},{'name':"F"},{'name':"P"},{'name':"S"},{'name':"T"},{'name':"W"},
                                                            {'name':"Y"},{'name':"V"},{'name':"N-term"},{'name':"C-term"},{'name':"U"},{'name':"O"},{'name':"J"}
                                                            ],
                                                        autoLoad: true
                                                    })
                                                },{
                                                    xtype: 'combo',
                                                    fieldLabel: 'Position',
                                                    submitValue: false,
                                                    editable: false,
                                                    value: 'Anywhere',
                                                    displayField: 'name',
                                                    store: Ext.create('Ext.data.Store', {
                                                        fields: ['name'],
                                                        data : [
                                                            {'name':"Anywhere"},{'name':"Any N-term"},{'name':"Any C-term"},{'name':"Protein N-term"},{'name':"Protein C-term"}
                                                            ],
                                                        autoLoad: true
                                                    })
                                                },{
                                                    xtype: 'combo',
                                                    fieldLabel: 'Classification',
                                                    submitValue: false,
                                                    editable: false,
                                                    displayField: 'name',
                                                    value: 'Post-translational',
                                                    store: Ext.create('Ext.data.Store', {
                                                        fields: ['name'],
                                                        data : [
                                                            {'name':"Post-translational"},{'name':"Co-translational"},{'name':"Pre-translational"},{'name':"Chemical derivative"},{'name':"Artefact"},
                                                            {'name':"N-linked glycosylation"},{'name':"O-linked glycosylation"},{'name':"Other glycosylation"},{'name':"Synth. pep. protect. gp."},
                                                            {'name':"Isotopic label"},{'name':"Non-standard residue"},{'name':"Multiple"},{'name':"Other"},{'name':"AA substitution"}
                                                            ],
                                                        autoLoad: true
                                                    })
                                                },{
                                                    xtype: 'hiddenfield',
                                                    name: 'new_modi_specificity',
                                                    value: '',
                                                },{
                                                    xtype: 'button',
                                                    text: 'Add',
                                                    margin: '0 0 5 0',
                                                    width: 60,
                                                    handler: function(){
                                                        var valueSymbol1 = this.up().items.items[1].value
                                                        var valueSymbol2 = this.up().items.items[2].value
                                                        var valueSymbol3 = this.up().items.items[3].value
                                                        this.up().items.items[0].store.add({'site':valueSymbol1,'position':valueSymbol2,'classification':valueSymbol3})
                                                        if(specificityText != ''){
                                                            specificityText += ';'
                                                        }
                                                        specificityText += valueSymbol1 + ',' + valueSymbol2 + ',' + valueSymbol3
                                                        console.log(specificityText)
                                                        this.up().items.items[4].setValue(specificityText)
                                                    }
                                                }]
                                            },{
                                                xtype: 'hiddenfield',
                                                name: 'upload_timestamp',
                                                value: timestamp
                                            },{
                                                xtype: 'hiddenfield',
                                                name: 'new_modi_addtime',
                                                value: new Date
                                            }]
                                        }]
                                    })
                                }                               
                            }, {
                                xtype: 'numberfield',
                                fieldLabel: 'Repeat Number',
                                name: 'repeat',
                                minValue: 1,
                                editable: true,
                                width: 240
                            }, {
                                xtype: 'numberfield',
                                fieldLabel: 'Fraction Number',
                                name: 'fraction',
                                minValue: 1,
                                editable: true,
                                width: 240
                            }, 
                            // {
                            //     xtype: 'fieldcontainer',
                            //     layout: {
                            //         type: 'hbox',
                            //         align: 'stretch'
                            //     },
                            //     defaults: {
                            //         labelWidth: 170,
                            //         editable: false,
                            //         allowBlank: false,
                            //         msgTarget: 'side',
                            //     },
                            //     items:[{
                            //         xtype: 'radiofield',
                            //         name: 'addexperimentFdr',
                            //         inputValue: 'Spectrum-Level FDR',
                            //         fieldLabel: '',
                            //         checked: true,
                            //         labelWidth: 0,
                            //         width: 155,
                            //         labelSeparator: '',
                            //         hideEmptyLabel: false,
                            //         boxLabel: 'Spectrum-Level FDR',
                            //         listeners:{
                            //             change: function( item, newValue, oldValue, eOpts ){
                            //                 if(newValue==true){
                            //                     item.up().down('numberfield').show()
                            //                 }else{
                            //                     item.up().down('numberfield').hide()
                            //                 }
                            //             }
                            //         }
                            //     },{
                            //         xtype: 'numberfield',
                            //         name: 'addexperimentSpectrumFdrValue',
                            //         fieldLabel: '',
                            //         margin: '0 0 0 20',
                            //         editable: true,
                            //         value: 0.01,
                            //         minValue: 0.01,
                            //         step: 0.01,
                            //         maxValue: 1
                            //     }]
                            // }, {
                            //     xtype: 'fieldcontainer',
                            //     layout: {
                            //         type: 'hbox',
                            //         align: 'stretch'
                            //     },
                            //     defaults: {
                            //         labelWidth: 170,
                            //         editable: false,
                            //         msgTarget: 'side',
                            //     },
                            //     items:[{
                            //         xtype: 'radiofield',
                            //         name: 'addexperimentFdr',
                            //         inputValue: 'Peptide-Level FDR',
                            //         fieldLabel: '',
                            //         labelWidth: 0,
                            //         width: 155,
                            //         labelSeparator: '',
                            //         hideEmptyLabel: false,
                            //         boxLabel: 'Peptide-Level FDR',
                            //         listeners:{
                            //             change: function( item, newValue, oldValue, eOpts ){
                            //                 if(newValue==true){
                            //                     item.up().down('numberfield').show()
                            //                 }else{
                            //                     item.up().down('numberfield').hide()
                            //                 }
                            //             }
                            //         }
                            //     },{
                            //         xtype: 'numberfield',
                            //         name: 'addexperimentPeptideFdrValue',
                            //         fieldLabel: '',
                            //         hidden: true,
                            //         margin: '0 0 0 20',
                            //         editable: true,
                            //         value: 0.01,
                            //         minValue: 0.01,
                            //         step: 0.01,
                            //         maxValue: 1
                            //     }]
                            // }, 
                            {
                                xtype: 'combobox',
                                name: 'quantificationMethods',
                                fieldLabel: 'Quantification Method',
                                afterLabelTextTpl: '',
                                displayField: 'quantificationMethod',
                                store: quantificationMethodsStore,
                                emptyText: '',
                                allowBlank: false,
                                width: 450,
                                afterLabelTextTpl: required,
                            },{
                                xtype: 'fieldcontainer',
                                layout: {
                                    type: 'hbox',
                                    align: 'stretch'
                                },
                                defaults: {
                                    labelWidth: 170,
                                    editable: false,
                                    msgTarget: 'side',
                                },
                                items:[{
                                    xtype: 'radiofield',
                                    name: 'addexperimentFdr',
                                    inputValue: 'Protein-Level FDR',
                                    fieldLabel: '',
                                    checked: true,
                                    labelWidth: 0,
                                    width: 155,
                                    labelSeparator: '',
                                    hideEmptyLabel: false,
                                    boxLabel: 'Protein-Level FDR',
                                    afterLabelTextTpl: required,
                                    listeners:{
                                        change: function( item, newValue, oldValue, eOpts ){
                                            if(newValue==true){
                                                item.up().down('numberfield').show()
                                            }else{
                                                item.up().down('numberfield').hide()
                                            }
                                        }
                                    }
                                },{
                                    xtype: 'numberfield',
                                    name: 'addexperimentProteinFdrValue',
                                    fieldLabel: '',
                                    // hidden: true,
                                    margin: '0 0 0 20',
                                    editable: true,
                                    value: 0.01,
                                    minValue: 0.01,
                                    step: 0.01,
                                    maxValue: 1
                                }]
                            }
                            ]
                        });

                        var commentPanel = Ext.create('Ext.panel.Panel', {
                            title: 'Comment',
                            // frame : true,
                            headerPosition: 'top',
                            bodyPadding: 10,
                            defaults: {
                                labelWidth: 120,
                                labelAlign: 'top',
                                width: 600,
                                allowBlank: true
                            },
                            items: [{
                                xtype: 'textfield',
                                fieldLabel: 'Ispec No.',
                                name: 'ispecno',
                                labelAlign: 'left'
                            }, 
                            // {
                            // xtype : 'textareafield',
                            // fieldLabel : 'Experiment Description',
                            // name : 'description'
                            // },
                            {
                                xtype: 'textareafield',
                                fieldLabel: 'Experiment Comments/Conclusions',
                                name: 'comments_conclusions'
                            }]
                        });
                        // button for submit of cancel form
                        var buttonPanel = Ext.create('Ext.panel.Panel', {
                            // frame : true,
                            border: true,
                            buttonAlign: "center",
                            buttons: [{
                                text: 'Submit',
                                handler: submitForm
                            }, {
                                text: 'Cancel',
                                handler: cancelForm
                            }]
                        });
                        var formPanel = Ext.create('Ext.form.Panel', {
                            id: timestamp,
                            // border:true,
                            // frame:true,
                            // renderTo : 'form',
                            overflowY: 'scroll',
                            items: [generalPanel, separationPanel, digestPanel, modePanel, searchEnginePanel, instrumentPanel, commentPanel, buttonPanel]
                        });
                        /*
                         * var win_addexp = new Ext.window.Window({ layout: 'fit', id:'add_exp_tab', title: 'Add
                         * Experiment', resizable :true, closable: true, maximizable:true, collapsible:true, height: 600,
                         * width: 1100, //draggable: { constrain: true, constrainTo: Ext.getBody() },
                         * 
                         * items:[formPanel]}); win_addexp.show();
                         */
                        tab = Ext.getCmp('content-panel')
                        tab.add({
                            id: 'add_exp_tab',
                            title: 'Add Experiment',
                            iconCls: 'addexperiment',
                            closable: true,
                            layout: 'fit',
                            items: [formPanel]
                        }).show();
                    
                    }
                }
            },
            '#addsample': {
                click: function() {
                    var panel = Ext.getCmp('add_sample_tab');
                    if (panel) {
                        var main = Ext.getCmp("content-panel");
                        main.setActiveTab(panel);
                        return 0;
                    }
                    var timestamp = 'compare' + (new Date()).valueOf()
                    // CSRF protection
                    csrftoken = Ext.util.Cookies.get('csrftoken');
                    var submitForm = function() {
                        formpanel = Ext.getCmp(timestamp);
                        var form = formpanel.getForm();
                        //var currentTime = Ext.Date.format(new Date(), 'n/d/Y');
                        //Ext.getCmp("gar.app.control.Menu.addsampleId").items.items[2].setValue(currentTime)
                        if (form.isValid()) {
                            Ext.Ajax.timeout = 180000;
                            form.submit({
                                url: '/experiments/save/sample/',
                                waitMsg: 'Adding Sample......',
                                //timeout : 300000,
                                success: function(frm, act) {
                                    val = String(act.result.msg);
                                    len = val.legnth;
                                    // console.log(len)
                                    // val=val.substring(1)
                                    if (val.length < 6) {
                                        for (var i = val.length; i < 6; i++)
                                            val = '0' + val;
                                    }
                                    Ext.Msg.alert('Success', 'Add a sample successfully. Sample No: ' + val);
                                    // Ext.Msg.alert('Success', 'Sample
                                    // add complete. Sample No: ' +
                                    // Ext.encode(act.result.msg));
                                },
                                failure: function(form, action) {
                                    Ext.Msg.alert('Failed', 'Add a sample unsuccessfully. Contact admin.');
                                }
                            });
                        }
                    }
                    ;
                    var cancelForm = function() {
                        formpanel = Ext.getCmp(timestamp);
                        formpanel.getForm().reset();
                    }
                    ;
                    // experimenter Model and store
                    var companyStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/all_company/',
                            reader: {
                                type: 'json',
                                root: 'all_company'
                            }
                        },
                        fields: [{
                            name: 'company',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var labStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/all_lab/',
                            reader: {
                                type: 'json',
                                root: 'all_lab'
                            }
                        },
                        fields: [{
                            name: 'lab',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var experimenterStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/all_experimenter/',
                            reader: {
                                type: 'json',
                                root: 'experimenters'
                            }
                        },
                        fields: [{
                            name: 'experimenter',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var sourceTissueTaxonAorMStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/Source_TissueTaxonAorM/',
                            reader: {
                                type: 'json',
                                root: 'Source_TissueTaxonAorM'
                            }
                        },
                        fields: [{
                            name: 'Source_TissueTaxonAorM',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var sourceTissueTaxonIDStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/Source_TissueTaxonID/',
                            reader: {
                                type: 'json',
                                root: 'tissueID'
                            }
                        },
                        fields: [{
                            name: 'tissueID',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var sourceTissueTaxonNameStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/Source_TissueTaxonName/',
                            reader: {
                                type: 'json',
                                root: 'tissueName'
                            }
                        },
                        fields: [{
                            name: 'tissueName',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var geneIDStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Source_TissueTaxonID/',
                            reader: {
                                type: 'json',
                                root: 'Source_TissueTaxonIDs'
                            }
                        },
                        fields: [{
                            name: 'Source_TissueTaxonID',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var SourceTissueSystemStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/Source_TissueSystem/',
                            reader: {
                                type: 'json',
                                root: 'Source_TissueSystem'
                            }
                        },
                        fields: [{
                            name: 'Source_TissueSystem',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var SourceTissueOrganStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/Source_TissueOrgan/',
                            reader: {
                                type: 'json',
                                root: 'Source_TissueOrgan'
                            }
                        },
                        fields: [{
                            name: 'Source_TissueOrgan',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var SourceTissueStructureStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display2/Source_TissueStructure/',
                            reader: {
                                type: 'json',
                                root: 'Source_TissueStructure'
                            }
                        },
                        fields: [{
                            name: 'Source_TissueStructure',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var SourceTissueTypeStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Source_TissueType/',
                            reader: {
                                type: 'json',
                                root: 'Source_TissueTypes'
                            }
                        },
                        fields: [{
                            name: 'Source_TissueType',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var sourceTissueTaxonStrainStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/Source_TissueTaxonStrain/',
                            reader: {
                                type: 'json',
                                root: 'tissueStrain'
                            }
                        },
                        fields: [{
                            name: 'tissueStrain',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var sourceTaxonStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Source_taxon/',
                            reader: {
                                type: 'json',
                                root: 'Source_taxons'
                            }
                        },
                        fields: [{
                            name: 'Source_taxon',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var allAgeUnitStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/All_AgeUnit/',
                            reader: {
                                type: 'json',
                                root: 'All_AgeUnits'
                            }
                        },
                        fields: [{
                            name: 'All_AgeUnit',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var rxUnitStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Rx_unit/',
                            reader: {
                                type: 'json',
                                root: 'Rx_units'
                            }
                        },
                        fields: [{
                            name: 'Rx_unit',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var rxUnitDetailStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/unit_detail/',
                            reader: {
                                type: 'json',
                                root: 'unit_detail'
                            }
                        },
                        fields: [{
                            name: 'unit_detail',
                            type: 'string'
                        }]
                        // autoLoad : true
                    });
                    var rxTreatmentStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Rx_treatment/',
                            reader: {
                                type: 'json',
                                root: 'Rx_treatments'
                            }
                        },
                        fields: [{
                            name: 'Rx_treatment',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var rxTreatmentDetailStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/treatment_detail/',
                            reader: {
                                type: 'json',
                                root: 'all_detail'
                            }
                        },
                        fields: [{
                            name: 'all_detail',
                            type: 'string'
                        }]
                        // autoLoad : true
                    });
                    var ubiSubcellStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Ubi_subcell/',
                            reader: {
                                type: 'json',
                                root: 'Ubi_subcells'
                            }
                        },
                        fields: [{
                            name: 'Ubi_subcell',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var ubiMethodStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Ubi_method/',
                            reader: {
                                type: 'json',
                                root: 'Ubi_methods'
                            }
                        },
                        fields: [{
                            name: 'Ubi_method',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var genotypeStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Genotype/',
                            reader: {
                                type: 'json',
                                root: 'Genotypes'
                            }
                        },
                        fields: [{
                            name: 'Genotype',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var cellTypeStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Cell_type/',
                            reader: {
                                type: 'json',
                                root: 'Cell_types'
                            }
                        },
                        fields: [{
                            name: 'Cell_type',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var cellcellTypeStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/source_CellType/',
                            reader: {
                                type: 'json',
                                root: 'source_CellTypes'
                            }
                        },
                        fields: [{
                            name: 'source_CellType',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var cellnameStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display2/Cell_Name/',
                            reader: {
                                type: 'json',
                                root: 'Cell_Name'
                            }
                        },
                        fields: [{
                            name: 'Cell_Name',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var tissueTypeStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Tissue_type/',
                            reader: {
                                type: 'json',
                                root: 'Tissue_types'
                            }
                        },
                        fields: [{
                            name: 'Tissue_type',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var tissueGenderStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Tissue_gender/',
                            reader: {
                                type: 'json',
                                root: 'Tissue_genders'
                            }
                        },
                        fields: [{
                            name: 'Tissue_gender',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var fluidNameStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Fluid_name/',
                            reader: {
                                type: 'json',
                                root: 'Fluid_names'
                            }
                        },
                        fields: [{
                            name: 'Fluid_name',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var ContainNoStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/ContainNoStore/',
                            reader: {
                                type: 'json',
                                root: 'ContainNo'
                            }
                        },
                        fields: [{
                            name: 'ContainNo',
                            type: 'string'
                        }]
                    });
                    var ContainBasketStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/ContainBasketStore/',
                            reader: {
                                type: 'json',
                                root: 'ContainBasket'
                            }
                        },
                        fields: [{
                            name: 'ContainBasket',
                            type: 'string'
                        }]
                    });
                    var ContainLayerStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/ContainLayerStore/',
                            reader: {
                                type: 'json',
                                root: 'ContainLayer'
                            }
                        },
                        fields: [{
                            name: 'ContainLayer',
                            type: 'string'
                        }]
                    });
                    
                    var sampleTemplateStore = Ext.create('Ext.data.Store', {
                        fields: [{
                            name: 'sample_no',
                            type: 'string'
                        }],
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/sample_no/',
                            reader: {
                                type: 'json',
                                root: 'sample_no'
                            }
                        },
                        autoLoad: true
                    });
                    
                    var setGeneralPanelLocalValue = function(cmpLocation, response) {
                        var text = response.responseText;
                        responseJson = Ext.JSON.decode(text).data;
                        
                        
                        //Sample Location
                        var sampleLocation = cmpLocation.getForm().findField('location');
                        if (responseJson.RefrigeratorLayer) {
                            sampleLocation.items.items[0].setValue(true);
                        } else if (responseJson.Nitrogen_Layer) {
                            sampleLocation.items.items[1].setValue(true);
                        } else {
                            sampleLocation.items.items[2].setValue(true);
                        }
                        
                        //Source Type
                        var sampleSourceType = cmpLocation.getForm().findField('cell_tissue');
                        var geneListLength = 0;
                        var geneSymbolVar = "geneSymbol";
                        var GeneIDVar = "GeneID";
                        var geneTaxonVar = "geneTaxon";
                        var geneSmallList;
                        var Cmp_source_cell
                        var geneListVar
                        
                        //deal Source Type
                        if (responseJson.cell_tissue == "Tissue") {
                            sampleSourceType.items.items[0].setValue(true);
                            //sampleSourceType.items.items[1].setValue(false);
                            //sampleSourceType.items.items[2].setValue(false);
                            //sampleSourceType.items.items[3].setValue(false);
                            
                            if (responseJson.geneList[0] != "") {
                                console.log("responseJson.geneList[0] != ''");
                                Cmp_source_tissue = Ext.getCmp('source_tissue').getForm();
                                //Get form of "Tissue"                              
                                geneListVar = responseJson.geneList;
                                //Get geneList : ["g1|g1-001|10036", "g2|g2-002|10090"]                                                                                                                     
                                Ext.getCmp("source_tissue").items.items[5].setValue(geneListVar.length);
                                //Set Total number of Target Gene
                                
                                if (geneListVar.length > 0) {
                                    for (var listIndex = 0; listIndex < geneListVar.length; listIndex++) {
                                        geneSmallList = geneListVar[listIndex].split("|");
                                        //Get geneList[index].split("|") : ["g1", "g1-001", "10036"]
                                        
                                        geneSymbolVar = "geneSymbol" + (listIndex + 1);
                                        //Set name "geneSymbol1"
                                        Cmp_source_tissue.findField(geneSymbolVar).setValue(geneSmallList[0]);
                                        //Set "geneSymbol" Value
                                        GeneIDVar = "GeneID" + (listIndex + 1);
                                        Cmp_source_tissue.findField(GeneIDVar).setValue(geneSmallList[1]);
                                        geneTaxonVar = "geneTaxon" + (listIndex + 1);
                                        Cmp_source_tissue.findField(geneTaxonVar).setValue(geneSmallList[2]);
                                    }
                                }
                            
                            } 
                            else {
                                Ext.getCmp("source_tissue").items.items[5].setValue(0);
                            }
                        
                        } else if (responseJson.cell_tissue == "Cell") {
                            //sampleSourceType.items.items[0].setValue(false);
                            sampleSourceType.items.items[1].setValue(true);
                            //sampleSourceType.items.items[2].setValue(false);
                            //sampleSourceType.items.items[3].setValue(false);
                            
                            if (responseJson.geneList[0] != "") {
                                Cmp_source_cell = Ext.getCmp('source_cell').getForm();
                                geneListVar = responseJson.geneList;
                                Ext.getCmp("source_cell").items.items[3].setValue(geneListVar.length);
                                
                                if (geneListVar.length > 0) {
                                    for (var listIndex = 0; listIndex < geneListVar.length; listIndex++) {
                                        geneSmallList = geneListVar[listIndex].split("|");
                                        console.log(geneSmallList);
                                        
                                        geneSymbolVar = "geneSymbol" + (listIndex + 1);
                                        //console.log(geneSymbolVar + "---" + geneSmallList[0])
                                        Cmp_source_cell.findField(geneSymbolVar).setValue(geneSmallList[0]);
                                        GeneIDVar = "GeneID" + (listIndex + 1);
                                        //console.log(GeneIDVar + "---" + geneSmallList[1])
                                        Cmp_source_cell.findField(GeneIDVar).setValue(geneSmallList[1]);
                                        geneTaxonVar = "geneTaxon" + (listIndex + 1);
                                        //console.log(geneTaxonVar + "---" + geneSmallList[2])
                                        Cmp_source_cell.findField(geneTaxonVar).setValue(geneSmallList[2]);
                                    }
                                }
                            } 
                            else {
                                Ext.getCmp("source_cell").items.items[3].setValue(0);
                            }
                        
                        
                        
                        } else if (responseJson.cell_tissue == "Fluid") {
                            //sampleSourceType.items.items[0].setValue(false);
                            //sampleSourceType.items.items[1].setValue(false);
                            sampleSourceType.items.items[2].setValue(true);
                            //sampleSourceType.items.items[3].setValue(false);
                            
                            if (responseJson.geneList[0] != "") {
                                Cmp_source_fluid = Ext.getCmp('source_fluid').getForm();
                                //Get form of "Fluid & Excreta"                             
                                geneListVar = responseJson.geneList;
                                //Get geneList : ["g1|g1-001|10036", "g2|g2-002|10090"]
                                Ext.getCmp("source_fluid").items.items[5].setValue(geneListVar.length);
                                //Set Total number of Target Gene
                                
                                if (geneListVar.length > 0) {
                                    for (var listIndex = 0; listIndex < geneListVar.length; listIndex++) {
                                        geneSmallList = geneListVar[listIndex].split("|");
                                        //Get geneList[index].split("|") : ["g1", "g1-001", "10036"]
                                        
                                        geneSymbolVar = "geneSymbol" + (listIndex + 1);
                                        //Set name "geneSymbol1"
                                        Cmp_source_fluid.findField(geneSymbolVar).setValue(geneSmallList[0]);
                                        //Set "geneSymbol" Value
                                        GeneIDVar = "GeneID" + (listIndex + 1);
                                        Cmp_source_fluid.findField(GeneIDVar).setValue(geneSmallList[1]);
                                        geneTaxonVar = "geneTaxon" + (listIndex + 1);
                                        Cmp_source_fluid.findField(geneTaxonVar).setValue(geneSmallList[2]);
                                    }
                                }
                            } 
                            else {
                                Ext.getCmp("source_fluid").items.items[3].setValue(0);
                            }
                        
                        } else {
                            //sampleSourceType.items.items[0].setValue(false);
                            //sampleSourceType.items.items[1].setValue(false);
                            //sampleSourceType.items.items[2].setValue(false);
                            sampleSourceType.items.items[3].setValue(true);
                        }
                        
                        
                        //Total number of Treatment
                        var totalNumberOfTreatment = cmpLocation.getForm().findField('treat_num');
                        totalNumberOfTreatment.setValue(responseJson.treatmentsCount);
                        
                        var treatIndex;
                        //deal Treatment + No.
                        if (responseJson.treatmentsCount > 0) {
                            for (treatIndex = 1; treatIndex <= responseJson.treatmentsCount; treatIndex++) {
                                console.log("pre--Rx_treatment");
                                Ext.getCmp('Treatment' + treatIndex).getForm().findField('Rx_treatment' + treatIndex).setValue(responseJson.rx_treatments[treatIndex - 1]);
                            }
                        }
                        
                        //deal Treatment + No.
                        if (responseJson.treatmentsCount > 0) {
                            for (treatIndex = 1; treatIndex <= responseJson.treatmentsCount; treatIndex++) {
                                console.log("pre--Rx_treatment");
                                Ext.getCmp("treantment_detail" + treatIndex).setValue(responseJson.rx_treatments_detail[treatIndex - 1]);
                                
                                console.log("pre--rx_duration")
                                Ext.getCmp("Treatment" + treatIndex).items.items[2].items.items[0].setValue(responseJson.rx_duration[treatIndex - 1]);
                                Ext.getCmp("Treatment" + treatIndex).items.items[2].items.items[1].setValue(responseJson.rx_duration_time[treatIndex - 1]);
                            }
                        }
                        
                        
                        //deal "Concentration"
                        var unitConcentration;
                        if (responseJson.treatmentsCount > 0) {
                            for (treatIndex = 1; treatIndex <= responseJson.treatmentsCount; treatIndex++) {
                                if (responseJson.rx_treatments[treatIndex - 1] != "Gene Engineering" && responseJson.rx_unit[treatIndex - 1] != "Concentration") {
                                    Ext.getCmp("samp-treat-unit" + treatIndex).items.items[1].setValue(responseJson.rx_unit[treatIndex - 1]);
                                    Ext.getCmp("samp-treat-unit" + treatIndex).items.items[2].setValue(responseJson.rx_unit_deatil1[treatIndex - 1]);
                                }
                                if (responseJson.rx_treatments[treatIndex - 1] != "Gene Engineering" && responseJson.rx_unit[treatIndex - 1] == "Concentration") {
                                    Ext.getCmp("samp-treat-unit" + treatIndex).items.items[1].setValue(responseJson.rx_unit[treatIndex - 1]);
                                    unitConcentration = responseJson.rx_unit_deatil2[treatIndex - 1].split("/");
                                    Ext.getCmp("unit_detail2_" + treatIndex).items.items[0].setValue(unitConcentration[0]);
                                    Ext.getCmp("unit_detail2_" + treatIndex).items.items[2].setValue(unitConcentration[1]);
                                }
                            }
                        
                        }
                    }
                    
                    // general panel
                    var generalPanel = Ext.create('Ext.form.Panel', {
                        title: 'General',
                        //id : 'sample-general',
                        id: "gar.app.control.Menu.addsampleId",
                        // frame : true,
                        storeId: 'methods',
                        layout: 'auto',
                        headerPosition: 'top',
                        bodyPadding: 10,
                        defaults: {
                            labelWidth: 120,
                            labelAligh: 'left',
                            width: 1000,
                            allowBlank: false
                        },
                        items: [{
                            xtype: 'combobox',
                            fieldLabel: 'Choose template',
                            displayField: 'sample_no',
                            name: 'sample-template',
                            store: sampleTemplateStore,
                            queryMode: 'local',
                            typeAhead: true,
                            width: 805,
                            allowBlank: true,
                            listeners: {
                                select: function() {
                                    var cmpLocation = Ext.getCmp("gar.app.control.Menu.addsampleId");
                                    var templateNo = cmpLocation.items.items[0].value;
                                    console.log(templateNo);
                                    
                                    
                                    
                                    Ext.Ajax.request({
                                        url: '/experiments/load/sample/',
                                        params: {
                                            sample_no: templateNo
                                            // csrfmiddlewaretoken : csrftoken
                                        },
                                        success: function(response) {
                                            /////////////////////////////////////////////////////////////////////////
                                            setGeneralPanelLocalValue(cmpLocation, response)
                                            /////////////////////////////////////////////////////////////////////////
                                        
                                        }
                                    });
                                    
                                    Ext.getCmp('add_sample_tab').items.items[0].getForm().load({
                                        url: '/experiments/load/sample/',
                                        method: 'POST',
                                        params: {
                                            sample_no: templateNo
                                        }
                                    });
                                    //alert("test");
                                    //var currentTime = Ext.Date.format(new Date(), 'n/d/Y');
                                    //cmpLocation.items.items[2].setValue(currentTime);
                                    //var currentTime = Ext.Date.format(new Date(), 'n/d/Y');
                                    // Ext.getCmp("gar.app.control.Menu.addsampleId").items.items[2].setValue(currentTime)
                                
                                
                                
                                }
                            }
                        
                        }, {
                            fieldLabel: 'Experimenter',
                            xtype: 'fieldcontainer',
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            defaults: {
                                editable: false
                            },
                            items: [{
                                xtype: 'combobox',
                                displayField: 'company',
                                name: 'company',
                                valueField: 'company',
                                store: companyStore,
                                queryMode: 'local',
                                allowBlank: false,
                                emptyText: 'Company',
                                width: 300,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            var lab = Ext.getCmp("lab");
                                            lab.clearValue();
                                            lab.store.load({
                                                params: {
                                                    id: records[0].data.company
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'combobox',
                                displayField: 'lab',
                                valueField: 'lab',
                                name: 'lab',
                                id: 'lab',
                                emptyText: 'Laboratory',
                                store: labStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 200,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            var experimenter = Ext.getCmp("experimenter");
                                            experimenter.clearValue();
                                            experimenter.store.load({
                                                params: {
                                                    id: records[0].data.lab
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'combobox',
                                displayField: 'experimenter',
                                valueField: 'experimenter',
                                emptyText: 'Experimenter',
                                name: 'experimenter',
                                id: 'experimenter',
                                store: experimenterStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 180
                            }]
                        }, {
                            xtype: 'datefield',
                            fieldLabel: 'Date',
                            value: Ext.Date.format(new Date(), 'n/d/Y'),
                            emptyText: 'Date',
                            name: 'date',
                            width: '200'
                            //                                          listeners:{
                            //                                              "select":function(field, value){
                            //                                                  var cmpLocation = Ext.getCmp("gar.app.control.Menu.addsampleId"); 
                            //                                                  cmpLocation.items.items[2].setValue(value);
                            //                                              }
                            //                                          }
                        }, {
                            xtype: 'radiogroup',
                            fieldLabel: 'Sample Location',
                            name: 'location',
                            id: 'location' + timestamp,
                            columns: 3,
                            items: [{
                                boxLabel: 'Refrigerator',
                                name: 'location',
                                inputValue: 'Refrigerator'
                            }, {
                                boxLabel: 'Liquid Nitrogen',
                                name: 'location',
                                inputValue: 'Liquid Nitrogen'
                            }, {
                                boxLabel: 'Others',
                                name: 'location',
                                inputValue: 'Others'
                            }]
                        }, {
                            xtype: 'radiogroup',
                            fieldLabel: 'Source Type',
                            name: 'cell_tissue',
                            id: 'cell_tissue' + timestamp,
                            columns: 2,
                            items: [{
                                boxLabel: 'Tissue',
                                name: 'cell_tissue',
                                inputValue: 'Tissue'
                            }, {
                                boxLabel: 'Cell \& MicroOrganism',
                                name: 'cell_tissue',
                                inputValue: 'Cell'
                            }, {
                                boxLabel: 'Fluid & Excreta',
                                name: 'cell_tissue',
                                inputValue: 'Fluid'
                            }, {
                                boxLabel: 'Others',
                                name: 'cell_tissue',
                                inputValue: 'Others'
                            }]
                        }, {
                            xtype: 'numberfield',
                            fieldLabel: 'Total number of Treatment',
                            afterLabelTextTpl: required,
                            id: 'treat_num',
                            name: 'treat_num',
                            minValue: 0,
                            maxValue: 10,
                            value: 0,
                            listeners: {
                                change: function(o, newV, oldV) {
                                    if (newV > 10) {
                                        alert('Number of treatment must be smaller than 10!')
                                        newV = 1
                                        Ext.getCmp('treat_num' + timestamp).setValue(1)
                                    }
                                    
                                    if (oldV) {
                                        delTreatment(oldV);
                                    }
                                    for (i = 1; i <= newV; i++) {
                                        addTreatment(i + 1, i);
                                    }
                                }
                            },
                            width: 240
                        }, {
                            xtype: 'hiddenfield',
                            name: 'csrfmiddlewaretoken',
                            value: csrftoken
                        }, {
                            xtype: 'hiddenfield',
                            name: 'timestamp',
                            value: timestamp
                        }]
                    });
                    // source tissue panel
                    var addGene = function(where, index, samplenum) {
                        var sample = {
                            fieldLabel: 'Target Gene ' + samplenum,
                            xtype: 'fieldcontainer',
                            id: 'target_Gene' + samplenum,
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            items: [{
                                xtype: 'textfield',
                                emptyText: 'Gene Symbol',
                                // fieldLabel : 'Target
                                // Gene',
                                name: 'geneSymbol' + samplenum,
                                allowBlank: true
                            }, {
                                xtype: 'textfield',
                                emptyText: 'Gene ID',
                                // fieldLabel : 'Target
                                // Gene',
                                name: 'GeneID' + samplenum,
                                allowBlank: true
                            }, {
                                xtype: 'combobox',
                                displayField: 'Source_TissueTaxonID',
                                valueField: 'Source_TissueTaxonID',
                                emptyText: 'TaxonID',
                                name: 'geneTaxon' + samplenum,
                                store: geneIDStore,
                                queryMode: 'local',
                                allowBlank: true,
                                width: 150
                            }]
                        };
                        var temp = Ext.getCmp(where);
                        console.log(temp)
                        temp.insert(index, sample);
                    }
                    var delGene = function(where, samplenum) {
                        for (i = samplenum; i > 0; i--) {
                            var sample = Ext.getCmp('target_Gene' + i);
                            var temp = Ext.getCmp(where);
                            temp.remove(sample);
                        }
                    }
                    ;
                    var source_tissue = Ext.create('Ext.form.Panel', {
                        title: 'Tissue',
                        border: true,
                        // frame : true,
                        id: 'source_tissue',
                        bodyPadding: 10,
                        headerPosition: 'left',
                        defaults: {
                            labelWidth: 120,
                            labelAligh: 'left',
                            width: 800,
                            allowBlank: false
                        },
                        items: [{
                            fieldLabel: 'Taxon',
                            xtype: 'fieldcontainer',
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            items: [{
                                xtype: 'combobox',
                                displayField: 'Source_TissueTaxonAorM',
                                name: 'Source_TissueTaxonAorM',
                                valueField: 'Source_TissueTaxonAorM',
                                store: new Ext.data.SimpleStore({
                                    fields: ["Source_TissueTaxonAorM"],
                                    data: [["Animal"], ["Plant"]]
                                }),
                                queryMode: 'local',
                                allowBlank: false,
                                width: 120,
                                emptyText: 'Animal/Plant',
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            var lab = Ext.getCmp("tissueName");
                                            lab.clearValue();
                                            lab.store.load({
                                                params: {
                                                    id: records[0].data.Source_TissueTaxonAorM
                                                }
                                            })
                                            var lab = Ext.getCmp("tissue-system");
                                            lab.clearValue();
                                            lab.store.load({
                                                params: {
                                                    id: records[0].data.Source_TissueTaxonAorM
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'combobox',
                                displayField: 'tissueName',
                                valueField: 'tissueName',
                                name: 'tissueName',
                                id: 'tissueName',
                                emptyText: 'Taxon Name',
                                store: sourceTissueTaxonNameStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 300,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            // console.log(records)
                                            var experimenter = Ext.getCmp("tissueID");
                                            experimenter.clearValue();
                                            experimenter.store.load({
                                                params: {
                                                    id: records[0].data.tissueName
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'combobox',
                                displayField: 'tissueID',
                                valueField: 'tissueID',
                                emptyText: 'Taxon ID',
                                name: 'tissueID',
                                id: 'tissueID',
                                store: sourceTissueTaxonIDStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 100,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            // console.log(records)
                                            var experimenter = Ext.getCmp("Tissue_strain");
                                            experimenter.clearValue();
                                            experimenter.store.load({
                                                params: {
                                                    id: records[0].data.tissueID
                                                }
                                            })
                                        }
                                    }
                                }
                            }]
                        }, {
                            xtype: 'combobox',
                            fieldLabel: 'Strain',
                            id: 'Tissue_strain',
                            emptyText: 'Strain Name',
                            valueField: 'tissueStrain',
                            displayField: 'tissueStrain',
                            name: 'tissueStrain',
                            queryMode: 'local',
                            store: sourceTissueTaxonStrainStore
                        }, {
                            xtype: 'fieldcontainer',
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            fieldLabel: 'Age',
                            items: [{
                                xtype: 'textfield',
                                name: 'tissue_age'
                            }, {
                                xtype: 'combobox',
                                displayField: 'All_AgeUnit',
                                valueField: 'All_AgeUnit',
                                name: 'All_AgeUnit',
                                store: allAgeUnitStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 180
                            }]
                        }, {
                            xtype: 'combobox',
                            fieldLabel: 'Gender',
                            displayField: 'Tissue_gender',
                            name: 'Tissue_gender',
                            store: tissueGenderStore,
                            width: 300
                        }, {
                            xtype: 'combobox',
                            fieldLabel: 'Genotype',
                            displayField: 'Genotype',
                            name: 'Genotype',
                            store: genotypeStore
                        }, {
                            xtype: 'numberfield',
                            fieldLabel: 'Total number of Target Gene',
                            afterLabelTextTpl: required,
                            // id : 'Gene_num',
                            name: 'Gene_num',
                            minValue: 0,
                            maxValue: 10,
                            value: 0,
                            listeners: {
                                change: function(o, newV, oldV) {
                                    if (newV > 10) {
                                        alert('Number of Gene must be smaller than 10!')
                                        newV = 1
                                        Ext.getCmp('Gene_num').setValue(1)
                                    }
                                    if (oldV) {
                                        delGene('source_tissue', oldV);
                                    }
                                    for (i = 1; i <= newV; i++) {
                                        addGene('source_tissue', i + 5, i);
                                    }
                                }
                            },
                            width: 240
                        }, {
                            fieldLabel: 'Tissue',
                            xtype: 'fieldcontainer',
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            items: [{
                                xtype: 'combobox',
                                displayField: 'Source_TissueSystem',
                                name: 'Source_TissueSystem',
                                valueField: 'Source_TissueSystem',
                                id: 'tissue-system',
                                store: SourceTissueSystemStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 180,
                                emptyText: 'System',
                                editable: false,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            var lab = Ext.getCmp("tissue-organ");
                                            lab.clearValue();
                                            lab.store.load({
                                                params: {
                                                    id: records[0].data.Source_TissueSystem
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'combobox',
                                displayField: 'Source_TissueOrgan',
                                valueField: 'Source_TissueOrgan',
                                name: 'Source_TissueOrgan',
                                id: 'tissue-organ',
                                emptyText: 'Organ',
                                store: SourceTissueOrganStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 150,
                                editable: false,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            var lab = Ext.getCmp("tissue-structure");
                                            lab.clearValue();
                                            lab.store.load({
                                                params: {
                                                    id: records[0].data.Source_TissueOrgan
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'combobox',
                                displayField: 'Source_TissueStructure',
                                valueField: 'Source_TissueStructure',
                                name: 'Source_TissueStructure',
                                id: 'tissue-structure',
                                emptyText: 'Anatomical Structure',
                                store: SourceTissueStructureStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 165,
                                editable: false,
                            }, {
                                xtype: 'combobox',
                                displayField: 'Source_TissueType',
                                valueField: 'Source_TissueType',
                                emptyText: 'Status',
                                name: 'Source_TissueType',
                                store: SourceTissueTypeStore,
                                queryMode: 'local',
                                allowBlank: false,
                                editable: false,
                            }]
                        }, 
                        // {
                        // fieldLabel : 'Target Gene',
                        // xtype : 'fieldcontainer',
                        // layout : {
                        // type : 'hbox',
                        // align : 'stretch'
                        // },
                        // items : [{
                        // xtype : 'textfield',
                        // emptyText : 'Gene Symbol',
                        // // fieldLabel : 'Target
                        // // Gene',
                        // name : 'geneSymbol',
                        // allowBlank : true
                        // }, {
                        // xtype : 'textfield',
                        // emptyText : 'Gene ID',
                        // // fieldLabel : 'Target
                        // // Gene',
                        // name : 'GeneID',
                        // allowBlank : true
                        // }, {
                        // xtype : 'combobox',
                        // displayField : 'Source_TissueTaxonID',
                        // valueField : 'Source_TissueTaxonID',
                        // emptyText : 'Gene Taxon',
                        // name : 'geneTaxon',
                        // store : geneIDStore,
                        // queryMode : 'local',
                        // allowBlank : true,
                        // width : 100
                        // }]
                        // },
                        {
                            xtype: 'timefield',
                            fieldLabel: 'CR Time',
                            format: 'G:i:s',
                            increment: 15,
                            name: 'circ_time',
                            allowBlank: true
                        }, {
                            xtype: 'textfield',
                            fieldLabel: 'Specific ID',
                            name: 'Specific_ID',
                            allowBlank: true
                        }]
                    });
                    // source cell panel
                    var source_cell = Ext.create('Ext.form.Panel', {
                        id: 'source_cell',
                        title: 'Cell and MicroOrganism',
                        border: true,
                        // frame : true,
                        bodyPadding: 10,
                        headerPosition: 'left',
                        defaults: {
                            labelWidth: 120,
                            labelAligh: 'left',
                            width: 800,
                            allowBlank: false
                        },
                        items: [{
                            fieldLabel: 'Taxon',
                            xtype: 'fieldcontainer',
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            items: [{
                                xtype: 'combobox',
                                displayField: 'Source_TissueTaxonAorM',
                                name: 'Source_TissueTaxonAorM',
                                emptyText: 'Cell/MicroOrganism',
                                valueField: 'Source_TissueTaxonAorM',
                                store: new Ext.data.SimpleStore({
                                    fields: ["Source_TissueTaxonAorM"],
                                    data: [["Animal"], ["Microorganism"]]
                                }),
                                queryMode: 'local',
                                allowBlank: false,
                                width: 120,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            var lab = Ext.getCmp("cellName");
                                            lab.clearValue();
                                            lab.store.load({
                                                params: {
                                                    id: records[0].data.Source_TissueTaxonAorM
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'combobox',
                                displayField: 'tissueName',
                                valueField: 'tissueName',
                                name: 'tissueName',
                                id: 'cellName',
                                emptyText: 'Taxon Name',
                                store: sourceTissueTaxonNameStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 300,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            // console.log(records)
                                            var experimenter = Ext.getCmp("cellID");
                                            experimenter.clearValue();
                                            experimenter.store.load({
                                                params: {
                                                    id: records[0].data.tissueName
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'combobox',
                                displayField: 'tissueID',
                                valueField: 'tissueID',
                                emptyText: 'Taxon ID',
                                name: 'tissueID',
                                id: 'cellID',
                                store: sourceTissueTaxonIDStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 100,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            // console.log(records)
                                            var experimenter = Ext.getCmp("cellstrain");
                                            experimenter.clearValue();
                                            experimenter.store.load({
                                                params: {
                                                    id: records[0].data.tissueID
                                                }
                                            })
                                        }
                                    }
                                }
                            }]
                        }, {
                            xtype: 'combobox',
                            fieldLabel: 'Strain',
                            emptyText: 'Strain Name',
                            id: 'cellstrain',
                            queryMode: 'local',
                            valueField: 'tissueStrain',
                            displayField: 'tissueStrain',
                            name: 'tissueStrain',
                            store: sourceTissueTaxonStrainStore
                        }, {
                            xtype: 'combobox',
                            fieldLabel: 'Genotype',
                            displayField: 'Genotype',
                            name: 'Genotype',
                            store: genotypeStore,
                            editable: false
                        }, {
                            xtype: 'numberfield',
                            fieldLabel: 'Total number of Target Gene',
                            afterLabelTextTpl: required,
                            // id : 'Gene_num',
                            name: 'Gene_num',
                            minValue: 0,
                            maxValue: 10,
                            value: 0,
                            listeners: {
                                change: function(o, newV, oldV) {
                                    if (newV > 10) {
                                        alert('Number of Gene must be smaller than 10!')
                                        newV = 1
                                        Ext.getCmp('Gene_num').setValue(1)
                                    }
                                    if (oldV) {
                                        delGene('source_cell', oldV);
                                    }
                                    for (i = 1; i <= newV; i++) {
                                        addGene('source_cell', i + 3, i);
                                    }
                                }
                            },
                            width: 240
                        }, {
                            fieldLabel: 'Cell',
                            xtype: 'fieldcontainer',
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            items: [{
                                xtype: 'combobox',
                                displayField: 'source_CellType',
                                name: 'cellcelltype',
                                emptyText: 'Type',
                                valueField: 'source_CellType',
                                store: cellcellTypeStore,
                                queryMode: 'local',
                                width: 300,
                                editable: false,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            var lab = Ext.getCmp("cellcellname");
                                            lab.clearValue();
                                            lab.store.load({
                                                params: {
                                                    id: records[0].data.source_CellType
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'combobox',
                                displayField: 'Cell_Name',
                                emptyText: 'Name',
                                valueField: 'Cell_Name',
                                name: 'Cell_Name',
                                id: 'cellcellname',
                                store: cellnameStore,
                                queryMode: 'local',
                                width: 300,
                                editable: false
                            }]
                        }, 
                        // {
                        // fieldLabel : 'Target Gene',
                        // xtype : 'fieldcontainer',
                        // layout : {
                        // type : 'hbox',
                        // align : 'stretch'
                        // },
                        // items : [{
                        // xtype : 'textfield',
                        // emptyText : 'Gene Symbol',
                        // // fieldLabel : 'Target
                        // // Gene',
                        // name : 'geneSymbol',
                        // allowBlank : true
                        // }, {
                        // xtype : 'textfield',
                        // emptyText : 'Gene ID',
                        // // fieldLabel : 'Target
                        // // Gene',
                        // name : 'GeneID',
                        // allowBlank : true
                        // }, {
                        // xtype : 'combobox',
                        // displayField : 'Source_TissueTaxonID',
                        // valueField : 'Source_TissueTaxonID',
                        // emptyText : 'Gene Taxon',
                        // name : 'geneTaxon',
                        // store : geneIDStore,
                        // queryMode : 'local',
                        // allowBlank : true,
                        // width : 100
                        // }]
                        // },
                        {
                            xtype: 'timefield',
                            fieldLabel: 'CR Time',
                            format: 'G:i:s',
                            increment: 15,
                            name: 'circ_time',
                            allowBlank: true
                        }, {
                            xtype: 'textfield',
                            fieldLabel: 'Specific ID',
                            name: 'Specific_ID',
                            allowBlank: true
                        }]
                    });
                    var source_fluid = Ext.create('Ext.form.Panel', {
                        id: 'source_fluid',
                        title: 'Fluid & Excreta',
                        border: true,
                        bodyPadding: 10,
                        // frame : true,
                        headerPosition: 'left',
                        defaults: {
                            labelWidth: 120,
                            labelAligh: 'left',
                            width: 800,
                            allowBlank: false
                        },
                        items: [{
                            fieldLabel: 'Taxon',
                            xtype: 'fieldcontainer',
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            items: [{
                                xtype: 'combobox',
                                displayField: 'Source_TissueTaxonAorM',
                                name: 'Source_TissueTaxonAorM',
                                valueField: 'Source_TissueTaxonAorM',
                                store: new Ext.data.SimpleStore({
                                    fields: ["Source_TissueTaxonAorM"],
                                    data: [["Animal"], ["Plant"]]
                                }),
                                queryMode: 'local',
                                allowBlank: false,
                                emptyText: 'Animal/Plant',
                                width: 120,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            var lab = Ext.getCmp("fluidName");
                                            lab.clearValue();
                                            lab.store.load({
                                                params: {
                                                    id: records[0].data.Source_TissueTaxonAorM
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'combobox',
                                displayField: 'tissueName',
                                valueField: 'tissueName',
                                emptyText: 'Taxon Name',
                                name: 'tissueName',
                                id: 'fluidName',
                                store: sourceTissueTaxonNameStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 300,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            // console.log(records)
                                            var experimenter = Ext.getCmp("fluidID");
                                            experimenter.clearValue();
                                            experimenter.store.load({
                                                params: {
                                                    id: records[0].data.tissueName
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'combobox',
                                displayField: 'tissueID',
                                valueField: 'tissueID',
                                emptyText: 'Taxon ID',
                                name: 'tissueID',
                                id: 'fluidID',
                                store: sourceTissueTaxonIDStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 100,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            // console.log(records)
                                            var experimenter = Ext.getCmp("fluidstrain");
                                            experimenter.clearValue();
                                            experimenter.store.load({
                                                params: {
                                                    id: records[0].data.tissueID
                                                }
                                            })
                                        }
                                    }
                                }
                            }]
                        }, {
                            xtype: 'combobox',
                            fieldLabel: 'Strain',
                            id: 'fluidstrain',
                            valueField: 'tissueStrain',
                            emptyText: 'Strain Name',
                            displayField: 'tissueStrain',
                            name: 'tissueStrain',
                            queryMode: 'local',
                            store: sourceTissueTaxonStrainStore
                        }, {
                            fieldLabel: 'Age',
                            xtype: 'fieldcontainer',
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            items: [{
                                xtype: 'textfield',
                                // fieldLabel : 'Target
                                // Gene',
                                name: 'tissue_age'
                            }, {
                                xtype: 'combobox',
                                displayField: 'All_AgeUnit',
                                valueField: 'All_AgeUnit',
                                name: 'All_AgeUnit',
                                // id : 'tissueName',
                                store: allAgeUnitStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 180
                            }]
                        }, {
                            xtype: 'combobox',
                            fieldLabel: 'Gender',
                            displayField: 'Tissue_gender',
                            name: 'Tissue_gender',
                            store: tissueGenderStore
                        }, {
                            xtype: 'combobox',
                            fieldLabel: 'Genotype',
                            displayField: 'Genotype',
                            name: 'Genotype',
                            store: genotypeStore,
                            editable: false
                        }, {
                            xtype: 'numberfield',
                            fieldLabel: 'Total number of Target Gene',
                            afterLabelTextTpl: required,
                            // id : 'Gene_num',
                            name: 'Gene_num',
                            minValue: 0,
                            maxValue: 10,
                            value: 0,
                            listeners: {
                                change: function(o, newV, oldV) {
                                    if (newV > 10) {
                                        alert('Number of Gene must be smaller than 10!')
                                        newV = 1
                                        Ext.getCmp('Gene_num').setValue(1)
                                    }
                                    if (oldV) {
                                        delGene('source_fluid', oldV);
                                    }
                                    for (i = 1; i <= newV; i++) {
                                        addGene('source_fluid', i + 5, i);
                                    }
                                }
                            },
                            width: 240
                        }, 
                        // {
                        // fieldLabel : 'Target Gene',
                        // xtype : 'fieldcontainer',
                        // layout : {
                        // type : 'hbox',
                        // align : 'stretch'
                        // },
                        // items : [{
                        // xtype : 'textfield',
                        // emptyText : 'Gene Symbol',
                        // // fieldLabel : 'Target
                        // // Gene',
                        // name : 'geneSymbol',
                        // allowBlank : true
                        // }, {
                        // xtype : 'textfield',
                        // emptyText : 'Gene ID',
                        // // fieldLabel : 'Target
                        // // Gene',
                        // name : 'GeneID',
                        // allowBlank : true
                        // }, {
                        // xtype : 'combobox',
                        // displayField : 'Source_TissueTaxonID',
                        // valueField : 'Source_TissueTaxonID',
                        // emptyText : 'Gene Taxon',
                        // name : 'geneTaxon',
                        // store : geneIDStore,
                        // queryMode : 'local',
                        // allowBlank : false,
                        // width : 100,
                        // allowBlank : true
                        // }]
                        // },
                        {
                            xtype: 'combobox',
                            store: fluidNameStore,
                            fieldLabel: 'Fluid/Excreta',
                            displayField: 'Fluid_name',
                            name: 'Fluid_name',
                            valueField: 'Fluid_name',
                            editable: false
                        }, {
                            xtype: 'textfield',
                            fieldLabel: 'Specific ID',
                            name: 'Specific_ID',
                            allowBlank: true
                        }]
                    });
                    var source_others = Ext.create('Ext.form.Panel', {
                        title: 'Others',
                        border: true,
                        // frame : true,
                        bodyPadding: 10,
                        headerPosition: 'left',
                        defaults: {
                            labelWidth: 120,
                            labelAligh: 'left',
                            width: 450,
                            allowBlank: false
                        },
                        items: [{
                            xtype: 'textareafield',
                            fieldLabel: 'Others',
                            name: 'tissue_others'
                        }]
                    });
                    // rx panel
                    var addTreatment = function(index, treatnum) {
                        var rxPanel = Ext.create('Ext.form.Panel', {
                            title: 'Treatment' + treatnum,
                            id: 'Treatment' + treatnum,
                            border: true,
                            bodyPadding: 10,
                            layout: 'anchor',
                            headerPosition: 'top',
                            defaults: {
                                labelWidth: 120,
                                labelAligh: 'left',
                                width: 800,
                                allowBlank: false
                            },
                            items: [{
                                xtype: 'fieldcontainer',
                                layout: {
                                    type: 'hbox',
                                    align: 'stretch'
                                },
                                items: [{
                                    xtype: 'combobox',
                                    fieldLabel: 'Treatments',
                                    displayField: 'Rx_treatment',
                                    name: 'Rx_treatment' + treatnum,
                                    store: rxTreatmentStore,
                                    queryMode: 'local',
                                    labelWidth: 120,
                                    width: 415,
                                    allowBlank: false,
                                    listeners: {
                                        select: {
                                            fn: function(combo, records, index) {
                                                var lab = Ext.getCmp("treantment_detail" + treatnum);
                                                lab.clearValue();
                                                lab.store.load({
                                                    params: {
                                                        id: records[0].data.Rx_treatment
                                                    }
                                                })
                                            }
                                        },
                                        change: {
                                            fn: function(combo, newValue, oldValue) {
                                                // console.log(box)
                                                var sample = {
                                                    fieldLabel: 'New Target Gene ',
                                                    xtype: 'fieldcontainer',
                                                    id: 'New_target_Gene' + treatnum,
                                                    layout: {
                                                        type: 'hbox',
                                                        align: 'stretch'
                                                    },
                                                    items: [{
                                                        xtype: 'textfield',
                                                        emptyText: 'Gene Symbol',
                                                        // fieldLabel : 'Target
                                                        // Gene',
                                                        name: 'newGeneSymbol' + treatnum,
                                                        allowBlank: true
                                                    }, {
                                                        xtype: 'textfield',
                                                        emptyText: 'Gene ID',
                                                        // fieldLabel : 'Target
                                                        // Gene',
                                                        name: 'newGeneID' + treatnum,
                                                        allowBlank: true
                                                    }, {
                                                        xtype: 'combobox',
                                                        displayField: 'Source_TissueTaxonID',
                                                        valueField: 'Source_TissueTaxonID',
                                                        emptyText: 'Gene Taxon',
                                                        name: 'newGeneTaxon' + treatnum,
                                                        store: geneIDStore,
                                                        queryMode: 'local',
                                                        allowBlank: true,
                                                        width: 100
                                                    }]
                                                };
                                                var sample2 = {
                                                    xtype: 'fieldcontainer',
                                                    id: 'samp-treat-unit' + treatnum,
                                                    layout: {
                                                        type: 'hbox',
                                                        align: 'stretch'
                                                    },
                                                    items: [{
                                                        xtype: 'textfield',
                                                        fieldLabel: 'Amount',
                                                        name: 'amount' + treatnum,
                                                        width: 180,
                                                        labelWidth: 120,
                                                        allowBlank: true
                                                    }, {
                                                        xtype: 'combobox',
                                                        displayField: 'Rx_unit',
                                                        name: 'Rx_unit' + treatnum,
                                                        store: rxUnitStore,
                                                        queryMode: 'local',
                                                        emptyText: 'Param type',
                                                        allowBlank: true,
                                                        listeners: {
                                                            change: {
                                                                fn: function(box, newValue, oldValue) {
                                                                    // console.log(box)
                                                                    var detailPanel = Ext.create('Ext.form.ComboBox', {
                                                                        id: 'unit_detail_' + treatnum,
                                                                        displayField: 'unit_detail',
                                                                        name: 'unit_detail_' + treatnum,
                                                                        store: rxUnitDetailStore,
                                                                        queryMode: 'local',
                                                                        emptyText: 'Param unit',
                                                                        editable: false,
                                                                        allowBlank: true
                                                                    })
                                                                    var detailPanel2 = {
                                                                        xtype: 'fieldcontainer',
                                                                        id: 'unit_detail2_' + treatnum,
                                                                        layout: {
                                                                            type: 'hbox',
                                                                            align: 'stretch'
                                                                        },
                                                                        items: [{
                                                                            xtype: 'combobox',
                                                                            // id :
                                                                            // 'detailPanel2-1',
                                                                            valueField: 'rx_dur_unit',
                                                                            displayField: 'rx_dur_unit',
                                                                            name: 'unit_detail2_' + treatnum,
                                                                            store: new Ext.data.SimpleStore({
                                                                                fields: ["rx_dur_unit"],
                                                                                data: [["L"], ["mL"], ["ng"], ["g"], ["kg"], ["mol"], ["mmol"]]
                                                                            })
                                                                        }, {
                                                                            xtype: 'displayfield',
                                                                            // id :
                                                                            // 'detailPanel2-2',
                                                                            value: ' / '
                                                                        }, {
                                                                            xtype: 'combobox',
                                                                            // id :
                                                                            // 'detailPanel22-1',
                                                                            valueField: 'rx_dur_unit',
                                                                            displayField: 'rx_dur_unit',
                                                                            name: 'unit_detail22_' + treatnum,
                                                                            store: new Ext.data.SimpleStore({
                                                                                fields: ["rx_dur_unit"],
                                                                                data: [["L"], ["mL"], ["uL"], ["nL"], ["Kg"], ["g"], ["mg"]]
                                                                            })
                                                                        }]
                                                                    }
                                                                    var temp = Ext.getCmp('samp-treat-unit' + treatnum);
                                                                    if (oldValue != 'Concentration')
                                                                        temp.remove(Ext.getCmp('unit_detail_' + treatnum), false)
                                                                    else if (oldValue == 'Concentration') {
                                                                        temp.remove(Ext.getCmp('unit_detail2_' + treatnum), false)
                                                                    }
                                                                    if (newValue != 'Concentration') {
                                                                        detailPanel.clearValue()
                                                                        detailPanel.store.load({
                                                                            params: {
                                                                                id: newValue
                                                                            }
                                                                        })
                                                                        temp.insert(2, detailPanel)
                                                                    } else if (newValue == 'Concentration') {
                                                                        temp.insert(2, detailPanel2)
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }]
                                                }
                                                var temp = Ext.getCmp('Treatment' + treatnum);
                                                // console.log(temp.items.items[2].id)
                                                // console.log(temp.items)
                                                // if (newValue != 'Gene Engineering') {
                                                // if ('New_target_Gene' + treatnum ==
                                                // temp.items.items[2].id){
                                                temp.remove(temp.items.items[1], false)
                                                // }
                                                // }
                                                if (newValue == 'Gene Engineering')
                                                    temp.insert(1, sample)
                                                else {
                                                    temp.insert(1, sample2)
                                                }
                                            }
                                        }
                                    }
                                }, {
                                    xtype: 'combobox',
                                    id: 'treantment_detail' + treatnum,
                                    // fieldLabel :
                                    // 'Treatments',
                                    displayField: 'all_detail',
                                    name: 'all_detail' + treatnum,
                                    store: rxTreatmentDetailStore,
                                    queryMode: 'local',
                                    labelWidth: 120,
                                    allowBlank: true
                                }]
                            }, {
                                xtype: 'fieldcontainer',
                                id: 'samp-treat-unit' + treatnum,
                                layout: {
                                    type: 'hbox',
                                    align: 'stretch'
                                },
                                items: [{
                                    xtype: 'textfield',
                                    fieldLabel: 'Amount',
                                    name: 'amount' + treatnum,
                                    width: 180,
                                    labelWidth: 120,
                                    allowBlank: true
                                }, {
                                    xtype: 'combobox',
                                    displayField: 'Rx_unit',
                                    name: 'Rx_unit' + treatnum,
                                    store: rxUnitStore,
                                    queryMode: 'local',
                                    emptyText: 'Param type',
                                    allowBlank: true,
                                    listeners: {
                                        change: {
                                            fn: function(box, newValue, oldValue) {
                                                // console.log(box)
                                                var detailPanel = Ext.create('Ext.form.ComboBox', {
                                                    id: 'unit_detail_' + treatnum,
                                                    displayField: 'unit_detail',
                                                    name: 'unit_detail' + treatnum,
                                                    store: rxUnitDetailStore,
                                                    queryMode: 'local',
                                                    emptyText: 'Param unit',
                                                    editable: false,
                                                    allowBlank: true
                                                })
                                                var detailPanel2 = {
                                                    xtype: 'fieldcontainer',
                                                    id: 'unit_detail2_' + treatnum,
                                                    layout: {
                                                        type: 'hbox',
                                                        align: 'stretch'
                                                    },
                                                    items: [{
                                                        xtype: 'combobox',
                                                        // id : 'detailPanel2-1',
                                                        valueField: 'rx_dur_unit',
                                                        displayField: 'rx_dur_unit',
                                                        name: 'unit_detail2' + treatnum,
                                                        store: new Ext.data.SimpleStore({
                                                            fields: ["rx_dur_unit"],
                                                            data: [["L"], ["mL"], ["ng"], ["g"], ["kg"], ["mol"], ["mmol"]]
                                                        })
                                                    }, {
                                                        xtype: 'displayfield',
                                                        // id : 'detailPanel2-2',
                                                        value: ' / '
                                                    }, {
                                                        xtype: 'combobox',
                                                        // id : 'detailPanel22-1',
                                                        valueField: 'rx_dur_unit',
                                                        displayField: 'rx_dur_unit',
                                                        name: 'unit_detail22' + treatnum,
                                                        store: new Ext.data.SimpleStore({
                                                            fields: ["rx_dur_unit"],
                                                            data: [["L"], ["mL"], ["uL"], ["nL"], ["Kg"], ["g"], ["mg"]]
                                                        })
                                                    }]
                                                }
                                                var temp = Ext.getCmp('samp-treat-unit' + treatnum);
                                                if (oldValue != 'Concentration')
                                                    temp.remove(Ext.getCmp('unit_detail_' + treatnum), false)
                                                else if (oldValue == 'Concentration') {
                                                    temp.remove(Ext.getCmp('unit_detail2_' + treatnum), false)
                                                }
                                                if (newValue != 'Concentration') {
                                                    detailPanel.clearValue()
                                                    detailPanel.store.load({
                                                        params: {
                                                            id: newValue
                                                        }
                                                    })
                                                    temp.insert(2, detailPanel)
                                                } else if (newValue == 'Concentration') {
                                                    temp.insert(2, detailPanel2)
                                                }
                                            }
                                        }
                                    }
                                }]
                            }, {
                                xtype: 'fieldcontainer',
                                fieldLabel: 'Duration',
                                layout: {
                                    type: 'hbox',
                                    align: 'stretch'
                                },
                                items: [{
                                    xtype: 'textfield',
                                    name: 'duration' + treatnum,
                                    labelWidth: 120,
                                    allowBlank: true
                                }, {
                                    xtype: 'combobox',
                                    displayField: 'rx_dur_unit',
                                    name: 'rx_dur_unit' + treatnum,
                                    valueField: 'rx_dur_unit',
                                    store: new Ext.data.SimpleStore({
                                        fields: ["rx_dur_unit"],
                                        data: [["Week"], ["Day"], ["Hour"], ["Minute"], ["Second"]]
                                    }),
                                    queryMode: 'local',
                                    width: 200
                                }]
                            }]
                        });
                        formPanel.insert(index, rxPanel);
                    }
                    ;
                    var delTreatment = function(samplenum) {
                        for (i = samplenum; i > 0; i--) {
                            var sample = Ext.getCmp('Treatment' + i);
                            formPanel.remove(sample);
                        }
                    }
                    ;
                    // var rxPanel = Ext.create('Ext.form.Panel', {
                    // title : 'Treatment',
                    // border : true,
                    // bodyPadding : 10,
                    // // frame : true,
                    // // bodyStyle : 'padding: 5 5 0',
                    // layout : 'anchor',
                    // headerPosition : 'top',
                    // defaults : {
                    // labelWidth : 120,
                    // labelAligh : 'left',
                    // width : 800,
                    // allowBlank : false
                    // },
                    // items : [{
                    // xtype : 'fieldcontainer',
                    // layout : {
                    // type : 'hbox',
                    // align : 'stretch'
                    // },
                    // items : [{
                    // xtype : 'combobox',
                    // fieldLabel : 'Treatments',
                    // displayField : 'Rx_treatment',
                    // name : 'Rx_treatment',
                    // store : rxTreatmentStore,
                    // queryMode : 'local',
                    // labelWidth : 120,
                    // width : 415,
                    // allowBlank : false,
                    // listeners : {
                    // select : {
                    // fn : function(combo, records, index) {
                    // var lab = Ext.getCmp("treantment_detail");
                    // lab.clearValue();
                    // lab.store.load({
                    // params : {
                    // id : records[0].data.Rx_treatment
                    // }
                    // })
                    // }
                    // }
                    // }
                    // }, {
                    // xtype : 'combobox',
                    // id : 'treantment_detail',
                    // // fieldLabel :
                    // // 'Treatments',
                    // displayField : 'all_detail',
                    // name : 'all_detail',
                    // store : rxTreatmentDetailStore,
                    // queryMode : 'local',
                    // labelWidth : 120,
                    // allowBlank : true
                    // }]
                    // }, {
                    // xtype : 'fieldcontainer',
                    // id : 'samp-treat-unit',
                    // layout : {
                    // type : 'hbox',
                    // align : 'stretch'
                    // },
                    // items : [{
                    // xtype : 'textfield',
                    // fieldLabel : 'Amount',
                    // name : 'amount',
                    // width : 180,
                    // labelWidth : 120,
                    // allowBlank : true
                    // }, {
                    // xtype : 'combobox',
                    // displayField : 'Rx_unit',
                    // name : 'Rx_unit',
                    // store : rxUnitStore,
                    // queryMode : 'local',
                    // emptyText : 'Param type',
                    // allowBlank : true,
                    // listeners : {
                    // change : {
                    // fn : function(box, newValue, oldValue) {
                    // // console.log(box)
                    // var temp = Ext.getCmp('samp-treat-unit');
                    // if (oldValue != 'Concentration')
                    // temp.remove(detailPanel, false)
                    // else if (oldValue == 'Concentration') {
                    // temp.remove(Ext.getCmp('unit_detail2'), false)
                    // }
                    // if (newValue != 'Concentration') {
                    // detailPanel.clearValue()
                    // detailPanel.store.load({
                    // params : {
                    // id : newValue
                    // }
                    // })
                    // temp.insert(2, detailPanel)
                    // } else if (newValue == 'Concentration') {
                    // temp.insert(2, detailPanel2)
                    // }
                    // }
                    // }
                    // }
                    // }]
                    // }, {
                    // xtype : 'fieldcontainer',
                    // layout : {
                    // type : 'hbox',
                    // align : 'stretch'
                    // },
                    // items : [{
                    // xtype : 'textfield',
                    // name : 'duration',
                    // fieldLabel : 'Duration',
                    // labelWidth : 120,
                    // allowBlank : true
                    // }, {
                    // xtype : 'combobox',
                    // displayField : 'rx_dur_unit',
                    // name : 'rx_dur_unit',
                    // valueField : 'rx_dur_unit',
                    // store : new Ext.data.SimpleStore({
                    // fields : ["rx_dur_unit"],
                    // data : [["Week"], ["Day"], ["Hour"], ["Minute"], ["Second"]]
                    // }),
                    // queryMode : 'local',
                    // width : 200
                    // }]
                    // }]
                    // });
                    var ubiPanel = Ext.create('Ext.form.Panel', {
                        title: 'Information',
                        border: true,
                        // frame : true,
                        bodyPadding: 10,
                        headerPosition: 'top',
                        defaults: {
                            labelWidth: 120,
                            labelAligh: 'left',
                            width: 800,
                            allowBlank: false
                        },
                        items: [{
                            xtype: 'fieldcontainer',
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            items: [{
                                xtype: 'combobox',
                                fieldLabel: 'Subcelluar Organelle',
                                name: 'Ubi_subcell',
                                displayField: 'Ubi_subcell',
                                store: ubiSubcellStore,
                                queryMode: 'local',
                                //queryMode : true,
                                multiSelect: true,
                                editable: true,
                                labelWidth: 120,
                                width: 415,
                                allowBlank: false
                            }]
                        }, {
                            xtype: 'fieldcontainer',
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            items: [{
                                xtype: 'combobox',
                                valueField: 'Ubi_method',
                                fieldLabel: 'Protocol',
                                displayField: 'Ubi_method',
                                name: 'Ubi_method',
                                store: ubiMethodStore,
                                // queryMode : 'local',
                                multiSelect: false,
                                labelWidth: 120,
                                width: 800,
                                allowBlank: false
                            }]
                        }, /*
                                             * { xtype : 'combobox', name : 'Ubi_detergent', displayField :
                                             * 'Ubi_detergent', fieldLabel : 'Detergent', store : ubiDetergentStore },
                                             */{
                            xtype: 'textfield',
                            name: 'Ubi_salt',
                            // displayField : 'Ubi_salt',
                            fieldLabel: 'Salt'
                            // store : ubiSaltStore
                        }]
                    });
                    var commentsPanel = Ext.create('Ext.form.Panel', {
                        title: 'Comments',
                        border: true,
                        // frame : true,
                        bodyPadding: 10,
                        headerPosition: 'top',
                        defaults: {
                            labelWidth: 120,
                            // labelAlign : 'top',
                            width: 800
                            // allowBlank : false
                        },
                        items: [{
                            xtype: 'textareafield',
                            name: 'comments',
                            fieldLabel: 'Extra Comments'
                        }, 
                        //                                      {
                        //                                          xtype : 'textfield',
                        //                                          // fieldLabel : 'Target
                        //                                          // Gene',
                        //                                          name : 'Ispec_num',
                        //                                          fieldLabel : 'Ispec No',
                        //                                          width : 400
                        //                                      },
                        {
                            xtype: 'textfield',
                            name: 'Ispec_num',
                            fieldLabel: 'Ispec No',
                            labelWidth: 120,
                            allowBlank: true
                        }
                        ]
                    });
                    var buttonPanel = Ext.create('Ext.panel.Panel', {
                        // frame : true,
                        // renderTo: 'button',
                        buttonAlign: "center",
                        buttons: [{
                            text: 'Submit',
                            handler: submitForm
                        }, {
                            text: 'Cancel',
                            handler: cancelForm
                        }]
                    });
                    var formPanel = Ext.create('Ext.form.Panel', {
                        id: timestamp,
                        // renderTo : 'form',
                        overflowY: 'scroll',
                        items: [generalPanel, ubiPanel, commentsPanel, buttonPanel]
                    });
                    // console.log(timestamp)
                    // event listener for type radio
                    typeradio = Ext.getCmp('cell_tissue' + timestamp);
                    typeradio.on('change', function(radio, newV, oldV, e) {
                        if (oldV.cell_tissue == 'Tissue') {
                            formPanel.remove(source_tissue, false);
                        } else if (oldV.cell_tissue == 'Cell') {
                            formPanel.remove(source_cell, false);
                        } else if (oldV.cell_tissue == 'Fluid') {
                            formPanel.remove(source_fluid, false);
                        } else if (oldV.cell_tissue == 'Others') {
                            formPanel.remove(source_others, false);
                        }
                        if (newV.cell_tissue == 'Tissue') {
                            formPanel.insert(1, source_tissue);
                        } else if (newV.cell_tissue == 'Cell') {
                            formPanel.insert(1, source_cell);
                        } else if (newV.cell_tissue == 'Fluid') {
                            formPanel.insert(1, source_fluid);
                        } else if (newV.cell_tissue == 'Others') {
                            formPanel.insert(1, source_others);
                        }
                    });
                    // For Container
                    var RefrigeratorNoStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Refrigerator_No/',
                            reader: {
                                type: 'json',
                                root: 'Refrigerator_Nos'
                            }
                        },
                        fields: [{
                            name: 'Refrigerator_No',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var RefrigeratorTemperStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Refrigerator_Temperature/',
                            reader: {
                                type: 'json',
                                root: 'Refrigerator_Temperatures'
                            }
                        },
                        fields: [{
                            name: 'Refrigerator_Temperature',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var RefrigeratorLayerStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Refrigerator_Layer/',
                            reader: {
                                type: 'json',
                                root: 'Refrigerator_Layers'
                            }
                        },
                        fields: [{
                            name: 'Refrigerator_Layer',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var RefrigeratorPanel = Ext.create('Ext.container.Container', {
                        // id : 'Location-Refrigerator',
                        layout: {
                            type: 'hbox'
                        },
                        defaults: {
                            labelWidth: 120,
                            width: 800
                        },
                        items: [{
                            xtype: 'combobox',
                            emptyText: 'Refrigerator No.',
                            fieldLabel: '#Refrigerator',
                            displayField: 'Refrigerator_No',
                            name: 'RefrigeratorNo',
                            store: RefrigeratorNoStore,
                            typeAhead: true,
                            width: 300
                        }, {
                            xtype: 'combobox',
                            emptyText: 'Temperature',
                            displayField: 'Refrigerator_Temperature',
                            name: 'RefrigeratorTemper',
                            store: RefrigeratorTemperStore,
                            typeAhead: true,
                            width: 300
                        }, {
                            xtype: 'combobox',
                            emptyText: 'Refrigerator Layer',
                            displayField: 'Refrigerator_Layer',
                            name: 'RefrigeratorLayer',
                            store: RefrigeratorLayerStore,
                            typeAhead: true,
                            width: 300
                        }]
                    })
                    // nitrogen-panel
                    var NitrogenContStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Nitrogen_Container/',
                            reader: {
                                type: 'json',
                                root: 'Nitrogen_Containers'
                            }
                        },
                        fields: [{
                            name: 'Nitrogen_Container',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var NitrogenBasketStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Nitrogen_Basket/',
                            reader: {
                                type: 'json',
                                root: 'Nitrogen_Baskets'
                            }
                        },
                        fields: [{
                            name: 'Nitrogen_Basket',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var NitrogenLayerStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Nitrogen_Layer/',
                            reader: {
                                type: 'json',
                                root: 'Nitrogen_Layers'
                            }
                        },
                        fields: [{
                            name: 'Nitrogen_Layer',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var NitrogenPanel = Ext.create('Ext.container.Container', {
                        // id : 'Location-Refrigerator',
                        layout: {
                            type: 'hbox'
                        },
                        defaults: {
                            labelWidth: 120,
                            width: 800
                        },
                        items: [{
                            xtype: 'combobox',
                            emptyText: 'Container No.',
                            fieldLabel: '#Liquid Nitrogen',
                            displayField: 'Nitrogen_Container',
                            name: 'Nitrogen_Container',
                            store: NitrogenContStore,
                            typeAhead: true,
                            width: 300
                        }, {
                            xtype: 'combobox',
                            emptyText: 'Nitrogen Basket',
                            displayField: 'Nitrogen_Basket',
                            name: 'Nitrogen_Basket',
                            store: NitrogenBasketStore,
                            typeAhead: true,
                            width: 300
                        }, {
                            xtype: 'combobox',
                            emptyText: 'Nitrogen Layer',
                            displayField: 'Nitrogen_Layer',
                            name: 'Nitrogen_Layer',
                            store: NitrogenLayerStore,
                            typeAhead: true,
                            width: 300
                        }]
                    })
                    // others
                    var OtherTemperStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Others_Temperature/',
                            reader: {
                                type: 'json',
                                root: 'Others_Temperatures'
                            }
                        },
                        fields: [{
                            name: 'Others_Temperature',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var OtherTemperPanel = Ext.create('Ext.container.Container', {
                        // id : 'Location-Refrigerator',
                        layout: {
                            type: 'hbox'
                        },
                        defaults: {
                            labelWidth: 120,
                            width: 800
                        },
                        items: [{
                            xtype: 'combobox',
                            emptyText: 'Temperature',
                            fieldLabel: '#Others',
                            displayField: 'Others_Temperature',
                            name: 'Others_Temperature',
                            store: OtherTemperStore,
                            typeAhead: true,
                            width: 300
                        }, {
                            xtype: 'textfield',
                            emptyText: 'Location',
                            name: 'Others_location',
                            width: 300
                        }]
                    })
                    typeradio = Ext.getCmp('location' + timestamp);
                    typeradio.on('change', function(radio, newV, oldV, e) {
                        // console.log(oldV)
                        // console.log(newV)
                        if (oldV.location == 'Refrigerator') {
                            generalPanel.remove(RefrigeratorPanel, false)
                        } else if (oldV.location == 'Liquid Nitrogen') {
                            generalPanel.remove(NitrogenPanel, false)
                        } else if (oldV.location == 'Others') {
                            generalPanel.remove(OtherTemperPanel, false)
                        }
                        if (newV.location == 'Refrigerator') {
                            generalPanel.insert(4, RefrigeratorPanel);
                        } else if (newV.location == 'Liquid Nitrogen') {
                            generalPanel.insert(4, NitrogenPanel);
                        } else if (newV.location == 'Others') {
                            generalPanel.insert(4, OtherTemperPanel);
                        }
                    });
                    tab = Ext.getCmp('content-panel')
                    tab.add({
                        id: 'add_sample_tab',
                        title: 'Add Sample',
                        iconCls: 'addsample',
                        closable: true,
                        layout: 'fit',
                        items: [formPanel]
                    }).show()
                }
            },
            '#addreagent': {
                click: function() {
                    var panel = Ext.getCmp('add_reagent_tab');
                    if (panel) {
                        var main = Ext.getCmp("content-panel");
                        main.setActiveTab(panel);
                        return 0;
                    }
                    var timestamp = 'compare' + (new Date()).valueOf();
                    var add_application = function() {
                        var win = new Ext.Window({
                            title: 'ADD Application',
                            width: 320,
                            items: [{
                                xtype: 'form',
                                border: false,
                                // frame : true,
                                bodyPadding: 10,
                                id: 'application_form' + timestamp,
                                items: [{
                                    xtype: 'textfield',
                                    labelWidth: 90,
                                    labelAligh: 'left',
                                    width: 250,
                                    fieldLabel: 'Application',
                                    name: 'Application'
                                }]
                            }],
                            bbar: ['->', {
                                text: 'Submit',
                                handler: function() {
                                    application_form = Ext.getCmp('application_form' + timestamp);
                                    var newV = application_form.items.items[0].value;
                                    applicationStore.add({
                                        Application: newV
                                    });
                                    win.close();
                                }
                            }]
                        });
                        win.show();
                    }
                    ;
                    var add_react_pecies = function() {
                        var win = new Ext.Window({
                            title: 'ADD React Species',
                            width: 400,
                            items: [{
                                xtype: 'form',
                                border: true,
                                // frame : true,
                                id: 'species_form' + timestamp,
                                items: [{
                                    xtype: 'textfield',
                                    labelWidth: 120,
                                    labelAligh: 'left',
                                    width: 450,
                                    fieldLabel: 'React Species',
                                    name: 'React Species'
                                }]
                            }],
                            bbar: ['->', {
                                text: 'Submit',
                                handler: function() {
                                    species_form = Ext.getCmp('species_form' + timestamp);
                                    var newV = species_form.items.items[0].value;
                                    reactSpeciesStore.add({
                                        React_species: newV
                                    });
                                    win.close();
                                }
                            }]
                        });
                        win.show();
                    }
                    ;
                    // CSRF protection
                    csrftoken = Ext.util.Cookies.get('csrftoken');
                    // function: submit / canel form
                    var submitForm = function() {
                        formpanel = Ext.getCmp(timestamp);
                        var form = formpanel.getForm();
                        //var currentTime = Ext.Date.format(new Date(), 'n/d/Y');
                        //Ext.getCmp("gar.app.control.Menu.addreagentId").items.items[4].setValue(currentTime)
                        if (form.isValid()) {
                            Ext.Ajax.timeout = 180000;
                            form.submit({
                                url: '/experiments/save/reagent/',
                                waitMsg: 'Adding Reagent......',
                                //timeout : 300000,
                                // standardSubmit : true
                                success: function(frm, act) {
                                    val = String(act.result.msg);
                                    len = val.legnth
                                    // console.log(len)
                                    // val=val.substring(1)
                                    if (val.length < 6) {
                                        for (i = val.length; i < 6; i++)
                                            val = '0' + val
                                    }
                                    Ext.Msg.alert('Success', 'Add a reagent successfully. Reagent No: ' + val);
                                },
                                failure: function(form, action) {
                                    Ext.Msg.alert('Failed', 'Add a reagent unsuccessfully. Contact admin.');
                                }
                            })
                        }
                    }
                    ;
                    var cancelForm = function() {
                        formpanel = Ext.getCmp(timestamp);
                        formpanel.getForm().reset();
                    }
                    ;
                    // Manufactorer Store
                    var companyStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/all_company/',
                            reader: {
                                type: 'json',
                                root: 'all_company'
                            }
                        },
                        fields: [{
                            name: 'company',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var labStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/all_lab/',
                            reader: {
                                type: 'json',
                                root: 'all_lab'
                            }
                        },
                        fields: [{
                            name: 'lab',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var experimenterStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/all_experimenter/',
                            reader: {
                                type: 'json',
                                root: 'experimenters'
                            }
                        },
                        fields: [{
                            name: 'experimenter',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var reagentManufacturerStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Reagent_manufacturer/',
                            reader: {
                                type: 'json',
                                root: 'Reagent_manufacturers'
                            }
                        },
                        fields: [{
                            name: 'Reagent_manufacturer',
                            type: 'string'
                        }],
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
                        fields: [{
                            name: 'React_species',
                            type: 'string'
                        }],
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
                        fields: [{
                            name: 'Antigen_clonal_type',
                            type: 'string'
                        }],
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
                        fields: [{
                            name: 'Antigen_species',
                            type: 'string'
                        }],
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
                        fields: [{
                            name: 'Antigen_modification',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    // Purification Store
                    var purificationStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Purification/',
                            reader: {
                                type: 'json',
                                root: 'Purifications'
                            }
                        },
                        fields: [{
                            name: 'Purification',
                            type: 'string'
                        }],
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
                        fields: [{
                            name: 'Conjugate',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    // Affinity Store
                    var affinityStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/display/Affinity/',
                            reader: {
                                type: 'json',
                                root: 'Affinitys'
                            }
                        },
                        fields: [{
                            name: 'Affinity',
                            type: 'string'
                        }],
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
                        fields: [{
                            name: 'Application',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    
                    var reagentTemplateStore = Ext.create('Ext.data.Store', {
                        fields: [{
                            name: 'reagent_no',
                            type: 'string'
                        }],
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/reagent_no/',
                            reader: {
                                type: 'json',
                                root: 'reagent_no'
                            }
                        },
                        autoLoad: true
                    });
                    // general panel information
                    var general = Ext.create('Ext.panel.Panel', {
                        id: "gar.app.control.Menu.addreagentId",
                        title: 'General',
                        // frame : true,
                        layout: 'auto',
                        headerPosition: 'top',
                        bodyPadding: 10,
                        defaults: {
                            labelWidth: 120,
                            labelAligh: 'left',
                            width: 800,
                            allowBlank: false
                        },
                        items: [{
                            xtype: 'combobox',
                            fieldLabel: 'Choose template',
                            displayField: 'reagent_no',
                            name: 'reagent-template',
                            store: reagentTemplateStore,
                            
                            //Are u sure queryModel is a config param?
                            // queryModel : true,
                            
                            queryMode: 'local',
                            typeAhead: true,
                            allowBlank: true,
                            listeners: {
                                select: function() {
                                    var cmpLocation = Ext.getCmp("gar.app.control.Menu.addreagentId");
                                    var templateNo = cmpLocation.items.items[0].value;
                                    console.log(templateNo);
                                    
                                    Ext.Ajax.request({
                                        url: '/experiments/load/reagent/',
                                        params: {
                                            reagent_no: templateNo
                                            // csrfmiddlewaretoken : csrftoken
                                        },
                                        success: function(response) {
                                            //var panel = Ext.create('gar.view.Experiment_detail')
                                            var text = response.responseText;
                                            responseJson = Ext.JSON.decode(text).data;
                                            console.log(responseJson.reagent_type);
                                            var reagentType = responseJson.reagent_type;
                                            var reagent_type_loc = cmpLocation.items.items[2];
                                            if (reagentType == "Antigen") {
                                                reagent_type_loc.items.items[0].setValue(true);
                                            } 
                                            else if (reagentType == "DNA") {
                                                reagent_type_loc.items.items[1].setValue(true);
                                            } 
                                            else if (reagentType == "Protein") {
                                                reagent_type_loc.items.items[2].setValue(true);
                                            } 
                                            else if (reagentType == "chemical") {
                                                reagent_type_loc.items.items[3].setValue(true);
                                            } 
                                            else {
                                                reagent_type_loc.items.items[4].setValue(true);
                                            }
                                            
                                            //Ext.getCmp(responseJson.reagent_type).setValue(true)
                                        }
                                    });
                                    
                                    Ext.getCmp('add_reagent_tab').items.items[0].getForm().load({
                                        url: '/experiments/load/reagent/',
                                        method: 'POST',
                                        params: {
                                            reagent_no: templateNo
                                        }
                                    });
                                    
                                    //var currentTime = Ext.Date.format(new Date(), 'n/d/Y');
                                    //cmpLocation.items.items[4].setValue(currentTime);
                                
                                }
                            }
                        }, {
                            fieldLabel: 'Experimenter',
                            xtype: 'fieldcontainer',
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            defaults: {
                                editable: false
                            },
                            items: [{
                                xtype: 'combobox',
                                displayField: 'company',
                                name: 'company',
                                valueField: 'company',
                                store: companyStore,
                                queryMode: 'local',
                                allowBlank: false,
                                emptyText: 'Company',
                                width: 300,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            var lab = Ext.getCmp("reagent-lab");
                                            lab.clearValue();
                                            lab.store.load({
                                                params: {
                                                    id: records[0].data.company
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'combobox',
                                displayField: 'lab',
                                valueField: 'lab',
                                name: 'lab',
                                id: 'reagent-lab',
                                emptyText: 'Laboratory',
                                store: labStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 200,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            var experimenter = Ext.getCmp("reagent-experimenter");
                                            experimenter.clearValue();
                                            experimenter.store.load({
                                                params: {
                                                    id: records[0].data.lab
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'combobox',
                                displayField: 'experimenter',
                                valueField: 'experimenter',
                                emptyText: 'Experimenter',
                                name: 'experimenter',
                                id: 'reagent-experimenter',
                                store: experimenterStore,
                                queryMode: 'local',
                                allowBlank: false,
                                width: 180
                            }]
                        }, {
                            xtype: 'radiogroup',
                            fieldLabel: 'Reagent type',
                            name: 'reagent_type',
                            id: 'reagent_type' + timestamp,
                            columns: 2,
                            vertical: true,
                            items: [{
                                boxLabel: 'Antibodies',
                                name: 'reagent_type',
                                inputValue: 'Antigen'
                            }, {
                                boxLabel: 'Nuclear Acid',
                                name: 'reagent_type',
                                inputValue: 'DNA'
                            }, {
                                boxLabel: 'Proteins Motif',
                                name: 'reagent_type',
                                inputValue: 'Protein',
                                hidden: true
                            }, {
                                boxLabel: 'Chemical',
                                name: 'reagent_type',
                                inputValue: 'chemical'
                            }, {
                                boxLabel: 'Other',
                                name: 'reagent_type',
                                inputValue: 'other'
                            }]
                        }, {
                            xtype: 'textfield',
                            fieldLabel: 'Reagent Name',
                            name: 'name'
                        }, {
                            xtype: 'datefield',
                            fieldLabel: 'Date',
                            value: Ext.Date.format(new Date(), 'n/d/Y'),
                            width: 450,
                            name: 'date'
                        }, {
                            xtype: 'combobox',
                            fieldLabel: 'Manufacturer',
                            displayField: 'Reagent_manufacturer',
                            name: 'Reagent_manufacturer',
                            store: reagentManufacturerStore,
                            queryModel: true,
                            typeAhead: true
                        }, {
                            xtype: 'textfield',
                            fieldLabel: 'Catalog No',
                            name: 'catalog_no',
                            allowBlank: true
                        }, {
                            xtype: 'combobox',
                            fieldLabel: 'Conjugate Beads',
                            displayField: 'Conjugate',
                            name: 'Conjugate',
                            store: conjugateStore,
                            queryModel: 'local',
                            typeAhead: true
                        }, {
                            xtype: 'fieldcontainer',
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            items: [{
                                xtype: 'combobox',
                                fieldLabel: 'Application',
                                displayField: 'Application',
                                name: 'Application',
                                store: applicationStore,
                                queryMode: 'local',
                                multiSelect: true,
                                labelWidth: 120,
                                width: 415,
                                allowBlank: false
                            }, {
                                xtype: 'button',
                                text: 'Add',
                                handler: add_application
                            }]
                        }, {
                            xtype: 'fieldcontainer',
                            // fieldLabel : 'Species React',
                            layout: {
                                type: 'hbox',
                                align: 'stretch'
                            },
                            items: [{
                                xtype: 'combobox',
                                valueField: 'React_species',
                                fieldLabel: 'Source Species',
                                name: 'React_species_source',
                                displayField: 'React_species',
                                store: reactSpeciesStore,
                                emptyText: 'Source',
                                queryMode: 'local',
                                multiSelect: true,
                                labelWidth: 120,
                                width: 415,
                                allowBlank: false
                            }, {
                                xtype: 'combobox',
                                valueField: 'React_species',
                                fieldLabel: 'Target Species',
                                // fieldLabel : 'Species
                                // React',
                                name: 'React_species_target',
                                displayField: 'React_species',
                                store: reactSpeciesStore,
                                queryMode: 'local',
                                emptyText: 'Target',
                                multiSelect: true,
                                labelWidth: 120,
                                width: 300,
                                allowBlank: false
                            }]
                        }, 
                        //                                      {
                        //                                          xtype : 'textfield',
                        //                                          name : 'isepc',
                        //                                          fieldLabel : 'Ispec No',
                        //                                          labelWidth : 120,
                        //                                          allowBlank : true
                        //                                      }, 
                        {
                            xtype: 'hiddenfield',
                            name: 'csrfmiddlewaretoken',
                            value: csrftoken
                        }, {
                            xtype: 'hiddenfield',
                            name: 'timestamp',
                            value: timestamp
                        }]
                    });
                    var buttonPanel = Ext.create('Ext.panel.Panel', {
                        // frame : true,
                        // renderTo : 'button',
                        // border : true,
                        buttonAlign: "center",
                        buttons: [{
                            text: 'Submit',
                            handler: submitForm
                        }, {
                            text: 'Cancel',
                            handler: cancelForm
                        }]
                    });
                    
                    var commentsPanel = Ext.create('Ext.form.Panel', {
                        title: 'Comments',
                        border: true,
                        // frame : true,
                        bodyPadding: 10,
                        headerPosition: 'top',
                        defaults: {
                            labelWidth: 120,
                            // labelAlign : 'top',
                            width: 800
                            // allowBlank : false
                        },
                        items: [{
                            xtype: 'textareafield',
                            name: 'comments',
                            fieldLabel: 'Extra Comments'
                        }, 
                        //                              {
                        //                                  xtype : 'textfield',
                        //                                  // fieldLabel : 'Target
                        //                                  // Gene',
                        //                                  name : 'Ispec_num',
                        //                                  fieldLabel : 'Ispec No',
                        //                                  width : 400
                        //                              },
                        {
                            xtype: 'textfield',
                            name: 'Ispec_num',
                            fieldLabel: 'Ispec No',
                            labelWidth: 120,
                            allowBlank: true
                        }
                        ]
                    });
                    
                    var formPanel = Ext.create('Ext.form.Panel', {
                        // frame : true,
                        // overflowY : 'scroll',
                        id: timestamp,
                        // layout: 'fit',
                        // renderTo : 'form',
                        items: [general, commentsPanel]
                    });
                    // antigen information
                    var antigen = Ext.create('Ext.panel.Panel', {
                        title: 'ANTIGEN INFO',
                        border: true,
                        bodyPadding: 10,
                        // frame : true,
                        id: 'antigen' + timestamp,
                        headerPosition: 'left',
                        defaults: {
                            labelWidth: 120,
                            labelAligh: 'left',
                            width: 450,
                            allowBlank: true
                        },
                        items: [{
                            xtype: 'textfield',
                            fieldLabel: 'GeneID',
                            name: 'gene_id'
                        }, {
                            xtype: 'combobox',
                            fieldLabel: 'Host Species',
                            displayField: 'Antigen_species',
                            name: 'Antigen_species',
                            store: antigenSpeciesStore,
                            queryMode: 'local',
                            typeAhead: true
                        }, {
                            xtype: 'combobox',
                            fieldLabel: 'Clonal Type',
                            name: 'Antigen_clonal_type',
                            displayField: 'Antigen_clonal_type',
                            store: antigenClonalTypeStore,
                            queryMode: 'local',
                            typeAhead: true
                        }, {
                            xtype: 'combobox',
                            fieldLabel: 'Modification',
                            name: 'Antigen_modification',
                            displayField: 'Antigen_modification',
                            store: antigenModificationStore,
                            queryMode: 'local',
                            typeAhead: true
                        }]
                    });
                    // dna information
                    var dna = Ext.create('Ext.panel.Panel', {
                        title: 'DNA INFO',
                        bodyPadding: 10,
                        border: true,
                        // frame : true,
                        id: 'dna' + timestamp,
                        headerPosition: 'left',
                        defaults: {
                            labelWidth: 120,
                            labelAligh: 'left',
                            width: 450,
                            allowBlank: false
                        },
                        items: [{
                            xtype: 'textareafield',
                            name: 'dna_sequence',
                            fieldLabel: 'DNA Sequence'
                        }]
                    });
                    // ubi information
                    var ubi = Ext.create('Ext.panel.Panel', {
                        title: 'UBI INFO',
                        border: true,
                        bodyPadding: 10,
                        // frame : true,
                        id: 'ubi' + timestamp,
                        headerPosition: 'left',
                        defaults: {
                            labelWidth: 120,
                            labelAligh: 'left',
                            width: 450,
                            allowBlank: false
                        },
                        items: [{
                            xtype: 'textareafield',
                            name: 'domain',
                            fieldLabel: 'Domain'
                        }]
                    });
                    var cas = Ext.create('Ext.panel.Panel', {
                        title: 'Chemical INFO',
                        bodyPadding: 10,
                        border: true,
                        // frame : true,
                        id: 'cas' + timestamp,
                        headerPosition: 'left',
                        defaults: {
                            labelWidth: 120,
                            labelAligh: 'left',
                            width: 450,
                            allowBlank: false
                        },
                        items: [{
                            xtype: 'textareafield',
                            name: 'cas_number',
                            fieldLabel: 'CAS Number'
                        }]
                    });
                    // Other information
                    var remarks = Ext.create('Ext.panel.Panel', {
                        title: 'Description',
                        border: true,
                        bodyPadding: 10,
                        // frame : true,
                        id: 'remarks' + timestamp,
                        headerPosition: 'left',
                        defaults: {
                            labelWidth: 120,
                            labelAligh: 'left',
                            width: 450,
                            allowBlank: false
                        },
                        items: [{
                            xtype: 'textareafield',
                            name: 'remarks',
                            fieldLabel: 'Remarks'
                        }]
                    });
                    // event listener for type radio
                    typeradio = Ext.getCmp('reagent_type' + timestamp);
                    typeradio.on('change', function(radio, newV, oldV, e) {
                        if (oldV.reagent_type == 'Antigen') {
                            formPanel.remove(antigen, false);
                        } else if (oldV.reagent_type == 'DNA') {
                            formPanel.remove(dna, false);
                        } else if (oldV.reagent_type == 'Protein') {
                            formPanel.remove(ubi, false);
                        } else if (oldV.reagent_type == 'other') {
                            formPanel.remove(remarks, false);
                        } else if (oldV.reagent_type == 'chemical') {
                            formPanel.remove(cas, false);
                        }
                        if (newV.reagent_type == 'Antigen') {
                            formPanel.add(antigen);
                        } else if (newV.reagent_type == 'DNA') {
                            formPanel.add(dna);
                        } else if (newV.reagent_type == 'Protein') {
                            formPanel.add(ubi);
                        } else if (newV.reagent_type == 'chemical') {
                            formPanel.add(cas);
                        } else {
                            formPanel.add(remarks);
                        }
                    });
                    // formPanel.add(buttonPanel)
                    tab = Ext.getCmp('content-panel')
                    tab.add({
                        id: 'add_reagent_tab',
                        title: 'Add Reagent',
                        iconCls: 'addreagent',
                        closable: true,
                        layout: 'anchor',
                        items: [formPanel, buttonPanel]
                    }).show()
                }
            },
            '#displayexperiment': {
                click: function() {
                    var timestamp = (new Date()).valueOf();
                    var store = Ext.create('gar.store.ShowExperiment');
                    var filters = {
                        ftype: 'filters',
                        encode: true, // json encode the filter query
                        // local: true,   // defaults to false (remote filtering)

                        // Filters are most naturally placed in the column definition, but can also be
                        // added here.
                        // filters: [{
                        //     type: 'boolean',
                        //     dataIndex: 'visible'
                        // }]
                    };
                    var grid = Ext.create('gar.view.ShowExperiment', {
                        id: 'show_experiment' + timestamp,
                        store: store,
                        emptyText: 'No Matching Experiment Records!',
                        features: [filters]
                    })
                    {
                        tab = Ext.getCmp('content-panel')
                        tab.add({
                            title: 'Show Experiment',
                            iconCls: 'displayexperiment',
                            closable: true,
                            layout: 'fit',
                            items: [grid]
                        }).show()
                    }
                }
            },
            '#displaysample': {
                click: function() {
                    var timestamp = (new Date()).valueOf();
                    var store = Ext.create('gar.store.ShowSample');
                    var filters = {
                        ftype: 'filters',
                        encode: true
                    };
                    var grid = Ext.create('gar.view.ShowSample', {
                        id: 'show_sample' + timestamp,
                        store: store,
                        features: [filters],
                        emptyText: 'No Matching Sample Records!'
                    });
                    console.log(grid.features)
                    {
                        tab = Ext.getCmp('content-panel')
                        tab.add({
                            title: 'Show Sample',
                            iconCls: 'displaysample',
                            closable: true,
                            layout: 'fit',
                            items: [grid]
                        }).show();
                    }
                }
            },
            '#displayreagent': {
                click: function() {
                    var timestamp = (new Date()).valueOf();
                    var store = Ext.create('gar.store.ShowReagent');
                    var grid = Ext.create('gar.view.ShowReagent', {
                        id: 'show_reagent' + timestamp,
                        store: store,
                        emptyText: 'No Matching Reagent Records!'
                    })
                    tab = Ext.getCmp('content-panel')
                    tab.add({
                        title: 'Show Reagent',
                        // id : 'show_experiment',
                        iconCls: 'displayreagent',
                        closable: true,
                        layout: 'fit',
                        items: [grid]
                    }).show()
                }
            },
            '#metic': {
                click: function() {
                    ticPlot("menu", [])
                }
            },
            '#mebarplot': {
                click: function() {
                    var data = (Ext.getCmp('info_experiments_selected').getValue()) ? Ext.decode(Ext.getCmp('info_experiments_selected').getValue()) : 0;
                    //Ext.getCmp('info_experiments_selected').setValue(0)
                    var store = Ext.create('gar.store.ExperimentPlot', {
                        data: data
                    });
                    var chart = Ext.create('Ext.chart.Chart', {
                        id: 'chartCmp',
                        xtype: 'chart',
                        style: 'background:#ffffff',
                        animate: true,
                        shadow: true,
                        store: store,
                        legend: {
                            position: 'right'
                        },
                        axes: [{
                            type: 'Numeric',
                            position: 'bottom',
                            fields: ['num_gene', 'num_peptide', 'num_spectrum'],
                            minimum: 0,
                            label: {
                                renderer: Ext.util.Format.numberRenderer('0,0')
                            },
                            grid: true,
                            title: 'Number of Hits'
                        }, {
                            type: 'Category',
                            position: 'left',
                            fields: ['name'],
                            title: 'Experiments or searches'
                        }],
                        series: [{
                            type: 'bar',
                            axis: 'bottom',
                            xField: 'name',
                            yField: ['num_gene', 'num_peptide', 'num_spectrum'],
                            label: {
                                display: 'insideEnd',
                                field: ['num_gene', 'num_peptide', 'num_spectrum'],
                                renderer: Ext.util.Format.numberRenderer('0'),
                                orientation: 'horizontal',
                                color: '#333333',
                                'text-anchor': 'middle'
                            }
                        }]
                    });
                    var win = Ext.create('Ext.window.Window', {
                        width: 800,
                        height: 600,
                        minHeight: 400,
                        minWidth: 550,
                        hidden: false,
                        maximizable: true,
                        title: 'Bar Chart',
                        animateTarget: 'mebarplot',
                        autoShow: true,
                        layout: 'fit',
                        tbar: [{
                            text: 'Save Chart',
                            handler: function() {
                                Ext.MessageBox.confirm('Confirm Download', 'Would you like to download the chart as an image?', function(choice) {
                                    if (choice == 'yes') {
                                        chart.save({
                                            type: 'image/png'
                                        });
                                    }
                                });
                            }
                        }],
                        items: chart
                    });
                }
            },
            '#mepca': {
                click: function() {
                    var data = (Ext.getCmp('info_experiments_selected').getValue()) ? Ext.decode(Ext.getCmp('info_experiments_selected').getValue()) : 0;
                    //Ext.getCmp('info_experiments_selected').setValue(0)
                    var store = Ext.create('gar.store.ExperimentPlot', {
                        data: data
                    });
                    var win = Ext.create('Ext.window.Window', {
                        draggable: {
                            constrain: true,
                            constrainTo: Ext.getBody()
                        },
                        width: 800,
                        height: 600,
                        minHeight: 400,
                        minWidth: 550,
                        hidden: false,
                        maximizable: true,
                        title: 'PCA Plot',
                        animateTarget: 'mepca',
                        autoShow: true,
                        layout: 'fit',
                        tbar: [{
                            text: 'Save Chart',
                            handler: function() {
                                Ext.MessageBox.confirm('Confirm Download', 'Would you like to download the chart as an image?', function(choice) {
                                });
                            }
                        }],
                        html: '<iframe id=thisIframe   width="100%" height="100%"   frameborder=0 src=rplot/?paras=' + data + '></iframe>'
                    });
                }
            },
            '#meplotdistribution': {
                click: function() {
                    var view = Ext.widget('globalplot');
                }
            },
            '#meradarplot': {
                click: function() {
                    generateData = function(n, floor) {
                        var data = [], p = (Math.random() * 11) + 1, i;
                        floor = (!floor && floor !== 0) ? 20 : floor;
                        for (i = 0; i < (n || 12); i++) {
                            data.push({
                                name: Ext.Date.monthNames[i % 12],
                                data1: Math.floor(Math.max((Math.random() * 100), floor)),
                                data2: Math.floor(Math.max((Math.random() * 100), floor)),
                                data3: Math.floor(Math.max((Math.random() * 100), floor)),
                                data4: Math.floor(Math.max((Math.random() * 100), floor)),
                                data5: Math.floor(Math.max((Math.random() * 100), floor)),
                                data6: Math.floor(Math.max((Math.random() * 100), floor)),
                                data7: Math.floor(Math.max((Math.random() * 100), floor)),
                                data8: Math.floor(Math.max((Math.random() * 100), floor)),
                                data9: Math.floor(Math.max((Math.random() * 100), floor))
                            });
                        }
                        return data;
                    }
                    ;
                    var store2 = Ext.create('Ext.data.JsonStore', {
                        fields: ['name', 'data1', 'data2', 'data3', 'data4', 'data5', 'data6', 'data7', 'data9', 'data9']
                        // data: generateData()
                    });
                    store2.loadData(generateData());
                    var chart = Ext.create('Ext.chart.Chart', {
                        id: 'chartCmp',
                        xtype: 'chart',
                        style: 'background:#ffffff',
                        theme: 'Category2',
                        insetPadding: 20,
                        animate: true,
                        store: store2,
                        legend: {
                            position: 'right'
                        },
                        axes: [{
                            type: 'Radial',
                            position: 'radial',
                            label: {
                                display: true
                            }
                        }],
                        series: [{
                            showInLegend: true,
                            type: 'radar',
                            xField: 'name',
                            yField: 'data1',
                            style: {
                                opacity: 0.4
                            }
                        }, {
                            showInLegend: true,
                            type: 'radar',
                            xField: 'name',
                            yField: 'data2',
                            style: {
                                opacity: 0.4
                            }
                        }, {
                            showInLegend: true,
                            type: 'radar',
                            xField: 'name',
                            yField: 'data3',
                            style: {
                                opacity: 0.4
                            }
                        }]
                    });
                    var win = Ext.create('Ext.Window', {
                        width: 800,
                        height: 600,
                        minHeight: 400,
                        minWidth: 550,
                        hidden: false,
                        shadow: false,
                        maximizable: true,
                        style: 'overflow: hidden;',
                        title: 'Demo Radar Chart',
                        animateTarget: 'meradarplot',
                        autoShow: true,
                        layout: 'fit',
                        tbar: [{
                            text: 'Save Chart',
                            handler: function() {
                                Ext.MessageBox.confirm('Confirm Download', 'Would you like to download the chart as an image?', function(choice) {
                                    if (choice == 'yes') {
                                        chart.save({
                                            type: 'image/png'
                                        });
                                    }
                                });
                            }
                        }, {
                            text: 'Reload Data',
                            handler: function() {
                                store2.loadData(generateData());
                            }
                        }, {
                            enableToggle: true,
                            pressed: true,
                            text: 'Animate',
                            toggleHandler: function(btn, pressed) {
                                var chart = Ext.getCmp('chartCmp');
                                chart.animate = pressed ? {
                                    easing: 'ease',
                                    duration: 500
                                } : false;
                            }
                        }],
                        items: chart
                    });
                }
            },
            '#mescatter': {
                click: function() {
                    var peptide_plot_store = Ext.create('gar.store.PeptidePlot');
                    peptide_plot_store.load({
                        params: {
                            search_id: 2,
                            pep_sequence: 'VNQIGSVTESIQAcK',
                            modification: 'Carbamidomethyl (C)(14)'
                        }
                    });
                    var xlabel = [0, 1, 2, 3];
                    var ylabel = [0, 1, 2, 3];
                    peptide_plot_store.on('load', function() {
                        xlabel = peptide_plot_store.getxlabel();
                        ylabel = peptide_plot_store.getylabel();
                        // Ext.Msg.alert('Experiment
                        // Info:'+xlabel,
                        // ylabel);
                        refresh();
                    });
                    // Ext.Msg.alert('Experiment
                    // Info:'+xlabel.length,
                    // ylabel.length);
                    // Ext.Msg.alert('Experiment Info:'+xlabel,
                    // ylabel);
                    var rank_store = Ext.create('gar.store.TicRank');
                    rank_store.load({
                        params: {
                            search_id: 2
                        }
                    });
                    var pieChart = Ext.create('Ext.chart.Chart', {
                        width: 200,
                        height: 100,
                        xtype: 'chart',
                        style: 'background:#fff',
                        animate: true,
                        store: peptide_plot_store,
                        shadow: true,
                        theme: 'Category1',
                        legend: {
                            position: 'right'
                        },
                        axes: [{
                            type: 'Numeric',
                            minimum: 0,
                            position: 'left',
                            fields: ['fraction_id'],
                            minorTickSteps: 1,
                            grid: {
                                odd: {
                                    opacity: 1,
                                    fill: '#ddd',
                                    stroke: '#bbb',
                                    'stroke-width': 0.5
                                }
                            }
                        }],
                        series: [{
                            type: 'line',
                            highlight: {
                                size: 7,
                                radius: 7
                            },
                            axis: 'left',
                            xField: 'fraction_id',
                            yField: 'repeat_id',
                            markerConfig: {
                                type: 'cross',
                                size: 4,
                                radius: 4,
                                'stroke-width': 0
                            }
                        }]
                    });
                    var grid = Ext.create('Ext.grid.Panel', {
                        store: peptide_plot_store,
                        height: 130,
                        width: 280,
                        columns: [{
                            text: 'xplot',
                            dataIndex: 'xplot'
                        }, {
                            text: 'yplot',
                            dataIndex: 'yplot'
                        }]
                    });
                    var Renderers = {};
                    (function() {
                        var ColorManager = {
                            rgbToHsv: function(rgb) {
                                var r = rgb[0] / 255, g = rgb[1] / 255, b = rgb[2] / 255, rd = Math.round, minVal = Math.min(r, g, b), maxVal = Math.max(r, g, b), delta = maxVal - minVal, h = 0, s = 0, v = 0, deltaRgb;
                                v = maxVal;
                                if (delta == 0) {
                                    return [0, 0, v];
                                } else {
                                    s = delta / maxVal;
                                    deltaRgb = {
                                        r: (((maxVal - r) / 6) + (delta / 2)) / delta,
                                        g: (((maxVal - g) / 6) + (delta / 2)) / delta,
                                        b: (((maxVal - b) / 6) + (delta / 2)) / delta
                                    };
                                    if (r == maxVal) {
                                        h = deltaRgb.b - deltaRgb.g;
                                    } else if (g == maxVal) {
                                        h = (1 / 3) + deltaRgb.r - deltaRgb.b;
                                    } else if (b == maxVal) {
                                        h = (2 / 3) + deltaRgb.g - deltaRgb.r;
                                    }
                                    // handle edge cases for hue
                                    if (h < 0) {
                                        h += 1;
                                    }
                                    if (h > 1) {
                                        h -= 1;
                                    }
                                }
                                h = rd(h * 360);
                                s = rd(s * 100);
                                v = rd(v * 100);
                                return [h, s, v];
                            },
                            hsvToRgb: function(hsv) {
                                var h = hsv[0] / 360, s = hsv[1] / 100, v = hsv[2] / 100, r, g, b, rd = Math.round;
                                if (s == 0) {
                                    v *= 255;
                                    return [v, v, v];
                                } else {
                                    var vh = h * 6
                                      , vi = vh >> 0
                                      , v1 = v * (1 - s)
                                      , v2 = v * (1 - s * (vh - vi))
                                      , v3 = v * (1 - s * (1 - (vh - vi)));
                                    switch (vi) {
                                    case 0:
                                        r = v;
                                        g = v3;
                                        b = v1;
                                        break;
                                    case 1:
                                        r = v2;
                                        g = v;
                                        b = v1;
                                        break;
                                    case 2:
                                        r = v1;
                                        g = v;
                                        b = v3;
                                        break;
                                    case 3:
                                        r = v1;
                                        g = v2;
                                        b = v;
                                        break;
                                    case 4:
                                        r = v3;
                                        g = v1;
                                        b = v;
                                        break;
                                    default:
                                        r = v;
                                        g = v1;
                                        b = v2;
                                    }
                                    return [rd(r * 255), rd(g * 255), rd(b * 255)];
                                }
                            }
                        };
                        // Generic number interpolator
                        var delta = function(x, y, a, b, theta) {
                            return a + (b - a) * (y - theta) / (y - x);
                        }
                        ;
                        // Add renderer methods.
                        Ext.apply(Renderers, {
                            color: function(fieldName, minColor, maxColor, minValue, maxValue) {
                                var re = /rgb\s*\(\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*\)\s*/
                                  , minColorMatch = minColor.match(re)
                                  , maxColorMatch = maxColor.match(re)
                                  , interpolate = function(theta) {
                                    return [delta(minValue, maxValue, minColor[0], maxColor[0], theta), delta(minValue, maxValue, minColor[1], maxColor[1], theta), delta(minValue, maxValue, minColor[2], maxColor[2], theta)];
                                }
                                ;
                                minColor = ColorManager.rgbToHsv([+minColorMatch[1], +minColorMatch[2], +minColorMatch[3]]);
                                maxColor = ColorManager.rgbToHsv([+maxColorMatch[1], +maxColorMatch[2], +maxColorMatch[3]]);
                                // Return the renderer
                                return function(sprite, record, attr, index, store) {
                                    var value = +record.get(fieldName)
                                      , rgb = ColorManager.hsvToRgb(interpolate(value))
                                      , rgbString = 'rgb(' + rgb[0] + ', ' + rgb[1] + ', ' + rgb[2] + ')';
                                    return Ext.apply(attr, {
                                        fill: rgbString
                                    });
                                }
                                ;
                            },
                            grayscale: function(fieldName, minColor, maxColor, minValue, maxValue) {
                                var re = /rgb\s*\(\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*\)\s*/
                                  , minColorMatch = minColor.match(re)
                                  , maxColorMatch = maxColor.match(re)
                                  , interpolate = function(theta) {
                                    var ans = delta(minValue, maxValue, +minColorMatch[1], +maxColorMatch[1], theta) >> 0;
                                    return [ans, ans, ans];
                                }
                                ;
                                // Return the renderer
                                return function(sprite, record, attr, index, store) {
                                    var value = +record.get(fieldName)
                                      , rgb = interpolate(value)
                                      , rgbString = 'rgb(' + rgb[0] + ', ' + rgb[1] + ', ' + rgb[2] + ')';
                                    return Ext.apply(attr, {
                                        fill: rgbString,
                                        strokeFill: 'rgb(0, 0, 0)'
                                    });
                                }
                                ;
                            },
                            radius: function(fieldName, minRadius, maxRadius, minValue, maxValue) {
                                var interpolate = function(theta) {
                                    return delta(minValue, maxValue, minRadius, maxRadius, theta);
                                }
                                ;
                                // Return the renderer
                                return function(sprite, record, attr, index, store) {
                                    var value = +record.get(fieldName)
                                      , radius = interpolate(value);
                                    return Ext.apply(attr, {
                                        radius: radius,
                                        size: radius
                                    });
                                }
                                ;
                            }
                        });
                    })();
                    // current renderer configuration
                    var rendererConfiguration = {
                        xField: 'xplot',
                        yField: 'yplot',
                        color: false,
                        colorFrom: 'rgb(250, 20, 20)',
                        colorTo: 'rgb(127, 0, 240)',
                        scale: false,
                        scaleFrom: 'rgb(20, 20, 20)',
                        scaleTo: 'rgb(220, 220, 220)',
                        radius: false,
                        radiusSize: 50
                    };
                    // update the visualization with the new
                    // renderer
                    // configuration
                    function refresh() {
                        var chart = Ext.getCmp('chartCmp'), series = chart.series.items, len = series.length, rc = rendererConfiguration, color, grayscale, radius, s;
                        for (var i = 0; i < len; i++) {
                            s = series[i];
                            s.xField = rc.xField;
                            s.yField = rc.yField;
                            color = rc.color ? Renderers.color(rc.color, rc.colorFrom, rc.colorTo, 0, 1) : function(a, b, attr) {
                                return attr;
                            }
                            ;
                            grayscale = rc.grayscale ? Renderers.grayscale(rc.grayscale, rc.scaleFrom, rc.scaleTo, 0, 1) : function(a, b, attr) {
                                return attr;
                            }
                            ;
                            radius = rc.radius ? Renderers.radius(rc.radius, 10, rc.radiusSize, 0, 1) : function(a, b, attr) {
                                return attr;
                            }
                            ;
                            s.renderer = function(sprite, record, attr, index, store) {
                                return radius(sprite, record, grayscale(sprite, record, color(sprite, record, attr, index, store), index, store), index, store);
                            }
                            ;
                        }
                        chart.redraw();
                    }
                    // form selection callbacks/handlers.
                    var xAxisHandler = function(elem) {
                        var xField = elem.text;
                        rendererConfiguration.xField = xField;
                        refresh();
                    }
                    ;
                    var yAxisHandler = function(elem) {
                        var yField = elem.text;
                        rendererConfiguration.yField = yField;
                        refresh();
                    }
                    ;
                    var colorVariableHandler = function(elem) {
                        var color = elem.text;
                        rendererConfiguration.color = color;
                        rendererConfiguration.grayscale = false;
                        refresh();
                    }
                    ;
                    var grayscaleVariableHandler = function(elem) {
                        var color = elem.text;
                        rendererConfiguration.grayscale = color;
                        rendererConfiguration.color = false;
                        refresh();
                    }
                    ;
                    var scaleFromHandler = function(elem) {
                        var from = elem.text;
                        rendererConfiguration.scaleFrom = from;
                        refresh();
                    }
                    ;
                    var scaleToHandler = function(elem) {
                        var to = elem.text;
                        rendererConfiguration.scaleTo = to;
                        refresh();
                    }
                    ;
                    var colorFromHandler = function(elem) {
                        var from = elem.text;
                        rendererConfiguration.colorFrom = from;
                        refresh();
                    }
                    ;
                    var colorToHandler = function(elem) {
                        var to = elem.text;
                        rendererConfiguration.colorTo = to;
                        refresh();
                    }
                    ;
                    var radiusHandler = function(elem) {
                        var radius = elem.text;
                        rendererConfiguration.radius = radius;
                        refresh();
                    }
                    ;
                    var radiusSizeHandler = function(elem) {
                        var radius = elem.text;
                        rendererConfiguration.radiusSize = parseInt(radius, 10);
                        refresh();
                    }
                    ;
                    var xAxisMenu = Ext.create('Ext.menu.Menu', {
                        id: 'xAxisMenu',
                        items: [{
                            text: 'xplot',
                            handler: xAxisHandler,
                            checked: true,
                            group: 'x'
                        }, {
                            text: 'yplot',
                            handler: xAxisHandler,
                            checked: false,
                            group: 'x'
                        }, {
                            text: 'area',
                            handler: xAxisHandler,
                            checked: false,
                            group: 'x'
                        }]
                    });
                    var yAxisMenu = Ext.create('Ext.menu.Menu', {
                        id: 'yAxisMenu',
                        items: [{
                            text: 'xplot',
                            handler: yAxisHandler,
                            checked: false,
                            group: 'y'
                        }, {
                            text: 'yplot',
                            handler: yAxisHandler,
                            checked: true,
                            group: 'y'
                        }, {
                            text: 'area',
                            handler: yAxisHandler,
                            checked: false,
                            group: 'y'
                        }]
                    });
                    var colorMenu = Ext.create('Ext.menu.Menu', {
                        id: 'colorMenu',
                        items: [{
                            text: 'xplot',
                            handler: colorVariableHandler,
                            checked: true,
                            group: 'color'
                        }, {
                            text: 'yplot',
                            handler: colorVariableHandler,
                            checked: false,
                            group: 'color'
                        }, {
                            text: 'area',
                            handler: colorVariableHandler,
                            checked: false,
                            group: 'color'
                        }, {
                            text: 'Color From',
                            menu: {
                                items: [{
                                    text: 'rgb(250, 20, 20)',
                                    handler: colorToHandler,
                                    checked: true,
                                    group: 'colorrange'
                                }, {
                                    text: 'rgb(20, 250, 20)',
                                    handler: colorToHandler,
                                    checked: false,
                                    group: 'colorrange'
                                }, {
                                    text: 'rgb(20, 20, 250)',
                                    handler: colorToHandler,
                                    checked: false,
                                    group: 'colorrange'
                                }, {
                                    text: 'rgb(127, 0, 240)',
                                    handler: colorFromHandler,
                                    checked: false,
                                    group: 'colorrange'
                                }, {
                                    text: 'rgb(213, 70, 121)',
                                    handler: colorToHandler,
                                    checked: false,
                                    group: 'colorrange'
                                }, {
                                    text: 'rgb(44, 153, 201)',
                                    handler: colorFromHandler,
                                    checked: false,
                                    group: 'colorrange'
                                }, {
                                    text: 'rgb(146, 6, 157)',
                                    handler: colorFromHandler,
                                    checked: false,
                                    group: 'colorrange'
                                }, {
                                    text: 'rgb(49, 149, 0)',
                                    handler: colorFromHandler,
                                    checked: false,
                                    group: 'colorrange'
                                }, {
                                    text: 'rgb(249, 153, 0)',
                                    handler: colorFromHandler,
                                    checked: false,
                                    group: 'colorrange'
                                }]
                            }
                        }, {
                            text: 'Color To',
                            menu: {
                                items: [{
                                    text: 'rgb(250, 20, 20)',
                                    handler: colorToHandler,
                                    checked: false,
                                    group: 'tocolorrange'
                                }, {
                                    text: 'rgb(20, 250, 20)',
                                    handler: colorToHandler,
                                    checked: false,
                                    group: 'tocolorrange'
                                }, {
                                    text: 'rgb(20, 20, 250)',
                                    handler: colorToHandler,
                                    checked: false,
                                    group: 'tocolorrange'
                                }, {
                                    text: 'rgb(127, 0, 220)',
                                    handler: colorFromHandler,
                                    checked: true,
                                    group: 'tocolorrange'
                                }, {
                                    text: 'rgb(213, 70, 121)',
                                    handler: colorToHandler,
                                    checked: false,
                                    group: 'tocolorrange'
                                }, {
                                    text: 'rgb(44, 153, 201)',
                                    handler: colorToHandler,
                                    checked: false,
                                    group: 'tocolorrange'
                                }, {
                                    text: 'rgb(146, 6, 157)',
                                    handler: colorToHandler,
                                    checked: false,
                                    group: 'tocolorrange'
                                }, {
                                    text: 'rgb(49, 149, 0)',
                                    handler: colorToHandler,
                                    checked: false,
                                    group: 'tocolorrange'
                                }, {
                                    text: 'rgb(249, 153, 0)',
                                    handler: colorToHandler,
                                    checked: false,
                                    group: 'tocolorrange'
                                }]
                            }
                        }]
                    });
                    var grayscaleMenu = Ext.create('Ext.menu.Menu', {
                        id: 'grayscaleMenu',
                        items: [{
                            text: 'xplot',
                            handler: grayscaleVariableHandler,
                            checked: false,
                            group: 'gs'
                        }, {
                            text: 'yplot',
                            handler: grayscaleVariableHandler,
                            checked: false,
                            group: 'gs'
                        }, {
                            text: 'area',
                            handler: grayscaleVariableHandler,
                            checked: false,
                            group: 'gs'
                        }, {
                            text: 'Scale From',
                            menu: {
                                items: [{
                                    text: 'rgb(20, 20, 20)',
                                    handler: scaleFromHandler,
                                    checked: true,
                                    group: 'gsrange'
                                }, {
                                    text: 'rgb(80, 80, 80)',
                                    handler: scaleFromHandler,
                                    checked: false,
                                    group: 'gsrange'
                                }, {
                                    text: 'rgb(120, 120, 120)',
                                    handler: scaleFromHandler,
                                    checked: false,
                                    group: 'gsrange'
                                }, {
                                    text: 'rgb(180, 180, 180)',
                                    handler: scaleFromHandler,
                                    checked: false,
                                    group: 'gsrange'
                                }, {
                                    text: 'rgb(220, 220, 220)',
                                    handler: scaleFromHandler,
                                    checked: false,
                                    group: 'gsrange'
                                }, {
                                    text: 'rgb(250, 250, 250)',
                                    handler: scaleFromHandler,
                                    checked: false,
                                    group: 'gsrange'
                                }]
                            }
                        }, {
                            text: 'Scale To',
                            menu: {
                                items: [{
                                    text: 'rgb(20, 20, 20)',
                                    handler: scaleToHandler,
                                    checked: false,
                                    group: 'togsrange'
                                }, {
                                    text: 'rgb(80, 80, 80)',
                                    handler: scaleToHandler,
                                    checked: false,
                                    group: 'togsrange'
                                }, {
                                    text: 'rgb(120, 120, 120)',
                                    handler: scaleToHandler,
                                    checked: false,
                                    group: 'togsrange'
                                }, {
                                    text: 'rgb(180, 180, 180)',
                                    handler: scaleToHandler,
                                    checked: false,
                                    group: 'togsrange'
                                }, {
                                    text: 'rgb(220, 220, 220)',
                                    handler: scaleToHandler,
                                    checked: true,
                                    group: 'togsrange'
                                }, {
                                    text: 'rgb(250, 250, 250)',
                                    handler: scaleToHandler,
                                    checked: false,
                                    group: 'togsrange'
                                }]
                            }
                        }]
                    });
                    var radiusMenu = Ext.create('Ext.menu.Menu', {
                        id: 'radiusMenu',
                        style: {
                            overflow: 'visible'// For
                            // the
                            // Combo
                            // popup
                        },
                        items: [{
                            text: 'xplot',
                            handler: radiusHandler,
                            checked: true,
                            group: 'radius'
                        }, {
                            text: 'yplot',
                            handler: radiusHandler,
                            checked: false,
                            group: 'radius'
                        }, {
                            text: 'area',
                            handler: radiusHandler,
                            checked: false,
                            group: 'radius'
                        }, {
                            text: 'Max Radius',
                            menu: {
                                items: [{
                                    text: '20',
                                    handler: radiusSizeHandler,
                                    checked: false,
                                    group: 'sradius'
                                }, {
                                    text: '30',
                                    handler: radiusSizeHandler,
                                    checked: false,
                                    group: 'sradius'
                                }, {
                                    text: '40',
                                    handler: radiusSizeHandler,
                                    checked: false,
                                    group: 'sradius'
                                }, {
                                    text: '50',
                                    handler: radiusSizeHandler,
                                    checked: true,
                                    group: 'sradius'
                                }, {
                                    text: '60',
                                    handler: radiusSizeHandler,
                                    checked: false,
                                    group: 'sradius'
                                }]
                            }
                        }]
                    });
                    var chart = Ext.create('Ext.chart.Chart', {
                        id: 'chartCmp',
                        xtype: 'chart',
                        style: 'background:#fff',
                        animate: true,
                        store: peptide_plot_store,
                        insetPadding: 50,
                        shadow: true,
                        axes: [{
                            type: 'Numeric',
                            minimum: 0,
                            position: 'left',
                            fields: ['yplot'],
                            label: {
                                renderer: function(v) {
                                    if (v == 0) {
                                        return ''
                                    } else {
                                        return 'Fraction:' + ylabel[parseInt(v - 1)]
                                    }
                                }
                            },
                            title: 'MS1 intensity',
                            minorTickSteps: 1,
                            majorTickSteps: ylabel.length,
                            grid: {
                                odd: {
                                    opacity: 0.15,
                                    fill: '#d93a49',
                                    stroke: '#ef5b9c',
                                    'stroke-width': 0
                                }
                            }
                        }, {
                            type: 'Numeric',
                            position: 'bottom',
                            fields: ['xplot'],
                            label: {
                                renderer: function(v) {
                                    if (v == 0) {
                                        return ''
                                    } else {
                                        return 'Repeat:' + xlabel[parseInt(v - 1)]
                                    }
                                }
                            },
                            title: 'Retention Time',
                            type: 'Numeric',
                            minimum: 0,
                            minorTickSteps: 1,
                            majorTickSteps: xlabel.length,
                            grid: {
                                odd: {
                                    opacity: 0.15,
                                    fill: '#444693',
                                    stroke: '#6a6da9',
                                    'stroke-width': 0
                                }
                            }
                        }],
                        series: [{
                            type: 'scatter',
                            axis: false,
                            xField: 'xplot',
                            yField: 'yplot',
                            color: '#bed742',
                            markerConfig: {
                                type: 'circle',
                                radius: 8,
                                size: 5
                            },
                            tips: {
                                trackMouse: true,
                                width: 580,
                                height: 170,
                                layout: 'fit',
                                items: {
                                    xtype: 'container',
                                    layout: 'hbox',
                                    items: [pieChart, grid]
                                },
                                renderer: function(klass, item) {
                                    var storeItem = item.storeItem;
                                    this
                                    .setTitle('Repeat' + storeItem.get('repeat_id') + '_Fraction_' + storeItem.get('fraction_id') + '( RT:' + storeItem.get('rt') + ', Intensity:' + storeItem.get('intensity') + ', Area:' + storeItem
                                    .get('area') + ")");
                                    grid.setSize(480, 130);
                                }
                            },
                            listeners: {
                                itemmousedown: function(obj) {
                                    var win = Ext.create('Ext.Window', {
                                        width: 1200,
                                        height: 735,
                                        minHeight: 400,
                                        minWidth: 550,
                                        hidden: true,
                                        maximizable: true,
                                        title: 'MS Viewer',
                                        renderTo: Ext.getBody(),
                                        layout: 'fit',
                                        html: '<iframe name="spview" width="100%" height="100%" frameborder=0 src=/gardener/peptide_viwer?sequence=' + obj.storeItem.data['sequence'] + '&charge=' + obj.storeItem.data['charge'] + '&pre_mz=' + obj.storeItem.data['pre_mz'] + '&search_id=' + obj.storeItem.data['search_id'] + '&ms1_scan=' + obj.storeItem.data['ms1_scan'] + '&ms2_scan=' + obj.storeItem.data['ms2_scan'] + '&rt=' + obj.storeItem.data['rt'] + '&ms1_rt=' + obj.storeItem.data['ms1_rt'] + '&filename=' + obj.storeItem.data['filename'] + '&id=' + obj.storeItem.data['id'] + '></iframe>'
                                    });
                                    win.getEl().setStyle('z-index', '80000');
                                    win.show();
                                    // alert(obj.storeItem.data['ms2_scan']
                                    // + '
                                    // &' +
                                    // obj.storeItem.data['ms1_scan']);
                                }
                            }
                        }]
                    });
                    var rank_comb = Ext.create('Ext.form.field.ComboBox', {
                        fieldLabel: 'Choose Batch',
                        store: rank_store,
                        queryMode: 'local',
                        displayField: 'rank',
                        valueField: 'rank_id',
                        forceSelection: true,
                        listeners: {
                            'select': function(combo, record, eOpts) {
                                peptide_plot_store.reload({
                                    params: {
                                        rank: record[0].data.rank_id,
                                        search_id: 2,
                                        pep_sequence: 'VNQIGSVTESIQAcK',
                                        modification: 'Carbamidomethyl (C)(14)'
                                    }
                                });
                                chart.redraw()
                            }
                        }
                    })
                    rank_comb.store.on("load", function(store) {
                        rank_comb.setValue(rank_comb.store.getAt(0).get('rank_id'));
                    }, this);
                    var win = Ext.create('Ext.Window', {
                        draggable: {
                            constrain: true,
                            constrainTo: Ext.getBody()
                        },
                        width: 700,
                        height: 400,
                        minHeight: 100,
                        minWidth: 100,
                        hidden: false,
                        maximizable: true,
                        title: 'Peptide Quantification Plot',
                        animateTarget: 'mescatter',
                        // renderTo : Ext.getBody(),
                        layout: 'fit',
                        tbar: [{
                            text: 'Save Chart',
                            handler: function() {
                                Ext.MessageBox.confirm('Confirm Download', 'Would you like to download the chart as an image?', function(choice) {
                                    if (choice == 'yes') {
                                        chart.save({
                                            type: 'image/png'
                                        });
                                    }
                                });
                            }
                        }, rank_comb, {
                            text: 'Select Color',
                            menu: colorMenu
                        }, {
                            text: 'Select Grayscale',
                            menu: grayscaleMenu
                        }],
                        items: chart
                    });
                    win.show()
                }
            },
            '#mevennplot': {
                click: function() {
                    var data = (Ext.getCmp('info_experiments_selected').getValue()) ? Ext.decode(Ext.getCmp('info_experiments_selected').getValue()) : 0;
                    //Ext.getCmp('info_experiments_selected').setValue(0)
                    var store = Ext.create('gar.store.ExperimentPlot', {
                        data: data
                    });
                    var count = store.getCount();
                    if (count < 2 || count > 4) {
                        Ext.Msg.alert('Venn plot error:', 'Please select 2 or 3 or 4 experiments or repeats.');
                    } else {
                        var exp = store.getExp();
                        var repeat = store.getRepeat();
                        if (exp.length * repeat.length != 0) {
                            Ext.Msg.alert('Venn plot error:', 'Please select one type of data, experiment or repeat!');
                        } else {
                            var type = (exp.length === 0) ? 'repeat' : 'exp';
                            var data = (exp.length === 0) ? repeat.join() : exp.join();
                            var imgList = []
                            var dataViewStore = Ext.create('Ext.data.Store', {
                                fields: ['name', 'url']
                            });
                            //main img initialize
                            var mainImg = Ext.create('Ext.Img', {
                                xtype: 'image',
                                margin: '0 0 0 90'
                                //                              id: 'toolsKHeatmapMainImg' + timestamp
                            })
                            var win = Ext.create('Ext.Window', {
                                width: 650,
                                height: 720,
                                hidden: false,
                                autoScroll: true,
                                maximizable: false,
                                title: 'Venn Plot Viewer',
                                animateTarget: 'mevennplot',
                                // renderTo : Ext.getBody(),
                                layout: 'anchor',
                                //                                      html : '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>',
                                items: [{
                                    xtype: 'panel',
                                    border: 0,
                                    autoScroll: true,
                                    anchor: '100%, 75%',
                                    margin: '10 0 0 0',
                                    //                                          id: 'PlotFrame' + timestamp,
                                    layout: 'absolute',
                                    items: [mainImg]
                                }, {
                                    xtype: 'panel',
                                    cls: 'venn-dataviewpanel',
                                    border: 0,
                                    autoScroll: true,
                                    anchor: '100%, 25%',
                                    //                                          id: 'PlotFrameSouth' + timestamp,
                                    items: [{
                                        xtype: 'dataview',
                                        //                                              id: 'toolsKHeatmapDataView' + timestamp,
                                        store: dataViewStore,
                                        tpl: [
                                        '<tpl for=".">', 
                                        '<div class="thumb-wrap" id="{name:stripTags}">', 
                                        '<div class="thumb"><img src="{url}" title="{name:htmlEncode}" ></div>', 
                                        '<span class="x-editable">{shortName:htmlEncode}</span>', 
                                        '</div>', 
                                        '</tpl>', 
                                        '<br\>', 
                                        '<br\>', 
                                        '<div class="x-clear"></div>'
                                        ],
                                        multiSelect: true,
//                                         height: 310,
                                        itemSelector: 'div.thumb-wrap',
                                        trackOver: true,
                                        emptyText: 'No images to display',
                                        overItemCls: 'x-item-over',
                                        plugins: [
                                        Ext.create('Ext.ux.DataView.DragSelector', {})
                                        // Ext.create('Ext.ux.DataView.LabelEditor', {dataIndex: 'name'})
                                        ],
                                        prepareData: function(data) {
                                            Ext.apply(data, {
                                                shortName: Ext.util.Format.ellipsis(data.name, 15),
                                                sizeString: Ext.util.Format.fileSize(data.size)
                                                // dateString: Ext.util.Format.date(data.lastmod, "m/d/Y g:i a")
                                            });
                                            return data;
                                        },
                                        listeners: {
                                                itemclick: function(me, record, item ){
                                                    if(record.data.name=='Protein')
                                                            mainImg.setSrc(imgList[0])
                                                    else if(record.data.name == 'Peptide')
                                                            mainImg.setSrc(imgList[1])
                                                    else
                                                            mainImg.setSrc('')
                                                }
                                            }
                                    }]
                                }],
                                listeners: {
                                    beforeRender: function() {
                                        //loading pic
                                        // mainImg.setWidth(300)
                                        // mainImg.setHeight(300)
                                        // mainImg.setLocalX(140)
                                        mainImg.setSrc('/static/images/loading/loading5.gif')
                                        Ext.Ajax.request({
                                            timeout: 600000,
                                            url: '/gardener/venn_plot/',
                                            method: 'GET',
                                            params: {
                                                type: type,
                                                data: data
                                            },
                                            success: function(response) {
                                                //set main heatmap img
                                                //mainImg.setWidth(350)
                                                
                                                imgList = response.responseText.split(',')
                                                dataViewStore.add({
                                                    'name': 'Protein',
                                                    'url': imgList[0]
                                                })
                                                dataViewStore.add({
                                                    'name': 'Peptide',
                                                    'url': imgList[1]
                                                })
                                                mainImg.setSrc(imgList[0])
                                            },
                                            failure: function() {
                                            //                                                              win.update("Sorry! Error happen, please contact Admin with current URL.");
                                            }
                                        });
                                    }
                                }
                            });
                            win.show();
                        }
                    }
                }
            },
            '#mekeggtools': {
                click: function() {
                    var actstore = cloneActiveStore();
                    actstore.on("load", function(store) {
                        var syms = actstore.getSym();
                        // var syms = new
                        // Array('FH','PGK1','IDH3A','PDHB','HADHA','GPI','ECHS1','ACAT2','GAPDH','PKM','ALDOA','SCD','PFKFB2','PCK1','ACACA','ACSS2','CPT1A','DLAT','MDH2','BPGM','DGAT1','ALDOA','CS','ACO1','PFKP','GPAM','FASN','OGDH','ME1','HADH','ENO1','DLST','ACLY')
                        // Ext.Msg.alert('WeiLai\'s data',syms)
                        if (syms.length > 0) {
                            var keggsym = syms.join('\r\n');
                            var form = Ext.create('Ext.form.Panel', {
                                title: 'KEGG submitter',
                                layout: 'fit',
                                height: 155,
                                width: 250,
                                hidden: true,
                                url: 'http://www.genome.jp/kegg-bin/color_pathway_object',
                                items: [{
                                    xtype: 'textfield',
                                    name: 'org',
                                    value: 'ko'
                                }, {
                                    xtype: 'textareafield',
                                    name: 'unclassified',
                                    value: keggsym
                                }, {
                                    xtype: 'textfield',
                                    name: 'target',
                                    value: 'alias'
                                }, {
                                    xtype: 'filefield',
                                    name: 'color_list',
                                    value: ''
                                }, {
                                    xtype: 'textfield',
                                    name: 'reference'
                                }, {
                                    xtype: 'textfield',
                                    name: 'warning',
                                    value: 'yes'
                                }, {
                                    xtype: 'textfield',
                                    name: 'all'
                                }, {
                                    xtype: 'textfield',
                                    name: 'other_dbs',
                                    value: ''
                                }]
                            });
                            form.getForm().doAction('standardsubmit', {
                                standardSubmit: true,
                                method: 'POST',
                                target: '_blank'
                            })
                            // form.submit({
                            // method:'GET',
                            // waitTitle:'Wait for KEGG
                            // connection:',
                            // waitMsg:'Data have
                            // successful submited,
                            // wait for
                            // KEGG mapping tools
                            // response.',
                            // success:
                            // function(form,action){
                            // Ext.Msg.alert('Data',action.responseText)
                            // },
                            // failure:
                            // function(form,action){
                            // Ext.Msg.alert('Error',action.response.msg)
                            // }
                            // })
                        } else {
                            Ext.Msg.alert('Warning', 'Please do the pathway maping at the grid with symbol column.');
                        }
                    }, this);
                    actstore.load()
                }
            },
            '#help': {
                click: function() {
                    window.open('/gardener/help/', "manul", "toolbar=yes, location=yes, directories=yes, status=yes, menubar=yes, scrollbars=yes, resizable=yes, copyhistory=yes, width=800, height=600");
                }
            },
            //          '#entrez' : {
            //              click : function() {
            //                  window.open('http://www.ncbi.nlm.nih.gov/', "_blank", "toolbar=yes, location=yes, directories=yes, status=yes, menubar=yes, scrollbars=yes, resizable=yes, copyhistory=yes, width=900, height=500");
            //              }
            //          },
            // '#upload_jsp' : {
            //  click : function() {
            //      // window.open('http://61.50.134.132:8080/swfUpLoad/indexSupp.jsp', "_blank", "toolbar=no,
            //      // location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes,
            //      // copyhistory=no, width=630, height=380");
            //      window.location.href = '/upload/firmianaUpload.jnlp'
            //  }
            // },
            '#entrez1': {
                click: function() {
                    var newwin = new Ext.Window({
                        // xtype: 'window',
                        title: "NCBI",
                        // modal: 'true', //can only click this window
                        width: 950,
                        height: 450,
                        maximizable: true,
                        // closeAction:'hide',
                        minimizable: true,
                        contentEl: Ext.DomHelper.append(document.body, {
                            tag: 'iframe',
                            src: 'http://www.ncbi.nlm.nih.gov/',
                            height: "100%",
                            width: "100%"
                        })
                    });
                    newwin.minimize = function(e) {
                        this.hide();
                        // this.show();
                    }
                    newwin.show(this);
                }
            },
            '#btfilemaker': {
                click: function() {
                    var data = (Ext.getCmp('info_experiments_selected').getValue()) ? Ext.decode(Ext.getCmp('info_experiments_selected').getValue()) : 0;
                    //Ext.getCmp('info_experiments_selected').setValue(0)
                    if (data == 0)
                        Ext.Msg.alert('No exp selected', 'Please choose at least one Experiment !')
                    var s = '?_dc=' + (new Date()).valueOf();
                    if (data != 0)
                        len = data.length
                    // console.log(len)
                    var ids = ''
                    fraction_num = -1
                    for (i = 0; i < len; i++) {
                        ids = ids + String(data[i].id) + ','
                        if (fraction_num == -1)
                            fraction_num = data[i].num_fraction
                        else if (data[i].num_fraction != fraction_num)
                            fraction_num = -2
                    }
                    s = s + '&sid=' + ids
                    window.open('/gardener/ispec_output/' + s);
                }
            },
            '#btreactome': {
                click: function() {
                    // openReactomePanel = function() {
                    //     view = Ext.widget('reactometool', {
                                        
                    //     });
                    // }
                    // openReactomePanel()
                    // if (!Ext.getCmp('reactomeTool')) {
                    //     Ext.Msg.alert('Testing function','This tool is still testing...',openReactomePanel)
                    // } else {
                    //     Ext.getCmp('reactomeTool').show()
                    // }
                    var tab = Ext.getCmp('content-panel')
                    var panel = Ext.widget('reactometool', {

                    });
                    tab.add({
                        title: 'Reactome',
                        iconCls: 'btreactome',
                        closable: true,
                        layout: 'fit',
                        items: [panel]
                    }).show();
                }
            },
            '#btpublic': {
                click: function() {
                    var data = (Ext.getCmp('info_experiments_selected').getValue()) ? Ext.decode(Ext.getCmp('info_experiments_selected').getValue()) : 0;
                    var len = (data != 0) ? data.length : 0
                    var explist = ''
                    var fraction_num = -1
                    var columndata
                    for (i = 0; i < len; i++) {
                        explist = explist + String(data[i].id) + ','
                    }
                    var companyStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/all_company/',
                            extraParams: {
                                share: 'True'
                            },
                            reader: {
                                type: 'json',
                                root: 'all_company'
                            }
                        },
                        fields: [{
                            name: 'company',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var labStore = Ext.create('Ext.data.Store', {
                        proxy: {
                            type: 'ajax',
                            url: '/experiments/ajax/all_lab/',
                            extraParams: {
                                share: 'True'
                            },
                            reader: {
                                type: 'json',
                                root: 'all_lab'
                            }
                        },
                        fields: [{
                            name: 'lab',
                            type: 'string'
                        }],
                        autoLoad: true
                    });
                    var win = new Ext.Window({
                        title: 'Share to Another Lab',
                        width: 400,
                        items: [{
                            xtype: 'form',
                            border: 0,
                            margin: '10 10 10 10',
                            // frame : true,
                            items: [{
                                xtype: 'combobox',
                                displayField: 'company',
                                name: 'company',
                                valueField: 'company',
                                store: companyStore,
                                queryMode: 'local',
                                emptyText: 'Company',
                                width: 300,
                                listeners: {
                                    select: {
                                        fn: function(combo, records, index) {
                                            var lab = Ext.getCmp("share-exp-lab");
                                            lab.clearValue();
                                            lab.store.load({
                                                params: {
                                                    id: records[0].data.company
                                                }
                                            })
                                        }
                                    }
                                }
                            }, {
                                xtype: 'combobox',
                                displayField: 'lab',
                                valueField: 'lab',
                                name: 'lab',
                                id: 'share-exp-lab',
                                emptyText: 'Laboratory',
                                store: labStore,
                                queryMode: 'local',
                                width: 300
                            }]
                        }],
                        bbar: ['->', {
                            text: 'Submit',
                            handler: function() {
                                Ext.Ajax.request({
                                    url: '/gardener/sendtopublic/',
                                    params: {
                                        explist: explist,
                                        lab: Ext.getCmp('share-exp-lab').getRawValue()
                                    },
                                    success: function(response) {
                                        var text = response.responseText;
                                        responseJson = Ext.JSON.decode(text);
                                        Ext.Msg.alert('Success', 'Request was successfull. Result is: ' + String(Ext.encode(responseJson.msg)));
                                    }
                                });
                            }
                        }]
                    });
                    win.show();
                }
            }
        })
    }
})
