Vue.component('skills', {
	template: `
	<div class="div-margin">
		<nav class="nav-two">
			<div>
				<ul v-for="category in skills">
					<li><h3>{{ category.name }}</h3></li>
					<ul v-for="skill in category.skills">
						<li>
							<input type="radio" :id="skill" :value="skill" v-model="picked" class="navbar-selection" v-on:change="changeSkill()">
							<label :for="skill" class="navbar-selection">{{ skill }}</label>
						</li>
					</ul>
				</ul>
			</div>
		</nav>
		<div style="margin-left: 200px;">
			<h1>{{ picked }} - {{ name }}</h1>
			<table id="skills-table">
				<tbody>
					<td>
						<h3>Description :</h3>
						<p>{{ description }}</p>
					</td>
					<td><skill-levels-chart :code="picked" :data="data" style="height: 200px;"/></td>
				</tbody>
			</table>
			<skill-details-table :code="picked" />
		</div>
	</div>
	`,
	data: function() {
		return {
			picked: "CSG1",
			name: "S'engager",
			description: "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.",
			data: [1,2,1,2,1]
		}
	},
	methods: {
		searchSkills() {
			//const response = await fetch(`/back/actor/${this.actorName}/${this.actorSurname}`);
			this.skills = [
				{
					name : 'Compétences générales',
					skills: ['CSG1', 'CSG2', 'CSG3']
				},
				{
					name : 'Compétences techniques',
					skills: ['CST1','CST2']
				}
			]
		},
		changeSkill() {
			//const response = await fetch(`/back/actor/${this.actorName}/${this.actorSurname}`);
			this.name = 'Coordonner une équipe';
			this.description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
			this.data = [2,1,2,3,5];
		}
	},
	created: function() {
		this.searchSkills();
	}
})

Vue.component('skill-levels-chart', {
	extends: VueChartJs.Bar,
	props: ["code", "data"],
	methods: {
		createChart() {
			this.renderChart({
				labels: ["Niveau 1", "Niveau 2", "Niveau 3", "Niveau 4", "Niveau 5"],
				datasets: [{
					label: this.code,
					backgroundColor: "#d2de81",
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
	    code() {
	        this.updateChart();
	    },
	    data() {
	        this.updateChart();
	        console.log(this.data);
	    }
	}
})

Vue.component('skill-details-table', {
	props: ["code"],
	template: `
	<table id="skill-details-table" class="info-table">
		<thead>
			<th>UE</th>
			<th>Période</th>
			<th>Niveau</th>
			<th>Jetons</th>
			<th>Evaluation</th>
		</thead>
		<tbody v-for="row in details">
			<tr>
				<td>{{ row.ue }}</td>
				<td>{{ row.period }}</td>
				<td>{{ row.level }}</td>
				<td>{{ row.tokens }}</td>
				<td>{{ row.eval }}</td>
			</tr>
		</tbody>
	</table>
	`,
	methods: {
		searchDetails() {
			//const response = await fetch(`/back/actor/${this.actorName}/${this.actorSurname}`);
			this.details = [
				{
					ue : 'APSA',
					period : 'A1S1',
					level : '3',
					tokens: '3',
					eval: '='
				},
				{
					ue : 'LV1',
					period : 'A1S1',
					level : '3',
					tokens: '3',
					eval: '+'
				},
				{
					ue : 'MPO',
					period : 'A1S2',
					level : '2',
					tokens: '3',
					eval: '='
				}
			]			
		}	
	},
	created: function() {
		this.searchDetails();
	}
})
