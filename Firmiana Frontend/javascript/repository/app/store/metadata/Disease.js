Ext.define('dataViewer.store.metadata.Disease', {
    extend: 'Ext.data.Store',

    proxy: {
        type: 'ajax',
        url: '/repos/display/Miape_Disease/',
        reader: {
            type: 'json',
            rootProperty: 'Miape_Diseases'
        }
    },
    fields: [{
        name: 'Miape_Disease',
        type: 'string'
    }],
    autoLoad: true

})