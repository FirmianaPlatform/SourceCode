Ext.onReady(function() {

			var nav = Ext.create('Ext.toolbar.Toolbar', {
						renderTo : 'nav',
						cls : 'nav-text',
						items : [{
									text : 'Home',
									href : '/',
									hrefTarget : ''

								}, '->', {
									text : 'login',
									href : 'http://58.198.178.210:8080/user/login',
									hrefTarget : ''
								}]
					});

		});
