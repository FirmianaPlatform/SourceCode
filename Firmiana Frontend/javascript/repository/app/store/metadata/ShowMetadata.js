Ext.define('dataViewer.store.metadata.ShowMetadata', {
    extend: 'Ext.data.Store',

    
    fields: [{
        name: 'affiliation',
        type: 'string'
    },{
        name: 'cellType',
        type: 'string'
    },{
        name: 'dataProtocol',
        type: 'string'
    },{
        name: 'disease',
        type: 'string'
    },{
        name: 'email',
        type: 'string'
    },{
        name: 'experimentType',
        type: 'string'
    },{
        name: 'instrument',
        type: 'string'
    },{
        name: 'keywords',
        type: 'string'
    },{
        name: 'linkToOther',
        type: 'string'
    },{
        name: 'modification',
        type: 'string'
    },{
        name: 'projectDescription',
        type: 'string'
    },{
        name: 'projectName',
        type: 'string'
    },{
        name: 'pubMedID',
        type: 'string'
    },{
        name: 'pxdNo',
        type: 'string'
    },{
        name: 'quantMethods',
        type: 'string'
    },{
        name: 'rePXaccession',
        type: 'string'
    },{
        name: 'sampleProtocol',
        type: 'string'
    },{
        name: 'species',
        type: 'string'
    },{
        name: 'tissue',
        type: 'string'
    }],
    autoLoad: true

})