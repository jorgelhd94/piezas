var MONTHS = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];

		var randomScalingFactor = function() {
			return Math.round(Math.random() * 100);
		};

		var config = {
			type: 'line',
			data: {
				labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
				datasets: [{
					label: 'Ventas',
					backgroundColor: window.chartColors.red,
					borderColor: window.chartColors.red,
					data: [
                        0,
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor(),
						randomScalingFactor()
					],
					fill: false,
				}, 
				// {
				// 	label: 'Piezas',
				// 	fill: false,
				// 	backgroundColor: window.chartColors.blue,
				// 	borderColor: window.chartColors.blue,
				// 	data: [
				// 		randomScalingFactor(),
				// 		randomScalingFactor(),
				// 		randomScalingFactor(),
				// 		randomScalingFactor(),
				// 		randomScalingFactor(),
				// 		randomScalingFactor(),
				// 		randomScalingFactor(),
				// 		randomScalingFactor(),
				// 		randomScalingFactor(),
				// 		randomScalingFactor(),
				// 		randomScalingFactor(),
				// 		randomScalingFactor()
				// 	],
				// }
			]
			},
			options: {
				responsive: true,
				title: {
					display: true,
					text: 'Estadística Mensual'
				},
				tooltips: {
					mode: 'index',
					intersect: false,
				},
				hover: {
					mode: 'nearest',
					intersect: true
				},
				scales: {
					xAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Meses del Año'
						}
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Valores Alcanzados'
						},
						ticks: {
							min: 0,
							max: 100,

							// forces step size to be 5 units
							stepSize: 10
						}
					}]
				}
			}
		};

		window.onload = function() {
			var ctx = document.getElementById('canvas').getContext('2d');
			window.myLine = new Chart(ctx, config);
		};

		// document.getElementById('randomizeData').addEventListener('click', function() {
		// 	config.data.datasets.forEach(function(dataset) {
		// 		dataset.data = dataset.data.map(function() {
		// 			return randomScalingFactor();
		// 		});
		// 	});

		// 	window.myLine.update();
		// });

		// var colorNames = Object.keys(window.chartColors);
		// document.getElementById('addDataset').addEventListener('click', function() {
		// 	var colorName = colorNames[config.data.datasets.length % colorNames.length];
		// 	var newColor = window.chartColors[colorName];
		// 	var newDataset = {
		// 		label: 'Dataset ' + config.data.datasets.length,
		// 		backgroundColor: newColor,
		// 		borderColor: newColor,
		// 		data: [],
		// 		fill: false
		// 	};

		// 	for (var index = 0; index < config.data.labels.length; ++index) {
		// 		newDataset.data.push(randomScalingFactor());
		// 	}

		// 	config.data.datasets.push(newDataset);
		// 	window.myLine.update();
		// });

		// document.getElementById('addData').addEventListener('click', function() {
		// 	if (config.data.datasets.length > 0) {
		// 		var month = MONTHS[config.data.labels.length % MONTHS.length];
		// 		config.data.labels.push(month);

		// 		config.data.datasets.forEach(function(dataset) {
		// 			dataset.data.push(randomScalingFactor());
		// 		});

		// 		window.myLine.update();
		// 	}
		// });

		// document.getElementById('removeDataset').addEventListener('click', function() {
		// 	config.data.datasets.splice(0, 1);
		// 	window.myLine.update();
		// });

		// document.getElementById('removeData').addEventListener('click', function() {
		// 	config.data.labels.splice(-1, 1); // remove the label first

		// 	config.data.datasets.forEach(function(dataset) {
		// 		dataset.data.pop();
		// 	});

		// 	window.myLine.update();
		// });