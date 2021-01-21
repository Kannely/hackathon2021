Vue.component('courses', {
	template: `
	<div class="div-margin">
		<nav class="nav-two">
			<div>
				<ul v-for="(slot_courses, slot) in sorted_courses">
					<li><h3>Créneau {{ slot }}</h3></li>
					<ul v-for="course in slot_courses">
						<li>
							<input type="radio" :id="course.code" :value="course.code" v-model="selected_course" class="navbar-selection" @change="updateCourse()">
							<label :for="course.code" class="navbar-selection">{{ course.code }}</label>
						</li>
					</ul>
				</ul>
			</div>
		</nav>
		<div style="margin-left: 200px;">
			<h1>{{ selected_course }} - {{ selected_course_data.name }}</h1>
			<h3>Description :</h3>
			<p>{{ selected_course_data.description }}</p>
			<h3>Responsable : <span class="normal">{{ selected_course_data.teacher }}</span></h3>
			<course-table :code="selected_course" />
		</div>
	</div>
	`,
	data: function() {
		return {
			courses: [
				/*{ 
				    code: '1',
				    slot: 'A',
				    in_progress: false,
				    done: false,
			    },*/
			],
			selected_course: "APSA",
			selected_course_data: {
    			name: 'Activité Physique, Sportive et Artistique',
			    description: 'Plein de sports sympas pour digérer la galette',
			    teacher: 'Nathalie MARSCHAL',
			    period: 'A1S1',
			    grade: 'B',
			    tokens: '5/6',
			    ects: '1/1',
			    skills: [
				    {
					    name: 'CG1',
					    level: 2,
					    tokens: '1/2',
					    eval: '='
				    },
				    {
					    name: 'CG1',
					    level: 3,
					    tokens: '2/2',
					    eval: '+'
				    }
			    ],
			}
		}
	},
	computed: {
	    sorted_courses() {
	        let sorted_courses = {};
	        for (const course of this.courses) {
	            if (!sorted_courses[course.slot]) sorted_courses[course.slot] = [];
	            let copied_course = {...course}; // Deep copy
	            delete copied_course.slot;
	            sorted_courses[course.slot].push(copied_course);
	        }
	        return sorted_courses;
	    }
	},
	methods: {
		async searchCourses() {
			const response = await fetch(`/back/ue_list`);
			this.info = await response.json();
			for (let i = 0; i < this.info.length; i++) {
				const info_course = this.info[i];
				const new_course = {
				    code: info_course.code,
				    slot: info_course.creneau,
				    in_progress: info_course.en_cours,
				    done: info_course.termine
				};
				const course_index = this.courses.findIndex(c => c.code == info_course.code);
				if (course_index > -1) Vue.set(this.courses, course_index, new_course);
				else this.courses.push(new_course);			
			}
		},
		updateCourse() {
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
	mounted () {
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
	data: function() {
	    return {
	        details: {}
	    };
	},
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
