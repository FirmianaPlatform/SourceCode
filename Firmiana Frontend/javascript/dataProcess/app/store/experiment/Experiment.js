Ext.define('Admin.store.experiment.Experiment', {
    extend: 'Ext.data.Store',

    alias: 'store.experiment',

    model: 'Admin.model.experiment.Experiment',

    pageSize: 20,

    autoLoad: true,

    proxy: {
        type: 'ajax',
        url: '/ispec/metadata/',
        extraParams:{
            start: 1,
            limit: 30
        },
        reader: {
            type: 'json',
            rootProperty: 'data'
        }
    }
});