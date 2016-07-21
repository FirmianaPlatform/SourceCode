Ext.define('gar.controller.ExperimentInfoLink_separationDetail', {
	extend : 'Ext.app.Controller',
	views : ['User'],
	init : function() {
		seprationDetailLink=function(expNo){
			var win = Ext.create('Ext.Window', {
				layout: {
					type: 'hbox',
					align: 'left'
				},
				autoScroll : true,
				resizable : true,
				title : 'Detailed Information of Separation',
				width : 700,
				height : 450,
				items : []
			});
			win.show();
			
			Ext.Ajax.request({
				url : '/experiments/loadnew/experiment/',
				params : {
					experiment_no : expNo
					// csrfmiddlewaretoken : csrftoken
				},
				success : function(response) {
					var panel = Ext.create('gar.view.Separation_detail');
					var text = response.responseText;
					sepResponseJson = Ext.JSON.decode(text).data;
						
					panel.items.items[0].setValue("Online")
					
					var showValue = ""
					for(var i=0;i<sepResponseJson.method_num;i++){
						showValue = showValue + "[" + (i+1) + "]: " 
									+ sepResponseJson.separationMethodList[i] + ";"
									+ sepResponseJson.separationSourceList[i] + ";"
									+ sepResponseJson.separationSizeList[i] + ";"
									+ sepResponseJson.separationBufferList[i] + ";"
									+ sepResponseJson.separationOthersList[i];
						if(i<sepResponseJson.method_num-1){
							showValue = showValue + "<br>";
						}
						
					}
					console.log(showValue)
					panel.items.items[1].setValue(showValue)
					//addSepration
						
					panel.items.items[2].setValue(sepResponseJson.separation_ajustments)
						
					win.insert(0, panel);
				}
			});
			
		}				
	}
});