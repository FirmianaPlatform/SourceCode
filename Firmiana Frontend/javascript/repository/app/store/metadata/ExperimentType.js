Ext.define('dataViewer.store.metadata.ExperimentType', {
    extend: 'Ext.data.Store',

    proxy: {
        type: 'ajax',
        url: '/repos/display/Miape_ExpType/',
        reader: {
            type: 'json',
            rootProperty: 'Miape_ExpTypes'
        }
    },
    fields: [{
        name: 'Miape_ExpType',
        type: 'string'
    }],
    autoLoad: true

})