Ext.define('gar.view.tools.toolsStatusBar',{
    extend: 'Ext.ux.statusbar.StatusBar',

    requires: [
    	
    ],

    alias: 'widget.toolsStatusBar',
    id: 'toolsStatusBar',
    defaultText: '',

    initComponent: function() {

        var val = this.val

     //    var startTime = function() {
     //        var today = new Date()
     //        var h = today.getHours()
     //        var m = today.getMinutes()
     //        var s = today.getSeconds()

     //        // add a zero in front of numbers<10
     //        m=checkTime(m)
     //        s=checkTime(s)

     //        Ext.getCmp('toolsStatusBar').setStatus({
     //            text: h+":"+m+":"+s
     //        });
     //        timeTask.delay(500)
     //    }
     //    var timeTask = new Ext.util.DelayedTask(startTime);

	    // timeTask.delay(500)

     //    var checkTime = function(i) {
     //        if (i<10) 
     //          {i="0" + i}
     //          return i
     //    }
    	this.callParent(arguments);
    }
});