Ext.define('gar.controller.ExperimentInfoLink_reagentDetail', {
	extend : 'Ext.app.Controller',
	views : ['User'],
	init : function() {
		reagentDetailLink=function(text){
			var win = Ext.create('Ext.Window', {
				layout: {
					type: 'hbox',
					align: 'left'
				},
				autoScroll : true,
				resizable : true,
				title : 'Detailed Information of ' + text,
				width : 700,
				height : 450,
				items : []
			});
			win.show();
			expList = text.split(';')
			for(expL = 0; expL < expList.length; expL++) {
				Ext.Ajax.request({
					url : '/experiments/load/reagent/',
					params : {
						reagent_no : expList[expL].split('Rea')[1]
						// csrfmiddlewaretoken : csrftoken
					},
					success : function(response) {
						var panel = Ext.create('gar.view.Reagent_detail')
						var text = response.responseText;
						reaResponseJson = Ext.JSON.decode(text).data;
						Reagent_name=String(reaResponseJson.Reagent_name)
						//console.log(Reagent_name)
						while (Reagent_name.length<6){
							Reagent_name='0'+Reagent_name}
							eagent_name='Rea'+Reagent_name
							panel.items.items[0].setValue(Reagent_name)
							panel.items.items[1].setValue(reaResponseJson.company + '/ ' + reaResponseJson.lab + '/ ' + reaResponseJson.experimenter)
							panel.items.items[2].setValue(reaResponseJson.date)
							panel.items.items[3].setValue(reaResponseJson.reagent_type)
							panel.items.items[4].setValue(reaResponseJson.Reagent_manufacturer)
							panel.items.items[5].setValue(reaResponseJson.catalog_no)
							panel.items.items[6].setValue(reaResponseJson.Conjugate)
							panel.items.items[7].setValue(reaResponseJson.Application)
							panel.items.items[8].setValue(reaResponseJson.React_species_source)
							panel.items.items[9].setValue(reaResponseJson.React_species_target)
							panel.items.items[10].setValue(reaResponseJson.Ispec_num)
							//panel.items.items[9].setValue(reaResponseJson.React_species_target)
							win.insert(0, panel)
						}
					});
					// console.log(win)
			}
				
		}
	}
});