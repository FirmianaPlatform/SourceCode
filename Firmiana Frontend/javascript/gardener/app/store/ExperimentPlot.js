Ext.define('gar.store.ExperimentPlot', {
    extend: 'Ext.data.Store',
			model:'gar.model.ExperimentPlot',
			proxy : {
				type : 'memory',
				reader : {
					type : 'json'
				}
	
			},
			save: function(){
				var rowsData = []; 
				var count = this.getCount(); 
				var record; 
				for (var i = 0; i < count; i++) { 
					record = this.getAt(i); 
					rowsData.push(record.data); 
				} 
				Ext.getCmp('info_experiments_selected').setValue(Ext.encode(rowsData));			

			},
			getExp: function(){
				var exps = []; 
				var count = this.getCount(); 
				var record; 
				for (var i = 0; i < count; i++) { 
					record = this.getAt(i); 
					if(record.data.type=='exp'){
						exps.push(record.data.exp_id); 
					}
					
				} 
				return exps
			},
			getRepeat: function(){
				var repeats = []; 
				var count = this.getCount(); 
				var record; 
				var repeats;
				for (var i = 0; i < count; i++) { 
					record = this.getAt(i); 
					if(record.data.type=='repeat'){
						repeats.push(record.data.repeat_id+'_'+record.data.exp_id); 
					}
					
				} 
				return repeats
			}
				// This particular service cannot sort on more than one
				// field, so if grouped, disable sorting
			
});

