Ext.define('gar.view.Sample_detail', {
			extend : 'Ext.form.Panel',
			alias : 'widget.sample_detail',
			border : true,
			bodyPadding : '10 0 10 10',
			defaults : {
				labelWidth : 120,
				labelAligh : 'left',
				width : 700,
				editable : false,
				allowBlank : false
			},
			items : [{
						fieldLabel : 'Sample_name',
						xtype : 'displayfield'
					}, {
						fieldLabel : 'Experimenter',
						xtype : 'displayfield'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Date'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Sample Location'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Source Type'
					},  {
						xtype : 'displayfield',
						fieldLabel : 'Taxon'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Genotype'
					},{
						xtype : 'displayfield',
						fieldLabel : 'Specific ID'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Subcelluar Organelle'
					},  {
						fieldLabel : 'treatmentCount',
						xtype : 'displayfield'
						
					},  {
						fieldLabel : 'treatmentContent',
						xtype : 'displayfield'
						
					},{
						fieldLabel : 'Protocol',
						xtype : 'displayfield'
						
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Extract Comments'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'IspecNo'
					}]
		});
