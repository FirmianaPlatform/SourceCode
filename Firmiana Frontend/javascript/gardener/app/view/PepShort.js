Ext.define('gar.view.PepShort', {
	extend : 'Ext.grid.Panel',
	alias : 'widget.pepshort',
	border : false,
	viewConfig : {
		stripeRows : false
	},
	columnLines : true,
	loadMask : true,
	columns : [{
				text : 'Sequeunce',
				width : 93,
				sortable : false,
				dataIndex : 'sequence'
			}, {
				text : 'PSM Num',
				sortable : false,
				dataIndex : 'num_psms'
			}, {
				text : 'Protein Num',
				sortable : false,
				dataIndex : 'num_proteins'
			}, // exp1
			// r1
			{
				text : 'iBAQs',
				width : 50,
				dataIndex : 'e1_r1_i',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					a = Math.random()
					if (a <= 0.3)
						return '<div class="x-grid3-cell-inner" style="background-color:lightblue;">'
								+ Ext.util.Format.round(value, 3) + '</div>'
					else
						return value

				}
			}, {
				text : 'Area',
				width : 50,
				dataIndex : 'e1_r1_a',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					return value
				}
			}, {
				text : 'Ratio',
				width : 50,
				dataIndex : 'e1_r1_p',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					if (value > 0) {
						p = parseInt(255 - value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#ff" + k + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					} else {
						p = parseInt(255 + value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#" + k + "ff" + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					}
				}
			},// r2
			{
				text : 'iBAQs',
				width : 50,
				dataIndex : 'e1_r2_i',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					a = Math.random()
					if (a <= 0.3)
						return '<div class="x-grid3-cell-inner" style="background-color:lightblue;">'
								+ Ext.util.Format.round(value, 3) + '</div>'
					else
						return value

				}
			}, {
				text : 'Area',
				width : 50,
				dataIndex : 'e1_r2_a',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					return value
				}
			}, {
				text : 'Ratio',
				width : 50,
				dataIndex : 'e1_r2_p',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					if (value > 0) {
						p = parseInt(255 - value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#ff" + k + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					} else {
						p = parseInt(255 + value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#" + k + "ff" + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					}
				}
			}// r3
			, {
				text : 'iBAQs',
				width : 50,
				dataIndex : 'e1_r3_i',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					a = Math.random()
					if (a <= 0.3)
						return '<div class="x-grid3-cell-inner" style="background-color:lightblue;">'
								+ Ext.util.Format.round(value, 3) + '</div>'
					else
						return value

				}
			}, {
				text : 'Area',
				width : 50,
				dataIndex : 'e1_r3_a',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					return value
				}
			}, {
				text : 'Ratio',
				width : 50,
				dataIndex : 'e1_r3_p',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					if (value > 0) {
						p = parseInt(255 - value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#ff" + k + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					} else {
						p = parseInt(255 + value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#" + k + "ff" + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					}
				}
			}
			// e2
			// r1
			, {
				text : 'iBAQs',
				width : 50,
				dataIndex : 'e2_r1_i',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					a = Math.random()
					if (a <= 0.3)
						return '<div class="x-grid3-cell-inner" style="background-color:lightblue;">'
								+ Ext.util.Format.round(value, 3) + '</div>'
					else
						return value

				}
			}, {
				text : 'Area',
				width : 50,
				dataIndex : 'e2_r1_a',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					return value
				}
			}, {
				text : 'Ratio',
				width : 50,
				dataIndex : 'e2_r1_p',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					if (value > 0) {
						p = parseInt(255 - value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#ff" + k + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					} else {
						p = parseInt(255 + value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#" + k + "ff" + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					}
				}
			}// r2
			, {
				text : 'iBAQs',
				width : 50,
				dataIndex : 'e2_r2_i',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					a = Math.random()
					if (a <= 0.1) {
						return '<div class="x-grid3-cell-inner" style="background-color:lightblue;">'
								+ Ext.util.Format.round(value, 3) + '</div>'
					} else
						return '<div class="x-grid3-cell-inner" style="width : 50,background-color:green;">'
								+ Ext.util.Format.round(value, 3) + '</div>'

				}
			}, {
				text : 'Area',
				width : 50,
				dataIndex : 'e2_r2_a',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					return value
				}
			}, {
				text : 'Ratio',
				width : 50,
				dataIndex : 'e2_r2_p',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					if (value > 0) {
						p = parseInt(255 - value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#ff" + k + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					} else {
						p = parseInt(255 + value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#" + k + "ff" + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					}
				}
			}// r3
			, {
				text : 'iBAQs',
				width : 50,
				dataIndex : 'e2_r3_i',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					a = Math.random()
					if (a <= 0.3)
						return '<div class="x-grid3-cell-inner" style="background-color:lightlightblue;">'
								+ Ext.util.Format.round(value, 3) + '</div>'
					else
						return value

				}
			}, {
				text : 'Area',
				width : 50,
				dataIndex : 'e2_r3_a',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					return value
				}
			}, {
				text : 'Ratio',
				width : 50,
				dataIndex : 'e2_r3_p',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					if (value > 0) {
						p = parseInt(255 - value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#ff" + k + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					} else {
						p = parseInt(255 + value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#" + k + "ff" + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					}
				}
			},// e3
			// r1
			{
				text : 'iBAQs',
				width : 50,
				dataIndex : 'e3_r1_i',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					a = Math.random()
					if (a <= 0.3)
						return '<div class="x-grid3-cell-inner" style="background-color:lightlightblue;">'
								+ Ext.util.Format.round(value, 3) + '</div>'
					else
						return value

				}
			}, {
				text : 'Area',
				width : 50,
				dataIndex : 'e3_r1_a',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					return value
				}
			}, {
				text : 'Ratio',
				width : 50,
				dataIndex : 'e3_r1_p',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					if (value > 0) {
						p = parseInt(255 - value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#ff" + k + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					} else {
						p = parseInt(255 + value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#" + k + "ff" + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					}
				}
			}// r2
			, {
				text : 'iBAQs',
				width : 50,
				dataIndex : 'e3_r2_i',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					a = Math.random()
					if (a <= 0.3)
						return '<div class="x-grid3-cell-inner" style="background-color:lightlightblue;">'
								+ Ext.util.Format.round(value, 3) + '</div>'
					else
						return value

				}
			}, {
				text : 'Area',
				width : 50,
				dataIndex : 'e3_r2_a',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					return value
				}
			}, {
				text : 'Ratio',
				width : 50,
				dataIndex : 'e3_r2_p',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					if (value > 0) {
						p = parseInt(255 - value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#ff" + k + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					} else {
						p = parseInt(255 + value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#" + k + "ff" + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					}
				}
			}// r3
			, {
				text : 'iBAQs',
				width : 50,
				dataIndex : 'e3_r3_i',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					a = Math.random()
					if (a <= 0.3)
						return '<div class="x-grid3-cell-inner" style="background-color:lightlightblue;">'
								+ Ext.util.Format.round(value, 3) + '</div>'
					else
						return value

				}
			}, {
				text : 'Area',
				width : 50,
				dataIndex : 'e3_r3_a',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					return value
				}
			}, {
				text : 'Ratio',
				width : 50,
				dataIndex : 'e3_r3_p',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					if (value > 0) {
						p = parseInt(255 - value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#ff" + k + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					} else {
						p = parseInt(255 + value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#" + k + "ff" + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					}
				}
			}// e4
			// r1
			, {
				text : 'iBAQs',
				width : 50,
				dataIndex : 'e4_r1_i',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					a = Math.random()
					if (a <= 0.3)
						return '<div class="x-grid3-cell-inner" style="background-color:lightlightblue;">'
								+ Ext.util.Format.round(value, 3) + '</div>'
					else
						return value

				}
			}, {
				text : 'Area',
				width : 50,
				dataIndex : 'e4_r1_a',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					return value
				}
			}, {
				text : 'Ratio',
				width : 50,
				dataIndex : 'e4_r1_p',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					if (value > 0) {
						p = parseInt(255 - value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#ff" + k + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					} else {
						p = parseInt(255 + value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#" + k + "ff" + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					}
				}
			}// r2
			, {
				text : 'iBAQs',
				width : 50,
				dataIndex : 'e4_r2_i',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					a = Math.random()
					if (a <= 0.3)
						return '<div class="x-grid3-cell-inner" style="background-color:lightlightblue;">'
								+ Ext.util.Format.round(value, 3) + '</div>'
					else
						return value

				}
			}, {
				text : 'Area',
				width : 50,
				dataIndex : 'e4_r2_a',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					return value
				}
			}, {
				text : 'Ratio',
				width : 50,
				dataIndex : 'e4_r2_p',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					if (value > 0) {
						p = parseInt(255 - value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#ff" + k + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					} else {
						p = parseInt(255 + value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#" + k + "ff" + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					}
				}
			}// r3
			, {
				text : 'iBAQs',
				width : 50,
				dataIndex : 'e4_r3_i',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					a = Math.random()
					if (a <= 0.3)
						return '<div class="x-grid3-cell-inner" style="background-color:lightblue;">'
								+ Ext.util.Format.round(value, 3) + '</div>'
					else
						return value

				}
			}, {
				text : 'Area',
				width : 50,
				dataIndex : 'e4_r3_a',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';
					return value
				}
			}, {
				text : 'Ratio',
				width : 50,
				dataIndex : 'e4_r3_p',
				renderer : function(value, metadata) {
					metadata.tdAttr = 'data-qtip="' + value + '"';

					if (value > 0) {
						p = parseInt(255 - value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#ff" + k + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					} else {
						p = parseInt(255 + value * 85);
						k = ("00" + p.toString(16))
								.substr(p.toString(16).length)
						s = "#" + k + "ff" + k
						return '<div class="x-grid3-cell-inner" style="background-color:'
								+ s + ';">' + Math.pow(10, value) + '</div>'
					}
				}
			}]

})