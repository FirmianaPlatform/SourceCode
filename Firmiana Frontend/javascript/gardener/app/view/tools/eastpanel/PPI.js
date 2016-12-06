Ext.define('gar.view.tools.eastpanel.PPI', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.eastPPI',
    split: true,
    closable: false,
    title: 'PPI',
    layout: 'anchor',

    initComponent: function() {
        var store = Ext.create('Ext.data.Store', {
            fields: [{
                name: 'giName',
                type: 'string'
            }, {
                name: 'symbol',
                type: 'string',
            }, {
                name: 'region',
                type: 'string'
            }],
            sorter: [{
                property: 'region',
                direction: 'ASC'
            }]
        })

        this.items = [{
            xtype: 'grid',
            id: 'ppiPlotGrid',
            anchor: '100% 100%',
            store: store,
            columns: [{
                header: 'Accession',
                dataIndex: 'giName',
                flex: 1
            }, {
                header: 'Symbol',
                dataIndex: 'symbol',
                flex: 1
            }, {
                header: 'Region',
                dataIndex: 'region',
                flex: 1
            }]
        }];
        this.callParent(arguments);
    }
});
