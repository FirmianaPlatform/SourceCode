Ext.define('gar.view.ppi', {
    extend: 'Ext.window.Window',

    /**
     * @requires gar.view.Tools.ToolType
     */
    requires: [
        'Ext.tip.QuickTipManager'
    ],
    alias: 'widget.ppi',
    layout: 'border',
    padding: 0,
    header: {
        titlePosition: 2,
        titleAlign: 'center'
    },
    maximizable: true,
    minimizable: true,
    
    width: 1400,
    height: 700,
    autoShow: true,
    closable: true,
    closeAction: 'destroy',
    listeners: {
        "minimize": function(window, opts) {
            window.collapse();
            window.setWidth(150);
            window.alignTo(Ext.getBody(), 'bl-bl')
        }
    },
    tools: [{
            type: 'restore',
            handler: function(evt, toolEl, owner, tool) {
                var window = owner.up('window');
                window.setWidth(1200);
                window.expand('', false);
                window.center();
            }
        }],
    /**
     * @method initComponent
     * @inheritdoc
     * @return {void}
     */
    initComponent: function() {
        var proteinIdControl = this.proteinIdControl
        var proteinIdCaseList = this.proteinIdCaseList

        console.log(proteinIdCaseList)

        this.title = 'PPI Analysis: ' + proteinIdControl
        var me = this
        var startFlag = false

        //case protein list
        var storeProteinCase = Ext.create('Ext.data.Store', {
            fields: [{
                name: 'proteinName',
                type: 'string'
            }]
        })
        for(var i = 0; i < proteinIdCaseList.length; i++){
            storeProteinCase.add({'proteinName': proteinIdCaseList[i]})
        }
        var gridProteinCase = Ext.create('Ext.grid.Panel', {
            forceFit: true,
            anchor: '100% 100%',
            store: storeProteinCase,
            columns: [
                {text: 'Protein name', dataIndex: 'proteinName'}
            ],
            bbar: [{
                xtype: 'button',
                text: 'Add',
                handler: function() {
                    Ext.Msg.prompt('Add protein', 'Please enter the right gi number:', function(btn, text){
                        if (btn == 'ok'){
                            // process text value and close...
                            giText = 'gi|'
                            for(var i = 0; i < text.length; i++){
                                if(text[i] >= '0' && text[i] <= '9'){
                                    giText += text[i]
                                }
                            }
                            storeProteinCase.add({'proteinName': giText})
                        }
                    })
                }
            },{
                xtype: 'button',
                text: 'Delete',
            }],
            listeners: {
                'selectionchange': function(view, record){
                    me.down('panel').down('panel').query('textfield')[1].setValue(record[0].data.proteinName)
                }
            }
        })

        //exp1List, exp2List
        var storeProtein1 = Ext.create('Ext.data.Store', {
            proxy : {
                type : 'ajax',
                url : '/api/gardener/ppi_analysis/',
                reader : {
                    type : 'json',
                    root : 'proteinName1',
                    totalProperty : 'total',
                    successProperty: 'success'
                }
            },
            fields : [{
                        name : 'expName',
                        type : 'string'
                    },{
                        name : 'fot',
                        type : 'float'
                    }]
        });

        var storeProtein2 = Ext.create('Ext.data.Store', {
            proxy : {
                type : 'ajax',
                url : '/api/gardener/ppi_analysis/',
                reader : {
                    type : 'json',
                    root : 'proteinName2'
                }
            },
            fields : [{
                        name : 'expName',
                        type : 'string'
                    },{
                        name : 'fot',
                        type : 'float'
                    }]
        });

        Ext.define('Score', {
            extend: 'Ext.data.Model',
            idProperty: 'scoreId',
            fields: [
                {name: 'comparedProtein',      type: 'string'},
                {name: 'expression',            type: 'float'},
                {name: 'orthology',             type: 'float'},
                {name: 'localization',          type: 'float'},
                {name: 'domainCo_occurrence',  type: 'float'},
                {name: 'ptmCo_occurrence',     type: 'float'},
                {name: 'disorder',              type: 'float'},
                {name: 'transitive',            type: 'float'},
                {name: 'sum',                   type: 'float'}
            ]
        });

        var interactionScoreStore = Ext.create('Ext.data.Store', {
            model: 'Score',
            // sorters: {property: 'due', direction: 'ASC'},
            // groupField: 'project'
        });

        var calculatePearsonScore = function(List) {
            var mean = function(List) {
                var sum = 0
                for(var i = 0; i < List.length; i++){
                    sum += List[i]
                }
                return sum / List.length
            }
            var sd = function(List) {
                var sum = 0
                var avg = mean(List)
                for(var i = 0; i < List.length; i++){
                    sum += (List[i] - avg)*(List[i] - avg)
                }
                return sqrt(sum / (List.length - 1))
            }
            var cov = function(List1, List2) {
                var sum = 0
                var avg1 = mean(List1)
                var avg2 = mean(List2)
                for(var i = 0; i < List.length; i++){
                    sum += (List1[i] - avg1) * (List2[i] - avg2)
                }
                return sum / (List1.length - 1)
            }

            var list1 = []
            var list2 = []
            for(var i = 0; i < List.length; i++){
                list1.push(List[i][1])
                list2.push(List[i][2])
            }
            return cov(list1, list2)/(sd(list1)*sd(list2))
        }

        this.items = [{
                region: 'west',
                xtype: 'panel',
                title: 'Params',
                split: true,
                layout: 'anchor',
                flex: 2,
                collapsible: true,
                items: [{
                    xtype: 'panel',
                    anchor: '100% 50%',
                    hideHeaders: true,
                    bbar: [{
                                xtype: 'button',
                                text: 'Basic info',
                                flex: 1,
                                handler: function() {

                                    var tempObject1 = Ext.getCmp('ppiProtein1Panel')
                                    var tempObject2 = Ext.getCmp('ppiProtein2Panel')

                                    tempObject1.setTitle('Control protein: ' + me.down('panel').down('panel').down('textfield').value) 
                                    tempObject2.setTitle('Case protein: ' + me.down('panel').down('panel').query('textfield')[1].value) 

                                    storeProtein1.load({
                                        params: {
                                            proteinName1: me.down('panel').down('panel').down('textfield').value,
                                            proteinName2: me.down('panel').down('panel').query('textfield')[1].value
                                        },
                                    })

                                    storeProtein2.load({
                                        params: {
                                            proteinName1: me.down('panel').down('panel').down('textfield').value,
                                            proteinName2: me.down('panel').down('panel').query('textfield')[1].value
                                        }
                                    })
                                    
                                    startFlag = true


                                    //chart protein detail function
                                    var barChart1 = Ext.create('Ext.chart.Chart', {
                                        shadow: true,
                                        animate: true,
                                        store: storeProtein1,
                                        axes: [{
                                                type: 'Numeric',
                                                position: 'left',
                                                fields: ['fot'],
                                                minimum: 0,
                                                hidden: false
                                            }, {
                                                type: 'Category',
                                                position: 'bottom',
                                                fields: ['expName'],
                                                hidden: false,
                                                label: {
                                                    renderer: function(v) {
                                                        return Ext.String.ellipsis(v, 15, false);
                                                    },
                                                    font: '5px Arial',
                                                    rotate: {
                                                        degrees: 300
                                                    }
                                                }
                                            }],
                                        series: [{
                                                type: 'line',
                                                axis: 'left',
                                                smooth: true,
                                                xField: 'expName',
                                                yField: ['fot'],
                                                markerConfig: {
                                                    type: 'circle',
                                                    size: 1,
                                                    radius: 1,
                                                    'stroke-width': 0
                                                }
                                            }]
                                    })

                                    var barChart2 = Ext.create('Ext.chart.Chart', {
                                        // height: 200,
                                        // margin: '3 3 3 3',
                                        // autoShow: true,
                                        // autoRender: true,
                                        // cls: 'x-panel-body-default',
                                        shadow: true,
                                        animate: true,
                                        store: storeProtein2,
                                        axes: [{
                                                type: 'Numeric',
                                                position: 'left',
                                                fields: ['fot'],
                                                minimum: 0,
                                                hidden: false
                                            }, {
                                                type: 'Category',
                                                position: 'bottom',
                                                fields: ['expName'],
                                                hidden: false,
                                                label: {
                                                    renderer: function(v) {
                                                        return Ext.String.ellipsis(v, 15, false);
                                                    },
                                                    font: '5px Arial',
                                                    rotate: {
                                                        degrees: 300
                                                    }
                                                }
                                            }],
                                        series: [{
                                                type: 'line',
                                                axis: 'left',
                                                smooth: true,
                                                xField: 'expName',
                                                yField: ['fot'],
                                                markerConfig: {
                                                    type: 'circle',
                                                    size: 1,
                                                    radius: 1,
                                                    'stroke-width': 0
                                                }
                                            }]
                                    })
                                    
                                    tempObject1.items.removeAll()
                                    tempObject1.items.add(barChart1)
                                    tempObject1.update()
                                    tempObject2.items.removeAll()
                                    tempObject2.items.add(barChart2)
                                    tempObject2.update()
                                }
                    },{
                        xtype: 'button',
                        text: 'Calculate',
                        flex: 1,
                        handler: function() {

                            var exp1List = []
                            var exp2List = []
                            storeProtein1.each(function(record){
                                exp1List.push([record.data.expName,record.data.fot])
                            })
                            storeProtein2.each(function(record){
                                exp2List.push([record.data.expName,record.data.fot])
                            })

                            var expIntersectionList = []
                            for(var i = 0; i < exp1List.length; i++){
                                for(var j = 0; j < exp2List.length; j++){
                                    if(exp1List[i][0] == exp2List[j][0]){
                                        expIntersectionList.push([exp1List[i][0], exp1List[i][1], exp2List[j][1]])
                                        break
                                    }
                                }
                            }

                            //intersection exp 
                            var storeProteinIntersection = Ext.create('Ext.data.Store', {
                                fields: [
                                    {name: 'expName', type: 'string'}, 
                                    {name: 'fot1', type: 'float'},
                                    {name: 'fot2', type: 'float'}
                                ]
                            })
                            for (var i = 0; (i < expIntersectionList.length) && (i < 40); i++) {
                                storeProteinIntersection.add({'expName': expIntersectionList[i][0],'fot1': expIntersectionList[i][1],'fot2': expIntersectionList[i][2]})
                            }


                            //chart protein detail function
                            var barChartIntersection = Ext.create('Ext.chart.Chart', {
                                // height: 400,
                                margin: '3 3 3 3',
                                autoShow: true,
                                autoRender: true,
                                shadow: true,
                                animate: true,
                                legend : {
                                    position : 'right'
                                },
                                store: storeProteinIntersection,
                                axes: [{
                                        type: 'Numeric',
                                        position: 'left',
                                        fields: ['fot1','fot2'],
                                        minimum: 0,
                                        title: 'iFot (*10^-6)',
                                        hidden: false,

                                    }, {
                                        type: 'Category',
                                        position: 'bottom',
                                        fields: ['expName'],
                                        label: {
                                            renderer: function(v) {
                                                return Ext.String.ellipsis(v, 15, false);
                                            },
                                            font: '7px Arial',
                                            rotate: {
                                                degrees: 300
                                            }
                                        }
                                    }],
                                series: [{
                                        type: 'line',
                                        axis: 'left',
                                        smooth: true,
                                        xField: 'expName',
                                        yField: ['fot1'],
                                        markerConfig: {
                                            type: 'circle',
                                            size: 4,
                                            radius: 4,
                                            'stroke-width': 0
                                        }
                                    },{
                                        type: 'line',
                                        axis: 'left',
                                        smooth: true,
                                        xField: 'expName',
                                        yField: ['fot2'],
                                        markerConfig: {
                                            type: 'cross',
                                            size: 4,
                                            radius: 4,
                                            'stroke-width': 0
                                        }
                                    }]
                            })
                            Ext.getCmp('ppiPlotPanel').items.removeAll()
                            Ext.getCmp('ppiPlotPanel').items.add(barChartIntersection)
                            Ext.getCmp('ppiPlotPanel').update()


                            var pearsonCoeff = calculatePearsonScore(expIntersectionList)
                            var sum = pearsonCoeff
                            interactionScoreStore.removeAll()
                            interactionScoreStore.add({
                                'comparedProtein': me.down('panel').down('panel').query('textfield')[1].value,
                                'expression': pearsonCoeff.toFixed(3),
                                'sum': sum
                            })
                            Ext.getCmp('ppiPlotGrid').reconfigure()
                        }
                    }],
                    items: [{
                        xtype: 'buttongroup',
                        title: 'Control Protein',
                        titleAlign: 'left',
                        margin: '4 4 4 4',
                        columns: 2,
                        items: [{
                                xtype: 'textfield',
                                name: 'proteinName1',
                                fieldLabel: 'Control Protein: ',
                                value: proteinIdControl,
                                labelAlign: 'top',
                                allowBlank: false
                            }, {
                                xtype: 'textfield',
                                name: 'proteinName2',
                                fieldLabel: 'Case Protein: ',
                                value: proteinIdCaseList[0],
                                labelAlign: 'top',
                                allowBlank: false
                            }]
                    }
                    // , {
                    //     // xtype: 'buttongroup',
                    //     // title: 'Analysis',
                    //     // titleAlign: 'left',
                    //     // margin: '4 4 4 4',
                    //     // columns: 2,
                        
                    // }
                    ]
                },{
                    xtype: 'panel',
                    anchor: '100% 50%',
                    hideHeaders: true,
                    layout: 'anchor',
                    items: [gridProteinCase]
                }]
            }, {
                region: 'center',
                xtype: 'panel',
                hideHeaders: true,
                split: true,
                flex: 5,
                layout: 'anchor',
                items: [{
                    xtype: 'panel',
                    id: 'ppiPlotPanel',
                    hideHeaders: true,
                    anchor: '100% 60%',
                    layout: 'fit',
                },{
                    xtype: 'grid',
                    id: 'ppiPlotGrid',
                    anchor: '100% 40%',
                    forceFit: true,
                    store: interactionScoreStore,
                    columns: [
                        {text: 'Protein',               dataIndex: 'comparedProtein'},
                        {text: 'Expression',            dataIndex: 'expression'},
                        {text: 'Orthology',             dataIndex: 'orthology'},
                        {text: 'Localization',          dataIndex: 'localization'},
                        {text: 'Domain co-occurrence',  dataIndex: 'domainCo_occurrence'},
                        {text: 'PTM co-occurrence',     dataIndex: 'ptmCo_occurrence'},
                        {text: 'Disorder',              dataIndex: 'disorder'},
                        {text: 'Transitive',            dataIndex: 'transitive'},
                        {text: 'Sum',                   dataIndex: 'sum'}
                    ],
                }]
            }, {
                region: 'east',
                xtype: 'panel',
                hideHeaders: true,
                split: true,
                flex: 3,
                layout: 'anchor',
                items: [{
                        xtype: 'panel',
                        id: 'ppiProtein1Panel',
                        title: 'Control protein: ',
                        anchor: '100% 50%',
                        // layout: {
                        //     type: 'vbox',
                        //     align: 'stretch'
                        // },
                        layout: 'fit',
                        items: []
                    }, {
                        xtype: 'panel',
                        id: 'ppiProtein2Panel',
                        title: 'Case protein: ',
                        anchor: '100% 50%',
                        // layout: {
                        //     type: 'vbox',
                        //     align: 'stretch'
                        // },
                        layout: 'fit',
                        items: []
                    }]
            }]
        this.callParent(arguments);
    },
})
