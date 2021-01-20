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
								<p>13/13 UEs validées</p>
								<h4>TAF {{ tafA2 }}</h4>
								<p>6/12 UEs validées</p>
								<h4>TAF {{ tafA3 }}</h4>
								<p>-</p>
							</td>
							<td>
								<h4>Année en cours</h4>
								<p>108 jetons</p>
								<p>20 ECTS</p>
								<h4>Total</h4>
								<p>300 jetons</p>
								<p>200 ECTS</p>
							</td>
						</table>
					</td>
				</tr>
			</table>
			<table id="synthesis-graph-table">
				<tr>
					<td>
						<synthesis-skills-chart style="height: 250px"/>
					</td>
					<td>
						<synthesis-obligations-chart style="height: 250px"/>
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
		}
	},
	methods: {
		async searchInfo() {
			const response = await fetch(`/back/synthesis`);
			this.info = await response.json();
			this.lastName = this.info["nom"];
			this.firstName = this.info["prenom"];
			this.campus = this.info["campus"];
			this.tafA2 = this.info["tafA2"];
			this.tafA3 = this.info["tafA3"];
			this.formation = this.info["formation"];
		}	
	},
	created: function() {
		this.searchInfo();
	}
})

Vue.component('synthesis-skills-chart', {
	extends: VueChartJs.Radar,
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
			labels: ["Validé","Non-validé"],
			datasets: [{
				label: 'Conditions de diplomation',
				backgroundColor: ["lightblue","blue"],
				data: [70,30]
			}]
		}, {responsive: true, maintainAspectRatio: false})
	}
})