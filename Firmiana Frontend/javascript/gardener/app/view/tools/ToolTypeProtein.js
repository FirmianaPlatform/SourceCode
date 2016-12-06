Ext.define('gar.view.tools.ToolTypeProtein',{
    extend: 'Ext.tree.Panel',
    alias: 'widget.tooltypeprotein',
    rootVisible: false,
    layout: 'fit',
    lines: false,
    useArrows: true,
    border: 0,

    initComponent: function() {

   		this.root = {
			expanded: true,
			children: [
			    {
			        text: 'Data Process',
			        expanded: true,
			        children: [
			        	{
			        		text: 'Density',
			        		leaf: true
			        	},
			        	{
			        		text: 'Distribution',
			        		leaf: true
			        	},
			        	{
			        		text: 'Correlation',
			        		leaf: true
			        	},
			        	{
			        		text: 'PCA',
			        		leaf: true
			        	},
			        	{
			        		text: 'MultiBoxplot',
			        		leaf: true
			        	}
			        ]
			    },
			    {
			        text: 'Data Analysis',
			        expanded: true,
			        children: [
			        	{
			        		text: 'Heatmap',
			        		leaf: true
			        	},
			        	{
			        		text: 'K-means Heatmap',
			        		leaf: true
			        	},
			        	{
			        		text: 'Volcano',
			        		leaf: true
			        	},
			        	{
			        		text: 'Venn',
			        		leaf: true
			        	}
			        ]
			    },
			    {
			        text: 'Data Mining',
			        expanded: true,
			        children: [
			        	{
			        		text: 'PPI',
			        		leaf: true
			        	},
			        	{
			        		text: 'GO Classification',
			        		leaf: true
			        	},
			        	{
			        		text: 'GO Enrich',
			        		leaf: true
			        	},
			        	{
			        		text: 'KEGG',
			        		leaf: true
			        	},
			        	{
			        		text: 'TF-TG',
			        		leaf: true
			        	},
			        	{
			        		text: 'Kinase/Substrate',
			        		leaf: true
			        	}
			        	// ,{
			        	// 	text: 'Test',
			        	// 	leaf: true
			        	// }
			        ]
			    }
			]
		}   	
    	this.callParent(arguments);
    }
});