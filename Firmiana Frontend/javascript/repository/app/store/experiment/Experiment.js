Ext.define('dataViewer.store.experiment.Experiment', {
    extend: 'Ext.data.Store',

    alias: 'store.experiment',

    model: 'dataViewer.model.experiment.Experiment',

    // pageSize: 20,

    autoLoad: true,

    proxy: {
        type: 'ajax',
        url: '/repos/showAllProjects/',
        reader: {
            type: 'json',
            rootProperty: 'data'
        }
    }
    // data : [
    //      {pxdno: '005217',   projectname: 'Tenascin-C promotes tumor angiogenesis through pro-angiogenic and anti-angiogenic effects involving YAP, Ephrin-B2 and CXCL12 signaling', species: 'Homo sapiens (Human) Mus musculus (Mouse)', status: 'Publicated'},
    //      {pxdno: '002971',   projectname: 'LC-MS/MS identification of Mycolactone protein targets', species: 'Homo sapiens (Human) ', status: 'Private'},
    //      {pxdno: '004866',   projectname: 'Desulfobacterium autotrophicum HRM2 shotgun analysis', species: 'Desulfobacterium autotrophicum HRM2 ', status: 'Publicated'},
    //      {pxdno: '000777',   projectname: 'C. thermocellum dHydG Acetate LC-MS/MS', species: 'Clostridium thermocellum (strain DSM 1313 / LMG 6656 / LQ8) ', status: 'Underreview'}
    //  ]
});