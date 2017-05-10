Ext.define('gar.controller.Experiment', {
	extend : 'Ext.app.Controller',
	views : ['Experiment', 'Protein'],
	stores : ['Experiment'],
	models : ['Experiment', 'Search', 'Protein', 'Peptide'],
	init : function() {
		var store = Ext.create('gar.store.ExperimentPlot');

		checkBoxList = []
        checkBoxIDList = []

		ticPlot = function(type, record) {
			if (type == "cellclick") {
				var exp_store = Ext.create('gar.store.ExperimentPlot')

				type = 'exp'
				exp_id = record.data.id
				repeat_id = 1
				rank = 1

				// console.log(store)
				exp_store.add({
							id : type + '_' + exp_id + '_' + repeat_id + '_' + rank,
							exp_id : exp_id,
							repeat_id : repeat_id,
							rank : rank,
							name : record.data.name,
							type : type,
							num_fraction : record.data.num_fraction,
							num_repeat : record.data.num_repeat,
							num_spectrum : record.data.num_spectrum,
							num_peptide : record.data.num_peptide,
							num_isoform : record.data.num_isoform,
							num_gene : record.data.num_gene,
							stage : record.data.stage
						});
			} else {
				var data = (Ext.getCmp('info_experiments_selected').getValue()) ? Ext.decode(Ext.getCmp('info_experiments_selected').getValue()) : 0;
				var exp_store = Ext.create('gar.store.ExperimentPlot', {
							data : data
						})
			}
			// Ext.getCmp('info_experiments_selected').setValue(0)

			var count = exp_store.getCount();
			if (count === 0) {
				Ext.Msg.alert('TIC plot error:', 'Please select at least one experiment before plot.');
			} else {
				if (count > 1) {
					Ext.Msg.alert('TIC plot notice:', 'Mutiple batchs selected, only the firstone will be viewed.');
				}
				var record = exp_store.getAt(0);
				var tic_fraction_store = Ext.create('gar.store.TicFraction');
				tic_fraction_store.load({
							params : {
								exp_id : record.data.exp_id,
								repeat_id : record.data.repeat_id,
								rank : record.data.rank
							}
						});
				var tic_store = Ext.create('gar.store.Ms1_tic');
				tic_store.load({
							params : {
								exp_id : record.data.exp_id,
								repeat_id : record.data.repeat_id,
								rank : record.data.rank
							}
						});
				console.log(tic_store)
				var chart = Ext.create('Ext.chart.Chart', {
							enableMask : true,
							style : 'background:#fff',
							animate : true,
							store : tic_store,
							shadow : true,
							theme : 'Category1',
							mask : 'horizontal',
							legend : {
								position : 'right'
							},
							axes : [{
										type : 'Numeric',
										minimum : 0,
										position : 'left',
										fields : ['intensity'],
										title : 'TIC',
										minorTickSteps : 1,
										grid : {
											odd : {
												opacity : 1,
												fill : '#ddd',
												stroke : '#bbb',
												'stroke-width' : 0.5
											}
										},
										label : {
											renderer : function(v) {
												return v.toExponential(1);
											}
										}
									}, {
										type : 'Numeric',
										position : 'bottom',
										fields : ['rt'],
										title : 'Retention Time(second)'
									}],
							series : [{
										type : 'line',
										highlight : {
											size : 4,
											radius : 3
										},
										axis : 'left',
										fill : true,
										xField : 'rt',
										yField : 'intensity',
										markerConfig : {
											type : 'circle',
											size : 2,
											radius : 2,
											'stroke-width' : 0
										}
									}],
							listeners : {
								select : {
									fn : function(me, selection) {
										me.setZoom(selection);
										me.mask.hide();
									}
								},
								dblclick : {
									fn : function(me, clickresion) {
										chart.restoreZoom();
									}
								}
							}
						});
				var fraction_comb = Ext.create('Ext.form.field.ComboBox', {
							fieldLabel : 'Choose Fraction',
							store : tic_fraction_store,
							queryMode : 'local',
							displayField : 'fraction',
							valueField : 'search_id',
							forceSelection : true,
							listeners : {
								'select' : function(combo, record, eOpts) {
									tic_store.reload({
												params : {
													search_id : record[0].data.search_id
												}
											});
									chart.restoreZoom();
									chart.redraw()
								}
							}
						})
				fraction_comb.store.on("load", function(store) {
							fraction_comb.setValue(fraction_comb.store.getAt(0).get('search_id'));
						}, this);
				var win = Ext.create('Ext.Window', {
							draggable : {
								constrain : true,
								constrainTo : Ext.getBody()
							},
							width : 1000,
							height : 600,
							minHeight : 200,
							minWidth : 200,
							hidden : false,
							maximizable : true,
							title : 'TIC Chart',
							// animateTarget: 'metic',
							// renderTo : Ext.getBody(),
							layout : 'fit',
							dockedItems : [{
								xtype : 'toolbar',
								dock : 'top',
								items : [{
									xtype : 'button',
									text : 'Save Chart',
									handler : function() {
										Ext.MessageBox.confirm('Confirm Download', 'Would you like to download the chart as an image?', function(
														choice) {
													if (choice == 'yes') {
														chart.save({
																	type : 'image/png'
																});
													}
												});
									}
								}, '|', fraction_comb]
							}],
							items : chart
						});
				win.show()
			}
		}

		var ucsc_plot = function(dbcell, td, cell, record, tr, row, e) {
			a = Ext.getElementById(td.id).classList[2].toString().substring(12)
			if (Ext.getElementById(a + '-textEl').textContent == "Accession" && cell > 0) {
				// var exploadMask = new Ext.LoadMask(this.up(), {
				// msg : 'Loading.....'
				// });
				// exploadMask.show()
				Ext.Ajax.request({
							url : '/gardener/genome/',
							params : {
								experiment_no : record.data.exp_name,
								gi : record.data.accession
							},
							timeout : 600000,
							success : function(response) {
								exploadMask.hide();
								var text = response.responseText;
								file = Ext.JSON.decode(text).file;
								species = Ext.JSON.decode(text).species;
								chr = Ext.JSON.decode(text).chr;
								c = Ext.getCmp('content-panel')
								tempStr = Ext.String.format(
										"https://genome.ucsc.edu/cgi-bin/hgTracks?org={0}&hgt.customText=http://firmiana.org{1}&position={2}",
										species, file, chr)
								Ext.getCmp('info_tab_index').value += 1
								c.add({
									title : 'UCSC Browser',
									// iconCls : 'tabs',
									closable : true,
									// id : 'tab_ucsc',
									// Ext.getCmp('info_tab_index').value,
									layout : 'fit',
									html : '<iframe name="spview" id="spview" width="100%" height="100%" frameborder=0 src="' + tempStr
											+ '"></iframe>'
								}).show()
							},
							failure : function() {
								exploadMask.hide();
							}
						});
				/*
				 * var win_ucsc = Ext.create('Ext.Window', { width : 1000, //
				 * height : 735, height : 600, minHeight : 400, minWidth : 550,
				 * hidden : false, maximizable : true, title : 'UCSC Viewer',
				 * //renderTo : Ext.getBody(), layout : 'fit', // html : '<iframe
				 * name="spview" id="spview" width="100%" // height="100%"
				 * frameborder=0 //
				 * src="https://genome.ucsc.edu/cgi-bin/hgTracks"></iframe>'
				 * html : '<iframe name="spview" id="spview" width="100%"
				 * height="100%" frameborder=0
				 * src="http://firmiana.org:8000/cgi-bin/hgGateway"></iframe>'
				 * 
				 * }); //Ext.WindowManager.register(win_ucsc);
				 * //Ext.WindowManager.bringToFront('win_ucsc');
				 */
			}
			/*
			 * else if (Ext.getElementById(a + '-textEl').textContent ==
			 * "Annotation" && cell > 0){ { //console.log("click annotation");
			 * var a0 = e.getTarget('.annotation_0'); var a1 =
			 * e.getTarget('.annotation_1'); var a2 =
			 * e.getTarget('.annotation_2'); if (a0) { console.log("click
			 * anno1"); } if (a1){ console.log("click anno2"); } if (a2){
			 * console.log("click anno3"); } } }
			 */
		}
		peptide_sum_plot = function(dbcell, td, cell, record, tr, row, e) {
			a = Ext.getElementById(td.id).classList[2].toString().substring(12)
			if (Ext.getElementById(a + '-textEl').textContent == "PSMs" && cell > 0) {
				var waitWin = new Ext.Window({
							draggable : {
								constrain : true,
								constrainTo : Ext.getBody()
							},
							title : 'Waiting for a while',
							height : 100,
							width : 250
						})
				waitWin.show()
				cellrecord = record
				var peptide_plot_store = Ext.create('gar.store.PeptidePlot');
				peptide_plot_store.load({
							params : {
								search_id : record.data.search_id,
								pep_sequence : record.data.sequence,
								modification : record.data.modification
							}
						});
				// Ext.Msg.alert('Experiment
				// Info:'+xlabel.length,
				// ylabel.length);
				// Ext.Msg.alert('Experiment
				// Info:'+xlabel,
				// ylabel);
				var rank_store = Ext.create('gar.store.TicRank');
				rank_store.load({
							params : {
								search_id : record.data.search_id
							}
						});
				var pieChart = Ext.create('Ext.chart.Chart', {
							width : 200,
							height : 100,
							xtype : 'chart',
							style : 'background:#fff',
							animate : true,
							store : peptide_plot_store,
							shadow : true,
							theme : 'Category1',
							legend : {
								position : 'right'
							},
							axes : [{
										type : 'Numeric',
										minimum : 0,
										position : 'left',
										fields : ['fraction_id'],
										minorTickSteps : 1,
										grid : {
											odd : {
												opacity : 1,
												fill : '#ddd',
												stroke : '#bbb',
												'stroke-width' : 0.5
											}
										}
									}],
							series : [{
										type : 'line',
										highlight : {
											size : 7,
											radius : 7
										},
										axis : 'left',
										xField : 'fraction_id',
										yField : 'repeat_id',
										markerConfig : {
											type : 'cross',
											size : 4,
											radius : 4,
											'stroke-width' : 0
										}
									}]
						});
				var grid = Ext.create('Ext.grid.Panel', {
							store : peptide_plot_store,
							height : 130,
							width : 280,
							columns : [{
										text : 'xplot',
										dataIndex : 'xplot'
									}, {
										text : 'yplot',
										dataIndex : 'yplot'
									}]
						});
				var Renderers = {};
				(function() {
					var ColorManager = {
						rgbToHsv : function(rgb) {
							var r = rgb[0] / 255, g = rgb[1] / 255, b = rgb[2] / 255, rd = Math.round, minVal = Math.min(r, g, b), maxVal = Math.max(
									r, g, b), delta = maxVal - minVal, h = 0, s = 0, v = 0, deltaRgb;
							v = maxVal;
							if (delta == 0) {
								return [0, 0, v];
							} else {
								s = delta / maxVal;
								deltaRgb = {
									r : (((maxVal - r) / 6) + (delta / 2)) / delta,
									g : (((maxVal - g) / 6) + (delta / 2)) / delta,
									b : (((maxVal - b) / 6) + (delta / 2)) / delta
								};
								if (r == maxVal) {
									h = deltaRgb.b - deltaRgb.g;
								} else if (g == maxVal) {
									h = (1 / 3) + deltaRgb.r - deltaRgb.b;
								} else if (b == maxVal) {
									h = (2 / 3) + deltaRgb.g - deltaRgb.r;
								}
								// handle
								// edge
								// cases
								// for
								// hue
								if (h < 0) {
									h += 1;
								}
								if (h > 1) {
									h -= 1;
								}
							}
							h = rd(h * 360);
							s = rd(s * 100);
							v = rd(v * 100);
							return [h, s, v];
						},
						hsvToRgb : function(hsv) {
							var h = hsv[0] / 360, s = hsv[1] / 100, v = hsv[2] / 100, r, g, b, rd = Math.round;
							if (s == 0) {
								v *= 255;
								return [v, v, v];
							} else {
								var vh = h * 6, vi = vh >> 0, v1 = v * (1 - s), v2 = v * (1 - s * (vh - vi)), v3 = v * (1 - s * (1 - (vh - vi)));
								switch (vi) {
									case 0 :
										r = v;
										g = v3;
										b = v1;
										break;
									case 1 :
										r = v2;
										g = v;
										b = v1;
										break;
									case 2 :
										r = v1;
										g = v;
										b = v3;
										break;
									case 3 :
										r = v1;
										g = v2;
										b = v;
										break;
									case 4 :
										r = v3;
										g = v1;
										b = v;
										break;
									default :
										r = v;
										g = v1;
										b = v2;
								}
								return [rd(r * 255), rd(g * 255), rd(b * 255)];
							}
						}
					};
					// Generic
					// number
					// interpolator
					var delta = function(x, y, a, b, theta) {
						return a + (b - a) * (y - theta) / (y - x);
					};
					// Add
					// renderer
					// methods.
					Ext.apply(Renderers, {
						color : function(fieldName, minColor, maxColor, minValue, maxValue) {
							var re = /rgb\s*\(\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*\)\s*/, minColorMatch = minColor.match(re), maxColorMatch = maxColor
									.match(re), interpolate = function(theta) {
								return [delta(minValue, maxValue, minColor[0], maxColor[0], theta),
										delta(minValue, maxValue, minColor[1], maxColor[1], theta),
										delta(minValue, maxValue, minColor[2], maxColor[2], theta)];
							};
							minColor = ColorManager.rgbToHsv([+minColorMatch[1], +minColorMatch[2], +minColorMatch[3]]);
							maxColor = ColorManager.rgbToHsv([+maxColorMatch[1], +maxColorMatch[2], +maxColorMatch[3]]);
							// Return
							// the
							// renderer
							return function(sprite, record, attr, index, store) {
								var value = +record.get(fieldName), rgb = ColorManager.hsvToRgb(interpolate(value)), rgbString = 'rgb(' + rgb[0]
										+ ', ' + rgb[1] + ', ' + rgb[2] + ')';
								return Ext.apply(attr, {
											fill : rgbString
										});
							};
						},
						grayscale : function(fieldName, minColor, maxColor, minValue, maxValue) {
							var re = /rgb\s*\(\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*\)\s*/, minColorMatch = minColor.match(re), maxColorMatch = maxColor
									.match(re), interpolate = function(theta) {
								var ans = delta(minValue, maxValue, +minColorMatch[1], +maxColorMatch[1], theta) >> 0;
								return [ans, ans, ans];
							};
							// Return
							// the
							// renderer
							return function(sprite, record, attr, index, store) {
								var value = +record.get(fieldName), rgb = interpolate(value), rgbString = 'rgb(' + rgb[0] + ', ' + rgb[1] + ', '
										+ rgb[2] + ')';
								return Ext.apply(attr, {
											fill : rgbString,
											strokeFill : 'rgb(0, 0, 0)'
										});
							};
						},
						radius : function(fieldName, minRadius, maxRadius, minValue, maxValue) {
							var interpolate = function(theta) {
								return delta(minValue, maxValue, minRadius, maxRadius, theta);
							};
							// Return
							// the
							// renderer
							return function(sprite, record, attr, index, store) {
								var value = +record.get(fieldName), radius = interpolate(value);
								return Ext.apply(attr, {
											radius : radius,
											size : radius
										});
							};
						}
					});
				})();
				// current
				// renderer
				// configuration
				var rendererConfiguration = {
					xField : 'xplot',
					yField : 'yplot',
					color : false,
					colorFrom : 'rgb(250, 20, 20)',
					colorTo : 'rgb(127, 0, 240)',
					scale : false,
					scaleFrom : 'rgb(20, 20, 20)',
					scaleTo : 'rgb(220, 220, 220)',
					radius : false,
					radiusSize : 50
				};
				// update
				// the
				// visualization
				// with
				// the
				// new
				// renderer
				// configuration
				function refresh() {
					var chart = Ext.getCmp('chartCmp'), series = chart.series.items, len = series.length, rc = rendererConfiguration, color, grayscale, radius, s;
					for (var i = 0; i < len; i++) {
						s = series[i];
						s.xField = rc.xField;
						s.yField = rc.yField;
						color = rc.color ? Renderers.color(rc.color, rc.colorFrom, rc.colorTo, 0, 1) : function(a, b, attr) {
							return attr;
						};
						grayscale = rc.grayscale ? Renderers.grayscale(rc.grayscale, rc.scaleFrom, rc.scaleTo, 0, 1) : function(a, b, attr) {
							return attr;
						};
						radius = rc.radius ? Renderers.radius(rc.radius, 10, rc.radiusSize, 0, 1) : function(a, b, attr) {
							return attr;
						};
						s.renderer = function(sprite, record, attr, index, store) {
							return radius(sprite, record, grayscale(sprite, record, color(sprite, record, attr, index, store), index, store), index,
									store);
						};
					}
					chart.redraw();
				}
				// form
				// selection
				// callbacks/handlers.
				var xAxisHandler = function(elem) {
					var xField = elem.text;
					rendererConfiguration.xField = xField;
					refresh();
				};
				var yAxisHandler = function(elem) {
					var yField = elem.text;
					rendererConfiguration.yField = yField;
					refresh();
				};
				var colorVariableHandler = function(elem) {
					var color = elem.text;
					rendererConfiguration.color = color;
					rendererConfiguration.grayscale = false;
					refresh();
				};
				var grayscaleVariableHandler = function(elem) {
					var color = elem.text;
					rendererConfiguration.grayscale = color;
					rendererConfiguration.color = false;
					refresh();
				};
				var scaleFromHandler = function(elem) {
					var from = elem.text;
					rendererConfiguration.scaleFrom = from;
					refresh();
				};
				var scaleToHandler = function(elem) {
					var to = elem.text;
					rendererConfiguration.scaleTo = to;
					refresh();
				};
				var colorFromHandler = function(elem) {
					var from = elem.text;
					rendererConfiguration.colorFrom = from;
					refresh();
				};
				var colorToHandler = function(elem) {
					var to = elem.text;
					rendererConfiguration.colorTo = to;
					refresh();
				};
				var radiusHandler = function(elem) {
					var radius = elem.text;
					rendererConfiguration.radius = radius;
					refresh();
				};
				var radiusSizeHandler = function(elem) {
					var radius = elem.text;
					rendererConfiguration.radiusSize = parseInt(radius, 10);
					refresh();
				};
				var xAxisMenu = Ext.create('Ext.menu.Menu', {
							id : 'xAxisMenu',
							items : [{
										text : 'xplot',
										handler : xAxisHandler,
										checked : true,
										group : 'x'
									}, {
										text : 'yplot',
										handler : xAxisHandler,
										checked : false,
										group : 'x'
									}, {
										text : 'area',
										handler : xAxisHandler,
										checked : false,
										group : 'x'
									}]
						});
				var yAxisMenu = Ext.create('Ext.menu.Menu', {
							id : 'yAxisMenu',
							items : [{
										text : 'xplot',
										handler : yAxisHandler,
										checked : false,
										group : 'y'
									}, {
										text : 'yplot',
										handler : yAxisHandler,
										checked : true,
										group : 'y'
									}, {
										text : 'area',
										handler : yAxisHandler,
										checked : false,
										group : 'y'
									}]
						});
				var colorMenu = Ext.create('Ext.menu.Menu', {
							id : 'colorMenu',
							items : [{
										text : 'xplot',
										handler : colorVariableHandler,
										checked : true,
										group : 'color'
									}, {
										text : 'yplot',
										handler : colorVariableHandler,
										checked : false,
										group : 'color'
									}, {
										text : 'area',
										handler : colorVariableHandler,
										checked : false,
										group : 'color'
									}, {
										text : 'Color From',
										menu : {
											items : [{
														text : 'rgb(250, 20, 20)',
														handler : colorToHandler,
														checked : true,
														group : 'colorrange'
													}, {
														text : 'rgb(20, 250, 20)',
														handler : colorToHandler,
														checked : false,
														group : 'colorrange'
													}, {
														text : 'rgb(20, 20, 250)',
														handler : colorToHandler,
														checked : false,
														group : 'colorrange'
													}, {
														text : 'rgb(127, 0, 240)',
														handler : colorFromHandler,
														checked : false,
														group : 'colorrange'
													}, {
														text : 'rgb(213, 70, 121)',
														handler : colorToHandler,
														checked : false,
														group : 'colorrange'
													}, {
														text : 'rgb(44, 153, 201)',
														handler : colorFromHandler,
														checked : false,
														group : 'colorrange'
													}, {
														text : 'rgb(146, 6, 157)',
														handler : colorFromHandler,
														checked : false,
														group : 'colorrange'
													}, {
														text : 'rgb(49, 149, 0)',
														handler : colorFromHandler,
														checked : false,
														group : 'colorrange'
													}, {
														text : 'rgb(249, 153, 0)',
														handler : colorFromHandler,
														checked : false,
														group : 'colorrange'
													}]
										}
									}, {
										text : 'Color To',
										menu : {
											items : [{
														text : 'rgb(250, 20, 20)',
														handler : colorToHandler,
														checked : false,
														group : 'tocolorrange'
													}, {
														text : 'rgb(20, 250, 20)',
														handler : colorToHandler,
														checked : false,
														group : 'tocolorrange'
													}, {
														text : 'rgb(20, 20, 250)',
														handler : colorToHandler,
														checked : false,
														group : 'tocolorrange'
													}, {
														text : 'rgb(127, 0, 220)',
														handler : colorFromHandler,
														checked : true,
														group : 'tocolorrange'
													}, {
														text : 'rgb(213, 70, 121)',
														handler : colorToHandler,
														checked : false,
														group : 'tocolorrange'
													}, {
														text : 'rgb(44, 153, 201)',
														handler : colorToHandler,
														checked : false,
														group : 'tocolorrange'
													}, {
														text : 'rgb(146, 6, 157)',
														handler : colorToHandler,
														checked : false,
														group : 'tocolorrange'
													}, {
														text : 'rgb(49, 149, 0)',
														handler : colorToHandler,
														checked : false,
														group : 'tocolorrange'
													}, {
														text : 'rgb(249, 153, 0)',
														handler : colorToHandler,
														checked : false,
														group : 'tocolorrange'
													}]
										}
									}]
						});
				var grayscaleMenu = Ext.create('Ext.menu.Menu', {
							id : 'grayscaleMenu',
							items : [{
										text : 'xplot',
										handler : grayscaleVariableHandler,
										checked : false,
										group : 'gs'
									}, {
										text : 'yplot',
										handler : grayscaleVariableHandler,
										checked : false,
										group : 'gs'
									}, {
										text : 'area',
										handler : grayscaleVariableHandler,
										checked : false,
										group : 'gs'
									}, {
										text : 'Scale From',
										menu : {
											items : [{
														text : 'rgb(20, 20, 20)',
														handler : scaleFromHandler,
														checked : true,
														group : 'gsrange'
													}, {
														text : 'rgb(80, 80, 80)',
														handler : scaleFromHandler,
														checked : false,
														group : 'gsrange'
													}, {
														text : 'rgb(120, 120, 120)',
														handler : scaleFromHandler,
														checked : false,
														group : 'gsrange'
													}, {
														text : 'rgb(180, 180, 180)',
														handler : scaleFromHandler,
														checked : false,
														group : 'gsrange'
													}, {
														text : 'rgb(220, 220, 220)',
														handler : scaleFromHandler,
														checked : false,
														group : 'gsrange'
													}, {
														text : 'rgb(250, 250, 250)',
														handler : scaleFromHandler,
														checked : false,
														group : 'gsrange'
													}]
										}
									}, {
										text : 'Scale To',
										menu : {
											items : [{
														text : 'rgb(20, 20, 20)',
														handler : scaleToHandler,
														checked : false,
														group : 'togsrange'
													}, {
														text : 'rgb(80, 80, 80)',
														handler : scaleToHandler,
														checked : false,
														group : 'togsrange'
													}, {
														text : 'rgb(120, 120, 120)',
														handler : scaleToHandler,
														checked : false,
														group : 'togsrange'
													}, {
														text : 'rgb(180, 180, 180)',
														handler : scaleToHandler,
														checked : false,
														group : 'togsrange'
													}, {
														text : 'rgb(220, 220, 220)',
														handler : scaleToHandler,
														checked : true,
														group : 'togsrange'
													}, {
														text : 'rgb(250, 250, 250)',
														handler : scaleToHandler,
														checked : false,
														group : 'togsrange'
													}]
										}
									}]
						});
				var radiusMenu = Ext.create('Ext.menu.Menu', {
							id : 'radiusMenu',
							style : {
								overflow : 'visible' // For
								// the
								// Combo
								// popup
							},
							items : [{
										text : 'xplot',
										handler : radiusHandler,
										checked : true,
										group : 'radius'
									}, {
										text : 'yplot',
										handler : radiusHandler,
										checked : false,
										group : 'radius'
									}, {
										text : 'area',
										handler : radiusHandler,
										checked : false,
										group : 'radius'
									}, {
										text : 'Max Radius',
										menu : {
											items : [{
														text : '20',
														handler : radiusSizeHandler,
														checked : false,
														group : 'sradius'
													}, {
														text : '30',
														handler : radiusSizeHandler,
														checked : false,
														group : 'sradius'
													}, {
														text : '40',
														handler : radiusSizeHandler,
														checked : false,
														group : 'sradius'
													}, {
														text : '50',
														handler : radiusSizeHandler,
														checked : true,
														group : 'sradius'
													}, {
														text : '60',
														handler : radiusSizeHandler,
														checked : false,
														group : 'sradius'
													}]
										}
									}]
						});
				peptide_plot_store.on('load', function() {
					var xlabel = peptide_plot_store.getxlabel();
					var ylabel = peptide_plot_store.getylabel();
					lxlabel = (xlabel.length === 1) ? 0 : xlabel.length
					lylabel = (ylabel.length === 1) ? 0 : ylabel.length
					var chart = Ext.create('Ext.chart.Chart', {
						id : 'chartCmp',
						xtype : 'chart',
						style : 'background:#fff',
						animate : true,
						store : peptide_plot_store,
						insetPadding : 50,
						shadow : true,
						axes : [{
									type : 'Numeric',
									minimum : 0,
									position : 'left',
									fields : ['yplot'],
									label : {
										renderer : function(v) {
											if (v == 0) {
												return ''
											} else {
												return 'Fraction:' + ylabel[parseInt(v - 1)]
											}
										}
									},
									title : 'MS1 intensity',
									minorTickSteps : 0.1,
									majorTickSteps : lylabel,
									grid : {
										odd : {
											opacity : 0.15,
											fill : '#d93a49',
											stroke : '#ef5b9c',
											'stroke-width' : 0
										}
									}
								}, {
									type : 'Numeric',
									position : 'bottom',
									fields : ['xplot'],
									label : {
										renderer : function(v) {
											if (v == 0) {
												return ''
											} else {
												return 'Repeat:' + xlabel[parseInt(v - 1)]
											}
										}
									},
									title : 'Retention Time',
									type : 'Numeric',
									minorTickSteps : 0.1,
									majorTickSteps : lxlabel,
									grid : {
										odd : {
											opacity : 0.15,
											fill : '#444693',
											stroke : '#6a6da9',
											'stroke-width' : 0
										}
									}
								}],
						series : [{
							type : 'scatter',
							axis : false,
							xField : 'xplot',
							yField : 'yplot',
							color : '#bed742',
							markerConfig : {
								type : 'circle',
								radius : 8,
								size : 5
							},
							tips : {
								trackMouse : true,
								width : 140,
								height : 60,
								layout : 'fit',
								items : {
									xtype : 'container',
									layout : 'hbox',
									//items : [pieChart, grid],
									items : []
								},
								renderer : function(klass, item) {
									var storeItem = item.storeItem;
//									this.setTitle('Repeat' + storeItem.get('repeat_id') + '_Fraction_' + storeItem.get('fraction_id') + '( RT:'
//											+ storeItem.get('rt') + ', Intensity:' + storeItem.get('intensity') + ', Area:' + storeItem.get('area')
//											+ ")");
									this.setTitle('Repeat' + storeItem.get('repeat_id') + '_Fraction_' + storeItem.get('fraction_id')+'</br>' + ' RT:'
											+ storeItem.get('rt') +'</br>'+ 'Intensity:' + storeItem.get('intensity').toExponential(3)+'');
									//grid.setSize(260, 130);
								}
							},
							listeners : {	
								itemmousedown : function(obj) {
									var win = Ext.create('Ext.Window', {
										width : 1200,
										// height
										// :
										// 735,
										height : 600,
										minHeight : 400,
										minWidth : 550,
										hidden : true,
										maximizable : true,
										title : 'MS Viewer',
										// renderTo
										// :
										// Ext.getBody(),
										layout : 'fit',
										html : 'Take about 1 minute for first time.<iframe name="spview" id="spview" width="100%" height="100%" frameborder=0 src=/gardener/peptide_viwer?sequence='
												+ obj.storeItem.data['sequence']
												+ '&charge='
												+ obj.storeItem.data['charge']
												+ '&pre_mz='
												+ obj.storeItem.data['pre_mz']
												+ '&search_id='
												+ obj.storeItem.data['search_id']
												+ '&ms1_scan='
												+ obj.storeItem.data['ms1_scan']
												+ '&ms2_scan='
												+ obj.storeItem.data['ms2_scan']
												+ '&rt='
												+ obj.storeItem.data['rt']
												+ '&ms1_rt='
												+ obj.storeItem.data['ms1_rt']
												+ '&filename='
												+ obj.storeItem.data['filename'] + '&id=' + obj.storeItem.data['id'] + '></iframe>'
									});
									// win.getEl().setStyle('z-index',
									// '80000');
									win.show();
									// alert(obj.storeItem.data['ms2_scan']
									// + '
									// &' +
									// obj.storeItem.data['ms1_scan']);
								}
							}
						}]
					});
					var win = Ext.create('Ext.Window', {
								draggable : {
									constrain : true,
									constrainTo : Ext.getBody()
								},
								width : 900,
								height : 500,
								minHeight : 100,
								minWidth : 100,
								hidden : true,
								maximizable : true,
								title : 'Peptide Quantification Plot',
								// renderTo
								// :
								// Ext.getBody(),
								layout : 'fit',
								tbar : [{
									text : 'Save Chart',
									handler : function() {
										Ext.MessageBox.confirm('Confirm Download', 'Would you like to download the chart as an image?', function(
														choice) {
													if (choice == 'yes') {
														chart.save({
																	type : 'image/png'
																});
													}
												});
									}
								}, {
									text : 'Select Color',
									menu : colorMenu
								}, {
									text : 'Select Grayscale',
									menu : grayscaleMenu
								}],
								items : chart
							});
					// win.getEl().setStyle('z-index',
					// '80000');
					win.show();
					waitWin.close()
					// Ext.Msg.alert('Experiment
					// Info:'+xlabel,
					// ylabel);
					refresh();
				});
			}
		}
		this.control({
			'experiment' : {
				cellclick : function(grid, td, cellIndex, record, tr, rowIndex, e, eOpts) {
					var clickedDataIndex = grid.panel.headerCt.getHeaderAtIndex(cellIndex).dataIndex;
					console.log(grid.panel.headerCt.getHeaderAtIndex(cellIndex))
					var clickedColumnName = grid.panel.headerCt.getHeaderAtIndex(cellIndex).text;
					var clickedCellValue = record.get(clickedDataIndex);

					var timestamp = (new Date()).valueOf()
					if (clickedColumnName == "Spectrum Num" && cellIndex > 0) {
						if (record.get('num_isoform') == 0) {
							Ext.Msg.alert('Warning', 'No Spectrum found.')
							return
						}
						ticPlot("cellclick", record);
						// alert("Show fraction")
					} else if (clickedColumnName == "Isoform Num" && cellIndex > 0) {
						if (record.get('num_isoform') == 0) {
							Ext.Msg.alert('Warning', 'No Isoform found.')
							return
						}

						var filters = {
							ftype : 'filters',
							encode : true
						}
						function onStoreSizeChange() {
							grid.down('#status').update({
										count : tstore.getTotalCount()
									});
						}
						var tstore = Ext.create('gar.store.Protein', {
									listeners : {
										totalcountchange : onStoreSizeChange
									}
								});
						tstore.getProxy().extraParams = {
							sid : record.data.id,
							stype : 'exper'
						};
						Ext.getCmp('info_protein_tab_index').value += 1;
						var grid = Ext.create('gar.view.Protein', {
							// id :
							// 'protein_tab_'+
							// Ext.getCmp('info_protein_tab_index').value,
							store : tstore,
							features : [filters],
							dockedItems : [{
								dock : 'top',
								xtype : 'toolbar',
								items : [{
											text : 'Clear Filter Data',
											handler : function() {
												grid.filters.clearFilters();
											}
										}, {
											text : 'All Filter Data',
											tooltip : 'Get Filter Data for Grid',
											handler : function() {
												var annoList = {
													'co_1': 'Coreg',
													'ki_1': 'Kinase', 
													'li_1': 'Ligand', 
													're_1': 'Receptor', 
													'pmm_1':'Plasma Membrane(Mouse)', 
													'pmh_1':'Plasma Membrane(Human)',
													'tf_1': 'Transcription Factor'
												}
												var modiList = {
													'Acetyl_1': 'N-terminal Acetyltrasferases',
													'Methyl_1': 'Methylation',
													'GlyGly_1': 'Ubiquitination',
													'Biotin_1': 'Biotin',
													'PhosphoST_1': 'Phosphorylation-ST',
													'PhosphoY_1': 'Phosphorylation-Y'
												}
												var filterData = grid.filters.getFilterData()
												var filtersStore = Ext.create('Ext.data.Store', {
												    fields:['field', 'type', 'value'],
												    data:[]
												});

												for( var i = 0; i < filterData.length; i++)
												{
													var field, type, value
													field = filterData[i].field
													switch(filterData[i].data.type)
													{
														case 'string':
															type = 'has string'
															value = filterData[i].data.value
															filtersStore.add({ 'field': field, "type": type, "value": value })
															break
														case 'list':
															type = 'has type'
															for( var j = 0; j < filterData[i].data.value.length; j++)
															{
																value = filterData[i].data.value[j]
																if(field == 'annotation')
																	filtersStore.add({ 'field': field, "type": type, "value": annoList[value] })
																else if (field == 'modification')
																	filtersStore.add({ 'field': field, "type": type, "value": modiList[value] })
															}
															break
														case 'numeric':
															switch(filterData[i].data.comparison.slice(0,2))
															{
																case 'gt':
																	type = 'is bigger than'
																	break
																case 'lt':
																	type = 'is little than'
																	break
																case 'eq':
																	type = 'equals to'
																	break
																default:
																	type = 'null'
															}
															value = filterData[i].data.value
															filtersStore.add({ 'field': field, "type": type, "value": value })
															break
														default: 
															type = 'null'
													}
												}

												var filterWindow = Ext.create(Ext.window.Window,{
													title: 'All filter data',
													height: 300,
													width: 500,
													modal: true,
													animateTarget: this,
													layout: 'fit',
													autoShow: true,
													items: [{
														xtype: 'grid',
														hideHeaders: true,
														columns: [
													        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
													        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
													        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
													    ],
													    store: filtersStore
													}]
												})
											}
										}, {
											text : 'Refresh This Tab',
											tooltip : 'Update to Latest Progress',
											handler : function() {
												tstore.load()
											}
										}, {
											iconCls : 'refresh',
											text : 'Batch Annotation',
											tooltip : '',
											handler : function() {
												var tab = Ext.create('Ext.form.Panel', {
															bodyPadding : 5,
															width : 350,
															url : '/gardener/batchAnnotation/',
															layout : 'anchor',
															defaults : {
																anchor : '100%'
															},
															defaultType : 'textfield',
															items : [{
																		xtype : 'textarea',
																		fieldLabel : 'Symbol List',
																		name : 'symbol',
																		height : 200,
																		allowBlank : false
																	}, {
																		fieldLabel : 'Annotation',
																		name : 'annotation',
																		allowBlank : false
																	}],
															buttons : [{
																		text : 'Get Current Symbols',
																		handler : function() {
																			var btn = this
																			var exploadMask = new Ext.LoadMask(grid, {
																						msg : 'Loading.....'
																					});
																			exploadMask.show();
																			var data = grid.filters.getFilterData();
																			var s = '[';
																			for (i = 0; i < data.length; i++) {
																				s += '{'
																				temp = String(Ext.encode(data[i].data))
																				s += temp.substr(1, temp.length - 2)
																				s += ',"field":"'
																				s += String(data[i].field)
																				s += '"}'
																				if (i != data.length - 1)
																					s += ','
																			}
																			s += ']'
																			Ext.Ajax.request({
																						url : '/gardener/data/showprotein/',
																						method : 'GET',
																						timeout : 600000,
																						params : {
																							sid : record.data.id,
																							stype : 'exper',
																							filter : s,
																							limit : -1
																						},
																						success : function(response) {
																							exploadMask.hide();
																							var text = response.responseText;
																							text = Ext.JSON.decode(text)
																							var data = text.data
																							var total = text.total
																							var tempstring = ''
																							for (var count = 0; count < total; count++) {
																								tempstring = tempstring + data[count].symbol + '\n'
																							}
																							btn.up('form').form.setValues({
																										symbol : tempstring
																									})
																						},
																						failure : function() {
																							exploadMask.hide();
																						}
																					});

																		}
																	}, {
																		text : 'Reset',
																		handler : function() {
																			this.up('form').getForm().reset();
																		}
																	}, {
																		text : 'Submit',
																		formBind : true,
																		// disabled:
																		// true,
																		handler : function() {
																			var form = this.up('form').getForm();
																			if (form.isValid()) {
																				// console.log('yes')
																				form.submit({
																							url : '/gardener/userAnnotation/',
																							params : {
																								exp : Ext.getCmp('content-panel').activeTab.title
																										.split('of ')[1],
																								batch : true
																							},
																							waitMsg : 'Adding Experiment......',
																							timeout : 300000,
																							success : function(form, action) {
																								Ext.Msg.alert('Success', action.result.msg);
																							},
																							failure : function(form, action) {
																								Ext.Msg.alert('Failed', action.result.msg);
																							}
																						});
																			}
																		}
																	}]
														});
												var win = new Ext.Window({
													draggable : {
														constrain : true,
														constrainTo : Ext.getBody()
													},
													// title : 'Comparison
													// Search',
													// width : 500,
													resizable : false,
													// animateTarget :
													// 'newcompare',
													items : [tab]
														/*
														 * , bbar : ['->', {
														 * text : 'Yes', handler :
														 * submitForm }, { text :
														 * 'No', handler :
														 * function() {
														 * win.close() } }]
														 */
													})
												win.show()
											}
										}, {
											text : 'To Genome Browser',
											// tooltip : 'Get Filter Data for
											// Grid',
											handler : function() {
												var exploadMask = new Ext.LoadMask(grid, {
															msg : 'Loading.....'
														});
												exploadMask.show();
												var data = grid.filters.getFilterData();
												var s = '[';
												for (i = 0; i < data.length; i++) {
													s += '{'
													temp = String(Ext.encode(data[i].data))
													s += temp.substr(1, temp.length - 2)
													s += ',"field":"'
													s += String(data[i].field)
													s += '"}'
													if (i != data.length - 1)
														s += ','
												}
												s += ']'
												Ext.Ajax.request({
													url : '/gardener/data/showprotein/',
													method : 'GET',
													timeout : 600000,
													params : {
														sid : record.data.id,
														stype : 'exper',
														filter : s,
														toGenome : true
													},
													success : function(response) {
														exploadMask.hide();
														var text = response.responseText;
														file = Ext.JSON.decode(text).file;
														species = Ext.JSON.decode(text).species;
														chr = Ext.JSON.decode(text).chr
														c = Ext.getCmp('content-panel')
														tempStr = Ext.String
																.format(
																		"https://genome.ucsc.edu/cgi-bin/hgTracks?org={0}&hgt.customText=http://firmiana.org{1}&position={2}",
																		species, file, chr)
														Ext.getCmp('info_tab_index').value += 1
														c.add({
															title : 'UCSC Browser',
															// iconCls : 'tabs',
															closable : true,
															// id : 'tab_ucsc',
															// Ext.getCmp('info_tab_index').value,
															layout : 'fit',
															html : '<iframe name="spview" id="spview" width="100%" height="100%" frameborder=0 src="'
																	+ tempStr + '"></iframe>'
														}).show()
													},
													failure : function() {
														exploadMask.hide();
													}
												});
											}
										}, {
											xtype : 'button',
											itemId : 'ppi',
											text : 'PPI Analysis',
											disabled : true,
											handler : function() {
												var tmpGrid = grid
												var sm = tmpGrid.getSelectionModel()
												var proteinIdControl = sm.getSelection()[0].data.accession
												var proteinIdCaseList = []
												for (var i = 1; i < sm.getSelection().length; i++) {
													proteinIdCaseList.push(sm.getSelection()[i].data.accession)
												}
												Ext.widget('ppi', {
															proteinIdControl : proteinIdControl,
															proteinIdCaseList : proteinIdCaseList
														})
											}
										}, '->', {
											xtype : 'component',
											itemId : 'status',
											tpl : 'Matching Proteins: {count}',
											style : 'margin-right:5px'
										}]
							}],
							emptyText : 'No Matching Records',
							listeners : {
								cellclick : function(dbcell, td, cell, record, tr, row, e) {
									var clickedDataIndex = dbcell.panel.headerCt.getHeaderAtIndex(cell).dataIndex;
									// console.log(dbcell.panel.headerCt.getHeaderAtIndex(cell))
									var clickedColumnName = dbcell.panel.headerCt.getHeaderAtIndex(cell).text;
									var clickedCellValue = record.get(clickedDataIndex);
									// console.log(clickedColumnName)
									if (clickedColumnName == 'Accession') {
										ucsc_plot(dbcell, td, cell, record, tr, row, e)
									} else if (clickedColumnName == 'Coverage') {
										console.log(record)
										accession = record.get('accession')
										expName = record.get('exp_name')
										var win = Ext.create('Ext.Window', {
													width : 650,
													height : 200,
													hidden : false,
													autoScroll : true,
													maximizable : true,
													title : 'Protein Coverage of ' + accession,
													// animateTarget :
													// 'mevennplot',
													layout : 'fit',
													html : '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>',
													listeners : {
														afterRender : function() {
															Ext.Ajax.request({
																		timeout : 600000,
																		url : '/gardener/coverage/',
																		method : 'GET',
																		params : {
																			accession : accession,
																			expName : expName
																		},
																		success : function(response) {
																			win.update(response.responseText);
																		},
																		failure : function() {
																			win.update("Sorry! Error happen, please contact Admin with current URL.");
																		}
																	});
														}
													}
												});
										win.show();
									}
								},
								'selectionchange' : function(view, records) {
									grid.down('#ppi').setDisabled(!records.length)
								}
							},
							plugins : [Ext.create('Ext.grid.plugin.CellEditing', {
												clicksToEdit : 1,
												listeners : {
													edit : function(editor, e) {
														// commit the changes
														// right after
														// editing finished
														// console.log(e)
														console.log(grid)
														var sym = grid.getStore().getAt(e.rowIdx).get('symbol')
														if (!sym || sym == '-') {
															Ext.Msg.alert('Error', 'Symbol error')
															return
														}
														Ext.Ajax.request({
																	timeout : 600000,
																	url : '/gardener/userAnnotation/',
																	method : 'POST',
																	params : {
																		exp : Ext.getCmp('content-panel').activeTab.title.split('of ')[1],
																		symbol : sym,
																		annotation : e.value
																	}
																});
													}
												}
											}), {
										ptype : 'rowexpander',
										selectRowOnExpand : true,
										expandOnDblClick : true,
										rowBodyTpl : ['<div id="Exp-Peptide-' + timestamp + '{id}" ></div>'],
										toggleRow : function(rowIdx, record) {
											var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
													.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view
													.getRecord(rowNode), grid = this.getCmp(), id = record.get('id'), targetId = 'Exp-Peptide-'
													+ timestamp + id, accession = record.get('accession'), search_id = record.get('search_id'), num_peptides = record
													.get('num_peptides');
											if (row.hasCls(this.rowCollapsedCls)) {
												row.removeCls(this.rowCollapsedCls);
												this.recordsExpanded[record.internalId] = true;
												this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
												if (rowNode.grid) {
													nextBd.removeCls(hiddenCls);
													rowNode.grid.doComponentLayout();
												} else {
													Ext.create('Ext.data.Store', {
																model : 'gar.model.Peptide',
																pageSize : 100,
																buffered : true,
																// leadingBufferZone
																// :
																// 300,
																autoLoad : true,
																proxy : {
																	type : 'ajax',
																	url : '/gardener/data/showpeptide/',
																	extraParams : {
																		sid : id,
																		accession : accession,
																		search_id : search_id,
																		stype : 'protein'
																	},
																	reader : {
																		type : 'json',
																		root : 'data',
																		totalProperty : 'total'
																	}
																},
																autoLoad : {
																	callback : function() {
																		nextBd.removeCls(hiddenCls);
																		// console.log(num_peptides);
																		var h = 100 + num_peptides * 20;
																		if (h > 400) {
																			h = 400
																		}
																		Ext.create('gar.view.Peptide', {
																					border : true,
																					height : h, // Redefine
																					// view
																					// of
																					// pep
																					renderTo : targetId,
																					store : this,
																					row : row,
																					layout : 'fit',
																					listeners : {
																						cellclick : peptide_sum_plot
																					}
																				});
																		rowNode.grid = grid;
																		// grid.suspendEvents();
																	}
																},
																listeners : {
																	beforeload : function() {
																		exploadMask.show();
																	},
																	load : function() {
																		exploadMask.hide();
																	}
																}
															});
												}
											} else {
												row.addCls(this.rowCollapsedCls);
												nextBd.addCls(this.rowBodyHiddenCls);
												this.recordsExpanded[record.internalId] = false;
												this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
											}
										}
									}]
						})
						c = Ext.getCmp('content-panel')
						// console.log(c)
						Ext.getCmp('info_tab_index').value += 1
						if(record.data.name == 'Exp007004'){
							var filters2 = {
								ftype : 'filters',
								encode : true
							}
							function onStoreSizeChange2() {
								grid2.down('#status').update({
											count : tstore2.getTotalCount()
										});
							}
							var tstore2 = Ext.create('gar.store.Protein', {
										listeners : {
											totalcountchange : onStoreSizeChange2
										}
									});
							tstore2.getProxy().url = '/gardener/data/silacprotein/'
							tstore2.getProxy().extraParams = {
								stype : 'exper',
								label: 'light',
								exp_name: record.data.name
							};
							var grid2 = Ext.create('gar.view.Protein', {
								// id :
								// 'protein_tab_'+
								// Ext.getCmp('info_protein_tab_index').value,
								store : tstore2,
								features : [filters2],
								dockedItems : [{
									dock : 'top',
									xtype : 'toolbar',
									items : [{
												text : 'Clear Filter Data',
												handler : function() {
													grid2.filters.clearFilters();
												}
											}, {
												text : 'All Filter Data',
												tooltip : 'Get Filter Data for Grid',
												handler : function() {
													var annoList = {
														'co_1': 'Coreg',
														'ki_1': 'Kinase', 
														'li_1': 'Ligand', 
														're_1': 'Receptor', 
														'pmm_1':'Plasma Membrane(Mouse)', 
														'pmh_1':'Plasma Membrane(Human)',
														'tf_1': 'Transcription Factor'
													}
													var modiList = {
														'Acetyl_1': 'N-terminal Acetyltrasferases',
														'Methyl_1': 'Methylation',
														'GlyGly_1': 'Ubiquitination',
														'Biotin_1': 'Biotin',
														'PhosphoST_1': 'Phosphorylation-ST',
														'PhosphoY_1': 'Phosphorylation-Y'
													}
													var filterData = grid2.filters.getFilterData()
													var filtersStore = Ext.create('Ext.data.Store', {
													    fields:['field', 'type', 'value'],
													    data:[]
													});

													for( var i = 0; i < filterData.length; i++)
													{
														var field, type, value
														field = filterData[i].field
														switch(filterData[i].data.type)
														{
															case 'string':
																type = 'has string'
																value = filterData[i].data.value
																filtersStore.add({ 'field': field, "type": type, "value": value })
																break
															case 'list':
																type = 'has type'
																for( var j = 0; j < filterData[i].data.value.length; j++)
																{
																	value = filterData[i].data.value[j]
																	if(field == 'annotation')
																		filtersStore.add({ 'field': field, "type": type, "value": annoList[value] })
																	else if (field == 'modification')
																		filtersStore.add({ 'field': field, "type": type, "value": modiList[value] })
																}
																break
															case 'numeric':
																switch(filterData[i].data.comparison.slice(0,2))
																{
																	case 'gt':
																		type = 'is bigger than'
																		break
																	case 'lt':
																		type = 'is little than'
																		break
																	case 'eq':
																		type = 'equals to'
																		break
																	default:
																		type = 'null'
																}
																value = filterData[i].data.value
																filtersStore.add({ 'field': field, "type": type, "value": value })
																break
															default: 
																type = 'null'
														}
													}

													var filterWindow = Ext.create(Ext.window.Window,{
														title: 'All filter data',
														height: 300,
														width: 500,
														modal: true,
														animateTarget: this,
														layout: 'fit',
														autoShow: true,
														items: [{
															xtype: 'grid',
															hideHeaders: true,
															columns: [
														        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
														        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
														        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
														    ],
														    store: filtersStore
														}]
													})
												}
											}, {
												text : 'Refresh This Tab',
												tooltip : 'Update to Latest Progress',
												handler : function() {
													tstore2.load()
												}
											}, {
												iconCls : 'refresh',
												text : 'Batch Annotation',
												tooltip : '',
												handler : function() {
													var tab = Ext.create('Ext.form.Panel', {
																bodyPadding : 5,
																width : 350,
																url : '/gardener/batchAnnotation/',
																layout : 'anchor',
																defaults : {
																	anchor : '100%'
																},
																defaultType : 'textfield',
																items : [{
																			xtype : 'textarea',
																			fieldLabel : 'Symbol List',
																			name : 'symbol',
																			height : 200,
																			allowBlank : false
																		}, {
																			fieldLabel : 'Annotation',
																			name : 'annotation',
																			allowBlank : false
																		}],
																buttons : [{
																			text : 'Get Current Symbols',
																			handler : function() {
																				var btn = this
																				var exploadMask = new Ext.LoadMask(grid2, {
																							msg : 'Loading.....'
																						});
																				exploadMask.show();
																				var data = grid2.filters.getFilterData();
																				var s = '[';
																				for (i = 0; i < data.length; i++) {
																					s += '{'
																					temp = String(Ext.encode(data[i].data))
																					s += temp.substr(1, temp.length - 2)
																					s += ',"field":"'
																					s += String(data[i].field)
																					s += '"}'
																					if (i != data.length - 1)
																						s += ','
																				}
																				s += ']'
																				Ext.Ajax.request({
																							url : '/gardener/data/showprotein/',
																							method : 'GET',
																							timeout : 600000,
																							params : {
																								sid : record.data.id,
																								stype : 'exper',
																								filter : s,
																								limit : -1
																							},
																							success : function(response) {
																								exploadMask.hide();
																								var text = response.responseText;
																								text = Ext.JSON.decode(text)
																								var data = text.data
																								var total = text.total
																								var tempstring = ''
																								for (var count = 0; count < total; count++) {
																									tempstring = tempstring + data[count].symbol + '\n'
																								}
																								btn.up('form').form.setValues({
																											symbol : tempstring
																										})
																							},
																							failure : function() {
																								exploadMask.hide();
																							}
																						});

																			}
																		}, {
																			text : 'Reset',
																			handler : function() {
																				this.up('form').getForm().reset();
																			}
																		}, {
																			text : 'Submit',
																			formBind : true,
																			// disabled:
																			// true,
																			handler : function() {
																				var form = this.up('form').getForm();
																				if (form.isValid()) {
																					// console.log('yes')
																					form.submit({
																								url : '/gardener/userAnnotation/',
																								params : {
																									exp : Ext.getCmp('content-panel').activeTab.title
																											.split('of ')[1],
																									batch : true
																								},
																								waitMsg : 'Adding Experiment......',
																								timeout : 300000,
																								success : function(form, action) {
																									Ext.Msg.alert('Success', action.result.msg);
																								},
																								failure : function(form, action) {
																									Ext.Msg.alert('Failed', action.result.msg);
																								}
																							});
																				}
																			}
																		}]
															});
													var win = new Ext.Window({
														draggable : {
															constrain : true,
															constrainTo : Ext.getBody()
														},
														// title : 'Comparison
														// Search',
														// width : 500,
														resizable : false,
														// animateTarget :
														// 'newcompare',
														items : [tab]
															/*
															 * , bbar : ['->', {
															 * text : 'Yes', handler :
															 * submitForm }, { text :
															 * 'No', handler :
															 * function() {
															 * win.close() } }]
															 */
														})
													win.show()
												}
											}, {
												text : 'To Genome Browser',
												// tooltip : 'Get Filter Data for
												// Grid',
												handler : function() {
													var exploadMask = new Ext.LoadMask(grid2, {
																msg : 'Loading.....'
															});
													exploadMask.show();
													var data = grid2.filters.getFilterData();
													var s = '[';
													for (i = 0; i < data.length; i++) {
														s += '{'
														temp = String(Ext.encode(data[i].data))
														s += temp.substr(1, temp.length - 2)
														s += ',"field":"'
														s += String(data[i].field)
														s += '"}'
														if (i != data.length - 1)
															s += ','
													}
													s += ']'
													Ext.Ajax.request({
														url : '/gardener/data/showprotein/',
														method : 'GET',
														timeout : 600000,
														params : {
															sid : record.data.id,
															stype : 'exper',
															filter : s,
															toGenome : true
														},
														success : function(response) {
															exploadMask.hide();
															var text = response.responseText;
															file = Ext.JSON.decode(text).file;
															species = Ext.JSON.decode(text).species;
															chr = Ext.JSON.decode(text).chr
															c = Ext.getCmp('content-panel')
															tempStr = Ext.String
																	.format(
																			"https://genome.ucsc.edu/cgi-bin/hgTracks?org={0}&hgt.customText=http://firmiana.org{1}&position={2}",
																			species, file, chr)
															Ext.getCmp('info_tab_index').value += 1
															c.add({
																title : 'UCSC Browser',
																// iconCls : 'tabs',
																closable : true,
																// id : 'tab_ucsc',
																// Ext.getCmp('info_tab_index').value,
																layout : 'fit',
																html : '<iframe name="spview" id="spview" width="100%" height="100%" frameborder=0 src="'
																		+ tempStr + '"></iframe>'
															}).show()
														},
														failure : function() {
															exploadMask.hide();
														}
													});
												}
											}, {
												xtype : 'button',
												itemId : 'ppi',
												text : 'PPI Analysis',
												disabled : true,
												handler : function() {
													var tmpGrid = grid2
													var sm = tmpGrid.getSelectionModel()
													var proteinIdControl = sm.getSelection()[0].data.accession
													var proteinIdCaseList = []
													for (var i = 1; i < sm.getSelection().length; i++) {
														proteinIdCaseList.push(sm.getSelection()[i].data.accession)
													}
													Ext.widget('ppi', {
																proteinIdControl : proteinIdControl,
																proteinIdCaseList : proteinIdCaseList
															})
												}
											}, '->', {
												xtype : 'component',
												itemId : 'status',
												tpl : 'Matching Proteins: {count}',
												style : 'margin-right:5px'
											}]
								}],
								emptyText : 'No Matching Records',
								listeners : {
									cellclick : function(dbcell, td, cell, record, tr, row, e) {
										var clickedDataIndex = dbcell.panel.headerCt.getHeaderAtIndex(cell).dataIndex;
										// console.log(dbcell.panel.headerCt.getHeaderAtIndex(cell))
										var clickedColumnName = dbcell.panel.headerCt.getHeaderAtIndex(cell).text;
										var clickedCellValue = record.get(clickedDataIndex);
										// console.log(clickedColumnName)
										if (clickedColumnName == 'Accession') {
											ucsc_plot(dbcell, td, cell, record, tr, row, e)
										} else if (clickedColumnName == 'Coverage') {
											console.log(record)
											accession = record.get('accession')
											expName = record.get('exp_name')
											var win = Ext.create('Ext.Window', {
														width : 650,
														height : 200,
														hidden : false,
														autoScroll : true,
														maximizable : true,
														title : 'Protein Coverage of ' + accession,
														// animateTarget :
														// 'mevennplot',
														layout : 'fit',
														html : '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>',
														listeners : {
															afterRender : function() {
																Ext.Ajax.request({
																			timeout : 600000,
																			url : '/gardener/coverage/',
																			method : 'GET',
																			params : {
																				accession : accession,
																				expName : expName
																			},
																			success : function(response) {
																				win.update(response.responseText);
																			},
																			failure : function() {
																				win.update("Sorry! Error happen, please contact Admin with current URL.");
																			}
																		});
															}
														}
													});
											win.show();
										}
									},
									'selectionchange' : function(view, records) {
										grid2.down('#ppi').setDisabled(!records.length)
									}
								},
								plugins : [Ext.create('Ext.grid.plugin.CellEditing', {
													clicksToEdit : 1,
													listeners : {
														edit : function(editor, e) {
															// commit the changes
															// right after
															// editing finished
															// console.log(e)
															console.log(grid2)
															var sym = grid2.getStore().getAt(e.rowIdx).get('symbol')
															if (!sym || sym == '-') {
																Ext.Msg.alert('Error', 'Symbol error')
																return
															}
															Ext.Ajax.request({
																		timeout : 600000,
																		url : '/gardener/userAnnotation/',
																		method : 'POST',
																		params : {
																			exp : Ext.getCmp('content-panel').activeTab.title.split('of ')[1],
																			symbol : sym,
																			annotation : e.value
																		}
																	});
														}
													}
												}), {
											ptype : 'rowexpander',
											selectRowOnExpand : true,
											expandOnDblClick : true,
											rowBodyTpl : ['<div id="Exp-Peptide-' + timestamp + '{id}" ></div>'],
											toggleRow : function(rowIdx, record) {
												var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
														.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view
														.getRecord(rowNode), grid2 = this.getCmp(), id = record.get('id'), targetId = 'Exp-Peptide-'
														+ timestamp + id, accession = record.get('accession'), search_id = record.get('search_id'), num_peptides = record
														.get('num_peptides');
												if (row.hasCls(this.rowCollapsedCls)) {
													row.removeCls(this.rowCollapsedCls);
													this.recordsExpanded[record.internalId] = true;
													this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
													if (rowNode.grid2) {
														nextBd.removeCls(hiddenCls);
														rowNode.grid2.doComponentLayout();
													} else {
														Ext.create('Ext.data.Store', {
																	model : 'gar.model.Peptide',
																	pageSize : 100,
																	buffered : true,
																	// leadingBufferZone
																	// :
																	// 300,
																	autoLoad : true,
																	proxy : {
																		type : 'ajax',
																		url : '/gardener/data/showpeptide/',
																		extraParams : {
																			sid : id,
																			accession : accession,
																			search_id : search_id,
																			stype : 'protein'
																		},
																		reader : {
																			type : 'json',
																			root : 'data',
																			totalProperty : 'total'
																		}
																	},
																	autoLoad : {
																		callback : function() {
																			nextBd.removeCls(hiddenCls);
																			// console.log(num_peptides);
																			var h = 100 + num_peptides * 20;
																			if (h > 400) {
																				h = 400
																			}
																			Ext.create('gar.view.Peptide', {
																						border : true,
																						height : h, // Redefine
																						// view
																						// of
																						// pep
																						renderTo : targetId,
																						store : this,
																						row : row,
																						layout : 'fit',
																						listeners : {
																							cellclick : peptide_sum_plot
																						}
																					});
																			rowNode.grid = grid2;
																			// grid.suspendEvents();
																		}
																	},
																	listeners : {
																		beforeload : function() {
																			exploadMask.show();
																		},
																		load : function() {
																			exploadMask.hide();
																		}
																	}
																});
													}
												} else {
													row.addCls(this.rowCollapsedCls);
													nextBd.addCls(this.rowBodyHiddenCls);
													this.recordsExpanded[record.internalId] = false;
													this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
												}
											}
										}]
							})
							var filters3 = {
								ftype : 'filters',
								encode : true
							}
							function onStoreSizeChange3() {
								grid3.down('#status').update({
											count : tstore3.getTotalCount()
										});
							}
							var tstore3 = Ext.create('gar.store.Protein', {
										listeners : {
											totalcountchange : onStoreSizeChange3
										}
									});
							tstore3.getProxy().url = '/gardener/data/silacprotein/'
							tstore3.getProxy().extraParams = {
								stype : 'exper',
								label: 'heavy',
								exp_name: record.data.name
							};
							var grid3 = Ext.create('gar.view.Protein', {
								// id :
								// 'protein_tab_'+
								// Ext.getCmp('info_protein_tab_index').value,
								store : tstore3,
								features : [filters3],
								dockedItems : [{
									dock : 'top',
									xtype : 'toolbar',
									items : [{
												text : 'Clear Filter Data',
												handler : function() {
													grid3.filters.clearFilters();
												}
											}, {
												text : 'All Filter Data',
												tooltip : 'Get Filter Data for Grid',
												handler : function() {
													var annoList = {
														'co_1': 'Coreg',
														'ki_1': 'Kinase', 
														'li_1': 'Ligand', 
														're_1': 'Receptor', 
														'pmm_1':'Plasma Membrane(Mouse)', 
														'pmh_1':'Plasma Membrane(Human)',
														'tf_1': 'Transcription Factor'
													}
													var modiList = {
														'Acetyl_1': 'N-terminal Acetyltrasferases',
														'Methyl_1': 'Methylation',
														'GlyGly_1': 'Ubiquitination',
														'Biotin_1': 'Biotin',
														'PhosphoST_1': 'Phosphorylation-ST',
														'PhosphoY_1': 'Phosphorylation-Y'
													}
													var filterData = grid3.filters.getFilterData()
													var filtersStore = Ext.create('Ext.data.Store', {
													    fields:['field', 'type', 'value'],
													    data:[]
													});

													for( var i = 0; i < filterData.length; i++)
													{
														var field, type, value
														field = filterData[i].field
														switch(filterData[i].data.type)
														{
															case 'string':
																type = 'has string'
																value = filterData[i].data.value
																filtersStore.add({ 'field': field, "type": type, "value": value })
																break
															case 'list':
																type = 'has type'
																for( var j = 0; j < filterData[i].data.value.length; j++)
																{
																	value = filterData[i].data.value[j]
																	if(field == 'annotation')
																		filtersStore.add({ 'field': field, "type": type, "value": annoList[value] })
																	else if (field == 'modification')
																		filtersStore.add({ 'field': field, "type": type, "value": modiList[value] })
																}
																break
															case 'numeric':
																switch(filterData[i].data.comparison.slice(0,2))
																{
																	case 'gt':
																		type = 'is bigger than'
																		break
																	case 'lt':
																		type = 'is little than'
																		break
																	case 'eq':
																		type = 'equals to'
																		break
																	default:
																		type = 'null'
																}
																value = filterData[i].data.value
																filtersStore.add({ 'field': field, "type": type, "value": value })
																break
															default: 
																type = 'null'
														}
													}

													var filterWindow = Ext.create(Ext.window.Window,{
														title: 'All filter data',
														height: 300,
														width: 500,
														modal: true,
														animateTarget: this,
														layout: 'fit',
														autoShow: true,
														items: [{
															xtype: 'grid',
															hideHeaders: true,
															columns: [
														        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
														        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
														        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
														    ],
														    store: filtersStore
														}]
													})
												}
											}, {
												text : 'Refresh This Tab',
												tooltip : 'Update to Latest Progress',
												handler : function() {
													tstore3.load()
												}
											}, {
												iconCls : 'refresh',
												text : 'Batch Annotation',
												tooltip : '',
												handler : function() {
													var tab = Ext.create('Ext.form.Panel', {
																bodyPadding : 5,
																width : 350,
																url : '/gardener/batchAnnotation/',
																layout : 'anchor',
																defaults : {
																	anchor : '100%'
																},
																defaultType : 'textfield',
																items : [{
																			xtype : 'textarea',
																			fieldLabel : 'Symbol List',
																			name : 'symbol',
																			height : 200,
																			allowBlank : false
																		}, {
																			fieldLabel : 'Annotation',
																			name : 'annotation',
																			allowBlank : false
																		}],
																buttons : [{
																			text : 'Get Current Symbols',
																			handler : function() {
																				var btn = this
																				var exploadMask = new Ext.LoadMask(grid3, {
																							msg : 'Loading.....'
																						});
																				exploadMask.show();
																				var data = grid3.filters.getFilterData();
																				var s = '[';
																				for (i = 0; i < data.length; i++) {
																					s += '{'
																					temp = String(Ext.encode(data[i].data))
																					s += temp.substr(1, temp.length - 2)
																					s += ',"field":"'
																					s += String(data[i].field)
																					s += '"}'
																					if (i != data.length - 1)
																						s += ','
																				}
																				s += ']'
																				Ext.Ajax.request({
																							url : '/gardener/data/showprotein/',
																							method : 'GET',
																							timeout : 600000,
																							params : {
																								sid : record.data.id,
																								stype : 'exper',
																								filter : s,
																								limit : -1
																							},
																							success : function(response) {
																								exploadMask.hide();
																								var text = response.responseText;
																								text = Ext.JSON.decode(text)
																								var data = text.data
																								var total = text.total
																								var tempstring = ''
																								for (var count = 0; count < total; count++) {
																									tempstring = tempstring + data[count].symbol + '\n'
																								}
																								btn.up('form').form.setValues({
																											symbol : tempstring
																										})
																							},
																							failure : function() {
																								exploadMask.hide();
																							}
																						});

																			}
																		}, {
																			text : 'Reset',
																			handler : function() {
																				this.up('form').getForm().reset();
																			}
																		}, {
																			text : 'Submit',
																			formBind : true,
																			// disabled:
																			// true,
																			handler : function() {
																				var form = this.up('form').getForm();
																				if (form.isValid()) {
																					// console.log('yes')
																					form.submit({
																								url : '/gardener/userAnnotation/',
																								params : {
																									exp : Ext.getCmp('content-panel').activeTab.title
																											.split('of ')[1],
																									batch : true
																								},
																								waitMsg : 'Adding Experiment......',
																								timeout : 300000,
																								success : function(form, action) {
																									Ext.Msg.alert('Success', action.result.msg);
																								},
																								failure : function(form, action) {
																									Ext.Msg.alert('Failed', action.result.msg);
																								}
																							});
																				}
																			}
																		}]
															});
													var win = new Ext.Window({
														draggable : {
															constrain : true,
															constrainTo : Ext.getBody()
														},
														// title : 'Comparison
														// Search',
														// width : 500,
														resizable : false,
														// animateTarget :
														// 'newcompare',
														items : [tab]
															/*
															 * , bbar : ['->', {
															 * text : 'Yes', handler :
															 * submitForm }, { text :
															 * 'No', handler :
															 * function() {
															 * win.close() } }]
															 */
														})
													win.show()
												}
											}, {
												text : 'To Genome Browser',
												// tooltip : 'Get Filter Data for
												// Grid',
												handler : function() {
													var exploadMask = new Ext.LoadMask(grid3, {
																msg : 'Loading.....'
															});
													exploadMask.show();
													var data = grid3.filters.getFilterData();
													var s = '[';
													for (i = 0; i < data.length; i++) {
														s += '{'
														temp = String(Ext.encode(data[i].data))
														s += temp.substr(1, temp.length - 2)
														s += ',"field":"'
														s += String(data[i].field)
														s += '"}'
														if (i != data.length - 1)
															s += ','
													}
													s += ']'
													Ext.Ajax.request({
														url : '/gardener/data/showprotein/',
														method : 'GET',
														timeout : 600000,
														params : {
															sid : record.data.id,
															stype : 'exper',
															filter : s,
															toGenome : true
														},
														success : function(response) {
															exploadMask.hide();
															var text = response.responseText;
															file = Ext.JSON.decode(text).file;
															species = Ext.JSON.decode(text).species;
															chr = Ext.JSON.decode(text).chr
															c = Ext.getCmp('content-panel')
															tempStr = Ext.String
																	.format(
																			"https://genome.ucsc.edu/cgi-bin/hgTracks?org={0}&hgt.customText=http://firmiana.org{1}&position={2}",
																			species, file, chr)
															Ext.getCmp('info_tab_index').value += 1
															c.add({
																title : 'UCSC Browser',
																// iconCls : 'tabs',
																closable : true,
																// id : 'tab_ucsc',
																// Ext.getCmp('info_tab_index').value,
																layout : 'fit',
																html : '<iframe name="spview" id="spview" width="100%" height="100%" frameborder=0 src="'
																		+ tempStr + '"></iframe>'
															}).show()
														},
														failure : function() {
															exploadMask.hide();
														}
													});
												}
											}, {
												xtype : 'button',
												itemId : 'ppi',
												text : 'PPI Analysis',
												disabled : true,
												handler : function() {
													var tmpGrid = grid3
													var sm = tmpGrid.getSelectionModel()
													var proteinIdControl = sm.getSelection()[0].data.accession
													var proteinIdCaseList = []
													for (var i = 1; i < sm.getSelection().length; i++) {
														proteinIdCaseList.push(sm.getSelection()[i].data.accession)
													}
													Ext.widget('ppi', {
																proteinIdControl : proteinIdControl,
																proteinIdCaseList : proteinIdCaseList
															})
												}
											}, '->', {
												xtype : 'component',
												itemId : 'status',
												tpl : 'Matching Proteins: {count}',
												style : 'margin-right:5px'
											}]
								}],
								emptyText : 'No Matching Records',
								listeners : {
									cellclick : function(dbcell, td, cell, record, tr, row, e) {
										var clickedDataIndex = dbcell.panel.headerCt.getHeaderAtIndex(cell).dataIndex;
										// console.log(dbcell.panel.headerCt.getHeaderAtIndex(cell))
										var clickedColumnName = dbcell.panel.headerCt.getHeaderAtIndex(cell).text;
										var clickedCellValue = record.get(clickedDataIndex);
										// console.log(clickedColumnName)
										if (clickedColumnName == 'Accession') {
											ucsc_plot(dbcell, td, cell, record, tr, row, e)
										} else if (clickedColumnName == 'Coverage') {
											console.log(record)
											accession = record.get('accession')
											expName = record.get('exp_name')
											var win = Ext.create('Ext.Window', {
														width : 650,
														height : 200,
														hidden : false,
														autoScroll : true,
														maximizable : true,
														title : 'Protein Coverage of ' + accession,
														// animateTarget :
														// 'mevennplot',
														layout : 'fit',
														html : '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>',
														listeners : {
															afterRender : function() {
																Ext.Ajax.request({
																			timeout : 600000,
																			url : '/gardener/coverage/',
																			method : 'GET',
																			params : {
																				accession : accession,
																				expName : expName
																			},
																			success : function(response) {
																				win.update(response.responseText);
																			},
																			failure : function() {
																				win.update("Sorry! Error happen, please contact Admin with current URL.");
																			}
																		});
															}
														}
													});
											win.show();
										}
									},
									'selectionchange' : function(view, records) {
										grid3.down('#ppi').setDisabled(!records.length)
									}
								},
								plugins : [Ext.create('Ext.grid.plugin.CellEditing', {
													clicksToEdit : 1,
													listeners : {
														edit : function(editor, e) {
															// commit the changes
															// right after
															// editing finished
															// console.log(e)
															console.log(grid3)
															var sym = grid3.getStore().getAt(e.rowIdx).get('symbol')
															if (!sym || sym == '-') {
																Ext.Msg.alert('Error', 'Symbol error')
																return
															}
															Ext.Ajax.request({
																		timeout : 600000,
																		url : '/gardener/userAnnotation/',
																		method : 'POST',
																		params : {
																			exp : Ext.getCmp('content-panel').activeTab.title.split('of ')[1],
																			symbol : sym,
																			annotation : e.value
																		}
																	});
														}
													}
												}), {
											ptype : 'rowexpander',
											selectRowOnExpand : true,
											expandOnDblClick : true,
											rowBodyTpl : ['<div id="Exp-Peptide-' + timestamp + '{id}" ></div>'],
											toggleRow : function(rowIdx, record) {
												var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
														.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view
														.getRecord(rowNode), grid3 = this.getCmp(), id = record.get('id'), targetId = 'Exp-Peptide-'
														+ timestamp + id, accession = record.get('accession'), search_id = record.get('search_id'), num_peptides = record
														.get('num_peptides');
												if (row.hasCls(this.rowCollapsedCls)) {
													row.removeCls(this.rowCollapsedCls);
													this.recordsExpanded[record.internalId] = true;
													this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
													if (rowNode.grid3) {
														nextBd.removeCls(hiddenCls);
														rowNode.grid3.doComponentLayout();
													} else {
														Ext.create('Ext.data.Store', {
																	model : 'gar.model.Peptide',
																	pageSize : 100,
																	buffered : true,
																	// leadingBufferZone
																	// :
																	// 300,
																	autoLoad : true,
																	proxy : {
																		type : 'ajax',
																		url : '/gardener/data/showpeptide/',
																		extraParams : {
																			sid : id,
																			accession : accession,
																			search_id : search_id,
																			stype : 'protein'
																		},
																		reader : {
																			type : 'json',
																			root : 'data',
																			totalProperty : 'total'
																		}
																	},
																	autoLoad : {
																		callback : function() {
																			nextBd.removeCls(hiddenCls);
																			// console.log(num_peptides);
																			var h = 100 + num_peptides * 20;
																			if (h > 400) {
																				h = 400
																			}
																			Ext.create('gar.view.Peptide', {
																						border : true,
																						height : h, // Redefine
																						// view
																						// of
																						// pep
																						renderTo : targetId,
																						store : this,
																						row : row,
																						layout : 'fit',
																						listeners : {
																							cellclick : peptide_sum_plot
																						}
																					});
																			rowNode.grid = grid3;
																			// grid.suspendEvents();
																		}
																	},
																	listeners : {
																		beforeload : function() {
																			exploadMask.show();
																		},
																		load : function() {
																			exploadMask.hide();
																		}
																	}
																});
													}
												} else {
													row.addCls(this.rowCollapsedCls);
													nextBd.addCls(this.rowBodyHiddenCls);
													this.recordsExpanded[record.internalId] = false;
													this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
												}
											}
										}]
							})
							
							var filters4 = {
								ftype : 'filters',
								encode : true
							}
							function onStoreSizeChange4() {
								grid4.down('#status').update({
											count : tstore4.getTotalCount()
										});
							}
							var tstore4 = Ext.create('gar.store.SilacProtein', {
										listeners : {
											totalcountchange : onStoreSizeChange4
										}
									});
							tstore4.getProxy().extraParams = {
								stype : 'exper',
								exp_name: record.data.name
							};
							console.log(tstore4)
							var grid4 = Ext.create('gar.view.SilacProtein', {
								// id :
								// 'protein_tab_'+
								// Ext.getCmp('info_protein_tab_index').value,
								store : tstore4,
								features : [filters4],
								dockedItems : [{
									dock : 'top',
									xtype : 'toolbar',
									items : [{
												text : 'Clear Filter Data',
												handler : function() {
													grid4.filters.clearFilters();
												}
											}, {
												text : 'All Filter Data',
												tooltip : 'Get Filter Data for Grid',
												handler : function() {
													var annoList = {
														'co_1': 'Coreg',
														'ki_1': 'Kinase', 
														'li_1': 'Ligand', 
														're_1': 'Receptor', 
														'pmm_1':'Plasma Membrane(Mouse)', 
														'pmh_1':'Plasma Membrane(Human)',
														'tf_1': 'Transcription Factor'
													}
													var modiList = {
														'Acetyl_1': 'N-terminal Acetyltrasferases',
														'Methyl_1': 'Methylation',
														'GlyGly_1': 'Ubiquitination',
														'Biotin_1': 'Biotin',
														'PhosphoST_1': 'Phosphorylation-ST',
														'PhosphoY_1': 'Phosphorylation-Y'
													}
													var filterData = grid4.filters.getFilterData()
													var filtersStore = Ext.create('Ext.data.Store', {
													    fields:['field', 'type', 'value'],
													    data:[]
													});

													for( var i = 0; i < filterData.length; i++)
													{
														var field, type, value
														field = filterData[i].field
														switch(filterData[i].data.type)
														{
															case 'string':
																type = 'has string'
																value = filterData[i].data.value
																filtersStore.add({ 'field': field, "type": type, "value": value })
																break
															case 'list':
																type = 'has type'
																for( var j = 0; j < filterData[i].data.value.length; j++)
																{
																	value = filterData[i].data.value[j]
																	if(field == 'annotation')
																		filtersStore.add({ 'field': field, "type": type, "value": annoList[value] })
																	else if (field == 'modification')
																		filtersStore.add({ 'field': field, "type": type, "value": modiList[value] })
																}
																break
															case 'numeric':
																switch(filterData[i].data.comparison.slice(0,2))
																{
																	case 'gt':
																		type = 'is bigger than'
																		break
																	case 'lt':
																		type = 'is little than'
																		break
																	case 'eq':
																		type = 'equals to'
																		break
																	default:
																		type = 'null'
																}
																value = filterData[i].data.value
																filtersStore.add({ 'field': field, "type": type, "value": value })
																break
															default: 
																type = 'null'
														}
													}

													var filterWindow = Ext.create(Ext.window.Window,{
														title: 'All filter data',
														height: 300,
														width: 500,
														modal: true,
														animateTarget: this,
														layout: 'fit',
														autoShow: true,
														items: [{
															xtype: 'grid',
															hideHeaders: true,
															columns: [
														        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
														        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
														        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
														    ],
														    store: filtersStore
														}]
													})
												}
											}, {
												text : 'Refresh This Tab',
												tooltip : 'Update to Latest Progress',
												handler : function() {
													tstore3.load()
												}
											}, {
												iconCls : 'refresh',
												text : 'Batch Annotation',
												tooltip : '',
												handler : function() {
													var tab = Ext.create('Ext.form.Panel', {
																bodyPadding : 5,
																width : 350,
																url : '/gardener/batchAnnotation/',
																layout : 'anchor',
																defaults : {
																	anchor : '100%'
																},
																defaultType : 'textfield',
																items : [{
																			xtype : 'textarea',
																			fieldLabel : 'Symbol List',
																			name : 'symbol',
																			height : 200,
																			allowBlank : false
																		}, {
																			fieldLabel : 'Annotation',
																			name : 'annotation',
																			allowBlank : false
																		}],
																buttons : [{
																			text : 'Get Current Symbols',
																			handler : function() {
																				var btn = this
																				var exploadMask = new Ext.LoadMask(grid4, {
																							msg : 'Loading.....'
																						});
																				exploadMask.show();
																				var data = grid4.filters.getFilterData();
																				var s = '[';
																				for (i = 0; i < data.length; i++) {
																					s += '{'
																					temp = String(Ext.encode(data[i].data))
																					s += temp.substr(1, temp.length - 2)
																					s += ',"field":"'
																					s += String(data[i].field)
																					s += '"}'
																					if (i != data.length - 1)
																						s += ','
																				}
																				s += ']'
																				Ext.Ajax.request({
																							url : '/gardener/data/showprotein/',
																							method : 'GET',
																							timeout : 600000,
																							params : {
																								sid : record.data.id,
																								stype : 'exper',
																								filter : s,
																								limit : -1
																							},
																							success : function(response) {
																								exploadMask.hide();
																								var text = response.responseText;
																								text = Ext.JSON.decode(text)
																								var data = text.data
																								var total = text.total
																								var tempstring = ''
																								for (var count = 0; count < total; count++) {
																									tempstring = tempstring + data[count].symbol + '\n'
																								}
																								btn.up('form').form.setValues({
																											symbol : tempstring
																										})
																							},
																							failure : function() {
																								exploadMask.hide();
																							}
																						});

																			}
																		}, {
																			text : 'Reset',
																			handler : function() {
																				this.up('form').getForm().reset();
																			}
																		}, {
																			text : 'Submit',
																			formBind : true,
																			// disabled:
																			// true,
																			handler : function() {
																				var form = this.up('form').getForm();
																				if (form.isValid()) {
																					// console.log('yes')
																					form.submit({
																								url : '/gardener/userAnnotation/',
																								params : {
																									exp : Ext.getCmp('content-panel').activeTab.title
																											.split('of ')[1],
																									batch : true
																								},
																								waitMsg : 'Adding Experiment......',
																								timeout : 300000,
																								success : function(form, action) {
																									Ext.Msg.alert('Success', action.result.msg);
																								},
																								failure : function(form, action) {
																									Ext.Msg.alert('Failed', action.result.msg);
																								}
																							});
																				}
																			}
																		}]
															});
													var win = new Ext.Window({
														draggable : {
															constrain : true,
															constrainTo : Ext.getBody()
														},
														// title : 'Comparison
														// Search',
														// width : 500,
														resizable : false,
														// animateTarget :
														// 'newcompare',
														items : [tab]
															/*
															 * , bbar : ['->', {
															 * text : 'Yes', handler :
															 * submitForm }, { text :
															 * 'No', handler :
															 * function() {
															 * win.close() } }]
															 */
														})
													win.show()
												}
											}, {
												text : 'To Genome Browser',
												// tooltip : 'Get Filter Data for
												// Grid',
												handler : function() {
													var exploadMask = new Ext.LoadMask(grid4, {
																msg : 'Loading.....'
															});
													exploadMask.show();
													var data = grid4.filters.getFilterData();
													var s = '[';
													for (i = 0; i < data.length; i++) {
														s += '{'
														temp = String(Ext.encode(data[i].data))
														s += temp.substr(1, temp.length - 2)
														s += ',"field":"'
														s += String(data[i].field)
														s += '"}'
														if (i != data.length - 1)
															s += ','
													}
													s += ']'
													Ext.Ajax.request({
														url : '/gardener/data/showprotein/',
														method : 'GET',
														timeout : 600000,
														params : {
															sid : record.data.id,
															stype : 'exper',
															filter : s,
															toGenome : true
														},
														success : function(response) {
															exploadMask.hide();
															var text = response.responseText;
															file = Ext.JSON.decode(text).file;
															species = Ext.JSON.decode(text).species;
															chr = Ext.JSON.decode(text).chr
															c = Ext.getCmp('content-panel')
															tempStr = Ext.String
																	.format(
																			"https://genome.ucsc.edu/cgi-bin/hgTracks?org={0}&hgt.customText=http://firmiana.org{1}&position={2}",
																			species, file, chr)
															Ext.getCmp('info_tab_index').value += 1
															c.add({
																title : 'UCSC Browser',
																// iconCls : 'tabs',
																closable : true,
																// id : 'tab_ucsc',
																// Ext.getCmp('info_tab_index').value,
																layout : 'fit',
																html : '<iframe name="spview" id="spview" width="100%" height="100%" frameborder=0 src="'
																		+ tempStr + '"></iframe>'
															}).show()
														},
														failure : function() {
															exploadMask.hide();
														}
													});
												}
											}, {
												xtype : 'button',
												itemId : 'ppi',
												text : 'PPI Analysis',
												disabled : true,
												handler : function() {
													var tmpGrid = grid4
													var sm = tmpGrid.getSelectionModel()
													var proteinIdControl = sm.getSelection()[0].data.accession
													var proteinIdCaseList = []
													for (var i = 1; i < sm.getSelection().length; i++) {
														proteinIdCaseList.push(sm.getSelection()[i].data.accession)
													}
													Ext.widget('ppi', {
																proteinIdControl : proteinIdControl,
																proteinIdCaseList : proteinIdCaseList
															})
												}
											}, '->', {
												xtype : 'component',
												itemId : 'status',
												tpl : 'Matching Proteins: {count}',
												style : 'margin-right:5px'
											}]
								}],
								emptyText : 'No Matching Records',
								listeners : {
									cellclick : function(dbcell, td, cell, record, tr, row, e) {
										var clickedDataIndex = dbcell.panel.headerCt.getHeaderAtIndex(cell).dataIndex;
										// console.log(dbcell.panel.headerCt.getHeaderAtIndex(cell))
										var clickedColumnName = dbcell.panel.headerCt.getHeaderAtIndex(cell).text;
										var clickedCellValue = record.get(clickedDataIndex);
										// console.log(clickedColumnName)
										if (clickedColumnName == 'Accession') {
											ucsc_plot(dbcell, td, cell, record, tr, row, e)
										} else if (clickedColumnName == 'Coverage') {
											console.log(record)
											accession = record.get('accession')
											expName = record.get('exp_name')
											var win = Ext.create('Ext.Window', {
														width : 650,
														height : 200,
														hidden : false,
														autoScroll : true,
														maximizable : true,
														title : 'Protein Coverage of ' + accession,
														// animateTarget :
														// 'mevennplot',
														layout : 'fit',
														html : '<div align="center"><img src=/static/images/loading/loading5.gif height=300 weight=400 /></div>',
														listeners : {
															afterRender : function() {
																Ext.Ajax.request({
																			timeout : 600000,
																			url : '/gardener/coverage/',
																			method : 'GET',
																			params : {
																				accession : accession,
																				expName : expName
																			},
																			success : function(response) {
																				win.update(response.responseText);
																			},
																			failure : function() {
																				win.update("Sorry! Error happen, please contact Admin with current URL.");
																			}
																		});
															}
														}
													});
											win.show();
										}
									},
									'selectionchange' : function(view, records) {
										grid4.down('#ppi').setDisabled(!records.length)
									}
								},
								plugins : [Ext.create('Ext.grid.plugin.CellEditing', {
													clicksToEdit : 1,
													listeners : {
														edit : function(editor, e) {
															// commit the changes
															// right after
															// editing finished
															// console.log(e)
															console.log(grid4)
															var sym = grid4.getStore().getAt(e.rowIdx).get('symbol')
															if (!sym || sym == '-') {
																Ext.Msg.alert('Error', 'Symbol error')
																return
															}
															Ext.Ajax.request({
																		timeout : 600000,
																		url : '/gardener/userAnnotation/',
																		method : 'POST',
																		params : {
																			exp : Ext.getCmp('content-panel').activeTab.title.split('of ')[1],
																			symbol : sym,
																			annotation : e.value
																		}
																	});
														}
													}
												}), {
											ptype : 'rowexpander',
											selectRowOnExpand : true,
											expandOnDblClick : true,
											rowBodyTpl : ['<div id="Exp-Peptide-' + timestamp + '{id}" ></div>'],
											toggleRow : function(rowIdx, record) {
												var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
														.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view
														.getRecord(rowNode), grid4 = this.getCmp(), id = record.get('id'), targetId = 'Exp-Peptide-'
														+ timestamp + id, accession = record.get('accession'), search_id = record.get('search_id'), num_peptides = record
														.get('num_peptides');
												if (row.hasCls(this.rowCollapsedCls)) {
													row.removeCls(this.rowCollapsedCls);
													this.recordsExpanded[record.internalId] = true;
													this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
													if (rowNode.grid4) {
														nextBd.removeCls(hiddenCls);
														rowNode.grid4.doComponentLayout();
													} else {
														Ext.create('Ext.data.Store', {
																	model : 'gar.model.Peptide',
																	pageSize : 100,
																	buffered : true,
																	// leadingBufferZone
																	// :
																	// 300,
																	autoLoad : true,
																	proxy : {
																		type : 'ajax',
																		url : '/gardener/data/showpeptide/',
																		extraParams : {
																			sid : id,
																			accession : accession,
																			search_id : search_id,
																			stype : 'protein'
																		},
																		reader : {
																			type : 'json',
																			root : 'data',
																			totalProperty : 'total'
																		}
																	},
																	autoLoad : {
																		callback : function() {
																			nextBd.removeCls(hiddenCls);
																			// console.log(num_peptides);
																			var h = 100 + num_peptides * 20;
																			if (h > 400) {
																				h = 400
																			}
																			Ext.create('gar.view.Peptide', {
																						border : true,
																						height : h, // Redefine
																						// view
																						// of
																						// pep
																						renderTo : targetId,
																						store : this,
																						row : row,
																						layout : 'fit',
																						listeners : {
																							cellclick : peptide_sum_plot
																						}
																					});
																			rowNode.grid = grid4;
																			// grid.suspendEvents();
																		}
																	},
																	listeners : {
																		beforeload : function() {
																			exploadMask.show();
																		},
																		load : function() {
																			exploadMask.hide();
																		}
																	}
																});
													}
												} else {
													row.addCls(this.rowCollapsedCls);
													nextBd.addCls(this.rowBodyHiddenCls);
													this.recordsExpanded[record.internalId] = false;
													this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
												}
											}
										}]
							})
							var silacTabpanel = Ext.create('Ext.tab.Panel', {
							    // layout: 'fit',
							    tabPosition: 'right'
							});
							c.add({
								title : 'Protein of ' + record.data.name,
								// iconCls :
								// 'tabs',
								closable : true,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [silacTabpanel]
							}).show()
							silacTabpanel.add({
								title : 'Mix',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid]
							}).show()
							silacTabpanel.add({
								title : 'Light',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid2]
							})
							silacTabpanel.add({
								title : 'Heavy',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid3]
							})
							silacTabpanel.add({
								title : 'Compare',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid4]
							})
							silacTabpanel.setActiveTab(silacTabpanel.items.items[0])
						}else{
							c.add({
								title : 'Protein of ' + record.data.name,
								// iconCls :
								// 'tabs',
								closable : true,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid]
							}).show()
						}
					} else if (clickedColumnName == "Peptide Num" && cellIndex > 0) {
						if (record.get('num_peptide') == 0) {
							Ext.Msg.alert('Warning', 'No Peptide found.')
							return
						}
						var filters = {
							ftype : 'filters',
							encode : true
						}
						function onStoreSizeChange() {
							grid.down('#status').update({
										count : tstore.getTotalCount()
									});
						}
						var tstore = Ext.create('gar.store.Peptide', {
									listeners : {
										totalcountchange : onStoreSizeChange
									}
								});
						tstore.getProxy().extraParams = {
							sid : record.data.id,
							stype : 'exper'
						};
						Ext.getCmp('info_protein_tab_index').value += 1
						var grid = Ext.create('gar.view.Peptide', {
							// id :
							// 'protein_tab_'+
							// Ext.getCmp('info_protein_tab_index').value,
							store : tstore,
							features : [filters],
							dockedItems : [{
										dock : 'top',
										xtype : 'toolbar',
										items : [{
													text : 'Clear Filter Data',
													handler : function() {
														grid.filters.clearFilters();
													}
												}, {
													text : 'All Filter Data',
													tooltip : 'Get Filter Data for Grid',
													handler : function() {
														var filterData = grid.filters.getFilterData()
														var filtersStore = Ext.create('Ext.data.Store', {
														    fields:['field', 'type', 'value'],
														    data:[]
														});

														for( var i = 0; i < filterData.length; i++)
														{
															var field, type, value
															field = filterData[i].field
															switch(filterData[i].data.type)
															{
																case 'string':
																	type = 'has string'
																	value = filterData[i].data.value
																	filtersStore.add({ 'field': field, "type": type, "value": value })
																	break
																case 'numeric':
																	switch(filterData[i].data.comparison.slice(0,2))
																	{
																		case 'gt':
																			type = 'is bigger than'
																			break
																		case 'lt':
																			type = 'is little than'
																			break
																		case 'eq':
																			type = 'equals to'
																			break
																		default:
																			type = 'null'
																	}
																	value = filterData[i].data.value
																	filtersStore.add({ 'field': field, "type": type, "value": value })
																	break
																default: 
																	type = 'null'
															}
														}

														var filterWindow = Ext.create(Ext.window.Window,{
															title: 'All filter data',
															height: 300,
															width: 500,
															modal: true,
															animateTarget: this,
															layout: 'fit',
															autoShow: true,
															items: [{
																xtype: 'grid',
																hideHeaders: true,
																columns: [
															        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
															        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
															        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
															    ],
															    store: filtersStore
															}]
														})
													}
												}, '->', {
													xtype : 'component',
													itemId : 'status',
													tpl : 'Matching Peptides: {count}',
													style : 'margin-right:5px'
												}]
									}],
							emptyText : 'No Matching Records',
							plugins : [{
								ptype : 'rowexpander',
								selectRowOnExpand : true,
								expandOnDblClick : true,
								rowBodyTpl : ['<div id="Sear-Peptide-' + timestamp + '{id}" ></div>'],
								toggleRow : function(rowIdx, record) {
									var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
											.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view.getRecord(rowNode), grid = this
											.getCmp(), id = record.get('id'), targetId = 'Sear-Peptide-' + timestamp + id, protein_group_accessions = record
											.get('protein_group_accessions'), search_id = record.get('search_id');
									if (row.hasCls(this.rowCollapsedCls)) {
										row.removeCls(this.rowCollapsedCls);
										this.recordsExpanded[record.internalId] = true;
										this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
										if (rowNode.grid) {
											nextBd.removeCls(hiddenCls);
											rowNode.grid.doComponentLayout();
										} else {
											Ext.create('Ext.data.Store', {
														model : 'gar.model.Protein',
														pageSize : 100,
														autoLoad : true,
														proxy : {
															type : 'ajax',
															url : '/gardener/data/showprotein/',
															extraParams : {
																sid : id,
																stype : 'peptide',
																protein_group_accessions : protein_group_accessions,
																search_id : search_id
															},
															reader : {
																type : 'json',
																root : 'data',
																totalProperty : 'total'
															}
														},
														autoLoad : {
															callback : function() {
																nextBd.removeCls(hiddenCls);
																Ext.create('gar.view.Protein', {
																			renderTo : targetId,
																			store : this,
																			row : row,
																			height : 100
																		});
																rowNode.grid = grid;
																// grid.suspendEvents();
															}
														},
														listeners : {
															beforeload : function() {
																exploadMask.show();
															},
															load : function() {
																exploadMask.hide();
															}
														}
													});
										}
									} else {
										row.addCls(this.rowCollapsedCls);
										nextBd.addCls(this.rowBodyHiddenCls);
										this.recordsExpanded[record.internalId] = false;
										this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
									}
								}
							}],
							listeners : {
								cellclick : peptide_sum_plot
							}
						})
						c = Ext.getCmp('content-panel')
						Ext.getCmp('info_tab_index').value += 1
						if(record.data.name == 'Exp007004'){
							var filters2 = {
								ftype : 'filters',
								encode : true
							}
							function onStoreSizeChange2() {
								grid2.down('#status').update({
											count : tstore2.getTotalCount()
										});
							}
							var tstore2 = Ext.create('gar.store.Peptide', {
										listeners : {
											totalcountchange : onStoreSizeChange2
										}
									});
							tstore2.getProxy().url = '/gardener/data/silacpeptide/'
							tstore2.getProxy().extraParams = {
								stype : 'exper',
								label: 'light',
								exp_name: record.data.name
							};
							var grid2 = Ext.create('gar.view.Peptide', {
								// id :
								// 'protein_tab_'+
								// Ext.getCmp('info_protein_tab_index').value,
								store : tstore2,
								features : [filters2],
								dockedItems : [{
											dock : 'top',
											xtype : 'toolbar',
											items : [{
														text : 'Clear Filter Data',
														handler : function() {
															grid2.filters.clearFilters();
														}
													}, {
														text : 'All Filter Data',
														tooltip : 'Get Filter Data for Grid',
														handler : function() {
															var filterData = grid2.filters.getFilterData()
															var filtersStore = Ext.create('Ext.data.Store', {
															    fields:['field', 'type', 'value'],
															    data:[]
															});

															for( var i = 0; i < filterData.length; i++)
															{
																var field, type, value
																field = filterData[i].field
																switch(filterData[i].data.type)
																{
																	case 'string':
																		type = 'has string'
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	case 'numeric':
																		switch(filterData[i].data.comparison.slice(0,2))
																		{
																			case 'gt':
																				type = 'is bigger than'
																				break
																			case 'lt':
																				type = 'is little than'
																				break
																			case 'eq':
																				type = 'equals to'
																				break
																			default:
																				type = 'null'
																		}
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	default: 
																		type = 'null'
																}
															}

															var filterWindow = Ext.create(Ext.window.Window,{
																title: 'All filter data',
																height: 300,
																width: 500,
																modal: true,
																animateTarget: this,
																layout: 'fit',
																autoShow: true,
																items: [{
																	xtype: 'grid',
																	hideHeaders: true,
																	columns: [
																        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
																        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
																        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
																    ],
																    store: filtersStore
																}]
															})
														}
													}, '->', {
														xtype : 'component',
														itemId : 'status',
														tpl : 'Matching Peptides: {count}',
														style : 'margin-right:5px'
													}]
										}],
								emptyText : 'No Matching Records',
								plugins : [{
									ptype : 'rowexpander',
									selectRowOnExpand : true,
									expandOnDblClick : true,
									rowBodyTpl : ['<div id="Sear-Peptide-' + timestamp + '{id}" ></div>'],
									toggleRow : function(rowIdx, record) {
										var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
												.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view.getRecord(rowNode), grid = this
												.getCmp(), id = record.get('id'), targetId = 'Sear-Peptide-' + timestamp + id, protein_group_accessions = record
												.get('protein_group_accessions'), search_id = record.get('search_id');
										if (row.hasCls(this.rowCollapsedCls)) {
											row.removeCls(this.rowCollapsedCls);
											this.recordsExpanded[record.internalId] = true;
											this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
											if (rowNode.grid) {
												nextBd.removeCls(hiddenCls);
												rowNode.grid.doComponentLayout();
											} else {
												Ext.create('Ext.data.Store', {
															model : 'gar.model.Protein',
															pageSize : 100,
															autoLoad : true,
															proxy : {
																type : 'ajax',
																url : '/gardener/data/showprotein/',
																extraParams : {
																	sid : id,
																	stype : 'peptide',
																	protein_group_accessions : protein_group_accessions,
																	search_id : search_id
																},
																reader : {
																	type : 'json',
																	root : 'data',
																	totalProperty : 'total'
																}
															},
															autoLoad : {
																callback : function() {
																	nextBd.removeCls(hiddenCls);
																	Ext.create('gar.view.Protein', {
																				renderTo : targetId,
																				store : this,
																				row : row,
																				height : 100
																			});
																	rowNode.grid = grid2;
																	// grid.suspendEvents();
																}
															},
															listeners : {
																beforeload : function() {
																	exploadMask.show();
																},
																load : function() {
																	exploadMask.hide();
																}
															}
														});
											}
										} else {
											row.addCls(this.rowCollapsedCls);
											nextBd.addCls(this.rowBodyHiddenCls);
											this.recordsExpanded[record.internalId] = false;
											this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
										}
									}
								}],
								listeners : {
									cellclick : peptide_sum_plot
								}
							})
							var filters3 = {
								ftype : 'filters',
								encode : true
							}
							function onStoreSizeChange3() {
								grid3.down('#status').update({
											count : tstore3.getTotalCount()
										});
							}
							var tstore3 = Ext.create('gar.store.Peptide', {
										listeners : {
											totalcountchange : onStoreSizeChange3
										}
									});
							tstore3.getProxy().url = '/gardener/data/silacpeptide/'
							tstore3.getProxy().extraParams = {
								stype : 'exper',
								label: 'heavy',
								exp_name: record.data.name
							};
							var grid3 = Ext.create('gar.view.Peptide', {
								// id :
								// 'protein_tab_'+
								// Ext.getCmp('info_protein_tab_index').value,
								store : tstore3,
								features : [filters3],
								dockedItems : [{
											dock : 'top',
											xtype : 'toolbar',
											items : [{
														text : 'Clear Filter Data',
														handler : function() {
															grid3.filters.clearFilters();
														}
													}, {
														text : 'All Filter Data',
														tooltip : 'Get Filter Data for Grid',
														handler : function() {
															var filterData = grid3.filters.getFilterData()
															var filtersStore = Ext.create('Ext.data.Store', {
															    fields:['field', 'type', 'value'],
															    data:[]
															});

															for( var i = 0; i < filterData.length; i++)
															{
																var field, type, value
																field = filterData[i].field
																switch(filterData[i].data.type)
																{
																	case 'string':
																		type = 'has string'
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	case 'numeric':
																		switch(filterData[i].data.comparison.slice(0,2))
																		{
																			case 'gt':
																				type = 'is bigger than'
																				break
																			case 'lt':
																				type = 'is little than'
																				break
																			case 'eq':
																				type = 'equals to'
																				break
																			default:
																				type = 'null'
																		}
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	default: 
																		type = 'null'
																}
															}

															var filterWindow = Ext.create(Ext.window.Window,{
																title: 'All filter data',
																height: 300,
																width: 500,
																modal: true,
																animateTarget: this,
																layout: 'fit',
																autoShow: true,
																items: [{
																	xtype: 'grid',
																	hideHeaders: true,
																	columns: [
																        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
																        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
																        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
																    ],
																    store: filtersStore
																}]
															})
														}
													}, '->', {
														xtype : 'component',
														itemId : 'status',
														tpl : 'Matching Peptides: {count}',
														style : 'margin-right:5px'
													}]
										}],
								emptyText : 'No Matching Records',
								plugins : [{
									ptype : 'rowexpander',
									selectRowOnExpand : true,
									expandOnDblClick : true,
									rowBodyTpl : ['<div id="Sear-Peptide-' + timestamp + '{id}" ></div>'],
									toggleRow : function(rowIdx, record) {
										var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
												.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view.getRecord(rowNode), grid = this
												.getCmp(), id = record.get('id'), targetId = 'Sear-Peptide-' + timestamp + id, protein_group_accessions = record
												.get('protein_group_accessions'), search_id = record.get('search_id');
										if (row.hasCls(this.rowCollapsedCls)) {
											row.removeCls(this.rowCollapsedCls);
											this.recordsExpanded[record.internalId] = true;
											this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
											if (rowNode.grid) {
												nextBd.removeCls(hiddenCls);
												rowNode.grid.doComponentLayout();
											} else {
												Ext.create('Ext.data.Store', {
															model : 'gar.model.Protein',
															pageSize : 100,
															autoLoad : true,
															proxy : {
																type : 'ajax',
																url : '/gardener/data/showprotein/',
																extraParams : {
																	sid : id,
																	stype : 'peptide',
																	protein_group_accessions : protein_group_accessions,
																	search_id : search_id
																},
																reader : {
																	type : 'json',
																	root : 'data',
																	totalProperty : 'total'
																}
															},
															autoLoad : {
																callback : function() {
																	nextBd.removeCls(hiddenCls);
																	Ext.create('gar.view.Protein', {
																				renderTo : targetId,
																				store : this,
																				row : row,
																				height : 100
																			});
																	rowNode.grid = grid3;
																	// grid.suspendEvents();
																}
															},
															listeners : {
																beforeload : function() {
																	exploadMask.show();
																},
																load : function() {
																	exploadMask.hide();
																}
															}
														});
											}
										} else {
											row.addCls(this.rowCollapsedCls);
											nextBd.addCls(this.rowBodyHiddenCls);
											this.recordsExpanded[record.internalId] = false;
											this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
										}
									}
								}],
								listeners : {
									cellclick : peptide_sum_plot
								}
							})
							var silacTabpanel = Ext.create('Ext.tab.Panel', {
							    // layout: 'fit',
							    tabPosition: 'right'
							});
							c.add({
								title : 'Peptide of ' + record.data.name,
								// iconCls :
								// 'tabs',
								closable : true,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [silacTabpanel]
							}).show()
							silacTabpanel.add({
								title : 'Mix',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid]
							}).show()
							silacTabpanel.add({
								title : 'Light',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid2]
							})
							silacTabpanel.add({
								title : 'Heavy',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid3]
							})
							silacTabpanel.setActiveTab(silacTabpanel.items.items[0])
						}else if(record.data.name == 'Exp007407'){
							var filters2 = {
								ftype : 'filters',
								encode : true
							}
							function onStoreSizeChange2() {
								grid2.down('#status').update({
											count : tstore2.getTotalCount()
										});
							}
							var tstore2 = Ext.create('gar.store.Peptide', {
										listeners : {
											totalcountchange : onStoreSizeChange2
										}
									});
							tstore2.getProxy().url = '/gardener/data/silacpeptide/'
							tstore2.getProxy().extraParams = {
								stype : 'exper',
								label: 'light',
								exp_name: record.data.name
							};
							var grid2 = Ext.create('gar.view.Peptide', {
								// id :
								// 'protein_tab_'+
								// Ext.getCmp('info_protein_tab_index').value,
								store : tstore2,
								features : [filters2],
								dockedItems : [{
											dock : 'top',
											xtype : 'toolbar',
											items : [{
														text : 'Clear Filter Data',
														handler : function() {
															grid2.filters.clearFilters();
														}
													}, {
														text : 'All Filter Data',
														tooltip : 'Get Filter Data for Grid',
														handler : function() {
															var filterData = grid2.filters.getFilterData()
															var filtersStore = Ext.create('Ext.data.Store', {
															    fields:['field', 'type', 'value'],
															    data:[]
															});

															for( var i = 0; i < filterData.length; i++)
															{
																var field, type, value
																field = filterData[i].field
																switch(filterData[i].data.type)
																{
																	case 'string':
																		type = 'has string'
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	case 'numeric':
																		switch(filterData[i].data.comparison.slice(0,2))
																		{
																			case 'gt':
																				type = 'is bigger than'
																				break
																			case 'lt':
																				type = 'is little than'
																				break
																			case 'eq':
																				type = 'equals to'
																				break
																			default:
																				type = 'null'
																		}
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	default: 
																		type = 'null'
																}
															}

															var filterWindow = Ext.create(Ext.window.Window,{
																title: 'All filter data',
																height: 300,
																width: 500,
																modal: true,
																animateTarget: this,
																layout: 'fit',
																autoShow: true,
																items: [{
																	xtype: 'grid',
																	hideHeaders: true,
																	columns: [
																        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
																        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
																        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
																    ],
																    store: filtersStore
																}]
															})
														}
													}, '->', {
														xtype : 'component',
														itemId : 'status',
														tpl : 'Matching Peptides: {count}',
														style : 'margin-right:5px'
													}]
										}],
								emptyText : 'No Matching Records',
								plugins : [{
									ptype : 'rowexpander',
									selectRowOnExpand : true,
									expandOnDblClick : true,
									rowBodyTpl : ['<div id="Sear-Peptide-' + timestamp + '{id}" ></div>'],
									toggleRow : function(rowIdx, record) {
										var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
												.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view.getRecord(rowNode), grid = this
												.getCmp(), id = record.get('id'), targetId = 'Sear-Peptide-' + timestamp + id, protein_group_accessions = record
												.get('protein_group_accessions'), search_id = record.get('search_id');
										if (row.hasCls(this.rowCollapsedCls)) {
											row.removeCls(this.rowCollapsedCls);
											this.recordsExpanded[record.internalId] = true;
											this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
											if (rowNode.grid) {
												nextBd.removeCls(hiddenCls);
												rowNode.grid.doComponentLayout();
											} else {
												Ext.create('Ext.data.Store', {
															model : 'gar.model.Protein',
															pageSize : 100,
															autoLoad : true,
															proxy : {
																type : 'ajax',
																url : '/gardener/data/showprotein/',
																extraParams : {
																	sid : id,
																	stype : 'peptide',
																	protein_group_accessions : protein_group_accessions,
																	search_id : search_id
																},
																reader : {
																	type : 'json',
																	root : 'data',
																	totalProperty : 'total'
																}
															},
															autoLoad : {
																callback : function() {
																	nextBd.removeCls(hiddenCls);
																	Ext.create('gar.view.Protein', {
																				renderTo : targetId,
																				store : this,
																				row : row,
																				height : 100
																			});
																	rowNode.grid = grid2;
																	// grid.suspendEvents();
																}
															},
															listeners : {
																beforeload : function() {
																	exploadMask.show();
																},
																load : function() {
																	exploadMask.hide();
																}
															}
														});
											}
										} else {
											row.addCls(this.rowCollapsedCls);
											nextBd.addCls(this.rowBodyHiddenCls);
											this.recordsExpanded[record.internalId] = false;
											this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
										}
									}
								}],
								listeners : {
									cellclick : peptide_sum_plot
								}
							})
							var filters3 = {
								ftype : 'filters',
								encode : true
							}
							function onStoreSizeChange3() {
								grid3.down('#status').update({
											count : tstore3.getTotalCount()
										});
							}
							var tstore3 = Ext.create('gar.store.Peptide', {
										listeners : {
											totalcountchange : onStoreSizeChange3
										}
									});
							tstore3.getProxy().url = '/gardener/data/silacpeptide/'
							tstore3.getProxy().extraParams = {
								stype : 'exper',
								label: 'heavy',
								exp_name: record.data.name
							};
							var grid3 = Ext.create('gar.view.Peptide', {
								// id :
								// 'protein_tab_'+
								// Ext.getCmp('info_protein_tab_index').value,
								store : tstore3,
								features : [filters3],
								dockedItems : [{
											dock : 'top',
											xtype : 'toolbar',
											items : [{
														text : 'Clear Filter Data',
														handler : function() {
															grid3.filters.clearFilters();
														}
													}, {
														text : 'All Filter Data',
														tooltip : 'Get Filter Data for Grid',
														handler : function() {
															var filterData = grid3.filters.getFilterData()
															var filtersStore = Ext.create('Ext.data.Store', {
															    fields:['field', 'type', 'value'],
															    data:[]
															});

															for( var i = 0; i < filterData.length; i++)
															{
																var field, type, value
																field = filterData[i].field
																switch(filterData[i].data.type)
																{
																	case 'string':
																		type = 'has string'
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	case 'numeric':
																		switch(filterData[i].data.comparison.slice(0,2))
																		{
																			case 'gt':
																				type = 'is bigger than'
																				break
																			case 'lt':
																				type = 'is little than'
																				break
																			case 'eq':
																				type = 'equals to'
																				break
																			default:
																				type = 'null'
																		}
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	default: 
																		type = 'null'
																}
															}

															var filterWindow = Ext.create(Ext.window.Window,{
																title: 'All filter data',
																height: 300,
																width: 500,
																modal: true,
																animateTarget: this,
																layout: 'fit',
																autoShow: true,
																items: [{
																	xtype: 'grid',
																	hideHeaders: true,
																	columns: [
																        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
																        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
																        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
																    ],
																    store: filtersStore
																}]
															})
														}
													}, '->', {
														xtype : 'component',
														itemId : 'status',
														tpl : 'Matching Peptides: {count}',
														style : 'margin-right:5px'
													}]
										}],
								emptyText : 'No Matching Records',
								plugins : [{
									ptype : 'rowexpander',
									selectRowOnExpand : true,
									expandOnDblClick : true,
									rowBodyTpl : ['<div id="Sear-Peptide-' + timestamp + '{id}" ></div>'],
									toggleRow : function(rowIdx, record) {
										var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
												.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view.getRecord(rowNode), grid = this
												.getCmp(), id = record.get('id'), targetId = 'Sear-Peptide-' + timestamp + id, protein_group_accessions = record
												.get('protein_group_accessions'), search_id = record.get('search_id');
										if (row.hasCls(this.rowCollapsedCls)) {
											row.removeCls(this.rowCollapsedCls);
											this.recordsExpanded[record.internalId] = true;
											this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
											if (rowNode.grid) {
												nextBd.removeCls(hiddenCls);
												rowNode.grid.doComponentLayout();
											} else {
												Ext.create('Ext.data.Store', {
															model : 'gar.model.Protein',
															pageSize : 100,
															autoLoad : true,
															proxy : {
																type : 'ajax',
																url : '/gardener/data/showprotein/',
																extraParams : {
																	sid : id,
																	stype : 'peptide',
																	protein_group_accessions : protein_group_accessions,
																	search_id : search_id
																},
																reader : {
																	type : 'json',
																	root : 'data',
																	totalProperty : 'total'
																}
															},
															autoLoad : {
																callback : function() {
																	nextBd.removeCls(hiddenCls);
																	Ext.create('gar.view.Protein', {
																				renderTo : targetId,
																				store : this,
																				row : row,
																				height : 100
																			});
																	rowNode.grid = grid3;
																	// grid.suspendEvents();
																}
															},
															listeners : {
																beforeload : function() {
																	exploadMask.show();
																},
																load : function() {
																	exploadMask.hide();
																}
															}
														});
											}
										} else {
											row.addCls(this.rowCollapsedCls);
											nextBd.addCls(this.rowBodyHiddenCls);
											this.recordsExpanded[record.internalId] = false;
											this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
										}
									}
								}],
								listeners : {
									cellclick : peptide_sum_plot
								}
							})
							var silacTabpanel = Ext.create('Ext.tab.Panel', {
							    // layout: 'fit',
							    tabPosition: 'right'
							});
							c.add({
								title : 'Peptide of ' + record.data.name,
								// iconCls :
								// 'tabs',
								closable : true,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [silacTabpanel]
							}).show()
							silacTabpanel.add({
								title : 'Mascot',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid]
							}).show()
							silacTabpanel.add({
								title : 'X!Tandem',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid2]
							})
							silacTabpanel.add({
								title : 'interProphet',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid3]
							})
							silacTabpanel.setActiveTab(silacTabpanel.items.items[0])
						}else if(record.data.name == 'Exp007522'){
							var filters2 = {
								ftype : 'filters',
								encode : true
							}
							function onStoreSizeChange2() {
								grid2.down('#status').update({
											count : tstore2.getTotalCount()
										});
							}
							var tstore2 = Ext.create('gar.store.Peptide', {
										listeners : {
											totalcountchange : onStoreSizeChange2
										}
									});
							tstore2.getProxy().url = '/gardener/data/silacpeptide/'
							tstore2.getProxy().extraParams = {
								stype : 'exper',
								label: 'light',
								exp_name: record.data.name
							};
							var grid2 = Ext.create('gar.view.Peptide', {
								// id :
								// 'protein_tab_'+
								// Ext.getCmp('info_protein_tab_index').value,
								store : tstore2,
								features : [filters2],
								dockedItems : [{
											dock : 'top',
											xtype : 'toolbar',
											items : [{
														text : 'Clear Filter Data',
														handler : function() {
															grid2.filters.clearFilters();
														}
													}, {
														text : 'All Filter Data',
														tooltip : 'Get Filter Data for Grid',
														handler : function() {
															var filterData = grid2.filters.getFilterData()
															var filtersStore = Ext.create('Ext.data.Store', {
															    fields:['field', 'type', 'value'],
															    data:[]
															});

															for( var i = 0; i < filterData.length; i++)
															{
																var field, type, value
																field = filterData[i].field
																switch(filterData[i].data.type)
																{
																	case 'string':
																		type = 'has string'
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	case 'numeric':
																		switch(filterData[i].data.comparison.slice(0,2))
																		{
																			case 'gt':
																				type = 'is bigger than'
																				break
																			case 'lt':
																				type = 'is little than'
																				break
																			case 'eq':
																				type = 'equals to'
																				break
																			default:
																				type = 'null'
																		}
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	default: 
																		type = 'null'
																}
															}

															var filterWindow = Ext.create(Ext.window.Window,{
																title: 'All filter data',
																height: 300,
																width: 500,
																modal: true,
																animateTarget: this,
																layout: 'fit',
																autoShow: true,
																items: [{
																	xtype: 'grid',
																	hideHeaders: true,
																	columns: [
																        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
																        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
																        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
																    ],
																    store: filtersStore
																}]
															})
														}
													}, '->', {
														xtype : 'component',
														itemId : 'status',
														tpl : 'Matching Peptides: {count}',
														style : 'margin-right:5px'
													}]
										}],
								emptyText : 'No Matching Records',
								plugins : [{
									ptype : 'rowexpander',
									selectRowOnExpand : true,
									expandOnDblClick : true,
									rowBodyTpl : ['<div id="Sear-Peptide-' + timestamp + '{id}" ></div>'],
									toggleRow : function(rowIdx, record) {
										var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
												.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view.getRecord(rowNode), grid = this
												.getCmp(), id = record.get('id'), targetId = 'Sear-Peptide-' + timestamp + id, protein_group_accessions = record
												.get('protein_group_accessions'), search_id = record.get('search_id');
										if (row.hasCls(this.rowCollapsedCls)) {
											row.removeCls(this.rowCollapsedCls);
											this.recordsExpanded[record.internalId] = true;
											this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
											if (rowNode.grid) {
												nextBd.removeCls(hiddenCls);
												rowNode.grid.doComponentLayout();
											} else {
												Ext.create('Ext.data.Store', {
															model : 'gar.model.Protein',
															pageSize : 100,
															autoLoad : true,
															proxy : {
																type : 'ajax',
																url : '/gardener/data/showprotein/',
																extraParams : {
																	sid : id,
																	stype : 'peptide',
																	protein_group_accessions : protein_group_accessions,
																	search_id : search_id
																},
																reader : {
																	type : 'json',
																	root : 'data',
																	totalProperty : 'total'
																}
															},
															autoLoad : {
																callback : function() {
																	nextBd.removeCls(hiddenCls);
																	Ext.create('gar.view.Protein', {
																				renderTo : targetId,
																				store : this,
																				row : row,
																				height : 100
																			});
																	rowNode.grid = grid2;
																	// grid.suspendEvents();
																}
															},
															listeners : {
																beforeload : function() {
																	exploadMask.show();
																},
																load : function() {
																	exploadMask.hide();
																}
															}
														});
											}
										} else {
											row.addCls(this.rowCollapsedCls);
											nextBd.addCls(this.rowBodyHiddenCls);
											this.recordsExpanded[record.internalId] = false;
											this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
										}
									}
								}],
								listeners : {
									cellclick : peptide_sum_plot
								}
							})
							var filters3 = {
								ftype : 'filters',
								encode : true
							}
							function onStoreSizeChange3() {
								grid3.down('#status').update({
											count : tstore3.getTotalCount()
										});
							}
							var tstore3 = Ext.create('gar.store.Peptide', {
										listeners : {
											totalcountchange : onStoreSizeChange3
										}
									});
							tstore3.getProxy().url = '/gardener/data/silacpeptide/'
							tstore3.getProxy().extraParams = {
								stype : 'exper',
								label: 'heavy',
								exp_name: record.data.name
							};
							var grid3 = Ext.create('gar.view.Peptide', {
								// id :
								// 'protein_tab_'+
								// Ext.getCmp('info_protein_tab_index').value,
								store : tstore3,
								features : [filters3],
								dockedItems : [{
											dock : 'top',
											xtype : 'toolbar',
											items : [{
														text : 'Clear Filter Data',
														handler : function() {
															grid3.filters.clearFilters();
														}
													}, {
														text : 'All Filter Data',
														tooltip : 'Get Filter Data for Grid',
														handler : function() {
															var filterData = grid3.filters.getFilterData()
															var filtersStore = Ext.create('Ext.data.Store', {
															    fields:['field', 'type', 'value'],
															    data:[]
															});

															for( var i = 0; i < filterData.length; i++)
															{
																var field, type, value
																field = filterData[i].field
																switch(filterData[i].data.type)
																{
																	case 'string':
																		type = 'has string'
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	case 'numeric':
																		switch(filterData[i].data.comparison.slice(0,2))
																		{
																			case 'gt':
																				type = 'is bigger than'
																				break
																			case 'lt':
																				type = 'is little than'
																				break
																			case 'eq':
																				type = 'equals to'
																				break
																			default:
																				type = 'null'
																		}
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	default: 
																		type = 'null'
																}
															}

															var filterWindow = Ext.create(Ext.window.Window,{
																title: 'All filter data',
																height: 300,
																width: 500,
																modal: true,
																animateTarget: this,
																layout: 'fit',
																autoShow: true,
																items: [{
																	xtype: 'grid',
																	hideHeaders: true,
																	columns: [
																        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
																        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
																        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
																    ],
																    store: filtersStore
																}]
															})
														}
													}, '->', {
														xtype : 'component',
														itemId : 'status',
														tpl : 'Matching Peptides: {count}',
														style : 'margin-right:5px'
													}]
										}],
								emptyText : 'No Matching Records',
								plugins : [{
									ptype : 'rowexpander',
									selectRowOnExpand : true,
									expandOnDblClick : true,
									rowBodyTpl : ['<div id="Sear-Peptide-' + timestamp + '{id}" ></div>'],
									toggleRow : function(rowIdx, record) {
										var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
												.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view.getRecord(rowNode), grid = this
												.getCmp(), id = record.get('id'), targetId = 'Sear-Peptide-' + timestamp + id, protein_group_accessions = record
												.get('protein_group_accessions'), search_id = record.get('search_id');
										if (row.hasCls(this.rowCollapsedCls)) {
											row.removeCls(this.rowCollapsedCls);
											this.recordsExpanded[record.internalId] = true;
											this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
											if (rowNode.grid) {
												nextBd.removeCls(hiddenCls);
												rowNode.grid.doComponentLayout();
											} else {
												Ext.create('Ext.data.Store', {
															model : 'gar.model.Protein',
															pageSize : 100,
															autoLoad : true,
															proxy : {
																type : 'ajax',
																url : '/gardener/data/showprotein/',
																extraParams : {
																	sid : id,
																	stype : 'peptide',
																	protein_group_accessions : protein_group_accessions,
																	search_id : search_id
																},
																reader : {
																	type : 'json',
																	root : 'data',
																	totalProperty : 'total'
																}
															},
															autoLoad : {
																callback : function() {
																	nextBd.removeCls(hiddenCls);
																	Ext.create('gar.view.Protein', {
																				renderTo : targetId,
																				store : this,
																				row : row,
																				height : 100
																			});
																	rowNode.grid = grid3;
																	// grid.suspendEvents();
																}
															},
															listeners : {
																beforeload : function() {
																	exploadMask.show();
																},
																load : function() {
																	exploadMask.hide();
																}
															}
														});
											}
										} else {
											row.addCls(this.rowCollapsedCls);
											nextBd.addCls(this.rowBodyHiddenCls);
											this.recordsExpanded[record.internalId] = false;
											this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
										}
									}
								}],
								listeners : {
									cellclick : peptide_sum_plot
								}
							})
							var silacTabpanel = Ext.create('Ext.tab.Panel', {
							    // layout: 'fit',
							    tabPosition: 'right'
							});
							c.add({
								title : 'Peptide of ' + record.data.name,
								// iconCls :
								// 'tabs',
								closable : true,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [silacTabpanel]
							}).show()
							silacTabpanel.add({
								title : 'ID result',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid]
							}).show()
							silacTabpanel.add({
								title : 'Compare',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid2]
							})
							// silacTabpanel.add({
							// 	title : 'iProphet',
							// 	// iconCls :
							// 	// 'tabs',
							// 	closable : false,
							// 	// id :
							// 	// 'tab_'+
							// 	// Ext.getCmp('info_tab_index').value,
							// 	layout : 'fit',
							// 	items : [grid3]
							// })
							silacTabpanel.setActiveTab(silacTabpanel.items.items[0])
						}else{
							c.add({
									title : 'Peptide of ' + record.data.name,
									// iconCls :
									// 'tabs',
									closable : true,
									// id :
									// 'tab_'+
									// Ext.getCmp('info_tab_index').value,
									layout : 'fit',
									items : [grid]
								}).show()
						}
					} else if (clickedColumnName == "Gene Num" && cellIndex > 0) {
						if (record.get('num_gene') == 0) {
							Ext.Msg.alert('Warning', 'No Gene found.')
							return
						}
						var filters = {
							ftype : 'filters',
							encode : true
						}
						function onStoreSizeChange() {
							grid.down('#status').update({
										count : tstore.getTotalCount()
									});
						}
						var tstore = Ext.create('gar.store.Gene', {
									listeners : {
										totalcountchange : onStoreSizeChange
									}
								});
						tstore.getProxy().extraParams = {
							sid : record.data.id,
							stype : 'exper'
						};
						Ext.getCmp('info_protein_tab_index').value += 1
						var grid = Ext.create('gar.view.Gene', {
									// id :
									// 'protein_tab_'+
									// Ext.getCmp('info_protein_tab_index').value,
									store : tstore,
									features : [filters],
									dockedItems : [{
										dock : 'top',
										xtype : 'toolbar',
										items : [{
													text : 'Clear Filter Data',
													handler : function() {
														grid.filters.clearFilters();
													}
												}, {
													text : 'All Filter Data',
													tooltip : 'Get Filter Data for Grid',
													handler : function() {
														var annoList = {
															'co_1': 'Coreg',
															'ki_1': 'Kinase', 
															'li_1': 'Ligand', 
															're_1': 'Receptor', 
															'pmm_1':'Plasma Membrane(Mouse)', 
															'pmh_1':'Plasma Membrane(Human)',
															'tf_1': 'Transcription Factor'
														}
														var modiList = {
															'Acetyl_1': 'N-terminal Acetyltrasferases',
															'Methyl_1': 'Methylation',
															'GlyGly_1': 'Ubiquitination',
															'Biotin_1': 'Biotin',
															'PhosphoST_1': 'Phosphorylation-ST',
															'PhosphoY_1': 'Phosphorylation-Y'
														}
														var filterData = grid.filters.getFilterData()
														var filtersStore = Ext.create('Ext.data.Store', {
														    fields:['field', 'type', 'value'],
														    data:[]
														});

														for( var i = 0; i < filterData.length; i++)
														{
															var field, type, value
															field = filterData[i].field
															switch(filterData[i].data.type)
															{
																case 'string':
																	type = 'has string'
																	value = filterData[i].data.value
																	filtersStore.add({ 'field': field, "type": type, "value": value })
																	break
																case 'list':
																	type = 'has type'
																	for( var j = 0; j < filterData[i].data.value.length; j++)
																	{
																		value = filterData[i].data.value[j]
																		if(field == 'annotation')
																			filtersStore.add({ 'field': field, "type": type, "value": annoList[value] })
																		else if (field == 'modification')
																			filtersStore.add({ 'field': field, "type": type, "value": modiList[value] })
																	}
																	break
																case 'numeric':
																	switch(filterData[i].data.comparison.slice(0,2))
																	{
																		case 'gt':
																			type = 'is bigger than'
																			break
																		case 'lt':
																			type = 'is little than'
																			break
																		case 'eq':
																			type = 'equals to'
																			break
																		default:
																			type = 'null'
																	}
																	value = filterData[i].data.value
																	filtersStore.add({ 'field': field, "type": type, "value": value })
																	break
																default: 
																	type = 'null'
															}
														}

														var filterWindow = Ext.create(Ext.window.Window,{
															title: 'All filter data',
															height: 300,
															width: 500,
															modal: true,
															animateTarget: this,
															layout: 'fit',
															autoShow: true,
															items: [{
																xtype: 'grid',
																hideHeaders: true,
																columns: [
															        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
															        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
															        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
															    ],
															    store: filtersStore
															}]
														})
													}
												}, {
													iconCls : 'refresh',
													text : 'Refresh This Tab',
													tooltip : 'Update to Latest Progress',
													handler : function() {
														tstore.load()
													}
												}, {
													// iconCls:'refresh',
													text : 'Batch Annotation',
													tooltip : '',
													handler : function() {
														var tab = Ext.create('Ext.form.Panel', {
																	bodyPadding : 5,
																	width : 350,
																	url : '/gardener/batchAnnotation/',
																	layout : 'anchor',
																	defaults : {
																		anchor : '100%'
																	},
																	defaultType : 'textfield',
																	items : [{
																				xtype : 'textarea',
																				fieldLabel : 'Symbol List',
																				name : 'symbol',
																				height : 200,
																				allowBlank : false
																			}, {
																				fieldLabel : 'Annotation',
																				name : 'annotation',
																				allowBlank : false
																			}],
																	buttons : [{
																				text : 'Get Current Symbols',
																				handler : function() {
																					var btn = this
																					var exploadMask = new Ext.LoadMask(grid, {
																								msg : 'Loading.....'
																							});
																					exploadMask.show();
																					var data = grid.filters.getFilterData();
																					var s = '[';
																					for (i = 0; i < data.length; i++) {
																						s += '{'
																						temp = String(Ext.encode(data[i].data))
																						s += temp.substr(1, temp.length - 2)
																						s += ',"field":"'
																						s += String(data[i].field)
																						s += '"}'
																						if (i != data.length - 1)
																							s += ','
																					}
																					s += ']'
																					Ext.Ajax.request({
																								url : '/gardener/data/showgene/',
																								method : 'GET',
																								timeout : 600000,
																								params : {
																									sid : record.data.id,
																									stype : 'exper',
																									filter : s,
																									limit : -1
																								},
																								success : function(response) {
																									exploadMask.hide();
																									var text = response.responseText;
																									text = Ext.JSON.decode(text)
																									var data = text.data
																									var total = text.total
																									var tempstring = ''
																									for (var count = 0; count < total; count++) {
																										tempstring = tempstring + data[count].symbol
																												+ '\n'
																									}
																									btn.up('form').form.setValues({
																												symbol : tempstring
																											})
																								},
																								failure : function() {
																									exploadMask.hide();
																								}
																							});

																				}
																			}, {
																				text : 'Reset',
																				handler : function() {
																					this.up('form').getForm().reset();
																				}
																			}, {
																				text : 'Submit',
																				formBind : true,
																				handler : function() {
																					var form = this.up('form').getForm();
																					if (form.isValid()) {
																						// console.log('yes')
																						form.submit({
																									url : '/gardener/userAnnotation/',
																									params : {
																										exp : Ext.getCmp('content-panel').activeTab.title
																												.split('of ')[1],
																										batch : true
																									},
																									waitMsg : 'Adding Experiment......',
																									timeout : 300000,
																									success : function(form, action) {
																										Ext.Msg.alert('Success', action.result.msg);
																									},
																									failure : function(form, action) {
																										Ext.Msg.alert('Failed', action.result.msg);
																									}
																								});
																					}
																				}
																			}]
																});
														var win = new Ext.Window({
															draggable : {
																constrain : true,
																constrainTo : Ext.getBody()
															},
															// title :
															// 'Comparison
															// Search',
															// width : 500,
															resizable : false,
															// animateTarget :
															// 'newcompare',
															items : [tab]
																/*
																 * , bbar :
																 * ['->', { text :
																 * 'Yes',
																 * handler :
																 * submitForm }, {
																 * text : 'No',
																 * handler :
																 * function() {
																 * win.close() } }]
																 */
															})
														win.show()
													}
												}, '->', {
													xtype : 'component',
													itemId : 'status',
													tpl : 'Matching Genes: {count}',
													style : 'margin-right:5px'
												}]
									}],
									emptyText : 'No Matching Records',
									plugins : [Ext.create('Ext.grid.plugin.CellEditing', {
														clicksToEdit : 1,
														listeners : {
															edit : function(editor, e) {
																console.log(grid)
																var sym = grid.getStore().getAt(e.rowIdx).get('symbol')
																if (!sym || sym == '-') {
																	Ext.Msg.alert('Error', 'Symbol error')
																	return
																}
																Ext.Ajax.request({
																			timeout : 600000,
																			url : '/gardener/userAnnotation/',
																			method : 'POST',
																			params : {
																				exp : Ext.getCmp('content-panel').activeTab.title.split('of ')[1],
																				symbol : sym,
																				annotation : e.value
																			}
																		});
															}
														}
													}), {
												ptype : 'rowexpander',
												selectRowOnExpand : true,
												expandOnDblClick : true,
												rowBodyTpl : ['<div id="Sear-Peptide-' + timestamp + '{id}" ></div>'],
												toggleRow : function(rowIdx, record) {
													var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
															.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view
															.getRecord(rowNode), grid = this.getCmp(), id = record.get('id'), targetId = 'Sear-Peptide-'
															+ timestamp + id, symbol = record.get('symbol'), search_id = record.get('search_id');
													if (row.hasCls(this.rowCollapsedCls)) {
														row.removeCls(this.rowCollapsedCls);
														this.recordsExpanded[record.internalId] = true;
														this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
														if (rowNode.grid) {
															nextBd.removeCls(hiddenCls);
															rowNode.grid.doComponentLayout();
														} else {
															Ext.create('Ext.data.Store', {
																		model : 'gar.model.Peptide',
																		pageSize : 100,
																		autoLoad : true,
																		proxy : {
																			type : 'ajax',
																			url : '/gardener/data/showpeptide/',
																			extraParams : {
																				sid : id,
																				stype : 'gene',
																				symbol : symbol,
																				search_id : search_id
																			},
																			reader : {
																				type : 'json',
																				root : 'data',
																				totalProperty : 'total'
																			}
																		},
																		autoLoad : {
																			callback : function() {
																				nextBd.removeCls(hiddenCls);
																				Ext.create('gar.view.Peptide', {
																							renderTo : targetId,
																							store : this,
																							row : row,
																							height : 200,
																							listeners : {
																								cellclick : peptide_sum_plot
																							}
																						});
																				rowNode.grid = grid;
																				// grid.suspendEvents();
																			}
																		},
																		listeners : {
																			beforeload : function() {
																				exploadMask.show();
																			},
																			load : function() {
																				exploadMask.hide();
																			}
																		}
																	});
														}
													} else {
														row.addCls(this.rowCollapsedCls);
														nextBd.addCls(this.rowBodyHiddenCls);
														this.recordsExpanded[record.internalId] = false;
														this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
													}
												}
											}],
									listeners : {
						// cellclick
									// :
									// ucsc_plot
							}
						})
						c = Ext.getCmp('content-panel')
						Ext.getCmp('info_tab_index').value += 1
						if(record.data.name == 'Exp007004'){
							var filters2 = {
								ftype : 'filters',
								encode : true
							}
							function onStoreSizeChange2() {
								grid2.down('#status').update({
											count : tstore2.getTotalCount()
										});
							}
							var tstore2 = Ext.create('gar.store.Gene', {
										listeners : {
											totalcountchange : onStoreSizeChange2
										}
									});
							tstore2.getProxy().url = '/gardener/data/silacgene/'
							tstore2.getProxy().extraParams = {
								stype : 'exper',
								label: 'light',
								exp_name: record.data.name
							};
							var grid2 = Ext.create('gar.view.Gene', {
										// id :
										// 'protein_tab_'+
										// Ext.getCmp('info_protein_tab_index').value,
										store : tstore2,
										features : [filters2],
										dockedItems : [{
											dock : 'top',
											xtype : 'toolbar',
											items : [{
														text : 'Clear Filter Data',
														handler : function() {
															grid2.filters.clearFilters();
														}
													}, {
														text : 'All Filter Data',
														tooltip : 'Get Filter Data for Grid',
														handler : function() {
															var annoList = {
																'co_1': 'Coreg',
																'ki_1': 'Kinase', 
																'li_1': 'Ligand', 
																're_1': 'Receptor', 
																'pmm_1':'Plasma Membrane(Mouse)', 
																'pmh_1':'Plasma Membrane(Human)',
																'tf_1': 'Transcription Factor'
															}
															var modiList = {
																'Acetyl_1': 'N-terminal Acetyltrasferases',
																'Methyl_1': 'Methylation',
																'GlyGly_1': 'Ubiquitination',
																'Biotin_1': 'Biotin',
																'PhosphoST_1': 'Phosphorylation-ST',
																'PhosphoY_1': 'Phosphorylation-Y'
															}
															var filterData = grid2.filters.getFilterData()
															var filtersStore = Ext.create('Ext.data.Store', {
															    fields:['field', 'type', 'value'],
															    data:[]
															});

															for( var i = 0; i < filterData.length; i++)
															{
																var field, type, value
																field = filterData[i].field
																switch(filterData[i].data.type)
																{
																	case 'string':
																		type = 'has string'
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	case 'list':
																		type = 'has type'
																		for( var j = 0; j < filterData[i].data.value.length; j++)
																		{
																			value = filterData[i].data.value[j]
																			if(field == 'annotation')
																				filtersStore.add({ 'field': field, "type": type, "value": annoList[value] })
																			else if (field == 'modification')
																				filtersStore.add({ 'field': field, "type": type, "value": modiList[value] })
																		}
																		break
																	case 'numeric':
																		switch(filterData[i].data.comparison.slice(0,2))
																		{
																			case 'gt':
																				type = 'is bigger than'
																				break
																			case 'lt':
																				type = 'is little than'
																				break
																			case 'eq':
																				type = 'equals to'
																				break
																			default:
																				type = 'null'
																		}
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	default: 
																		type = 'null'
																}
															}

															var filterWindow = Ext.create(Ext.window.Window,{
																title: 'All filter data',
																height: 300,
																width: 500,
																modal: true,
																animateTarget: this,
																layout: 'fit',
																autoShow: true,
																items: [{
																	xtype: 'grid',
																	hideHeaders: true,
																	columns: [
																        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
																        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
																        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
																    ],
																    store: filtersStore
																}]
															})
														}
													}, {
														iconCls : 'refresh',
														text : 'Refresh This Tab',
														tooltip : 'Update to Latest Progress',
														handler : function() {
															tstore.load()
														}
													}, {
														// iconCls:'refresh',
														text : 'Batch Annotation',
														tooltip : '',
														handler : function() {
															var tab = Ext.create('Ext.form.Panel', {
																		bodyPadding : 5,
																		width : 350,
																		url : '/gardener/batchAnnotation/',
																		layout : 'anchor',
																		defaults : {
																			anchor : '100%'
																		},
																		defaultType : 'textfield',
																		items : [{
																					xtype : 'textarea',
																					fieldLabel : 'Symbol List',
																					name : 'symbol',
																					height : 200,
																					allowBlank : false
																				}, {
																					fieldLabel : 'Annotation',
																					name : 'annotation',
																					allowBlank : false
																				}],
																		buttons : [{
																					text : 'Get Current Symbols',
																					handler : function() {
																						var btn = this
																						var exploadMask = new Ext.LoadMask(grid2, {
																									msg : 'Loading.....'
																								});
																						exploadMask.show();
																						var data = grid2.filters.getFilterData();
																						var s = '[';
																						for (i = 0; i < data.length; i++) {
																							s += '{'
																							temp = String(Ext.encode(data[i].data))
																							s += temp.substr(1, temp.length - 2)
																							s += ',"field":"'
																							s += String(data[i].field)
																							s += '"}'
																							if (i != data.length - 1)
																								s += ','
																						}
																						s += ']'
																						Ext.Ajax.request({
																									url : '/gardener/data/showgene/',
																									method : 'GET',
																									timeout : 600000,
																									params : {
																										sid : record.data.id,
																										stype : 'exper',
																										filter : s,
																										limit : -1
																									},
																									success : function(response) {
																										exploadMask.hide();
																										var text = response.responseText;
																										text = Ext.JSON.decode(text)
																										var data = text.data
																										var total = text.total
																										var tempstring = ''
																										for (var count = 0; count < total; count++) {
																											tempstring = tempstring + data[count].symbol
																													+ '\n'
																										}
																										btn.up('form').form.setValues({
																													symbol : tempstring
																												})
																									},
																									failure : function() {
																										exploadMask.hide();
																									}
																								});

																					}
																				}, {
																					text : 'Reset',
																					handler : function() {
																						this.up('form').getForm().reset();
																					}
																				}, {
																					text : 'Submit',
																					formBind : true,
																					handler : function() {
																						var form = this.up('form').getForm();
																						if (form.isValid()) {
																							// console.log('yes')
																							form.submit({
																										url : '/gardener/userAnnotation/',
																										params : {
																											exp : Ext.getCmp('content-panel').activeTab.title
																													.split('of ')[1],
																											batch : true
																										},
																										waitMsg : 'Adding Experiment......',
																										timeout : 300000,
																										success : function(form, action) {
																											Ext.Msg.alert('Success', action.result.msg);
																										},
																										failure : function(form, action) {
																											Ext.Msg.alert('Failed', action.result.msg);
																										}
																									});
																						}
																					}
																				}]
																	});
															var win = new Ext.Window({
																draggable : {
																	constrain : true,
																	constrainTo : Ext.getBody()
																},
																// title :
																// 'Comparison
																// Search',
																// width : 500,
																resizable : false,
																// animateTarget :
																// 'newcompare',
																items : [tab]
																	/*
																	 * , bbar :
																	 * ['->', { text :
																	 * 'Yes',
																	 * handler :
																	 * submitForm }, {
																	 * text : 'No',
																	 * handler :
																	 * function() {
																	 * win.close() } }]
																	 */
																})
															win.show()
														}
													}, '->', {
														xtype : 'component',
														itemId : 'status',
														tpl : 'Matching Genes: {count}',
														style : 'margin-right:5px'
													}]
										}],
										emptyText : 'No Matching Records',
										plugins : [Ext.create('Ext.grid.plugin.CellEditing', {
															clicksToEdit : 1,
															listeners : {
																edit : function(editor, e) {
																	console.log(grid2)
																	var sym = grid2.getStore().getAt(e.rowIdx).get('symbol')
																	if (!sym || sym == '-') {
																		Ext.Msg.alert('Error', 'Symbol error')
																		return
																	}
																	Ext.Ajax.request({
																				timeout : 600000,
																				url : '/gardener/userAnnotation/',
																				method : 'POST',
																				params : {
																					exp : Ext.getCmp('content-panel').activeTab.title.split('of ')[1],
																					symbol : sym,
																					annotation : e.value
																				}
																			});
																}
															}
														}), {
													ptype : 'rowexpander',
													selectRowOnExpand : true,
													expandOnDblClick : true,
													rowBodyTpl : ['<div id="Sear-Peptide-' + timestamp + '{id}" ></div>'],
													toggleRow : function(rowIdx, record) {
														var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
																.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view
																.getRecord(rowNode), grid = this.getCmp(), id = record.get('id'), targetId = 'Sear-Peptide-'
																+ timestamp + id, symbol = record.get('symbol'), search_id = record.get('search_id');
														if (row.hasCls(this.rowCollapsedCls)) {
															row.removeCls(this.rowCollapsedCls);
															this.recordsExpanded[record.internalId] = true;
															this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
															if (rowNode.grid) {
																nextBd.removeCls(hiddenCls);
																rowNode.grid.doComponentLayout();
															} else {
																Ext.create('Ext.data.Store', {
																			model : 'gar.model.Peptide',
																			pageSize : 100,
																			autoLoad : true,
																			proxy : {
																				type : 'ajax',
																				url : '/gardener/data/showpeptide/',
																				extraParams : {
																					sid : id,
																					stype : 'gene',
																					symbol : symbol,
																					search_id : search_id
																				},
																				reader : {
																					type : 'json',
																					root : 'data',
																					totalProperty : 'total'
																				}
																			},
																			autoLoad : {
																				callback : function() {
																					nextBd.removeCls(hiddenCls);
																					Ext.create('gar.view.Peptide', {
																								renderTo : targetId,
																								store : this,
																								row : row,
																								height : 200,
																								listeners : {
																									cellclick : peptide_sum_plot
																								}
																							});
																					rowNode.grid = grid2;
																					// grid.suspendEvents();
																				}
																			},
																			listeners : {
																				beforeload : function() {
																					exploadMask.show();
																				},
																				load : function() {
																					exploadMask.hide();
																				}
																			}
																		});
															}
														} else {
															row.addCls(this.rowCollapsedCls);
															nextBd.addCls(this.rowBodyHiddenCls);
															this.recordsExpanded[record.internalId] = false;
															this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
														}
													}
												}],
										listeners : {
							// cellclick
										// :
										// ucsc_plot
								}
							})
							var filters3 = {
								ftype : 'filters',
								encode : true
							}
							function onStoreSizeChange3() {
								grid3.down('#status').update({
											count : tstore3.getTotalCount()
										});
							}
							var tstore3 = Ext.create('gar.store.Gene', {
										listeners : {
											totalcountchange : onStoreSizeChange3
										}
									});
							tstore3.getProxy().url = '/gardener/data/silacgene/'
							tstore3.getProxy().extraParams = {
								stype : 'exper',
								label: 'heavy',
								exp_name: record.data.name
							};
							var grid3 = Ext.create('gar.view.Gene', {
										// id :
										// 'protein_tab_'+
										// Ext.getCmp('info_protein_tab_index').value,
										store : tstore3,
										features : [filters3],
										dockedItems : [{
											dock : 'top',
											xtype : 'toolbar',
											items : [{
														text : 'Clear Filter Data',
														handler : function() {
															grid3.filters.clearFilters();
														}
													}, {
														text : 'All Filter Data',
														tooltip : 'Get Filter Data for Grid',
														handler : function() {
															var annoList = {
																'co_1': 'Coreg',
																'ki_1': 'Kinase', 
																'li_1': 'Ligand', 
																're_1': 'Receptor', 
																'pmm_1':'Plasma Membrane(Mouse)', 
																'pmh_1':'Plasma Membrane(Human)',
																'tf_1': 'Transcription Factor'
															}
															var modiList = {
																'Acetyl_1': 'N-terminal Acetyltrasferases',
																'Methyl_1': 'Methylation',
																'GlyGly_1': 'Ubiquitination',
																'Biotin_1': 'Biotin',
																'PhosphoST_1': 'Phosphorylation-ST',
																'PhosphoY_1': 'Phosphorylation-Y'
															}
															var filterData = grid3.filters.getFilterData()
															var filtersStore = Ext.create('Ext.data.Store', {
															    fields:['field', 'type', 'value'],
															    data:[]
															});

															for( var i = 0; i < filterData.length; i++)
															{
																var field, type, value
																field = filterData[i].field
																switch(filterData[i].data.type)
																{
																	case 'string':
																		type = 'has string'
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	case 'list':
																		type = 'has type'
																		for( var j = 0; j < filterData[i].data.value.length; j++)
																		{
																			value = filterData[i].data.value[j]
																			if(field == 'annotation')
																				filtersStore.add({ 'field': field, "type": type, "value": annoList[value] })
																			else if (field == 'modification')
																				filtersStore.add({ 'field': field, "type": type, "value": modiList[value] })
																		}
																		break
																	case 'numeric':
																		switch(filterData[i].data.comparison.slice(0,2))
																		{
																			case 'gt':
																				type = 'is bigger than'
																				break
																			case 'lt':
																				type = 'is little than'
																				break
																			case 'eq':
																				type = 'equals to'
																				break
																			default:
																				type = 'null'
																		}
																		value = filterData[i].data.value
																		filtersStore.add({ 'field': field, "type": type, "value": value })
																		break
																	default: 
																		type = 'null'
																}
															}

															var filterWindow = Ext.create(Ext.window.Window,{
																title: 'All filter data',
																height: 300,
																width: 500,
																modal: true,
																animateTarget: this,
																layout: 'fit',
																autoShow: true,
																items: [{
																	xtype: 'grid',
																	hideHeaders: true,
																	columns: [
																        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
																        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
																        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
																    ],
																    store: filtersStore
																}]
															})
														}
													}, {
														iconCls : 'refresh',
														text : 'Refresh This Tab',
														tooltip : 'Update to Latest Progress',
														handler : function() {
															tstore.load()
														}
													}, {
														// iconCls:'refresh',
														text : 'Batch Annotation',
														tooltip : '',
														handler : function() {
															var tab = Ext.create('Ext.form.Panel', {
																		bodyPadding : 5,
																		width : 350,
																		url : '/gardener/batchAnnotation/',
																		layout : 'anchor',
																		defaults : {
																			anchor : '100%'
																		},
																		defaultType : 'textfield',
																		items : [{
																					xtype : 'textarea',
																					fieldLabel : 'Symbol List',
																					name : 'symbol',
																					height : 200,
																					allowBlank : false
																				}, {
																					fieldLabel : 'Annotation',
																					name : 'annotation',
																					allowBlank : false
																				}],
																		buttons : [{
																					text : 'Get Current Symbols',
																					handler : function() {
																						var btn = this
																						var exploadMask = new Ext.LoadMask(grid3, {
																									msg : 'Loading.....'
																								});
																						exploadMask.show();
																						var data = grid3.filters.getFilterData();
																						var s = '[';
																						for (i = 0; i < data.length; i++) {
																							s += '{'
																							temp = String(Ext.encode(data[i].data))
																							s += temp.substr(1, temp.length - 2)
																							s += ',"field":"'
																							s += String(data[i].field)
																							s += '"}'
																							if (i != data.length - 1)
																								s += ','
																						}
																						s += ']'
																						Ext.Ajax.request({
																									url : '/gardener/data/showgene/',
																									method : 'GET',
																									timeout : 600000,
																									params : {
																										sid : record.data.id,
																										stype : 'exper',
																										filter : s,
																										limit : -1
																									},
																									success : function(response) {
																										exploadMask.hide();
																										var text = response.responseText;
																										text = Ext.JSON.decode(text)
																										var data = text.data
																										var total = text.total
																										var tempstring = ''
																										for (var count = 0; count < total; count++) {
																											tempstring = tempstring + data[count].symbol
																													+ '\n'
																										}
																										btn.up('form').form.setValues({
																													symbol : tempstring
																												})
																									},
																									failure : function() {
																										exploadMask.hide();
																									}
																								});

																					}
																				}, {
																					text : 'Reset',
																					handler : function() {
																						this.up('form').getForm().reset();
																					}
																				}, {
																					text : 'Submit',
																					formBind : true,
																					handler : function() {
																						var form = this.up('form').getForm();
																						if (form.isValid()) {
																							// console.log('yes')
																							form.submit({
																										url : '/gardener/userAnnotation/',
																										params : {
																											exp : Ext.getCmp('content-panel').activeTab.title
																													.split('of ')[1],
																											batch : true
																										},
																										waitMsg : 'Adding Experiment......',
																										timeout : 300000,
																										success : function(form, action) {
																											Ext.Msg.alert('Success', action.result.msg);
																										},
																										failure : function(form, action) {
																											Ext.Msg.alert('Failed', action.result.msg);
																										}
																									});
																						}
																					}
																				}]
																	});
															var win = new Ext.Window({
																draggable : {
																	constrain : true,
																	constrainTo : Ext.getBody()
																},
																// title :
																// 'Comparison
																// Search',
																// width : 500,
																resizable : false,
																// animateTarget :
																// 'newcompare',
																items : [tab]
																	/*
																	 * , bbar :
																	 * ['->', { text :
																	 * 'Yes',
																	 * handler :
																	 * submitForm }, {
																	 * text : 'No',
																	 * handler :
																	 * function() {
																	 * win.close() } }]
																	 */
																})
															win.show()
														}
													}, '->', {
														xtype : 'component',
														itemId : 'status',
														tpl : 'Matching Genes: {count}',
														style : 'margin-right:5px'
													}]
										}],
										emptyText : 'No Matching Records',
										plugins : [Ext.create('Ext.grid.plugin.CellEditing', {
															clicksToEdit : 1,
															listeners : {
																edit : function(editor, e) {
																	console.log(grid3)
																	var sym = grid3.getStore().getAt(e.rowIdx).get('symbol')
																	if (!sym || sym == '-') {
																		Ext.Msg.alert('Error', 'Symbol error')
																		return
																	}
																	Ext.Ajax.request({
																				timeout : 600000,
																				url : '/gardener/userAnnotation/',
																				method : 'POST',
																				params : {
																					exp : Ext.getCmp('content-panel').activeTab.title.split('of ')[1],
																					symbol : sym,
																					annotation : e.value
																				}
																			});
																}
															}
														}), {
													ptype : 'rowexpander',
													selectRowOnExpand : true,
													expandOnDblClick : true,
													rowBodyTpl : ['<div id="Sear-Peptide-' + timestamp + '{id}" ></div>'],
													toggleRow : function(rowIdx, record) {
														var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
																.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view
																.getRecord(rowNode), grid = this.getCmp(), id = record.get('id'), targetId = 'Sear-Peptide-'
																+ timestamp + id, symbol = record.get('symbol'), search_id = record.get('search_id');
														if (row.hasCls(this.rowCollapsedCls)) {
															row.removeCls(this.rowCollapsedCls);
															this.recordsExpanded[record.internalId] = true;
															this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
															if (rowNode.grid) {
																nextBd.removeCls(hiddenCls);
																rowNode.grid.doComponentLayout();
															} else {
																Ext.create('Ext.data.Store', {
																			model : 'gar.model.Peptide',
																			pageSize : 100,
																			autoLoad : true,
																			proxy : {
																				type : 'ajax',
																				url : '/gardener/data/showpeptide/',
																				extraParams : {
																					sid : id,
																					stype : 'gene',
																					symbol : symbol,
																					search_id : search_id
																				},
																				reader : {
																					type : 'json',
																					root : 'data',
																					totalProperty : 'total'
																				}
																			},
																			autoLoad : {
																				callback : function() {
																					nextBd.removeCls(hiddenCls);
																					Ext.create('gar.view.Peptide', {
																								renderTo : targetId,
																								store : this,
																								row : row,
																								height : 200,
																								listeners : {
																									cellclick : peptide_sum_plot
																								}
																							});
																					rowNode.grid = grid3;
																					// grid.suspendEvents();
																				}
																			},
																			listeners : {
																				beforeload : function() {
																					exploadMask.show();
																				},
																				load : function() {
																					exploadMask.hide();
																				}
																			}
																		});
															}
														} else {
															row.addCls(this.rowCollapsedCls);
															nextBd.addCls(this.rowBodyHiddenCls);
															this.recordsExpanded[record.internalId] = false;
															this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
														}
													}
												}],
										listeners : {
							// cellclick
										// :
										// ucsc_plot
								}
							})
							var silacTabpanel = Ext.create('Ext.tab.Panel', {
							    // layout: 'fit',
							    tabPosition: 'right'
							});
							c.add({
								title : 'Gene of ' + record.data.name,
								// iconCls :
								// 'tabs',
								closable : true,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [silacTabpanel]
							}).show()
							silacTabpanel.add({
								title : 'Mix',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid]
							}).show()
							silacTabpanel.add({
								title : 'Light',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid2]
							})
							silacTabpanel.add({
								title : 'Heavy',
								// iconCls :
								// 'tabs',
								closable : false,
								// id :
								// 'tab_'+
								// Ext.getCmp('info_tab_index').value,
								layout : 'fit',
								items : [grid3]
							})
							silacTabpanel.setActiveTab(silacTabpanel.items.items[0])
						}else{
							c.add({
									title : 'Gene of ' + record.data.name,
									// iconCls :
									// 'tabs',
									closable : true,
									// id :
									// 'tab_'+
									// Ext.getCmp('info_tab_index').value,
									layout : 'fit',
									items : [grid]
								}).show()
						}
					} else if (clickedColumnName == "Name" && cellIndex > 0) {
						var rec = grid.getStore().getAt(rowIndex);
						// console.log(rec.data)
						var panel = Ext.create('gar.view.Experiment_detail')
						var win = Ext.create('Ext.Window', {
									// draggable : {
									// constrain : true,
									// constrainTo : Ext.getBody()
									// },
									autoScroll : true,
									resizable : true,
									title : 'Experiment Info',
									width : 615,
									height : 450,
									// y : 50,
									items : [panel]
								})
						win.show()
						Ext.Ajax.request({
									url : '/experiments/load/experiment/',
									params : {
										experiment_no : rec.data.name.split('Exp')[1]
										// csrfmiddlewaretoken : csrftoken
									},
									success : function(response) {
										var text = response.responseText;
										exp_Info_responseJson = Ext.JSON.decode(text).data;
										// console.log(panel)
										panel.items.items[0].setValue(exp_Info_responseJson.expname);
										panel.items.items[1].setValue(exp_Info_responseJson.company + '/ ' + exp_Info_responseJson.lab + '/ '
												+ exp_Info_responseJson.experimenter);
										panel.items.items[2].setValue(exp_Info_responseJson.date);
										panel.items.items[3].setValue(exp_Info_responseJson.Funding + '/ ' + exp_Info_responseJson.Project + '/ '
												+ exp_Info_responseJson.PI);
										panel.items.items[4].setValue(exp_Info_responseJson.SubProject + '/ ' + exp_Info_responseJson.Subject + '/ '
												+ exp_Info_responseJson.Manager);
										panel.items.items[5].setValue(exp_Info_responseJson.Experiment_type);
										panel.items.items[6].setValue(exp_Info_responseJson.description);
										panel.items.items[7].setValue(exp_Info_responseJson.sample_id);
										panel.items.items[8].setValue(exp_Info_responseJson.reagent_id);
										panel.items.items[9].setValue(exp_Info_responseJson.method_num);
										panel.items.items[10]
												.setValue(exp_Info_responseJson.Digest_type + '/ ' + exp_Info_responseJson.Digest_enzyme);
										panel.items.items[11].setValue(exp_Info_responseJson.search_database + '/ '
												+ exp_Info_responseJson.instrument_name + '/ ms1:' + exp_Info_responseJson.ms1 + '-'
												+ exp_Info_responseJson.ms1_details + '/ ms2:' + exp_Info_responseJson.ms2 + '-'
												+ exp_Info_responseJson.ms2_details);
										panel.items.items[12].setValue(exp_Info_responseJson.Dynamic_Modification);
										panel.items.items[13].setValue(exp_Info_responseJson.Fixed_Modification);
										panel.items.items[14].setValue(exp_Info_responseJson.ispec);
										panel.items.items[15].setValue(exp_Info_responseJson.comments_conclusions);
										// console.log(responseJson)
									}
								});
					} else if (clickedColumnName == "Progress" && cellIndex > 0) {
						return
						if (record.get('stage') < 0) {
							Ext.Msg.alert('Warning', 'No file found.')
							return
						}
						/*
						 * // console.log(record) if (record.get('stage') == 5) {
						 * Ext.Msg.alert('Report', 'This experiment is done.');
						 * return; } Ext.Msg.alert('Notice', 'Checking
						 * status...(maybe very slow)') Ext.Ajax.request({
						 * timeout : 3600000, url : '/checkError/', params : {
						 * exp_name : record.get('name'),// 'Exp000197',
						 * instrument : record.get('instrument') // 5600 },
						 * method : 'GET', success : function(response) { var
						 * win = new Ext.Window({ title : 'Report', // width // : //
						 * 200, bodyPadding : 10, html : response.responseText
						 * }); win.show(); //
						 * Ext.Msg.alert('Report',response.responseText) },
						 * failure : function(response) { var win = new
						 * Ext.Window({ title : 'Failed', // width // : // 200,
						 * bodyPadding : 10, html : 'Network error,do check next
						 * time.' }); win.show(); //
						 * Ext.Msg.alert('Failed','Check // failed,try // next
						 * time.') } });
						 */
						var fileListStore = Ext.create('Ext.data.Store', {
									proxy : {
										type : 'ajax',
										url : '/getLocalFileList/',
										reader : {
											type : 'json',
											root : 'fileList'
										}
									},
									fields : [{
												name : 'file',
												type : 'string'
											}, {
												name : 'mascot_file',
												type : 'string'
											}],
									autoLoad : true
								});
						fileListStore.getProxy().extraParams = {
							exp_name : record.get('name'), // 'Exp000197',
							instru : record.get('instrument')
							// 5600
						};
						var grid = Ext.create('Ext.grid.Panel', {
									// title: 'File List Grid',
									store : fileListStore,
									height : 310,
									// width : 570,
									forceFit : true,
									viewConfig : {
										// trackOver: false,
										stripeRows : true,
										enableTextSelection : true
									},
									columns : [{
												text : "No.",
												xtype : 'rownumberer',
												width : 45
											}, {
												text : 'File name',
												dataIndex : 'file',
												width : 450,
												renderer : function(value, metaData, record, rowIndex, colIndex, store) {
													metaData.tdAttr = "title='" + value + "'";
													return value
												}
											}, {
												text : 'Mascot File Path',
												dataIndex : 'mascot_file',
												width : 400,
												renderer : function(value, metaData, record, rowIndex, colIndex, store) {
													metaData.tdAttr = "title='" + value + "'";
													return value
												}
											}, {
												text : 'Action',
												xtype : 'actioncolumn',
												flex : 1,
												items : [{
															icon : '/static/images/detail.png',
															tooltip : 'Info',
															handler : function(grid, rowIndex, colIndex) {
																Ext.Msg.alert('Building', 'This function is not ready.')
															}
														}]
											}]
								});
						// if (record.get('stage') == 5)
						// { Ext.Msg.alert('Report', 'This experiment is
						// done.'); }
						var win = new Ext.Window({
									title : 'File list of ' + record.get('name'),
									width : 580,
									height : 350,
									bodyPadding : 0,
									items : [grid],
									resizable : true
								}).show();
					} else {
						var data = (Ext.getCmp('info_experiments_selected').getValue()) ? Ext.decode(Ext.getCmp('info_experiments_selected')
								.getValue()) : 0;
						type = 'exp'
						exp_id = record.data.id
						console.log(record.data.id)
						repeat_id = 1
						rank = 1
						if (document.getElementById('experiment_selector_' + exp_id).checked == true) {
							// console.log(store)
							store.add({
										id : type + '_' + exp_id + '_' + repeat_id + '_' + rank,
										exp_id : exp_id,
										repeat_id : repeat_id,
										rank : rank,
										name : record.data.name,
										type : type,
										num_fraction : record.data.num_fraction,
										num_repeat : record.data.num_repeat,
										num_spectrum : record.data.num_spectrum,
										num_peptide : record.data.num_peptide,
										num_isoform : record.data.num_isoform,
										num_gene : record.data.num_gene,
										stage : record.data.stage
									});
							checkBoxList.push(record.data.name)
                            checkBoxIDList.push(record.data.id)
						} else {
							checkBoxList.remove(record.data.name)
                            checkBoxIDList.remove(record.data.id)
							store.removeAt(store.indexOfId(type + '_' + exp_id + '_' + repeat_id + '_' + rank))
							store.save()
						}
						store.save()
					}
				}
			},
			'search' : {
				cellclick : function(grid, td, cellIndex, record, tr, rowIndex, e, eOpts) {
					var clickedDataIndex = grid.panel.headerCt.getHeaderAtIndex(cellIndex).dataIndex;
					var clickedColumnName = grid.panel.headerCt.getHeaderAtIndex(cellIndex).text;
					var clickedCellValue = record.get(clickedDataIndex);

					// a =
					// Ext.getElementById(td.id).classList[2].toString().substring(12)
					if (clickedColumnName == "Isoform Num") {
						// console.log(record)
						var filters = {
							ftype : 'filters',
							encode : true
						}
						function onStoreSizeChange() {
							grid.down('#status').update({
										count : store.getTotalCount()
									});
						}
						var store = Ext.create('gar.store.Protein', {
									listeners : {
										totalcountchange : onStoreSizeChange
									}
								});
						store.getProxy().extraParams = {
							sid : record.data.repeat_id,
							rankid : record.data.rank,
							search_id : record.data.search_id,
							stype : 'search'
						};
						Ext.getCmp('info_protein_tab_index').value += 1
						var grid = Ext.create('gar.view.Protein', {
							// id :
							// 'protein_tab_'+
							// Ext.getCmp('info_protein_tab_index').value,
							store : store,
							features : [filters],
							multiSelect : true,
							dockedItems : [{
										dock : 'top',
										xtype : 'toolbar',
										items : [{
													text : 'Clear Filter Data',
													handler : function() {
														grid.filters.clearFilters();
													}
												}, {
													text : 'All Filter Data',
													tooltip : 'Get Filter Data for Grid',
													handler : function() {
														var annoList = {
															'co_1': 'Coreg',
															'ki_1': 'Kinase', 
															'li_1': 'Ligand', 
															're_1': 'Receptor', 
															'pmm_1':'Plasma Membrane(Mouse)', 
															'pmh_1':'Plasma Membrane(Human)',
															'tf_1': 'Transcription Factor'
														}
														var modiList = {
															'Acetyl_1': 'N-terminal Acetyltrasferases',
															'Methyl_1': 'Methylation',
															'GlyGly_1': 'Ubiquitination',
															'Biotin_1': 'Biotin',
															'PhosphoST_1': 'Phosphorylation-ST',
															'PhosphoY_1': 'Phosphorylation-Y'
														}
														var filterData = grid.filters.getFilterData()
														var filtersStore = Ext.create('Ext.data.Store', {
														    fields:['field', 'type', 'value'],
														    data:[]
														});

														for( var i = 0; i < filterData.length; i++)
														{
															var field, type, value
															field = filterData[i].field
															switch(filterData[i].data.type)
															{
																case 'string':
																	type = 'has string'
																	value = filterData[i].data.value
																	filtersStore.add({ 'field': field, "type": type, "value": value })
																	break
																case 'list':
																	type = 'has type'
																	for( var j = 0; j < filterData[i].data.value.length; j++)
																	{
																		value = filterData[i].data.value[j]
																		if(field == 'annotation')
																			filtersStore.add({ 'field': field, "type": type, "value": annoList[value] })
																		else if (field == 'modification')
																			filtersStore.add({ 'field': field, "type": type, "value": modiList[value] })
																	}
																	break
																case 'numeric':
																	switch(filterData[i].data.comparison.slice(0,2))
																	{
																		case 'gt':
																			type = 'is bigger than'
																			break
																		case 'lt':
																			type = 'is little than'
																			break
																		case 'eq':
																			type = 'equals to'
																			break
																		default:
																			type = 'null'
																	}
																	value = filterData[i].data.value
																	filtersStore.add({ 'field': field, "type": type, "value": value })
																	break
																default: 
																	type = 'null'
															}
														}

														var filterWindow = Ext.create(Ext.window.Window,{
															title: 'All filter data',
															height: 300,
															width: 500,
															modal: true,
															animateTarget: this,
															layout: 'fit',
															autoShow: true,
															items: [{
																xtype: 'grid',
																hideHeaders: true,
																columns: [
															        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
															        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
															        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
															    ],
															    store: filtersStore
															}]
														})
													}
												}, '->', {
													xtype : 'component',
													itemId : 'status',
													tpl : 'Matching Proteins: {count}',
													style : 'margin-right:5px'
												}]
									}],
							emptyText : 'No Matching Records',
							plugins : [{
								ptype : 'rowexpander',
								selectRowOnExpand : true,
								expandOnDblClick : true,
								rowBodyTpl : ['<div id="Sear-Peptide-{id}" ></div>'],
								toggleRow : function(rowIdx) {
									var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
											.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view.getRecord(rowNode), grid = this
											.getCmp(), id = record.get('id'), targetId = 'Sear-Peptide-' + id, accession = record.get('accession'), search_id = record
											.get('search_id');
									if (row.hasCls(this.rowCollapsedCls)) {
										row.removeCls(this.rowCollapsedCls);
										this.recordsExpanded[record.internalId] = true;
										this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
										if (rowNode.grid) {
											nextBd.removeCls(hiddenCls);
											rowNode.grid.doComponentLayout();
										} else {
											Ext.create('Ext.data.Store', {
														model : 'gar.model.Peptide',
														pageSize : 100,
														autoLoad : true,
														buffered : true,
														proxy : {
															type : 'ajax',
															url : '/gardener/data/showpeptide/',
															extraParams : {
																sid : id,
																accession : accession,
																search_id : search_id,
																stype : 'protein'
															},
															reader : {
																type : 'json',
																root : 'data',
																totalProperty : 'total'
															}
														},
														autoLoad : {
															callback : function() {
																nextBd.removeCls(hiddenCls);
																Ext.create('gar.view.Peptide', {
																			renderTo : targetId,
																			store : this,
																			row : row,
																			height : 200
																		});
																rowNode.grid = grid;
																// grid.suspendEvents();
															}
														}
													});
										}
									} else {
										row.addCls(this.rowCollapsedCls);
										nextBd.addCls(this.rowBodyHiddenCls);
										this.recordsExpanded[record.internalId] = false;
										this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
									}
								}
							}],
							listeners : {
								cellclick : ucsc_plot
							}
						})
						{
							c = Ext.getCmp('content-panel')
							c.add({
										title : 'Protein of Exp' + record.data.name.split('_')[0],
										// iconCls
										// :
										// 'tabs',
										closable : true,
										layout : 'fit',
										items : [grid]
									}).show()
						}
					} else if (clickedColumnName == "Peptide Num") {
						// console.log(record.data)
						var filters = {
							ftype : 'filters',
							encode : true
						}
						function onStoreSizeChange() {
							grid.down('#status').update({
										count : store.getTotalCount()
									});
						}
						var store = Ext.create('gar.store.Peptide', {
									listeners : {
										totalcountchange : onStoreSizeChange
									}
								});
						store.getProxy().extraParams = {
							search_id : record.data.search_id,
							stype : 'search'
						}
						Ext.getCmp('info_protein_tab_index').value += 1
						var grid = Ext.create('gar.view.Peptide', {
							// id :
							// 'protein_tab_'+
							// Ext.getCmp('info_protein_tab_index').value,
							store : store,
							features : [filters],
							multiSelect : true,
							dockedItems : [{
										dock : 'top',
										xtype : 'toolbar',
										items : [{
													text : 'Clear Filter Data',
													handler : function() {
														grid.filters.clearFilters();
													}
												}, {
													text : 'All Filter Data',
													tooltip : 'Get Filter Data for Grid',
													handler : function() {
														var filterData = grid.filters.getFilterData()
														var filtersStore = Ext.create('Ext.data.Store', {
														    fields:['field', 'type', 'value'],
														    data:[]
														});

														for( var i = 0; i < filterData.length; i++)
														{
															var field, type, value
															field = filterData[i].field
															switch(filterData[i].data.type)
															{
																case 'string':
																	type = 'has string'
																	value = filterData[i].data.value
																	filtersStore.add({ 'field': field, "type": type, "value": value })
																	break
																case 'numeric':
																	switch(filterData[i].data.comparison.slice(0,2))
																	{
																		case 'gt':
																			type = 'is bigger than'
																			break
																		case 'lt':
																			type = 'is little than'
																			break
																		case 'eq':
																			type = 'equals to'
																			break
																		default:
																			type = 'null'
																	}
																	value = filterData[i].data.value
																	filtersStore.add({ 'field': field, "type": type, "value": value })
																	break
																default: 
																	type = 'null'
															}
														}

														var filterWindow = Ext.create(Ext.window.Window,{
															title: 'All filter data',
															height: 300,
															width: 500,
															modal: true,
															animateTarget: this,
															layout: 'fit',
															autoShow: true,
															items: [{
																xtype: 'grid',
																hideHeaders: true,
																columns: [
															        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
															        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
															        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
															    ],
															    store: filtersStore
															}]
														})
													}
												}, '->', {
													xtype : 'component',
													itemId : 'status',
													tpl : 'Matching Peptides: {count}',
													style : 'margin-right:5px'
												}]
									}],
							emptyText : 'No Matching Records',
							plugins : [{
								ptype : 'rowexpander',
								selectRowOnExpand : true,
								expandOnDblClick : true,
								rowBodyTpl : ['<div id="Sear-Peptide-{id}" ></div>'],
								toggleRow : function(rowIdx, record) {
									var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
											.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view.getRecord(rowNode), grid = this
											.getCmp(), id = record.get('id'), targetId = 'Sear-Peptide-' + id, protein_group_accessions = record
											.get('protein_group_accessions'), search_id = record.get('search_id');
									if (row.hasCls(this.rowCollapsedCls)) {
										row.removeCls(this.rowCollapsedCls);
										this.recordsExpanded[record.internalId] = true;
										this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
										if (rowNode.grid) {
											nextBd.removeCls(hiddenCls);
											rowNode.grid.doComponentLayout();
										} else {
											Ext.create('Ext.data.Store', {
														model : 'gar.model.Protein',
														pageSize : 100,
														autoLoad : true,
														proxy : {
															type : 'ajax',
															url : '/gardener/data/showprotein/',
															extraParams : {
																sid : id,
																stype : 'peptide',
																protein_group_accessions : protein_group_accessions,
																search_id : search_id
															},
															reader : {
																type : 'json',
																root : 'data',
																totalProperty : 'total'
															}
														},
														autoLoad : {
															callback : function() {
																nextBd.removeCls(hiddenCls);
																Ext.create('gar.view.Protein', {
																			renderTo : targetId,
																			store : this,
																			row : row,
																			height : 120
																		});
																rowNode.grid = grid;
																// grid.suspendEvents();
															}
														}
													});
										}
									} else {
										row.addCls(this.rowCollapsedCls);
										nextBd.addCls(this.rowBodyHiddenCls);
										this.recordsExpanded[record.internalId] = false;
										this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
									}
								}
							}],
							listeners : {
								cellclick : peptide_sum_plot
							}
						})
						c = Ext.getCmp('content-panel')
						Ext.getCmp('info_tab_index').value += 1
						c.add({
									title : 'Peptide of Exp' + record.data.name.split('_')[0],
									// iconCls :
									// 'tabs',
									closable : true,
									// id :
									// 'tab_'+
									// Ext.getCmp('info_tab_index').value,
									layout : 'fit',
									items : [grid]
								}).show()
					} else if (clickedColumnName == "Gene Num" && cellIndex > 0) {
						var filters = {
							ftype : 'filters',
							encode : true
						}
						function onStoreSizeChange() {
							grid.down('#status').update({
										count : store.getTotalCount()
									});
						}
						var store = Ext.create('gar.store.Gene', {
									listeners : {
										totalcountchange : onStoreSizeChange
									}
								});
						// console.log(record)
						store.getProxy().extraParams = {
							sid : record.data.search_id,
							stype : 'search'
						};
						Ext.getCmp('info_protein_tab_index').value += 1
						var grid = Ext.create('gar.view.Gene', {
							// id :
							// 'protein_tab_'+
							// Ext.getCmp('info_protein_tab_index').value,
							store : store,
							features : [filters],
							multiSelect : true,
							dockedItems : [{
										dock : 'top',
										xtype : 'toolbar',
										items : [{
													text : 'Clear Filter Data',
													handler : function() {
														grid.filters.clearFilters();
													}
												}, {
													text : 'All Filter Data',
													tooltip : 'Get Filter Data for Grid',
													handler : function() {
														var annoList = {
															'co_1': 'Coreg',
															'ki_1': 'Kinase', 
															'li_1': 'Ligand', 
															're_1': 'Receptor', 
															'pmm_1':'Plasma Membrane(Mouse)', 
															'pmh_1':'Plasma Membrane(Human)',
															'tf_1': 'Transcription Factor'
														}
														var modiList = {
															'Acetyl_1': 'N-terminal Acetyltrasferases',
															'Methyl_1': 'Methylation',
															'GlyGly_1': 'Ubiquitination',
															'Biotin_1': 'Biotin',
															'PhosphoST_1': 'Phosphorylation-ST',
															'PhosphoY_1': 'Phosphorylation-Y'
														}
														var filterData = grid.filters.getFilterData()
														var filtersStore = Ext.create('Ext.data.Store', {
														    fields:['field', 'type', 'value'],
														    data:[]
														});

														for( var i = 0; i < filterData.length; i++)
														{
															var field, type, value
															field = filterData[i].field
															switch(filterData[i].data.type)
															{
																case 'string':
																	type = 'has string'
																	value = filterData[i].data.value
																	filtersStore.add({ 'field': field, "type": type, "value": value })
																	break
																case 'list':
																	type = 'has type'
																	for( var j = 0; j < filterData[i].data.value.length; j++)
																	{
																		value = filterData[i].data.value[j]
																		if(field == 'annotation')
																			filtersStore.add({ 'field': field, "type": type, "value": annoList[value] })
																		else if (field == 'modification')
																			filtersStore.add({ 'field': field, "type": type, "value": modiList[value] })
																	}
																	break
																case 'numeric':
																	switch(filterData[i].data.comparison.slice(0,2))
																	{
																		case 'gt':
																			type = 'is bigger than'
																			break
																		case 'lt':
																			type = 'is little than'
																			break
																		case 'eq':
																			type = 'equals to'
																			break
																		default:
																			type = 'null'
																	}
																	value = filterData[i].data.value
																	filtersStore.add({ 'field': field, "type": type, "value": value })
																	break
																default: 
																	type = 'null'
															}
														}

														var filterWindow = Ext.create(Ext.window.Window,{
															title: 'All filter data',
															height: 300,
															width: 500,
															modal: true,
															animateTarget: this,
															layout: 'fit',
															autoShow: true,
															items: [{
																xtype: 'grid',
																hideHeaders: true,
																columns: [
															        { text: 'Field',  	dataIndex: 'field',	flex: 3 },
															        { text: 'Type', 	dataIndex: 'type', 	flex: 2 },
															        { text: 'Value', 	dataIndex: 'value',	flex: 3 }
															    ],
															    store: filtersStore
															}]
														})
													}
												}, '->', {
													xtype : 'component',
													itemId : 'status',
													tpl : 'Matching Genes: {count}',
													style : 'margin-right:5px'
												}]
									}],
							emptyText : 'No Matching Records',
							plugins : [{
								ptype : 'rowexpander',
								selectRowOnExpand : true,
								expandOnDblClick : true,
								rowBodyTpl : ['<div id="Sear-Peptide-{id}" ></div>'],
								toggleRow : function(rowIdx, record) {
									var rowNode = this.view.getNode(rowIdx), row = Ext.get(rowNode), nextBd = Ext.get(row)
											.down(this.rowBodyTrSelector), hiddenCls = this.rowBodyHiddenCls, record = this.view.getRecord(rowNode), grid = this
											.getCmp(), id = record.get('id'), targetId = 'Sear-Peptide-' + id, symbol = record.get('symbol'), search_id = record
											.get('search_id');
									if (row.hasCls(this.rowCollapsedCls)) {
										row.removeCls(this.rowCollapsedCls);
										this.recordsExpanded[record.internalId] = true;
										this.view.fireEvent('expandbody', rowNode, record, nextBd.dom);
										if (rowNode.grid) {
											nextBd.removeCls(hiddenCls);
											rowNode.grid.doComponentLayout();
										} else {
											Ext.create('Ext.data.Store', {
														model : 'gar.model.Peptide',
														pageSize : 100,
														autoLoad : true,
														proxy : {
															type : 'ajax',
															url : '/gardener/data/showpeptide/',
															extraParams : {
																sid : id,
																stype : 'gene',
																symbol : symbol,
																search_id : search_id
															},
															reader : {
																type : 'json',
																root : 'data',
																totalProperty : 'total'
															}
														},
														autoLoad : {
															callback : function() {
																nextBd.removeCls(hiddenCls);
																Ext.create('gar.view.Peptide', {
																			renderTo : targetId,
																			store : this,
																			row : row,
																			height : 200
																		});
																rowNode.grid = grid;
																// grid.suspendEvents();
															}
														}
													});
										}
									} else {
										row.addCls(this.rowCollapsedCls);
										nextBd.addCls(this.rowBodyHiddenCls);
										this.recordsExpanded[record.internalId] = false;
										this.view.fireEvent('collapsebody', rowNode, record, nextBd.dom);
									}
								}
							}],
							listeners : {
								cellclick : ucsc_plot
							}
						})
						c = Ext.getCmp('content-panel')
						Ext.getCmp('info_tab_index').value += 1
						c.add({
									title : 'Gene of Exp' + record.data.name.split('_')[0],
									// iconCls :
									// 'tabs',
									closable : true,
									// id :
									// 'tab_'+
									// Ext.getCmp('info_tab_index').value,
									layout : 'fit',
									items : [grid]
								}).show()
					}
				}
			},
			'checkcolumn' : {
				checkchange : function(gridcheck, rowIndex, checked, eOpts) {
					var data = (Ext.getCmp('info_experiments_selected').getValue())
							? Ext.decode(Ext.getCmp('info_experiments_selected').getValue())
							: 0;
					var record = gridcheck.up('grid').store.getAt(rowIndex);
					if (record.data.species == null) {
						type = 'repeat'
						repeat_id = record.data.repeat_id
						exp_id = record.data.exp_id // exp_id is from TABLE
						// gardener_experiment
						rank = record.data.rank
					} else {
						type = 'exp'
						exp_id = record.data.id // exp_id is from TABLE
						// gardener_experiment
						repeat_id = 1
						rank = record.data.rank
					}
					if (checked == true) {
						// console.log(record.data)
						store.add({
							id : type + '_' + exp_id + '_' + rank + '_' + repeat_id,
							exp_id : exp_id,
							repeat_id : repeat_id,
							rank : rank,
							name : record.data.name,
							type : type,
							num_fraction : record.data.num_fraction,
							num_repeat : record.data.num_repeat,
							num_spectrum : record.data.num_spectrum,
							num_peptide : record.data.num_peptide,
							num_isoform : record.data.num_isoform,
							num_gene : record.data.num_gene
								// progress:record.data.stage
							});
					} else {
						store.removeAt(store.indexOfId(type + '_' + exp_id + '_' + rank + '_' + repeat_id))
						store.save()
					}
					store.save()
				}
			},
			'experiment_detail' : {
				afterrender : this.beenRendered
			}
		});
	},
	beenRendered : function(df) {
		// console.log('Rendered!'); // Getting here
		var el = df.el;
		el.on("click", handleClick);
		function handleClick(e, t) {
			e.preventDefault();
			text = t.innerText
			console.log(text)
			/*
			 * if (text.indexOf('Sam') != -1) { //Sample_detail(text) //
			 * Metadata.js sampleDetailLink(text);
			 * //ExperimentInfoLink_sampleDetail.js }
			 * 
			 * if (text.indexOf('Rea') != -1) { //Reagent_detail(text)//
			 * Metadata.js reagentDetailLink(text);
			 * //ExperimentInfoLink_reagentDetail.js }
			 */
			if (text == exp_Info_responseJson.sample_id || text.indexOf('Sam') != -1) {
				sampleDetailLink(text); // ExperimentInfoLink_sampleDetail.js
			}
			if (text == exp_Info_responseJson.reagent_id || text.indexOf('Rea') != -1) {
				reagentDetailLink(text); // ExperimentInfoLink_reagentDetail.js
			}
			if (text == exp_Info_responseJson.method_num) {
				console.log("We have clicked Sepration");
				var expNo = exp_Info_responseJson.expname.split("Exp")[1];
				seprationDetailLink(expNo);
			}
		}
	}
})
