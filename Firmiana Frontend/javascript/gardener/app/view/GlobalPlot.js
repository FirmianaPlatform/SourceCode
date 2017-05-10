Ext.define('gar.view.GlobalPlot', {
    extend: 'Ext.window.Window',
    alias: 'widget.globalplot',
    
    title: 'Global Search Plot',
    layout: 'border',
    defaults: {
        collapsible: true,
        split: true,
        bodyPadding: 15
    },
    width: 670,
    height: 660,
    autoShow: true,
    layout: 'anchor',
    
    
    initComponent: function() {
        var htmlstring = '<iframe scrolling="auto" frameborder="0" width="100%" height="100%" src="' + '/static/canvasxpress/';
        var timestamp = (new Date()).valueOf();
        var act = Ext.getCmp('content-panel').activeTab.items;
        var data = Ext.getCmp(String(act.items[0].id)).filters.getFilterData();
        var filterText = '[';
        for (i = 0; i < data.length; i++) {
            filterText += '{'
            temp = String(Ext.encode(data[i].data))
            filterText += temp.substr(1, temp.length - 2)
            filterText += ',"field":"'
            filterText += String(data[i].field)
            filterText += '"}'
            if (i != data.length - 1)
                filterText += ','
        }
        ;
        filterText += ']';
        
        text = '';
        var xstr = '';
        var ystr = '';
        var zstr = '';
        
        var xaxis = Ext.create('Ext.data.Store', {
            fields: ['name'],
            data: [
                {"name": "Tissue/Cell_Type"}
            ]
        });

        var yaxis = Ext.create('Ext.data.Store', {
            fields: ['name'],
            data: [
                {"name": "Treatment"}
            ]
        });
        
        var zaxis = Ext.create('Ext.data.Store', {
            fields: ['name'],
            data: [
                {"name": "Area"}, 
                {"name": "iBAQ"}, 
                {"name": "iFOT"}
            ]
        });
        
        var plotframe = Ext.create('Ext.panel.Panel', {
            height: 670,
            anchor: '100%', 
        	//layout:'fit', 
            html: "<canvas id='canvas4' width='100' height='100'></canvas>"
        });
        
        
        this.items = [
	        // {
	        // 	title: 'Details',
	        //     region: 'south',
	        //     items: []
	        // },
            {
                region: 'center',
                collapsible: false,
                bodyPadding: 0,
                layout: {
                    type: 'vbox',
                    align: 'stretch'
                },
                items: [
                    {
                        xtype: 'toolbar',
                        items: [{
                                xtype: 'combo',
                                fieldLabel: 'X Axis:',
                                editable: false,
                                id: 'xaxis',
                                store: xaxis,
                                width: 150,
                                labelWidth: 50,
                                displayField: 'name'
                            }, {
                                xtype: 'combo',
                                fieldLabel: 'Y Axis:',
                                editable: false,
                                id: 'yaxis',
                                store: yaxis,
                                width: 150,
                                labelWidth: 50,
                                displayField: 'name'
                            }, 
                            ' Z Axis:',{
                                xtype: 'combo',
                                editable: false,
                                id: 'zaxis',
                                store: zaxis,
                                width: 90,
                                displayField: 'name'
                            },'-',{
                                text: 'Plot Type',
                                menu: [{
                                    text: '3D Histogram',
                                    handler: function() {
                                    	var loading = '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>';
                                    	plotframe.update(loading);
                                        //updateHtmlString = htmlstring + 'bar2.html' + '"></iframe>';
                                    	updateHtmlString = "<canvas id='canvas4' width='540' height='540'></canvas>"

                                        console.log(Ext.getCmp('anywhere').getRawValue(),filterText,Ext.getCmp("xaxis").getRawValue(),Ext.getCmp("yaxis").getRawValue(),Ext.getCmp("zaxis").getRawValue())
                                        
                                        Ext.Ajax.request({
                                            method: "GET",
                                            timeout : 6000000,
                                            url: '/api/gardener/show3DplotDataDemo/',
                                            //http://www.firmiana.org/api
                                            //url: 'http://www.firmiana.org/api/gardener/show3DplotDataDemo/',
                                            params: {
                                                symbol: Ext.getCmp('anywhere').getRawValue(),
                                                start: 0,
                                                limit: -1,
                                                filter: filterText,
                                                xstr: Ext.getCmp("xaxis").getRawValue(),
                                                ystr: Ext.getCmp("yaxis").getRawValue(),
                                                zstr: Ext.getCmp("zaxis").getRawValue()
                                            },
                                            success: function(response) {
                                                text = response.responseText
                                                responseJson = Ext.JSON.decode(text);
                                                
                                                vars = responseJson.data.organList;
                                                //vars[0] = "no organInfo";
                                                smps = responseJson.data.treatmentList;
                                                //smps[0] = "no treatmentInfo";
                                                if(Ext.getCmp("zaxis").getRawValue()=="Area"){
                                                	zValue = "Area(*1e+6)";
                                                }
                                                else if(Ext.getCmp("zaxis").getRawValue()=="iBAQ"){
                                                	zValue = "iBAQ(*1e+6)";
                                                }
                                                else{//iFOT
                                                	zValue = "iFOT(*10^-6)";
                                                }
                                                
                                                
                                                data = responseJson.data.organ_treatment_multilist;
                                                
                                                // process server response here
                                                // sessionStorage.setItem("test_text", text);
                                                plotframe.update(updateHtmlString);
                                                var cx4 = new CanvasXpress('canvas4',{
                                                	'y' : {
              											'vars' : vars,	//x
              											'smps' : smps,	//y
              											'data' : data,	//z
              											'desc' : [zValue, 'Value']
               											}
          											},
          											{
          												"xAxisTitle": zValue,
  														"yAxisTitle": "-",
  														
  														'fontStyle': "Times New Roman",
  														
  														"legendFontStyle": "Times New Roman",
  														
  														"smpLabelFontStyle": "Times New Roman",
  														
  														"colorScheme": "light",
  														
          												'bar3DInverseWeight': 1.2,
          												'graphType': 'Bar',
          												'is3DPlot': true,
          												'scatterType': 'bar',
          												'x3DRatio': 0.5
          											}
        										);
                                            }
                                        });
                                    }
                                }, {
                                    text: 'Bar Plot',
                                    handler: function() {
                                    	var loading = '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>';
                                    	plotframe.update(loading);
                                        //updateHtmlString = htmlstring + 'bar3.html' + '"></iframe>';
                                    	updateHtmlString = "<canvas id='canvas4' width='540' height='540'></canvas>"
                                        // xstr = Ext.getCmp("xaxis").getRawValue();
                                        // ystr = Ext.getCmp("yaxis").getRawValue();
                                        // zstr = Ext.getCmp("zaxis").getRawValue();
                                        // sessionStorage.setItem("xstr_sto", xstr);
                                        // sessionStorage.setItem("ystr_sto", ystr);
                                        // sessionStorage.setItem("zstr_sto", zstr);
                                        
/*                                        Ext.Ajax.request({
                                            method: "GET",
                                            timeout : 600000,
                                            url: 'http://61.50.134.132/api/gardener/show3DplotDataDemo/',
                                            params: {
                                                symbol: Ext.getCmp('anywhere').getRawValue(),
                                                start: 0,
                                                limit: -1,
                                                filter: filterText,
                                                xstr: Ext.getCmp("xaxis").getRawValue(),
                                                ystr: Ext.getCmp("yaxis").getRawValue(),
                                                zstr: Ext.getCmp("zaxis").getRawValue()
                                            },
                                            success: function(response) {
                                                text = response.responseText;
                                                // process server response here
                                                sessionStorage.setItem("test_text", text);
                                                plotframe.update(updateHtmlString);
                                            }
                                        });*/
                                    	 Ext.Ajax.request({
                                            method: "GET",
                                            timeout : 600000,
                                            //url: 'http://61.50.134.132/api/gardener/show3DplotDataDemo/',
                                            url: '/api/gardener/show3DplotDataDemo/',
                                            params: {
                                                symbol: Ext.getCmp('anywhere').getRawValue(),
                                                start: 0,
                                                limit: -1,
                                                filter: filterText,
                                                xstr: Ext.getCmp("xaxis").getRawValue(),
                                                ystr: Ext.getCmp("yaxis").getRawValue(),
                                                zstr: Ext.getCmp("zaxis").getRawValue()
                                            },
                                            success: function(response) {
                                                text = response.responseText
                                                responseJson = Ext.JSON.decode(text);
                                                
                                                vars = responseJson.data.organList;
                                                vars[0] = "no organInfo";
                                                smps = responseJson.data.treatmentList;
                                                smps[0] = "no treatmentInfo";
                                                if(Ext.getCmp("zaxis").getRawValue()=="Area"){
                                                	zValue = "Area(*1e+6)";
                                                }
                                                else if(Ext.getCmp("zaxis").getRawValue()=="iBAQ"){
                                                	zValue = "iBAQ(*1e+5)";
                                                }
                                                else{//iFOT
                                                	zValue = "iFOT(*10^-6)";
                                                }
                                                
                                                
                                                data = responseJson.data.organ_treatment_multilist;
                                                
                                                // process server response here
                                                // sessionStorage.setItem("test_text", text);
                                                plotframe.update(updateHtmlString);
                                                var cx4 = new CanvasXpress('canvas4',{
                                                	'y' : {
              											'vars' : vars,	//x
              											'smps' : smps,	//y
              											'data' : data,	//z
              											'desc' : [' ', ' ']
               											}
          											},
          											{
          												'axisTickScaleFontFactor': 1.5,
          												'axisTitleScaleFontFactor': 1.5,
          												'fontStyle': 'bold italic',
          												'graphOrientation': 'vertical',
          												'graphType': 'Bar',
          												'legendBox': false,
          												'legendFontStyle': 'italic',
          												'legendScaleFontFactor': 1.2,
          												'plotByVariable': true,
          												'showShadow': true,
          												'smpLabelFontStyle': 'italic',
          												'smpLabelInterval': 2,
          												'smpLabelRotate': 45,
          												'smpLabelScaleFontFactor': 0.8,
          												'smpTitle': xstr,
          												'smpTitleScaleFontFactor': 1.5,
          												'title': 'Distribution Plot',
          												'titleHeight': 60,
          												"xAxisTitle": zValue,
          												'xAxis2Show': false
          											}
        									);}
                                        });
                                    	
                                    }
                                }]
                            }
                        ]
                    }, 
                    plotframe
                ]
            }
        ];
        this.callParent(arguments);
    }

});
