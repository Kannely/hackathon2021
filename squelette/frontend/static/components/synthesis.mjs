Vue.component('synthesis-skills-chart', {
	extends: VueChartJs.Bar,
	mounted () {
		this.renderChart({
			labels: ["CST1","CST2","CST3","CST4","CST5"],
			datasets: [{
				label: 'Niveaux de compétences',
				backgroundColor: "blue",
				data: [2,1,2,3,5]
			}]
		}, {responsive: true, maintainAspectRatio: false})
	}

})

Vue.component('synthesis-obligations-chart', {
	extends: VueChartJs.Pie,
	mounted () {
		this.renderChart({
			datasets: [{
				label: 'Conditions de diplomation',
				backgroundColor: ["lightblue","blue"],
				data: [70,30]
			}]
		}, {responsive: true, maintainAspectRatio: false})
	}

})