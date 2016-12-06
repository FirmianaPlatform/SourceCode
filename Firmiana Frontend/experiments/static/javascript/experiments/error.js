Ext.onReady( function(){
    var error_message = Ext.get('error').dom.innerText;
    console.log(error_message);
    Ext.Msg.alert('Error', error_message);
});

