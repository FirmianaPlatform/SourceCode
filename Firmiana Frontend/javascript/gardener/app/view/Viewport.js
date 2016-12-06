Ext.define('gar.view.Viewport',{ 
    extend: 'Ext.Viewport', 
    alias : 'widget.viewport',
    layout: 'fit', 
    hideBorders: true, 
    requires : [
        'gar.view.Menu', 
        'gar.view.TabPanel',
        'gar.view.Experiment',
        'gar.view.State'
    ]
}) 