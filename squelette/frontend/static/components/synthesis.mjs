Vue.component('synthesis', {
	template:`
		<div>
			<table id="synthesis-table">
				<tr>
					<td>
						<img src="/static/user.png"/>
					</td>
					<td>
						<h2>{{ firstName }} {{ lastName }}</h2>
						<h4>Campus : {{ campus }}</h4>
						<h4>{{ formation }}</h4>
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
						<synthesis-skills-chart style="height: 250px" :data="comp_gen"/>
					</td>
					<td>
						<synthesis-obligations-chart style="height: 250px" :percentages="percentages"/>
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
			comp_gen: new Array(14).fill(0),
			percentages: new Array(2).fill(0)
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
		},
		async searchCG() {
			//const response = await fetch(`/back/comp_gen`);
			//this.info = await response.json();
			for (var i = 1; i < 15; i++) {
				//if (this.info["CG"+i] >= 0)
					this.comp_gen[i-1] = Math.abs(Math.random()*5);
					//this.comp_gen[i] = this.info["CG"+i];
			}
		},
		async searchObligations() {
			this.percentages = [30,70];
		}
	},
	created: function() {
		this.searchSynthesis();
		this.searchTokens();
		this.searchECTS();
		this.searchUE();
		this.searchCG();
		this.searchObligations();
	}
})

Vue.component('synthesis-skills-chart', {
	extends: VueChartJs.Bar,
	props: ["data"],
	methods: {
		createChart() {
			this.renderChart({
				labels: [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
				datasets: [{
					label: 'Niveaux des compétences',
					backgroundColor: "blue",
					data: this.data
				}]
			}, {responsive: true, maintainAspectRatio: false})
		},
		updateChart() {
			this._chart.destroy();
			this.createChart();
		}
	},
	mounted () {
		this.createChart();
	},
	watch: {
		data() {
			this.updateChart();
		}
	}
})

Vue.component('synthesis-obligations-chart', {
	extends: VueChartJs.Pie,
	props: ["percentages"],
	methods: {
		createChart() {
			this.renderChart({
				labels: ["Validé", "Non-validé"],
				datasets: [{
					label: 'Conditions de diplomation',
					backgroundColor: ["lightblue","blue"],
					data: this.percentages
				}]
			}, {responsive: true, maintainAspectRatio: false})
		},
		updateChart() {
			this._chart.destroy();
			this.createChart();
		}
	},
	mounted () {
		this.createChart();
	},
	watch: {
	    code() {
	        this.updateChart();
	    }
	}
})