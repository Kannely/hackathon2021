Vue.component('synthesis', {
	template:`
		<div>
			<table id="synthesis-table">
				<tr class="synthesis-info">
					<td>
						<img src="/static/user.png"/>
					</td>
					<td>
						<h1>{{ firstName }} {{ lastName }}</h1>
						<h3>Campus : {{ campus }}</h3>
						<h3>{{ formation }}</h3>
					</td>
					<td>
						<table style="width:100%">
							<td>
								<h4>PCF</h4>
								<p>{{ courses_a1.result }}/{{ courses_a1.total }} UEs validées</p>
								<h4>TAF {{ tafA2 }}</h4>
								<p v-if="tafA2 != '-'">{{ courses_a2.result }}/{{ courses_a2.total }} UEs validées</p>
								<p v-else>-</p>
								<h4>TAF {{ tafA3 }}</h4>
								<p v-if="tafA3 != '-'">{{ courses_a3.result }}/{{ courses_a3.total }} UEs validées</p>
								<p v-else>-</p>
							</td>
							<td>
								<h4>Année en cours</h4>
								<p>{{ tokens.current_year }} jetons</p>
								<p>{{ ects.current_year }}  ECTS</p>
								<h4>Total</h4>
								<p>{{ tokens.total }} jetons</p>
								<p>{{ ects.total }}  ECTS</p>
							</td>
						</table>
					</td>
				</tr>
			</table>
			<table id="synthesis-graph-table">
				<tr>
					<td>
						<synthesis-skills-chart style="height: 300px"/>
					</td>
					<td>
						<synthesis-obligations-chart style="height: 300px"/>
					</td>
				</tr>
			</table>
		</div>
	`,
	data: function() {
		return {
			user: 0,
			lastName: '',
			firstName: '',
			campus: '',
			tafA2: '',
			tafA3: '',
			formation: '',
			tokens: { current_year: 0, total: 0 },
			ects: { current_year: 0, total: 0 },
			courses_a1: { result: 0, total: 0},
			courses_a2: { result: 0, total: 0},
			courses_a3: { result: 0, total: 0},
		}
	},
	methods: {
		async searchSynthesis() {
			const response = await fetch(`/back/synthesis`);
			this.info = await response.json();
			this.lastName = this.info["nom"];
			this.firstName = this.info["prenom"];
			this.campus = this.info["campus"];
			this.tafA2 = this.info["tafA2"];
			this.tafA3 = this.info["tafA3"];
			this.formation = this.info["formation"];
		},
		async searchTokens() {
			const response = await fetch(`/back/jetons`);
			this.info = await response.json();
			this.tokens.current_year = this.info["current_year"];
			this.tokens.total = this.info["total"];
		},
		async searchECTS() {
			const response = await fetch(`/back/ects`);
			this.info = await response.json();
			this.ects.current_year = this.info["current_year"];
			this.ects.total = this.info["total"];
		},
		async searchUE() {
			const response = await fetch(`/back/ue_per_year`);
			this.info = await response.json();
			this.courses_a1.result = this.info["A1"]["valide"];
			this.courses_a1.total = this.info["A1"]["tente"];
			this.courses_a2.result = this.info["A2"]["valide"];
			this.courses_a2.total = this.info["A2"]["tente"];
			this.courses_a3.result = this.info["A3"]["valide"];
			this.courses_a3.total = this.info["A3"]["tente"];
		}
	},
	mounted: function() {
		this.searchSynthesis();
		this.searchTokens();
		this.searchECTS();
		this.searchUE();
	}
})

Vue.component('synthesis-skills-chart', {
	extends: VueChartJs.Radar,
	data: function() {
		return {
			skills: new Array(14).fill(0)
		}
	},
	methods: {
		async searchSkills() {
			const response = await fetch(`/back/comp_gen`);
			this.info = await response.json();
			for (var i = 1; i < 15; i++) {
				if (this.info["CG"+i] >= 0)
					this.skills[i-1] = this.info["CG"+i];
			}
			console.log(this.skills);
	        this.updateChart(); // We do not watch because not only it would recreate the chart 14 times, but it would also require using Vue.set above
		},
		createChart() {
			this.renderChart({
				labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
				datasets: [{
					label: 'Niveaux des compétences',
					backgroundColor: "#679436",
					borderColor: "#678436",
					data: this.skills
				}]
			},
			{
			    responsive: true,
			    maintainAspectRatio: false,
				scale: {
                    ticks: {
                        beginAtZero: true,
                        max: 5,
                        min: 0,
                        stepSize: 1
				    }
			    }
		    })
		},
		updateChart() {
			this._chart.destroy();
			this.createChart();
		}
	},
	mounted: function () {
		this.searchSkills();
		this.createChart();
	}
})

Vue.component('synthesis-obligations-chart', {
	extends: VueChartJs.Pie,
	data: function() {
		return {
			percentage: 0
		}
	},
	methods: {
		async searchObligations() {
			const response = await fetch(`/back/obligations`);
			this.info = await response.json();
			this.percentage = Math.round(100*this.info["percentage"]);
		},
		createChart() {
			this.renderChart({
				labels: ["Validé", "Non-validé"],
				datasets: [{
					label: 'Conditions de diplomation',
					backgroundColor: ["#679436","#d2de81"],
					data: [this.percentage,100-this.percentage]
				}]
			}, {responsive: true, maintainAspectRatio: false})
		},
		updateChart() {
			this._chart.destroy();
			this.createChart();
		}
	},
	mounted: function () {
		this.searchObligations();
		this.createChart();
	},
	watch: {
	    percentage() {
	        this.updateChart();
	    }
	}
})
