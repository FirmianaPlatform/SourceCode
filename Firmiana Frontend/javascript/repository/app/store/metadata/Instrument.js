Ext.define('dataViewer.store.metadata.Instrument', {
    extend: 'Ext.data.Store',

    proxy: {
        type: 'ajax',
        url: '/repos/display/Miape_Instrument/',
        reader: {
            type: 'json',
            rootProperty: 'Miape_Instruments'
        }
    },
    fields: [{
        name: 'Miape_Instrument',
        type: 'string'
    }],
    autoLoad: true

})