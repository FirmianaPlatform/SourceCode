Ext.define('dataViewer.store.metadata.Modification', {
    extend: 'Ext.data.Store',

    proxy: {
        type: 'ajax',
        url: '/repos/display/Miape_Modification/',
        reader: {
            type: 'json',
            rootProperty: 'Miape_Modifications'
        }
    },
    fields: [{
        name: 'Miape_Modification',
        type: 'string'
    }],
    autoLoad: true

})