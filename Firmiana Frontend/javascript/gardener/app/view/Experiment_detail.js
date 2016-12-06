Ext.define('gar.view.Experiment_detail', {
			extend : 'Ext.form.Panel',
			alias : 'widget.experiment_detail',
			border : true,
			bodyPadding : '10 0 10 10',
			defaults : {
				labelWidth : 80,
				labelAligh : 'left',
				width : 600,
				editable : false,
				allowBlank : false
			},
			items : [{
						fieldLabel : 'Exp_name',
						xtype : 'displayfield'
					}, {
						fieldLabel : 'Experimenter',
						xtype : 'displayfield'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Date'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Funding'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Execution'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Type'
					}, {
						fieldLabel : 'Description',
						xtype : 'displayfield'
						
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Sample No',
						renderer : function(value) {
							var panel = this.up('panel')
							// console.log(panel)
							// panel.items.add(separationPanel)
							cssstring = '<div title="Click to view Sample Deatail" class="x-grid3-cell-inner" style="text-align:left;';
							cssstring += '">' + "<a href='#'>"
							return cssstring + value + '</a>' + '</div>'
						}
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Reagent No',
						renderer : function(value) {
							var panel = this.up('panel')
							// console.log(panel)
							// panel.items.add(separationPanel)
							cssstring = '<div title="Click to view Reagent Deatail" class="x-grid3-cell-inner" style="text-align:left;';
							cssstring += '">' + "<a href='#'>"
							return cssstring + value + '</a>' + '</div>'
						}
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Sepration',
						renderer : function(value) {
							var panel = this.up('panel')
							// console.log(panel)
							// panel.items.add(separationPanel)
							//return value
							cssstring = '<div title="Click to view Seperation Deatail" class="x-grid3-cell-inner" style="text-align:left;';
							cssstring += '">' + "<a href='#'>"
							return cssstring + value + '</a>' + '</div>'
						}
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Digest'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Database Params'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Dynamic Modifications'
					},{
						xtype : 'displayfield',
						fieldLabel : 'Fixed Modifications'
					},{
						xtype : 'displayfield',
						fieldLabel : 'IspecNo'
					}, {
						xtype : 'displayfield',
						fieldLabel : 'Comments'
					}]
		})
