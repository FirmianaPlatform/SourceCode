Ext.require(['Ext.tip.QuickTipManager', 'Ext.menu.*',
		'Ext.form.field.ComboBox', 'Ext.layout.container.Table',
		'Ext.container.ButtonGroup']);

Ext.onReady(function() {

	var nav = Ext.create('Ext.toolbar.Toolbar', {
				height:60,
				renderTo : 'nav',
				cls : 'nav-text',
				items : ['Thank you for registration!'/*{
							type : 'button',
							text : 'Home',
							href : '/',
							hrefTarget : ''
						}, {
							text : 'Experiment Management',
							href : '/experiments/experiment',
							hrefTarget : '',
							// <-- submenu by nested config object
							menu : {
								items : [{
											text : 'Experiment Display',
											href : '/experiments/experiment/',
											hrefTarget : ''
										}, {

											text : 'Sample Display',
											href : '/experiments/sample/',
											hrefTarget : ''
											,
										}, {
											text : 'Reagent Display',
											href : '/experiments/reagent/',
											hrefTarget : ''
											,

										}, {
											text : 'Add Experiment',
											href : '/experiments/form/experiment/',
											hrefTarget : ''
											,
										}, {
											text : 'Add Sample',
											href : '/experiments/form/sample/',
											hrefTarget : ''
											,
										}, {
											text : 'Add Reagent',
											href : '/experiments/form/reagent/',
											hrefTarget : ''
											,
										}]
							}
						}, {
							text : 'Analysis Result Display',
							href : '/msanalysis/experiment/',
							hrefTarget : '',
							menu : {
								items : [{
											text : 'Experiment Result Display',
											href : '/msanalysis/experiment/',
											hrefTarget : ''
										}, {

											text : 'Comparison Result Display',
											href : '/LFQuantViewer/comparison/',
											hrefTarget : ''
											,
										}]
							}
						}, 
							{
							text : 'Contact',
							href : '/contact/',
							hrefTarget : ''
							,
						}, 
							{
							text : 'Admin',
							href : '/admin/',
							hrefTarget : '',
							menu : {
								items : [{
											text : 'invite',
											href : '/invite/',
											hrefTarget : ''
										},
										{
											text : 'database admin',
											href : '/admin/',
											hrefTarget : ''
										},]
							}
						}, '->', {
							text : 'logout',
							href : '/logout/'
						}
						*/]
			});
});
