Ext.define('gar.view.tools.centerpanel.PCA', {
	extend : 'Ext.panel.Panel',
	alias : 'widget.PCA',
	width : 600,
	split : true,
	floatable : false,
	closable : true,
	title : 'PCA',
	layout:'border',
	/**
	 * @requires 'gar.view.Notice'
	 */
	requires : ['gar.view.Notice'],
	initComponent : function() {
		var east_temp_panel = Ext.widget( 'east' + this.title );
	    this.objEastPanel.add(east_temp_panel);
	    this.objEastPanel.setActiveTab(east_temp_panel);
	    
	    this.on('activate', function() { 
			this.objEastPanel.setActiveTab(east_temp_panel)
		}) 		
		
	    this.on('close', function() { 
			east_temp_panel.close()
		}) 		
		var timestamp = (new Date()).valueOf();
		var statis = 'Average';
		var loading = '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>';
		var preImage=tmpFile=tmpMetaFile=tmpHtml=tmpSrcMetadata=tmpSrcCorMatrixFile='', metadataJson=[];
		var tmpFileAdjust = tmpMetaFileAdjust = tmpHtmlAdjust = tmpSrcMetadataAdjust = tmpSrcCorMatrixFileAdjust = '', metadataJsonAdjust = [];
		var ifAdjust = 0;
		// disable normalization button
		var normalizationButtonDisable = true
    	var temp_name = this.temp_name
    	var gridType = this.gridType
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
		var plotlevel = plot_level.last().data.name;
		var pc_opt = Ext.create('Ext.data.Store', {
					fields : ['name'],
					data : [{
								"name" : 'PC1'
							}, {
								"name" : 'PC2'
							}, {
								"name" : 'PC3'
							}]
				});

		var getColumn = function(columndata, level) {
			outExperiment = [];
			outCondition = [];
			var startNum;
            if (newcolumndata[1].dataIndex == 'Sequence') {
                startNum = 5
            } else {
                startNum = 7
            }
//            if (level == 'Group') 
//            {
//                for (var i = startNum; i < columndata.length; i++) {
//                    out.push(columndata[i].dataIndex);
//                }
//            } 
//            else if (level == 'Condition') 
//            {} 
            
            for (var i = startNum; i < columndata.length; i++) {
                var gNode = columndata[i]
                for (var j = 0; j < gNode.columns.length; j++) {
                    outCondition.push(gNode.columns[j].dataIndex)
                }
            }
            
//            else if (level == 'Experiment') {}
            
			for (var i = startNum; i < columndata.length; i++) {
				var gNode = columndata[i]
				for (var j = 0; j < gNode.columns.length; j++) {
					var cNode = gNode.columns[j]
					var tempStr = ''
					for (var k = 0; k < cNode.columns.length; k++) {
						outExperiment.push(cNode.columns[k].columns[0].columns[0].dataIndex + '|' + cNode.columns[k].columns[0].columns[0].dataIndex)
					}
				}
			}
			
			compare_grid = Ext.getCmp(info_compare_tool_index);
			temp_filter = compare_grid.filters.buildQuery(compare_grid.filters.getFilterData());
			return [outCondition, outExperiment, temp_filter];
		};

		var get = function(columndata, level) {
			temp = getColumn(columndata, level);
			outCondition = temp[0];
			outExperiment = temp[1]; 
			temp_filter = temp[2];

		};
		
		var toolsPcaPc1='PC1',toolsPcaPc2='PC2';
		
		var pcaStart = function(){
			if(toolsPcaPc1 == toolsPcaPc2){
					Ext.Msg.alert('Warning','Choose different PCs.');
					return
			}		
//			if (plotlevel != plot_level.last().data.name) {
//				Ext.Msg.alert('Warning', 'Need '+plot_level.last().data.name+' level.');
//				return
//			}
			plotlevel = 'Condition'
			get(columndata, plotlevel);
	
			if (outExperiment.length < 3) {
				Ext.Msg.alert('Warning', 'Sample number must be greater than <b>THREE</b>.');
				//Ext.getCmp('PlotFrame' + timestamp).update("<div style='padding:20px'>Sample number must be more than 3.</div>");
				return
			}
			
			var plot = function(type,objWin) {	

				var centerWin = Ext.getCmp('PlotFrame'+timestamp)
				//var level = Ext.getCmp('plotlevel' + timestamp).getRawValue();
				var pcList = toolsPcaPc1 + ',' + toolsPcaPc2;
				var val = String(rec.get('csv_name'));
				// var type = 'boxplot';

				centerWin.update(loading);
	
				var metadataList = ''
				//var checkList = Ext.getCmp('eastpanelPCA').down('panel').items.items[0].items.items
				var checkList = objWin.down('panel').down('fieldset').items.items
				Ext.Array.forEach(checkList, function(x) {
							if (x.checked) {
								metadataList = metadataList + x.name + ';'
							}
						})
				if (metadataList == '') {
					Ext.Msg.alert('Warning', 'Select one or more metadata.');
					return
				}
				objWin.close();
				Ext.Ajax.request({
					timeout : 600000,
					url : '/gardener/newcmpprotein/',
					method : 'POST',
					params : {
						id : val,
						levels : outExperiment,
						conditionLevels : outCondition,
						filter : temp_filter,
						R_type : type,
						statistical : statis,
						pcList : pcList,
						metadataList : metadataList,
						temp_name:temp_name,
						gridType:gridType,
						normalizationLevel: normalizationLevel
					},
					success : function(response) {
						ifAdjust++;
						//console.log(response);
						var tmpResponse = Ext.JSON.decode(response.responseText);
						preImage = tmpResponse.imageSrc
						tmpHtml = tmpResponse.tmpHtml
						tmpFile = tmpResponse.tmpFile
						tmpMetaFile = tmpResponse.tmpMetaFile
						tmpSrcMetadata = tmpResponse.tmpSrcMetadata
						tmpSrcCorMatrixFile = tmpResponse.tmpSrcCorMatrixFile
						metadataJson = tmpResponse.dataMeta
						//['expName', 'species','instrument', 'dateOfExperiment', 'dateOfOperation',  'method','separation','sex','age','reagent','sample','tissueType','strain']
						centerWin.update(tmpHtml);

						//pop success msg
						Ext.example.msg('Suceess','Plotting done.')
					},
					failure : function() {
						centerWin.update("<div style='padding:20px'>Sorry! Error happen, please contact Admin with current URL.</div>");
					}
				});
			}
						
			var win = new Ext.Window({
					modal:true,
					title : 'Metadata',
					width : 310,
					height : 480,
					animateTarget: 'toolsPcaStart' + timestamp,
					bodyPadding : 0,
					//maximizable : true,
					resizable : false,
					buttons: [
						{
							text: 'OK',
							handler :function(){
								plot( 'pca', this.up().up() )
							}
						},
						{
							text: 'Cancel',
							handler:function(){this.up().up().close();}
						}
					],
					items : [Ext.widget('pcaMetaMenu')]
				}).show();
		}
		
		var pcaAdjust = function() {

			if (ifAdjust == 0) {
				Ext.Msg.alert('Warning', 'Execute normal PCA before adjustment.');
				return
			}
//			if (plotlevel != plot_level.last().data.name) {
//				Ext.Msg.alert('Warning', 'Execute adjustment under ' + plot_level.last().data.name + ' level.');
//				return
//			}
			var funAdjustAjax = function()
			{	
				var centerWin = Ext.getCmp('PlotFrame'+timestamp)
				var loading = '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>';
				var val = String(rec.get('csv_name'));
				var pcList = toolsPcaPc1 + ',' + toolsPcaPc2;
				var metadataList = '' 
				//var checkList = this.up().up().down('panel').items.items[0].items.items
				var checkList = this.up().up().down('panel').down('fieldset').items.items
				Ext.Array.forEach(checkList, function(x) {
							if (x.checked) {
								metadataList = metadataList + x.name + ';'
							}
						})
				if (metadataList == '') {
					Ext.Msg.alert('Warning', 'Select one or more metadata.');
					return
				}
				this.up().up().close()// close adjustment window
				
				centerWin.update(loading);
				
				Ext.Ajax.request({
						timeout : 600000,
						url : '/gardener/newcmp_pcaAdjust/',
						method : 'GET',
						params : {
							id : val,
							pcList:pcList,
							preImage : preImage,
							preSrcCorMatrixFile:tmpSrcCorMatrixFile,
							tmpFile : tmpFile,
							tmpMetaFile : tmpMetaFile,
							todo_metalist : metadataList
						},
						success : function(response) {
							//{"adjustedFile":adjustedFile, "ok":1,'code':code}
							//console.log(response);
							var tmpResponse = Ext.JSON.decode(response.responseText);
							var adjustedFile_static = tmpResponse.adjustedFile_static
							var ok = tmpResponse.ok
							var code = tmpResponse.code
							
							if(ok){
								tmpHtmlAdjust = tmpResponse.tmpHtml
								tmpFileAdjust = tmpResponse.tmpFile
								tmpMetaFileAdjust = tmpResponse.tmpMetaFile
								tmpSrcMetadataAdjust = tmpResponse.tmpSrcMetadata
								tmpSrcCorMatrixFileAdjust = tmpResponse.tmpSrcCorMatrixFile
								metadataJsonAdjust = tmpResponse.dataMeta
								//['expName', 'species','instrument', 'dateOfExperiment', 'dateOfOperation',  'method','separation','sex','age','reagent','sample','tissueType','strain']
								centerWin.update(tmpHtmlAdjust);
								
								Ext.Msg.alert('OK', 'Adjust done.');
								//window.open(adjustedFile_static,'','height=300,width=400,top=0,left=0,toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no');
								//window.open(adjustedFile_static, "manul", "toolbar=yes, location=yes, directories=yes, status=yes, menubar=yes, scrollbars=yes, resizable=yes, copyhistory=yes, width=800, height=600");
							}
							else{
								Ext.Msg.alert('Error', 'Adjustment failed.');
								centerWin.update(tmpHtml);
							}
						},
						failure : function() {
							Ext.Msg.alert('Error', 'Adjustment failed.(Unable to adjust.)');
							centerWin.update(tmpHtml);
						}
					});
				
			}

			var win = new Ext.Window({
					modal:true,
					title : 'Metadata',
					width : 310,
					height : 480,
					animateTarget: 'toolsPcaAdj' + timestamp,
					bodyPadding : 0,
					//maximizable : true,
					resizable : false,
					buttons: [
						{
							text: 'OK',
							handler : funAdjustAjax
						},
						{
							text: 'Cancel',
							handler:function(){this.up().up().close();}
						}
					],
					items : [Ext.widget('pcaMetaMenu')]
			
				}).show();
				
			
		}
		var abc = function(){}
		
		var viewMetadata = function(viewType) {
			//Ext.getCmp('eastpanelPCA').removeAll()				
			
			var val = String(rec.get('csv_name'));
			get(columndata, plotlevel);
			
			var store = east_temp_panel.down('grid').getStore();
			store.getProxy().extraParams = {
				forMetaMatrix:1,
				id : val,
				levels : outExperiment,
				filter : temp_filter,
				R_type : 'pca',
				statistical : 'statis',
				pcList : 'pcList',
				metadataList : 'metadataList'
			};
			store.load()
			//Ext.getCmp('eastpanelPCA').add(goGrid);
			
//			var win = new Ext.Window({
//				title : viewType,
//				x:10,
//				y:10,
//				width : 800,
//				height : 350,
//				animateTarget: 'toolsPcaView'+viewType + timestamp,
//				bodyPadding : 0,
//				maximizable : true,
//				resizable : true,
//				layout:'fit',
//				//html : '<iframe name="" id="" width="100%" height="100%" frameborder=0 src=' + fileSrc + '></iframe>'
//				items:[goGrid]
//			}).show();
		}
		
		var viewCorrelation = function(viewType) {
			var fileSrc = tmpSrcCorMatrixFile
			if(fileSrc)	
			{
				var win = new Ext.Window({
					title : viewType,
					width : 1100,
					height : 350,
					animateTarget: 'toolsPcaView'+viewType + timestamp,
					bodyPadding : 0,
					maximizable : true,
					resizable : true,
					html : '<iframe name="" id="" width="100%" height="100%" frameborder=0 src=' + fileSrc + '></iframe>'
			
				}).show();
			}
			else{ Ext.Msg.alert('Warning', 'Execute PCA first.'); }

		}

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
		
		this.items = [
			{
				region:'north',
				xtype : 'toolbar',
				border : '0 0 1 0',
				items : 
				[
				
//							{
//								xtype : 'combo',
//								//id : 'plotlevel' + timestamp,
//								editable : false,
//								fieldLabel : 'Plot level:',
//								value : plot_level.last().data.name,
//								scale: 'large',
//								rowspan: 3,
//								width : 175,
//								labelWidth : 65,
//								store : plot_level,
//								displayField : 'name',
//					            listeners: {
//					            	change: function(item, newvalue) {
//					            		plotlevel = newvalue
//					            	}
//					            }
//							}, 
							{
								xtype : 'combo',
								//id : 'toolsPcaPc1' + timestamp,
								editable : false,
								fieldLabel : 'X:',
								value : 'PC1',
								width : 88,
								labelWidth : 18,
								store : pc_opt,
								displayField : 'name',
					            listeners: {
					            	change: function(item, newvalue) {
					            		toolsPcaPc1 = newvalue
					            	}
					            }
							},
							{
								xtype : 'combo',
								//id : 'toolsPcaPc2' + timestamp,
								editable : false,
								fieldLabel : 'Y:',
								value : 'PC2',
								width : 88,
								labelWidth : 18,
								store : pc_opt,
								displayField : 'name',
					            listeners: {
					            	change: function(item, newvalue) {
					            		toolsPcaPc2 = newvalue
					            	}
					            }
							}, {
								text: 'Statistical',
					        	menu: statisMenu
				        	}, {
								xtype : 'button',
								text : 'Start',
								id : 'toolsPcaStart' + timestamp,
								//scale: 'large',
								//rowspan: 3,
								handler : function() {
									pcaStart()
									normalizationButtonDisable = false
								}
							},
							{
								id:'toolsPcaViewMetadata'+ timestamp,
								xtype : 'button',
								text : 'View Metadata',
								handler:function(){viewMetadata('Metadata')}
							}, 
							{
								id:'toolsPcaViewCorrelation'+ timestamp,
								xtype : 'button',
								text : 'View Correlation',
								handler:function(){viewCorrelation('Correlation')}
							},
							{
								xtype : 'button',
								text : 'Adjust',
								id : 'toolsPcaAdj' + timestamp,
								handler : function() {
									pcaAdjust();
		
									// Status bar notice
									//Ext.getCmp('toolsStatusBarPanel').removeAll()
//									var statusBarStackNormalization = Ext.create(
//											'Ext.ux.statusbar.StatusBar', {
//												text : 'PCA Normalization is done. Would you like to submit changes?',
//												cls : 'toolsControlPanel_alert_yellow',
//												items : [{
//													xtype : 'button',
//													text : 'Yes',
//													handler : function() {
//														// add a new param into grid
//														// store named "Nomalize"
//														// var tmpStore =
//														// Ext.getCmp(info_compare_tool_index).getStore()
//														// tmpStore.getProxy().extraParams['Normalize']
//														// = true
//		
//														// status bar notice
//														Ext.getCmp('toolsStatusBarPanel').remove(statusBarStackNormalization)
//														var statusBarInitial = Ext.widget('toolsStatusBar')
//														Ext.getCmp('toolsStatusBarPanel').add(statusBarInitial)
//														Ext.getCmp('toolsStatusBar').setStatus({
//																	text : 'Submit changes successfully.',
//																	clear : {
//																		wait : 2000,
//																		anim : true,
//																		useDefaults : true
//																	}
//																});
//													}
//												}, {
//													xtype : 'button',
//													text : 'No',
//													handler : function() {
//														Ext.getCmp('toolsStatusBarPanel').remove(statusBarStackNormalization)
//														var statusBarInitial = Ext.widget('toolsStatusBar')
//														Ext.getCmp('toolsStatusBarPanel').add(statusBarInitial)
//														Ext.getCmp('toolsStatusBar').setStatus({
//																	text : 'Submitting canceled.',
//																	clear : {
//																		wait : 2000,
//																		anim : true,
//																		useDefaults : true
//																	}
//																});
//													}
//												}]
//											})
//									Ext.getCmp('toolsStatusBarPanel').add(statusBarStackNormalization)
								}
							}
//							, 
//							{
//								xtype : 'button',
//								text : 'Download'
//							}					
						
//					{
//						xtype: 'buttongroup',
//						columns: 6,
//						//title: 'Options',
//						items: 
//						[]
//					}
				]
			},
			{
				region:'center',
				xtype : 'panel',
				border : 0,
				id : 'PlotFrame' + timestamp,
				//layout : 'fit',
				//height : 600,
				autoScroll:true,
				html : ''
			}];
		this.callParent(arguments);
	}
});