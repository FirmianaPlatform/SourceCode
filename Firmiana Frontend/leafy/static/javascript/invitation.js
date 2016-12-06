Ext.onReady(function(){
    Ext.tip.QuickTipManager.init();
    csrftoken = Ext.util.Cookies.get('csrftoken');
    var submitForm = function(){
        form = invitationPanel.getForm();
        if (form.isValid()){
            form.submit({
                url: '/invite/',
                standardSubmit: true
            })
        }
    };

    var resetForm = function(){
        form = invitationPanel.getForm()
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

    var invitationPanel = Ext.create('Ext.form.FormPanel',{
        renderTo: 'invitation',
        title: 'User Invitation',
        width: 350,
        frame: true,
        bodyStyle: {
            padding: '20px 10px'
        },
        defaults: {
            width: 300
        },
        labelWidth: 50,
        items:[{
            xtype: 'textfield',
            fieldLabel: 'Name',
            name: 'name'
        },{
            xtype: 'textfield',
            fieldLabel: 'Email',
            name: 'email',
            vtype: 'email'
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
