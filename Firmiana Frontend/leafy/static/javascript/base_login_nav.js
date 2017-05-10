Ext.require(['Ext.tip.QuickTipManager', 'Ext.menu.*',
		'Ext.form.field.ComboBox', 'Ext.layout.container.Table',
		'Ext.container.ButtonGroup',]);

Ext.onReady(function() {

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
							/*{
							text : 'Help',
							href : '',
							hrefTarget : ''
							,
						}, */
							{
							text : 'Contact',
							href : '/contact/',
							hrefTarget : ''
							,
						}, 
							/*{
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
						}*/
						]
			});

		/*
		 * Ext.QuickTips.init();
		 * 
		 * var menu = Ext.create('Ext.menu.Menu', { id: 'mainMenu', style: {
		 * overflow: 'visible' // For the Combo popup }, items: [ combo, // A
		 * Field in a Menu { text: 'I like Ext', checked: true, // when checked
		 * has a boolean value, it is assumed to be a CheckItem checkHandler:
		 * onItemCheck }, '-', { text: 'Radio Options', menu: { // <-- submenu
		 * by nested config object items: [ // stick any markup in a menu '<b
		 * class="menu-title">Choose a Theme</b>', { text: 'Aero Glass',
		 * checked: true, group: 'theme', checkHandler: onItemCheck }, { text:
		 * 'Vista Black', checked: false, group: 'theme', checkHandler:
		 * onItemCheck }, { text: 'Gray Theme', checked: false, group: 'theme',
		 * checkHandler: onItemCheck }, { text: 'Default Theme', checked: false,
		 * group: 'theme', checkHandler: onItemCheck } ] } },{ text: 'Choose a
		 * Date', iconCls: 'calendar', menu: dateMenu // <-- submenu by
		 * reference },{ text: 'Choose a Color', menu: colorMenu // <-- submenu
		 * by reference } ] });
		 * 
		 * var tb = Ext.create('Ext.toolbar.Toolbar'); tb.render('toolbar');
		 * tb.suspendLayouts();
		 * 
		 * tb.add({ text:'Button w/ Menu', iconCls: 'bmenu', // <-- icon menu:
		 * menu // assign menu by instance }, { text: 'Users', iconCls: 'user',
		 * menu: { xtype: 'menu', plain: true, items: { xtype: 'buttongroup',
		 * title: 'User options', columns: 2, defaults: { xtype: 'button',
		 * scale: 'large', iconAlign: 'left' }, items: [{ text: 'User<br/>manager',
		 * iconCls: 'edit', width: 90 },{ iconCls: 'add', tooltip: 'Add user',
		 * width: 40 },{ colspan: 2, text: 'Import', scale: 'small', width: 130
		 * },{ colspan: 2, text: 'Who is online?', scale: 'small', width: 130 }] } } },
		 * Ext.create('Ext.button.Split', { text: 'Split Button', handler:
		 * onButtonClick, tooltip: {text:'This is a an example QuickTip for a
		 * toolbar item', title:'Tip Title'}, iconCls: 'blist', // Menus can be
		 * built/referenced by using nested menu config objects menu : { items: [{
		 * text: '<b>Bold</b>', handler: onItemClick }, { text: '<i>Italic</i>',
		 * handler: onItemClick }, { text: '<u>Underline</u>', handler:
		 * onItemClick }, '-', { text: 'Pick a Color', handler: onItemClick,
		 * menu: { showSeparator: false, items: [ Ext.create('Ext.ColorPalette', {
		 * listeners: { select: function(cp, color){ Ext.example.msg('Color
		 * Selected', 'You chose {0}.', color); } } }), '-', { text: 'More
		 * Colors...', handler: onItemClick } ] } }, { text: 'Extellent!',
		 * handler: onItemClick }] } }), '-', { text: 'Toggle Me', enableToggle:
		 * true, toggleHandler: onItemToggle, pressed: true });
		 * 
		 * menu.add(' '); // Menus have a rich api for // adding and removing
		 * elements dynamically var item = menu.add({ text: 'Dynamically added
		 * Item' }); // items support full Observable API item.on('click',
		 * onItemClick); // items can easily be looked up menu.add({ text:
		 * 'Disabled Item', id: 'disableMe' // <-- Items can also have an id for
		 * easy lookup // disabled: true <-- allowed but for sake of example we
		 * use long way below }); // access items by id or index
		 * menu.items.get('disableMe').disable(); // They can also be referenced
		 * by id in or components tb.add('-', { icon: 'list-items.gif', // icons
		 * can also be specified inline cls: 'x-btn-icon', tooltip: '<b>Quick
		 * Tips</b><br/>Icon only button with tooltip<br><b>Activated on
		 * mousedown</b>', clickEvent: 'mousedown', handler: function(){
		 * Ext.example.msg('Button Click','You clicked the "icon only"
		 * button.'); } }, '-');
		 * 
		 * var scrollMenu = Ext.create('Ext.menu.Menu'); for (var i = 0; i < 50;
		 * ++i){ scrollMenu.add({ text: 'Item ' + (i + 1), handler: onItemClick
		 * }); } // scrollable menu tb.add({ icon: 'preview.png', cls:
		 * 'x-btn-text-icon', text: 'Scrolling Menu', menu: scrollMenu });
		 * 
		 * tb.add({ text: 'Link', url: 'http://www.google.com/search',
		 * baseParams: { q: 'html+anchor+tag' }, tooltip: 'This is a link. You
		 * can right click. You can see where it will take you' });
		 * 
		 * tb.resumeLayouts(true);
		 */

});
