Ext.require(['Ext.tip.QuickTipManager', 'Ext.menu.*',
		'Ext.form.field.ComboBox', 'Ext.layout.container.Table',
		'Ext.container.ButtonGroup',]);

Ext.onReady(function() {

	experiment_display = Ext.create('Ext.menu.Menu', {
    shadow: 'frame',
    allowOtherMenus: true,
    items: [
            {
                text: 'Experiment Display',
                href:'/experiments/experiment/',
                hrefTarget:''
            },{

                text: 'Sample Display',
                href: '/experiments/sample/',
                hrefTarget: '',
            },{
                text: 'Reagent Display',
                href: '/experiments/reagent/',
                hrefTarget: '',
            
            }
    ]
});

experiment_add = Ext.create('Ext.menu.Menu', {
    shadow: 'frame',
    allowOtherMenus: true,
    items: [
            {
                text: 'Add Experiment',
                href: '/experiments/form/experiment/',
                hrefTarget: '',
            },{
                text: 'Add Sample',
                href: '/experiments/form/sample/',
                hrefTarget: '',
            },{
                text: 'Add Reagent',
                href: '/experiments/form/reagent/',
                hrefTarget: '',
            }
    ]
});

	var nav = Ext.create('Ext.toolbar.Toolbar', {
				renderTo : 'nav',
				cls : 'nav-text',
				items : [{
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
								items :  items: [
            {
                type: 'button',
                text:'Home',
                href:'/',
                hrefTarget:''
            },
            	{text: 'Experiment Display', menu: experiment_display}
            ,{text: 'Experiment Add', menu: experiment_add}
            ]
			});

		});s
