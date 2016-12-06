Ext.define('gar.controller.ExperimentInfoLink_sampleDetail', {
	extend : 'Ext.app.Controller',
	views : ['User'],
	init : function() {
		sampleDetailLink=function(text){
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
			expList = text.split(';');
			for(expL = 0; expL < expList.length; expL++) {
				Ext.Ajax.request({
					url : '/experiments/load/sample/',
					params : {
						sample_no : expList[expL].split('Sam')[1]
						// csrfmiddlewaretoken : csrftoken
					},
					success : function(response) {
						var panel = Ext.create('gar.view.Sample_detail');
						var text = response.responseText;
						samResponseJson = Ext.JSON.decode(text).data;
						Sample_name=String(samResponseJson.Sample_name)
						//console.log(Reagent_name)
						while(Sample_name.length<6){
							Sample_name='0'+Sample_name
						}
						Sample_name='Sam'+Sample_name
						panel.items.items[0].setValue(Sample_name)
						panel.items.items[1].setValue(samResponseJson.company + '/ ' + samResponseJson.lab + '/ ' + samResponseJson.experimenter)
						panel.items.items[2].setValue(samResponseJson.date)
						panel.items.items[3].setValue(samResponseJson.detail_location)
						
						panel.items.items[4].setValue(samResponseJson.cell_tissue)
						panel.items.items[5].setValue(samResponseJson.Source_TissueTaxonAorM + ';' + samResponseJson.tissueName + ';' + samResponseJson.tissueID)
						panel.items.items[6].setValue(samResponseJson.Genotype)
						
						panel.items.items[7].setValue(samResponseJson.Specific_ID)
						panel.items.items[8].setValue(samResponseJson.Ubi_subcell)
						panel.items.items[9].setValue(samResponseJson.treatmentsCount)
						
						
						panel.items.items[11].setValue(samResponseJson.Ubi_method)
						panel.items.items[12].setValue(samResponseJson.comments)
						panel.items.items[13].setValue(samResponseJson.Ispec_num)
						
						//items[10]
						treatmentCount = samResponseJson.treatmentsCount
						var tempStr = ""
						if(treatmentCount>0){
							for(var i=0;i<treatmentCount;i++){
								tempStr = tempStr + "[" + (i+1) + "] " 
											+ "Treatments:"
											+ samResponseJson.rx_treatments[i] + "&"
											+ samResponseJson.rx_treatments_detail[i] + ";"
											//+ samResponseJson.rx_treatments_detail_detail[i] + ";"
											+ "Amount:"
											+ samResponseJson.rx_amount + "-" + samResponseJson.rx_unit[i]
											+ "-" + samResponseJson.rx_unit_deatil1[i] + "-" + samResponseJson.rx_unit_deatil2[i] + ";"
											+ "Duration:"
											+ samResponseJson.rx_duration[i] + "-" + samResponseJson.rx_duration_time[i]
								if(i<treatmentCount-1){
									tempStr = tempStr + "<br>"
								}						
							}
							panel.items.items[10].setValue(tempStr)
						}
						else{
							panel.items.items[10].setValue("")
						}
						
						
						win.insert(0, panel)
					}
				});
				// console.log(win)
			}
				
		}				
	}
});