Ext.define('gar.view.Separation_detail', {
	extend : 'Ext.form.Panel',
	alias : 'widget.separation_detail',
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
		xtype : 'displayfield',
		fieldLabel : 'Methods'			
	}, {
		xtype : 'displayfield',
		fieldLabel : 'Separation Method'
	}, {
		xtype : 'displayfield',
		fieldLabel : 'Adjustments'
	}]
});
	
	
	