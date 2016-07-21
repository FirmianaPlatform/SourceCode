
Ext.Loader.setPath('Ext.ux', '/static/ext4/examples/ux');
Ext.Loader.setConfig({
			enabled : true
		});

Ext.application({
			requires : ['Ext.grid.*', 'Ext.data.*', 'Ext.util.*', 'Ext.tree.*', 'Ext.grid.plugin.BufferedRenderer', 'Ext.ux.form.SearchField',
					'Ext.ux.grid.FiltersFeature', 'Ext.ux.grid.FiltersFeatureAdvanced','Ext.toolbar.Paging', 'Ext.chart.*', 'Ext.Window', 'Ext.fx.target.Sprite', 'Ext.layout.container.Fit',
					'Ext.window.MessageBox', 'Ext.tip.*', 'Ext.selection.CheckboxModel','Ext.tab.*','Ext.ux.TabCloseMenu'],
			name : 'gar',
			appFolder : 'app',
			views : ['Tools'],
			controllers : ['Experiment', 'Menu', 'Statebar','User','NewCompare','Metadata','GlobalPlot', 'ExperimentInfoLink_sampleDetail', 'ExperimentInfoLink_reagentDetail', 'ExperimentInfoLink_separationDetail'],

			launch : function() {

				Ext.create('gar.view.Viewport', {
							layout : 'fit',
							items : [{
										id : 'desk',
										layout : 'border',
										items : [	//Ext.create('gar.view.WestNavi'),
													
													Ext.create('gar.view.Menu'), 
													Ext.create('gar.view.TabPanel'), 
													Ext.create('gar.view.State')
												]
									}]
							}
				);	
				var uname = Ext.util.Cookies.get("username");
	  	  		//Ext.getElementById('loading_pic').innerHTML = '';
				Ext.getElementById('loading_pic').style.display = 'none';
	  	  		if(uname=='guest')
	  	  			{
	  	  				Ext.getCmp('newcompare').disable();
	  	  				//Ext.getCmp('anywhere').disable();
	  	  				//Ext.getCmp('anywhere-combo').disable();
	  	  				Ext.getCmp('changepw').hide();
	  	  				Ext.getCmp('btcube').disable();
	  	  				Ext.getCmp('addexperiment').disable();
	  	  				Ext.getCmp('addsample').disable();
	  	  				Ext.getCmp('addreagent').disable();
	  	  			};
			}

		});
/*Ext.onReady(function(){
	var p = Ext.getCmp('west_navi')
	p.collapse()
	});*/