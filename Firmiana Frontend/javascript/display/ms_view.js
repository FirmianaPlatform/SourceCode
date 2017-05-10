Ext.onReady( function(){
    charge =parseInt( Ext.get('current_charge').getHTML())-1;
    var chargeImage = Ext.create('Ext.tab.Panel', {
        frame: true,
        activeTab: charge,
        renderTo: 'image_panel',
        minTabWidth: 100,
        plain: true,
        enableTabScroll: true,
        defaults: { autoScroll: true },
        items: [{
            title: '+1',
            contentEl: 'image_charge1',
        },{
            title: '+2',
            contentEl : 'image_charge2'
        },{
            title: '+3',
            contentEl : 'image_charge3'
        },{
            title: '+4',
            contentEl : 'image_charge4'
        },{
            title: '+5',
            contentEl : 'image_charge5'
        },{
            title: '+6',
            contentEl : 'image_charge6'
        },{
            title: '+7',
            contentEl : 'image_charge7'
        }],
        listeners: {
            'tabchange': function(tabPanel, newCard, oldCard){
                activeIndex = tabPanel.items.indexOf(newCard);
                chargeTab.setActiveTab(activeIndex);
            }
        }
    });

    var total = Ext.create('Ext.panel.Panel', {
        title: 'PeptideProphet analysis results',
        renderTo: 'total',
        contentEl: 'total_content',
        frame: true
    });

    var score = Ext.create('Ext.panel.Panel', {
        title: 'Scores',
        renderTo: 'score',
        contentEl: 'score_content',
        frame: true
    });

    // table_panel
    var chargeTab = Ext.create('Ext.tab.Panel', {
        frame: true,
        activeTab: charge,
        renderTo: 'table_panel',
        minTabWidth: 100,
        plain: true,
        enableTabScroll: true,
        defaults: { autoScroll: true },
        items: [{
            title: '+1',
            contentEl: 'table_charge1',
        },{
            title: '+2',
            contentEl : 'table_charge2'
        },{
            title: '+3',
            contentEl : 'table_charge3'
        },{
            title: '+4',
            contentEl : 'table_charge4'
        },{
            title: '+5',
            contentEl : 'table_charge5'
        },{
            title: '+6',
            contentEl : 'table_charge6'
        },{
            title: '+7',
            contentEl : 'table_charge7'
        },{
            title: 'All',
            contentEl : 'table_charge_all'
        }],
        listeners: {
            'tabchange': function(tabPanel, newCard, oldCard){
                activeIndex = tabPanel.items.indexOf(newCard);
                if (activeIndex <= 6){
                    chargeImage.setActiveTab(activeIndex);
                }
            }
        }
    });

});

