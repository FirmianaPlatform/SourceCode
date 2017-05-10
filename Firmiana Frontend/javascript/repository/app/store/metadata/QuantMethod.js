Ext.define('dataViewer.store.metadata.QuantMethod', {
    extend: 'Ext.data.Store',

    proxy: {
        type: 'ajax',
        url: '/repos/display/Miape_QuantMethod/',
        reader: {
            type: 'json',
            rootProperty: 'Miape_QuantMethods'
        }
    },
    fields: [{
        name: 'Miape_QuantMethod',
        type: 'string'
    }],
    autoLoad: true

})