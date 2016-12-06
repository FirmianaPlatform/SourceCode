Ext.define('gar.view.Reagent_detail', {
			extend : 'Ext.form.Panel',
			alias : 'widget.reagent_detail',
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
						fieldLabel : 'Reagent_name',
						xtype : 'displayfield'
					}, {
						fieldLabel : 'Experimenter',
						xtype : 'displayfield'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Date'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Reagent_type'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Manufaturer'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Catalog No.'
					}, {
						fieldLabel : 'Conjugate Beads',
						xtype : 'displayfield'
						
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Application',
						renderer : function(value) {
							var panel = this.up('panel')
							// console.log(panel)
							// panel.items.add(separationPanel)
							return value
						}
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Source Species'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Target Species'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'IspecNo'
					}]
		})
