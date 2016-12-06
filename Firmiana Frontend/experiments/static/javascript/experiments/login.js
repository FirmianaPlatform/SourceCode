Ext.onReady(function(){
    Ext.tip.QuickTipManager.init();
    
    csrftoken = Ext.util.Cookies.get('csrftoken');
    var submitForm = function(){
        form = loginPanel.getForm();
        if (form.isValid()){
            form.submit({
                url: '/experiments/login/',
                standardSubmit: true
            })
        }
    };

    var resetForm = function(){
        form = loginPanel.getForm()
        form.reset()
    };

    var loginPanel = Ext.create('Ext.form.FormPanel',{
        renderTo: 'login',
        frame: true,
        title: 'Login',
        width: 300,
        bodyStyle: {
            padding: '10px 20px'
        },
        defaults: {
            width: 200
        },
        labelWidth: 50,
        items:[{
            xtype: 'textfield',
            fieldLabel: 'Username',
            name: 'username'
        },{
            xtype: 'textfield',
            fieldLabel: 'Password',
            name: 'password',
            inputType: 'password',
        },{
            xtype: 'hiddenfield',
            name: 'csrfmiddlewaretoken',
            value: csrftoken
        }],
        buttons: [
            {text: 'Submit', handler: submitForm},
            {text: 'Reset', handler: resetForm}
        ]
    });

})
