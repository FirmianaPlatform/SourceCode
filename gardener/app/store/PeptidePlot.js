Ext.define('gar.store.PeptidePlot', {
			extend : 'Ext.data.Store',
			model : 'gar.model.PeptidePlot',
			proxy : {
				type : 'ajax',
				url : '/gardener/data/sum_pep_viewer/',
				reader : {
					type : 'json',
					root : 'data',
					totalProperty : 'total'
				}

			},
			getxlabel: function(){
				var label = []; 
				var count = this.getCount(); 
				var record; 
				for (var i = 0; i < count; i++) { 
					record = this.getAt(i); 
					if(label.indexOf(record.data.repeat_id)==-1){
						label.push(record.data.repeat_id)						
					}
				}
				label.sort(function(a, b) {
				    return a - b;
				});
				return label;
//				

			},
			getylabel: function(){
				var label = []; 
				var count = this.getCount(); 
				var record; 
				for (var i = 0; i < count; i++) { 
					record = this.getAt(i); 
					if(label.indexOf(record.data.fraction_id)==-1){
						label.push(record.data.fraction_id)						
					}
				}
				label.sort(function(a, b) {
				    return a - b;
				});
				return label;
//				

			}
		});
