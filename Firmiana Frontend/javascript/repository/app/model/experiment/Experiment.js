Ext.define('dataViewer.model.experiment.Experiment', {
	extend: 'Ext.data.Model',
    fields: [
        {
            type: 'string',
            name: 'pxdNo'
        },
        {
            type: 'string',
            name: 'projectName'
        },
        {
            type: 'string',
            name: 'species'
        },
        {
            type: 'string',
            name: 'status'
        }
    ]
});