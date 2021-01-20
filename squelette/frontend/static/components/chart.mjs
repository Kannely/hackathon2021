import { debounce } from './utils/general.mjs';
import { planetChartData } from '../data/chart-data.js';
import Chart from 'chart.js';

Vue.component('chart-component', {
	template: `
	<div id="app">
		<canvas id="planet-chart"></canvas>
	</div>
	`,
	data: function() {
		return {
			planetChartData: planetChartData,
		}
	},
	methods: {
		createChart(chartId, chartData) {
		    const ctx = document.getElementById(chartId);
		    const myChart = new Chart(ctx, {
		      type: chartData.type,
		      data: chartData.data,
		      options: chartData.options,
		    });
		  }
	},
	mounted() {
		this.createChart('planet-chart', this.planetChartData);
	}
})
