Ext.define('gar.view.KeggStatistic', {
			extend : 'Ext.grid.Panel',
			alias : 'widget.keggs',
			name : 'keggstatistic',
			autoscroll : true,
			rowLines : true,
			columnLines : true,
			loadMask : true,
			columns : [],
			viewConfig : {
				stripeRows : true,
				enableTextSelection : true
			}
		})
