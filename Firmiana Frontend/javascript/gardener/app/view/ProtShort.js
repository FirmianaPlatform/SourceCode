Ext.define('gar.view.ProtShort', {
	extend : 'Ext.grid.Panel',
	alias : 'widget.protshort',
	border : false,
	viewConfig : {
		stripeRows : false
	},
	columnLines : true,
	loadMask : true,
	columns : [{
				text : 'Accession',
				sortable : false,
				dataIndex : 'accession'
			}, {
				text : 'Annotation',
				renderer : function(value, metaData, record, rowIndex,
						colIndex, store) {
					value = '      ';
					bkimg = "";
					bksz = "";
					bkpst = "";
					bkrp = "";
					pst = 0;
					{
						if (record.data.test1_1 > 0) {
							bkimg += ("url(/static/images/bkg_pink.png),")
						} else {
							bkimg += ("url(/static/images/bkg_gray.png),")
						}
						bksz += ("12% 100%,")
						bkpst += (pst.toString());
						pst += 15
						bkpst += ("% 0%,")
						bkrp += "no-repeat,"
					}
					{
						if (record.data.test1_2 > 0) {
							bkimg += ("url(/static/images/bkg_red.png),")
						} else {
							bkimg += ("url(/static/images/bkg_gray.png),")
						}
						bksz += ("12% 100%,")
						bkpst += (pst.toString());
						pst += 15
						bkpst += ("% 0%,")
						bkrp += "no-repeat,"
					}
					{
						if (record.data.test1_3 > 0) {
							bkimg += ("url(/static/images/bkg_yellow.png),")
						} else {
							bkimg += ("url(/static/images/bkg_gray.png),")
						}
						bksz += ("12% 100%,")
						bkpst += (pst.toString());
						pst += 15
						bkpst += ("% 0%,")
						bkrp += "no-repeat,"
					}
					{
						if (record.data.test1_4 > 0) {
							bkimg += ("url(/static/images/bkg_green.png),")
						} else {
							bkimg += ("url(/static/images/bkg_gray.png),")
						}
						bksz += ("12% 100%,")
						bkpst += (pst.toString());
						pst += 15
						bkpst += ("% 0%,")
						bkrp += "no-repeat,"
					}
					{
						if (record.data.test1_5 > 0) {
							bkimg += ("url(/static/images/bkg_blue.png),")
						} else {
							bkimg += ("url(/static/images/bkg_gray.png),")
						}
						bksz += ("12% 100%,")
						bkpst += (pst.toString());
						pst += 15
						bkpst += ("% 0%,")
						bkrp += "no-repeat,"
					}
					{
						if (record.data.test1_6 > 0) {
							bkimg += ("url(/static/images/bkg_violet.png),")
						} else {
							bkimg += ("url(/static/images/bkg_gray.png),")
						}
						bksz += ("12% 100%,")
						bkpst += (pst.toString());
						pst += 15
						bkpst += ("% 0%,")
						bkrp += "no-repeat,"
					}
					{
						if (record.data.test1_7 > 0) {
							bkimg += ("url(/static/images/bkg_brown.png),")
						} else {
							bkimg += ("url(/static/images/bkg_gray.png),")
						}
						bksz += ("12% 100%,")
						bkpst += (pst.toString());
						pst += 15
						bkpst += ("% 0%,")
						bkrp += "no-repeat,"
					}
					cssstring = '<div class="x-grid3-cell-inner" style="white-space: pre;';
					{
						cssstring += 'background-image:';
						cssstring += bkimg.substr(0, bkimg.length - 1) + ";";
						cssstring += 'background-size:';
						cssstring += bksz.substr(0, bksz.length - 1) + ";";
						cssstring += 'background-position:';
						cssstring += bkpst.substr(0, bkpst.length - 1) + ";";
						cssstring += 'background-repeat:';
						cssstring += bkrp.substr(0, bkrp.length - 1) + ";";

					}
					cssstring += '">'
					return cssstring + value + '</div>'
				},
				sortable : false
			}, {
				text : 'Relation',
				sortable : false,
				renderer : function(value, metaData, record, rowIndex,
						colIndex, store) {
					value = '      ';
					bkimg = "";
					bksz = "";
					bkpst = "";
					bkrp = "";
					pst = 0;
					{
						if (record.data.test2_1 > 0) {
							bkimg += ("url(/static/images/bkg_pink.png),")
						} else {
							bkimg += ("url(/static/images/bkg_gray.png),")
						}
						bksz += ("12% 100%,")
						bkpst += (pst.toString());
						pst += 15
						bkpst += ("% 0%,")
						bkrp += "no-repeat,"
					}
					{
						if (record.data.test2_2 > 0) {
							bkimg += ("url(/static/images/bkg_red.png),")
						} else {
							bkimg += ("url(/static/images/bkg_gray.png),")
						}
						bksz += ("12% 100%,")
						bkpst += (pst.toString());
						pst += 15
						bkpst += ("% 0%,")
						bkrp += "no-repeat,"
					}
					{
						if (record.data.test2_3 > 0) {
							bkimg += ("url(/static/images/bkg_yellow.png),")
						} else {
							bkimg += ("url(/static/images/bkg_gray.png),")
						}
						bksz += ("12% 100%,")
						bkpst += (pst.toString());
						pst += 15
						bkpst += ("% 0%,")
						bkrp += "no-repeat,"
					}
					{
						if (record.data.test2_4 > 0) {
							bkimg += ("url(/static/images/bkg_green.png),")
						} else {
							bkimg += ("url(/static/images/bkg_gray.png),")
						}
						bksz += ("12% 100%,")
						bkpst += (pst.toString());
						pst += 15
						bkpst += ("% 0%,")
						bkrp += "no-repeat,"
					}
					{
						if (record.data.test2_5 > 0) {
							bkimg += ("url(/static/images/bkg_blue.png),")
						} else {
							bkimg += ("url(/static/images/bkg_gray.png),")
						}
						bksz += ("12% 100%,")
						bkpst += (pst.toString());
						pst += 15
						bkpst += ("% 0%,")
						bkrp += "no-repeat,"
					}
					{
						if (record.data.test2_6 > 0) {
							bkimg += ("url(/static/images/bkg_violet.png),")
						} else {
							bkimg += ("url(/static/images/bkg_gray.png),")
						}
						bksz += ("12% 100%,")
						bkpst += (pst.toString());
						pst += 15
						bkpst += ("% 0%,")
						bkrp += "no-repeat,"
					}
					{
						if (record.data.test2_7 > 0) {
							bkimg += ("url(/static/images/bkg_brown.png),")
						} else {
							bkimg += ("url(/static/images/bkg_gray.png),")
						}
						bksz += ("12% 100%,")
						bkpst += (pst.toString());
						pst += 15
						bkpst += ("% 0%,")
						bkrp += "no-repeat,"
					}
					cssstring = '<div class="x-grid3-cell-inner" style="white-space: pre;';
					{
						cssstring += 'background-image:';
						cssstring += bkimg.substr(0, bkimg.length - 1) + ";";
						cssstring += 'background-size:';
						cssstring += bksz.substr(0, bksz.length - 1) + ";";
						cssstring += 'background-position:';
						cssstring += bkpst.substr(0, bkpst.length - 1) + ";";
						cssstring += 'background-repeat:';
						cssstring += bkrp.substr(0, bkrp.length - 1) + ";";

					}
					cssstring += '">'
					return cssstring + value + '</div>'
				}
			}, {
				text : 'Exp1',
				columns : [{
					text : 'R1',
					columns : [{
								text : 'iBAQs',
								dataIndex : 'e1_r1_i',
								width : 50,
								renderer : function(value, metadata) {
									metadata.tdAttr = 'data-qtip="' + value + '"';
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
									metadata.tdAttr = 'data-qtip="' + Math.pow(10, value) + '"';
									if (value > 0) {
										p = parseInt(255 - value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#ff" + k + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									} else {
										p = parseInt(255 + value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#" + k + "ff" + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									}
								}
							}]
				}, {
					text : 'R2',
					columns : [{
								text : 'iBAQs',
								width : 50,
								dataIndex : 'e1_r2_i',
								renderer : function(value, metadata) {
									metadata.tdAttr = 'data-qtip="' + value + '"';
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
								renderer : function(value,metadata) {
									metadata.tdAttr = 'data-qtip="' + Math.pow(10, value) + '"';
									if (value > 0) {
										p = parseInt(255 - value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#ff" + k + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									} else {
										p = parseInt(255 + value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#" + k + "ff" + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									}
								}
							}]
				}, {
					text : 'R3',
					columns : [{
								text : 'iBAQs',
								width : 50,
								dataIndex : 'e1_r3_i',
								renderer : function(value, metadata) {
									metadata.tdAttr = 'data-qtip="' + value + '"';
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
								renderer : function(value,metadata) {
									metadata.tdAttr = 'data-qtip="' + Math.pow(10, value) + '"';
									if (value > 0) {
										p = parseInt(255 - value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#ff" + k + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									} else {
										p = parseInt(255 + value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#" + k + "ff" + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									}
								}
							}]
				}]
			}, {
				text : 'Exp2',
				columns : [{
					text : 'R1',
					columns : [{
								text : 'iBAQs',
								width : 50,
								dataIndex : 'e2_r1_i',
								renderer : function(value, metadata) {
									metadata.tdAttr = 'data-qtip="' + value + '"';
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
								renderer : function(value,metadata) {
									metadata.tdAttr = 'data-qtip="' + Math.pow(10, value) + '"';
									if (value > 0) {
										p = parseInt(255 - value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#ff" + k + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									} else {
										p = parseInt(255 + value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#" + k + "ff" + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									}
								}
							}]
				}, {
					text : 'R2',
					columns : [{
								text : 'iBAQs',
								width : 50,
								dataIndex : 'e2_r2_i',
								renderer : function(value, metadata) {
									metadata.tdAttr = 'data-qtip="' + value + '"';
									return value
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
								renderer : function(value,metadata) {
									metadata.tdAttr = 'data-qtip="' + Math.pow(10, value) + '"';
									if (value > 0) {
										p = parseInt(255 - value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#ff" + k + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									} else {
										p = parseInt(255 + value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#" + k + "ff" + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									}
								}
							}]
				}, {
					text : 'R3',
					columns : [{
								text : 'iBAQs',
								width : 50,
								dataIndex : 'e2_r3_i',
								renderer : function(value, metadata) {
									metadata.tdAttr = 'data-qtip="' + value + '"';
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
								renderer : function(value,metadata) {
									metadata.tdAttr = 'data-qtip="' + Math.pow(10, value) + '"';
									if (value > 0) {
										p = parseInt(255 - value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#ff" + k + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									} else {
										p = parseInt(255 + value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#" + k + "ff" + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									}
								}
							}]
				}]
			}, {
				text : 'Exp3',
				columns : [{
					text : 'R1',
					columns : [{
								text : 'iBAQs',
								width : 50,
								dataIndex : 'e3_r1_i',
								renderer : function(value, metadata) {
									metadata.tdAttr = 'data-qtip="' + value + '"';
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
								renderer : function(value,metadata) {
									metadata.tdAttr = 'data-qtip="' + Math.pow(10, value) + '"';
									if (value > 0) {
										p = parseInt(255 - value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#ff" + k + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									} else {
										p = parseInt(255 + value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#" + k + "ff" + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									}
								}
							}]
				}, {
					text : 'R2',
					columns : [{
								text : 'iBAQs',
								width : 50,
								dataIndex : 'e3_r2_i',
								renderer : function(value, metadata) {
									metadata.tdAttr = 'data-qtip="' + value + '"';
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
								renderer : function(value,metadata) {
									metadata.tdAttr = 'data-qtip="' + Math.pow(10, value) + '"';
									if (value > 0) {
										p = parseInt(255 - value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#ff" + k + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									} else {
										p = parseInt(255 + value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#" + k + "ff" + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									}
								}
							}]
				}, {
					text : 'R3',
					columns : [{
								text : 'iBAQs',
								width : 50,
								dataIndex : 'e3_r3_i',
								renderer : function(value, metadata) {
									metadata.tdAttr = 'data-qtip="' + value + '"';
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
								renderer : function(value,metadata) {
									metadata.tdAttr = 'data-qtip="' + Math.pow(10, value) + '"';
									if (value > 0) {
										p = parseInt(255 - value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#ff" + k + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									} else {
										p = parseInt(255 + value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#" + k + "ff" + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									}
								}
							}]
				}]
			}, {
				text : 'Exp4',
				columns : [{
					text : 'R1',
					columns : [{
								text : 'iBAQs',
								width : 50,
								dataIndex : 'e4_r1_i',
								renderer : function(value, metadata) {
									metadata.tdAttr = 'data-qtip="' + value + '"';
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
								renderer : function(value,metadata) {
									metadata.tdAttr = 'data-qtip="' + Math.pow(10, value) + '"';
									if (value > 0) {
										p = parseInt(255 - value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#ff" + k + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									} else {
										p = parseInt(255 + value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#" + k + "ff" + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									}
								}
							}]
				}, {
					text : 'R2',
					columns : [{
								text : 'iBAQs',
								width : 50,
								dataIndex : 'e4_r2_i',
								renderer : function(value, metadata) {
									metadata.tdAttr = 'data-qtip="' + value + '"';
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
								renderer : function(value,metadata) {
									metadata.tdAttr = 'data-qtip="' + Math.pow(10, value) + '"';
									if (value > 0) {
										p = parseInt(255 - value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#ff" + k + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									} else {
										p = parseInt(255 + value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#" + k + "ff" + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									}
								}
							}]
				}, {
					text : 'R3',
					columns : [{
								text : 'iBAQs',
								width : 50,
								dataIndex : 'e4_r3_i',
								renderer : function(value, metadata) {
									metadata.tdAttr = 'data-qtip="' + value + '"';
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
								renderer : function(value,metadata) {
									metadata.tdAttr = 'data-qtip="' + Math.pow(10, value) + '"';
									if (value > 0) {
										p = parseInt(255 - value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#ff" + k + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									} else {
										p = parseInt(255 + value * 85);
										k = ("00" + p.toString(16)).substr(p
												.toString(16).length)
										s = "#" + k + "ff" + k
										return '<div class="x-grid3-cell-inner" style="background-color:'
												+ s
												+ ';">'
												+ Math.pow(10, value)
												+ '</div>'
									}
								}
							}]
				}]
			}]

})