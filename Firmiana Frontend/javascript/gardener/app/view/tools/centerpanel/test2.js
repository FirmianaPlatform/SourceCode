Ext.define('gar.view.tools.centerpanel.test', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.Test',
    width: 600,
    split: true,
    floatable: false,
    closable: true,
    title: 'Test',
    layout:'border',

    /**
     * @requires 'gar.view.Notice'
     */
    requires: [
        'gar.view.Notice'
    ],
    
    initComponent: function() {
        
        Ext.tip.QuickTipManager.init();
        var timestamp = (new Date()).valueOf();  

        var plot = function() {
            $('#heatmap').heatmap(
                    {
                        data: {
                            values: new jheatmap.readers.TableHeatmapReader({ url: "/static/jheatmap/examples/enrichment/analysis-results.tsv"})
                        },

                        init: function (heatmap) {

                            // Setup default zoom
                            heatmap.cols.zoom = 12;
                            heatmap.rows.zoom = 12;

                            // Default cell value
                            heatmap.cells.selectedValue = "right-p-value";

                            // Configure decorators and aggregators
                            var decoratorPValue = new jheatmap.decorators.PValue();
                            var aggregatorPValue = new jheatmap.aggregators.PValue({});
                            $.each([
                                "left-p-value",
                                "right-p-value",
                                "two-tail-p-value",
                                "corrected-left-p-value",
                                "corrected-right-p-value",
                                "corrected-two-tail-p-value"], function (pos, value) {
                                heatmap.cells.decorators[value] = decoratorPValue;
                                heatmap.cells.aggregators[value] = aggregatorPValue;
                            });

                            // Add filters
                            heatmap.rows.filters.add(
                                    "Hide non-significant rows",
                                    new jheatmap.filters.NonSignificance(),
                                    [
                                        "right-p-value"
                                    ],
                                    [
                                        "left-p-value",
                                        "right-p-value",
                                        "two-tail-p-value",
                                        "corrected-left-p-value",
                                        "corrected-right-p-value",
                                        "corrected-two-tail-p-value"
                                    ]
                            );

                            // Sorting
                            heatmap.rows.sorter = new jheatmap.sorters.AggregationValueSorter("right-p-value");
                            heatmap.cols.sorter = new jheatmap.sorters.AggregationValueSorter("right-p-value");

                        }
                    }
            );
        };

        this.items = [{
            region:'north',
            xtype: 'toolbar',
            border: 0,
            items: ['->',{
                text: 'GO',
                handler: function() {
                    plot()
                }
            }]
        },{
            region:'center',
            xtype: 'panel',
            border: 0,
            id: 'PlotFrame'+timestamp,
            autoScroll:true,
            html: '<div id="heatmap"></div>'
        }]
        this.callParent(arguments);
    }
});
