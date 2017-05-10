Ext.define('Admin.model.experiment.Experiment', {
    extend: 'Admin.model.Base',

    fields: [
        {
            type: 'string',
            name: 'Exp_Number'
        },
        {
            type: 'string',
            name: 'FoundCountT'
        },
        {
            type: 'string',
            name: 'ExpType'
        },
        {
            type: 'string',
            name: 'Exp_date'
        },
        {
            type: 'string',
            name: 'Exp_experimenter'
        },
        {
            type: 'string',
            name: 'Cell_Tissue'
        },
        {
            type: 'string',
            name: 'Fraction'
        },
        {
            type: 'string',
            name: 'Genotype'
        },
        {
            type: 'string',
            name: 'Treatment'
        },
        {
            type: 'string',
            name: 'AffinityRecNumber'
        }
    ]
});