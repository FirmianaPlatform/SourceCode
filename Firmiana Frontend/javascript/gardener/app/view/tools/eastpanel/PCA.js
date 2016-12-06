Ext.define("gar.view.tools.eastpanel.PCA", {
    extend: 'Ext.panel.Panel',
    height: 600,
    width: 300,
    layout: 'anchor',
    //id: 'eastpanelPCA',
    closable: false,
    alias: 'widget.eastPCA',
    title: 'Metadata',
    

    /**
     * @method initComponent
     * @inheritdoc
     * @return {void}
     */
    initComponent: function() {
		
			var fileListStore = Ext.create('Ext.data.Store', {
				proxy : {
							type : 'ajax',
							url : '/gardener/newcmpprotein/',
							reader : {
								type : 'json',
								root : 'dataMeta'
							}
						},
				fields : [{
							name : 'expName',
							type : 'string'
						},{
							name : 'species',
							type : 'string'
						},{
							name : 'instrument',
							type : 'string'
						},{
							name : 'dateOfExperiment',
							type : 'string'
						},{
							name : 'dateOfOperation',
							type : 'string'
						},{
							name : 'method',
							type : 'string'
						},{
							name : 'separation',
							type : 'string'
						},{
							name : 'sex',
							type : 'string'
						},{
							name : 'age',
							type : 'string'
						},{
							name : 'reagent',
							type : 'string'
						},{
							name : 'sample',
							type : 'string'
						},{
							name : 'tissueType',
							type : 'string'
						},{
							name : 'strain',
							type : 'string'
						},{
							name : 'circ_time',
							type : 'string'
						}],
						listeners : {},
						autoLoad : false
			});

		
			//fileListStore.sort('Description','DESC');
			var goGrid = Ext.create('Ext.grid.Panel', {
			
				//title: 'File List Grid',
				store : fileListStore,
				anchor: '100% 100%',
				//forceFit:true,
				viewConfig : {
				//trackOver: false,
					stripeRows : true,
					enableTextSelection : true
				},
				defaults : {
					width : 100
				},
				columns : [{
							text : 'Exp Name',
							dataIndex : 'expName'
						},{
							text : 'TaxID',
							dataIndex : 'species'
						},{
							text : 'Instrument',
							dataIndex : 'instrument'
						},{
							text : 'Date Of Experiment',
							dataIndex : 'dateOfExperiment'
						},{
							text : 'Date Of Operation',
							dataIndex : 'dateOfOperation'
						},{
							text : 'Method',
							dataIndex : 'method'
						},{
							text : 'Separation',
							dataIndex : 'separation'
						},{
							text : 'Sex',
							dataIndex : 'sex'
						},{
							text : 'Age',
							dataIndex : 'age'
						},{
							text : 'Reagent',
							dataIndex : 'reagent'
						},{
							text : 'Sample',
							dataIndex : 'sample'
						},{
							text : 'TissueType',
							dataIndex : 'tissueType'
						},{
							text : 'Strain',
							dataIndex : 'strain'
						},{
							text : 'CR Time',
							dataIndex : 'circ_time'
						}]
			
			});
        this.items = [goGrid]
    	this.callParent(arguments);
    }
})