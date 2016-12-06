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
                  {xtype:'button',text:'查看设备故障',name:'btDeviceFault', icon:iconPath+'wrench_orange.png'}  
                  ],  
            columns:[  
                     //new Ext.grid.RowNumberer({header:'编号',width:50}),  
                     {xtype:'rownumberer',header:'编号',width:40,renderer:function(value, cellmeta, record, rowIndex, columnIndex, store){  
                         return rowIndex+1;  
                         }},  
                     {text:'测点类型',width:200,sortable:true,dataIndex:'dotType', filterable: true},  
                     {text:'测点名称',width:200,sortable:true,dataIndex:'dotName',filter: {  
                        type: 'string'  
                        // specify disabled to disable the filter menu  
                        //, disabled: true  
                     }},  
                     {text:'监测值',width:150,sortable:true,dataIndex:'dotValue',renderer:function(value ,metaData ,record ){  
                         return value+record.data.dotUnit;  
                     }, filter: {  
                            type: 'numeric'  // specify type here or in store fields config  
                        }  
                     },  
                     {text:'告警时间',width:150,sortable:true,dataIndex:'alarmTime',    format: 'Y-m-d h:i:s'},  
                     {text:'状态',width:200,sortable:true,dataIndex:'alarmStatus', filter: true},  
                     {  header:'操作',  
                            xtype:'actioncolumn',  
                            width:100,  
                            items: [{  
                                icon: './resources/images/warn.png',  // Use a URL in the icon config  
                                tooltip: '告警确认',  
                                style: {marginRight:'100px'}  
                            },{  
                                icon: './resources/images/edit.gif',  // Use a URL in the icon config  
                                tooltip: '告警定位',  
                                style: {marginRight:'100px'}  
                            },{  
                                icon: './resources/images/emos.png',  // Use a URL in the icon config  
                                tooltip: '告警派单',  
                                style: {marginRight:'100px'}  
                            }]}  
                     ],  
            listeners:{  
                destroy:function(){  
                    clearInterval(realtimeInterval);  
                },  
                afterrender:function(){  
                   
                    /** 
                     * 定时刷新grid数据 
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
   