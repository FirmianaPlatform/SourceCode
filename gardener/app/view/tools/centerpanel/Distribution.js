Ext.define('gar.view.tools.centerpanel.Distribution', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.Distribution',
    width: 600,
    split: true,
    floatable: false,
    closable: true,
    title: 'Distribution',
    /**
     * @requires 'gar.view.Notice'
     */
    requires: [
        'gar.view.Notice'
    ],
    
    initComponent: function() {
        
        Ext.tip.QuickTipManager.init();
        var east_temp_panel = Ext.widget('east' + this.title.replace(" ", ""));
        this.objEastPanel.add(east_temp_panel);
        this.objEastPanel.setActiveTab(east_temp_panel);
        
        this.on('activate', function() {
            this.objEastPanel.setActiveTab(east_temp_panel)
        })
        
        this.on('close', function() {
            east_temp_panel.close()
        })
        var val = this.val
        var timestamp = (new Date()).valueOf();
        var statis = 'Average';
        var temp_name = this.temp_name
        var gridType = this.gridType
        var mainImgUrl = ''
        switch(groupLevel)
        {
            case 1: {
                var plot_level = Ext.create('Ext.data.Store', {
                    fields: ['name'],
                    data : [
                        {"name": 'Group'}
                    ]
                })
                break
            }
            case 2: {
                var plot_level = Ext.create('Ext.data.Store', {
                    fields: ['name'],
                    data : [
                        {"name": 'Group'},
                        {"name": 'Condition'}
                    ]
                })
                break
            }
            case 3: {
                var plot_level = Ext.create('Ext.data.Store', {
                    fields: ['name'],
                    data : [
                        {"name": 'Group'},
                        {"name": 'Condition'},
                        {"name": 'Experiment'}
                    ]
                })
                break
            }
            default: break
        }
        
        var getColumn = function(columndata, level) {
            var startNum
            if (newcolumndata[1].dataIndex == 'Sequence') {
                startNum = 5
            } else {
                startNum = 7
            }
            out = [];
            if (level == 'Group') 
            {
                for (var i = startNum; i < columndata.length; i++) {
                    out.push(columndata[i].dataIndex);
                }
            } 
            else if (level == 'Condition') 
            {
                for (var i = startNum; i < columndata.length; i++) {
                    var gNode = columndata[i]
                    for (var j = 0; j < gNode.columns.length; j++) {
                        out.push(gNode.columns[j].dataIndex)
                    }
                }
            } 
            else if (level == 'Experiment') 
            {
                for (var i = startNum; i < columndata.length; i++) {
                    var gNode = columndata[i]
                    for (var j = 0; j < gNode.columns.length; j++) {
                        var cNode = gNode.columns[j]
                        var tempStr = ''
                        for (var k = 0; k < cNode.columns.length; k++) {
                            out.push(cNode.columns[k].columns[0].columns[0].dataIndex + '|' + cNode.columns[k].columns[0].columns[0].dataIndex)
                        }
                    }
                }
            }
            compare_grid = Ext.getCmp(info_compare_tool_index);
            temp_filter = compare_grid.filters.buildQuery(compare_grid.filters.getFilterData());
            return [out, temp_filter];
        };
        
        var get = function(columndata, level) {
            temp = getColumn(columndata, level);
            out = temp[0];
            temp_filter = temp[1];
        
        };


        /*	type is the plot type
			tryNormalize is the normalize style
				|	1. old plot
				|	2. old and new plot
				|	3. new plot only
		*/
        var plot = function(type, tryNormalize) {
            
            var loading = '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>';
            var level = Ext.getCmp('plotlevel' + timestamp).getRawValue();
            var val = String(rec.get('csv_name'));
            mainImg.setSrc('')
            Ext.getCmp('PlotFrame' + timestamp).update(loading);
            get(columndata, level);

            Ext.Ajax.request({
                timeout: 600000,
                url: '/gardener/newcmpprotein/',
                method: 'GET',
                params: {
                    id: val,
                    levels: out,
                    filter: temp_filter,
                    R_type: type,
                    statistical: statis,
                    tryNormalize: tryNormalize,
                    temp_name: temp_name,
                    gridType: gridType,
                    normalizationLevel: normalizationLevel
                },
                success: function(response) {
                    if (tryNormalize == 1) 
                    {
                        // console.log(response.responseText);
                        Ext.getCmp('PlotFrame' + timestamp).update('');
                        jsonObject = Ext.JSON.decode(response.responseText)

                        //set main heatmap img
                        mainImg.setSrc('')
                        mainImg.setHeight(350)
                        mainImg.setLocalX(140)
                        mainImgUrl = jsonObject.img
                        mainImg.setSrc(mainImgUrl)
                    }
                    if (tryNormalize == 2) 
                    {
                        // mainImg.setSrc('')
                        var jsonObject = Ext.JSON.decode(response.responseText)
                        // Ext.getCmp('PlotFrame' + timestamp).update(jsonObject.img);
                        
                        var normalizeConfirmWindow = Ext.create(Ext.window.Window, {
                            title: 'Normalization',
                            height: 450,
                            width: 700,
                            autoShow: true,
                            modal: true,
                            html: jsonObject.img,
                            dockedItems: [{
                                    dock: 'bottom',
                                    ui: 'footer',
                                    xtype: 'toolbar',
                                    // layout: {
                                    //     pack: 'center',
                                    //     align: 'middle'
                                    // },
                                    border: 1,
                                    style: {
                                        borderColor: 'rgb(56,146,211)',
                                        borderStyle: 'solid'
                                    },
                                    items: ['<b>Normalization is done. Would you like to submit changes?</b>','->',{
                                            text: 'YES',
                                            width: 70,
                                            handler: function() {
                       //                      	add a new param into grid store named "Nomalize"
				                           		var tmpStore = Ext.getCmp(info_compare_tool_index).getStore()
				                    			tmpStore.getProxy().extraParams['normalizationLevel'] = normalizationLevel
				                    			tmpStore.getProxy().extraParams['levels'] = out
				                    			tmpStore.load()
				                    			normalizeConfirmWindow.close()

                                                normalizationLevel = 'Distribution_' + Ext.getCmp('plotlevel' + timestamp).value
				                     			//plot again

				                    			plot('boxplot',3)
				                    			// createGrid()
                                            }
                                        }, {
                                            text: 'NO',
                                            width: 70,
                                            handler: function() {
                                            	plot('boxplot',1)
                                            	normalizeConfirmWindow.close()
                                            }
                                        }]
                                }]
                        })

                    // Ext.Msg.show({
                    //     			title: 'Normalization',
                    //     			msg: 'Normalization is done. Would you like to submit changes?',
                    //     			buttons: Ext.Msg.OKCANCEL,
                    //     			icon: Ext.Msg.QUESTION,
                    //     			fn: function(btn) {
                    //         if (btn === 'ok') {
                    //             //add a new param into grid store named "Nomalize"
                    //        		var tmpStore = Ext.getCmp(info_compare_tool_index).getStore()
                    // 			tmpStore.getProxy().extraParams['Normalize'] = true
                    // 			tmpStore.getProxy().extraParams['level'] = out
                    // 			tmpStore.load()

                    // 			//plot again
                    // 			plot('boxplot',3)
                    // 			createGrid()
                    //         } else {
                    //             console.log('Cancel pressed');
                    //         } 
                    //     }
                    //     		})
                    }
                    if (tryNormalize == 3) 
                    {
                        // console.log(response.responseText);
                        Ext.getCmp('PlotFrame' + timestamp).update('');
                        jsonObject = Ext.JSON.decode(response.responseText)

                        //set main heatmap img
                        mainImg.setSrc('')
                        mainImg.setHeight(350)
                        mainImg.setLocalX(140)
                        mainImgUrl = jsonObject.img
                        mainImg.setSrc(mainImgUrl)
                    }

                    //pop success msg
                    Ext.example.msg('Suceess', 'Plotting done.')
                },
                failure: function() {
                    Ext.getCmp('PlotFrame' + timestamp).update("Sorry! Error happen, please contact Admin with current URL.");
                }
            });
        }
        
        var createGrid = function() {
            var timestamp = (new Date()).valueOf()
            var tab = Ext.getCmp('content-panel');
            var store = Ext.create('Ext.data.Store', {
                autoLoad: true,
                buffered: true,
                pageSize: 10000,
                model: 'dynamicModel',
                leadingBufferZone: 300,
                proxy: {
                    type: 'ajax',
                    method: 'POST',
                    timeout: 3000000,
                    url: '/gardener/newcmpprotein/',
                    reader: {
                        type: 'json',
                        root: 'data',
                        metaProperty: 'metaData',
                        totalProperty: 'total'
                    },
                    extraParams: {
                        id: val,
                        temp_name: temp_name,
                        gridType: gridType
                    }
                },
            // listeners : {
            // 	totalcountchange : onStoreSizeChange,
            // 	metachange : function(store, meta) {
            // 	}
            // }
            });
            var grid = Ext.create('gar.view.MBRun', {
                store: store,
                dockedItems: [{
                        dock: 'top',
                        xtype: 'toolbar',
                        items: [{
                                text: 'testing',
                                handler: function() {
                                }
                            }]
                    }]
            })
            tab.add({
                title: 'After Normalization',
                closable: true,
                layout: 'fit',
                items: []
            }).show()
        }

        //main img initialize
        var mainImg = Ext.create('Ext.Img', {
            xtype: 'image',
            id: 'toolsDistributionMainImg' + timestamp
        })

        var statisMenu = Ext.create('Ext.menu.Menu',{
            defaults: {
                checked: false,
                group: 'statismunu' + timestamp
            },
            items: [{
                text: 'Average',
                checked: true,
                handler: function() {
                    statis = 'Average'
                }
            },{
                text: 'Median',
                handler: function() {
                    statis = 'Median'
                }
            }]
        })
        
        this.items = [{
                xtype: 'toolbar',
                ui: 'header',
                border: 0,
                items: [{
                        xtype: 'combo',
                        id: 'plotlevel' + timestamp,
                        fieldLabel: 'Plot level:',
                        editable : false,
                        value: plot_level.last().data.name,
                        width: 185,
                        labelWidth: 65,
                        store: plot_level,
                        displayField: 'name'
                    }, {
                        text: 'Statistical',
                        menu: statisMenu
                    }, {
                        xtype: 'button',
                        text: 'GO',
                        handler: function() {
                            plot('boxplot', 1)
                        }
                    }, {
                        xtype: 'button',
                        text: 'Normalization',
                        handler: function() {
                            //plot function
                            if(Ext.getCmp('plotlevel' + timestamp).value != plot_level.last().data.name)
                                Ext.Msg.alert('Warning','Choose right plot level before normalization.')
                            else
                            {
                                plot('boxplot', 2)
                            }


                        //  		var statusBarStackNormalization = Ext.create('Ext.ux.statusbar.StatusBar', {
                        //     text: 'Normalization is done. Would you like to submit changes?',
                        //     cls: 'toolsControlPanel_alert_yellow',
                        //     items: [{
                        //     	xtype: 'button',
                        //     	text: 'Yes',
                        //     	handler: function() {
                        //     		//add a new param into grid store named "Nomalize"
                        //     		var tmpStore = Ext.getCmp(info_compare_tool_index).getStore()
                        // tmpStore.getProxy().extraParams['Normalize'] = true
                        // tmpStore.getProxy().extraParams['level'] = out
                        // tmpStore.load()

                        // //plot again
                        // plot('boxplot',3)

                        //     		//status bar notice
                        //     		Ext.getCmp('toolsStatusBarPanel').remove(statusBarStackNormalization)
                        //     		var statusBarInitial = Ext.widget('toolsStatusBar')
                        //    Ext.getCmp('toolsStatusBarPanel').add(statusBarInitial)
                        //    Ext.getCmp('toolsStatusBar').setStatus({
                        //     text: 'Submit changes successfully.',
                        //     clear: {
                        //         wait: 2000,
                        //         anim: true,
                        //         useDefaults: true
                        //     }
                        // });
                        //     	}
                        //     },{
                        //     	xtype: 'button',
                        //     	text: 'No',
                        //     	handler: function() {
                        //     		Ext.getCmp('toolsStatusBarPanel').remove(statusBarStackNormalization)
                        //     		var statusBarInitial = Ext.widget('toolsStatusBar')
                        //    Ext.getCmp('toolsStatusBarPanel').add(statusBarInitial)
                        //    Ext.getCmp('toolsStatusBar').setStatus({
                        //     text: 'Submitting canceled.',
                        //     clear: {
                        //         wait: 2000,
                        //         anim: true,
                        //         useDefaults: true
                        //     }
                        // });
                        //     	}
                        //     }
                        //     ]
                        // })
                        //Ext.getCmp('toolsStatusBarPanel').add(statusBarStackNormalization)
                        }
                    }, '->', 
                    {
                        xtype: 'button',
                        text: 'Download'
                    }
                // {
                //     xtype: 'textfield',
                //     width: 170,
                //     labelWidth: 45,
                //     name: 'protein search',
                //     fieldLabel: 'Search',
                //     emptyText: 'Protein Search',
                //     labelAlign: 'right'
                // }
                ]
            }, {
                xtype: 'panel',
                border: 0,
                autoScroll: true,
                id: 'PlotFrame' + timestamp,
                layout: 'absolute',
                height: 600,
                items: [mainImg],
                html: ''
            }
        ];
        this.callParent(arguments);
    }
});
