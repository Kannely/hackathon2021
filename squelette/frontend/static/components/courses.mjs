Vue.component('courses', {
	template: `
	<div class="div-margin">
		<nav class="nav-two">
			<div>
				<ul v-for="slot in courses">
					<li><h3>Créneau {{ slot[0] }}</h3></li>
					<ul v-for="course in slot[1]">
						<li>
							<input type="radio" :id="course[0]" :value="course[0]" v-model="picked" class="navbar-selection" v-on:change="changeCourse()">
							<label :for="course[0]" class="navbar-selection">{{ course[0] }}</label>
						</li>
					</ul>
				</ul>
			</div>
		</nav>
		<div style="margin-left: 200px;">
			<h1>{{ picked }} - {{ name }}</h1>
			<h3>Description :</h3>
			<p>{{ description }}</p>
			<h3>Responsable : <span class="normal">{{ teacher }}</span></h3>
			<course-table :code="picked" />
		</div>
	</div>
	`,
	data: function() {
		return {
			picked: "APSA",
			name: 'Activité Physique, Sportive et Artistique',
			description: 'Plein de sports sympas pour digérer la galette',
			teacher: 'Nathalie MARSCHAL',
			period: 'A1S1',
			grade: 'B',
			tokens: '5/6',
			ects: '1/1',
			skills: [
				{
					'name': 'CG1',
					'level': 2,
					'tokens': '1/2',
					'eval': '='
				},
				{
					'name': 'CG1',
					'level': 3,
					'tokens': '2/2',
					'eval': '+'
				}
			],
			courses: new Map([
				['A', [[2,false,false], [4,true,true]]],
				['B', [[1,false,false], [1,true,false]]]
			])
		}
	},
	methods: {
		async searchCourses() {
			const response = await fetch(`/back/ue_list`);
			this.info = await response.json();
			for (var i = 0; i < this.info.length; i++) {
				var slot = this.info[i].creneau;
				var courses_slot = [];
				if (this.courses.has(slot)) {
					courses_slot = this.courses.get(slot);
					courses_slot.push([this.info[i].code, this.info[i].termine, this.info[i].en_cours]);
					this.courses.set(slot, courses_slot);
				} else {
					this.courses.set(slot, [[this.info[i].code, this.info[i].termine, this.info[i].en_cours]]);
				}				
			}
		},
		changeCourse() {
			//const response = await fetch(`/back/actor/${this.actorName}/${this.actorSurname}`);
			//this.info = await response.json();
			this.name = 'Hackathon';
			this.description = 'On va vous en mettre plein la vue !';
			this.teacher = 'Hervé GRALL';
		}
	},
	mounted: function() {
		this.searchCourses();
	},
	watch: {
		skills() {

		}
	}
})

Vue.component('course-levels-chart', {
	extends: VueChartJs.Bar,
	props: ["code", "data"],
	methods: {
		createChart() {
			this.renderChart({
				labels: ["Niveau 1", "Niveau 2", "Niveau 3", "Niveau 4", "Niveau 5"],
				datasets: [{
					label: this.code,
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
	mounted: function () {
		this.createChart();
	},
	watch: {
	    code() {
	        this.updateChart();
	    },
	    data() {
	        this.updateChart();
	    }
	}
})

Vue.component('course-table', {
	props: ["code"],
	template: `
	<div>
		<table id="course-details-table">
			<tbody>
				<tr>
					<td>Période : {{ details.period }}</td>
					<td>Grade : {{ details.grade }}</td>
					<td>
						<tr>Jetons : {{ details.tokens }}</tr>
						<tr>ECTS : {{ details.ects }}</tr>
					</td>
				</tr>
			</tbody>
		</table>
		<table id="course-skills-table" class="info-table">
			<thead>
				<th>Compétence</th>
				<th>Niveau</th>
				<th>Jetons</th>
				<th>Evaluation</th>
			</thead>
			<tbody v-for="row in details.skills">
				<tr>
					<td>{{ row.name }}</td>
					<td>{{ row.level }}</td>
					<td>{{ row.tokens }}</td>
					<td>{{ row.eval }}</td>
				</tr>
			</tbody>
		</table>
	</div>
	`,
	methods: {
		searchDetails() {
			//const response = await fetch(`/back/actor/${this.actorName}/${this.actorSurname}`);
			this.details = {
				period: 'A2S2',
				grade: 'C',
				tokens: '3/3',
				ects: '4/5',
				skills: [
					{
						name : 'CSG1',
						level : '3',
						tokens: '3',
						eval: '='
					},
					{
						name : 'CSG3',
						level : '3',
						tokens: '3',
						eval: '+'
					},
					{
						name : 'CST1',
						level : '2',
						tokens: '3',
						eval: '='
					}
				]
			}		
		}	
	},
	mounted: function() {
		this.searchDetails();
	}
})
