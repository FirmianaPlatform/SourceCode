Ext.define('dataViewer.store.metadata.Species', {
    extend: 'Ext.data.Store',

    proxy: {
        type: 'ajax',
        url: '/repos/display/Miape_Species/',
        reader: {
            type: 'json',
            rootProperty: 'Miape_Speciess'
        }
    },
    fields: [{
        name: 'Miape_Species',
        type: 'string'
    }],
    autoLoad: true

})