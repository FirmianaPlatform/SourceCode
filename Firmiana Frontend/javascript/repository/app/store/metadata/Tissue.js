Ext.define('dataViewer.store.metadata.Tissue', {
    extend: 'Ext.data.Store',

    proxy: {
        type: 'ajax',
        url: '/repos/display/Miape_Tissue/',
        reader: {
            type: 'json',
            rootProperty: 'Miape_Tissues'
        }
    },
    fields: [{
        name: 'Miape_Tissue',
        type: 'string'
    }],
    autoLoad: true

})