Ext.define('gar.view.Annotation',{ 
    extend: 'Ext.window.Window', 
    alias : 'widget.annotation',
    autoShow: true,
    initComponent : function(){ 
    		
    	
      Ext.apply(this,{ 
	    layout: 'fit',
	    id:'anno_filter_win',
	    title: 'Annotation Filter',
	    resizable :true,
	    closable: true,
	    height: 300,
	    width: 280,
	    draggable: {
            constrain: true,
            constrainTo: Ext.getBody()
        },
	    
	    items:[ 
	    {  
	    	xtype:'form',
	    	//url: '/gardener/data/showprotein/',
	    	height: 260,
	    	width: 300,
	    	bodyPadding: 10,
	    	border:false,
	    	//defaultType: 'textfield',
        
	    	items: [
	        {
	        	xtype : 'radiogroup',
	        	fieldLabel : 'Coreg',
	        	name : 'anno1', id : 'anno1', columns : 2, vertical : true,
	        	items : [
	        				{ boxLabel : 'Always', name : 'a1', inputValue : '1' },
	        				{ boxLabel : 'Never', name : 'a1', inputValue : '0' }
	        			]
	        },{
	        	xtype : 'radiogroup',
	        	fieldLabel : 'Kinase',
	        	name : 'anno2', id : 'anno2', columns : 2, vertical : true,
	        	items : [
	        				{ boxLabel : 'Always', name : 'a2', inputValue : '1' },
	        				{ boxLabel : 'Never', name : 'a2', inputValue : '0' }
	        			]		
	        },
	        {
	        	xtype : 'radiogroup',
	        	fieldLabel : 'Ligand',
	        	name : 'anno3', id : 'anno3', columns : 2, vertical : true,
	        	items : [
	        				{ boxLabel : 'Always', name : 'a3', inputValue : '1' },
	        				{ boxLabel : 'Never', name : 'a3', inputValue : '0' }
	        			]
	        },
	        {
	        	xtype : 'radiogroup',
	        	fieldLabel : 'Receptor',
	        	name : 'anno4', id : 'anno4', columns : 2, vertical : true,
	        	items : [
	        				{ boxLabel : 'Always', name : 'a4', inputValue : '1' },
	        				{ boxLabel : 'Never', name : 'a4', inputValue : '0' }
	        			]
	        },
	        {
	        	xtype : 'radiogroup',
	        	fieldLabel : 'PlasmaMembrane-mouse',
	        	name : 'anno5', id : 'anno5', columns : 2, vertical : true,
	        	items : [
	        				{ boxLabel : 'Always', name : 'a5', inputValue : '1' },
	        				{ boxLabel : 'Never', name : 'a5', inputValue : '0' }
	        			]
	        },
	        {
	        	xtype : 'radiogroup',
	        	fieldLabel : 'PlasmaMembrane-human',
	        	name : 'anno6', id : 'anno6', columns : 2, vertical : true,
	        	items : [
	        				{ boxLabel : 'Always', name : 'a6', inputValue : '1' },
	        				{ boxLabel : 'Never', name : 'a6', inputValue : '0' }
	        			]
	        },
	        {
	        	xtype : 'radiogroup',
	        	fieldLabel : 'Transcription Factor',
	        	name : 'anno7', id : 'anno7', columns : 2, vertical : true,
	        	items : [
	        				{ boxLabel : 'Always', name : 'a7', inputValue : '1' },
	        				{ boxLabel : 'Never', name : 'a7', inputValue : '0' }
	        			]
	        },
	        {
				xtype : 'hidden',
				name : 'stype',
				value : 'anno'
			} 
			],
	        buttons: [{
        		text: 'Reset',
        		handler: function() { this.up('form').getForm().reset(); }
    		}, {
        		text: 'Start',
        		formBind: true, //only enabled once the form is valid
        		handler: function() {
        			var form = this.up('form').getForm();
        			var a1 = form.findField('a1').getSubmitValue()
        			var a2 = form.findField('a2').getSubmitValue()
        			var a3 = form.findField('a3').getSubmitValue()
        			var a4 = form.findField('a4').getSubmitValue()
        			var a5 = form.findField('a5').getSubmitValue()
        			var a6 = form.findField('a6').getSubmitValue()
        			var a7 = form.findField('a7').getSubmitValue()
        			var annos = [a1,a2,a3,a4,a5,a6,a7]
        			console.log(annos)
        			var if_anno = Ext.getCmp('content-panel').getActiveTab().down('grid').getStore().getAt(0).data.annotation
                    if (!if_anno){Ext.Msg.alert('Failed','No annotation found') ;return 0}
                    var store = Ext.getCmp('content-panel').getActiveTab().down('grid').getStore();
                    store.load()
        		}
    		}]
	    }]
        }); 
        this.callParent(arguments); 
    } 
})

