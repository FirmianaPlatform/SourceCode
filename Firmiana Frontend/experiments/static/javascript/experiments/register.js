Ext.onReady(function(){
    Ext.tip.QuickTipManager.init();
    csrftoken = Ext.util.Cookies.get('csrftoken');
    var submitForm = function(){
        form = registerPanel.getForm();
        if (form.isValid()){
            form.submit({
                url: '/experiments/register/',
                standardSubmit: true
            })
        }
    };

    var resetForm = function(){
        form = registerPanel.getForm()
        form.reset()
    };


    Ext.apply(Ext.form.field.VTypes, {
        password: function(val, field){
            if(field.initialPassField){
                var pwd = field.up('form').down('#'+field.initialPassField);
                return (val==pwd.getValue());
            }
            return true;
        },

        passwordText: 'Passwrod do not match'
    });

    var registerPanel = Ext.create('Ext.form.FormPanel',{
        renderTo: 'register',
        title: 'Register Form',
        width: 300,
        frame: true,
        bodyStyle: {
            padding: '20px 10px'
        },
        defaults: {
            width: 200
        },
        labelWidth: 50,
        items:[{
            xtype: 'textfield',
            fieldLabel: 'Name',
            name: 'username'
        },{
            xtype: 'textfield',
            fieldLabel: 'Email',
            name: 'email',
            vtype: 'email'
        },{
            xtype: 'textfield',
            fieldLabel: 'Password',
            name: 'password1',
            inputType: 'password',
            itemId: 'password1'
        },{
            xtype: 'textfield',
            fieldLabel: 'Confirm Password',
            name: 'password2',
            inputType: 'password',
            vtype: 'password',
            initialPassField: 'password1'
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
