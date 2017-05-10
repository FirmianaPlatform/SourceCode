/**
 * This class is the main view for the application. It is specified in app.js as the
 * "mainView" property. That setting automatically applies the "viewport"
 * plugin causing this view to become the body element (i.e., the viewport).
 *
 * TODO - Replace this content of this view to suite the needs of your application.
 */
Ext.define('register.view.main.Main', {
    extend: 'Ext.tab.Panel',
    xtype: 'app-main',

    requires: [
        'Ext.plugin.Viewport',
        'Ext.window.MessageBox',

//        'register.view.main.MainController',
//        'register.view.main.MainModel',
        'register.view.main.Register',
        'register.view.main.ForgetPsd'
    ],

//    controller: 'main',
//    viewModel: 'main',

    ui: 'navigation',
    id: 'userManagement',
    tabBarHeaderPosition: 1,
    titleRotation: 0,
    tabRotation: 0,

    header: {
        layout: {
            align: 'stretchmax'
        },
        title: {
            text: 'USER MANAGEMENT',
            flex: 0
        },
        iconCls: 'fa-th-list'
    },

    tabBar: {
        flex: 1,
        layout: {
            align: 'stretch',
            overflowHandler: 'none'
        }
    },

    responsiveConfig: {
        tall: {
            headerPosition: 'top'
        },
        wide: {
            headerPosition: 'left'
        }
    },

    defaults: {
        bodyPadding: 20,
        tabConfig: {
            plugins: 'responsive',
            responsiveConfig: {
                wide: {
                    iconAlign: 'left',
                    textAlign: 'left'
                },
                tall: {
                    iconAlign: 'top',
                    textAlign: 'center',
                    width: 120
                }
            }
        }
    },
    
//    items:[{
//    	xtype:'register'
//    }]

    items: [{
        title: 'Register',
        iconCls: 'fa-user',
        items: [{
            xtype: 'register'
        }]
    }, {
        title: 'Forget password',
        iconCls: 'fa-cog',
        itemId: 'forgetPsd',
        items: [{
            xtype: 'forgetPsd'
        }]
//    }, {
//        title: 'Groups',
//        iconCls: 'fa-users',
//        html: '{loremIpsum}'
//    }, {
//        title: 'Settings',
//        iconCls: 'fa-cog',
//        html: 'User profile'
    }]
});
