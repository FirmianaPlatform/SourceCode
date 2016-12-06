Ext.define('dataViewer.store.subaccount.SubAccount', {
    extend: 'Ext.data.Store',

    alias: 'store.subaccount',

    // pageSize: 20,

    autoLoad: true,

    fields: [
        {
            type: 'string',
            name: 'username'
        },
        {
            type: 'string',
            name: 'annotation'
        },
        {
            type: 'string',
            name: 'isActive'
        },
        {
            type: 'string',
            name: 'sharedProjectList'
        }
    ],

    proxy: {
        type: 'ajax',
        url: '/repos/showAllChildAccountInfoInProjectLevel//',
        reader: {
            type: 'json',
            rootProperty: 'data'
        }
    }
});