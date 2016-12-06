Ext.onReady(function() {

    var nav = Ext.create('Ext.toolbar.Toolbar',{
        renderTo: 'nav',
        items: [
            {
                text:'Home',
                href:'/',
                hrefTarget: ''
            
            },'->',{
                text: 'Login',
                href: '/experiments/login/',
                hrefTarget: ''
            },{
                text: 'Register',
                href: '/experiments/register/',
                hrefTarget: ''
            }]
    });

});


