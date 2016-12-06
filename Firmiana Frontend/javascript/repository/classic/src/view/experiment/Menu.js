Ext.define('dataViewer.view.experiment.Menu', {
    extend: 'Ext.menu.Menu',

    plain: true,
    defaults: { // defaults are applied to items, not the container
        handler: function(e){
            Ext.Ajax.request({
                url: '/repos/sharedProjectToChild/',
                params: {
                    childName: e.text,
                    sharedProject: project_pxdNo
                },
                method: 'GET',
                success: function(response) {
                    Ext.Msg.alert('Success', Ext.JSON.decode(response.responseText).msg);
                },
                failure: function(response) {
                    Ext.Msg.alert('Failure', Ext.JSON.decode(response.responseText).msg);
                }
            })
        }
    },
    /**
     * @method initComponent
     * @inheritdoc
     * @return {void}
     */
    initComponent: function() {
        
        this.items = []
        var me = this

        
        Ext.Ajax.request({
            url: '/repos/showAllChildAccountInfoInProjectLevel/',
            method: 'GET',
            success: function(response) {
                data = Ext.JSON.decode(response.responseText).data
                for(var i=0;i<data.length;i++){
                    me.add({text: data[i].username})
                }
            },
            failure: function(response) {
                
            }
        })
        this.callParent(arguments);
    },
})