Ext.define('dataViewer.store.metadata.CellType', {
    extend: 'Ext.data.Store',

    proxy: {
        type: 'ajax',
        url: '/repos/display/Miape_CellType/',
        reader: {
            type: 'json',
            rootProperty: 'Miape_CellTypes'
        }
    },
    fields: [{
        name: 'Miape_CellType',
        type: 'string'
    }],
    autoLoad: true
})