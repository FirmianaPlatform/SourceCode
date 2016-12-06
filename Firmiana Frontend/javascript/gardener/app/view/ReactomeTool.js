Ext.define('gar.view.ReactomeTool',{
	// extend: 'Ext.window.Window',
	extend: 'Ext.panel.Panel',

	/**
	 * @requires 
	 */
	requires: [
		''
	],

	alias: 'widget.reactometool',
	layout: 'fit',
	padding: 0,
	id: 'reactomeTool',
	header:{
		titlePosition: 2,
		titleAlign: 'center'
	},
	maximizable: true,
	header: false,
	width: 1200,
	height: 660,
	autoShow: true,
	closeAction: 'destroy',

	/**
	 * @method initComponent
	 * @inheritdoc
	 * @return {void}
	 */
	initComponent: function() {
		me = this
		this.center()

		var pathwayStore = Ext.create('Ext.data.Store',{
			fields:['dbId','pathwayName','speciesName']
		})
		var reactometoolResultGrid = Ext.create('Ext.grid.Panel',{
			anchor: '100% 30%',
			id: 'reactometoolResultGrid',
			columns: [
				{text: 'dbID',				dataIndex: 'dbId',			flex: 1},
				{text: 'Pathway Name',		dataIndex: 'pathwayName',	flex: 6},
				{text: 'Entities pValue',	flex: 2},
				{text: 'Entities FDR',		flex: 2},
				{text: 'Species Name', 		dataIndex: 'speciesName',	flex: 3}
			],
			store: pathwayStore
		})

		var reactometoolResultGridLoadMask = new Ext.LoadMask(reactometoolResultGrid, {
			msg : 'Loading.....'
		});

		type = 'application/json'
		function doPost(url, type, body) {
			ajax = new XMLHttpRequest();
			ajax.open("POST", url, true);

			ajax.setRequestHeader("Content-type", "text/plain");
			ajax.setRequestHeader("Accept", type);

			ajax.onreadystatechange = function() {
				if(ajax.readyState == 4 && ajax.status == 200) {
					jsonObject = JSON.parse(ajax.responseText)
					for(i = 0; i < jsonObject.length; i++){
						pathwayStore.add({'dbId':jsonObject[i].dbId,'pathwayName':jsonObject[i].displayName,'speciesName':jsonObject[i].speciesName})
					}
					reactometoolResultGridLoadMask.hide()
				}
			};
			ajax.send(body);
		}

		function queryHitPathways(type, body) {
			url = "/reactome/ReactomeRESTfulAPI/RESTfulWS/queryHitPathways";
			// body="SMC1\nSMC3\nRAD21\nSTAG2\nSTAG1";
			doPost(url, type, body);
		}

		//Creating the Reactome Diagram widget
	    //Take into account a proxy needs to be set up in your server side pointing to www.reactome.org
	    function onReactomeDiagramReady(width,height){  //This function is automatically called when the widget code is ready to be used
	        var diagram = Reactome.Diagram.create({
	            "proxyPrefix" : "/reactome",
	            "placeHolder" : "diagramHolder",
	            "width" : width*0.98,
	            "height" : height*0.95
	        });

	        //Initialising it to the "Metabolism of nucleotides" pathway
	        diagram.loadDiagram("R-HSA-15869");

	        //Adding different listeners

	        diagram.onDiagramLoaded(function (loaded) {
	            console.info("Loaded ", loaded);
	            diagram.selectItem("R-HSA-111804");
	            diagram.flagItems("TXN");
	        });

	        diagram.onObjectHovered(function (hovered){
	            console.info("Hovered ", hovered);
	        });

	        diagram.onObjectSelected(function (selected){
	            console.info("Selected ", selected);
	        });
	    }

		this.items = [{
			xtype: 'tabpanel',
			id: 'reactometoolTabpanel',
		    tabPosition: 'left',
		    minTabHeight: 180,
			items: [{
				title: 'Analysis',
				layout: 'border',
				items: [{
					xtype: 'form',
					region: 'center',
					flex: 2,
					border: 1,
					layout: {
						type: 'vbox',
						align: 'stretch'
					},
					items: [{
						xtype: 'combo',
						store: Ext.create('Ext.data.ArrayStore',{
							fields: ['species'],
							data: [
								['Homo sapiens']
							]
						}),
						displayField: 'species',
						emptyText: 'Choose a species',
						allowBlank: false,
						fieldLabel: 'Pathways for',
						queryMode: 'local',
						name: 'species',
						editable: false,
						margin: '12 10 0 10'
					},{
						xtype: 'textarea',
						fieldLabel: 'Gene list',
						name: 'genelist',
						allowBlank: false,
						hideLabel: true,
						id: 'reactometoolGenelist',
						margin: '10 10 15 10',
						emptyText: 'Input your genes here.',
						flex: 1
					}],
					dockedItems: [{
						xtype: 'toolbar',
						dock: 'bottom',
						border: 1,
						padding: 8,
						layout: {
							pack: 'center'
						},
						items: [{
							minWidth: 80,
							text: 'Submit',
							handler: function(){
								var panel = Ext.getCmp('reactometoolTabpanel')
								var form = panel.down('form')
								if (form.isValid()){
									formValue = form.getValues()
									queryText = formValue.genelist
									for (j = queryText.length - 1; queryText.charAt(j) == "\n"; j--){}
										queryText = queryText.substring(0, j + 1)
									queryText = queryText.split('\n').join(',')
									panel.setActiveTab(1)
									reactometoolResultGridLoadMask.show();
									queryHitPathways(type, queryText)
									Ext.getCmp('reacometoolResultDiagram').update('<div id="diagramHolder"></div>')
									var width = Ext.getCmp('reacometoolResultDiagram').getWidth()
									var height = Ext.getCmp('reacometoolResultDiagram').getHeight()
									onReactomeDiagramReady(width,height)
								}
							}
						},{
							minWidth: 80,
							text: 'Clear',
							handler: function(){
								Ext.getCmp('reactometoolGenelist').reset()
							}
						}]
					}]
				},{
					xtype: 'panel',
					region: 'east',
					flex: 1,
					border: 1,
					layout: 'border',
					items: [{
						xtype: 'panel',
						height: 180,
						border: 0,
						region: 'north',
 						html:'<div style="margin: 25px 15px 10px 15px"><h1 align="center" style="color: blue">Analyse your data</h1><h4>This tool merges pathway identifier mapping, overrepresentation and expression analysis into a single tabbed data analysis portal, with integrated visualization and summary features.</h4></br><h3>Sample data:</h3></div>'
					},{
						xtype: 'panel',
						region: 'center',
						border: 0,
						items: [{
							xtype: 'button',
							minWidth: 180,
							margin: '0 0 0 15',
							text:'Gene name list',
							handler: function(){
								Ext.getCmp('reactometoolTabpanel').down('textarea').setValue('SMC1\nSMC3\nRAD21\nSTAG2\nSTAG1')
							}
						}]
					}]
				}]
			},{
				title: 'Result',
				width: 300,
				layout: 'anchor',
				items: [{
					xtype: 'panel',
					anchor: '100% 70%',
					id: 'reacometoolResultDiagram',
					padding: 10
				},reactometoolResultGrid]
			}]
			// controller: 'ReactomeTool',
		}]
		this.callParent(arguments);
	},
})