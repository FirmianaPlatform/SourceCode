Ext.define('dataViewer.view.metadata.MetadataController', {
    extend: 'Ext.app.ViewController',

    alias: 'controller.metadata',

    init: function() {
        // Ext.Ajax.request({
        //     timeout : 3600000,
        //     url : '/ispec/metadata/',
        //     method : 'GET',
        //     params : {
        //         start: 1,
        //         limit: 30
        //     },
        //     success : function(response) {
        //         var jsonObject = Ext.JSON.decode(response.responseText)
        //         console.log(jsonObject)
        //     },
        //     failure : function() {
        //         Ext.Msg.alert('Error!','An unknown error occured.')
        //     }
        // });
    }
});