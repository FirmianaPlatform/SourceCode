Ext.define("view.monitor.realtimedata.RealtimePointGrid",{  
    extend:'Ext.grid.Panel',   
    alias:'widget.realtimepointgrid',  
    initComponent:function(){   
        var encode = false;  
        var local = true;  
        var filters = {  
            ftype: 'filters',  
            // encode and local configuration options defined previously for easier reuse  
            encode: encode, // json encode the filter query  
            local: local,   // defaults to false (remote filtering)  
      
            // Filters are most naturally placed in the column definition, but can also be  
            // added here.  
            filters: [  
                {  
                    type: 'boolean',  
                    dataIndex: 'visible'  
                }  
            ]  
        };  
          
        var realtimeInterval=null;   
        var store=Ext.create('Ext.data.Store',{  
            fields:['dotType','dotName','dotValue','alarmTime','alarmStatus','dataType','data','pointId','pointType']  
            //data:recArray  
        });  
        Ext.apply(this, {   
            store:store,  
            autoScroll:true,  
            features: [filters],  
            tbar:[   
                  {xtype:'button',text:'�鿴�豸����',name:'btDeviceFault', icon:iconPath+'wrench_orange.png'}  
                  ],  
            columns:[  
                     //new Ext.grid.RowNumberer({header:'���',width:50}),  
                     {xtype:'rownumberer',header:'���',width:40,renderer:function(value, cellmeta, record, rowIndex, columnIndex, store){  
                         return rowIndex+1;  
                         }},  
                     {text:'�������',width:200,sortable:true,dataIndex:'dotType', filterable: true},  
                     {text:'�������',width:200,sortable:true,dataIndex:'dotName',filter: {  
                        type: 'string'  
                        // specify disabled to disable the filter menu  
                        //, disabled: true  
                     }},  
                     {text:'���ֵ',width:150,sortable:true,dataIndex:'dotValue',renderer:function(value ,metaData ,record ){  
                         return value+record.data.dotUnit;  
                     }, filter: {  
                            type: 'numeric'  // specify type here or in store fields config  
                        }  
                     },  
                     {text:'�澯ʱ��',width:150,sortable:true,dataIndex:'alarmTime',    format: 'Y-m-d h:i:s'},  
                     {text:'״̬',width:200,sortable:true,dataIndex:'alarmStatus', filter: true},  
                     {  header:'����',  
                            xtype:'actioncolumn',  
                            width:100,  
                            items: [{  
                                icon: './resources/images/warn.png',  // Use a URL in the icon config  
                                tooltip: '�澯ȷ��',  
                                style: {marginRight:'100px'}  
                            },{  
                                icon: './resources/images/edit.gif',  // Use a URL in the icon config  
                                tooltip: '�澯��λ',  
                                style: {marginRight:'100px'}  
                            },{  
                                icon: './resources/images/emos.png',  // Use a URL in the icon config  
                                tooltip: '�澯�ɵ�',  
                                style: {marginRight:'100px'}  
                            }]}  
                     ],  
            listeners:{  
                destroy:function(){  
                    clearInterval(realtimeInterval);  
                },  
                afterrender:function(){  
                   
                    /** 
                     * ��ʱˢ��grid���� 
                     */  
                     var id=this.up().up().name;  
                     realtimeInterval=  setInterval(function() {   
                            store.loadData(filterPointArray(id,recArray));  
                            
                     },2000);  
                }  
            }  
        });  
        this.callParent(arguments);   
          
    }  
});  
   